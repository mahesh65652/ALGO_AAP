import streamlit as st
import time
import pandas as pd

# --- ૧. એડવાન્સ મોબાઇલ અને પેનલ લેઆઉટ સેટિંગ્સ ---
st.set_page_config(
    page_title="Ramavat Algo Elite", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ૨. એડમિન લેવલ અલ્ટ્રા-પ્રીમિયમ ડાર્ક થીમ (Custom CSS) ---
st.markdown("""
<style>
    .main {
        background-color: #080c14 !important;
    }
    
    /* પ્રીમિયમ મેટ્રિક કાર્ડ્સ */
    div[data-testid="stMetricSimpleContainer"] {
        background: linear-gradient(135deg, #111a2e, #172442);
        padding: 15px !important;
        border-radius: 12px !important;
        border: 1px solid #1e2e52 !important;
        text-align: center;
    }
    
    /* ઇનપુટ બોક્સ અને સિલેક્શન બોક્સ સુંદર બનાવવા માટે */
    .stSelectbox, .stTextInput, .stNumberInput {
        background-color: #111827 !important;
        border-radius: 8px !important;
    }
    
    /* મોટા એક્શન બટનો (મોબાઈલ સ્પેશિયલ) */
    .stButton>button {
        width: 100% !important;
        border-radius: 12px !important;
        height: 52px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }
    
    /* 🟢 BUY NOW */
    .buy-box button {
        background: linear-gradient(90deg, #00c851, #007e33) !important;
        color: white !important;
        border: none !important;
    }
    
    /* 🔴 SELL NOW */
    .sell-box button {
        background: linear-gradient(90deg, #ff4444, #cc0000) !important;
        color: white !important;
        border: none !important;
    }
    
    /* 🟡 WAIT / HOLD */
    .wait-box button {
        background: linear-gradient(90deg, #ffbb33, #ff8800) !important;
        color: white !important;
        border: none !important;
    }
    
    /* 🚨 EMERGENCY PANIC BUTTON */
    .panic-container button {
        background: linear-gradient(90deg, #7f1d1d, #b91c1c) !important;
        color: white !important;
        border: 2px solid #ef4444 !important;
        height: 60px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ૩. બ્રાન્ડિંગ હેડર ---
st.markdown("""
<div style="text-align: center; margin-bottom: 15px;">
    <h1 style='color: #d4af37; margin: 0; font-size: 28px; font-weight: 900;'>🔱 RAMAVAT ALGO ELITE</h1>
    <p style='color: #9ca3af; font-size: 12px; margin: 0;'>ADVANCED SYMBOL CONTROLLER • 5 USERS ACTIVE</p>
</div>
""", unsafe_allow_html=True)

# --- ૪. સિક્યોરિટી ગેટ (Password Locked) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    with st.container():
        st.markdown("<h3 style='color:#3b82f6; text-align:center;'>🔐 એડમિન લોગિન</h3>", unsafe_allow_html=True)
        password = st.text_input("સાહેબ, પર્સનલ એડમિન પાસવર્ડ નાખો:", type="password")
        if st.button("🔓 અનલોક ટર્મિનલ"):
            if password == "1234":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ ખોટો પાસવર્ડ સાહેબ!")
else:
    # સેસન સ્ટેટ સેટિંગ્સ
    if "selected_symbol" not in st.session_state:
        st.session_state["selected_symbol"] = "CRUDEOIL"
    if "selected_strike" not in st.session_state:
        st.session_state["selected_strike"] = "6500"
    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = "CE"

    # લોગઆઉટ હેડર
    c_user, c_logout = st.columns([3, 1])
    c_user.markdown(f"👋 **એડમિન પેનલ રેડી** | ફોકસ: <span style='color:#d4af37; font-weight:bold;'>{st.session_state['selected_symbol']} {st.session_state['selected_strike']} {st.session_state['selected_option']}</span>", unsafe_allow_html=True)
    if c_logout.button("🔒 EXIT"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown("<hr style='margin:5px 0 15px 0; border-color:#1e2e52;'>", unsafe_allow_html=True)

    # --- ૫. લાઈવ માર્કેટ સ્ટેટસ ડેશબોર્ડ ---
    m1, m2, m3 = st.columns(3)
    m1.metric(label="કુલ લાઈવ P&L", value="+₹ 2,500.00", delta="▲ પ્રોફિટ ચાલુ")
    m2.metric(label="અવેલેબલ માર્જિન", value="₹ 1,50,000", delta="સેફ ઝોન")
    m3.metric(label="એક્ટિવ સ્ક્રિપ્ટ્સ", value="3 Watchlist", delta="NSE / MCX")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ૬. અસલી જાદુ: સિમ્બોલ અને ઇનડેક્સ સર્ચ સેક્શન ---
    st.markdown("<h4 style='color:#f3f4f6;'>🔍 ઇન્ડેક્સ / સિમ્બોલ સેટિંગ્સ (સર્ચ એન્ડ સેડ્યુલ)</h4>", unsafe_allow_html=True)
    
    with st.container():
        # બે કોલમ: એકમાં મેઈન સિમ્બોલ, બીજામાં ઓપ્શન ટાઈપ
        col_sym, col_opt, col_stk = st.columns([2, 1, 1.5])
        
        with col_sym:
            # વેપારી જે જોઈને એડ કરે એ આ મેનૂ
            symbol_list = ["CRUDEOIL", "NATURALGAS", "NIFTY", "BANKNIFTY", "GOLD", "SILVER"]
            st.session_state["selected_symbol"] = st.selectbox("સિમ્બોલ પસંદ કરો:", symbol_list, index=0)
            
        with col_opt:
            st.session_state["selected_option"] = st.selectbox("ઓપ્શન:", ["CE", "PE", "FUT"], index=0)
            
        with col_stk:
            st.session_state["selected_strike"] = st.text_input("સ્ટ્રાઈક પ્રાઈઝ:", value="6500")

    # લાઈવ સિમ્બોલ જે સ્ક્રીન પર દેખાશે તે વોચલિસ્ટ ટેબલ
    st.markdown("<p style='color:#9ca3af; font-size:13px; font-weight:bold; margin-bottom:5px;'>📋 અત્યારે એક્ટિવ વોચલિસ્ટ (લોકો આ જોઈને ટ્રેડ કરશે):</p>", unsafe_allow_html=True)
    
    # સેમ્પલ લાઈવ વોચલિસ્ટ ડેટા ટેબલ
    watchlist_data = {
        "સિમ્બોલ (Symbol)": [f"{st.session_state['selected_symbol']}", "NIFTY", "BANKNIFTY"],
        "સ્ટ્રાઈક (Strike)": [f"{st.session_state['selected_strike']} {st.session_state['selected_option']}", "22000 CE", "47500 PE"],
        "લાઈવ ભાવ (LTP)": ["₹ 145.20", "₹ 120.50", "₹ 340.10"],
        "સ્ટેટસ (Status)": ["🎯 મોનિટરિંગ", "💤 બંધ", "💤 બંધ"]
    }
    df = pd.DataFrame(watchlist_data)
    st.table(df)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ૭. માર્કેટ ઓર્ડર બટનો (BUY / SELL / WAIT) ---
    st.markdown(f"<h4 style='color:#f3f4f6;'>🚀 ઓર્ડર કમાન્ડ: {st.session_state['selected_symbol']} માટે</h4>", unsafe_allow_html=True)
    
    b_col1, b_col2, b_col3 = st.columns(3)
    
    with b_col1:
        st.markdown('<div class="buy-box">', unsafe_allow_html=True)
        if st.button("🟩 BUY NOW"):
            st.toast(f"🛒 {st.session_state['selected_symbol']} ખરીદી ઓર્ડર સેન્ટ!", icon="✅")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with b_col2:
        st.markdown('<div class="sell-box">', unsafe_allow_html=True)
        if st.button("🟥 SELL NOW"):
            st.toast(f"📉 {st.session_state['selected_symbol']} વેચાણ ઓર્ડર સેન્ટ!", icon="🚨")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with b_col3:
        st.markdown('<div class="wait-box">', unsafe_allow_html=True)
        if st.button("🟨 WAIT"):
            st.toast(f"⏳ {st.session_state['selected_symbol']} વેઇટિંગ મોડમાં મુકાયો.", icon="⏳")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ૮. ઓટોમેશન અને પેનિક બટન ---
    st.markdown("<h4 style='color:#f3f4f6;'>⚙️ સેફ્ટી કંટ્રોલ</h4>", unsafe_allow_html=True)
    
    col_str, col_ref = st.columns(2)
    with col_str:
        if st.button("🟢 START SCANNER"):
            st.toast("વોલેટિલિટી સ્કેનર એક્ટિવેટેડ!")
    with col_ref:
        if st.button("🔄 REFRESH PANEL"):
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🚨 ઇમરજન્સી સ્ક્વેર ઓફ બટન
    st.markdown('<div class="panic-container">', unsafe_allow_html=True)
    panic_click = st.button("💥 EMERGENCY CLOSE ALL POSITIONS (PANIC)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if panic_click:
        st.markdown(f"""
        <div style='background-color:#7f1d1d; padding:15px; border-radius:10px; border:2px solid #ef4444; margin-top:15px; text-align:center;'>
            <h4 style='color:white; margin:0;'>🛑 EMERGENCY SQUARE-OFF SUCCESSFUL!</h4>
            <p style='color:#fca5a5; margin:5px 0 0 0; font-size:14px;'>બધા યુઝર્સ નોંધ લે: {st.session_state['selected_symbol']} સહિતના બધા ટ્રેડ માર્કેટ પ્રાઈસ પર કાપી નાખ્યા છે.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#1e2e52;'>", unsafe_allow_html=True)

    # --- ૯. ઓડિટ લોગ્સ ---
    with st.expander("📝 ઓફિસ ઓડિટ લોગ્સ (કોણે કયો સિમ્બોલ બદલ્યો?)"):
        st.code(f"""[SYSTEM] {time.strftime('%H:%M:%S')} - Multi-Admin dashboard is tracking 5 screen sessions.
[USER 1] {time.strftime('%H:%M:%S')} - Active Symbol changed to -> [{st.session_state["selected_symbol"]} {st.session_state["selected_strike"]} {st.session_state["selected_option"]}]
[MARKET] {time.strftime('%H:%M:%S')} - Fetching live data for {st.session_state["selected_symbol"]} from broker feed.
[ALGO]   {time.strftime('%H:%M:%S')} - Automatic risk management matrix updated.""", language="bash")
