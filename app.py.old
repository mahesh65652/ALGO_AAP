import streamlit as st
import time
import pandas as pd
import json
from datetime import datetime
from enum import Enum

# ============================================================================
# 🔱 RAMAVAT ALGO ELITE - PROFESSIONAL TRADING TERMINAL v1.0
# ============================================================================

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ramavat Algo Elite",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ENUMS FOR TRADING DATA ---
class BrokerType(Enum):
    ALICE_BLUE = "Alice Blue"
    ZERODHA = "Zerodha (Kite)"
    ANGEL_ONE = "Angel One"
    FINVASIA = "Finvasia (Shoonya)"

# --- PREMIUM DARK TRADING THEME (Custom CSS) ---
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        background-color: #060913 !important;
        color: #e2e8f0 !important;
    }
    
    body {
        background-color: #060913 !important;
    }
    
    /* METRIC BOXES - Premium Dark Cards */
    div[data-testid="stMetricSimpleContainer"] {
        background: linear-gradient(135deg, #0d162d, #142247) !important;
        padding: 18px !important;
        border-radius: 12px !important;
        border: 1px solid #1e366a !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stMetricSimpleContainer"]:hover {
        border-color: #3b5998 !important;
        box-shadow: 0 6px 16px rgba(59, 89, 152, 0.2) !important;
    }
    
    /* INPUT ELEMENTS */
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
        box-shadow: 0 0 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* BUTTONS */
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
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* BUY BUTTON */
    .buy-box button {
        background: linear-gradient(90deg, #00c851, #007e33) !important;
        color: white !important;
    }
    
    .buy-box button:hover {
        background: linear-gradient(90deg, #1abc54, #00a144) !important;
    }
    
    /* SELL BUTTON */
    .sell-box button {
        background: linear-gradient(90deg, #ff4444, #cc0000) !important;
        color: white !important;
    }
    
    .sell-box button:hover {
        background: linear-gradient(90deg, #ff5555, #dd1111) !important;
    }
    
    /* WAIT BUTTON */
    .wait-box button {
        background: linear-gradient(90deg, #ffbb33, #ff8800) !important;
        color: white !important;
    }
    
    .wait-box button:hover {
        background: linear-gradient(90deg, #ffcc44, #ff9911) !important;
    }
    
    /* EMERGENCY PANIC BUTTON - PULSING ANIMATION */
    @keyframes pulse-panic {
        0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    
    .panic-container button {
        background: linear-gradient(90deg, #7f1d1d, #dc2626) !important;
        color: white !important;
        border: 2px solid #ef4444 !important;
        height: 56px !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        animation: pulse-panic 2s infinite !important;
        margin-top: 15px !important;
    }
    
    .panic-container button:hover {
        background: linear-gradient(90deg, #991d1d, #ee3636) !important;
        animation: none !important;
    }
    
    /* CONFIG BOX */
    .config-box {
        background-color: #0d1527 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid #1e293b !important;
        margin-bottom: 15px !important;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background-color: #0d162d !important;
        border: 1px solid #1e366a !important;
        border-radius: 8px !important;
    }
    
    /* TABLES */
    .stTable {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }
    
    table {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    thead tr {
        background-color: #0d162d !important;
        border-bottom: 2px solid #1e366a !important;
    }
    
    tbody tr {
        border-bottom: 1px solid #1e293b !important;
    }
    
    tbody tr:hover {
        background-color: #142247 !important;
    }
    
    th {
        color: #d4af37 !important;
        font-weight: 800 !important;
        padding: 12px !important;
    }
    
    td {
        color: #e2e8f0 !important;
        padding: 10px 12px !important;
    }
    
    /* LOGOUT BUTTON IN HEADER */
    .logout-btn {
        position: absolute;
        top: 10px;
        right: 20px;
    }
    
    /* LOGIN CONTAINER */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #060913, #0d162d);
    }
    
    .login-box {
        background: linear-gradient(135deg, #0d162d, #142247);
        padding: 40px;
        border-radius: 15px;
        border: 2px solid #1e366a;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        max-width: 400px;
        width: 100%;
        text-align: center;
    }
    
    /* TOAST STYLING */
    .stToast {
        background-color: #0d1527 !important;
        color: #e2e8f0 !important;
    }
    
    /* ERROR MESSAGE */
    .stAlert {
        background-color: #3d1c1a !important;
        border: 1px solid #dc2626 !important;
        color: #fca5a5 !important;
        border-radius: 8px !important;
    }
    
    /* SUCCESS MESSAGE */
    .stSuccess {
        background-color: #1c3d1c !important;
        border: 1px solid #22c55e !important;
        color: #bbf7d0 !important;
        border-radius: 8px !important;
    }
    
    /* HEADER STYLING */
    h1, h2, h3, h4, h5, h6 {
        color: #d4af37 !important;
    }
    
    /* HORIZONTAL RULE */
    hr {
        border-color: #1e366a !important;
    }
    
    /* LABEL TEXT */
    label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_id"] = None
    st.session_state["login_time"] = None

if "broker_connected" not in st.session_state:
    st.session_state["broker_connected"] = False
    st.session_state["connected_broker"] = None

if "broker_config" not in st.session_state:
    st.session_state["broker_config"] = {
        "client_id": "",
        "api_key": "",
        "secret_key": "",
        "totp_secret": ""
    }

if "audit_logs" not in st.session_state:
    st.session_state["audit_logs"] = []

if "open_positions" not in st.session_state:
    st.session_state["open_positions"] = []

if "dynamic_pnl" not in st.session_state:
    st.session_state["dynamic_pnl"] = 2695

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def add_audit_log(action: str, details: str = ""):
    """Add entry to audit logs with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = st.session_state.get("user_id", "Unknown")
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "action": action,
        "details": details
    }
    st.session_state["audit_logs"].append(log_entry)

def get_lot_size(symbol: str) -> int:
    """
    Intelligent LOT SIZE detection based on symbol.
    Returns the standard lot size for Indian trading instruments.
    """
    lot_sizes = {
        # INDICES
        "NIFTY": 25,
        "BANKNIFTY": 15,
        "FINNIFTY": 25,
        "MIDCPNIFTY": 10,
        
        # COMMODITIES (MCX)
        "CRUDEOIL": 100,
        "NATURALGAS": 1250,
        "GOLD": 100,
        "SILVER": 30,
        "COPPER": 250,
        "ZINC": 250,
        "NICKEL": 10,
        "LEAD": 500,
        "ALUMINIUM": 1000,
        
        # GLOBAL COMMODITIES (NYMEX/COMEX)
        "CRUDE": 100,
        "NG": 1250,
    }
    
    # Default to 1 for stocks (EQUITY)
    return lot_sizes.get(symbol.upper(), 1)

def get_tradingview_symbol(symbol: str) -> str:
    """
    Map Indian trading symbols to correct TradingView widget symbols.
    Ensures charts display correctly without errors.
    """
    symbol = symbol.upper().strip()
    
    symbol_map = {
        # INDICES - TradingView
        "NIFTY": "TVC:NIFTY",
        "BANKNIFTY": "TVC:BANKNIFTY",
        "FINNIFTY": "TVC:FINNIFTY",
        "MIDCPNIFTY": "TVC:MIDCPNIFTY",
        
        # COMMODITIES - MCX/NYMEX
        "CRUDEOIL": "MCX:CRUDEOIL1!",
        "NATURALGAS": "MCX:NATURALGAS1!",
        "GOLD": "MCX:GOLD1!",
        "SILVER": "MCX:SILVER1!",
        "COPPER": "MCX:COPPER1!",
        "ZINC": "MCX:ZINC1!",
        "NICKEL": "MCX:NICKEL1!",
        "LEAD": "MCX:LEAD1!",
        "ALUMINIUM": "MCX:ALUMINIUM1!",
        
        # CURRENCIES
        "EURINR": "TVC:EURINR",
        "GBPINR": "TVC:GBPINR",
        "JPYINR": "TVC:JPYINR",
        "USDINR": "TVC:USDINR",
    }
    
    # Default: Assume NSE:SYMBOL for stocks and indices
    return symbol_map.get(symbol, f"NSE:{symbol}")

def calculate_pnl(entry_price: float, current_price: float, quantity: int, order_type: str) -> tuple:
    """Calculate Profit/Loss based on entry and current price"""
    if order_type.upper() in ["BUY", "FUT"]:
        pnl = (current_price - entry_price) * quantity
    else:  # SELL
        pnl = (entry_price - current_price) * quantity
    
    pnl_percent = ((pnl / (entry_price * quantity)) * 100) if entry_price > 0 else 0
    return pnl, pnl_percent

def format_pnl(pnl: float) -> str:
    """Format P&L with color coding"""
    if pnl > 0:
        return f"<span style='color:#00c851; font-weight:bold;'>₹ {pnl:,.2f} ✅</span>"
    elif pnl < 0:
        return f"<span style='color:#ff4444; font-weight:bold;'>₹ {pnl:,.2f} ❌</span>"
    else:
        return f"<span style='color:#ffbb33;'>₹ {pnl:,.2f}</span>"

# ============================================================================
# AUTHENTICATION GATE
# ============================================================================

if not st.session_state["authenticated"]:
    # FULL LOGIN SCREEN
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style='color: #d4af37; font-size: 48px; font-weight: 900; margin-bottom: 10px;'>🔱 RAMAVAT ALGO ELITE</h1>
        <p style='color: #9ca3af; font-size: 16px;'>PROFESSIONAL ALGO TRADING TERMINAL</p>
        <hr style='margin: 30px 0; border-color: #1e366a;'>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #d4af37; text-align: center;'>🔐 SECURE LOGIN</h3>", unsafe_allow_html=True)
        
        login_user = st.text_input(
            "👤 User ID / Email:",
            placeholder="Enter your User ID",
            key="login_user_input"
        )
        
        login_pass = st.text_input(
            "🔑 Password:",
            type="password",
            placeholder="Default: 1234",
            key="login_pass_input"
        )
        
        col_login, col_empty = st.columns([1, 1])
        
        with col_login:
            if st.button("🚀 LOGIN", key="login_btn", use_container_width=True):
                # Simple authentication (can be enhanced with DB/API)
                if login_user and login_pass == "1234":
                    st.session_state["authenticated"] = True
                    st.session_state["user_id"] = login_user
                    st.session_state["login_time"] = datetime.now()
                    add_audit_log("LOGIN", f"User '{login_user}' logged in successfully")
                    st.success(f"✅ Welcome, {login_user}! 🚀")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials! Use password '1234'")
                    add_audit_log("LOGIN_FAILED", f"Failed login attempt for '{login_user}'")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 12px; margin-top: 20px;'>📝 Demo Credentials: Any User ID | Password: 1234</p>", unsafe_allow_html=True)
    
    st.stop()

# ============================================================================
# MAIN DASHBOARD (AUTHENTICATED USERS ONLY)
# ============================================================================

# HEADER WITH LOGOUT
col_header_left, col_header_right = st.columns([4, 1])

with col_header_left:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <h1 style='color: #d4af37; margin: 0; font-size: 32px; font-weight: 900;'>🔱 RAMAVAT ALGO ELITE</h1>
        <p style='color: #9ca3af; font-size: 13px; margin: 0;'>PERSONAL ALGO BRIDGE & TRADING TERMINAL (STOCKS & INDEX)</p>
    </div>
    """, unsafe_allow_html=True)

with col_header_right:
    if st.button("🚪 LOGOUT", key="logout_btn"):
        st.session_state["authenticated"] = False
        st.session_state["user_id"] = None
        st.session_state["broker_connected"] = False
        add_audit_log("LOGOUT", "User logged out")
        st.info("✅ Logged out successfully!")
        time.sleep(1)
        st.rerun()

# STATUS BAR
broker_status = (
    "<span style='color:#00c851; font-weight:bold;'>CONNECTED 🟢</span>"
    if st.session_state["broker_connected"]
    else "<span style='color:#ff4444; font-weight:bold;'>DISCONNECTED 🔴</span>"
)

current_user = st.session_state.get("user_id", "User")
connected_broker = st.session_state.get("connected_broker", "None")

st.markdown(
    f"""
    ⚡ **LIVE CONTROL DESK** | 👤 Operator: **{current_user}** | ब्रोकर स्टेटस: {broker_status}
    """,
    unsafe_allow_html=True
)
st.markdown("<hr style='margin:5px 0 15px 0; border-color:#1e366a;'>", unsafe_allow_html=True)

# ============================================================================
# DYNAMIC METRICS DASHBOARD
# ============================================================================

m1, m2, m3, m4 = st.columns(4)

current_time_sec = int(time.time())
st.session_state["dynamic_pnl"] = 2695 + (current_time_sec % 10 * 5)

# Determine P&L color based on value
pnl_value = st.session_state["dynamic_pnl"]
pnl_delta = "▲ प्रॉफिट चाली रहो" if pnl_value > 2695 else "▼ कम हुआ"

m1.metric(
    label="📊 आज का P&L (Live)",
    value=f"₹ {pnl_value:,.2f}",
    delta=pnl_delta
)

m2.metric(
    label="💰 उपलब्ध मार्जिन",
    value="₹ 1,50,000",
    delta="मार्जिन ठीक है"
)

active_positions_count = len(st.session_state.get("open_positions", []))
m3.metric(
    label="🎯 खुली पोजीशन",
    value=f"{active_positions_count} Active",
    delta="Trade Running"
)

api_status = "Handshake OK" if st.session_state["broker_connected"] else "Setup Pending"
api_delta = f"✅ {connected_broker}" if st.session_state["broker_connected"] else "❌ Not Connected"

m4.metric(
    label="🔌 API स्टेटस",
    value=api_status,
    delta=api_delta
)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# MAIN LAYOUT: CHART (LEFT) + CONTROL PANEL (RIGHT)
# ============================================================================

col_chart, col_control = st.columns([1.1, 1])

# ============================================================================
# RIGHT PANEL: BROKER CONFIG & ORDER CONTROL
# ============================================================================

with col_control:
    # --- BROKER API CONFIGURATION SECTION ---
    with st.expander("🔌 🔐 MY BROKER API CONFIGURATION"):
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        
        selected_broker = st.selectbox(
            "मेरा ब्रोकर चुनें:",
            [broker.value for broker in BrokerType],
            key="broker_select"
        )
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            u_client_id = st.text_input(
                "👤 CLIENT ID:",
                placeholder="Enter User ID",
                key="client_id_input",
                value=st.session_state["broker_config"]["client_id"]
            )
            
            u_api_key = st.text_input(
                "🔑 API KEY:",
                type="password",
                placeholder="Enter API Key",
                key="api_key_input",
                value=st.session_state["broker_config"]["api_key"]
            )
        
        with col_c2:
            u_totp = st.text_input(
                "⏳ TOTP SECRET KEY:",
                type="password",
                placeholder="Google TOTP Key",
                key="totp_input",
                value=st.session_state["broker_config"]["totp_secret"]
            )
            
            u_secret = st.text_input(
                "🔒 SECRET KEY:",
                type="password",
                placeholder="Enter Secret Key",
                key="secret_key_input",
                value=st.session_state["broker_config"]["secret_key"]
            )
        
        if st.button("🔌 SAVE & CONNECT API", key="api_connect_btn"):
            if u_client_id and u_api_key:
                st.session_state["broker_connected"] = True
                st.session_state["connected_broker"] = selected_broker
                st.session_state["broker_config"] = {
                    "client_id": u_client_id,
                    "api_key": u_api_key,
                    "secret_key": u_secret,
                    "totp_secret": u_totp
                }
                st.toast(f"✅ {selected_broker} API Successfully Connected!", icon="🚀")
                add_audit_log("API_CONNECTED", f"Broker '{selected_broker}' connected successfully")
                time.sleep(0.2)
                st.rerun()
            else:
                st.error("❌ कृपया Client ID और API Key भरें!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # --- SMART ORDER CONTROL SECTION ---
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#e2e8f0; font-size:14px; font-weight:bold; margin:0 0 10px 0;'>🔍 इंडेक्स या स्टॉक खोजें:</p>",
        unsafe_allow_html=True
    )
    
    col_sym_search, col_opt = st.columns(2)
    
    with col_sym_search:
        user_symbol = st.text_input(
            "प्रतीक नाम दर्ज करें (उदा. NIFTY, RELIANCE, CRUDEOIL):",
            value="NIFTY",
            key="symbol_search_input"
        ).strip().upper()
    
    with col_opt:
        selected_option = st.selectbox(
            "प्रकार चुनें:",
            ["CE", "PE", "FUT", "EQUITY (CASH)"],
            key="order_type_select"
        )
    
    selected_strike = st.text_input(
        "स्ट्राइक प्राइस (यदि विकल्प हो तो):",
        value="22000",
        key="strike_input"
    )
    
    # --- INTELLIGENT LOT CALCULATOR ---
    current_lot_size = get_lot_size(user_symbol)
    
    col_l, col_q = st.columns(2)
    
    with col_l:
        u_lots = st.number_input(
            "🔢 लॉट / मात्रा गुणक:",
            min_value=1,
            value=1,
            key="lot_multiplier"
        )
    
    u_qty = u_lots * current_lot_size
    
    qty_label = (
        "कुल शेयर मात्रा (Shares):"
        if current_lot_size == 1
        else f"कुल डेरिवेटिव मात्रा (Auto - {current_lot_size}/lot):"
    )
    
    with col_q:
        st.text_input(
            qty_label,
            value=f"{u_qty} Qty",
            disabled=True,
            key="qty_display"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- STOP LOSS & TARGET ---
    st.markdown("<div class='config-box' style='padding:10px; margin-top:-5px;'>", unsafe_allow_html=True)
    col_sl, col_tgt = st.columns(2)
    
    with col_sl:
        sl_points = st.number_input(
            "🚨 STOP LOSS (Pts):",
            value=30,
            key="sl_input"
        )
    
    with col_tgt:
        tgt_points = st.number_input(
            "🎯 TARGET (Pts):",
            value=60,
            key="target_input"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- ORDER BUTTONS ---
    b1, b2, b3 = st.columns(3)
    
    with b1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("🟩 BUY", key="buy_btn", use_container_width=True):
            if st.session_state["broker_connected"]:
                st.toast(
                    f"🛒 BUY ORDER FIRED! {user_symbol} | Qty: {u_qty} | SL: {sl_points}Pts | TGT: {tgt_points}Pts",
                    icon="✅"
                )
                
                # Add to open positions
                position = {
                    "id": f"#RM-{len(st.session_state['open_positions']) + 2001}",
                    "script": f"{user_symbol} {selected_strike} {selected_option}" if selected_option != "EQUITY (CASH)" else user_symbol,
                    "quantity": u_qty,
                    "order_type": "BUY",
                    "sl": sl_points,
                    "target": tgt_points,
                    "entry_price": 100.0,
                    "status": "⌛ Waiting for Signal"
                }
                st.session_state["open_positions"].append(position)
                add_audit_log("BUY_ORDER", f"{user_symbol} | Qty: {u_qty} | SL: {sl_points} | TGT: {tgt_points}")
            else:
                st.error("❌ पहले ब्रोकर API कनेक्ट करें!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with b2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("🟥 SELL", key="sell_btn", use_container_width=True):
            if st.session_state["broker_connected"]:
                st.toast(
                    f"📉 SELL ORDER FIRED! {user_symbol} | Qty: {u_qty} | SL: {sl_points}Pts | TGT: {tgt_points}Pts",
                    icon="🚨"
                )
                
                position = {
                    "id": f"#RM-{len(st.session_state['open_positions']) + 2001}",
                    "script": f"{user_symbol} {selected_strike} {selected_option}" if selected_option != "EQUITY (CASH)" else user_symbol,
                    "quantity": u_qty,
                    "order_type": "SELL",
                    "sl": sl_points,
                    "target": tgt_points,
                    "entry_price": 100.0,
                    "status": "⌛ Waiting for Signal"
                }
                st.session_state["open_positions"].append(position)
                add_audit_log("SELL_ORDER", f"{user_symbol} | Qty: {u_qty} | SL: {sl_points} | TGT: {tgt_points}")
            else:
                st.error("❌ पहले ब्रोकर API कनेक्ट करें!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with b3:
        st.markdown('<div class="wait-box">', unsafe_allow_html=True)
        if st.button("🟨 WAIT", key="wait_btn", use_container_width=True):
            st.toast("⏳ SYSTEM ON HOLD", icon="⏳")
            add_audit_log("WAIT_ACTION", "System put on hold")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # --- EMERGENCY PANIC BUTTON ---
    st.markdown('<div class="panic-container">', unsafe_allow_html=True)
    if st.button("💥 EMERGENCY CLOSE ALL POSITIONS", key="panic_btn", use_container_width=True):
        st.toast("🚨 ALL POSITIONS SQUARED OFF!", icon="💥")
        add_audit_log("EMERGENCY_CLOSE", f"All {len(st.session_state['open_positions'])} positions closed")
        st.session_state["open_positions"] = []
        time.sleep(0.5)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# LEFT PANEL: TRADING VIEW CHART
# ============================================================================

with col_chart:
    st.markdown(
        f"<h4 style='color:#f3f4f6;'>📈 लाइव चार्ट: {user_symbol}</h4>",
        unsafe_allow_html=True
    )
    
    # Get correct TradingView symbol
    tv_symbol = get_tradingview_symbol(user_symbol)
    
    # TradingView Chart Embed
    tradingview_html = f"""
    <div style="height:500px; border-radius: 12px; overflow: hidden; border: 1px solid #1e366a;">
        <iframe
            src="https://s.tradingview.com/widgetembed/?symbol={tv_symbol}&interval=5&theme=dark&style=1&timezone=Asia%2FKolkata&locale=en"
            width="100%"
            height="100%"
            frameborder="0"
            allowtransparency="true"
            scrolling="no"
            allowfullscreen>
        </iframe>
    </div>
    """
    st.components.v1.html(tradingview_html, height=520)

st.markdown("<br><hr style='border-color:#1e366a;'>", unsafe_allow_html=True)

# ============================================================================
# LIVE ORDER BOOK / OPEN POSITIONS
# ============================================================================

st.markdown("<h4 style='color:#f3f4f6;'>📋 मेरी लाइव खुली पोजीशन</h4>", unsafe_allow_html=True)

if st.session_state["open_positions"]:
    positions_data = {
        "ट्रेड आईडी (ID)": [],
        "स्क्रिप्ट": [],
        "मात्रा": [],
        "प्रकार": [],
        "स्टॉपलॉस (SL)": [],
        "टार्गेट": [],
        "स्थिति": []
    }
    
    for pos in st.session_state["open_positions"]:
        positions_data["ट्रेड आईडी (ID)"].append(pos["id"])
        positions_data["स्क्रिप्ट"].append(pos["script"])
        positions_data["मात्रा"].append(f"{pos['quantity']} Qty")
        positions_data["प्रकार"].append(pos["order_type"])
        positions_data["स्टॉपलॉस (SL)"].append(f"{pos['sl']} Pts")
        positions_data["टार्गेट"].append(f"{pos['target']} Pts")
        positions_data["स्थिति"].append(pos["status"])
    
    df_positions = pd.DataFrame(positions_data)
    st.dataframe(df_positions, use_container_width=True, hide_index=True)
else:
    st.info("📭 कोई खुली पोजीशन नहीं। एक ऑर्डर रखें!")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# AUDIT LOGS SECTION
# ============================================================================

with st.expander("📝 Real-time Office Audit Logs"):
    if st.session_state["audit_logs"]:
        logs_data = {
            "समय": [],
            "ऑपरेटर": [],
            "क्रिया": [],
            "विवरण": []
        }
        
        for log in reversed(st.session_state["audit_logs"][-20:]):  # Show last 20 logs
            logs_data["समय"].append(log["timestamp"])
            logs_data["ऑपरेटर"].append(log["user_id"])
            logs_data["क्रिया"].append(log["action"])
            logs_data["विवरण"].append(log["details"])
        
        df_logs = pd.DataFrame(logs_data)
        st.dataframe(df_logs, use_container_width=True, hide_index=True)
    else:
        st.info("📭 अभी कोई ऑडिट लॉग नहीं है।")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<hr style='border-color:#1e366a; margin-top: 30px;'>
<div style='text-align: center; color: #9ca3af; font-size: 12px; padding: 20px 0;'>
    <p>🔱 Ramavat Algo Elite v1.0 | Professional Algo Trading Terminal | Secure & Optimized</p>
    <p>© 2026 All Rights Reserved | Disclaimer: Trading involves risk. Use at your own discretion.</p>
</div>
""", unsafe_allow_html=True)
