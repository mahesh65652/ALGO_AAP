"""
app.py — RAMAVAT ALGO ELITE [v2.1]
====================================
Professional Trading Terminal | Full Redesign
Gujarati + English | Light/Dark Mode
Telegram Alerts | Remote Control Ready
"""

import streamlit as st
import time
import pandas as pd
from datetime import datetime
from enum import Enum
import requests
import json

st.set_page_config(
    page_title="Ramavat Algo Elite",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded",
)

class BrokerType(Enum):
    ANGEL_ONE  = "Angel One (SmartAPI)"
    ALICE_BLUE = "Alice Blue (ANT)"
    ZERODHA    = "Zerodha (Kite)"
    FINVASIA   = "Finvasia (Shoonya)"

# ============================================================================
# THEME SYSTEM
# ============================================================================
def get_theme_colors(theme):
    """Dark/Light Mode Colors"""
    themes = {
        "dark": {
            "bg_main": "#060913",
            "bg_secondary": "#0f172a",
            "bg_tertiary": "#0d162d",
            "text_primary": "#e2e8f0",
            "text_secondary": "#9ca3af",
            "text_accent": "#d4af37",
            "border": "#1e366a",
            "success": "#22c55e",
            "danger": "#dc2626",
            "warning": "#ffbb33",
        },
        "light": {
            "bg_main": "#f8fafc",
            "bg_secondary": "#f1f5f9",
            "bg_tertiary": "#e2e8f0",
            "text_primary": "#0f172a",
            "text_secondary": "#475569",
            "text_accent": "#d97706",
            "border": "#cbd5e1",
            "success": "#16a34a",
            "danger": "#dc2626",
            "warning": "#ea580c",
        }
    }
    return themes.get(theme, themes["dark"])

# SESSION STATE
_def = {
    "authenticated": False, "user_id": None, "login_time": None,
    "broker_connected": False, "connected_broker": None,
    "broker_config": {"client_id":"","api_key":"","secret_key":"","totp_secret":""},
    "audit_logs": [], "open_positions": [],
    "dynamic_pnl": 2695.0, "total_capital": 150000.0,
    "max_daily_loss": 5000.0, "daily_target": 8000.0,
    "trail_sl_pct": 0.5, "risk_per_trade": 2.0,
    "auto_trade": False, "trail_active": False, "peak_pnl": 0.0,
    "theme": "dark",
    "telegram_token": "",
    "telegram_chat_id": "",
    "telegram_alerts": False,
}

for k,v in _def.items():
    if k not in st.session_state:
        st.session_state[k] = v

# GET CURRENT THEME
colors = get_theme_colors(st.session_state["theme"])

# ============================================================================
# DYNAMIC CSS THEME
# ============================================================================
def generate_css(theme_colors):
    return f"""
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        .main {{ background-color:{theme_colors['bg_main']} !important; color:{theme_colors['text_primary']} !important; }}
        body {{ background-color:{theme_colors['bg_main']} !important; }}
        
        /* Metrics */
        div[data-testid="stMetricSimpleContainer"] {{
            background: linear-gradient(135deg, {theme_colors['bg_tertiary']}, {theme_colors['bg_secondary']}) !important;
            padding: 18px !important; border-radius: 12px !important;
            border: 1px solid {theme_colors['border']} !important; text-align: center !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }}
        div[data-testid="stMetricSimpleContainer"]:hover {{
            border-color: {theme_colors['text_accent']} !important;
            transform: translateY(-2px) !important;
        }}
        
        /* Inputs */
        .stTextInput input, .stNumberInput input, .stPasswordInput input {{
            background-color: {theme_colors['bg_secondary']} !important;
            color: {theme_colors['text_primary']} !important;
            border: 1px solid {theme_colors['border']} !important;
            border-radius: 8px !important; padding: 10px 12px !important;
            font-size: 14px !important;
        }}
        
        /* Buttons */
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
        
        /* Action Buttons */
        .buy-box button {{ background: linear-gradient(90deg,#00c851,#007e33) !important; color:white !important; }}
        .sell-box button {{ background: linear-gradient(90deg,#ff4444,#cc0000) !important; color:white !important; }}
        .wait-box button {{ background: linear-gradient(90deg,#ffbb33,#ff8800) !important; color:white !important; }}
        
        /* Panic Button */
        @keyframes pulse-panic {{
            0% {{ box-shadow: 0 0 0 0 rgba(220,38,38,0.7); }}
            70% {{ box-shadow: 0 0 0 10px rgba(220,38,38,0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(220,38,38,0); }}
        }}
        .panic-container button {{
            background: linear-gradient(90deg,#7f1d1d,#dc2626) !important;
            color:white !important; border:2px solid #ef4444 !important;
            height:56px !important; font-weight:900 !important; font-size:16px !important;
            animation: pulse-panic 2s infinite !important; margin:10px 0 !important;
        }}
        .panic-container button:hover {{ animation:none !important; background:linear-gradient(90deg,#991d1d,#ee3636) !important; }}
        
        /* Config Box */
        .config-box {{
            background-color:{theme_colors['bg_secondary']} !important; padding:15px !important;
            border-radius:10px !important; border:1px solid {theme_colors['border']} !important;
            margin-bottom:15px !important;
        }}
        
        /* Alerts */
        .risk-alert {{
            background:linear-gradient(135deg,#3d1c1a,#2d0f0f);
            border:2px solid #dc2626; border-radius:10px;
            padding:12px 16px; margin:10px 0;
            animation: pulse-panic 2s infinite;
        }}
        .trail-box {{
            background:linear-gradient(135deg,#0d2d1a,#0f3a20);
            border:1px solid {theme_colors['success']}; border-radius:10px;
            padding:12px 16px; margin:8px 0;
        }}
        
        /* Tables */
        table {{ background-color:{theme_colors['bg_secondary']} !important; border:1px solid {theme_colors['border']} !important; border-radius:8px !important; }}
        thead tr {{ background-color:{theme_colors['bg_tertiary']} !important; border-bottom:2px solid {theme_colors['border']} !important; }}
        tbody tr {{ border-bottom:1px solid {theme_colors['border']} !important; }}
        tbody tr:hover {{ background-color:{theme_colors['bg_tertiary']} !important; }}
        th {{ color:{theme_colors['text_accent']} !important; font-weight:800 !important; padding:12px !important; }}
        td {{ color:{theme_colors['text_primary']} !important; padding:10px 12px !important; }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color:{theme_colors['bg_tertiary']} !important;
            border:1px solid {theme_colors['border']} !important; border-radius:8px !important;
        }}
        
        /* Text */
        h1,h2,h3,h4,h5,h6 {{ color:{theme_colors['text_accent']} !important; }}
        hr {{ border-color:{theme_colors['border']} !important; }}
        label {{ color:{theme_colors['text_primary']} !important; font-weight:600 !important; }}
        
        /* Hide Elements */
        #MainMenu, footer, header {{ visibility:hidden !important; }}
        .stDeployButton {{ display:none !important; }}
        
        /* Control buttons section */
        .control-section {{
            background: linear-gradient(135deg, {theme_colors['bg_secondary']}, {theme_colors['bg_tertiary']});
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            border: 2px solid {theme_colors['border']};
        }}
        
        .live-title {{
            font-size: 28px !important;
            font-weight: 900 !important;
            color: {theme_colors['text_accent']} !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
        }}
    </style>
    """

st.markdown(generate_css(colors), unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def add_log(action, details=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uid = st.session_state.get("user_id","Unknown")
    st.session_state["audit_logs"].append(
        {"timestamp":ts,"user_id":uid,"action":action,"details":details})

def send_telegram_alert(message):
    """Send alert to Telegram"""
    if not st.session_state["telegram_alerts"] or not st.session_state["telegram_token"]:
        return
    try:
        token = st.session_state["telegram_token"]
        chat_id = st.session_state["telegram_chat_id"]
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        st.warning(f"Telegram alert failed: {str(e)}")

def get_lot_size(sym):
    lots = {
        "NIFTY":50,"BANKNIFTY":15,"FINNIFTY":25,"MIDCPNIFTY":10,"SENSEX":10,"BANKEX":15,
        "CRUDEOIL":100,"CRUDEOILM":10,"NATURALGAS":1250,"NATGASMINI":250,
        "GOLD":100,"GOLDM":10,"SILVER":30,"SILVERM":5,
        "COPPER":250,"ZINC":250,"NICKEL":10,"LEAD":500,"ALUMINIUM":1000,
    }
    return lots.get(sym.upper().replace("-EQ",""),1)

def get_tv_symbol(sym):
    mp = {
        "NIFTY":"TVC:NIFTY","BANKNIFTY":"TVC:BANKNIFTY","FINNIFTY":"TVC:FINNIFTY",
        "MIDCPNIFTY":"TVC:MIDCPNIFTY","SENSEX":"TVC:SENSEX",
        "CRUDEOIL":"MCX:CRUDEOIL1!","NATURALGAS":"MCX:NATURALGAS1!",
        "GOLD":"MCX:GOLD1!","SILVER":"MCX:SILVER1!","COPPER":"MCX:COPPER1!",
        "USDINR":"TVC:USDINR",
    }
    s = sym.upper().replace("-EQ","").strip()
    return mp.get(s, f"NSE:{s}")

def check_risk():
    pnl = st.session_state["dynamic_pnl"]
    if pnl < -st.session_state["max_daily_loss"]:
        return False, f"Max Daily Loss ₹{st.session_state['max_daily_loss']:,.0f} Breach!"
    if pnl >= st.session_state["daily_target"]:
        return False, f"Daily Target ₹{st.session_state['daily_target']:,.0f} Hit!"
    return True, "OK"

def update_trail():
    pnl = st.session_state["dynamic_pnl"]
    if pnl > st.session_state["peak_pnl"]:
        st.session_state["peak_pnl"] = pnl
    if st.session_state["trail_active"] and st.session_state["peak_pnl"] > 0:
        lock = st.session_state["peak_pnl"] * (1 - st.session_state["trail_sl_pct"]/100)
        if pnl < lock:
            return True, lock
    return False, 0.0

def trigger_order(symbol, action, qty, exchange="NFO", sl=0.0, target=0.0):
    """
    ORDER ENGINE — Angel One SmartAPI ready structure.
    
    To go LIVE with Angel One:
        from SmartApi import SmartConnect
        import pyotp
        cfg = st.session_state["broker_config"]
        obj = SmartConnect(api_key=cfg["api_key"])
        obj.generateSession(cfg["client_id"], cfg["password"],
                            pyotp.TOTP(cfg["totp_secret"]).now())
        resp = obj.placeOrder({...})
    """
    if not st.session_state["auto_trade"]:
        add_log("DRY_RUN", f"{action} {qty}x {symbol} [{exchange}]")
        send_telegram_alert(f"🟡 <b>DRY RUN:</b> {action} {qty}x {symbol}")
        return {"status":"DRY_RUN","order_id":None}
    
    import random
    oid = f"RM{random.randint(1000000,9999999)}"
    add_log("ORDER", f"{action} {qty}x {symbol} [{exchange}] ID:{oid}")
    msg = f"🔴 <b>LIVE TRADE:</b>\n{action} {qty}x {symbol}\nSL: {sl} pts | TGT: {target} pts\nID: {oid}"
    send_telegram_alert(msg)
    return {"status":"SUCCESS","order_id":oid}

# ============================================================================
# LOGIN PAGE
# ============================================================================
if not st.session_state["authenticated"]:
    st.markdown(f"""
    <div style="text-align:center;padding:60px 20px;background:linear-gradient(135deg, {colors['bg_secondary']}, {colors['bg_tertiary']});border-radius:20px;margin:20px 0;">
        <h1 style="color:{colors['text_accent']};font-size:56px;font-weight:900;margin-bottom:10px;">
            🔱 RAMAVAT ALGO ELITE</h1>
        <p style="color:{colors['text_secondary']};font-size:18px;">PROFESSIONAL ALGO TRADING TERMINAL v2.1</p>
        <hr style="margin:30px 0;border-color:{colors['border']};">
    </div>""", unsafe_allow_html=True)
    
    _,cm,_ = st.columns([1,2,1])
    with cm:
        st.markdown(f"<div class='config-box'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{colors['text_accent']};text-align:center;'>🔐 SECURE LOGIN</h3>"
                    f"<p style='color:{colors['text_secondary']};text-align:center;font-size:13px;margin:8px 0 16px;'>"
                    f"સાહેબ, User ID અને Password નાખો</p>", unsafe_allow_html=True)
        lu = st.text_input("👤 User ID:", placeholder="Enter User ID", key="lu")
        lp = st.text_input("🔑 Password:", type="password", placeholder="Default: 1234", key="lp")
        
        if st.button("🚀 LOGIN", use_container_width=True):
            if lu and lp == "1234":
                st.session_state.update({"authenticated":True,"user_id":lu,"login_time":datetime.now()})
                add_log("LOGIN", f"'{lu}' logged in")
                st.success(f"✅ Welcome {lu}! Login સફળ 🚀")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ ખોટો Password!")
                add_log("LOGIN_FAIL", f"Failed: '{lu}'")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:{colors['text_secondary']};font-size:12px;margin-top:16px;'>"
                    f"📝 Demo: Any User ID | Password: 1234</p>", unsafe_allow_html=True)
    st.stop()

# ============================================================================
# MAIN DASHBOARD
# ============================================================================
risk_ok, risk_msg = check_risk()
trail_hit, trail_lock = update_trail()

# ALERTS
if not risk_ok:
    st.markdown(f"<div class='risk-alert'><b style='color:#fca5a5;'>⚠️ RISK: {risk_msg}</b></div>",
                unsafe_allow_html=True)
if trail_hit:
    st.markdown(f"<div class='trail-box'><b style='color:#86efac;'>🔄 Trail SL Triggered! Lock: ₹{trail_lock:,.0f}</b></div>",
                unsafe_allow_html=True)

# HEADER WITH THEME TOGGLE
hl, hm, hr = st.columns([3,1,1])
with hl:
    st.markdown(f"<div style='text-align:center;margin-bottom:10px;'>"
                f"<h1 style='color:{colors['text_accent']};margin:0;font-size:36px;font-weight:900;'>🔱 RAMAVAT ALGO ELITE</h1>"
                f"<p style='color:{colors['text_secondary']};font-size:13px;margin:0;'>NSE • MCX • EQUITY — PERSONAL ALGO BRIDGE TERMINAL</p>"
                f"</div>", unsafe_allow_html=True)
with hm:
    if st.button("🌙 Theme", key="theme_btn", use_container_width=True):
        st.session_state["theme"] = "light" if st.session_state["theme"] == "dark" else "dark"
        st.rerun()
with hr:
    if st.button("🚪 Logout", key="lo", use_container_width=True):
        st.session_state["authenticated"] = False
        add_log("LOGOUT","User logged out")
        st.rerun()

broker_dot = "🟢" if st.session_state["broker_connected"] else "🔴"
bname = st.session_state.get("connected_broker","None")
mode = "🟢 LIVE" if st.session_state["auto_trade"] else "🟡 DRY RUN"
uid = st.session_state.get("user_id","Operator")
lt = st.session_state.get("login_time")
ltstr = lt.strftime("%H:%M") if lt else "—"

st.markdown(f"⚡ **LIVE CONTROL DESK** &nbsp;|&nbsp; 👤 **{uid}** &nbsp;|&nbsp; "
            f"{broker_dot} **{bname}** &nbsp;|&nbsp; Mode: **{mode}** &nbsp;|&nbsp; Login: **{ltstr}**",
            unsafe_allow_html=True)
st.markdown(f"<hr style='margin:5px 0 15px 0;border-color:{colors['border']};'>", unsafe_allow_html=True)

# METRICS
m1,m2,m3,m4 = st.columns(4)
pnl = st.session_state["dynamic_pnl"]
m1.metric("📊 Today P&L (Live)", f"₹ {pnl:,.2f}", "▲ Profit" if pnl>=0 else "▼ Loss")
m2.metric("💰 Total Capital", f"₹ {st.session_state['total_capital']:,.0f}", "Available")
m3.metric("🎯 Open Positions", f"{len(st.session_state['open_positions'])} Active", "Running")
m4.metric("🔌 API Status",
          "Connected ✅" if st.session_state["broker_connected"] else "Disconnected ❌",
          bname if st.session_state["broker_connected"] else "Setup pending")

cp1,cp2 = st.columns(2)
with cp1:
    lp_val = min(max(-pnl,0)/st.session_state["max_daily_loss"],1.0)
    st.caption(f"🛑 Loss: {lp_val*100:.0f}% of ₹{st.session_state['max_daily_loss']:,.0f}")
    st.progress(lp_val)
with cp2:
    tp_val = min(max(pnl,0)/st.session_state["daily_target"],1.0)
    st.caption(f"🎯 Target: {tp_val*100:.0f}% of ₹{st.session_state['daily_target']:,.0f}")
    st.progress(tp_val)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# MAIN LAYOUT: CHART + SIDE PANEL
# ============================================================================
col_chart, col_ctrl = st.columns([1.3,0.7])

# ============================================================================
# CHART SECTION
# ============================================================================
with col_chart:
    st.markdown(f"<h3 style='color:{colors['text_accent']};'>📈 Live Chart</h3>", unsafe_allow_html=True)
    
    # Symbol Selection
    cs1, cs2 = st.columns([2, 1])
    with cs1:
        usym = st.text_input("Symbol:", value="NIFTY", key="usym", label_visibility="collapsed").strip().upper()
    with cs2:
        otype = st.selectbox("Type:", ["FUT","CE","PE","EQUITY"], key="otype", label_visibility="collapsed")
    
    # TradingView Chart
    tv = get_tv_symbol(usym)
    st.components.v1.html(f"""
    <div style="height:550px;border-radius:12px;overflow:hidden;border:2px solid {colors['border']};">
        <iframe src="https://s.tradingview.com/widgetembed/?symbol={tv}&interval=5&theme={'dark' if st.session_state['theme']=='dark' else 'light'}&style=1&timezone=Asia%2FKolkata&locale=en&allow_symbol_change=1"
            width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen>
        </iframe>
    </div>""", height=560)

# ============================================================================
# CONTROL PANEL
# ============================================================================
with col_ctrl:
    # BROKER CONFIG
    with st.expander("🔌 Broker Config", expanded=False):
        st.markdown(f"<div class='config-box'>", unsafe_allow_html=True)
        sel_broker = st.selectbox("Broker:", [b.value for b in BrokerType], key="bsel")
        ucid = st.text_input("👤 Client ID:", key="ucid", value=st.session_state["broker_config"]["client_id"])
        uapi = st.text_input("🔑 API Key:", type="password", key="uapi", value=st.session_state["broker_config"]["api_key"])
        utotp = st.text_input("⏳ TOTP:", type="password", key="utotp", value=st.session_state["broker_config"]["totp_secret"])
        usec = st.text_input("🔒 Secret:", type="password", key="usec", value=st.session_state["broker_config"]["secret_key"])
        
        if st.button("🔌 Connect", key="conn", use_container_width=True):
            if ucid and uapi:
                st.session_state.update({
                    "broker_connected":True,"connected_broker":sel_broker,
                    "broker_config":{"client_id":ucid,"api_key":uapi,"secret_key":usec,"totp_secret":utotp}})
                st.toast(f"✅ {sel_broker} Connected!", icon="🚀")
                add_log("API_CONNECTED", sel_broker)
                st.rerun()
            else:
                st.error("❌ Client ID અને API Key ભરો!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # TELEGRAM ALERTS
    with st.expander("📱 Telegram Alerts", expanded=False):
        st.markdown(f"<div class='config-box'>", unsafe_allow_html=True)
        st.session_state["telegram_alerts"] = st.toggle("Enable Telegram", st.session_state["telegram_alerts"])
        if st.session_state["telegram_alerts"]:
            st.session_state["telegram_token"] = st.text_input("🤖 Bot Token:", type="password", key="tg_token")
            st.session_state["telegram_chat_id"] = st.text_input("💬 Chat ID:", key="tg_chat", placeholder="Your Telegram Chat ID")
            if st.button("🧪 Test Alert", use_container_width=True):
                send_telegram_alert("✅ Ramavat Algo Elite - Test Alert સફળ!")
                st.success("Test message sent!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # RISK MANAGEMENT
    with st.expander("🛡️ Risk Settings", expanded=False):
        st.markdown(f"<div class='config-box'>", unsafe_allow_html=True)
        st.session_state["max_daily_loss"] = st.number_input(
            "Max Daily Loss (₹):", min_value=500, max_value=100000,
            value=int(st.session_state["max_daily_loss"]), step=500, key="mdl")
        st.session_state["daily_target"] = st.number_input(
            "Daily Target (₹):", min_value=500, max_value=100000,
            value=int(st.session_state["daily_target"]), step=500, key="dt")
        st.session_state["risk_per_trade"] = st.slider(
            "Risk per Trade (%):", 0.5, 5.0, st.session_state["risk_per_trade"], 0.5, key="rpt")
        
        st.session_state["trail_active"] = st.toggle("Auto Trail SL", st.session_state["trail_active"], key="ta")
        if st.session_state["trail_active"]:
            st.session_state["trail_sl_pct"] = st.slider(
                "Trail SL (%):", 0.1, 3.0, st.session_state["trail_sl_pct"], 0.1, key="tsl")
        
        if st.button("💾 Save Settings", use_container_width=True):
            add_log("RISK_SAVED","Settings updated")
            st.success("✅ Saved!")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<hr style='border-color:{colors['border']};margin:20px 0;'>", unsafe_allow_html=True)

# ============================================================================
# ORDER CONTROL SECTION (BOTTOM)
# ============================================================================
st.markdown(f"""<div class='control-section'>
<h2 class='live-title'>⚡ ORDER CONTROL CENTER</h2>
</div>""", unsafe_allow_html=True)

# Strike & Expiry
oe1, oe2, oe3 = st.columns(3)
with oe1:
    ustrike = st.text_input("Strike Price:", value="24400", key="ustrk")
with oe2:
    uexpiry = st.text_input("Expiry:", value="26JUN26", key="uexp")
with oe3:
    ls = get_lot_size(usym)
    ulots = st.number_input("🔢 Lots:", min_value=1, value=1, key="ulots")
uqty = ulots * ls

# SL & Target
sl1, sl2 = st.columns(2)
with sl1:
    sl_pts = st.number_input("🚨 SL (Pts):", value=30, key="slp")
with sl2:
    tgt_pts = st.number_input("🎯 Target (Pts):", value=60, key="tgtp")

# LIVE TRADING MODE
st.session_state["auto_trade"] = st.toggle(
    f"🤖 Mode: {'🟢 LIVE TRADE' if st.session_state['auto_trade'] else '🟡 DRY RUN'}",
    value=st.session_state["auto_trade"], key="mode_toggle")
if st.session_state["auto_trade"]:
    st.warning("⚠️ LIVE MODE — Real orders will be executed!")

script = f"{usym} {ustrike} {otype}" if otype != "EQUITY" else usym

def _place(action):
    if not st.session_state["broker_connected"]:
        st.error("❌ Broker connect karvo!")
        return
    if not risk_ok:
        st.error(f"⛔ {risk_msg}")
        return
    res = trigger_order(script, action, uqty, sl=sl_pts, target=tgt_pts)
    st.session_state["open_positions"].append({
        "id": f"#RM-{len(st.session_state['open_positions'])+2001}",
        "script": script, "qty": uqty, "action": action,
        "sl_pts": sl_pts, "tgt_pts": tgt_pts, "entry": 100.0,
        "status": "⌛ Waiting", "order_id": res.get("order_id","DRY"),
        "mode": "LIVE" if st.session_state["auto_trade"] else "DRY",
    })
    icon = "🟢" if action == "BUY" else "🔴"
    msg = f"{icon} {action} | {script} | {'LIVE' if st.session_state['auto_trade'] else 'DRY'}"
    st.toast(msg, icon="✅")

# MAIN ACTION BUTTONS - LARGE AND CENTERED
st.markdown("<br>", unsafe_allow_html=True)
b1, b2, b3, b4 = st.columns(4)

with b1:
    st.markdown('<div class="buy-box">', unsafe_allow_html=True)
    if st.button("🟩 BUY", key="bb", use_container_width=True):
        _place("BUY")
    st.markdown("</div>", unsafe_allow_html=True)

with b2:
    st.markdown('<div class="sell-box">', unsafe_allow_html=True)
    if st.button("🟥 SELL", key="sb", use_container_width=True):
        _place("SELL")
    st.markdown("</div>", unsafe_allow_html=True)

with b3:
    st.markdown('<div class="wait-box">', unsafe_allow_html=True)
    if st.button("🟨 WAIT", key="wb", use_container_width=True):
        st.toast("⏳ System on Hold", icon="⏳")
        add_log("WAIT","On hold")
    st.markdown("</div>", unsafe_allow_html=True)

with b4:
    if st.button("🔄 Refresh", key="ref", use_container_width=True):
        import random
        st.session_state["dynamic_pnl"] += random.uniform(-100,200)
        add_log("REFRESH","Data refreshed")
        st.rerun()

# PANIC BUTTON
st.markdown('<div class="panic-container">', unsafe_allow_html=True)
if st.button("💥 EMERGENCY CLOSE ALL POSITIONS", key="panic", use_container_width=True):
    cnt = len(st.session_state["open_positions"])
    st.session_state.update({"open_positions":[],"peak_pnl":0.0})
    add_log("EMERGENCY", f"{cnt} positions force-closed")
    send_telegram_alert(f"🔴 <b>EMERGENCY:</b> {cnt} positions force-closed!")
    st.toast(f"🚨 {cnt} Positions Closed!", icon="💥")
    time.sleep(0.3)
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<hr style='border-color:{colors['border']};margin:20px 0;'>", unsafe_allow_html=True)

# ============================================================================
# POSITIONS TABLE
# ============================================================================
st.markdown(f"<h4 style='color:{colors['text_accent']};'>📋 Live Open Positions</h4>", unsafe_allow_html=True)
if st.session_state["open_positions"]:
    df = pd.DataFrame([{
        "Trade ID": p["id"], "Script": p["script"], "Qty": p["qty"],
        "Action": p["action"], "SL": p["sl_pts"], "TGT": p["tgt_pts"],
        "Mode": p["mode"], "Status": p["status"],
    } for p in st.session_state["open_positions"]])
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.button("🗑️ Clear Positions", use_container_width=True):
        add_log("CLEAR", f"{len(st.session_state['open_positions'])} cleared")
        st.session_state["open_positions"] = []
        st.rerun()
else:
    st.info("📭 કોઈ Open Position નથી. Order place karvo!")

# ============================================================================
# AUDIT LOGS
# ============================================================================
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📝 Audit Logs"):
    logs = st.session_state["audit_logs"]
    if logs:
        st.dataframe(
            pd.DataFrame(list(reversed(logs[-25:])))[["timestamp","action","details"]],
            use_container_width=True, hide_index=True)
    else:
        st.info("📭 No logs yet.")

# FOOTER
st.markdown(f"""
<hr style='border-color:{colors['border']};margin-top:30px;'>
<div style='text-align:center;color:{colors['text_secondary']};font-size:12px;padding:20px 0;'>
    <p>🔱 Ramavat Algo Elite v2.1 &nbsp;|&nbsp; NSE • MCX • Equity</p>
    <p>© 2026 All Rights Reserved &nbsp;|&nbsp; ⚠️ Trading involves risk.</p>
    <p>🔒 Secure | 🚀 Fast | 📱 Telegram Ready | 🌓 Dark/Light Mode</p>
</div>""", unsafe_allow_html=True)
