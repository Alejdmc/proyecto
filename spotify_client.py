import httpx
import base64
import asyncio

SPOTIFY_CLIENT_ID = "b525d3400c074caaae9309e1f4a83dd6"
SPOTIFY_CLIENT_SECRET = "ba393364a02c48bd96f883c8b08523ea"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

access_token = None

async def get_access_token():
    global access_token
    creds = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded_creds = base64.b64encode(creds.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_creds}", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data['access_token']

async def spotify_search(query: str, type_: str):
    global access_token
    if not access_token:
        await get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPOTIFY_BASE_URL}/search", params={"q": query, "type": type_}, headers=headers)
        if response.status_code == 401:
            await get_access_token()
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(f"{SPOTIFY_BASE_URL}/search", params={"q": query, "type": type_}, headers=headers)
        response.raise_for_status()
        return response.json()
    #a