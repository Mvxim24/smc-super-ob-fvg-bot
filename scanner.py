import ccxt
import pandas as pd
import asyncio
from datetime import datetime
from signals import detect_fvg, detect_super_ob
from config import SYMBOLS, TIMEFRAMES, MIN_FVG_SIZE_PCT

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'},
})

async def scan_market(bot, chat_id):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Сканирование...")

    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            try:
                bars = exchange.fetch_ohlcv(symbol, tf, limit=180)
                df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

                fvgs = detect_fvg(df)

                for fvg in fvgs[-4:]:   # последние 4 FVG
                    is_bullish = "Bullish" in fvg['type']
                    ob = detect_super_ob(df, fvg['index'], is_bullish)

                    if ob:
                        direction = "🟢 LONG" if is_bullish else "🔴 SHORT"
                        entry_zone = f"{ob['low']:.5f} — {ob['high']:.5f}"

                        message = f"""
🚨 <b>SUPER OB + FVG</b> {direction}

📊 <b>{symbol}</b> • {tf}
🔹 {ob['type']}

📍 <b>Зона входа:</b>
<code>{entry_zone}</code>

FVG: <code>{fvg['low']:.5f} — {fvg['high']:.5f}</code> ({fvg['size_pct']:.2f}%)

🕒 {datetime.now().strftime('%d.%m %H:%M')}
                        """.strip()

                        await bot.send_message(chat_id, message, parse_mode="HTML")
                        print(f"✅ Сигнал отправлен → {symbol} {tf}")
                        await asyncio.sleep(4)  # анти-спам

            except Exception as e:
                continue