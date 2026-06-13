"""
app.py — RAMAVAT ALGO ELITE  [v3.0]
====================================
Professional Trading Terminal
Premium Dark Neon Theme | Fixed TradingView Widget
"""

import streamlit as st
import time
import pandas as pd
from datetime import datetime
from enum import Enum

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ramavat Algo Elite v3.0",
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
# 🎨 PREMIUM DARK NEON GLASS LOOK (ULTRA MODERN)
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    .main { background: radial-gradient(circle at top, #0f172a, #020617) !important; color:#f8fafc !important; }
    body  { background-color:#020617 !important; }

    /* MODERN PREMIUM CARDS */
    div[data-testid="stMetricSimpleContainer"] {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 20px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        text-align: center !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    
    /* INPUT FIELDS */
    .stTextInput input, .stNumberInput input, .stSelectbox, .stPasswordInput input {
        background-color: #0f172a !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    /* GLOWING BUTTONS */
    .buy-box .stButton > button {
        background: linear-gradient(135deg, #22c55e, #15803d) !important;
        color: white !important; height: 65px !important; font-size: 20px !important; font-weight: 800 !important;
        border-radius: 12px !important; border: none !important;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.4) !important;
    }
    .sell-box .stButton > button {
        background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
        color: white !important; height: 65px !important; font-size: 20px !important; font-weight: 800 !important;
        border-radius: 12px !important; border: none !important;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.4) !important;
    }
    .wait-box .stButton > button {
        background: linear-gradient(135deg, #eab308, #a16207) !important;
        color: black !important; height: 50px !important; font-size: 16px !important; font-weight: 700 !important;
        border-radius: 12px !important; border: none !important;
    }
    
    .config-box {
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 20px !important; border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.05) !important; margin-bottom: 15px !important;
    }
    h1, h2, h3, h4 { color: #f59e0b !important; font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# DATA & SESSION INITIALIZATION
# ══════════════════════════════════════════════════════════════════
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True  # સેટિંગ્સ માટે બાયપાસ
    st.session_state["dynamic_pnl"] = 2695.0
    st.session_state["total_capital"] = 150000.0
    st.session_state["max_daily_loss"] = 5000.0
    st.session_state["daily_target"] = 8000.0
    st.session_state["broker_connected"] = True
    st.session_state["connected_broker"] = "Angel One (SmartAPI)"
    st.session_state["open_positions"] = []
    st.session_state["audit_logs"] = []
    st.session_state["auto_trade"] = False

# ── FIXED TRADINGVIEW MAPPING FUNCTION ─────────────────────────────
def get_tradingview_symbol(symbol: str) -> str:
    s = symbol.upper().strip()
    tv_map = {
        "NIFTY": "NSE:NIFTY1!",
        "BANKNIFTY": "NSE:BANKNIFTY1!",
        "SBIN": "NSE:SBIN",
        "CRUDEOIL": "MCX:CRUDEOIL1!"
    }
    return tv_map.get(s, f"NSE:{s}")

# ── HEADER ─────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-bottom: 20px;">
    <h1 style="font-size:36px; font-weight:900; letter-spacing:1px;">🔱 RAMAVAT ALGO ELITE v3.0</h1>
    <p style="color:#94a3b8;">✨ PREMIUM TRADING TERMINAL • SATURDAY CONTROL DESK</p>
</div>""", unsafe_allow_html=True)

# ── METRICS DASHBOARD ──────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
pnl = st.session_state["dynamic_pnl"]
m1.metric("📊 Today P&L (Live)", f"₹ {pnl:,.2f}", "▲ Profit" if pnl >= 0 else "▼ Loss")
m2.metric("💰 Total Capital", f"₹ {st.session_state['total_capital']:,.0f}", "Available")
m3.metric("🎯 Open Positions", f"{len(st.session_state['open_positions'])} Active")
m4.metric("🔌 API Status", "Connected ✅" if st.session_state["broker_connected"] else "Disconnected ❌")

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
col_chart, col_ctrl = st.columns([1.2, 1])

with col_ctrl:
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    user_symbol = st.text_input("🔍 Quick Symbol Search (e.g., SBIN, NIFTY):", value="SBIN").upper().strip()
    sel_type = st.selectbox("Type:", ["EQUITY (CASH)", "CE", "PE", "FUT"])
    u_lots = st.number_input("🔢 Lots / Qty:", min_value=1, value=10)
    st.markdown("</div>", unsafe_allow_html=True)

    # ACTION BUTTONS
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("🟩 BUY", use_container_width=True):
            st.toast(f"🚀 BUY Order executed for {user_symbol}!")
        st.markdown('</div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("🟥 SELL", use_container_width=True):
            st.toast(f"🚨 SELL Order executed for {user_symbol}!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="wait-box" style="margin-top:10px;">', unsafe_allow_html=True)
    if st.button("🟨 WAIT / SYSTEM HOLD", use_container_width=True):
        st.toast("⏳ System on Hold Mode")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    st.markdown(f"#### 📈 Live Chart: {user_symbol}")
    tv_sym = get_tradingview_symbol(user_symbol)
    
    # ── FIX: TRADINGVIEW EMBED CODE WITH CORRECT TICKER ID ──
    chart_html = f"""
    <div style="height:480px; border-radius:16px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
        <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol={tv_sym}&interval=5&theme=dark&style=1&timezone=Asia%2FKolkata&studies=%5B%5D&local=en&calendar=1" 
                width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe>
    </div>
    """
    st.components.v1.html(chart_html, height=490, scrolling=False)
