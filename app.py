"""
app.py — RAMAVAT ALGO [v4.0 - ULTRA 3D PREMIUM]
================================================
Professional Trading Terminal — Short Name + 3D Buttons
"""

import streamlit as st
import time
import pandas as pd
from datetime import datetime
from enum import Enum

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ramavat Algo v4.0",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

class BrokerType(Enum):
    ANGEL_ONE  = "Angel One (SmartAPI)"
    ALICE_BLUE = "Alice Blue (ANT)"
    ZERODHA    = "Zerodha (Kite)"
    FINVASIA   = "Finvasia (Shoonya)"

# ══════════════════════════════════════════════════════════════════
# 🎨 ULTRA FANCY MULTI-COLOR & 3D NEON BUTTON STYLE
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Rajdhani:wght@600;700&display=swap');

    * { margin:0; padding:0; box-sizing:border-box; }
    .main { background: radial-gradient(circle at top inside, #160c22, #03030a) !important; color:#f8fafc !important; }
    body  { background-color:#03030a !important; }

    /* FANCY NEON PINK HEADER (SHORT & SWEET) */
    .fancy-title-container {
        text-align: center;
        padding: 18px 0;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 16px;
        border: 1px solid rgba(236, 72, 153, 0.2);
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.1);
        margin-bottom: 20px;
    }
    .fancy-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 38px;
        letter-spacing: 3px;
        margin: 0;
        padding: 0;
    }
    .word-pink {
        color: #ff007f;
        text-shadow: 0 0 12px #ff007f, 0 0 30px #ff007f;
    }
    .word-gold {
        color: #f59e0b;
        text-shadow: 0 0 12px #f59e0b, 0 0 25px #f59e0b;
    }
    .subtitle-terminal {
        font-family: 'Rajdhani', sans-serif;
        color: #94a3b8;
        font-size: 13px;
        letter-spacing: 5px;
        margin-top: 6px;
        text-transform: uppercase;
    }

    /* PREMIUM GLASS CARDS */
    div[data-testid="stMetricSimpleContainer"] {
        background: rgba(22, 16, 41, 0.5) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        padding: 20px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(236, 72, 153, 0.12) !important;
        text-align: center !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
    }
    
    /* INPUT FIELDS */
    .stTextInput input, .stNumberInput input, .stSelectbox, .stPasswordInput input {
        background-color: #0a081a !important;
        color: #f1f5f9 !important;
        border: 1px solid #3c285c !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    /* 🟩 3D NEON BUY BUTTON */
    .buy-box .stButton > button {
        background: linear-gradient(135deg, #22c55e, #166534) !important;
        color: #ffffff !important; 
        height: 75px !important; 
        font-size: 24px !important; 
        font-family: 'Orbitron', sans-serif; 
        font-weight: 900 !important;
        border-radius: 14px !important; 
        border: 1px solid #4ade80 !important;
        box-shadow: 0 6px 0 #14532d, 0 10px 20px rgba(0,0,0,0.6) !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
        transition: all 0.1s ease-child;
    }
    .buy-box .stButton > button:hover {
        background: linear-gradient(135deg, #4ade80, #15803d) !important;
        box-shadow: 0 6px 0 #14532d, 0 12px 25px rgba(34,197,94,0.4) !important;
    }
    .buy-box .stButton > button:active {
        border-bottom: 2px solid #4ade80 !important;
        box-shadow: 0 2px 0 #14532d, 0 4px 10px rgba(0,0,0,0.6) !important;
        transform: translateY(4px) !important;
    }

    /* 🟥 3D NEON SELL BUTTON */
    .sell-box .stButton > button {
        background: linear-gradient(135deg, #ef4444, #991b1b) !important;
        color: #ffffff !important; 
        height: 75px !important; 
        font-size: 24px !important; 
        font-family: 'Orbitron', sans-serif; 
        font-weight: 900 !important;
        border-radius: 14px !important; 
        border: 1px solid #f87171 Suspend !important;
        box-shadow: 0 6px 0 #7f1d1d, 0 10px 20px rgba(0,0,0,0.6) !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
    }
    .sell-box .stButton > button:hover {
        background: linear-gradient(135deg, #f87171, #b91c1c) !important;
        box-shadow: 0 6px 0 #7f1d1d, 0 12px 25px rgba(239,68,68,0.4) !important;
    }
    .sell-box .stButton > button:active {
        box-shadow: 0 2px 0 #7f1d1d, 0 4px 10px rgba(0,0,0,0.6) !important;
        transform: translateY(4px) !important;
    }

    /* 🟨 3D WAIT BUTTON */
    .wait-box .stButton > button {
        background: linear-gradient(135deg, #d97706, #78350f) !important;
        color: white !important; 
        height: 52px !important; 
        font-size: 16px !important; 
        font-weight: 800 !important;
        border-radius: 12px !important; 
        border: 1px solid #f59e0b !important;
        box-shadow: 0 4px 0 #451a03, 0 6px 12px rgba(0,0,0,0.5) !important;
    }
    .wait-box .stButton > button:active {
        box-shadow: 0 1px 0 #451a03, 0 2px 5px rgba(0,0,0,0.5) !important;
        transform: translateY(3px) !important;
    }
    
    .config-box {
        background: rgba(10, 8, 26, 0.75) !important;
        padding: 20px !important; border-radius: 14px !important;
        border: 1px solid rgba(236, 72, 153, 0.08) !important; margin-bottom: 15px !important;
    }
    h4 { color: #ff007f !important; font-family: 'Rajdhani', sans-serif; font-size: 19px !important; font-weight: 700; }
    #MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# DATA & SESSION INITIALIZATION
# ══════════════════════════════════════════════════════════════════
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True
    st.session_state["dynamic_pnl"] = 2695.0
    st.session_state["total_capital"] = 150000.0
    st.session_state["max_daily_loss"] = 5000.0
    st.session_state["daily_target"] = 8000.0
    st.session_state["broker_connected"] = True
    st.session_state["connected_broker"] = "Angel One (SmartAPI)"
    st.session_state["open_positions"] = []
    st.session_state["audit_logs"] = []

def get_tradingview_symbol(symbol: str) -> str:
    s = symbol.upper().strip()
    tv_map = {
        "NIFTY": "NSE:NIFTY1!",
        "BANKNIFTY": "NSE:BANKNIFTY1!",
        "SBIN": "NSE:SBIN",
        "CRUDEOIL": "MCX:CRUDEOIL1!"
    }
    return tv_map.get(s, f"NSE:{s}")

# ── FANCY SHORT & SWEET HEADER ─────────────────────────────────────
st.markdown("""
<div class="fancy-title-container">
    <h1 class="fancy-title">
        <span class="word-pink">🔱 RAMAVAT</span> 
        <span class="word-gold">ALGO</span>
    </h1>
    <div class="subtitle-terminal">⚡ PREMIUM QUANT TRADING TERMINAL • LIVE DESK ⚡</div>
</div>""", unsafe_allow_html=True)

# ── METRICS DASHBOARD ──────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
pnl = st.session_state["dynamic_pnl"]
m1.metric("📊 Today P&L (Live)", f"₹ {pnl:,.2f}", "▲ Profit" if pnl >= 0 else "▼ Loss")
m2.metric("💰 Total Capital", f"₹ {st.session_state['total_capital']:,.0f}", "Available")
m3.metric("🎯 Open Positions", f"{len(st.session_state['open_positions'])} Active")
m4.metric("🔌 API Status", "Connected ✅")

loss_pct = min(max(-pnl, 0) / st.session_state["max_daily_loss"], 1.0)
profit_pct = min(max(pnl, 0) / st.session_state["daily_target"], 1.0)

col_prog1, col_prog2 = st.columns(2)
with col_prog1:
    st.caption(f"🛑 Loss Used: {loss_pct*100:.0f}% of ₹{st.session_state['max_daily_loss']:,.0f}")
    st.progress(loss_pct)
with col_prog2:
    st.caption(f"🎯 Target Reached: {profit_pct*100:.0f}% of ₹{st.session_state['daily_target']:,.0f}")
    st.progress(profit_pct)

st.markdown("<br>", unsafe_allow_html=True)

# ── MAIN LAYOUT ────────────────────────────────────────────────────
col_chart, col_ctrl = st.columns([1.3, 1])

with col_ctrl:
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    user_symbol = st.text_input("🔍 Quick Symbol Search (e.g., SBIN, NIFTY):", value="SBIN").upper().strip()
    sel_type = st.selectbox("Type:", ["EQUITY (CASH)", "CE", "PE", "FUT"])
    u_lots = st.number_input("🔢 Lots / Qty:", min_value=1, value=10)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3D ACTION BUTTONS AREA
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("BUY", use_container_width=True):
            st.toast(f"🚀 BUY Order executed for {user_symbol}!")
        st.markdown('</div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("SELL", use_container_width=True):
            st.toast(f"🚨 SELL Order executed for {user_symbol}!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="wait-box" style="margin-top:15px;">', unsafe_allow_html=True)
    if st.button("WAIT / SYSTEM HOLD", use_container_width=True):
        st.toast("⏳ System on Hold Mode")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    st.markdown(f"#### 📈 Live Neon Chart: {user_symbol}")
    tv_sym = get_tradingview_symbol(user_symbol)
    
    chart_html = f"""
    <div style="height:490px; border-radius:16px; overflow:hidden; border:1px solid rgba(236,72,153,0.3); box-shadow: 0 0 15px rgba(236,72,153,0.15);">
        <iframe src="https://s.tradingview.com/widgetembed/?symbol={tv_sym}&interval=5&theme=dark&style=1&timezone=Asia%2FKolkata&studies=%5B%5D&local=en" 
                width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe>
    </div>
    """
    st.components.v1.html(chart_html, height=500, scrolling=False)
