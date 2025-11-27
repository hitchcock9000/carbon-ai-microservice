import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def verify():
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")
    
    if not token or not repo:
        print("MISSING_CREDENTIALS")
        return

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
    if response.status_code == 200:
        print(f"SUCCESS: Connected to {repo}")
    else:
        print(f"FAILURE: {response.status_code} - {response.text}")

if __name__ == "__main__":
    asyncio.run(verify())
