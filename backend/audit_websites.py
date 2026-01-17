
import asyncio
import uuid
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.abspath("d:/Inyutek/newcrm/CRM/backend"))

from app.db.session import AsyncSessionLocal
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

async def run_test():
    async with AsyncSessionLocal() as db:
        try:
            print("--- Starting Database Integrity Audit for Websites (Raw SQL) ---")

            # 1. Setup Test Tenants
            tenant1_id = str(uuid.uuid4())
            tenant2_id = str(uuid.uuid4())
            
            # Create dummy tenants
            try:
                await db.execute(text("INSERT INTO tenant (id, name, slug, created_at, updated_at, is_active) VALUES (:id, :name, :slug, NOW(), NOW(), TRUE)"), {"id": tenant1_id, "name": "Audit Test Tenant 1", "slug": "audit-tenant-1"})
                await db.execute(text("INSERT INTO tenant (id, name, slug, created_at, updated_at, is_active) VALUES (:id, :name, :slug, NOW(), NOW(), TRUE)"), {"id": tenant2_id, "name": "Audit Test Tenant 2", "slug": "audit-tenant-2"})
                await db.commit()
                print("[PASS] Created Test Tenants")
            except Exception as e:
                 print(f"[WARN] Tenant creation failed: {e}")
                 await db.rollback()
                 return # Cannot proceed if tenants fail

            domain_test = "integrity-test.com"

            # 2. Test Case 1: Create Website for Tenant 1
            print("\n[TEST 1] Create 'integrity-test.com' for Tenant 1")
            web1_id = str(uuid.uuid4())
            try:
                await db.execute(text("""
                    INSERT INTO website (id, domain, name, tracking_id, tenant_id, is_active, is_system, created_at)
                    VALUES (:id, :domain, 'Test Site 1', 'TRK-TEST-1', :tenant_id, TRUE, FALSE, NOW())
                """), {"id": web1_id, "domain": domain_test, "tenant_id": tenant1_id})
                await db.commit()
                print(f"[PASS] Successfully created website {web1_id}")
            except Exception as e:
                print(f"[FAIL] Failed to create initial website: {e}")
                await db.rollback()

            # 3. Test Case 2: Create Duplicate 'integrity-test.com' for Tenant 1 (SHOULD FAIL)
            print("\n[TEST 2] Create DUPLICATE 'integrity-test.com' for Tenant 1")
            web2_id = str(uuid.uuid4())
            try:
                await db.execute(text("""
                    INSERT INTO website (id, domain, name, tracking_id, tenant_id, is_active, is_system, created_at)
                    VALUES (:id, :domain, 'Test Site Duplicate', 'TRK-TEST-2', :tenant_id, TRUE, FALSE, NOW())
                """), {"id": web2_id, "domain": domain_test, "tenant_id": tenant1_id})
                await db.commit()
                print("[FAIL] Database allowed duplicate domain for same tenant!")
            except IntegrityError as e:
                await db.rollback()
                print(f"[PASS] Database correctly rejected duplicate.")
            except Exception as e:
                await db.rollback()
                print(f"[WARN] Unexpected error during duplicate check: {e}")


            # 4. Test Case 3: Create 'integrity-test.com' for Tenant 2 (SHOULD PASS)
            print("\n[TEST 3] Create 'integrity-test.com' for Tenant 2")
            web3_id = str(uuid.uuid4())
            try:
                await db.execute(text("""
                    INSERT INTO website (id, domain, name, tracking_id, tenant_id, is_active, is_system, created_at)
                    VALUES (:id, :domain, 'Test Site Tenant 2', 'TRK-TEST-3', :tenant_id, TRUE, FALSE, NOW())
                """), {"id": web3_id, "domain": domain_test, "tenant_id": tenant2_id})
                await db.commit()
                print(f"[PASS] Database correctly allowed same domain for different tenant.")
            except IntegrityError as e:
                await db.rollback()
                print(f"[FAIL] Database incorrectly rejected same domain for different tenant: {e}")
            except Exception as e:
                await db.rollback()
                print(f"[FAIL] Unexpected error for Tenant 2 insert: {e}")

            # 5. Clean up
            print("\n[CLEANUP] Removing test data...")
            await db.execute(text("DELETE FROM website WHERE domain = :domain"), {"domain": domain_test})
            await db.execute(text("DELETE FROM tenant WHERE id IN (:t1, :t2)"), {"t1": tenant1_id, "t2": tenant2_id})
            await db.commit()
            print("[DONE] Audit Complete.")

        except Exception as e:
            print(f"\n[CRITICAL ERROR] Script failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_test())

