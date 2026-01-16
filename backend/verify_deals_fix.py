
import asyncio
import httpx
import uuid
import random
import string
import sys
import os

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from app.db.session import AsyncSessionLocal
from app.models.tenant import Tenant
from app.models.user import User, UserRole
from app.models.website import Website
from app.models.contact import Contact
from app.models.form import Form
from app.models.form_field import FormField
from app.models.deal import Deal
from app.models.activity import Activity
from app.core.security import get_password_hash

BASE_URL = "http://localhost:8000"

def random_str(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

async def seed_db():
    print("🌱 Seeding Database locally...")
    async with AsyncSessionLocal() as db:
        try:
            # 1. Tenant
            slug = f"seed_{random_str()}"
            tenant = Tenant(
                name="Seed Corp",
                slug=slug
            )
            db.add(tenant)
            await db.flush() # get ID
            
            # 2. User
            email = f"admin_{random_str()}@seed.com"
            password = "Password123!"
            user = User(
                email=email,
                password_hash=get_password_hash(password),
                full_name="Seed Admin",
                role=UserRole.ADMIN,
                tenant_id=tenant.id
            )
            db.add(user)
            
            # 3. Website
            website = Website(
                domain=f"{slug}.com",
                name="Seed Site",
                tenant_id=tenant.id,
                tracking_id=f"TRK-{random_str()}"
            )
            db.add(website)
            await db.flush() # get ID
            
            # 4. Contact
            contact = Contact(
                name="Seed Contact",
                email=f"contact_{random_str()}@seed.com",
                tenant_id=tenant.id,
                website_id=website.id,
                status="new"
            )
            db.add(contact)
            
            await db.commit()
            print(f"✅ Seeding Complete. Tenant: {slug}, User: {email}")
            return slug, email, password, str(contact.id)
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Seeding Failed: {e}")
            raise e

async def verify_deals_fix():
    # 1. Seed Data
    try:
        slug, email, password, contact_id = await seed_db()
    except Exception:
        return

    async with httpx.AsyncClient() as client:
        # 2. Login
        print("🔐 Logging in...")
        login_payload = {
            "tenant_slug": slug,
            "email": email,
            "password": password
        }
        r = await client.post(f"{BASE_URL}/api/v1/auth/login", json=login_payload)
        if r.status_code != 200:
            print(f"❌ Login Failed: {r.text}")
            return
            
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Logged in")
        
        # 3. Create Deal
        print("💼 Creating Deal via API...")
        deal_payload = {
            "title": "Seeded Deal",
            "value": 10000,
            "contact_id": contact_id
        }
        r = await client.post(f"{BASE_URL}/api/v1/deals/", json=deal_payload, headers=headers)
        if r.status_code != 200:
            print(f"❌ Create Deal Failed: {r.text}")
            return
        deal_id = r.json()["id"]
        stage = r.json()["stage"]
        print(f"✅ Deal Created: {deal_id} (Stage: {stage})")
        
        # 4. Update Deal Stage
        print("🚀 Updating Deal Stage via PUT Endpoint...")
        update_payload = {"stage": "proposal"}
        r = await client.put(f"{BASE_URL}/api/v1/deals/{deal_id}/stage", json=update_payload, headers=headers)
        
        if r.status_code == 200:
            new_stage = r.json()["stage"]
            if new_stage == "proposal":
                print(f"✅ SUCCESS: Deal Stage updated to '{new_stage}'")
            else:
                print(f"⚠️ Warning: Response 200 but stage is '{new_stage}'")
        else:
            print(f"❌ Update Failed: {r.status_code} - {r.text}")
            
if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_deals_fix())
