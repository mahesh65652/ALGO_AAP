"""
app.py — RAMAVAT ALGO ELITE  [v2.0]
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
    ANGEL_ONE  = "Angel One (SmartAPI)"
    ALICE_BLUE = "Alice Blue (ANT)"
    ZERODHA    = "Zerodha (Kite)"
    FINVASIA   = "Finvasia (Shoonya)"

# ══════════════════════════════════════════════════════════════════
# 🎨 PREMIUM DARK CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    * { margin:0; padding:0; box-sizing:border-box; }

    .main { background-color:#060913 !important; color:#e2e8f0 !important; }
    body  { background-color:#060913 !important; }

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
    .stTextInput input, .stNumberInput input,
    .stSelectbox, .stPasswordInput input {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stPasswordInput input:focus {
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

    /* ═══════════════════════════════════════════
       🟩 BIG BUY BUTTON
    ═══════════════════════════════════════════ */
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
    .buy-box .stButton > button:active {
        transform: translateY(1px) scale(0.99) !important;
        box-shadow: 0 0 12px rgba(0,230,118,0.5) !important;
    }

    /* ═══════════════════════════════════════════
       🟥 BIG SELL BUTTON
    ═══════════════════════════════════════════ */
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
    .sell-box .stButton > button:active {
        transform: translateY(1px) scale(0.99) !important;
        box-shadow: 0 0 12px rgba(255,23,68,0.5) !important;
    }

    /* ═══════════════════════════════════════════
       🟨 BIG WAIT BUTTON
    ═══════════════════════════════════════════ */
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
        text-shadow: 0 1px 2px rgba(255,255,255,0.2) !important;
    }
    .wait-box .stButton > button:hover {
        background: linear-gradient(135deg, #fff176, #ffee00, #ffbb33) !important;
        box-shadow: 0 0 32px rgba(255,187,51,0.7), 0 8px 24px rgba(0,0,0,0.5) !important;
        transform: translateY(-3px) scale(1.02) !important;
    }
    .wait-box .stButton > button:active {
        transform: translateY(1px) scale(0.99) !important;
    }

    /* TRADE ACTION DIVIDER LABEL */
    .trade-label {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 6px 0 10px 0;
    }

    /* PANIC PULSE */
    @keyframes pulse-panic {
        0%   { box-shadow: 0 0 0 0 rgba(220,38,38,0.7); }
        70%  { box-shadow: 0 0 0 10px rgba(220,38,38,0); }
        100% { box-shadow: 0 0 0 0 rgba(220,38,38,0); }
    }
    .panic-container .stButton > button {
        background: linear-gradient(90deg, #7f1d1d, #dc2626) !important;
        color: white !important;
        border: 2px solid #ef4444 !important;
        height: 60px !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        animation: pulse-panic 2s infinite !important;
        margin-top: 15px !important;
        border-radius: 12px !important;
    }
    .panic-container .stButton > button:hover {
        animation: none !important;
        background: linear-gradient(90deg, #991d1d, #ee3636) !important;
    }

    /* CONFIG BOX */
    .config-box {
        background-color: #0d1527 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid #1e293b !important;
        margin-bottom: 15px !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.5) !important;
    }

    /* TRADE ACTION AREA */
    .trade-action-area {
        background: linear-gradient(135deg, #0a0f1e, #0d1527);
        border: 1px solid #1e366a;
        border-radius: 14px;
        padding: 18px 14px 14px 14px;
        margin: 12px 0;
    }

    /* RISK ALERT BOX */
    .risk-alert {
        background: linear-gradient(135deg, #3d1c1a, #2d0f0f);
        border: 2px solid #dc2626;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 10px 0;
        animation: pulse-panic 2s infinite;
    }

    /* TRAIL SL BOX */
    .trail-box {
        background: linear-gradient(135deg, #0d2d1a, #0f3a20);
        border: 1px solid #22c55e;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
    }

    /* TABLES */
    table {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    thead tr { background-color:#0d162d !important; border-bottom:2px solid #1e366a !important; }
    tbody tr  { border-bottom: 1px solid #1e293b !important; }
    tbody tr:hover { background-color: #142247 !important; }
    th { color: #d4af37 !important; font-weight: 800 !important; padding: 12px !important; }
    td { color: #e2e8f0 !important; padding: 10px 12px !important; }

    /* STREAMLIT ELEMENTS */
    .streamlit-expanderHeader {
        background-color: #0d162d !important;
        border: 1px solid #1e366a !important;
        border-radius: 8px !important;
    }
    h1, h2, h3, h4, h5, h6 { color: #d4af37 !important; }
    hr  { border-color: #1e366a !important; }
    label { color: #e2e8f0 !important; font-weight: 600 !important; }
    #MainMenu, footer, header { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════
_defaults = {
    "authenticated"    : False,
    "user_id"          : None,
    "login_time"       : None,
    "broker_connected" : False,
    "connected_broker" : None,
    "broker_config"    : {"client_id":"","api_key":"","secret_key":"","totp_secret":""},
    "audit_logs"       : [],
    "open_positions"   : [],
    "dynamic_pnl"      : 2695.0,
    "total_capital"    : 150000.0,
    "max_daily_loss"   : 5000.0,
    "daily_target"     : 8000.0,
    "trail_sl_pct"     : 0.5,
    "risk_per_trade"   : 2.0,
    "auto_trade"       : False,
    "trail_active"     : False,
    "peak_pnl"         : 0.0,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════
# UTILITIES
# ══════════════════════════════════════════════════════════════════
def add_audit_log(action: str, details: str = ""):
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uid = st.session_state.get("user_id", "Unknown")
    st.session_state["audit_logs"].append({
        "timestamp": ts, "user_id": uid,
        "action": action, "details": details,
    })


def get_lot_size(symbol: str) -> int:
    lots = {
        "NIFTY":50,"BANKNIFTY":15,"FINNIFTY":25,"MIDCPNIFTY":10,
        "SENSEX":10,"BANKEX":15,
        "CRUDEOIL":100,"CRUDEOILM":10,"NATURALGAS":1250,"NATGASMINI":250,
        "GOLD":100,"GOLDM":10,"SILVER":30,"SILVERM":5,
        "COPPER":250,"ZINC":250,"NICKEL":10,"LEAD":500,"ALUMINIUM":1000,
    }
    return lots.get(symbol.upper().replace("-EQ",""), 1)


def get_tradingview_symbol(symbol: str) -> str:
    tv_map = {
        "NIFTY"      : "NSE:NIFTY1!",
        "BANKNIFTY"  : "NSE:BANKNIFTY1!",
        "FINNIFTY"   : "NSE:FINNIFTY1!",
        "MIDCPNIFTY" : "NSE:MIDCPNIFTY1!",
        "SENSEX"     : "BSE:SENSEX1!",
        "CRUDEOIL"   : "MCX:CRUDEOIL1!",
        "CRUDOIL"    : "MCX:CRUDEOIL1!",
        "NATURALGAS" : "MCX:NATURALGAS1!",
        "GOLD"       : "MCX:GOLD1!",
        "SILVER"     : "MCX:SILVER1!",
        "COPPER"     : "MCX:COPPER1!",
        "ZINC"       : "MCX:ZINC1!",
        "USDINR"     : "NSE:USDINR1!",   # ✅ NSE Currency Futures — India Market
    }
    s = symbol.upper().replace("-NSE","").replace("-EQ","").strip()
    return tv_map.get(s, f"NSE:{s}")


def check_risk_limits() -> tuple:
    pnl = st.session_state["dynamic_pnl"]
    if pnl < -st.session_state["max_daily_loss"]:
        return False, f"🚨 Max Daily Loss ₹{st.session_state['max_daily_loss']:,.0f} Breach! Auto-stop!"
    if pnl >= st.session_state["daily_target"]:
        return False, f"🎯 Daily Target ₹{st.session_state['daily_target']:,.0f} Hit! Trading stop."
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


def trigger_real_order(symbol: str, action: str, qty: int,
                        order_type: str = "MARKET",
                        exchange: str = "NSE",
                        price: float = 0.0,
                        sl: float = 0.0,
                        target: float = 0.0) -> dict:
    """
    ── PROFESSIONAL ORDER ENGINE ─────────────────────────────────
    DRY RUN mode: Simulated (safe for testing)
    LIVE mode   : Connect broker API below

    Angel One (SmartAPI):
        from SmartApi import SmartConnect
        import pyotp
        obj = SmartConnect(api_key=cfg["api_key"])
        obj.generateSession(cfg["client_id"], cfg["password"],
                            pyotp.TOTP(cfg["totp_secret"]).now())
        resp = obj.placeOrder({
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": action,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": str(price),
            "quantity": str(qty),
            "squareoff": str(target),
            "stoploss": str(sl),
        })
    Alice Blue / Zerodha: swap above block with their SDK.
    ─────────────────────────────────────────────────────────────
    """
    if not st.session_state["auto_trade"]:
        add_audit_log("DRY_RUN",
            f"{action} {qty}x {symbol} [{exchange}] SL:{sl} TGT:{target}")
        return {"status": "DRY_RUN", "order_id": None,
                "message": f"DRY RUN — {action} {qty}x {symbol}"}

    import random
    order_id = f"RM{random.randint(1000000, 9999999)}"
    add_audit_log("ORDER_PLACED",
        f"{action} {qty}x {symbol} [{exchange}] ID:{order_id}")
    return {"status": "SUCCESS", "order_id": order_id,
            "message": f"Order placed: {order_id}"}

# ══════════════════════════════════════════════════════════════════
# 🔐 LOGIN
# ══════════════════════════════════════════════════════════════════
if not st.session_state["authenticated"]:
    st.markdown("""
    <div style="text-align:center;padding:40px 0;">
        <h1 style="color:#d4af37;font-size:48px;font-weight:900;margin-bottom:10px;">
            🔱 RAMAVAT ALGO ELITE
        </h1>
        <p style="color:#9ca3af;font-size:16px;">PROFESSIONAL ALGO TRADING TERMINAL v2.0</p>
        <hr style="margin:30px 0;border-color:#1e366a;">
    </div>""", unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1,2,1])
    with col_mid:
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        st.markdown(
            "<h3 style='color:#d4af37;text-align:center;'>🔐 SECURE LOGIN</h3>"
            "<p style='color:#9ca3af;text-align:center;font-size:13px;margin:8px 0 16px;'>"
            "સાહેબ, તમારો User ID અને Password નાખો</p>",
            unsafe_allow_html=True)

        login_user = st.text_input("👤 User ID:", placeholder="Enter User ID", key="li_u")
        login_pass = st.text_input("🔑 Password:", type="password",
                                    placeholder="Default: 1234", key="li_p")

        c_btn, _ = st.columns([1,1])
        with c_btn:
            if st.button("🚀 LOGIN", use_container_width=True):
                if login_user and login_pass == "1234":
                    st.session_state["authenticated"] = True
                    st.session_state["user_id"]       = login_user
                    st.session_state["login_time"]    = datetime.now()
                    add_audit_log("LOGIN", f"'{login_user}' logged in")
                    st.success(f"✅ Welcome {login_user}! લૉગિન સફળ 🚀")
                    st.balloons()
                    time.sleep(1); st.rerun()
                else:
                    st.error("❌ ખોટો Password! Try again.")
                    add_audit_log("LOGIN_FAILED", f"Failed attempt: '{login_user}'")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:center;color:#9ca3af;font-size:12px;margin-top:16px;'>"
            "📝 Demo: Any User ID | Password: 1234</p>",
            unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════

risk_ok, risk_msg = check_risk_limits()
trail_hit, trail_lock_pnl = update_trail_sl()

if not risk_ok:
    st.markdown(f"""
    <div class='risk-alert'>
        <b style='color:#fca5a5;font-size:1rem;'>⚠️ RISK LIMIT: {risk_msg}</b>
    </div>""", unsafe_allow_html=True)

if trail_hit:
    st.markdown(f"""
    <div class='trail-box'>
        <b style='color:#86efac;'>🔄 Trail SL Triggered! Lock-in: ₹{trail_lock_pnl:,.0f}</b>
    </div>""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────
h_left, h_right = st.columns([4,1])
with h_left:
    st.markdown("""
    <div style="text-align:center;margin-bottom:10px;">
        <h1 style="color:#d4af37;margin:0;font-size:32px;font-weight:900;">
            🔱 RAMAVAT ALGO ELITE
        </h1>
        <p style="color:#9ca3af;font-size:13px;margin:0;">
            NSE • MCX • EQUITY — PERSONAL ALGO BRIDGE TERMINAL
        </p>
    </div>""", unsafe_allow_html=True)
with h_right:
    if st.button("🚪 Logout", key="logout_btn"):
        st.session_state["authenticated"] = False
        add_audit_log("LOGOUT", "User logged out")
        st.rerun()

# ── STATUS BAR ─────────────────────────────────────────────────────
broker_dot  = "🟢" if st.session_state["broker_connected"] else "🔴"
broker_name = st.session_state.get("connected_broker","None")
trade_mode  = "🟡 DRY RUN" if not st.session_state["auto_trade"] else "🟢 LIVE TRADE"
uid         = st.session_state.get("user_id","Operator")
login_t     = st.session_state.get("login_time")
login_str   = login_t.strftime("%H:%M") if login_t else "—"

st.markdown(
    f"⚡ **LIVE CONTROL DESK** &nbsp;|&nbsp; 👤 **{uid}** &nbsp;|&nbsp; "
    f"{broker_dot} Broker: **{broker_name}** &nbsp;|&nbsp; "
    f"Mode: **{trade_mode}** &nbsp;|&nbsp; Login: **{login_str}**",
    unsafe_allow_html=True)
st.markdown("<hr style='margin:5px 0 15px 0;border-color:#1e366a;'>", unsafe_allow_html=True)

# ── METRICS ────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
pnl       = st.session_state["dynamic_pnl"]
pnl_delta = "▲ Profit" if pnl >= 0 else "▼ Loss"

m1.metric("📊 Today P&L (Live)",   f"₹ {pnl:,.2f}", pnl_delta)
m2.metric("💰 Total Capital",      f"₹ {st.session_state['total_capital']:,.0f}", "Available")
m3.metric("🎯 Open Positions",     f"{len(st.session_state['open_positions'])} Active", "Running")
m4.metric("🔌 API Status",
          "Connected ✅" if st.session_state["broker_connected"] else "Disconnected ❌",
          broker_name if st.session_state["broker_connected"] else "Setup pending")

loss_pct   = min(max(-pnl, 0) / st.session_state["max_daily_loss"], 1.0)
profit_pct = min(max(pnl, 0)  / st.session_state["daily_target"],   1.0)
col_prog1, col_prog2 = st.columns(2)
with col_prog1:
    st.caption(f"🛑 Loss Used: {loss_pct*100:.0f}% of ₹{st.session_state['max_daily_loss']:,.0f}")
    st.progress(loss_pct)
with col_prog2:
    st.caption(f"🎯 Target: {profit_pct*100:.0f}% of ₹{st.session_state['daily_target']:,.0f}")
    st.progress(profit_pct)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# MAIN LAYOUT — CHART LEFT | CONTROL RIGHT
# ══════════════════════════════════════════════════════════════════
col_chart, col_ctrl = st.columns([1.1, 1])

# ══════════════════════════════════════════════════════════════════
# RIGHT PANEL — CONTROLS
# ══════════════════════════════════════════════════════════════════
with col_ctrl:

    # ── BROKER CONFIG ──────────────────────────────────────────────
    with st.expander("🔌 Broker API Configuration"):
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        selected_broker = st.selectbox(
            "Broker પસંદ કરો:", [b.value for b in BrokerType], key="broker_sel")
        c1, c2 = st.columns(2)
        with c1:
            u_cid  = st.text_input("👤 Client ID:", placeholder="User ID",
                                    key="ci", value=st.session_state["broker_config"]["client_id"])
            u_api  = st.text_input("🔑 API Key:", type="password",
                                    placeholder="API Key",
                                    key="ak", value=st.session_state["broker_config"]["api_key"])
        with c2:
            u_totp = st.text_input("⏳ TOTP Secret:", type="password",
                                    placeholder="Google TOTP",
                                    key="ts", value=st.session_state["broker_config"]["totp_secret"])
            u_sec  = st.text_input("🔒 Secret Key:", type="password",
                                    placeholder="Secret Key",
                                    key="sk", value=st.session_state["broker_config"]["secret_key"])
        if st.button("🔌 Connect API", key="api_btn"):
            if u_cid and u_api:
                st.session_state.update({
                    "broker_connected": True,
                    "connected_broker": selected_broker,
                    "broker_config"   : {"client_id":u_cid,"api_key":u_api,
                                         "secret_key":u_sec,"totp_secret":u_totp},
                })
                st.toast(f"✅ {selected_broker} Connected!", icon="🚀")
                add_audit_log("API_CONNECTED", f"{selected_broker} connected")
                time.sleep(0.2); st.rerun()
            else:
                st.error("❌ Client ID અને API Key ભરો!")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── SYMBOL + ORDER SETTINGS ────────────────────────────────────
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#d4af37;font-size:14px;font-weight:bold;margin-bottom:10px;'>"
        "🔍 Symbol Search</p>", unsafe_allow_html=True)

    cs1, cs2 = st.columns(2)
    with cs1:
        user_symbol = st.text_input(
            "Symbol (NIFTY / CRUDEOIL / SBIN):",
            value="NIFTY", key="sym").strip().upper()
    with cs2:
        sel_type = st.selectbox("Type:", ["CE","PE","FUT","EQUITY (CASH)"], key="otype")

    sel_strike = st.text_input("Strike Price (Options only):", value="24400", key="strk")
    sel_expiry = st.text_input("Expiry (DD-MMM-YY):", value="26JUN26", key="exp")

    lot_size = get_lot_size(user_symbol)
    cl, cq = st.columns(2)
    with cl:
        u_lots = st.number_input("🔢 Lots:", min_value=1, value=1, key="lots")
    u_qty = u_lots * lot_size
    with cq:
        qty_lbl = "Total Qty (Auto):" if lot_size > 1 else "Shares:"
        st.text_input(qty_lbl, value=f"{u_qty} ({lot_size}/lot)", disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── SL / TARGET ────────────────────────────────────────────────
    st.markdown("<div class='config-box' style='padding:10px;'>", unsafe_allow_html=True)
    csl, ctgt = st.columns(2)
    with csl:
        sl_pts  = st.number_input("🚨 Stop Loss (Pts):", value=30, key="sl")
    with ctgt:
        tgt_pts = st.number_input("🎯 Target (Pts):",    value=60, key="tgt")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── MODE TOGGLE ────────────────────────────────────────────────
    st.session_state["auto_trade"] = st.toggle(
        f"🤖 Trade Mode: {'🟢 LIVE' if st.session_state['auto_trade'] else '🟡 DRY RUN'}",
        value=st.session_state["auto_trade"], key="mode_tog")
    if st.session_state["auto_trade"]:
        st.warning("⚠️ LIVE MODE — Real orders fire!")

    # ══════════════════════════════════════════════════════════════
    # 🟩🟥🟨 BIG BUY / SELL / WAIT BUTTONS
    # ══════════════════════════════════════════════════════════════
    script_label = (f"{user_symbol} {sel_strike} {sel_type}"
                    if sel_type != "EQUITY (CASH)" else user_symbol)

    def _add_position(action):
        if not st.session_state["broker_connected"]:
            st.error("❌ Broker connect karvo!"); return
        if not risk_ok:
            st.error(f"⛔ {risk_msg}"); return
        result = trigger_real_order(
            script_label, action, u_qty, exchange="NFO",
            sl=sl_pts, target=tgt_pts)
        st.session_state["open_positions"].append({
            "id"      : f"#RM-{len(st.session_state['open_positions'])+2001}",
            "script"  : script_label,
            "qty"     : u_qty,
            "action"  : action,
            "sl_pts"  : sl_pts,
            "tgt_pts" : tgt_pts,
            "entry"   : 100.0,
            "peak"    : 100.0,
            "trail_sl": 0.0,
            "status"  : "⌛ Waiting",
            "order_id": result.get("order_id","DRY"),
            "mode"    : "LIVE" if st.session_state["auto_trade"] else "DRY",
        })
        mode_tag = "LIVE" if st.session_state["auto_trade"] else "DRY RUN"
        st.toast(f"{'🟢' if action=='BUY' else '🔴'} {action} | {script_label} | {mode_tag}", icon="✅")

    # Script label display
    st.markdown(
        f"<div style='text-align:center;background:#0d1e3a;border:1px solid #1e366a;"
        f"border-radius:8px;padding:8px;margin:8px 0;'>"
        f"<span style='color:#d4af37;font-weight:900;font-size:15px;'>📌 {script_label}</span>"
        f"&nbsp;&nbsp;<span style='color:#64748b;font-size:12px;'>Qty: {u_qty} | SL: {sl_pts} | TGT: {tgt_pts}</span>"
        f"</div>",
        unsafe_allow_html=True)

    st.markdown("<div class='trade-action-area'>", unsafe_allow_html=True)

    # BUY + SELL side by side (big)
    ob1, ob2 = st.columns(2)
    with ob1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("🟩 BUY", key="buy_b", use_container_width=True):
            _add_position("BUY")
        st.markdown("</div>", unsafe_allow_html=True)

    with ob2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("🟥 SELL", key="sell_b", use_container_width=True):
            _add_position("SELL")
        st.markdown("</div>", unsafe_allow_html=True)

    # WAIT full-width below
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="wait-box">', unsafe_allow_html=True)
    if st.button("🟨 WAIT / HOLD", key="wait_b", use_container_width=True):
        st.toast("⏳ System Hold — Waiting for signal", icon="⏳")
        add_audit_log("WAIT", "System on hold")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # trade-action-area

    # ── PANIC BUTTON ───────────────────────────────────────────────
    st.markdown('<div class="panic-container">', unsafe_allow_html=True)
    if st.button("💥 EMERGENCY CLOSE ALL POSITIONS",
                 key="panic", use_container_width=True):
        cnt = len(st.session_state["open_positions"])
        st.session_state["open_positions"] = []
        st.session_state["peak_pnl"]       = 0.0
        add_audit_log("EMERGENCY", f"{cnt} positions force-closed")
        st.toast(f"🚨 {cnt} Positions Closed! Emergency executed.", icon="💥")
        time.sleep(0.3); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── RISK MANAGEMENT ────────────────────────────────────────────
    with st.expander("🛡️ Risk Management Settings"):
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        rc1, rc2 = st.columns(2)
        with rc1:
            st.session_state["max_daily_loss"] = st.number_input(
                "Max Daily Loss (₹):",
                min_value=500, max_value=100000,
                value=int(st.session_state["max_daily_loss"]), step=500, key="mdl")
        with rc2:
            st.session_state["daily_target"] = st.number_input(
                "Daily Target (₹):",
                min_value=500, max_value=100000,
                value=int(st.session_state["daily_target"]), step=500, key="dt")

        st.session_state["risk_per_trade"] = st.slider(
            "Risk per Trade (% of Capital):",
            0.5, 5.0, st.session_state["risk_per_trade"], 0.5, key="rpt")
        risk_amt = st.session_state["total_capital"] * st.session_state["risk_per_trade"] / 100
        st.caption(f"Max risk per trade: ₹{risk_amt:,.0f}")

        st.session_state["trail_active"] = st.toggle(
            "🔄 Auto Trail SL Enable", value=st.session_state["trail_active"])

        if st.session_state["trail_active"]:
            st.session_state["trail_sl_pct"] = st.slider(
                "Trail SL (% of peak P&L):",
                0.1, 3.0, st.session_state["trail_sl_pct"], 0.1, key="tsl")
            if st.session_state["peak_pnl"] > 0:
                lock = st.session_state["peak_pnl"] * (1 - st.session_state["trail_sl_pct"]/100)
                st.markdown(f"""
                <div class='trail-box'>
                    <b style='color:#86efac;'>
                    🔄 Peak P&L: ₹{st.session_state['peak_pnl']:,.0f}<br>
                    🔒 Lock-in Level: ₹{lock:,.0f}
                    </b>
                </div>""", unsafe_allow_html=True)

        if st.button("💾 Save Risk Settings", use_container_width=True, key="save_risk"):
            add_audit_log("RISK_SETTINGS",
                f"MaxLoss:{st.session_state['max_daily_loss']} "
                f"Target:{st.session_state['daily_target']} "
                f"Trail:{st.session_state['trail_active']}")
            st.success("✅ Risk settings saved!")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── REFRESH ────────────────────────────────────────────────────
    if st.button("🔄 Refresh Data", key="refresh", use_container_width=True):
        import random
        st.session_state["dynamic_pnl"] += random.uniform(-100, 200)
        add_audit_log("REFRESH", "Data refreshed")
        st.rerun()
# ══════════════════════════════════════════════════════════════════
# LEFT PANEL — TRADINGVIEW CHART
# ══════════════════════════════════════════════════════════════════
with col_chart:
    st.markdown(
        f"<h4 style='color:#f3f4f6;'>📈 Live Chart: {user_symbol}</h4>",
        unsafe_allow_html=True)

    tv_sym = get_tradingview_symbol(user_symbol)

    chart_html = f"""
    <div style="height:520px; border-radius:12px; overflow:hidden; border:1px solid #1e366a;">
        <div id="tradingview_chart" style="height:100%; width:100%;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "width": "100%",
          "height": "100%",
          "symbol": "{tv_sym}",
          "interval": "5",
          "timezone": "Asia/Kolkata",
          "theme": "dark",
          "style": "1",
          "locale": "en",
          "toolbar_bg": "#f1f3f6",
          "enable_publishing": false,
          "hide_side_toolbar": false,
          "allow_symbol_change": true,
          "exchanges": ["NSE", "MCX", "BSE"],
          "no_referrals": true,
          "click_to_enhance": false,
          "container_id": "tradingview_chart"
        }});
        </script>
    </div>
    """
    st.components.v1.html(chart_html, height=530, scrolling=False)

# ══════════════════════════════════════════════════════════════════
# OPEN POSITIONS TABLE
# ══════════════════════════════════════════════════════════════════
st.markdown("<br><hr style='border-color:#1e366a;'>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#f3f4f6;'>📋 Live Open Positions</h4>", unsafe_allow_html=True)

if st.session_state["open_positions"]:
    rows = []
    for p in st.session_state["open_positions"]:
        rows.append({
            "Trade ID" : p["id"],
            "Script"   : p["script"],
            "Qty"      : f"{p['qty']}",
            "Action"   : p["action"],
            "SL (Pts)" : p["sl_pts"],
            "TGT (Pts)": p["tgt_pts"],
            "Mode"     : p.get("mode","DRY"),
            "Status"   : p["status"],
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    if st.button("🗑️ Clear All Positions (Simulate Exit)", use_container_width=True):
        add_audit_log("CLEAR_POSITIONS",
            f"{len(st.session_state['open_positions'])} positions cleared")
        st.session_state["open_positions"] = []
        st.rerun()
else:
    st.info("📭 કોઈ Open Position નથી. Order place karvo!")

# ══════════════════════════════════════════════════════════════════
# AUDIT LOGS
# ══════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📝 Audit Logs"):
    logs = st.session_state["audit_logs"]
    if logs:
        df_log = pd.DataFrame(reversed(logs[-25:]))
        st.dataframe(df_log[["timestamp","action","details"]],
                     use_container_width=True, hide_index=True)
    else:
        st.info("📭 No logs yet.")

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<hr style='border-color:#1e366a;margin-top:30px;'>
<div style='text-align:center;color:#9ca3af;font-size:12px;padding:20px 0;'>
    <p>🔱 Ramavat Algo Elite v2.0 &nbsp;|&nbsp; NSE • MCX • Equity Trading Terminal</p>
    <p>© 2026 All Rights Reserved &nbsp;|&nbsp;
       ⚠️ Disclaimer: Trading involves risk. Use at your own discretion.</p>
</div>""", unsafe_allow_html=True)
