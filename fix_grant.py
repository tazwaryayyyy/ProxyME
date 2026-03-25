import asyncio
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from backend.auth0_client import Auth0Client

async def patch_client_grant():
    auth0 = Auth0Client()
    print("Fetching Management Token...")
    # This will now get a token with the newly added update:client_grants scope
    # (assuming it was authorized for the M2M app)
    token = await auth0.get_management_token()
    
    if not token:
        print("Failed to get token. Check your .env AUTH0_ variables.")
        return

    # From your screenshot
    grant_id = "cgr_y8Fdkxrj3TLhAVGU"
    url = f"https://{auth0.domain}/api/v2/client-grants/{grant_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # This explicitly permits the 'proxy_me_approval' type for this client/API pair
    payload = {
        "authorization_details": [
            {
                "type": "proxy_me_approval"
            }
        ]
    }

    print(f"Fetching Grant {grant_id}...")
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ Success! Current Grant details:")
            import json
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                print(response.json())
            except:
                print(response.text)

if __name__ == "__main__":
    asyncio.run(patch_client_grant())
