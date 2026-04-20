import ccxt
import pandas as pd
import asyncio
from datetime import datetime
from signals import detect_fvg, detect_super_ob
from config import SYMBOLS, TIMEFRAMES

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'},
})

def calculate_signal_strength(ob, fvg, df):
    """Расчёт силы сигнала (1-3 звезды)"""
    strength = 1
    reasons = []
    
    # Размер FVG
    if fvg['size_pct'] > 0.25:
        strength += 1
        reasons.append("Большой FVG")
    
    # Сила импульса
    impulse_size = abs(df['close'].iloc[ob['index']+1:ob['index']+6].mean() - df['close'].iloc[ob['index']]) / df['close'].iloc[ob['index']]
    if impulse_size > 0.003:
        strength += 1
        reasons.append("Сильный импульс")
    
    strength = min(strength, 3)
    return "★★★" if strength == 3 else "★★☆" if strength == 2 else "★☆☆", strength


async def scan_market(bot, chat_id):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Сканирование рынка...")

    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            try:
                bars = exchange.fetch_ohlcv(symbol, tf, limit=200)
                df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

                fvgs = detect_fvg(df)

                for fvg in fvgs[-5:]:
                    is_bullish = "Bullish" in fvg['type']
                    ob = detect_super_ob(df, fvg['index'], is_bullish)

                    if ob:
                        # Расчёт уровней
                        entry = (ob['low'] + ob['high']) / 2
                        
                        if is_bullish:  # LONG
                            sl = ob['low'] * 0.9985
                            risk = entry - sl
                            tp1 = entry + risk * 2.0
                            tp2 = entry + risk * 3.2
                            tp3 = entry + risk * 5.0
                            direction = "🟢 LONG"
                            emoji = "📈"
                        else:  # SHORT
                            sl = ob['high'] * 1.0015
                            risk = sl - entry
                            tp1 = entry - risk * 2.0
                            tp2 = entry - risk * 3.2
                            tp3 = entry - risk * 5.0
                            direction = "🔴 SHORT"
                            emoji = "📉"

                        rr = round((tp2 - entry) / risk if is_bullish else (entry - tp2) / risk, 1)
                        strength_stars, strength_num = calculate_signal_strength(ob, fvg, df)

                        message = f"""
🚨 <b>SUPER OB + FVG</b>
{direction} <b>{strength_stars}</b>

📊 <b>{symbol}</b> • <b>{tf}</b> {emoji}

📍 <b>Зона входа</b>
<code>{ob['low']:.4f} — {ob['high']:.4f}</code>

🛡️ <b>Stop Loss</b>
<code>{sl:.4f}</code> <i>(-{((entry-sl)/entry*100):.2f}%)</i>

🎯 <b>Take Profit</b>
TP1 <code>{tp1:.4f}</code> (1:2.0)
TP2 <code>{tp2:.4f}</code> (1:{rr})
TP3 <code>{tp3:.4f}</code> (1:5.0)

📈 <b>RR</b> 1:{rr} | <b>Сила</b> {strength_stars}

──────────────────
FVG: {fvg['size_pct']:.2f}% | Импульс: Strong
🕒 {datetime.now().strftime('%d.%m.%Y %H:%M')}
                        """.strip()

                        await bot.send_message(chat_id, message, parse_mode="HTML")
                        print(f"✅ Сигнал отправлен: {symbol} {tf} {direction}")
                        await asyncio.sleep(5)  # пауза чтобы не спамило

            except Exception as e:
                continue
