import pandas as pd


def is_strong_impulse(df, start_idx, end_idx, is_bullish):
    """Проверка силы импульса"""
    candles = df.iloc[start_idx:end_idx]
    if is_bullish:
        return (candles['close'].iloc[-1] > candles['open'].iloc[0] * 1.008) and len(candles) >= 3
    else:
        return (candles['close'].iloc[-1] < candles['open'].iloc[0] * 0.992) and len(candles) >= 3


def detect_fvg(df: pd.DataFrame):
    """Улучшенное обнаружение FVG"""
    fvgs = []
    for i in range(2, len(df)):
        # Bullish FVG
        if df['low'].iloc[i] > df['high'].iloc[i - 2]:
            fvg_low = df['high'].iloc[i - 2]
            fvg_high = df['low'].iloc[i]
            size_pct = (fvg_high - fvg_low) / fvg_low * 100

            if size_pct >= 0.08:  # фильтр размера
                fvgs.append({
                    'type': 'Bullish FVG',
                    'index': i,
                    'low': fvg_low,
                    'high': fvg_high,
                    'size_pct': size_pct,
                    'mitigation': False
                })

        # Bearish FVG
        elif df['high'].iloc[i] < df['low'].iloc[i - 2]:
            fvg_low = df['high'].iloc[i]
            fvg_high = df['low'].iloc[i - 2]
            size_pct = (fvg_high - fvg_low) / fvg_low * 100

            if size_pct >= 0.08:
                fvgs.append({
                    'type': 'Bearish FVG',
                    'index': i,
                    'low': fvg_low,
                    'high': fvg_high,
                    'size_pct': size_pct,
                    'mitigation': False
                })
    return fvgs


def detect_super_ob(df: pd.DataFrame, fvg_idx: int, is_bullish: bool):
    """Улучшенное определение Super Order Block"""
    lookback = 12
    start = max(0, fvg_idx - lookback)

    best_ob = None
    best_strength = 0

    for i in range(start, fvg_idx - 1):
        if is_bullish and df['close'].iloc[i] < df['open'].iloc[i]:  # bearish candle (для лонга)
            impulse_strength = df['high'].iloc[i + 1:i + 5].max() - df['low'].iloc[i]
            if impulse_strength > best_strength:
                best_strength = impulse_strength
                best_ob = {
                    'type': 'Bullish Super OB',
                    'low': df['low'].iloc[i] * 0.999,
                    'high': df['high'].iloc[i] * 1.001,
                    'index': i
                }

        elif not is_bullish and df['close'].iloc[i] > df['open'].iloc[i]:  # bullish candle (для шорта)
            impulse_strength = df['high'].iloc[i] - df['low'].iloc[i + 1:i + 5].min()
            if impulse_strength > best_strength:
                best_strength = impulse_strength
                best_ob = {
                    'type': 'Bearish Super OB',
                    'low': df['low'].iloc[i] * 0.999,
                    'high': df['high'].iloc[i] * 1.001,
                    'index': i
                }

    return best_ob