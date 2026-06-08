"""
app.py — RAMAVAT ALGO ELITE  [v3.0]
=====================================
Mobile-First | Chart Top | Big Digits
Light + Dark Mode | Telegram + Trade
Multi-Broker | Remote Control Ready
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
.elite-hdr::before {{
  content:''; position:absolute;
  top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
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
  background:var(--card);
  border:1px solid var(--border);
  border-radius:14px; padding:14px 10px;
  text-align:center; transition:.3s;
}}
.metric-card:hover {{ border-color:var(--gold); }}
.metric-lbl {{ font-size:.65rem; color:var(--muted) !important; letter-spacing:2px; font-family:'JetBrains Mono',monospace !important; margin-bottom:4px; }}
.metric-val {{ font-size:1.8rem; font-weight:900; font-family:'JetBrains Mono',monospace !important; }}
.metric-delta {{ font-size:.7rem; margin-top:3px; font-family:'JetBrains Mono',monospace !important; }}
.c-green {{ color:{GREEN} !important; }}
.c-red   {{ color:{RED} !important; }}
.c-gold  {{ color:{GOLD} !important; }}
.c-blue  {{ color:{BLUE} !important; }}
.c-muted {{ color:{MUTED} !important; }}

/* STATUS DOT */
.live-dot {{
  display:inline-flex; align-items:center; gap:5px;
  background:rgba(0,200,81,.1); border:1px solid {GREEN};
  border-radius:20px; padding:3px 10px;
  font-size:.68rem; font-family:'JetBrains Mono',monospace !important;
  color:{GREEN} !important; margin-top:6px;
}}
.dot {{ width:7px;height:7px;background:{GREEN};border-radius:50%; animation:pulse 1.5s infinite; }}
@keyframes pulse {{ 0%,100%{{opacity:1;transform:scale(1)}} 50%{{opacity:.4;transform:scale(1.4)}} }}

/* SECTION LABEL */
.sec-lbl {{
  font-size:.65rem; color:var(--muted) !important; letter-spacing:3px;
  font-family:'JetBrains Mono',monospace !important;
  text-transform:uppercase; padding-bottom:6px;
  border-bottom:1px solid var(--border); margin:14px 0 8px;
}}

/* CONFIG BOX */
.cfg {{ background:var(--bg2); border:1px solid var(--border); border-radius:12px; padding:14px; margin-bottom:10px; }}

/* PANIC */
@keyframes ppulse {{
  0%{{box-shadow:0 0 0 0 rgba(220,38,38,.7)}}
  70%{{box-shadow:0 0 0 10px rgba(220,38,38,0)}}
  100%{{box-shadow:0 0 0 0 rgba(220,38,38,0)}}
}}
.panic-wrap .stButton>button {{
  background:linear-gradient(90deg,#7f1d1d,#dc2626) !important;
  color:white !important; border:2px solid #ef4444 !important;
  height:54px !important; font-weight:900 !important; font-size:15px !important;
  animation:ppulse 2s infinite !important; border-radius:12px !important;
}}
.panic-wrap .stButton>button:hover {{ animation:none !important; }}

/* BUY/SELL/WAIT */
.buy-w  .stButton>button {{ background:linear-gradient(90deg,#00c851,#007e33) !important; color:#000 !important; }}
.sell-w .stButton>button {{ background:linear-gradient(90deg,#ff4444,#cc0000) !important; color:#fff !important; }}
.wait-w .stButton>button {{ background:linear-gradient(90deg,#ffbb33,#ff8800) !important; color:#000 !important; }}

/* ALL BUTTONS */
.stButton>button {{
  width:100% !important; border-radius:12px !important;
  height:46px !important; font-weight:800 !important;
  font-size:14px !important; border:none !important;
  transition:all .2s !important; text-transform:uppercase !important;
}}
.stButton>button:hover {{ transform:translateY(-2px) !important; }}

/* INPUTS */
.stTextInput input, .stNumberInput input, .stPasswordInput input {{
  background:var(--bg2) !important; color:var(--txt) !important;
  border:1px solid var(--border) !important; border-radius:9px !important;
  font-family:'JetBrains Mono',monospace !important;
}}
.stTextInput input:focus {{ border-color:var(--blue) !important; }}

/* TABLE */
.stDataFrame {{ border:1px solid var(--border) !important; border-radius:10px !important; }}

/* PROGRESS */
.stProgress>div>div {{ background:linear-gradient(90deg,{GOLD},{GREEN}) !important; border-radius:4px !important; }}

/* TOGGLE */
.stToggle label {{ font-size:.9rem !important; }}

/* RISK/TRAIL BOXES */
.risk-box {{
  background:linear-gradient(135deg,#3d1c1a,#2d0f0f);
  border:2px solid #dc2626; border-radius:10px; padding:10px 14px; margin:8px 0;
}}
.trail-box {{
  background:linear-gradient(135deg,#0d2d1a,#0f3a20);
  border:1px solid #22c55e; border-radius:10px; padding:10px 14px; margin:8px 0;
}}

/* LOGIN */
.login-card {{
  background:var(--card); border:1px solid var(--border);
  border-radius:18px; padding:28px 20px; text-align:center; margin:20px 0;
}}

/* CHART CONTAINER */
.chart-container {{
  background:var(--card); 
  border:1px solid var(--border); 
  border-radius:14px; 
  padding:0;
  overflow:hidden;
  height:500px !important;
}}

#MainMenu,footer,header,.stDeployButton {{ visibility:hidden !important; display:none !important; }}
</style>
""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════
def add_log(action, details=""):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state["audit_logs"].insert(0, {
        "time":ts, "user":st.session_state.get("user_id","—"),
        "action":action, "details":details})
    if len(st.session_state["audit_logs"]) > 50:
        st.session_state["audit_logs"] = st.session_state["audit_logs"][:50]

def send_telegram(msg: str):
    tok = st.session_state.get("tg_token","")
    cid = st.session_state.get("tg_chat_id","")
    if not tok or not cid: return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/sendMessage",
            data={"chat_id":cid,"text":msg,"parse_mode":"HTML"}, timeout=6)
        return r.status_code == 200
    except: return False

def get_lot_size(sym):
    lots = {
        "NIFTY":50,"BANKNIFTY":15,"FINNIFTY":25,"MIDCPNIFTY":10,"SENSEX":10,"BANKEX":15,
        "CRUDEOIL":100,"CRUDEOILM":10,"NATURALGAS":1250,"NATGASMINI":250,
        "GOLD":100,"GOLDM":10,"SILVER":30,"SILVERM":5,"COPPER":250,
    }
    return lots.get(sym.upper().replace("-EQ",""),1)

def get_tv_sym(sym):
    mp = {
        "NIFTY":"NIFTY1!","BANKNIFTY":"BANKNIFTY1!",
        "FINNIFTY":"FINNIFTY1!","MIDCPNIFTY":"MIDCPNIFTY1!",
        "SENSEX":"SENSEX1!",
        "CRUDEOIL":"CRUDEOIL1!","NATURALGAS":"NATURALGAS1!",
        "GOLD":"GOLD1!","SILVER":"SILVER1!","COPPER":"COPPER1!",
    }
    s = sym.upper().replace("-EQ","")
    return mp.get(s, f"NSE:{s}")

def check_risk():
    pnl = st.session_state["dynamic_pnl"]
    if pnl < -st.session_state["max_daily_loss"]:
        return False, f"Max Daily Loss ₹{st.session_state['max_daily_loss']:,.0f} Breach!"
    if pnl >= st.session_state["daily_target"]:
        return False, f"Daily Target ₹{st.session_state['daily_target']:,.0f} Hit!"
    return True,"OK"

def trigger_order(symbol, action, qty, exchange="NFO", sl=0.0, target=0.0):
    """
    PROFESSIONAL ORDER ENGINE — Angel One SmartAPI
    ─────────────────────────────────────────────
    To activate LIVE trading:
      1. Set AUTO_TRADE toggle = LIVE
      2. Connect Broker API with credentials
      3. Replace simulation block below with:

      from SmartApi import SmartConnect
      import pyotp
      cfg = st.session_state["broker_config"]
      obj = SmartConnect(api_key=cfg["api_key"])
      obj.generateSession(
          cfg["client_id"], cfg["password"],
          pyotp.TOTP(cfg["totp_secret"]).now())
      resp = obj.placeOrder({
          "variety":"NORMAL","tradingsymbol":symbol,
          "symboltoken": <fetch_token_from_master>,
          "transactiontype":action,"exchange":exchange,
          "ordertype":"MARKET","producttype":"INTRADAY",
          "duration":"DAY","price":"0","quantity":str(qty),
      })
      return {"status":"SUCCESS","order_id":resp["data"]["orderid"]}
    ─────────────────────────────────────────────
    """
    mode = "LIVE" if st.session_state["auto_trade"] else "DRY"
    oid  = f"RM{random.randint(1000000,9999999)}" if st.session_state["auto_trade"] else None

    # Telegram alert (always sent if configured)
    direction = "📈 BUY" if action=="BUY" else "📉 SELL"
    color_dot  = "🟢" if action=="BUY" else "🔴"
    tg_msg = (
        f"{color_dot} <b>RAMAVAT ALGO — {mode} ORDER</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📋 <b>{symbol}</b> | {direction}\n"
        f"🔢 Qty: {qty} | Exchange: {exchange}\n"
        f"🛑 SL: {sl} pts | 🎯 TGT: {target} pts\n"
        f"━━━━━━━━━━━━━━━\n"
        + (f"✅ Order ID: <code>{oid}</code>\n" if oid else "🟡 DRY RUN — No real order\n") +
        f"⏰ {datetime.now().strftime('%d-%b %I:%M %p')}\n"
        f"#RamavatAlgo #{action} #{exchange}"
    )
    tg_ok = send_telegram(tg_msg)

    add_log(f"{action} [{mode}]", f"{qty}x {symbol} SL:{sl} TGT:{target} TG:{'✅' if tg_ok else '—'}")
    return {"status": "LIVE" if oid else "DRY_RUN", "order_id": oid}

# ══════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════
if not st.session_state["authenticated"]:
    st.markdown("""
    <div class="elite-hdr">
      <div class="elite-name">🔱 RAMAVAT ALGO</div>
      <div class="elite-sub">ELITE TRADING TERMINAL v3.0</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:2.5rem;'>🔐</div>"
                f"<p style='color:{MUTED};margin-bottom:16px;'>સાહેબ, User ID અને Password નાખો</p>",
                unsafe_allow_html=True)
    lu = st.text_input("👤 User ID", placeholder="Enter User ID", key="lu", label_visibility="collapsed")
    lp = st.text_input("🔑 Password", type="password", placeholder="Password (default: 1234)", key="lp", label_visibility="collapsed")
    if st.button("🚀 UNLOCK TERMINAL", use_container_width=True):
        if lu and lp == "1234":
            st.session_state.update({"authenticated":True,"user_id":lu,"login_time":datetime.now()})
            add_log("LOGIN", f"'{lu}' logged in")
            st.success(f"✅ Welcome {lu}! Login સફળ 🚀")
            st.balloons(); time.sleep(1); st.rerun()
        else:
            st.error("❌ ખોટો Password!")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:{MUTED};font-size:.7rem;margin-top:12px;'>Demo: Any ID | Password: 1234</p>", unsafe_allow_html=True)
    st.stop()
# ══════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════
risk_ok, risk_msg = check_risk()
pnl = st.session_state["dynamic_pnl"]

# Risk alerts
if not risk_ok:
    st.markdown(f"<div class='risk-box'><b style='color:#fca5a5;'>⚠️ {risk_msg}</b></div>",
                unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────
uid = st.session_state.get("user_id","Operator")
lt  = st.session_state.get("login_time")
lts = lt.strftime("%H:%M") if lt else "—"
bconn = st.session_state["broker_connected"]
bname = st.session_state.get("connected_broker","None")
mode_str = "🟢 LIVE" if st.session_state["auto_trade"] else "🟡 DRY"

hc1, hc2 = st.columns([3,1])
with hc1:
    st.markdown(f"""
    <div class="elite-hdr">
      <div class="elite-name">🔱 RAMAVAT ALGO</div>
      <div class="elite-sub">NSE • MCX • EQUITY TERMINAL</div>
      <div class="live-dot" style="display:inline-flex;">
        <span class="dot"></span> LIVE • {lts} • {uid}
      </div>
    </div>""", unsafe_allow_html=True)
with hc2:
    # Dark/Light toggle
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🌙" if dark else "☀️", key="theme_btn",
                 help="Dark/Light Mode"):
        st.session_state["dark_mode"] = not dark; st.rerun()
    if st.button("🚪", key="lo", help="Logout"):
        st.session_state["authenticated"] = False
        add_log("LOGOUT"); st.rerun()

# Status bar
st.markdown(
    f"{'🟢' if bconn else '🔴'} **{bname}** &nbsp;|&nbsp; "
    f"Mode: **{mode_str}** &nbsp;|&nbsp; "
    f"{'✅ Connected' if bconn else '❌ Setup needed'}",
    unsafe_allow_html=True)

# ── BIG METRIC CARDS ───────────────────────────────────────────────
pnl_c = "c-green" if pnl >= 0 else "c-red"
pnl_d = f"+₹{pnl:,.0f}" if pnl >= 0 else f"-₹{abs(pnl):,.0f}"
cap   = st.session_state["total_capital"]
npos  = len(st.session_state["open_positions"])

st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="metric-lbl">📊 TODAY P&L</div>
    <div class="metric-val {pnl_c}">{pnl_d}</div>
    <div class="metric-delta {pnl_c}">{'▲ PROFIT' if pnl>=0 else '▼ LOSS'}</div>
  </div>
  <div class="metric-card">
    <div class="metric-lbl">💰 CAPITAL</div>
    <div class="metric-val c-gold">₹{cap/1000:.0f}K</div>
    <div class="metric-delta c-muted">AVAILABLE</div>
  </div>
  <div class="metric-card">
    <div class="metric-lbl">🎯 POSITIONS</div>
    <div class="metric-val c-blue">{npos}</div>
    <div class="metric-delta c-muted">OPEN</div>
  </div>
  <div class="metric-card">
    <div class="metric-lbl">🔌 API</div>
    <div class="metric-val {'c-green' if bconn else 'c-red'}" style="font-size:1.1rem!important;">{'LIVE ✅' if bconn else 'SETUP ❌'}</div>
    <div class="metric-delta c-muted">{bname[:12] if bconn else 'Not connected'}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Progress bars
l_pct = min(max(-pnl,0)/st.session_state["max_daily_loss"],1.0)
t_pct = min(max(pnl,0)/st.session_state["daily_target"],1.0)
pc1,pc2 = st.columns(2)
with pc1:
    st.caption(f"🛑 Loss: {l_pct*100:.0f}% of ₹{st.session_state['max_daily_loss']:,.0f}")
    st.progress(l_pct)
with pc2:
    st.caption(f"🎯 Target: {t_pct*100:.0f}% of ₹{st.session_state['daily_target']:,.0f}")
    st.progress(t_pct)

# ══════════════════════════════════════════════════════════════════
# SYMBOL SELECTOR + CHART (WIDE LAYOUT)
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-lbl">📈 LIVE CHART</div>', unsafe_allow_html=True)

# Chart controls in a neat row
chart_col1, chart_col2, chart_col3 = st.columns([2, 1, 1])

with chart_col1:
    sym_opts = ["NIFTY","BANKNIFTY","SENSEX","FINNIFTY","CRUDEOIL","NATURALGAS","GOLD","SILVER"]
    usym = st.selectbox("Symbol:", sym_opts,
        index=sym_opts.index(st.session_state.get("chart_symbol","NIFTY")),
        key="chart_sym_sel", label_visibility="collapsed")
    st.session_state["chart_symbol"] = usym

with chart_col2:
    tf = st.select_slider("Timeframe:", ["1","3","5","15","30","60","D"], value="5", label_visibility="collapsed")

with chart_col3:
    if st.button("🔄 Refresh", help="Reload Chart"):
        st.rerun()

# ── LIGHTWEIGHT CHARTS (No CORS Issues) ────────────────────────────
tv_theme = "dark" if dark else "light"

chart_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <script src='https://unpkg.com/lightweight-charts@4/dist/lightweight-charts.standalone.production.js'></script>
    <style>
        body {{ margin:0; padding:0; background:transparent; }}
        #container {{ width:100%; height:500px; }}
    </style>
</head>
<body>
    <div id='container'></div>
    <script>
        const container = document.getElementById('container');
        const chart = LightweightCharts.createChart(container, {{
            layout: {{
                background: {{ color: '{"#060913" if dark else "#f0f2f6"}' }},
                textColor: '{"#e2e8f0" if dark else "#1a202c"}',
            }},
            width: container.clientWidth,
            height: 500,
            timeScale: {{
                timeVisible: true,
                secondsVisible: false,
            }},
        }});
        
        const candlestickSeries = chart.addCandlestickSeries({{
            upColor: '#00c851',
            downColor: '#ff4444',
            borderDownColor: '#ff4444',
            borderUpColor: '#00c851',
            wickDownColor: '#ff4444',
            wickUpColor: '#00c851',
        }});
        
        // Generate realistic OHLC data
        const now = Math.floor(Date.now() / 1000);
        const data = [];
        let price = 21000;
        
        for (let i = 50; i > 0; i--) {{
            const volatility = (Math.random() - 0.5) * 100;
            const o = price + volatility;
            const h = Math.max(o, price + Math.random() * 100);
            const l = Math.min(o, price - Math.random() * 100);
            const c = l + Math.random() * (h - l);
            
            data.push({{
                time: now - (i * 300),
                open: o,
                high: h,
                low: l,
                close: c,
            }});
            price = c;
        }}
        
        candlestickSeries.setData(data);
        chart.timeScale().fitContent();
        
        // Add RSI indicator (line series)
        const rsiSeries = chart.addLineSeries({{ 
            color: '#3b82f6',
            lineWidth: 2,
            title: 'RSI(14)'
        }});
        
        const rsiData = data.map((d, i) => ({
            time: d.time,
            value: 30 + Math.sin(i / 5) * 30 + Math.random() * 10
        }));
        
        rsiSeries.setData(rsiData);
        
        // Responsive resize
        window.addEventListener('resize', () => {{
            if(container.clientWidth > 0) {{
                chart.applyOptions({{ width: container.clientWidth }});
            }}
        }});
    </script>
</body>
</html>
"""

st.markdown(f'<div class="chart-container">', unsafe_allow_html=True)
st.components.v1.html(chart_html, height=520, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# ORDER CONTROLS (below chart)
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-lbl">⚙️ ORDER CONTROLS</div>', unsafe_allow_html=True)

st.markdown("<div class='cfg'>", unsafe_allow_html=True)
oc1,oc2 = st.columns(2)
with oc1:
    sym_inp = st.text_input("Symbol:", value=usym, key="sym_i").strip().upper()
    otype   = st.selectbox("Type:", ["CE","PE","FUT","EQUITY"], key="otyp")
with oc2:
    strike  = st.text_input("Strike:", value="24400", key="strk")
    expiry  = st.text_input("Expiry:", value="26JUN26", key="expy")

ls = get_lot_size(sym_inp)
lc1,lc2 = st.columns(2)
with lc1:
    ulots = st.number_input("Lots:", min_value=1, value=1, key="lots")
uqty = ulots * ls
with lc2:
    st.text_input("Total Qty:", value=f"{uqty} ({ls}/lot)", disabled=True)

sc1,sc2 = st.columns(2)
with sc1: sl_pts  = st.number_input("🚨 SL (Pts):",  value=30, key="slp")
with sc2: tgt_pts = st.number_input("🎯 TGT (Pts):", value=60, key="tgtp")
st.markdown("</div>", unsafe_allow_html=True)

# Mode toggle
st.session_state["auto_trade"] = st.toggle(
    f"{'🟢 LIVE TRADE MODE' if st.session_state['auto_trade'] else '🟡 DRY RUN MODE'}",
    value=st.session_state["auto_trade"])
if st.session_state["auto_trade"]:
    st.warning("⚠️ LIVE MODE — Real orders + Telegram!")

script = f"{sym_inp} {strike} {otype}" if otype!="EQUITY" else sym_inp

def _place(action):
    if not st.session_state["broker_connected"] and st.session_state["auto_trade"]:
        st.error("❌ Broker connect karvo!"); return
    if not risk_ok: st.error(f"⛔ {risk_msg}"); return
    res = trigger_order(script, action, uqty,
                        exchange="NFO" if otype in ["CE","PE","FUT"] else "NSE",
                        sl=sl_pts, target=tgt_pts)
    st.session_state["open_positions"].append({
        "id":f"#RM-{len(st.session_state['open_positions'])+2001}",
        "script":script,"qty":uqty,"action":action,
        "sl":sl_pts,"tgt":tgt_pts,"entry":100.0,
        "status":"⌛ Waiting","oid":res.get("order_id","DRY"),
        "mode":"LIVE" if st.session_state["auto_trade"] else "DRY",
    })
    icon = "🟢" if action=="BUY" else "🔴"
    st.toast(f"{icon} {action} | {script} | {'LIVE ✅' if st.session_state['auto_trade'] else 'DRY 🟡'}")

# BUY / SELL / WAIT
b1,b2,b3 = st.columns(3)
with b1:
    st.markdown('<div class="buy-w">', unsafe_allow_html=True)
    if st.button("🟩 BUY",  key="bb", use_container_width=True): _place("BUY")
    st.markdown("</div>", unsafe_allow_html=True)
with b2:
    st.markdown('<div class="sell-w">', unsafe_allow_html=True)
    if st.button("🟥 SELL", key="sb", use_container_width=True): _place("SELL")
    st.markdown("</div>", unsafe_allow_html=True)
with b3:
    st.markdown('<div class="wait-w">', unsafe_allow_html=True)
    if st.button("🟨 WAIT", key="wb", use_container_width=True):
        st.toast("⏳ On Hold"); add_log("WAIT","On hold")
    st.markdown("</div>", unsafe_allow_html=True)

# PANIC
st.markdown('<div class="panic-wrap">', unsafe_allow_html=True)
if st.button("💥 EMERGENCY CLOSE ALL POSITIONS", key="panic", use_container_width=True):
    cnt = len(st.session_state["open_positions"])
    send_telegram(f"🚨 <b>EMERGENCY CLOSE</b>\n{cnt} positions force-closed!\n⏰ {datetime.now().strftime('%I:%M %p')}")
    st.session_state.update({"open_positions":[],"peak_pnl":0.0})
    add_log("EMERGENCY", f"{cnt} positions closed")
    st.toast(f"🚨 {cnt} Positions Closed!"); st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SETTINGS EXPANDERS
# ══════════════════════════════════════════════════════════════════

# BROKER CONFIG
with st.expander("🔌 Broker API & Telegram Setup"):
    st.markdown("<div class='cfg'>", unsafe_allow_html=True)
    sel_b = st.selectbox("Broker:", [b.value for b in BrokerType], key="bsel")
    bc1,bc2 = st.columns(2)
    with bc1:
        ucid  = st.text_input("Client ID:", key="ucid", value=st.session_state["broker_config"]["client_id"])
        uapi  = st.text_input("API Key:",   type="password", key="uapi", value=st.session_state["broker_config"]["api_key"])
        upwd  = st.text_input("Password:", type="password", key="upwd", value=st.session_state["broker_config"]["password"])
    with bc2:
        utotp = st.text_input("TOTP Secret:", type="password", key="utotp", value=st.session_state["broker_config"]["totp_secret"])
        usec  = st.text_input("Secret Key:", type="password", key="usec",  value=st.session_state["broker_config"]["secret_key"])
    if st.button("🔌 Connect Broker", use_container_width=True, key="conn"):
        if ucid and uapi:
            st.session_state.update({
                "broker_connected":True,"connected_broker":sel_b,
                "broker_config":{"client_id":ucid,"api_key":uapi,
                                  "secret_key":usec,"totp_secret":utotp,"password":upwd}})
            add_log("BROKER_CONNECTED", sel_b)
            st.toast(f"✅ {sel_b} Connected!"); time.sleep(.2); st.rerun()
        else: st.error("❌ Client ID & API Key ભરો!")
    st.markdown("</div>", unsafe_allow_html=True)

    # TELEGRAM
    st.markdown('<div class="sec-lbl">📱 TELEGRAM ALERTS</div>', unsafe_allow_html=True)
    st.markdown("<div class='cfg'>", unsafe_allow_html=True)
    tc1,tc2 = st.columns(2)
    with tc1:
        tg_tok = st.text_input("Bot Token:", type="password", key="tgt",
                                value=st.session_state.get("tg_token",""))
    with tc2:
        tg_cid = st.text_input("Chat ID:", key="tgc",
                                value=st.session_state.get("tg_chat_id",""))
    if st.button("📱 Test Telegram", use_container_width=True, key="tg_test"):
        st.session_state["tg_token"]   = tg_tok
        st.session_state["tg_chat_id"] = tg_cid
        ok = send_telegram(
            "✅ <b>Ramavat Algo Elite — Telegram Test</b>\n"
            f"Connection successful!\n⏰ {datetime.now().strftime('%I:%M %p')}")
        st.success("✅ Telegram OK!") if ok else st.error("❌ Token/Chat ID check karvo!")
    st.markdown("</div>", unsafe_allow_html=True)

# RISK MANAGEMENT
with st.expander("🛡️ Risk Management"):
    st.markdown("<div class='cfg'>", unsafe_allow_html=True)
    rr1,rr2 = st.columns(2)
    with rr1:
        st.session_state["max_daily_loss"] = st.number_input(
            "Max Daily Loss (₹):", min_value=500, max_value=200000,
            value=int(st.session_state["max_daily_loss"]), step=500)
    with rr2:
        st.session_state["daily_target"] = st.number_input(
            "Daily Target (₹):", min_value=500, max_value=200000,
            value=int(st.session_state["daily_target"]), step=500)
    st.session_state["risk_per_trade"] = st.slider(
        "Risk per Trade (%):", 0.5, 5.0, st.session_state["risk_per_trade"], 0.5)
    risk_amt = st.session_state["total_capital"] * st.session_state["risk_per_trade"] / 100
    st.caption(f"Max risk per trade: ₹{risk_amt:,.0f}")
    st.session_state["trail_active"] = st.toggle("🔄 Auto Trail SL", value=st.session_state["trail_active"])
    if st.session_state["trail_active"]:
        st.session_state["trail_sl_pct"] = st.slider("Trail %:", 0.1, 3.0, st.session_state["trail_sl_pct"], 0.1)
    if st.button("💾 Save", use_container_width=True, key="risk_save"):
        add_log("RISK_SAVED","Updated"); st.success("✅ Saved!")
    st.markdown("</div>", unsafe_allow_html=True)

# REFRESH
if st.button("🔄 Refresh P&L", use_container_width=True, key="ref"):
    st.session_state["dynamic_pnl"] += random.uniform(-150,250)
    add_log("REFRESH"); st.rerun()

# ══════════════════════════════════════════════════════════════════
# POSITIONS TABLE
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-lbl">📋 OPEN POSITIONS</div>', unsafe_allow_html=True)
if st.session_state["open_positions"]:
    df = pd.DataFrame([{
        "ID":p["id"],"Script":p["script"],"Qty":p["qty"],
        "Action":p["action"],"SL":p["sl"],"TGT":p["tgt"],
        "Mode":p["mode"],"Status":p["status"],
    } for p in st.session_state["open_positions"]])
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.button("🗑️ Clear Positions", use_container_width=True, key="clr"):
        add_log("CLEAR",f"{len(st.session_state['open_positions'])} cleared")
        st.session_state["open_positions"]=[]; st.rerun()
else:
    st.info("📭 No open positions. Place an order!")

# AUDIT LOGS
with st.expander("📝 Audit Logs"):
    logs = st.session_state["audit_logs"]
    if logs:
        st.dataframe(pd.DataFrame(logs[:20])[["time","action","details"]],
                     use_container_width=True, hide_index=True)
    else: st.info("📭 No logs yet.")

# FOOTER
st.markdown(f"""
<hr style='border-color:{BORDER};margin-top:24px;'>
<div style='text-align:center;color:{MUTED};font-size:.65rem;padding:14px 0;'>
  🔱 Ramavat Algo Elite v3.0 &nbsp;|&nbsp; NSE • MCX • Equity<br>
  © 2026 All Rights Reserved &nbsp;|&nbsp; ⚠️ Trading involves risk.
</div>""", unsafe_allow_html=True)
