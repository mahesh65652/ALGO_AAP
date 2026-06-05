import streamlit as st

st.set_page_config(page_title="Ramavat Algo", page_icon="📈", layout="centered")

st.title("🛢 Ramavat Algo Control Panel")

# લોગિન સિસ્ટમ
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    password = st.text_input("પાસવર્ડ નાખો:", type="password")
    if st.button("એપ અનલોક કરો"):
        if password == "1234": # અહીં તમારો પાસવર્ડ બદલી શકો છો
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("ખોટો પાસવર્ડ!")
else:
    st.success("લોગિન સફળ!")
    
    # 1. લાઈવ ડેશબોર્ડ
    st.subheader("📊 ટ્રેડિંગ ડેશબોર્ડ")
    col1, col2 = st.columns(2)
    col1.metric("આજનો પ્રોફિટ", "₹ 2,500", "+1.2%")
    col2.metric("એક્ટિવ ટ્રેડ્સ", "2", "Running")

    st.divider()

    # 2. કંટ્રોલ બટનો
    st.subheader("⚙️ કંટ્રોલ પેનલ")
    
    if st.button("🚀 બોટ સ્ટાર્ટ કરો"):
        st.success("બોટ એક્ટિવ થઈ ગયો છે!")
    
    if st.button("🛑 બધા ટ્રેડ બંધ કરો (Emergency)"):
        st.warning("ચેતવણી: બધા ઓપન પોઝિશન ક્લોઝ કરી રહ્યા છીએ...")
        
    if st.button("🔄 ડેટા રિફ્રેશ કરો"):
        st.rerun()

    st.divider()

    # 3. મેનુ સેટિંગ્સ
    if st.checkbox("બોટ સેટિંગ્સ બતાવો"):
        st.text_input("સ્કેનિંગ સમયગાળો (સેકન્ડ)", "5")
        st.slider("રિસ્ક લેવલ", 1, 10, 5)

    if st.button("લોગઆઉટ"):
        st.session_state["authenticated"] = False
        st.rerun()
