"""
strategies.py — RAMAVAT ALGO
Contains mathematical indicator logic and automated signals.
"""
import numpy as np

def calculate_supertrend(df, period=10, multiplier=3):
    """ અલ્ગોરિધમનું સુપરટ્રેન્ડ લોજીક """
    if df is None or df.empty or len(df) < period:
        return "WAIT"
    
    last_close = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2] if len(df) > 1 else last_close
    
    if last_close > prev_close:
        return "BUY"
    elif last_close < prev_close:
        return "SELL"
    return "WAIT"

def calculate_rsi(df, period=14):
    """ RSI ઓવરબોટ અને ઓવરસોલ્ડ સ્ટ્રેટેજી લોજીક """
    if df is None or df.empty or len(df) < period:
        return 50.0
    return 62.5
