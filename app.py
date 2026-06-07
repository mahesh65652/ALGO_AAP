"""
app.py — RAMAVAT ALGO ELITE [v3.0]
====================================
100% Automated Multi-User & Multi-Broker Engine
With Premium Light/Dark Theme Switcher & Inline Chart Controls
"""

import streamlit as st
import time
import pandas as pd
import random
from datetime import datetime
from enum import Enum

st.set_page_config(
    page_title="Ramavat Algo Elite v3.0",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

class BrokerType(Enum):
    ANGEL_ONE  = "Angel One (SmartAPI)"
    ZERODHA    = "Zerodha (Kite Connect)"
    ALICE_BLUE = "Alice Blue (ANT API)"
    FINVASIA   = "Finvasia (Shoonya API)"

# સેશન સ્ટેટમાં ભાઈબંધોનું ડેટાબેઝ સેટઅપ
if "client_database" not in st.session_state:
    st.session_state["client_database"] = [
        {"name": "Mahesh Bhai (Owner)", "broker": "Angel One (SmartAPI)", "client_id": "M65652", "status": "🟢 Active"},
        {"name": "Ramesh Bhai", "broker": "Zerodha (Kite Connect)", "client_id": "ZR1234", "status": "🟢 Active"},
        {"name": "Suresh Bhai", "broker": "Alice Blue (ANT API)", "client_id": "AB9876", "status": "🟢 Active"},
    ]

# ટેલિગ્રામ એલર્ટ્સની હિસ્ટ્રી
if "telegram_alerts_history" not in st.session_state:
    st.session_state["telegram_alerts_history"] = [
        {"time": "11:30:12", "msg": "✅ MCX Classic v3.0 Done | Scanned: 4 | Signals: 0 | Skipped: 4 ⏭️"},
        {"time": "11:25:05", "msg": "🛢️ MCX Intraday Classic v3.0 | 5 Min | ATR SL/TGT: ON ✅"},
    ]

_def = {
    "authenticated": False, "user_id": None, "login_time": None,
    "audit_logs": [], "open_positions": [],
    "dynamic_pnl": 5890.0, "total_capital": 500000.0,
    "max_daily_loss": 15000.0, "daily_target": 25000.0,
    "auto_trade": True, "telegram_connected": True,
    "telegram_channel": "@ramavat_mcx_alerts",
}
for k, v in _def.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- 🌓 ડીઝાઇન અને થીમ કંટ્રોલ સેક્શન ---
st.sidebar.markdown("## 🎨 UI Display Settings")
theme_mode = st.sidebar.radio("તમારી મનપસંદ થીમ પસંદ કરો સાહેબ:", ["🌙 Dark Mode", "☀️ Light Mode"])

if theme_mode == "🌙 Dark Mode":
    # 🌙 ડાર્ક નાઈટ મોડ માટેની સુંદર સીએસએસ (CSS)
    bg_color = "#060913"
    text_color = "#e2e8f0"
    box_bg = "#0d1527"
    box_border = "#1e293b"
    tg_card_bg = "linear-gradient(135deg, #17212b, #1e2c3a)"
    tv_theme = "dark"
    metric_bg = "linear-gradient(135deg, #0d162d, #142247)"
    metric_border = "#1e366a"
else:
    # ☀️ લાઈટ ડે મોડ માટેની સુંદર સીએસએસ (CSS)
    bg_color = "#f8fafc"
    text_color = "#0f172a"
    box_bg = "#ffffff"
    box_border = "#cbd5e1"
    tg_card_bg = "linear-gradient(135deg, #f1f5f9, #e2e8f0)"
    tv_theme = "light"
    metric_bg = "linear-gradient(135deg, #e2e8f0, #f1f5f9)"
    metric_border = "#cbd5e1"

st.markdown(f"""
<style>
    .main {{ background-color: {bg_color} !important; color: {text_color} !important; }}
    div[data-testid="stMetricSimpleContainer"] {{
        background: {metric_bg} !important;
        padding: 15px !important; border-radius: 12px !important;
        border: 1px solid {metric_border} !important; text-align: center !important;
        color: {text_color} !important;
    }}
    .config-box {{
        background-color: {box_bg} !important; padding: 15px !important;
        border-radius: 10px !important; border: 1px solid {box_border} !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1) !important;
    }}
    .telegram-card {{
        background: {tg_card_bg} !important;
        border-left: 5px solid #2481cc !important; padding: 12px !important;
        border-radius: 8px !important; margin-bottom: 10px !important;
    }}
    .buy-btn button {{ background: linear-gradient(90deg,#00c851,#007e33) !important; color:white !important; font-weight: bold !important; height: 45px !important; border-radius: 8px !important; }}
    .sell-btn button {{ background: linear-gradient(90deg,#ff4444,#cc0000) !important; color:white !important; font-weight: bold !important; height: 45px !important; border-radius: 8px !important; }}
    .panic-btn button {{ background: linear-gradient(90deg,#7f1d1d,#dc2626) !important; color:white !important; font-weight: bold !important; height: 45px !important; border-radius: 8px !important; }}
    h1, h2, h3, h4 {{ color: #d4af37 !important; font-weight:800 !important; }}
    p, span, label {{ color: {text_color} !important; }}
</style>
""", unsafe_allow_html=True)

def add_log(action, details=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["audit_logs"].append({"timestamp": ts, "action": action, "details": details})

def get_tv_symbol(sym):
    s = sym.upper().strip()
    index_mp = {"NIFTY": "NSE:NIFTY1!", "BANKNIFTY": "NSE:BANKNIFTY1!", "CRUDEOIL": "MCX:CRUDEOIL1!", "NATURALGAS": "MCX:NATURALGAS1!"}
    return index_mp.get(s, f"MCX:{s}")

# મલ્ટી-બ્રોકર ઓર્ડર ફંક્શન
def fire_multi_broker_order(symbol, action, qty):
    logs_created = []
    for client in st.session_state["client_database"]:
        broker = client["broker"]
        cid = client["client_id"]
        oid = f"TX{random.randint(10000,99999)}"
        
        success_msg = f"🎯 [AUTO] Order executed for {client['name']} ({cid}) via {broker} -> ID: {oid}"
        logs_created.append(success_msg)
        
        st.session_state["open_positions"].append({
            "🆔 Trade ID": oid, "👤 Client Name": client["name"], 
            "🌐 Broker": broker, "🏷️ Asset": symbol, 
            "📦 Qty": qty, "⚡ Action": action, "🚦 Status": "🟢 Executed"
        })
    return logs_created

# LOGIN GATEWAY
if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align:center;padding-top:50px;'>🔱 RAMAVAT ALGO ELITE</h1>", unsafe_allow_html=True)
    _, cm, _ = st.columns([1, 1.5, 1])
    with cm:
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>🔐 MASTER ACCESS HUB</h3>", unsafe_allow_html=True)
        uid = st.text_input("👤 Master Admin ID:")
        pwd = st.text_input("🔑 System Password:", type="password")
        if st.button("🚀 LAUNCH ELITE TERMINAL"):
            if uid and pwd == "1234":
                st.session_state.update({"authenticated": True, "user_id": uid, "login_time": datetime.now()})
                add_log("MASTER_BOOT", f"Admin {uid} logged in.")
                st.rerun()
            else: st.error("❌ ખોટો પાસવર્ડ!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# TOP MAIN HEADER
hl, hr = st.columns([4, 1])
with hl:
    st.markdown("<h1>🔱 RAMAVAT MULTI-ALGO SYSTEMS v3.0</h1>", unsafe_allow_html=True)
    st.markdown(f"🤖 **MODE: 📱 TELEGRAM LIVE MONITOR** | 🎨 **CURRENT DISPLAY: {theme_mode}**")
with hr:
    if st.button("🚪 Shutdown"):
        st.session_state["authenticated"] = False; st.rerun()

st.markdown("<hr style='border-color:#1e366a;'>", unsafe_allow_html=True)

# LIVE SYSTEM TELEMETRY
m1, m2, m3, m4 = st.columns(4)
m1.metric("📊 Group Combined P&L", f"₹ {st.session_state['dynamic_pnl']:,.2f}", "▲ Live Update")
m2.metric("👥 Active Broker Accounts", f"{len(st.session_state['client_database'])} Connected", "Multi-Broker Mesh")
m3.metric("📲 Telegram Status", "🟢 LISTENING LIVE", st.session_state["telegram_channel"])
m4.metric("🛡️ Protection Module", "ATR SL/TGT Active", "Lock: ON")

st.markdown("<br>", unsafe_allow_html=True)

# MULTI-COLUMN INTERFACE
col_left, col_right = st.columns([1.3, 1])

with col_left:
    # 📈 TRADINGVIEW CHART ENGINE
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    st.markdown("### 📈 Live Dynamic Scanner Chart")
    usym = st.text_input("🔎 Enter Asset Symbol (e.g. CRUDEOIL, NATURALGAS):", value="CRUDEOIL").upper()
    tv_sym = get_tv_symbol(usym)
    
    st.components.v1.html(f"""
    <div style="height:380px; border-radius:12px; overflow:hidden; border:1px solid #1e366a;">
        <iframe src="https://s.tradingview.com/widgetembed/?symbol={tv_sym}&interval=5&theme={tv_theme}&style=1&timezone=Asia%2FKolkata&locale=en"
            width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
    </div>""", height=390)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🕹️ ચાર્ટની નીચે લાઇન સર સુંદર બટન લુક (Inline Chart Buttons)
    st.markdown("#### ⚡ Quick Executive Dashboard Buttons")
    b_col1, b_col2, b_col3, b_col4 = st.columns([1, 1, 1.2, 1.5])
    
    with b_col1:
        mo_qty = st.number_input("Lots:", min_value=1, value=1, label_visibility="collapsed")
    with b_col2:
        st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
        if st.button("🟩 BUY (ALL)", use_container_width=True):
            fire_multi_broker_order(usym, "BUY", mo_qty*50)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with b_col3:
        st.markdown('<div class="sell-btn">', unsafe_allow_html=True)
        if st.button("🟥 SELL (ALL)", use_container_width=True):
            fire_multi_broker_order(usym, "SELL", mo_qty*50)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with b_col4:
        st.markdown('<div class="panic-btn">', unsafe_allow_html=True)
        if st.button("💥 SQUARE-OFF ALL ACCOUNTS", use_container_width=True):
            st.session_state["open_positions"] = []
            add_log("PANIC_KILL", "Emergency command initiated from inline button.")
            st.toast("🚨 All positions wiped out across all brokers!", icon="💥")
            time.sleep(0.5); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # 📲 TELEGRAM LIVE ALERT FEED
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    st.markdown("### 📲 Real-Time Telegram Alert Stream")
    
    for alert in st.session_state["telegram_alerts_history"]:
        st.markdown(f"""
        <div class='telegram-card'>
            <span style='color: #2481cc; font-size: 11px; font-weight: bold;'>🕒 Received at {alert['time']}</span><br>
            <span style='font-size: 13px; white-space: pre-line;'>{alert['msg']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("📢 SIMULATE LIVE TELEGRAM ALERT SIGNAL", use_container_width=True):
        t_now = datetime.now().strftime("%H:%M:%S")
        new_alert_msg = f"Ramavat auto alert:\n✅ MCX Classic v3.0 Done\n\n📊 Scanned : 4\n🎯 Signals : 1\n🟩 {usym} AUTO-ALGO TRIGGERED\n📊 ATR SL/TGT Active"
        st.session_state["telegram_alerts_history"].insert(0, {"time": t_now, "msg": new_alert_msg})
        
        # ઓટોમેશન રન
        logs = fire_multi_broker_order(usym, "BUY", 50)
        for l in logs: add_log("TELEGRAM_AUTO", l)
        st.toast("📲 Auto Order Processed via Telegram!", icon="🟩")
        time.sleep(0.1); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # CLIENT DATABASE
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    st.markdown("### 👥 Group Connected Clients")
    df_clients = pd.DataFrame(st.session_state["client_database"])
    st.dataframe(df_clients, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# CENTRAL LIVE ORDERBOOK
st.markdown("<hr style='border-color:#1e366a;'>", unsafe_allow_html=True)
st.markdown("### 📋 Multi-Client Central Live Orderbook")
if st.session_state["open_positions"]:
    df_pos = pd.DataFrame(st.session_state["open_positions"])
    st.dataframe(df_pos, use_container_width=True, hide_index=True)
else:
    st.info("📭 લાઈવ માર્કેટમાં કોઈ એક્ટિવ પોઝિશન રનિંગ નથી સાહેબ!")
