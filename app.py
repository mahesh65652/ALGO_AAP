"""
app.py — RAMAVAT ALGO ELITE  [v4.7]
====================================
Professional Trading Terminal
Gujarati + English UI | No Hindi
Dark Premium & Light Premium Dynamic Theme Selector
Inline Chart Controls Fixed Under TradingView
"""

import streamlit as st
import time
import pandas as pd
import random
from datetime import datetime
from enum import Enum

st.set_page_config(
    page_title="Ramavat Algo Elite",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

class BrokerType(Enum):
    ANGEL_ONE  = "Angel One (SmartAPI)"
    ALICE_BLUE = "Alice Blue (ANT)"
    ZERODHA    = "Zerodha (Kite)"
    FINVASIA   = "Finvasia (Shoonya)"

# SESSION STATE
_def = {
    "authenticated":False,"user_id":None,"login_time":None,
    "broker_connected":False,"connected_broker":None,
    "broker_config":{"client_id":"","api_key":"","secret_key":"","totp_secret":""},
    "audit_logs":[],"open_positions":[],
    "dynamic_pnl":2695.0,"total_capital":150000.0,
    "max_daily_loss":5000.0,"daily_target":8000.0,
    "trail_sl_pct":0.5,"risk_per_trade":2.0,
    "auto_trade":False,"trail_active":False,"peak_pnl":0.0,
}
for k,v in _def.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- 🌓 DYNAMIC THEME SWITCHER ENGINE ---
st.sidebar.markdown("## 🎨 UI Display Settings")
theme_mode = st.sidebar.radio("તમારી મનપસંદ થીમ પસંદ કરો સાહેબ:", ["🌙 Dark Mode", "☀️ Light Mode"])

if theme_mode == "🌙 Dark Mode":
    bg_color = "#060913"
    text_color = "#e2e8f0"
    box_bg = "#0d1527"
    box_border = "#1e293b"
    tv_theme = "dark"
    metric_bg = "linear-gradient(135deg, #0d162d, #142247)"
    metric_border = "#1e366a"
else:
    bg_color = "#f8fafc"
    text_color = "#0f172a"
    box_bg = "#ffffff"
    box_border = "#cbd5e1"
    tv_theme = "light"
    metric_bg = "linear-gradient(135deg, #e2e8f0, #f1f5f9)"
    metric_border = "#cbd5e1"

st.markdown(f"""
<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    .main {{ background-color:{bg_color} !important; color:{text_color} !important; }}
    body  {{ background-color:{bg_color} !important; }}
    div[data-testid="stMetricSimpleContainer"] {{
        background: {metric_bg} !important;
        padding: 18px !important; border-radius: 12px !important;
        border: 1px solid {metric_border} !important; text-align: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }}
    .stTextInput input, .stNumberInput input, .stPasswordInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #0f172a !important; color: #e2e8f0 !important;
        border: 1px solid #1e293b !important; border-radius: 8px !important;
        padding: 2px 4px !important; font-size: 14px !important;
    }}
    .stButton > button {{
        width: 100% !important; border-radius: 10px !important;
        height: 48px !important; font-weight: 800 !important;
        font-size: 15px !important; text-transform: uppercase !important;
        border: none !important; transition: all 0.3s ease !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.4) !important;
    }}
    .buy-box button  {{ background: linear-gradient(90deg,#00c851,#007e33) !important; color:white !important; }}
    .sell-box button {{ background: linear-gradient(90deg,#ff4444,#cc0000) !important; color:white !important; }}
    .wait-box button {{ background: linear-gradient(90deg,#ffbb33,#ff8800) !important; color:white !important; }}
    
    @keyframes pulse-panic {{
        0%  {{ box-shadow: 0 0 0 0 rgba(220,38,38,0.7); }}
        70% {{ box-shadow: 0 0 0 10px rgba(220,38,38,0); }}
        100%{{ box-shadow: 0 0 0 0 rgba(220,38,38,0); }}
    }}
    .panic-container button {{
        background: linear-gradient(90deg,#7f1d1d,#dc2626) !important;
        color:white !important; border:2px solid #ef4444 !important;
        height:56px !important; font-weight:900 !important; font-size:16px !important;
        animation: pulse-panic 2s infinite !important; margin-top:15px !important;
    }}
    .config-box {{
        background-color:{box_bg} !important; padding:15px !important;
        border-radius:10px !important; border:1px solid {box_border} !important;
        margin-bottom:15px !important;
    }}
    h1,h2,h3,h4,h5,h6 {{ color:#d4af37 !important; }}
    p, span, label {{ color: {text_color} !important; }}
</style>
""", unsafe_allow_html=True)

def add_log(action, details=""):
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uid = st.session_state.get("user_id","Unknown")
    st.session_state["audit_logs"].append({"timestamp":ts,"user_id":uid,"action":action,"details":details})

def get_lot_size(sym):
    lots = {
        "NIFTY":50,"BANKNIFTY":15,"FINNIFTY":25,"MIDCPNIFTY":10,"SENSEX":10,"BANKEX":15,
        "CRUDEOIL":100,"CRUDEOILM":10,"NATURALGAS":1250,"NATGASMINI":250,
    }
    return lots.get(sym.upper().replace("-EQ",""),1)

def get_tv_symbol(sym):
    s = sym.upper().strip().replace("-EQ", "")
    index_mp = {"NIFTY": "NSE:NIFTY1!", "BANKNIFTY": "NSE:BANKNIFTY1!", "CRUDEOIL": "MCX:CRUDEOIL1!", "NATURALGAS": "MCX:NATURALGAS1!"}
    return index_mp.get(s, f"NSE:{s}")

# LOGIN GATEWAY (UNCHANGED FROM v2.0)
if not st.session_state["authenticated"]:
    st.markdown("<div style='text-align:center;padding:40px 0;'><h1>🔱 RAMAVAT ALGO ELITE</h1><p>🏢 PROFESSIONAL ALGO TRADING TERMINAL v2.0</p></div>", unsafe_allow_html=True)
    _,cm,_ = st.columns([1,2,1])
    with cm:
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>🔐 SECURE SYSTEM ACCESS</h3>", unsafe_allow_html=True)
        lu = st.text_input("👤 User ID:", key="lu")
        lp = st.text_input("🔑 Password:", type="password", key="lp")
        if st.button("🚀 ACCESS ACCOUNT", use_container_width=True):
            if lu and lp == "1234":
                st.session_state.update({"authenticated":True,"user_id":lu,"login_time":datetime.now()})
                st.rerun()
            else: st.error("❌ ખોટો Password!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# MAIN TERMINAL HEADER
hl, hr = st.columns([4,1])
with hl:
    st.markdown("<div style='text-align:center;margin-bottom:10px;'><h1>🔱 RAMAVAT ALGO ELITE</h1></div>", unsafe_allow_html=True)
with hr:
    if st.button("🚪 Exit System", key="lo"):
        st.session_state["authenticated"] = False; st.rerun()

# TELEMETRY DISPLAY
m1,m2,m3,m4 = st.columns(4)
pnl = st.session_state["dynamic_pnl"]
m1.metric("📊 Live Net P&L", f"₹ {pnl:,.2f}")
m2.metric("💰 Account Capital", f"₹ {st.session_state['total_capital']:,.0f}")
m3.metric("🎯 Open Positions", f"{len(st.session_state['open_positions'])} Active")
m4.metric("🔌 API Gateway Status", "Connected ✅" if st.session_state["broker_connected"] else "Disconnected ❌")

st.markdown("<br>", unsafe_allow_html=True)

# 📊 TWO COLUMN WORKING SPLIT
col_chart, col_ctrl = st.columns([1.2, 1])

with col_chart:
    # 📈 REAL-TIME ADVANCED CHART
    usym = st.text_input("🏷️ Base Asset Symbol:", value="CRUDEOIL", key="usym").strip().upper()
    tv = get_tv_symbol(usym)
    
    st.components.v1.html(f"""
    <div style="height:400px;border-radius:12px;overflow:hidden;border:1px solid #1e366a;">
        <iframe src="https://s.tradingview.com/widgetembed/?symbol={tv}&interval=5&theme={tv_theme}&style=1&timezone=Asia%2FKolkata&locale=en"
            width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
    </div>""", height=410)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🕹️ ચાર્ટની નીચે જરૂરી બટન લુક જે લાઇન સર દેખાય તેવા (Inline Executive Row)
    st.markdown("#### ⚡ Quick Inline Execution Dock")
    b_col1, b_col2, b_col3, b_col4 = st.columns([1, 1.2, 1.2, 1.5])
    
    ls = get_lot_size(usym)
    with b_col1:
        ulots = st.number_input("Lots:", min_value=1, value=1, key="ulots", label_visibility="collapsed")
    with b_col2:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("🟩 BUY LONG", key="bb", use_container_width=True):
            st.session_state["open_positions"].append({"id": f"#RM-{random.randint(1000,9999)}", "script": usym, "qty": ulots*ls, "action": "BUY", "status": "🟢 Executed", "mode": "LIVE"})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with b_col3:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("🟥 SELL SHORT", key="sb", use_container_width=True):
            st.session_state["open_positions"].append({"id": f"#RM-{random.randint(1000,9999)}", "script": usym, "qty": ulots*ls, "action": "SELL", "status": "🟢 Executed", "mode": "LIVE"})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with b_col4:
        st.markdown('<div class="panic-container" style="margin-top:-15px;">', unsafe_allow_html=True)
        if st.button("💥 PANIC SQR-OFF", key="panic", use_container_width=True):
            st.session_state["open_positions"] = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with col_ctrl:
    # 🔌 BROKER CONFIG
    with st.expander("🔌 1. Client API & TOTP Gateway Setup", expanded=True):
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        sel_broker = st.selectbox("🌐 Choose Broker Engine:", [b.value for b in BrokerType], key="bsel")
        ucid = st.text_input("👤 Client Account ID:", key="ucid", value=st.session_state["broker_config"]["client_id"])
        uapi = st.text_input("🔑 SmartAPI Key:", type="password", key="uapi", value=st.session_state["broker_config"]["api_key"])
        utotp= st.text_input("⏳ TOTP Token Secret:", type="password", key="utotp", value=st.session_state["broker_config"]["totp_secret"])
        
        if st.button("🔌 LINK BROKER ENGINE", key="conn"):
            if ucid and uapi:
                st.session_state.update({"broker_connected":True,"connected_broker":sel_broker,"broker_config":{"client_id":ucid,"api_key":uapi,"secret_key":"","totp_secret":utotp}})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# POSITIONS DATA ROOM
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("### 📋 Active Positions Ledger")
if st.session_state["open_positions"]:
    st.dataframe(pd.DataFrame(st.session_state["open_positions"]), use_container_width=True, hide_index=True)
else:
    st.info("📭 કોઈ સક્રિય પોઝિશન બજારમાં નથી.")
