import streamlit as st

# એપનું સેટિંગ
st.set_page_config(page_title="Ramavat Algo", page_icon="📈", layout="centered")

# મુખ્ય હેડિંગ
st.title("🛢 Ramavat Algo Control Panel")
st.write("સાહેબ, આ તમારી પર્સનલ અલ્ગો ટ્રેડિંગ એપ્લિકેશન છે (Testing Mode).")

st.divider()

# ટેસ્ટિંગ ડેટા
st.subheader("📊 આજનો લાઈવ પ્રોફિટ / લોસ (સેમ્પલ)")
st.metric(label="Total P&L", value="+₹ 2,500.00", delta="Live Market")

st.divider()

# બોટ ઓન/ઓફ સ્વીચ
st.subheader("🤖 Bot Status")
option = st.checkbox("Volatility Scanner Bot ચાલુ કરો")

if option:
    st.success("🚀 બોટ સક્રિય છે! બેકએન્ડ કનેક્ટ થઈ રહ્યું છે...")
else:
    st.info("🛑 બોટ અત્યારે બંધ છે.")
