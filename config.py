from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Основные настройки
SYMBOLS = ["BTCUSDT", "ETHUSDT"]
TIMEFRAMES = ["15m", "1h", "4h"]

SCAN_INTERVAL_SECONDS = 240   # каждые 4 минуты

# Фильтры качества сигнала
MIN_FVG_SIZE_PCT = 0.08      # минимальный размер FVG в %
MIN_IMPULSE_CANDLES = 3      # минимум свечей сильного импульса
RR_MIN = 2.0