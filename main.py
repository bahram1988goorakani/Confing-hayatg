import os
import re
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = os.getenv("STRING_SESSION")
target = os.getenv("TARGET_CHANNEL")

# فقط کانال واقعی و درست
channels = [
    "@Farah_VPN"
]

patterns = [
    r"vmess://[^\s]+",
    r"vless://[^\s]+",
    r"trojan://[^\s]+",
    r"ss://[^\s]+"
]

client = TelegramClient(
    StringSession(session),
    api_id,
    api_hash
)

async def main():
    for ch in channels:
        try:
            async for msg in client.iter_messages(ch, limit=20):
                if msg.message:
                    for p in patterns:
                        for config in re.findall(p, msg.message):
                            await client.send_message(target, config)
        except Exception as e:
            print(f"Error in channel {ch}: {e}")

with client:
    client.loop.run_until_complete(main())
