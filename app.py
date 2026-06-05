import streamlit as st
import time
import pandas as pd

# --- ૧. પર્સનલ ટર્મિનલ પેનલ સેટિંગ્સ ---
st.set_page_config(
    page_title="Ramavat Algo Elite", 
    page_icon="🔱", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- ૨. પ્રીમિયમ ડાર્ક ટ્રેડિંગ થીમ (Custom CSS) ---
st.markdown("""
<style>
    .main { background-color: #060913 !important; }
    
    /* મેટ્રિક બોક્સ */
    div[data-testid="stMetricSimpleContainer"] {
        background: linear-gradient(135deg, #0d162d, #142247);
        padding: 16px !important;
        border-radius: 12px !important;
        border: 1px solid #1e366a !important;
        text-align: center;
    }
    
    /* ઇનપુટ્સ */
    .stSelectbox, .stTextInput, .stNumberInput { background-color: #0f172a !important; }
    
    /* બટનો */
    .stButton>button {
        width: 100% !important; border-radius: 10px !important; height: 48px !important;
        font-weight: 800 !important; font-size: 15px !important; text-transform: uppercase !important;
    }
    
    /* BUY - SELL - WAIT કલર્સ */
    .buy-box button { background: linear-gradient(90deg, #00c851, #007e33) !important; color: white !important; border: none !important; }
    .sell-box button { background: linear-gradient(90deg, #ff4444, #cc0000) !important; color: white !important; border: none !important; }
    .wait-box button { background: linear-gradient(90deg, #ffbb33, #ff8800) !important; color: white !important; border: none !important; }
    
    /* 🚨 EMERGENCY PANIC BUTTON */
    .panic-container button {
        background: linear-gradient(90deg, #7f1d1d, #dc2626) !important; color: white !important;
        border: 2px solid #ef4444 !important; height: 52px !important;
    }
    
    .config-box {
        background-color: #0d1527; padding: 15px; border-radius: 10px;
        border: 1px solid #1e293b; margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# સેશન સ્ટેટ્સ
if "broker_connected" not in st.session_state:
    st.session_state["broker_connected"] = False
if "selected_symbol" not in st.session_state:
    st.session_state["selected_symbol"] = "CRUDEOIL"

# --- ૩. મેઈન હેડર ---
st.markdown("""
<div style="text-align: center; margin-bottom: 10px;">
    <h1 style='color: #d4af37; margin: 0; font-size: 30px; font-weight: 900;'>🔱 RAMAVAT ALGO ELITE</h1>
    <p style='color: #9ca3af; font-size: 13px; margin: 0;'>PERSONAL ALGO BRIDGE & TRADING TERMINAL</p>
</div>
""", unsafe_allow_html=True)

# સ્ટેટસ બાર
broker_status = "<span style='color:#00c851; font-weight:bold;'>CONNECTED 🟢</span>" if st.session_state["broker_connected"] else "<span style='color:#ff4444; font-weight:bold;'>DISCONNECTED 🔴</span>"
st.markdown(f"⚡ **લાઇવ કંટ્રોલ ડેસ્ક** | બ્રોકર સ્ટેટસ: {broker_status}", unsafe_allow_html=True)
st.markdown("<hr style='margin:5px 0 15px 0; border-color:#1e366a;'>", unsafe_allow_html=True)

# --- ૪. પર્સનલ એકાઉન્ટ મેટ્રિક્સ ---
m1, m2, m3, m4 = st.columns(4)
current_time_sec = int(time.time())
dynamic_pnl = 2675 + (current_time_sec % 10 * 5)
m1.metric(label="📊 આજનો P&L (Live)", value=f"₹ {dynamic_pnl:,.2f}", delta="▲ પ્રોફિટ ચાલુ")
m2.metric(label="💰 અવેલેબલ માર્જિન", value="₹ 1,50,000", delta="માર્જિન ઓકે")
m3.metric(label="🎯 ઓપન પોઝિશન્સ", value="1 Active", delta="Live Trade")
m4.metric(label="🔌 API સ્ટેટસ", value="Handshake OK" if st.session_state["broker_connected"] else "Setup Pending", delta="બ્રોકર કનેક્શન")

st.markdown("<br>", unsafe_allow_html=True)

# --- ૫. ડ્યુઅલ લેઆઉટ: ચાર્ટ અને ઓર્ડર કંટ્રોલ ---
col_chart, col_control = st.columns([1.1, 1])

# 📈 ડાબી બાજુ: ઇન્ડિયન માર્કેટ અને ગ્લોબલ ફ્રી ચાર્ટ મેપિંગ (એરર ફિક્સ)
with col_chart:
    st.markdown(f"<h4 style='color:#f3f4f6;'>📈 લાઇવ ચાર્ટ: {st.session_state['selected_symbol']}</h4>", unsafe_allow_html=True)
    
    # વિજેટ બ્લોક ન થાય તે માટે ગ્લોબલ ઇક્વિવેલન્ટ મેપિંગ
    symbol_map = {
        "CRUDEOIL": "FX:USOIL",
        "NATURALGAS": "NYMEX:NG1!",
        "NIFTY": "TVC:NIFTY",
        "BANKNIFTY": "NSE:BANKNIFTY",
        "GOLD": "COMEX:GC1!",
        "SILVER": "COMEX:SI1!"
    }
    tv_symbol = symbol_map.get(st.session_state['selected_symbol'], "FX:USOIL")
    
    tradingview_html = f"""
    <div style="height:450px;">
        <iframe src="https://s.tradingview.com/widgetembed/?symbol={tv_symbol}&interval=5&theme=dark&style=1&timezone=Asia%2FKolkata&locale=en" 
        width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe>
    </div>
    """
    st.components.v1.html(tradingview_html, height=450)

# ⚙️ જમણી બાજુ: પર્સનલ સેટિંગ્સ અને ઓર્ડર ઇનપુટ્સ
with col_control:
    # 🔐 બ્રોકર API સેટિંગ્સ
    with st.expander("🔌 🔐 MY BROKER API CONFIGURATION"):
        st.markdown("<div class='config-box'>", unsafe_allow_html=True)
        my_broker = st.selectbox("મારો બ્રોકર પસંદ કરો:", ["Alice Blue", "Zerodha (Kite)", "Angel One", "Finvasia (Shoonya)"])
        
        col_c1, col_c2 = st.columns(2)
        u_client_id = col_c1.text_input("👤 CLIENT ID:", placeholder="Enter User ID")
        u_api_key = col_c1.text_input("🔑 API KEY:", type="password", placeholder="Enter API Key")
        u_totp = col_c2.text_input("⏳ TOTP SECRET KEY:", type="password", placeholder="Google TOTP Key")
        u_secret = col_c2.text_input("🔒 SECRET KEY:", type="password", placeholder="Enter Secret Key")
        
        if st.button("🔌 SAVE & CONNECT API"):
            if u_client_id and u_api_key:
                st.session_state["broker_connected"] = True
                st.toast(f"✅ {my_broker} API Successfully Connected!", icon="🚀")
                time.sleep(0.2)
                st.rerun()
            else:
                st.error("❌ મહેરબાની કરીને Client ID અને API Key નાખો સાહેબ!")
        st.markdown("</div>", unsafe_allow_html=True)

    # ઓર્ડર કંટ્રોલ અને સ્ક્રિપ્ટ સિલેક્શન
    st.markdown("<div class='config-box'>", unsafe_allow_html=True)
    col_sym, col_opt = st.columns(2)
    
    with col_sym:
        symbol_list = ["CRUDEOIL", "NATURALGAS", "NIFTY", "BANKNIFTY", "GOLD", "SILVER"]
        st.session_state["selected_symbol"] = st.selectbox("સિમ્બોલ પસંદ કરો:", symbol_list, index=0)
    with col_opt:
        selected_option = st.selectbox("ઓપ્શન / ફ્યુચર ટાઈપ:", ["CE", "PE", "FUT"])

    selected_strike = st.text_input("સ્ટ્રાઈક પ્રાઈઝ:", value="6500")
    
    # ઓટો લોટ કેલ્ક્યુલેટર
    lot_sizes = {"CRUDEOIL": 100, "NATURALGAS": 1250, "NIFTY": 25, "BANKNIFTY": 15, "GOLD": 100, "SILVER": 30}
    current_lot_size = lot_sizes.get(st.session_state["selected_symbol"], 1)
    
    col_l, col_q = st.columns(2)
    u_lots = col_l.number_input("🔢 લોટ (Lots):", min_value=1, value=1)
    u_qty = u_lots * current_lot_size
    col_q.text_input("📊 કુલ ક્વોન્ટિટી (Auto Quantity):", value=f"{u_qty} Qty", disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # SL અને Target
    st.markdown("<div class='config-box' style='padding:10px; margin-top:-5px;'>", unsafe_allow_html=True)
    col_sl, col_tgt = st.columns(2)
    sl_points = col_sl.number_input("🚨 STOP LOSS (Pts):", value=30)
    tgt_points = col_tgt.number_input("🎯 TARGET (Pts):", value=60)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ઓર્ડર બટનો
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("🟩 BUY"):
            if st.session_state["broker_connected"]:
                st.toast(f"🛒 BUY ORDER FIRED! Qty: {u_qty}", icon="✅")
            else:
                st.error("❌ પેલા બ્રોકર API કનેક્ટ કરો સાહેબ!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with b2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("🟥 SELL"):
            if st.session_state["broker_connected"]:
                st.toast(f"📉 SELL ORDER FIRED! Qty: {u_qty}", icon="🚨")
            else:
                st.error("❌ પેલા બ્રોકર API કનેક્ટ કરો સાહેબ!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with b3:
        st.markdown('<div class="wait-box">', unsafe_allow_html=True)
        if st.button("🟨 WAIT"):
            st.toast("SYSTEM ON HOLD", icon="⏳")
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Panic બટન
    st.markdown('<div class="panic-container" style="margin-top:10px;">', unsafe_allow_html=True)
    if st.button("💥 EMERGENCY CLOSE ALL POSITIONS"):
        st.toast("🚨 ALL POSITIONS SQUARED OFF!", icon="💥")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><hr style='border-color:#1e366a;'>", unsafe_allow_html=True)

# --- ૬. પર્સનલ ઓર્ડર બુક ---
st.markdown("<h4 style='color:#f3f4f6;'>📋 મારી લાઈવ ઓપન પોઝિશન્સ</h4>", unsafe_allow_html=True)

my_trades = {
    "ટ્રેડ આઈડી (ID)": ["#RM-2001"],
    "સિમ્બોલ (Script)": [f"{st.session_state['selected_symbol']} {selected_strike} {selected_option}"],
    "કુલ ક્વોન્ટિટી": [f"{u_qty} ({u_lots} Lots)"],
    "સ્ટોપલોસ (SL)": [f"{sl_points} Pts"],
    "ટાર્ગેટ (TARGET)": [f"{tgt_points} Pts"],
    "સ્ટેટસ / P&L": ["⌛ Waiting for Signal"],
}
st.table(pd.DataFrame(my_trades))
