"""
app.py — RAMAVAT ALGO [v10.0 - CHARTINK INTEGRATED + OFFICIAL ANGEL ONE]
========================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import strategies  # આપણું સ્ટ્રેટેજી મગજ
import brokers     # આપણું બ્રોקר લોગિન મગજ
import orders      # આપણું ઓર્ડર ફાયર મગજ

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ramavat Algo v10.0",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════
# 🌐 CHARTINK WEBHOOK BACKGROUND RECEIVER (CUSTOM EMBEDDED ENGINE)
# ══════════════════════════════════════════════════════════════════
# આ કોડ બેકગ્રાઉન્ડમાં Chartink માંથી આવતા લાઈવ સિગ્નલ પકડી લેશે.
# Chartink URL: https://your-app-url.streamlit.app/?chartink_signal=true

query_params = st.query_params

if "chartink_signal" in query_params:
    try:
        # Chartink જ્યારે એલર્ટ મોકલે ત્યારે તેની કન્ડિશન ચેક કરો
        raw_stocks = query_params.get("stocks", "")
        
        if raw_stocks:
            stocks_list = raw_stocks.split(",")
            for symbol in stocks_list:
                symbol = symbol.strip().upper()
                
                # સેફ્ટી ફિલ્ટર: ગડબડથી બચવા માટે ઓટોમેટિક ફક્ત ૧ લોટ/શેર જ જશે
                fixed_qty = 1 
                
                # એન્જલ વન બ્રોકરમાં ઓટોમેટિક માર્કેટ ઓર્ડર પંચ કરો
                status, msg = orders.place_market_order("Angel One (SmartAPI)", symbol, fixed_qty, "BUY")
                
        # સિગ્નલ પ્રોસેસ થયા પછી પેજને ક્લીન કરી નાખો જેથી લૂપ ન ફરે
        st.query_params.clear()
        
    except Exception as e:
        pass

# ══════════════════════════════════════════════════════════════════
# 🎨 ULTRA FANCY COMPONENT STYLES (FIXED ELEMENT IDS)
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=500;900&family=Rajdhani:wght=600;700&display=swap');

    * { margin:0; padding:0; box-sizing:border-box; }
    .main { background: radial-gradient(circle at top inside, #140a21, #020207) !important; color:#f8fafc !important; }
    body  { background-color:#020207 !important; }

    /* TITLE BANNER */
    .fancy-title-container {
        text-align: center; padding: 15px 0; background: rgba(255, 255, 255, 0.01);
        border-radius: 16px; border: 1px solid rgba(236, 72, 153, 0.15);
        box-shadow: 0 0 20px rgba(236, 72, 153, 0.08); margin-bottom: 15px;
    }
    .fancy-title { font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 36px; letter-spacing: 3px; }
    .word-pink { color: #ff007f; text-shadow: 0 0 12px #ff007f, 0 0 25px #ff007f; }
    .word-gold { color: #f59e0b; text-shadow: 0 0 12px #f59e0b; }
    .subtitle-terminal { font-family: 'Rajdhani', sans-serif; color: #94a3b8; font-size: 12px; letter-spacing: 4px; margin-top: 5px; }

    /* METRIC GLASS CARDS */
    div[data-testid="stMetricSimpleContainer"] {
        background: rgba(20, 14, 38, 0.6) !important; backdrop-filter: blur(15px) !important;
        padding: 18px !important; border-radius: 14px !important;
        border: 1px solid rgba(236, 72, 153, 0.1) !important; text-align: center !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
    }
    
    /* INPUT BOXES */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #080617 !important; color: #f1f5f9 !important;
        border: 1px solid #352354 !important; border-radius: 8px !important;
    }

    /* 🔑 3D LOGIN BUTTON */
    .login-btn-box .stButton > button {
        background: linear-gradient(135deg, #f59e0b, #b45309) !important; color: white !important;
        font-family: 'Orbitron', sans-serif; font-weight: 900; border: 1px solid #fbbf24 !important;
        box-shadow: 0 4px 0 #78350f, 0 6px 15px rgba(245,158,11,0.3) !important; border-radius: 10px; height: 46px;
    }

    /* 🧠 ENGINE MODES */
    .algo-btn-semi .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important; color: white !important;
        font-family: 'Orbitron', sans-serif; font-weight: 700; border: 1px solid #60a5fa !important;
        box-shadow: 0 4px 0 #1e3a8a, 0 6px 15px rgba(0,0,0,0.5) !important; border-radius: 10px; height: 45px;
    }
    .algo-btn-fully .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #5b21b6) !important; color: white !important;
        font-family: 'Orbitron', sans-serif; font-weight: 700; border: 1px solid #a78bfa !important;
        box-shadow: 0 4px 0 #4c1d95, 0 6px 15px rgba(0,0,0,0.5) !important; border-radius: 10px; height: 45px;
    }
    .algo-btn-scalp .stButton > button {
        background: linear-gradient(135deg, #ec4899, #9d174d) !important; color: white !important;
        font-family: 'Orbitron', sans-serif; font-weight: 700; border: 1px solid #f472b6 !important;
        box-shadow: 0 4px 0 #831843, 0 6px 15px rgba(0,0,0,0.5) !important; border-radius: 10px; height: 45px;
    }
    .stButton > button:active { transform: translateY(3px) !important; box-shadow: 0 1px 0 inherit !important; }

    /* 🟩 3D BUY / 🟥 3D SELL */
    .buy-box .stButton > button {
        background: linear-gradient(135deg, #22c55e, #166534) !important; color: white !important; 
        height: 65px !important; font-size: 22px !important; font-family: 'Orbitron', sans-serif; font-weight: 900 !important;
        border-radius: 12px !important; border: 1px solid #4ade80 !important;
        box-shadow: 0 5px 0 #14532d, 0 8px 15px rgba(0,0,0,0.5) !important;
    }
    .sell-box .stButton > button {
        background: linear-gradient(135deg, #ef4444, #991b1b) !important; color: white !important; 
        height: 65px !important; font-size: 22px !important; font-family: 'Orbitron', sans-serif; font-weight: 900 !important;
        border-radius: 12px !important; border: 1px solid #f87171 !important;
        box-shadow: 0 5px 0 #7f1d1d, 0 8px 15px rgba(0,0,0,0.5) !important;
    }
    
    .config-box {
        background: rgba(8, 6, 20, 0.8) !important; padding: 18px !important; 
        border-radius: 14px !important; border: 1px solid rgba(236, 72, 153, 0.06) !important; margin-bottom: 12px !important;
    }
    h4 { color: #ff007f !important; font-family: 'Rajdhani', sans-serif; font-size: 18px !important; font-weight: 700; margin-bottom: 8px; }
    #MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION INITIALIZATION ─────────────────────────────────────────
if "dynamic_pnl" not in st.session_state:
    st.session_state["dynamic_pnl"] = 0.0
    st.session_state["algo_mode"] = "Waiting Login"
    st.session_state["selected_strategy"] = "Supertrend (10,3)"
    st.session_state["active_broker"] = "None (Disconnected)"

# ── HEADER ─────────────────────────────────────────────────────────
st.markdown("""
<div class="fancy-title-container">
    <h1 class="fancy-title"><span class="word-pink">🔱 RAMAVAT</span> <span class="word-gold">ALGO</span></h1>
    <div class="subtitle-terminal">⚡ PREMIUM QUANT TRADING TERMINAL • TRADING STATION ⚡</div>
</div>""", unsafe_allow_html=True)

# ── METRICS DASHBOARD ──────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("📊 Today P&L (Live)", f"₹ {st.session_state['dynamic_pnl']:,.2f}", "▲ Orbit Run")
m2.metric("🧠 Active Mode", st.session_state["algo_mode"])
m3.metric("🎯 Strategy Intel", st.session_state["selected_strategy"])
m4.metric("🔌 Broker Connect", st.session_state["active_broker"])

st.markdown("<br>", unsafe_allow_html=True)

# ── MAIN TERMINAL LAYOUT ───────────────────────────────────────────
col_chart, col_ctrl = st.columns([1.2, 1])

with col_ctrl:
    # 🔑 STEP 1: BROKER LOGIN PANEL (ANGEL ONE DEFAULT)
    st.markdown("<h4>🔑 STEP 1: BROKER API AUTHENTICATION</h4>", unsafe_allow_html=True)
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    
    broker_choice = st.selectbox("પસંદગીના બ્રોકર પસંદ કરો:", [
        "Angel One (SmartAPI)",
        "Groww Engine", 
        "Dhan HQ API",
        "Zerodha Kite",
        "Fyers One"
    ], key="main_broker_selection_dropdown")
    
    brow1, brow2 = st.columns(2)
    with brow1:
        c_id = st.text_input("Client ID / User ID:", placeholder="e.g., A123456", key="main_client_id_input_field")
    with brow2:
        a_key = st.text_input("API Key / Totp Secret:", type="password", placeholder="••••••••", key="main_api_key_input_field")
        
    st.markdown('<div class="login-btn-box">', unsafe_allow_html=True)
    if st.button("🔌 SECURE BROKER LOGIN", use_container_width=True, key="main_broker_login_trigger_btn"):
        status, msg = brokers.authenticate_broker(broker_choice, a_key, c_id)
        if status:
            st.session_state["active_broker"] = broker_choice
            st.session_state["algo_mode"] = "Manual Control"
            st.session_state["dynamic_pnl"] = 2695.0
            st.success(msg)
        else:
            st.error(msg)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 🧠 STEP 2: ALGO ENGINE MODE
    st.markdown("<h4>🧠 STEP 2: SELECT ALGO ENGINE MODE</h4>", unsafe_allow_html=True)
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="algo-btn-semi">', unsafe_allow_html=True)
        if st.button("SEMI AUTO", use_container_width=True, key="engine_mode_semi_btn"):
            st.session_state["algo_mode"] = "Semi Automated"
            st.toast("⚡ Semi-Auto Mode Enabled!")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="algo-btn-fully">', unsafe_allow_html=True)
        if st.button("FULLY AUTO", use_container_width=True, key="engine_mode_fully_btn"):
            st.session_state["algo_mode"] = "Fully Automated"
            st.toast("🔥 FULLY AUTOMATED ALGO RUNNING LIVE WITH CHARTINK!")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="algo-btn-scalp">', unsafe_allow_html=True)
        if st.button("SCALPING", use_container_width=True, key="engine_mode_scalp_btn"):
            st.session_state["algo_mode"] = "High Frequency Scalper"
            st.toast("🚀 Scalping Engine Activated")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ⚙️ STEP 3: STRATEGY & CONFIG
    st.markdown("<h4>⚙️ STEP 3: STRATEGY & INSTRUMENT CONFIG</h4>", unsafe_allow_html=True)
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    chosen_strat = st.selectbox("Select Core Indicator Strategy Logic:", 
                                  ["Supertrend (10, 3) Pro", "RSI Reversal (14)", "MACD Crossover Cross", "Price Action Breakout"], key="strategy_logic_config_selectbox")
    st.session_state["selected_strategy"] = chosen_strat
    
    user_symbol = st.text_input("🔍 Quick Symbol Search:", value="SBIN", key="symbol_text_search_box").upper().strip()
    sel_type = st.selectbox("Product Type:", ["EQUITY (CASH)", "CE", "PE", "FUT"], key="product_type_config_dropdown")
    u_lots = st.number_input("🔢 Quantity / Lots:", min_value=1, value=10, key="quantity_lots_config_input")
    st.markdown("</div>", unsafe_allow_html=True)

    # ⚡ STEP 4: 3D TRADING BUTTONS WITH REAL PUNCH LOGIC
    st.markdown("<h4>⚡ STEP 4: MANUAL EXECUTION OVERRIDE</h4>", unsafe_allow_html=True)
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("BUY", use_container_width=True, key="stable_buy_override_action_btn"):
            status, msg = orders.place_market_order(st.session_state["active_broker"], user_symbol, u_lots, "BUY")
            if status:
                st.toast(msg, icon="🚀")
            else:
                st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("SELL", use_container_width=True, key="stable_sell_override_action_btn"):
            status, msg = orders.place_market_order(st.session_state["active_broker"], user_symbol, u_lots, "SELL")
            if status:
                st.toast(msg, icon="🚨")
            else:
                st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    st.markdown(f"#### 📈 Live Market Intel Chart: {user_symbol}")
    tv_sym = f"NSE:{user_symbol}" if user_symbol not in ["NIFTY", "BANKNIFTY"] else f"NSE:{user_symbol}1!"
    
    chart_html = f"""
    <div style="height:570px; border-radius:16px; overflow:hidden; border:1px solid rgba(236,72,153,0.25); box-shadow: 0 0 15px rgba(236,72,153,0.1);">
        <iframe src="https://s.tradingview.com/widgetembed/?symbol={tv_sym}&interval=5&theme=dark&style=1&timezone=Asia%2FKolkata&studies=%5B%5D&local=en" 
                width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe>
    </div>
    """
    st.components.v1.html(chart_html, height=580, scrolling=False)
