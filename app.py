import streamlit as st
import time

# --- ૧. પેજ કોન્ફિગરેશન (મોબાઈલ અને ડાર્ક થીમ માટે ઓપ્ટિમાઈઝ્ડ) ---
st.set_page_config(
    page_title="Ramavat Algo", 
    page_icon="📈", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ૨. કસ્ટમ CSS સ્ટાઈલિંગ (બટનો અને કન્ટેનર્સ સજાવવા માટે) ---
st.markdown("""
<style>
    /* એપનું બેકગ્રાઉન્ડ અને ફોન્ટ સેટિંગ્સ */
    .reportview-container {
        background: #0e1117;
    }
    
    /* મેટ્રિક્સ કાર્ડ્સને સુંદર લુક આપવા માટે */
    div[data-testid="stMetricSimpleContainer"] {
        background-color: #1f293d;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #2d3748;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* સામાન્ય બટન સ્ટાઈલ */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 48px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    /* લીલું બટન (Start All Systems) */
    div[data-testid="stHorizontalBlock"] div:nth-of-type(1) button {
        background-color: #059669 !important;
        color: white !important;
        border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div:nth-of-type(1) button:hover {
        background-color: #047857 !important;
    }

    /* ઇમરજન્સી લાલ બટન (Panic Button) */
    .panic-box button {
        background-color: #dc2626 !important;
        color: white !important;
        border: none !important;
        font-size: 16px !important;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3) !important;
    }
    
    /* સ્ટેટસ બોક્સ */
    .status-card {
        background-color: #111827;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #3b82f6;
        margin: 10px 0px;
    }
</style>
""", unsafe_allow_html=True)

# મુખ્ય ટાઈટલ
st.title("🛢 Ramavat Algo Control Panel")
st.caption("🔒 Advanced Algo Trading Terminal • Mobile Edition")

# --- ૩. સિક્યોરિટી લોગિન સિસ્ટમ ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("---")
    with st.container():
        st.subheader("🔐 સિક્યોરિટી લોગિન")
        password = st.text_input("સાહેબ, તમારો પર્સનલ પાસવર્ડ નાખો:", type="password")
        login_button = st.button("🔓 એપ્લિકેશન અનલોક કરો")
        
        if login_button:
            if password == "1234":  # ડિફોલ્ટ પાસવર્ડ
                st.session_state["authenticated"] = True
                st.toast("લોગિન સફળ થયું છે સાહેબ!", icon="✅")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ ખોટો પાસવર્ડ! સરખો પાસવર્ડ નાખો સાહેબ.")
else:
    # --- ૪. અસલી ડેશબોર્ડ (લોગિન થયા પછી) ---
    
    # ટોપ હેડર રો (User Info & Logout)
    col_user, col_logout = st.columns([3, 1.2])
    col_user.markdown("👋 **વેલકમ સાહેબ!** તમારી સિસ્ટમ લાઈવ છે.")
    if col_logout.button("🔒 લોગઆઉટ"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown("---")

    # --- ૫. ટ્રેડિંગ ડેશબોર્ડ મેટ્રિક્સ (Metrics) ---
    st.subheader("📊 આજનું માર્કેટ સ્ટેટસ")
    
    # મોબાઈલ વ્યુ માટે ૩ અલગ અલગ કોલમ
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="આજનો P&L", value="+₹ 2,500.00", delta="▲ લાભ (Green)", delta_color="normal")
    with m2:
        st.metric(label="કુલ કેપિટલ", value="₹ 1,50,000", delta="Margin OK", delta_color="off")
    with m3:
        st.metric(label="એક્ટિવ ટ્રેડ", value="2 Positions", delta="Running", delta_color="inverse")

    st.markdown("---")

    # --- ૬. બોટ કંટ્રોલ સેક્શન (Toggles & Buttons) ---
    st.subheader("⚙️ અલ્ગો સિસ્ટમ કંટ્રોલ")
    
    # વોલેટિલિટી બોટ સ્વિચ
    bot_switch = st.toggle("🤖 Volatility Scanner Bot (Start/Stop)", value=False)
    
    if bot_switch:
        st.markdown("""
        <div class="status-card">
            <h5 style='color:#3b82f6; margin:0;'>🚀 બોટ સ્ટેટસ: એક્ટિવ</h5>
            <p style='color:#9ca3af; margin:5px 0 0 0; font-size:14px;'>બેકએન્ડમાં NSE/MCX ડેટા સ્કેનિંગ ચાલુ છે...</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-card" style="border-left-color: #6b7280;">
            <h5 style='color:#9ca3af; margin:0;'>💤 બોટ સ્ટેટસ: સ્લીપ મોડ</h5>
            <p style='color:#6b7280; margin:5px 0 0 0; font-size:14px;'>બોટ અત્યારે બંધ છે. સિગ્નલ સ્કેનિંગ અટકેલું છે.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("") # સ્પેસ માટે

    # એક્શન બટન્સ (Start & Refresh)
    col_start, col_refresh = st.columns(2)
    with col_start:
        if st.button("🟢 Start All Systems"):
            st.toast("બધા ઓટોમેશન ટાસ્ક ચાલુ થઈ ગયા!", icon="🚀")
            
    with col_refresh:
        if st.button("🔄 Refresh Data"):
            st.toast("ડેટા રિફ્રેશ થઈ રહ્યો છે...", icon="🔄")
            time.sleep(0.3)
            st.rerun()

    st.write("")
    
    # 🚨 ઇમરજન્સી લાલ પેનિક બટન
    st.markdown('<div class="panic-box">', unsafe_allow_html=True)
    panic_click = st.button("🛑 EMERGENCY CLOSE ALL POSITIONS (PANIC BUTTON)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if panic_click:
        st.markdown("""
        <div style='background-color:#ffe6e6; padding:15px; border-radius:8px; border:1px solid #ff9999; margin-top:10px;'>
            <h4 style='color:#cc0000; margin:0;'>🚨 EMERGENCY SIGNAL SENT!</h4>
            <p style='color:#111; margin:5px 0 0 0; font-weight:bold;'>બધી ચાલુ ઓપન પોઝિશન્સ માર્કેટ પ્રાઇસ પર સ્ક્વેર ઓફ (Square Off) કરી દીધી છે!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- ૭. ઇન્ટરેક્ટિવ સિસ્ટમ લોગ્સ (System Logs) ---
    with st.expander("📝 સિસ્ટમ લાઈવ લોગ્સ (System Logs) જુઓ"):
        st.markdown("⬇️ *બેકએન્ડમાં ચાલતી પ્રોસેસની વિગત:*")
        log_data = f"""[INFO] {time.strftime('%H:%M:%S')} - Ramavat Algo Engine v2.0 Initialization Successful.
[INFO] {time.strftime('%H:%M:%S')} - Connecting to Broker API... Connected.
[SUCCESS] {time.strftime('%H:%M:%S')} - Fetching Margin Details: Margin Available ₹1,50,000.
[INFO] {time.strftime('%H:%M:%S')} - Volatility Scanner Bot started watching NIFTY / CRUDEOIL.
[SUCCESS] {time.strftime('%H:%M:%S')} - Sample Target Achieved! +₹ 2,500.00"""
        st.code(log_data, language="bash")
