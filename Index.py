import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

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
    .copy-box {
        background-color: #0b3d91;
        padding: 12px 16px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    /* Big portal-selector buttons */
    div[data-testid="stButton"] > button {
        width: 100%;
        min-height: 70px;
        font-size: 18px !important;
        white-space: normal;
        line-height: 1.3;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #16a34a;
        border: 3px solid #4ade80;
    }
    </style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────
st.title("🔍 સરકારી અરજી અને ઈનવર્ડ નંબર ટ્રેકર")
st.caption("ગાંધીનગર સચિવાલય, કલેક્ટર કચેરી (iORA) અને ઈન્ડિયા પોસ્ટ ટ્રેકિંગ સિસ્ટમ")
st.info(
    "ℹ️ **નોંધ:** સરકારી પોર્ટલ્સ OTP / CAPTCHA સુરક્ષા વાપરે છે, એટલે લોગિન અને OTP તમારે "
    "જાતે જ કરવાના રહેશે. આ ટૂલ ફક્ત તમારો નંબર **સાચી જગ્યાએ ઝડપથી પહોંચાડવા** (clipboard copy "
    "+ ડાયરેક્ટ લિંક) માટે મદદ કરે છે, જેથી ફરી ટાઈપ ન કરવું પડે."
)
st.divider()

# ── SIDEBAR MENU ───────────────────────────────────────────────────
with st.sidebar:
    st.header("🌐 સત્તાવાર સરકારી પોર્ટેલ્સ")
    st.link_button("🏛️ e-Sarkar (સચિવાલય)", "https://esarkar.gujarat.gov.in/", use_container_width=True)
    st.link_button("🏢 iORA (કલેક્ટર/મહેસૂલ)", "https://iora.gujarat.gov.in/", use_container_width=True)
    st.link_button("📢 SWAGAT ઓનલાઈન", "https://swagat.gujarat.gov.in/", use_container_width=True)
    st.link_button("📮 ઇન્ડિયા પોસ્ટ ટ્રેકિંગ", "https://www.indiapost.gov.in/", use_container_width=True)


def copy_to_clipboard_widget(text_to_copy: str, label: str = "📋 નંબર કોપી કરો"):
    """Renders a button that copies `text_to_copy` to the clipboard via JS."""
    safe_text = text_to_copy.replace("\\", "\\\\").replace("`", "\\`")
    components.html(
        f"""
        <div style="display:flex; justify-content:flex-start;">
        <button id="copyBtn" style="
            background-color:#16a34a;color:white;border:none;
            padding:10px 18px;border-radius:8px;font-weight:bold;
            cursor:pointer;font-size:14px;">
            {label}
        </button>
        <span id="copyMsg" style="margin-left:10px;color:#4ade80;font-weight:bold;"></span>
        </div>
        <script>
        const btn = document.getElementById("copyBtn");
        btn.addEventListener("click", async () => {{
            try {{
                await navigator.clipboard.writeText(`{safe_text}`);
                document.getElementById("copyMsg").innerText = "✅ કોપી થયું!";
            }} catch (err) {{
                document.getElementById("copyMsg").innerText = "⚠️ કોપી ન થયું, જાતે સિલેક્ટ કરો";
            }}
        }});
        </script>
        """,
        height=50,
    )


# ── PORTAL SELECTOR (BIG BUTTONS, FULL WIDTH) ──────────────────────
st.subheader("👉 પહેલા કચેરી/પોર્ટલ પસંદ કરો (નીચે બટન દબાવો)")

if "portal_type" not in st.session_state:
    st.session_state.portal_type = "1. e-Sarkar (ગાંધીનગર સચિવાલય / મહેસૂલ વિભાગ)"

PORTAL_OPTIONS = [
    ("1. e-Sarkar (ગાંધીનગર સચિવાલય / મહેસૂલ વિભાગ)", "🏛️ e-Sarkar\n(સચિવાલય)"),
    ("2. iORA પોર્ટલ (મોરબી કલેક્ટર / જમીન કચેરી)", "🏢 iORA\n(કલેક્ટર/જમીન)"),
    ("3. SWAGAT / PG Portal (ઓનલાઈન ફરિયાદ સ્ટેટસ)", "📢 SWAGAT\n(ફરિયાદ સ્ટેટસ)"),
    ("4. સ્પીડ પોસ્ટ ટ્રેકિંગ (India Post)", "📮 India Post\n(સ્પીડ પોસ્ટ)"),
]

btn_cols = st.columns(4, gap="medium")
for col, (value, label) in zip(btn_cols, PORTAL_OPTIONS):
    with col:
        is_selected = st.session_state.portal_type == value
        if st.button(
            label,
            key=f"portal_btn_{value}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
        ):
            st.session_state.portal_type = value
            st.rerun()

portal_type = st.session_state.portal_type
st.success(f"✅ પસંદ કરેલું: **{portal_type}**")
st.divider()

# ── MAIN TRACKING SECTION ─────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📌 ઈનવર્ડ નંબર અથવા રસીદ વિગત નાખો")

    inward_num = st.text_input(
        "ઈનવર્ડ નંબર / એપ્લિકેશન નંબર / ટ્રેકિંગ ID:",
        placeholder="દા.ત. EG639444752IN અથવા Inward No."
    )

    selected_year = st.selectbox("અરજીનું વર્ષ:", ["2026", "2025", "2024"])

    go = st.button("🔎 નંબર તૈયાર કરો → પોર્ટલ પર જાઓ", use_container_width=True)

    if go and not inward_num:
        st.warning("કૃપા કરીને ઈનવર્ડ નંબર અથવા સ્પીડ પોસ્ટ ટ્રેકિંગ ID નાખો.")

with col2:
    st.subheader("🌐 પોર્ટલ ટ્રેકિંગ અને ડાયરેક્ટ એક્સેસ")

    clean_num = inward_num.strip() if inward_num else ""

    if "1. e-Sarkar" in portal_type:
        st.markdown("""
        <div class="status-card">
            <h4>🏛️ e-Sarkar પોર્ટલ (ગાંધીનગર)</h4>
            <p>ગાંધીનગર સચિવાલયમાં આપેલી અરજીનો ઈનવર્ડ નંબર ટ્રેક કરવા માટે:</p>
            <ol>
                <li>નીચે "કોપી કરો" દબાવીને નંબર કોપી કરો.</li>
                <li>પછી "e-Sarkar પર જાઓ" દબાવો — નવી ટેબમાં પોર્ટલ ખૂલશે.</li>
                <li>ત્યાં <b>Inward Number</b> ફિલ્ડમાં Paste (Ctrl+V) કરો અને <b>Year</b> નાખો.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        if clean_num:
            copy_to_clipboard_widget(clean_num)
        st.link_button("🔗 e-Sarkar પર જાઓ", "https://esarkar.gujarat.gov.in/trackApp.jsp", use_container_width=True)

    elif "2. iORA" in portal_type:
        st.markdown("""
        <div class="status-card">
            <h4>🏢 iORA પોર્ટલ (જિલ્લા કલેક્ટર કચેરી)</h4>
            <p>મોરબી કલેક્ટર કચેરી કે લેન્ડ ગ્રેબિંગ શાખાની અરજી ટ્રેક કરવા માટે:</p>
            <ol>
                <li>નીચે "કોપી કરો" દબાવીને Application/Inward No કોપી કરો.</li>
                <li>"iORA પર જાઓ" દબાવો.</li>
                <li>ત્યાં નંબર Paste કરો અને રજિસ્ટર્ડ મોબાઈલ પર આવેલ OTP નાખો.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        if clean_num:
            copy_to_clipboard_widget(clean_num)
        st.link_button("🔗 iORA પર જાઓ", "https://iora.gujarat.gov.in/OnlineAppStatus.aspx", use_container_width=True)

    elif "3. SWAGAT" in portal_type:
        st.markdown("""
        <div class="status-card">
            <h4>📢 સ્વાગત (SWAGAT) / CPGRAMS પોર્ટલ</h4>
            <p>મુખ્યમંત્રીશ્રી ઓનલાઈન ફરિયાદ નિવારણ પોર્ટલ સ્ટેટસ:</p>
            <ol>
                <li>નીચે "કોપી કરો" દબાવીને ફરિયાદ નંબર કોપી કરો.</li>
                <li>"SWAGAT પર જાઓ" દબાવો અને નંબર Paste કરો.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        if clean_num:
            copy_to_clipboard_widget(clean_num)
        st.link_button("🔗 SWAGAT પર જાઓ", "https://swagat.gujarat.gov.in/", use_container_width=True)

    else:
        st.markdown("""
        <div class="status-card">
            <h4>📮 India Post ટ્રેકિંગ</h4>
            <p>તમારી સ્પીડ પોસ્ટ ટપાલ કચેરીમાં પહોંચી છે કે નહીં તે જાણવા:</p>
        </div>
        """, unsafe_allow_html=True)
        if clean_num:
            copy_to_clipboard_widget(clean_num, label="📋 Article No કોપી કરો")
            # India Post's tracking page reads the article number from this query param
            # on load in most cases — if it doesn't auto-fill, paste it manually.
            direct_url = (
                "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/"
                "trackconsignment.aspx?ArticleNo=" + urllib.parse.quote(clean_num)
            )
            st.link_button("🔗 India Post પર સીધું ટ્રેક કરો", direct_url, use_container_width=True)
            st.caption("જો પોર્ટલ પર નંબર આપોઆપ ના દેખાય, તો Paste (Ctrl+V) કરી લેજો.")
        else:
            st.link_button(
                "🔗 India Post પર ટ્રેક કરો",
                "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx",
                use_container_width=True
            )

st.divider()
st.caption(
    "🔒 સુરક્ષાની નોંધ: આ એપ કોઈપણ સરકારી પોર્ટલનું લોગિન, OTP કે CAPTCHA બાયપાસ કરતી નથી — "
    "એ સ્ટેપ તમારે જાતે પૂરા કરવાના રહેશે. આ ફક્ત નંબર ઝડપથી સાચી જગ્યાએ પહોંચાડવામાં મદદ કરે છે."
)
