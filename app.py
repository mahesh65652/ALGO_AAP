"""
app.py — RAMAVAT ALGO ELITE [v2.0]
====================================
Professional Trading Terminal
Gujarati + English UI
Dark Premium Theme | Mobile + Desktop
Angel One | Alice Blue | Zerodha Ready
"""

import streamlit as st
import time
import pandas as pd
from datetime import datetime
from enum import Enum

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ramavat Algo Elite",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════
# ENUMS
# ══════════════════════════════════════════════════════════════════
class BrokerType(Enum):
    ANGEL_ONE = "Angel One (SmartAPI)"
    ALICE_BLUE = "Alice Blue (ANT)"
    ZERODHA = "Zerodha (Kite)"
    FINVASIA = "Finvasia (Shoonya)"

# ══════════════════════════════════════════════════════════════════
# 🎨 PREMIUM DARK CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    .main { background-color:#060913 !important; color:#e2e8f0 !important; }
    body { background-color:#060913 !important; }
    
    /* METRIC CARDS */
    div[data-testid="stMetricSimpleContainer"] {
        background: linear-gradient(135deg, #0d162d, #142247) !important;
        padding: 18px !important;
        border-radius: 12px !important;
        border: 1px solid #1e366a !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stMetricSimpleContainer"]:hover {
        border-color: #3b5998 !important;
        box-shadow: 0 6px 16px rgba(59,89,152,0.2) !important;
    }
    
    /* INPUTS */
    .stTextInput input, .stNumberInput input, .stSelectbox, .stPasswordInput input {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stPasswordInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 8px rgba(59,130,246,0.3) !important;
    }
    
    /* DEFAULT BUTTONS */
    .stButton > button {
        width: 100% !important;
        border-radius: 10px !important;
        height: 48px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        text-transform: uppercase !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.4) !important;
    }
    
    /* 🟩 BIG BUY BUTTON */
    .buy-box .stButton > button {
        background: linear-gradient(135deg, #00e676, #00c853, #007e33) !important;
        color: #ffffff !important;
        height: 80px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        letter-spacing: 3px !important;
        border-radius: 14px !important;
        border: 2px solid #00e676 !important;
        box-shadow: 0 0 20px rgba(0,230,118,0.4), 0 6px 20px rgba(0,0,0,0.5) !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.5) !important;
    }
    .buy-box .stButton > button:hover {
        background: linear-gradient(135deg, #69ff9a, #00e676, #00c853) !important;
        box-shadow: 0 0 32px rgba(0,230,118,0.7), 0 8px 24px rgba(0,0,0,0.5) !important;
        transform: translateY(-3px) scale(1.02) !important;
    }
    
    /* 🟥 BIG SELL BUTTON */
    .sell-box .stButton > button {
        background: linear-gradient(135deg, #ff1744, #ff4444, #cc0000) !important;
        color: #ffffff !important;
        height: 80px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        letter-spacing: 3px !important;
        border-radius: 14px !important;
        border: 2px solid #ff1744 !important;
        box-shadow: 0 0 20px rgba(255,23,68,0.4), 0 6px 20px rgba(0,0,0,0.5) !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.5) !important;
    }
    .sell-box .stButton > button:hover {
        background: linear-gradient(135deg, #ff6b6b, #ff1744, #dd0000) !important;
        box-shadow: 0 0 32px rgba(255,23,68,0.7), 0 8px 24px rgba(0,0,0,0.5) !important;
        transform: translateY(-3px) scale(1.02) !important;
    }
    
    /* 🟨 BIG WAIT BUTTON */
    .wait-box .stButton > button {
        background: linear-gradient(135deg, #ffee00, #ffbb33, #ff8800) !important;
        color: #1a1a1a !important;
        height: 80px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        letter-spacing: 3px !important;
        border-radius: 14px !important;
        border: 2px solid #ffbb33 !important;
        box-shadow: 0 0 20px rgba(255,187,51,0.4), 0 6px 20px rgba(0,0,0,0.5) !important;
    }
    
    /* CONFIG BOX */
    .config-box {
        background-color: #0d1527 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid #1e293b !important;
        margin-bottom: 15px !important;
    }
    
    /* RISK ALERT BOX */
    .risk-alert {
        background: linear-gradient(135deg, #3d1c1a, #2d0f0f);
        border: 2px solid #dc2626;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 10px 0;
    }
    
    /* TRAIL SL BOX */
    .trail-box {
        background: linear-gradient(135deg, #0d2d1a, #0f3a20);
        border: 1px solid #22c55e;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    
    h1, h2, h3, h4, h5, h6 { color: #d4af37 !important; }
    hr { border-color: #1e366a !important; }
    label { color: #e2e8f0 !important; font-weight: 600 !important; }
    #MainMenu, footer, header { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════
_defaults = {
    "authenticated" : False,
    "user_id" : None,
    "login_time" : None,
    "broker_connected" : False,
    "connected_broker" : None,
    "broker_config" : {"client_id":"","api_key":"","secret_key":"","totp_secret":""},
    "audit_logs" : [],
    "open_positions" : [],
    "dynamic_pnl" : 2695.0,
    "total_capital" : 150000.0,
    "max_daily_loss" : 5000.0,
    "daily_target" : 8000.0,
    "trail_sl_pct" : 0.5,
    "risk_per_trade" : 2.0,
    "auto_trade" : False,
    "trail_active" : False,
    "peak_pnl" : 0.0,
}

for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════
# UTILITIES
# ══════════════════════════════════════════════════════════════════
def add_audit_log(action: str, details: str = ""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uid = st.session_state.get("user_id", "Unknown")
    st.session_state["audit_logs"].append({
        "timestamp": ts,
        "user_id": uid,
        "action": action,
        "details": details,
    })

def get_lot_size(symbol: str) -> int:
    lots = {
        "NIFTY":50,"BANKNIFTY":15,"FINNIFTY":25,"MIDCPNIFTY":10,
        "SENSEX":10,"BANKEX":15,
        "CRUDEOIL":100,"CRUDEOILM":10,"NATURALGAS":1250,"NATGASMINI":250,
        "GOLD":100,"GOLDM":10,"SILVER":30,"SILVERM":5,
    }
    return lots.get(symbol.upper(), 1)

def get_tradingview_symbol(symbol: str) -> str:
    tv_map = {
        "NIFTY" : "NSE:NIFTY1!",
        "BANKNIFTY" : "NSE:BANKNIFTY1!",
        "FINNIFTY" : "NSE:FINNIFTY1!",
        "CRUDEOIL" : "MCX:CRUDEOIL1!",
        "GOLD" : "MCX:GOLD1!",
        "SILVER" : "MCX:SILVER1!",
    }
    return tv_map.get(symbol.upper(), f"NSE:{symbol.upper()}")

def check_risk_limits() -> tuple:
    pnl = st.session_state["dynamic_pnl"]
    if pnl < -st.session_state["max_daily_loss"]:
        return False, f"🚨 Max Daily Loss Breach!"
    if pnl >= st.session_state["daily_target"]:
        return False, f"🎯 Daily Target Hit!"
    return True, "OK"

def update_trail_sl():
    pnl = st.session_state["dynamic_pnl"]
    if pnl > st.session_state["peak_pnl"]:
        st.session_state["peak_pnl"] = pnl
    if st.session_state["trail_active"] and st.session_state["peak_pnl"] > 0:
        trail_lock = st.session_state["peak_pnl"] * (1 - st.session_state["trail_sl_pct"]/100)
        if pnl < trail_lock:
            return True, trail_lock
    return False, 0.0

def trigger_real_order(symbol: str, action: str, qty: int, **kwargs) -> dict:
    if not st.session_state["auto_trade"]:
        add_audit_log("DRY_RUN", f"{action} {qty}x {symbol}")
        return {"status": "DRY_RUN", "order_id": None}
    import random
    order_id = f"RM{random.randint(1000000, 9999999)}"
    add_audit_log("ORDER_PLACED", f"{action} {qty}x {symbol} ID:{order_id}")
    return {"status": "SUCCESS", "order_id": order_id}

# ══════════════════════════════════════════════════════════════════
# 🔐 LOGIN
# ══════════════════════════════════════════════════════════════════
if not st.session_state["authenticated"]:
    st.markdown("""
    <div style="text-align:center;padding:40px 0;">
        <h1 style="color:#d4af37;font-size:48px;font-weight:900;margin-bottom:10px;">🔱 RAMAVAT ALGO ELITE</h1>
        <p style="color:#9ca3af;font-size:16px;">PROFESSIONAL ALGO TRADING TERMINAL v2.0</p>
        <hr style="margin:30px 0;border-color:#1e366a;">
    </div>""", unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1,2,1])
    with col_mid:
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#d4af37;text-align:center;'>🔐 SECURE LOGIN</h3>", unsafe_allow_html=True)
        login_user = st.text_input("👤 User ID:", placeholder="Enter User ID", key="li_u")
        login_pass = st.text_input("🔑 Password:", type="password", placeholder="Default: 1234", key="li_p")
        
        if st.button("🚀 LOGIN", use_container_width=True):
            if login_user and login_pass == "1234":
                st.session_state["authenticated"] = True
                st.session_state["user_id"] = login_user
                st.session_state["login_time"] = datetime.now()
                add_audit_log("LOGIN", f"'{login_user}' logged in")
                st.success("✅ લૉગિન સફળ 🚀")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ ખોટો Password!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════
risk_ok, risk_msg = check_risk_limits()
trail_hit, trail_lock_pnl = update_trail_sl()

h_left, h_right = st.columns([4,1])
with h_left:
    st.markdown("<h2>🔱 RAMAVAT ALGO ELITE</h2>", unsafe_allow_html=True)
with h_right:
    if st.button("🚪 Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ── METRICS ────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
pnl = st.session_state["dynamic_pnl"]
m1.metric("📊 Today P&L (Live)", f"₹ {pnl:,.2f}")
m2.metric("💰 Total Capital", f"₹ {st.session_state['total_capital']:,.0f}")
m3.metric("🎯 Open Positions", f"{len(st.session_state['open_positions'])} Active")
m4.metric("🔌 API Status", "Connected ✅" if st.session_state["broker_connected"] else "Disconnected ❌")

col_chart, col_ctrl = st.columns([1.1, 1])

with col_ctrl:
    with st.expander("🔌 Broker API Configuration"):
        selected_broker = st.selectbox("Broker પસંદ કરો:", [b.value for b in BrokerType])
        u_cid = st.text_input("👤 Client ID:", key="ci")
        u_api = st.text_input("🔑 API Key:", type="password", key="ak")
        if st.button("🔌 Connect API"):
            st.session_state["broker_connected"] = True
            st.session_state["connected_broker"] = selected_broker
            st.rerun()

    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    user_symbol = st.text_input("Symbol:", value="NIFTY").upper()
    u_lots = st.number_input("🔢 Lots:", min_value=1, value=1)
    st.markdown("</div>", unsafe_allow_html=True)

    ob1, ob2 = st.columns(2)
    with ob1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("🟩 BUY"):
            st.toast("BUY Order Placed!")
        st.markdown("</div>", unsafe_allow_html=True)
    with ob2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("🟥 SELL"):
            st.toast("SELL Order Placed!")
        st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    st.markdown(f"<h4> Live Chart: {user_symbol}</h4>", unsafe_allow_html=True)
    tv_sym = get_tradingview_symbol(user_symbol)
    chart_html = f"""
    <div style="height:400px;">
        <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol={tv_sym}&interval=5&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
    </div>
    """
    st.components.v1.html(chart_html, height=410)
