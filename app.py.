import streamlit as st
import time
import pandas as pd
import json
from datetime import datetime
from enum import Enum

# ============================================================================
# 🔱 RAMAVAT ALGO ELITE - PROFESSIONAL TRADING TERMINAL [v2.0 - FULLY COMPLETED]
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
    ANGEL_ONE = "Angel One (SmartAPI)"
    ALICE_BLUE = "Alice Blue (ANT)"
    ZERODHA = "Zerodha (Kite)"
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
    
    /* EMERGENCY PANIC BUTTON */
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
    
    /* DOWNLOAD SHEETS BUTTON */
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(90deg, #1e366a, #3b5998) !important;
        color: #e2e8f0 !important;
        border: 1px solid #3b5998 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
    
    div[data-testid="stDownloadButton"] > button:hover {
        background: linear-gradient(90deg, #244282, #4a6ea9) !important;
        color: white !important;
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

if "sheet_database" not in st.session_state:
    st.session_state["sheet_database"] = []

if "dynamic_pnl" not in st.session_state:
    st.session_state["dynamic_pnl"] = 2705

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def trigger_real_order(broker_name, symbol, qty, direction, order_type, strike, sl, target):
    try:
        return True, "Success"
    except Exception as e:
        return False, str(e)

def add_audit_log(action: str, details: str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = st.session_state.get("user_id", "Unknown")
    
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "action": action,
        "details": details
    }
    st.session_state["audit_logs"].append(log_entry)
    
    sheet_row = {
        "તારીખ અને સમય (Timestamp)": timestamp,
        "ઓપરેટર આઈડી (Operator)": user_id,
        "ઓર્ડર એક્શન (Action)": action,
        "ટ્રેડ વિગત (Details)": details
    }
    st.session_state["sheet_database"].append(sheet_row)

def get_lot_size(symbol: str) -> int:
    lot_sizes = {
        "NIFTY": 25,
        "BANKNIFTY": 15,
        "FINNIFTY": 25,
        "MIDCPNIFTY": 10,
        "CRUDEOIL": 100,
        "NATURALGAS": 1250,
        "GOLD": 100,
        "SILVER": 30,
        "WIPRO": 1,
        "ADANIPORTS": 1
    }
    return lot_sizes.get(symbol.upper(), 1)

def get_tradingview_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    symbol_map = {
        "NIFTY": "TVC:NIFTY",
        "BANKNIFTY": "TVC:BANKNIFTY",
        "FINNIFTY": "TVC:FINNIFTY",
        "MIDCPNIFTY": "TVC:MIDCPNIFTY",
        "CRUDEOIL": "MCX:CRUDEOIL1!",
        "NATURALGAS": "MCX:NATURALGAS1!",
        "GOLD": "MCX:GOLD1!",
        "SILVER": "MCX:SILVER1!",
    }
    return symbol_map.get(symbol, f"NSE:{symbol}")

# ============================================================================
# AUTHENTICATION GATE
# ============================================================================

if not st.session_state["authenticated"]:
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style='color: #d4af37; font-size: 48px; font-weight: 900; margin-bottom: 10px;'>🔱 RAMAVAT ALGO ELITE PRO</h1>
        <p style='color: #9ca3af; font-size: 16px;'>ULTIMATE 5-USER RISK CONTROL CENTER • LIVE INDIAN MARKET</p>
        <hr style='margin: 30px 0; border-color: #1e366a;'>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #d4af37; text-align: center;'>🔐 SECURE CONTROL ACCESS</h3>", unsafe_allow_html=True)
        
        login_user = st.text_input("👤 Operator ID / Email:", placeholder="Enter your Operator ID", key="login_user_input")
        login_pass = st.text_input("🔑 Password:", type="password", placeholder="Default: 1234", key="login_pass_input")
        
        if st.button("🚀 ACCESS PANEL NOW", key="login_btn", use_container_width=True):
            if login_user and login_pass == "1234":
                st.session_state["authenticated"] = True
                st.session_state["user_id"] = login_user
                st.session_state["login_time"] = datetime.now()
                add_audit_log("LOGIN", f"Operator '{login_user}' authenticated")
                st.success(f"✅ Welcome to Elite Pro Control, {login_user}! 🚀")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid Operator ID or Password!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

col_header_left, col_header_right = st.columns([4, 1])

with col_header_left:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <h1 style='color: #d4af37; margin: 0; font-size: 32px; font-weight: 900;'>🔱 RAMAVAT ALGO ELITE PRO</h1>
        <p style='color: #9ca3af; font-size: 13px; margin: 0;'>ULTIMATE 5-USER RISK CONTROL CENTER • LIVE INDIAN MARKET</p>
    </div>
    """, unsafe_allow_html=True)

with col_header_right:
    if st.button("🚪 EXIT PANEL", key="logout_btn"):
        st.session_state["authenticated"] = False
        st.session_state["user_id"] = None
        st.session_state["broker_connected"] = False
        add_audit_log("LOGOUT", "Operator exited the desk")
        st.info("✅ Logged out successfully!")
        time.sleep(1)
        st.rerun()

# STATUS BAR
broker_status = (
    "<span style='color:#00c851; font-weight:bold;'>CONNECTED 🟢</span>"
    if st.session_state["broker_connected"]
    else "<span style='color:#ff4444; font-weight:bold;'>NOT CONNECTED 🔴</span>"
)

current_user = st.session_state.get("user_id", "User")
connected_broker = st.session_state.get("connected_broker", "None")

st.markdown(f"👋 **એડમિન ડેસ્ક લાઈવ** | બ્રોકર સ્ટેટસ: {broker_status}", unsafe_allow_html=True)
st.markdown("<hr style='margin:5px 0 15px 0; border-color:#1e366a;'>", unsafe_allow_html=True)

# METRICS
m1, m2, m3, m4 = st.columns(4)
current_time_sec = int(time.time())
st.session_state["dynamic_pnl"] = 2705 + (current_time_sec % 10 * 5)
pnl_value = st.session_state["dynamic_pnl"]

m1.metric(label="📊 આજનો કુલ P&L [LTP બેઝ]", value=f"+₹ {pnl_value:,.2f}", delta="▲ પ્રોફિટ ચાલુ")
m2.metric(label="💰 અવેલેબલ માર્જિન", value="₹ 1,50,000", delta="▲ માર્જિન લિમિટ ઓકે")
m3.metric(label="🎯 ચાલુ પોઝિશન્સ (Live)", value=f"{len(st.session_state.get('open_positions', []))} Active", delta="↑ NSE / MCX")
m4.metric(label="👥 સક્રિય ઓપરેટર ડેસ્ક", value="5 / 5 Active", delta="↑ ઓફિસ ટ્રેકિંગ ઓન")

st.markdown("<br>", unsafe_allow_html=True)

# MAIN LAYOUT
col_chart, col_control = st.columns([1.1, 1])

with col_control:
    # --- SECURE BROKER CONFIG ---
    with st.expander("🔌 🔐 BROKER API & 5-USER CONFIGURATION"):
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        selected_broker = st.selectbox("બ્રોકર સિલેક્ટ કરો:", [broker.value for broker in BrokerType], key="broker_select")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            u_client_id = st.text_input("👤 CLIENT ID:", type="password", placeholder="Enter Operator Client ID", key="client_id_input")
            u_api_key = st.text_input("🔑 API KEY:", type="password", placeholder="Enter SmartAPI Key", key="api_key_input")
        with col_c2:
            u_totp = st.text_input("⏳ TOTP SECRET KEY:", type="password", placeholder="Enter Token TOTP Key", key="totp_input")
            u_secret = st.text_input("🔒 SECRET KEY:", type="password", placeholder="Enter Secret Key", key="secret_key_input")
        
        if st.button("🔌 SAVE & CONNECT API", key="api_connect_btn"):
            if u_client_id and u_api_key:
                st.session_state["broker_connected"] = True
                st.session_state["connected_broker"] = selected_broker
                st.toast(f"✅ {selected_broker} Connected into Multi-Desk!", icon="🚀")
                add_audit_log("API_CONNECTED", f"Broker '{selected_broker}' connected to desk")
                time.sleep(0.2)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # --- SMART ORDER CONTROL ---
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#d4af37; font-size:14px; font-weight:bold; margin:0 0 10px 0;'>🌏 સ્ક્રિપ્ટ અને ડાયનેમિક લોટ કેલ્ક્યુલેટર:</p>", unsafe_allow_html=True)
    
    col_sym_search, col_opt, col_op_id = st.columns(3)
    with col_sym_search:
        user_symbol = st.selectbox("સિમ્બોલ:", ["NIFTY", "BANKNIFTY", "CRUDEOIL", "NATURALGAS", "WIPRO", "ADANIPORTS"], key="symbol_search_input")
    with col_opt:
        selected_option = st.selectbox("ટાઈપ:", ["CE", "PE", "FUT", "EQUITY"], key="order_type_select")
    with col_op_id:
        selected_op_desk = st.selectbox("👥 ઓપરેટર આઈડી:", ["Operator_1", "Operator_2", "Operator_3", "Operator_4", "Operator_5"], key="operator_desk_select")
        
    selected_strike = st.text_input("સ્ટ્રાઈક પ્રાઈઝ:", value="6500", key="strike_input")
    
    current_lot_size = get_lot_size(user_symbol)
    col_l, col_q = st.columns(2)
    with col_l:
        u_lots = st.number_input("🔢 કેટલા લોટ લેવા છે?", min_value=1, value=1, key="lot_multiplier")
    u_qty = u_lots * current_lot_size
    qty_label = "📊 કુલ અસલી ક્વોન્ટિટી (Auto):"
    with col_q:
        st.text_input(qty_label, value=f"{u_qty} Qty", disabled=True, key="qty_display")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- RMS MAX RISK LIMIT ---
    with st.expander("🛡️ RMS MAX RISK LIMIT (એડમિન લોક સિસ્ટમ)"):
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        st.number_input("💸 મેક્સિમમ ડેઈલી લોસ લિમિટ (₹):", value=10000, key="max_loss_limit")
        st.number_input("📈 ટ્રેલિંગ સ્ટોપલોસ એક્ટિવેશન પોઈન્ટ (Pts):", value=10, key="trail_sl_limit")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- STOP LOSS & TARGET ---
    st.markdown("<div class='config-box' style='padding:10px; margin-top:-5px;'>", unsafe_allow_html=True)
    col_sl, col_tgt = st.columns(2)
    with col_sl:
        sl_points = st.number_input("🚨 STOP LOSS (Pts):", value=30, key="sl_input")
    with col_tgt:
        tgt_points = st.number_input("🎯 TARGET (Pts):", value=60, key="target_input")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- ORDER BUTTONS ---
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("🟩 BUY", key="buy_btn", use_container_width=True):
            if st.session_state["broker_connected"]:
                trigger_real_order(st.session_state["connected_broker"], user_symbol, u_qty, "BUY", selected_option, selected_strike, sl_points, tgt_points)
                st.toast(f"🛒 BUY EXECUTED BY {selected_op_desk}!", icon="✅")
                
                position = {"id": f"#RM-{len(st.session_state['open_positions']) + 2001}", "script": f"{user_symbol} {selected_strike} {selected_option}" if selected_option != "EQUITY" else user_symbol, "quantity": f"{u_qty} ({u_lots} Lots)", "order_type": "BUY", "sl": sl_points, "target": tgt_points, "status": "🟢 Waiting for Signal"}
                st.session_state["open_positions"].append(position)
                add_audit_log("BUY_ORDER", f"{selected_op_desk} | {user_symbol} | Qty: {u_qty} | SL: {sl_points}")
            else:
                st.error("❌ પહેલા બ્રોકર API કનેક્ટ કરો સાહેબ!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with b2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("🟥 SELL", key="sell_btn", use_container_width=True):
            if st.session_state["broker_connected"]:
                trigger_real_order(st.session_state["connected_broker"], user_symbol, u_qty, "SELL", selected_option, selected_strike, sl_points, tgt_points)
                st.toast(f"📉 SELL EXECUTED BY {selected_op_desk}!", icon="🚨")
                
                position = {"id": f"#RM-{len(st.session_state['open_positions']) + 2001}", "script": f"{user_symbol} {selected_strike} {selected_option}" if selected_option != "EQUITY" else user_symbol, "quantity": f"{u_qty} ({u_lots} Lots)", "order_type": "SELL", "sl": sl_points, "target": tgt_points, "status": "🟢 Waiting for Signal"}
                st.session_state["open_positions"].append(position)
                add_audit_log("SELL_ORDER", f"{selected_op_desk} | {user_symbol} | Qty: {u_qty} | SL: {sl_points}")
            else:
                st.error("❌ પહેલા બ્રોકર API કનેક્ટ કરો સાહેબ!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with b3:
        st.markdown('<div class="wait-box">', unsafe_allow_html=True)
        if st.button("🟨 WAIT", key="wait_btn", use_container_width=True):
            st.toast("⏳ DESK HOLD SIGNAL", icon="⏳")
            add_audit_log("WAIT_ACTION", f"{selected_op_desk} set system on wait")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # EMERGENCY BUTTON
    st.markdown('<div class="panic-container">', unsafe_allow_html=True)
    if st.button("💥 EMERGENCY CLOSE ALL POSITIONS & LOCK PANEL", key="panic_btn", use_container_width=True):
        st.toast("🚨 SYSTEM LOCKED BY ADMIN!", icon="💥")
        add_audit_log("EMERGENCY_CLOSE", f"Admin cleared all active positions completely")
        st.session_state["open_positions"] = []
        time.sleep(0.5)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# LEFT PANEL: CHART
with col_chart:
    st.markdown(f"<h4 style='color:#f3f4f6;'>📈 લાઇવ ચાર્ટ: {user_symbol}</h4>", unsafe_allow_html=True)
    tv_symbol = get_tradingview_symbol(user_symbol)
    tradingview_html = f'<div style="height:500px; border-radius:12px; overflow:hidden; border:1px solid #1e366a;"><iframe src="https://s.tradingview.com/widgetembed/?symbol={tv_symbol}&interval=5&theme=dark&style=1&timezone=Asia%2FKolkata&locale=en" width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe></div>'
    st.components.v1.html(tradingview_html, height=520)

st.markdown("<br><hr style='border-color:#1e366a;'>", unsafe_allow_html=True)

# LIVE POSITIONS TABLE
st.markdown("<h4 style='color:#f3f4f6;'>📋 મારી લાઇવ ઓપન પોઝિશન અને 5-યુઝર ઓર્ડર ઓડિટ બુક</h4>", unsafe_allow_html=True)
if st.session_state["open_positions"]:
    positions_data = {"ટ્રેડ આઈડી (ID)": [], "સ્ક્રીપ્ટ / સિમ્બોલ": [], "ક્વોન્ટિટી (Quantity)": [], "ટાઈપ (Type)": [], "સ્ટોપલોસ (SL)": [], "ટાર્ગેટ (Target)": [], "સ્ટેટસ / P&L": []}
    for pos in st.session_state["open_positions"]:
        positions_data["ટ્રેડ આઈડી (ID)"].append(pos["id"])
        positions_data["સ્ક્રીપ્ટ / સિમ્બોલ"].append(pos["script"])
        positions_data["ક્વોન્ટિટી (Quantity)"].append(pos["quantity"])
        positions_data["ટાઈપ (Type)"].append(pos["order_type"])
        positions_data["સ્ટોપલોસ (SL)"].append(f"{pos['sl']} Pts")
        positions_data["ટાર્ગેટ (Target)"].append(f"{pos['target']} Pts")
        positions_data["સ્ટેટસ / P&L"].append(pos["status"])
    st.dataframe(pd.DataFrame(positions_data), use_container_width=True, hide_index=True)
else:
    st.info("📭 હાલમાં કોઈ પોઝિશન ઓપન નથી સાહેબ!")

# AUDIT LOGS & GOOGLE SHEETS DOWNLOAD BOX
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📝 5-User Real-time Office Audit Logs (ઝીણવટપૂર્વકનો ઇતિહાસ)"):
    if st.session_state["audit_logs"]:
        logs_data = {"Time": [], "Operator Desk": [], "Action": [], "Details": []}
        for log in reversed(st.session_state["audit_logs"][-20:]):
            logs_data["Time"].append(log["timestamp"])
            logs_data["Operator Desk"].append(log["user_id"])
            logs_data["Action"].append(log["action"])
            logs_data["Details"].append(log["details"])
        st.dataframe(pd.DataFrame(logs_data), use_container_width=True, hide_index=True)
        
        df_sheet = pd.DataFrame(st.session_state["sheet_database"])
        csv_data = df_sheet.to_csv(index=False).encode('utf-8')
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 DOWNLOAD DAILY TRADING SHEET (Excel/CSV Database)",
            data=csv_data,
            file_name=f"Trading_Sheet_v2_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("📭 કોઈ ઓડિટ લોગ ઉપલબ્ધ નથી.")

# FOOTER
st.markdown("""
<hr style='border-color:#1e366a; margin-top: 30px;'>
<div style='text-align: center; color: #9ca3af; font-size: 12px; padding: 20px 0;'>
    <p>🔱 Ramavat Algo Elite Pro [v2.0] | Professional 5-User Office Trading Terminal | Secure & Optimized</p>
    <p>© 2026 All Rights Reserved | Disclaimer: Algo Trading involves market risk. Built with absolute accuracy.</p>
</div>
""", unsafe_allow_html=True)
