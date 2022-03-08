import asyncio
from dotenv import load_dotenv
import json
import os
from telethon import TelegramClient

load_dotenv()

# Use your own values from my.telegram.org
APP_ID = os.getenv("TELEGRAM_APP_ID")
HASH_ID = os.getenv("TELEGRAM_HASH_ID")

TARGET_CHAT = os.getenv("TELEGRAM_TARGET_CHAT")

# read data from json
try:
    with open("data.json", "r") as json_file:
        data = json.load(json_file)
except:
    data = {"items": [], "min_id": 0}


async def main():
    # The first parameter is the .session file name (absolute paths allowed)
    client = TelegramClient(".tele", APP_ID, HASH_ID)
    await client.start()
    messages = client.iter_messages(TARGET_CHAT, min_id=data["min_id"])
    is_first = True
    new_songs = 0
    async for message in messages:
        if is_first:
            data["min_id"] = message.id
            is_first = False

        if not hasattr(message, "media"):
            continue

        document = getattr(message.media, "document", None)
        if not document:
            continue

        if document.mime_type in ("audio/mpeg", "audio/m4a", "audio/mp4"):

            # for handling files
            if not hasattr(document.attributes[0], "title"):
                title = document.attributes[0].file_name.strip(".mp3,.m4a")
            else:
                title = document.attributes[0].title

            splits = (
                title.split("-")
                if "-" in title
                else (document.attributes[0].performer, title)
            )
            artist, song = splits[0].strip(), splits[1].strip()

            new_item = {"song": song, "artist": artist}
            if new_item not in data["items"]:
                print("> new song found:", new_item)
                data["items"].append(new_item)
                new_songs += 1
            else:
                print(">>> duplicate: ", new_item)

    if new_songs:
        with open("data.json", "w") as outfile:
            json.dump(data, outfile, indent=4)
            print(f"{new_songs} New songs added to data.json")
    else:
        print("No new songs")

    await client.disconnect()


asyncio.run(main())
