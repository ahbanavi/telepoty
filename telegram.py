import os
from dotenv import load_dotenv
import asyncio
from telethon import TelegramClient

# Use your own values from my.telegram.org
api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"


async def main():
    # The first parameter is the .session file name (absolute paths allowed)
    async with TelegramClient("anon", api_id, api_hash).start() as client:
        await client.send_message("me", "Hello, myself!")


asyncio.run(main())
