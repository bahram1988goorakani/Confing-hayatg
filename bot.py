import os
import re
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# دریافت اطلاعات از Secrets گیت‌هاب
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("STRING_SESSION")
TARGET = os.getenv("TARGET_CHANNEL")

# اگر TARGET عددی است، آن را به int تبدیل می‌کنیم (مخصوص آیدی‌های -100...)
if TARGET and TARGET.lstrip('-').isdigit():
    TARGET = int(TARGET)

# لیست کانال‌های سورس
SOURCE_CHANNELS = [
    "@oneclickvpnkeys",
    "@ConfigX2ray",
    "@Farah_VPN"
]

# الگوهای پیدا کردن کانفیگ
PATTERNS = [
    r"vmess://[^\s]+",
    r"vless://[^\s]+",
    r"trojan://[^\s]+",
    r"ss://[^\s]+"
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def main():
    await client.start()
    print("Bot started...")
    
    all_configs = []

    # خواندن کانفیگ‌ها
    for channel in SOURCE_CHANNELS:
        print(f"Checking {channel}...")
        try:
            async for msg in client.iter_messages(channel, limit=10):
                if msg.message:
                    for pattern in PATTERNS:
                        matches = re.findall(pattern, msg.message)
                        all_configs.extend(matches)
        except Exception as e:
            print(f"Error reading {channel}: {e}")

    # حذف تکراری‌ها و محدود کردن به ۵ عدد
    unique_configs = list(set(all_configs))[:5]
    
    if not unique_configs:
        print("No configs found.")
        return

    # ارسال به کانال مقصد
    print(f"Sending {len(unique_configs)} configs to {TARGET}...")
    for config in unique_configs:
        try:
            await client.send_message(TARGET, f"🚀 New Config:\n\n`{config}`")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"Send error: {e}")

    print("Task completed.")

with client:
    client.loop.run_until_complete(main())
