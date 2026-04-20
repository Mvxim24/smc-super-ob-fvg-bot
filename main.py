import os
import sys
import asyncio

print("=== БОТ НАЧИНАЕТ ЗАПУСК ===")
print(f"Python version: {sys.version}")

# --- ВСТАВЬТЕ ВАШИ ДАННЫЕ ТУТ ---
BOT_TOKEN = "8548326510:AAEZh6U0xOhBdV_uZ-5Wd8cTjSand-YYUes"
CHAT_ID = "8548326510"
# -------------------------------

print(f"BOT_TOKEN: {'✅ Прописан' if len(BOT_TOKEN) > 20 else '❌ ОШИБКА В ТОКЕНЕ'}")
print(f"CHAT_ID: {'✅ Прописан' if CHAT_ID else '❌ НЕ НАЙДЕН'}")

if not BOT_TOKEN or "ВАШ_" in BOT_TOKEN:
    print("❌ ОШИБКА: Вы не заменили шаблон на реальный BOT_TOKEN!")
    sys.exit(1)

print("✅ Данные встроены в код")
print("🤖 Бот должен работать...")

async def main():
    print("✅ Асинхронный запуск прошёл успешно")
    while True:
        print(f"[{asyncio.get_event_loop().time():.0f}] Бот живой...")
        await asyncio.sleep(30)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
