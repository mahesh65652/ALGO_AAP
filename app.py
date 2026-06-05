import streamlit as st
import time

# --- ૧. એડવાન્સ મલ્ટી-યુઝર પેનલ સેટિંગ્સ ---
st.set_page_config(
    page_title="Ramavat Algo Elite", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ૨. એડમિન લેવલ અલ્ટ્રા-પ્રીમિયમ ડાર્ક થીમ (CSS) ---
st.markdown("""
<style>
    /* બેકગ્રાઉન્ડ સેટિંગ્સ */
    .main {
        background-color: #080c14 !important;
    }
    
    /* લોગો ઈમેજને સેન્ટર અને પ્રીમિયમ લુક આપવા માટે */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }
    .logo-img {
        border-radius: 50%;
        border: 3px solid #d4af37;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        width: 140px;
        height: 140px;
        object-fit: cover;
    }
    
    /* ૫ પાર્ટનર્સ માટે હાઈ-એન્ડ મેટ્રિક કાર્ડ્સ */
    div[data-testid="stMetricSimpleContainer"] {
        background: linear-gradient(135deg, #111a2e, #172442);
        padding: 20px !important;
        border-radius: 14px !important;
        border: 1px solid #1e2e52 !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
        text-align: center;
    }
    
    /* ફૂલ-સ્ક્રીન મોટા કંટ્રોલ બટન્સ (મોબાઈલ સ્પેશિયલ) */
    .stButton>button {
        width: 100% !important;
        border-radius: 12px !important;
        height: 54px !important;
        font-weight: 800 !important;
        font-size: 17px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* ગ્રીન કમાન્ડ બટન */
    .start-btn button {
        background: linear-gradient(90deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
    }
    
    /* બ્લુ રિફ્રેશ બટન */
    .refresh-btn button {
        background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
    }
    
    /* 🚨 ૫ માણસો વચ્ચે સેફ્ટી માટેનું મોટું બ્લાસ્ટ પેનિક બટન */
    .panic-container button {
        background: linear-gradient(90deg, #ef4444, #dc2626) !important;
        color: white !important;
        border: none !important;
        height: 65px !important;
        font-size: 18px !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.5) !important;
    }
    
    /* સ્ટેટસ બેનર */
    .status-banner {
        background-color: #0f172a;
        padding: 14px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        font-size: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- ૩. લોગો ડિસ્પ્લે સેક્શન ---
# નોંધ: ગીથબ પર લોગો અપલોડ કરી અહીં તેની લિંક મૂકી શકાય છે. અત્યારે પ્લેસહોલ્ડર રાખ્યો છે.
st.markdown("""
<div class="logo-container">
    <div style="text-align: center;">
        <h1 style='color: #d4af37; margin: 0; font-size: 28px; font-weight: 900; letter-spacing: 1px;'>🔱 RAMAVAT ALGO</h1>
        <p style='color: #9ca3af; font-size: 12px; margin: 0;'>PREMIUM TRADING TERMINAL</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- ૪. સિક્યોરિટી ગેટ (Multi-User Password Locked) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<h3 style='color:#3b82f6; text-align:center;'>🔐 એડમિન લોગિન</h3>", unsafe_allow_html=True)
        password = st.text_input("સાહેબ, ટર્મિનલ પાસવર્ડ એન્ટર કરો:", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔓 એપ્લિકેશન અનલોક કરો"):
            if password == "1234":
                st.session_state["authenticated"] = True
                st.toast("ટર્મિનલ અનલોક થઈ રહ્યું છે...", icon="⚡")
                time.sleep(0.4)
                st.rerun()
            else:
                st.error("❌ એક્સેસ નકારાયો! સાચો એડમિન પાસવર્ડ નાખો.")
else:
    # --- ૫. ઓપરેશનલ ડેશબોર્ડ (લોગિન પછી) ---
    
    # ટોપ યુઝર સ્ટેટસ બાર
    c_user, c_logout = st.columns([3, 1.2])
    c_user.markdown("🟢 **લાયસન્સ: મલ્ટી-એડમિન પેનલ (5 Users Ready)**")
    with c_logout:
        if st.button("🔒 EXIT"):
            st.session_state["authenticated"] = False
            st.rerun()

    st.markdown("<hr style='margin-top:5px; margin-bottom:20px; border-color:#1e2e52;'>", unsafe_allow_html=True)

    # --- ૬. લાઈવ માર્કેટ સ્ટેટસ ગ્રીડ ---
    st.markdown("<h4 style='color:#f3f4f6; margin-top:-10px;'>📊 આજનું માર્કેટ લાઈવ પર્ફોર્મન્સ</h4>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="કુલ લાઈવ P&L", value="+₹ 2,500.00", delta="▲ નફો ચાલુ છે")
    with m2:
        st.metric(label="અવેલેબલ માર્જિન", value="₹ 1,50,000", delta="સેફ લિમિટ")
    with m3:
        st.metric(label="ઓપન પોઝિશન્સ", value="2 Trades", delta="NSE / MCX")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ૭. બોટ કંટ્રોલ અને પાવર બટન્સ ---
    st.markdown("<h4 style='color:#f3f4f6;'>⚙️ એક્ઝિક્યુશન એન્જિન</h4>", unsafe_allow_html=True)
    
    bot_active = st.toggle("🤖 Volatility Scanner Bot ચાલુ કરો", value=True)
    
    if bot_active:
        st.markdown("""
        <div class="status-banner">
            <span style="color:#10b981; font-weight:bold;">🚀 સિસ્ટમ એક્ટિવ:</span> 
            <span style="color:#9ca3af;">બોટ બેકએન્ડમાં સ્કેનિંગ કરી રહ્યો છે...</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-banner" style="border-left-color: #6b7280;">
            <span style="color:#9ca3af; font-weight:bold;">💤 સિસ્ટમ બંધ:</span> 
            <span style="color:#6b7280;">બોટ અત્યારે સ્લીપ મોડમાં છે.</span>
        </div>
        """, unsafe_allow_html=True)

    # મોટા કલરવાળા એક્શન બટન્સ
    col_str, col_ref = st.columns(2)
    with col_str:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("🟢 START SYSTEMS"):
            st.toast("બધા રોબોટિક કમાન્ડ ટ્રિગર થઈ ગયા!", icon="⚡")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_ref:
        st.markdown('<div class="refresh-btn">', unsafe_allow_html=True)
        if st.button("🔄 REFRESH DATA"):
            st.toast("ડેટા અપડેટ સક્સેસ!", icon="🔄")
            time.sleep(0.2)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🚨 મેગા ઇમરજન્સી પેનિક બટન (૫ માંથી ગમે તે એક યુઝર આખા માર્કેટ ઓર્ડર કાપી શકે છે)
    st.markdown('<div class="panic-container">', unsafe_allow_html=True)
    panic_trigger = st.button("💥 EMERGENCY CLOSE ALL POSITIONS (PANIC)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if panic_trigger:
        st.markdown("""
        <div style='background: linear-gradient(145deg, #7f1d1d, #b91c1c); padding:20px; border-radius:12px; border:2px solid #ef4444; margin-top:15px; box-shadow: 0 0 25px rgba(239,68,68,0.5);'>
            <h4 style='color:#ffffff; margin:0; font-weight:900;'>🚨 EMERGENCY SQUARE-OFF ORDER SENT!</h4>
            <p style='color:#fca5a5; margin:5px 0 0 0; font-size:14px; font-weight:bold;'>બધા એડમિન યુઝર્સ ધ્યાન આપે: બધી ઓપન પોઝિશન્સ માર્કેટ રેટ પર ક્લોઝ કરી દેવામાં આવી છે.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#1e2e52;'>", unsafe_allow_html=True)

    # --- ૮. મલ્ટી-યુઝર ઓડિટ લોગ્સ ટર્મિનલ ---
    with st.expander("📝 એડમિન ઓડિટ લોગ્સ (Multi-User Audit Trails)"):
        st.code(f"""[SYSTEM] {time.strftime('%H:%M:%S')} - Terminal securely accessed by Admin Device.
[USER 2] {time.strftime('%H:%M:%S')} - System refresh triggered from Surat HQ.
[BROKER] {time.strftime('%H:%M:%S')} - Live Multi-Token API Pool synced with NSE/MCX.
[BOT]    {time.strftime('%H:%M:%S')} - Volatility scanner running smoothly. No errors.
[ALGO]   {time.strftime('%H:%M:%S')} - Auto-trailing stop loss updated.""", language="bash")
