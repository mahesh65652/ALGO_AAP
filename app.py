import streamlit as st
import streamlit.components.v1 as components

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="અરજી સ્ટેટસ અને ઈનવર્ડ ટ્રેકર",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 8px; font-weight: bold; background-color: #2563eb; color: white; }
    div[data-baseweb="select"] { background-color: #1e222d; border-radius: 8px; }
    .status-card {
        background-color: #1e222d;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2563eb;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────
st.title("🔍 સરકારી અરજી અને ઈનવર્ડ નંબર ટ્રેકર")
st.caption("ગાંધીનગર સચિવાલય, કલેક્ટર કચેરી (iORA) અને ઈન્ડિયા પોસ્ટ ટ્રેકિંગ સિસ્ટમ")
st.divider()

# ── SIDEBAR MENU ───────────────────────────────────────────────────
with st.sidebar:
    st.header("🌐 સત્તાવાર સરકારી પોર્ટેલ્સ")
    st.link_button("🏛️ e-Sarkar (સચિવાલય)", "https://esarkar.gujarat.gov.in/", use_container_width=True)
    st.link_button("🏢 iORA (કલેક્ટર/મહેસૂલ)", "https://iora.gujarat.gov.in/", use_container_width=True)
    st.link_button("📢 SWAGAT ઓનલાઈન", "https://swagat.gujarat.gov.in/", use_container_width=True)
    st.link_button("📮 ઇન્ડિયા પોસ્ટ ટ્રેકિંગ", "https://www.indiapost.gov.in/", use_container_width=True)

# ── MAIN TRACKING SECTION ─────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📌 ઈનવર્ડ નંબર અથવા રસીદ વિગત નાખો")
    
    portal_type = st.selectbox(
        "કઈ કચેરી/પોર્ટલની વિગત ટ્રેક કરવી છે?",
        options=[
            "1. e-Sarkar (ગાંધીનગર સચિવાલય / મહેસૂલ વિભાગ)",
            "2. iORA પોર્ટલ (મોરબી કલેક્ટર / જમીન કચેરી)",
            "3. SWAGAT / PG Portal (ઓનલાઈન ફરિયાદ સ્ટેટસ)",
            "4. સ્પીડ પોસ્ટ ટ્રેકિંગ (India Post)"
        ]
    )

    inward_num = st.text_input("ઈનવર્ડ નંબર / એપ્લિકેશન નંબર / ટ્રેકિંગ ID:", placeholder="દા.ત. EG639444752IN અથવા Inward No.")
    
    selected_year = st.selectbox("અરજીનું વર્ષ:", ["2026", "2025", "2024"])

    if st.button("🔎 ઓનલાઈન પોર્ટલ પર સ્ટેટસ જુઓ", use_container_width=True):
        if inward_num:
            st.success(f"નંબર **{inward_num}** માટે ટ્રેકિંગ પોર્ટલ નીચે રીડાયરેક્ટ થાય છે...")
        else:
            st.warning("કૃપા કરીને ઈનવર્ડ નંબર અથવા સ્પીડ પોસ્ટ ટ્રેકિંગ ID નાખો.")

with col2:
    st.subheader("🌐 પોર્ટલ ટ્રેકિંગ અને ડાયરેક્ટ એક્સેસ")
    
    if "1. e-Sarkar" in portal_type:
        st.markdown("""
        <div class="status-card">
            <h4>🏛️ e-Sarkar પોર્ટલ (ગાંધીનગર)</h4>
            <p>ગાંધીનગર સચિવાલયમાં આપેલી અરજીનો ઈનવર્ડ નંબર ટ્રેક કરવા માટે:</p>
            <ul>
                <li>નીચે આપેલા બટન પર ક્લિક કરી ડાયરેક્ટ પોર્ટલ પર જાઓ.</li>
                <li>ત્યાં <b>Inward Number</b> અને <b>Year (2026)</b> દાખલ કરો.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 e-Sarkar પર ટ્રેક કરો", "https://esarkar.gujarat.gov.in/trackApp.jsp", use_container_width=True)

    elif "2. iORA" in portal_type:
        st.markdown("""
        <div class="status-card">
            <h4>🏢 iORA પોર્ટલ (જિલ્લા કલેક્ટર કચેરી)</h4>
            <p>મોરબી કલેક્ટર કચેરી કે લેન્ડ ગ્રેબિંગ શાખાની અરજી ટ્રેક કરવા માટે:</p>
            <ul>
                <li>તમારો <b>Application / Inward No</b> નાખો.</li>
                <li>રજિસ્ટર્ડ મોબીલ નંબર પર આવેલ OTP દાખલ કરો.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 iORA પર ટ્રેક કરો", "https://iora.gujarat.gov.in/OnlineAppStatus.aspx", use_container_width=True)

    elif "3. SWAGAT" in portal_type:
        st.markdown("""
        <div class="status-card">
            <h4>📢 સ્વાગત (SWAGAT) / CPGRAMS પોર્ટલ</h4>
            <p>મુખ્યમંત્રીશ્રી ઓનલાઈન ફરિયાદ નિવારણ પોર્ટલ સ્ટેટસ:</p>
            <ul>
                <li>તમારો ઓનલાઈન ફરિયાદ નંબર નાખીને સીધું સ્ટેટસ જુઓ.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 SWAGAT પર ટ્રેક કરો", "https://swagat.gujarat.gov.in/", use_container_width=True)

    else:
        st.markdown("""
        <div class="status-card">
            <h4>📮 India Post ટ્રેકિંગ</h4>
            <p>તમારી સ્પીડ પોસ્ટ ટપાલ કચેરીમાં પહોંચી છે કે નહીં તે જાણવા:</p>
            <ul>
                <li><b>Article No:</b> EG639444752IN જેવો નંબર નાખો.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 India Post પર ટ્રેક કરો", "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx", use_container_width=True)

st.divider()

# ── DIRECT EMBEDDED IFRAME (OPTIONAL VISUAL) ──────────────────────
st.subheader("📲 પોર્ટલ ક્વિક વ્યુ")
st.caption("જો સરકારી પોર્ટેલ પરમિટ આપશે તો સીધું જ નીચે પેજ ખૂલશે, નહીંતર ઉપર આપેલા બટન પર ક્લિક કરો.")

if "1. e-Sarkar" in portal_type:
    components.iframe("https://esarkar.gujarat.gov.in/", height=500, scrolling=True)
elif "4. સ્પીડ પોસ્ટ" in portal_type:
    components.iframe("https://www.indiapost.gov.in/", height=500, scrolling=True)
else:
    st.info("આ પોર્ટલ સુરક્ષા કારણોસર સત્તાવાર વેબસાઈટ પર જઈને જ ટ્રેક કરી શકાશે. ઉપર આપેલી લિંક પર ક્લિક કરો.")
