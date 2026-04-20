import os
import sys
import asyncio
from dotenv import load_dotenv

print("=== БОТ НАЧИНАЕТ ЗАПУСК ===")
print(f"Python version: {sys.version}")

# Загружаем .env
load_dotenv()
print("✅ .env загружен")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(f"BOT_TOKEN: {'✅ Есть' if BOT_TOKEN and len(BOT_TOKEN) > 20 else '❌ НЕ НАЙДЕН'}")
print(f"CHAT_ID: {'✅ Есть' if CHAT_ID else '❌ НЕ НАЙДЕН'}")

if not BOT_TOKEN or not CHAT_ID:
    print("❌ ОШИБКА: BOT_TOKEN или CHAT_ID отсутствуют!")
    sys.exit(1)

print("✅ Все переменные окружения на месте")
print("🤖 Бот должен работать...")

# Простой тестовый запуск
async def main():
    print("✅ Асинхронный запуск прошёл успешно")
    while True:
        print(f"[{asyncio.get_event_loop().time():.0f}] Бот живой...")
        await asyncio.sleep(30)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
