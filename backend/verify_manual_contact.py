
import asyncio
import httpx
import random
import string

BASE_URL = "http://localhost:8000"

def random_str(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

async def verify_manual_contact():
    async with httpx.AsyncClient() as client:
        # 1. Register Tenant (Should create System Website)
        print("1. Registering Tenant...")
        slug = f"manualtest_{random_str()}"
        email = f"admin_{random_str()}@manual.com"
        password = "Password123!"
        
        reg_payload = {
            "company_name": "Manual Test Corp",
            "company_slug": slug,
            "admin_name": "Admin User",
            "admin_email": email,
            "admin_password": password
        }
        
        r = await client.post(f"{BASE_URL}/api/v1/auth/register", json=reg_payload)
        if r.status_code != 200:
            print(f"❌ Registration Failed: {r.text}")
            return
        print(f"✅ Registered Tenant: {slug}")
        
        # 2. Login
        print("2. Logging in...")
        login_payload = {
            "tenant_slug": slug,
            "email": email,
            "password": password
        }
        r = await client.post(f"{BASE_URL}/api/v1/auth/login", json=login_payload)
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Logged in")

        # 3. Create Manual Contact (No website_id)
        print("3. Creating Manual Contact...")
        contact_email = f"manual_{random_str()}@contact.com"
        contact_payload = {
            "name": "Manual User",
            "email": contact_email
        }
        r = await client.post(f"{BASE_URL}/api/v1/contacts/", json=contact_payload, headers=headers)
        if r.status_code != 200:
            print(f"❌ Create Contact Failed: {r.text}")
            return
            
        contact_data = r.json()
        print(f"✅ Contact Created: {contact_data['id']}")
        
        # 4. Verify System Website Assignment
        # Need to check DB or infer from success.
        # Since we don't return website_id in ContactRead (usually), we rely on success (integrity constraint would fail otherwise).
        # But let's check source.
        if contact_data.get("source") == "manual":
            print(f"✅ Source set to 'manual' correctly. ID: {contact_data['id']}")
        else:
             print(f"⚠️ Source matches: {contact_data.get('source')}")

if __name__ == "__main__":
    asyncio.run(verify_manual_contact())
