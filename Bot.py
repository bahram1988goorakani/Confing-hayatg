import os
import re
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("STRING_SESSION")
TARGET = os.getenv("TARGET_CHANNEL")

# کانال‌های سورس
SOURCE_CHANNELS = [
    "@oneclickvpnkeys",
    "@ConfigX2ray",
    "@Farah_VPN"
]

# الگوهای کانفیگ
PATTERNS = [
    r"vmess://[^\s]+",
    r"vless://[^\s]+",
    r"trojan://[^\s]+",
    r"ss://[^\s]+"
]

client = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)

sent_configs = set()


async def send_config(config):
    try:
        await client.send_message(TARGET, config)
        print("SENT:", config[:30])

        # anti flood
        await asyncio.sleep(2)

    except Exception as e:
        print("SEND ERROR:", e)


async def fetch_from_channel(channel):
    found = []

    try:
        async for msg in client.iter_messages(channel, limit=20):

            if not msg.message:
                continue

            for pattern in PATTERNS:

                matches = re.findall(pattern, msg.message)

                for config in matches:

                    if config not in sent_configs:
                        sent_configs.add(config)
                        found.append(config)

    except Exception as e:
        print("CHANNEL ERROR:", channel, e)

    return found


async def main():

    all_configs = []

    for channel in SOURCE_CHANNELS:

        print("CHECKING:", channel)

        configs = await fetch_from_channel(channel)

        all_configs.extend(configs)

    # فقط 5 تا در هر اجرا
    batch = all_configs[:5]

    print("TOTAL NEW:", len(all_configs))
    print("SENDING:", len(batch))

    sent = 0

    for config in batch:

        await send_config(config)

        sent += 1

    # گزارش
    report = (
        f"📊 Report\n"
        f"Found: {len(all_configs)}\n"
        f"Sent: {sent}"
    )

    await client.send_message(TARGET, report)

    print(report)


with client:
    client.loop.run_until_complete(main())
