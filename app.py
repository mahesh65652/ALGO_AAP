"""
app.py — RAMAVAT ALGO ELITE  [v3.2 - FIXED]
===========================================
Centered Chart | Full Premium Border | No More Search Popups
"""

import streamlit as st
import time, random, requests
import pandas as pd
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

# ══════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════
_def = {
    "authenticated":False,"user_id":None,"login_time":None,
    "dark_mode":True,
    "broker_connected":False,"connected_broker":None,
    "broker_config":{"client_id":"","api_key":"","secret_key":"","totp_secret":"","password":""},
    "tg_token":"","tg_chat_id":"",
    "audit_logs":[],"open_positions":[],
    "dynamic_pnl":2695.0,"total_capital":150000.0,
    "max_daily_loss":5000.0,"daily_target":8000.0,
    "trail_sl_pct":0.5,"risk_per_trade":2.0,
    "auto_trade":False,"trail_active":False,"peak_pnl":0.0,
    "chart_symbol":"NIFTY",
}
for k,v in _def.items():
    if k not in st.session_state: st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════
# THEME CSS
# ══════════════════════════════════════════════════════════════════
dark = st.session_state["dark_mode"]

BG      = "#060913"  if dark else "#f0f2f6"
BG2     = "#0d162d"  if dark else "#ffffff"
CARD    = "#142247"  if dark else "#ffffff"
BORDER  = "#1e366a"  if dark else "#d1d5db"
TXT     = "#e2e8f0"  if dark else "#1a202c"
MUTED   = "#9ca3af"  if dark else "#6b7280"
GOLD    = "#d4af37"
GREEN   = "#00c851"
RED     = "#ff4444"
AMBER   = "#ffbb33"
BLUE    = "#3b82f6"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Rajdhani:wght@500;700;900&display=swap');

:root {{
  --bg:{BG}; --bg2:{BG2}; --card:{CARD};
  --border:{BORDER}; --txt:{TXT}; --muted:{MUTED};
  --gold:{GOLD}; --green:{GREEN}; --red:{RED};
  --amber:{AMBER}; --blue:{BLUE};
}}

/* GLOBAL */
.stApp {{ background:var(--bg) !important; }}
.main  {{ background:var(--bg) !important; }}
.main .block-container {{ max-width:1400px !important; padding:0.8rem !important; margin:0 auto !important; }}
* {{ color:var(--txt) !important; font-family:'Rajdhani',sans-serif !important; }}

/* HEADER */
.elite-hdr {{
  background:linear-gradient(135deg,{BG2},{CARD});
  border:1px solid var(--gold);
  border-radius:18px; padding:18px 14px;
  text-align:center; margin-bottom:12px;
  box-shadow:0 0 30px rgba(212,175,55,.12);
  position:relative; overflow:hidden;
}}
.elite-name {{
  font-size:2rem; font-weight:900; letter-spacing:3px;
  color:var(--gold) !important;
  text-shadow:0 0 20px rgba(212,175,55,.5);
}}
.elite-sub {{ font-size:.7rem; color:var(--muted) !important; letter-spacing:3px; font-family:'JetBrains Mono',monospace !important; }}

/* BIG METRIC CARDS */
.metric-row {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:10px 0; }}
.metric-card {{
  background:var(--card); border:1px solid var(--border);
  border-radius:14px; padding:14px 10px; text-align:center;
}}
.metric-lbl {{ font-size:.65rem; color:var(--muted) !important; letter-spacing:2px; font-family:'JetBrains Mono',monospace !important; }}
.metric-val {{ font-size:1.8rem; font-weight:900; font-family:'JetBrains Mono',monospace !important; }}
.c-green {{ color:{GREEN} !important; }}
.c-red   {{ color:{RED} !important; }}
.c-gold  {{ color:{GOLD} !important; }}
.c-blue  {{ color:{BLUE} !important; }}

/* SECTION LABEL */
.sec-lbl {{
  font-size:.65rem; color:var(--muted) !important; letter-spacing:3px;
  font-family:'JetBrains Mono',monospace !important;
  text-transform:uppercase; padding-bottom:6px;
  border-bottom:1px solid var(--border); margin:14px 0 8px;
}}

.cfg {{ background:var(--bg2); border:1px solid var(--border); border-radius:12px; padding:14px; margin-bottom:10px; }}

/* BUY/SELL/WAIT BUTTONS */
.buy-w  .stButton>button {{ background:linear-gradient(90deg,#00c851,#007e33) !important; color:#000 !important; }}
.sell-w .stButton>button {{ background:linear-gradient(90deg,#ff4444,#cc0000) !important; color:#fff !important; }}
.wait-w .stButton>button {{ background:linear-gradient(90deg,#ffbb33,#ff8800) !important; color:#000 !important; }}

.stButton>button {{
  width:100% !important; border-radius:12px !important;
  height:46px !important; font-weight:800 !important; text-transform:uppercase !important;
}}

/* 📦 PREMIUM FULL BORDER BOX FOR CHART */
.chart-box-wrapper {{
  border: 3px solid var(--gold) !important; /* ગોલ્ડન પ્રીમિયમ બોર્ડર */
  border-radius: 16px;
  padding: 8px;
  background: var(--bg2);
  box-shadow: 0 0 25px rgba(212,175,55,0.15);
  margin-bottom: 15px;
}}

.login-card {{
  background:var(--card); border:1px solid var(--border);
  border-radius:18px; padding:28px 20px; text-align:center;
}}
#MainMenu,footer,header,.stDeployButton {{ visibility:hidden !important; display:none !important; }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════
def get_tv_sym(sym):
    mp = {
        "NIFTY": "NSE:NIFTY",
        "BANKNIFTY": "NSE:BANKNIFTY",
        "FINNIFTY": "NSE:FINNIFTY",
        "SENSEX": "BSE:SENSEX",
        "CRUDEOIL": "MCX:CRUDEOIL1!",
        "NATURALGAS": "MCX:NATURALGAS1!",
    }
    return mp.get(sym.upper(), f"NSE:{sym.upper()}")

# ══════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════
if not st.session_state["authenticated"]:
    st.markdown('<div class="elite-hdr"><div class="elite-name">🔱 RAMAVAT ALGO</div></div>', unsafe_allow_html=True)
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    lu = st.text_input("👤 User ID", placeholder="Enter User ID")
    lp = st.text_input("🔑 Password", type="password", placeholder="Password")
    if st.button("🚀 UNLOCK TERMINAL", use_container_width=True):
        if lp == "1234":
            st.session_state.update({"authenticated":True,"user_id":lu,"login_time":datetime.now()})
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════
# MAIN INTERFACE (LAYOUT)
# ══════════════════════════════════════════════════════════════════
pnl = st.session_state["dynamic_pnl"]

# ── [1] TOP: HEADER & KPI METRICS ─────────────────────────────────
hc1, hc2 = st.columns([3,1])
with hc1:
    st.markdown(f'<div class="elite-hdr"><div class="elite-name">🔱 RAMAVAT ALGO ELITE</div><div class="elite-sub">CONNECTED TO SYSTEM</div></div>', unsafe_allow_html=True)
with hc2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT", use_container_width=True):
        st.session_state["authenticated"] = False; st.rerun()

st.markdown(f"""
<div class="metric-row">
  <div class="metric-card"><div class="metric-lbl">📊 TODAY P&L</div><div class="metric-val c-green">₹{pnl:,.2f}</div></div>
  <div class="metric-card"><div class="metric-lbl">💰 TOTAL CAPITAL</div><div class="metric-val c-gold">₹{st.session_state["total_capital"]:,.0f}</div></div>
</div>
""", unsafe_allow_html=True)

# ── [2] TOP CONTROLS: API & RISK CONFIGS ──────────────────────────
with st.expander("🔌 Broker Config & Telegram Setup"):
    st.text_input("Client ID:", value="MRARAMAVAT52")
    st.button("🔌 Connect API")

with st.expander("🛡️ Risk & Target Settings"):
    st.number_input("Max Loss Limit:", value=5000)

# ── [3] CENTER: THE LIVE CHART (વચ્ચે ફૂલ ગોલ્ડન બોર્ડર સાથે) ──────────
st.markdown('<div class="sec-lbl">📈 LIVE MARKET CHART</div>', unsafe_allow_html=True)

cc1, cc2 = st.columns([3,1])
with cc1:
    sym_opts = ["NIFTY","BANKNIFTY","SENSEX","FINNIFTY","CRUDEOIL","NATURALGAS"]
    usym = st.selectbox("Symbol", sym_opts, label_visibility="collapsed")
with cc2:
    tf = st.selectbox("TF", ["1","3","5","15","30","60","D"], index=2, label_visibility="collapsed")

# TradingView Advanced Widget Code (આનાથી સર્ચ પોપઅપ ગાયબ થઈ જશે)
tv_symbol = get_tv_sym(usym)
chart_html = f"""
<div id="tradingview_widget"></div>
<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
<script type="text/javascript">
new TradingView.widget({{
  "autosize": true,
  "symbol": "{tv_symbol}",
  "interval": "{tf}",
  "timezone": "Asia/Kolkata",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "enable_publishing": false,
  "hide_side_toolbar": false,
  "allow_symbol_change": false,
  "studies": ["RSI@tv-basicstudies"],
  "container_id": "tradingview_widget"
}});
</script>
<style>
  html, body, #tradingview_widget {{ height: 100%; margin: 0; padding: 0; background-color: #060913; }}
</style>
"""

# આ રહ્યું ફૂલ બોર્ડર વાળું કન્ટેનર
st.markdown('<div class="chart-box-wrapper">', unsafe_allow_html=True)
st.components.v1.html(chart_html, height=500, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)

# ── [4] BOTTOM: ORDER CONTROL CENTER & BUTTONS ────────────────────
st.markdown('<div class="sec-lbl">⚡ ORDER CONTROL CENTER</div>', unsafe_allow_html=True)
st.markdown("<div class='cfg'>", unsafe_allow_html=True)
oc1, oc2, oc3 = st.columns(3)
with oc1:
    st.text_input("Strike Price:", value="24400")
with oc2:
    st.text_input("Expiry:", value="26JUN26")
with oc3:
    st.number_input("Lots:", min_value=1, value=1)
st.markdown("</div>", unsafe_allow_html=True)

b1, b2, b3 = st.columns(3)
with b1:
    st.markdown('<div class="buy-w">', unsafe_allow_html=True)
    st.button("🟩 BUY", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with b2:
    st.markdown('<div class="sell-w">', unsafe_allow_html=True)
    st.button("🟥 SELL", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with b3:
    st.markdown('<div class="wait-w">', unsafe_allow_html=True)
    if st.button("🔄 REFRESH", use_container_width=True): st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# POSITIONS STATUS
st.markdown('<div class="sec-lbl">📋 LIVE OPEN POSITIONS</div>', unsafe_allow_html=True)
st.info("કોઈ Open Position નથી. Order place karvo!")
