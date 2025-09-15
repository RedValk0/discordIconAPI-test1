from fastapi import FastAPI
import httpx
import os

app = FastAPI()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@app.get("/avatar/{user_id}")
async def get_avatar(user_id: int):
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}

    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://discord.com/api/v10/users/{user_id}", headers=headers)

    if r.status_code != 200:
        return {"error": f"Discord API error {r.status_code}"}

    data = r.json()

    avatar_hash = data.get("avatar")
    if avatar_hash:
        # gif if hash starts with "a_"
        ext = "gif" if avatar_hash.startswith("a_") else "png"
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.{ext}?size=1024"
    else:
        # default avatar
        discrim = int(data.get("discriminator", 0)) % 5
        avatar_url = f"https://cdn.discordapp.com/embed/avatars/{discrim}.png"

    return {"avatar_url": avatar_url}
