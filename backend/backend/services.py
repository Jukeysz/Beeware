from datetime import datetime, timedelta, timezone

import httpx

from backend.settings import Settings

igdb_token_info = {"token": None, "expires_at": datetime.now(timezone.utc)}


async def post_to_igdb_token():
    igdb_baseurl = 'https://id.twitch.tv/oauth2/token'
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{igdb_baseurl}?client_id={Settings().IGDB_CLIENT_ID}&client_secret={Settings().IGDB_CLIENT_SECRET}&grant_type=client_credentials")

        response.raise_for_status()
        data = response.json()
        igdb_token_info['token'] = data['access_token']
        now = datetime.now(timezone.utc)
        diff = timedelta(seconds=data["expires_in"])
        igdb_token_info["expires_at"] = now + diff
        return data


async def get_igdb_token():
    expired = igdb_token_info["expires_at"] <= datetime.now(timezone.utc)
    if igdb_token_info["token"] is None or expired:
        await post_to_igdb_token()

    return igdb_token_info["token"]
