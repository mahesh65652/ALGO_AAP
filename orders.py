"""
orders.py — RAMAVAT ALGO
Handles order execution and punching logic for brokers.
"""

def place_market_order(broker_name, symbol, quantity, transaction_type):
    """
    જ્યારે BUY કે SELL ક્લિક થાય ત્યારે બ્રોકરના ટર્મિનલ પર ઓર્ડર મોકલવાનું લોજીક.
    """
    if broker_name == "None (Disconnected)":
        return False, "❌ ઓર્ડર ફેલ: પહેલા બ્રોકર લોગિન કરો!"
        
    # ઓર્ડર પ્લેસમેન્ટ મોક રિસ્પોન્સ
    return True, f"🚀 {transaction_type} ઓર્ડર સફળ! {quantity} ક્વોન્ટિટી {symbol} માટે {broker_name} માં પંચ થઈ ગઈ છે."
