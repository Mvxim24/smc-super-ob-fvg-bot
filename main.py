import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, CHAT_ID
from scanner import scan_market
import config

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("✅ <b>Super OB + FVG Бот запущен и готов к работе!</b>", parse_mode="HTML")

@dp.message(Command("status"))
async def status(message: Message):
    await message.answer(f"✅ Бот активен\nСимволов: {len(config.SYMBOLS)}\nТФ: {config.TIMEFRAMES}\nИнтервал сканирования: {config.SCAN_INTERVAL_SECONDS} сек")

@dp.message(Command("scan"))
async def manual_scan(message: Message):
    await message.answer("🔄 Запускаю ручное сканирование...")
    await scan_market(bot, CHAT_ID)
    await message.answer("✅ Сканирование завершено")

async def main():
    print("🤖 Бот успешно запущен!")
    asyncio.create_task(scanner_loop())
    await dp.start_polling(bot)

async def scanner_loop():
    while True:
        await scan_market(bot, CHAT_ID)
        await asyncio.sleep(config.SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())