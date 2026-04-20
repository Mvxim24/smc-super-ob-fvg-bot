import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

# --- Токен ---
BOT_TOKEN = "8548326510:AAGV7zU_kGL3scX6xGgU9BehGqTLjgSwSzI"
# ------------

print("=== БОТ НАЧИНАЕТ ЗАПУСК ===")
print(f"Python version: {sys.version}")
print(f"BOT_TOKEN: {'✅ Прописан' if len(BOT_TOKEN) > 30 else '❌ ОШИБКА'}")

if len(BOT_TOKEN) < 30:
    print("❌ ОШИБКА: Токен выглядит неверно!")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message()
async def echo(message: Message):
    await message.answer(f"Получил: {message.text}")

async def main():
    print("✅ Асинхронный запуск прошёл успешно")
    print("🤖 Бот подключается к Telegram...")
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Вебхук удалён, начинаем polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен вручную")
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        raise
