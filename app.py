import streamlit as st

# એપનું સેટિંગ
st.set_page_config(page_title="Ramavat Algo", page_icon="📈", layout="centered")

# મુખ્ય હેડિંગ
st.title("🛢 Ramavat Algo Control Panel")

# --- સિક્યોરિટી લોક (Password System) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.subheader("🔐 સિક્યોરિટી લોગિન")
    password = st.text_input("સાહેબ, તમારો પર્સનલ પાસવર્ડ નાખો:", type="password")
    login_button = st.button("એપ ચાલુ કરો")
    
    # અહીં તમે તમારો મનપસંદ પાસવર્ડ બદલી શકો છો (અત્યારે '1234' રાખ્યો છે)
    if login_button:
        if password == "1234":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ ખોટો પાસવર્ડ! સરખો પાસવર્ડ નાખો સાહેબ.")
else:
    # --- પાસવર્ડ સાચો પડે પછી આ અસલી ડેશબોર્ડ દેખાશે ---
    st.success("🔓 લોગિન સફળ! વેલકમ સાહેબ.")
    
    st.divider()

    # લાઈવ ડેટાનું બોક્સ
    st.subheader("📊 આજનો લાઈવ પ્રોફિટ / લોસ")
    
    # અહીં આપણે ભવિષ્યમાં ગૂગલ શીટ કે બ્રોકર માંથી લાઈવ P&L લાવીશું
    st.metric(label="Total P&L (Testing Mode)", value="+₹ 2,500.00", delta="Live")

    st.divider()

    # બોટ કંટ્રોલ સ્વીચ
    st.subheader("🤖 Bot Control")
    bot_status = st.toggle("Volatility Scanner Bot ચાલુ કરો")

    if bot_status:
        st.success("🚀 બોટ બેકએન્ડમાં સિગ્નલ સ્કેન કરી રહ્યો છે...")
    else:
        st.error("🛑 બોટ અત્યારે બંધ છે.")
        
    # લોગઆઉટ બટન
    if st.button("લોગઆઉટ (Lock App)"):
        st.session_state["authenticated"] = False
        st.rerun()
