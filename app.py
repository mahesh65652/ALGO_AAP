import streamlit as st
import streamlit.components.v1 as components

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Modern Legal & Municipal Portal",
    page_icon="🏛️",
    layout="wide"
)

# ── CUSTOM CSS FOR 3CX NEON DARK THEME ─────────────────────────────
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #020b18 0%, #08142b 100%) !important;
        color: #ffffff !important;
    }
    
    /* Header Styling */
    .main-title {
        color: #40a9ff;
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #8c8c8c;
        font-size: 16px;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Top Grid Feature Cards */
    .card-box {
        background: rgba(13, 27, 54, 0.7);
        border: 1px solid #173b70;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .card-box:hover {
        border-color: #1890ff;
        box-shadow: 0 0 15px rgba(24, 144, 255, 0.4);
        transform: translateY(-2px);
    }
    .card-icon {
        font-size: 28px;
        margin-bottom: 10px;
        color: #40a9ff;
    }
    .card-title {
        color: #1890ff !important;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .card-desc {
        color: #a6c5e8 !important;
        font-size: 13px;
        line-height: 1.4;
    }

    /* Workflow Container */
    .workflow-container {
        background: rgba(13, 27, 54, 0.5);
        border: 1px solid #173b70;
        border-radius: 16px;
        padding: 25px;
        margin-top: 25px;
    }
    .workflow-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Process Flow Item */
    .flow-step {
        background: #091a38;
        border: 1px solid #173b70;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: #ffffff;
    }
    .arrow-icon {
        font-size: 24px;
        color: #1890ff;
        text-align: center;
        line-height: 60px;
    }
    
    /* Native Buttons Dark Modern Override */
    div[data-testid="stButton"] > button {
        background-color: #0d1b36 !important;
        border: 1px solid #173b70 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #1890ff !important;
        color: #1890ff !important;
        box-shadow: 0 0 10px rgba(24, 144, 255, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────
st.markdown('<div class="main-title">3CX Style - લીગલ & સિવિલ પોર્ટલ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">તમારા ડ્રાફ્ટિંગ અને સરકારી કામકાજ માટે મોર્ડન ડેશબોર્ડ</div>', unsafe_allow_html=True)

# ── TOP GRID BUTTONS / CARDS (ઈમેજના 3 Cards જેવું) ────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="card-box">
            <div class="card-icon">🎧</div>
            <div class="card-title">Support</div>
            <div class="card-desc">સરકારી અરજીઓ અને દસ્તાવેજ ટ્રેકિંગ માટે મદદ મેળવો.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card-box">
            <div class="card-icon">📈</div>
            <div class="card-title">Legal Drafts</div>
            <div class="card-desc">CPC, SMC અને રેવન્યુ માટે ડાયરેક્ટ અરજીઓ તૈયાર કરો.</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card-box">
            <div class="card-icon">📋</div>
            <div class="card-title">Status Check</div>
            <div class="card-desc">ઈનવર્ડ નંબર અને કેસ સ્ટેટસ તુરંત જ ચેક કરો.</div>
        </div>
    """, unsafe_allow_html=True)

# ── FLOW PROCESS (ઈમેજના "From conversation to action" જેવું) ───────
st.markdown("""
    <div class="workflow-container">
        <div class="workflow-title">અરજી બનાવવાની સરળ પ્રક્રિયા (Workflow)</div>
    </div>
""", unsafe_allow_html=True)

fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns([2, 0.5, 2, 0.5, 2])

with fcol1:
    st.markdown("""
        <div class="flow-step">
            <div style="font-size:24px;">📝</div>
            <b>૧. ફોર્મ ભરો</b>
        </div>
    """, unsafe_allow_html=True)

with fcol2:
    st.markdown('<div class="arrow-icon">➔</div>', unsafe_allow_html=True)

with fcol3:
    st.markdown("""
        <div class="flow-step">
            <div style="font-size:24px;">📄</div>
            <b>૨. ડ્રાફ્ટ તૈયાર થશે</b>
        </div>
    """, unsafe_allow_html=True)

with fcol4:
    st.markdown('<div class="arrow-icon">➔</div>', unsafe_allow_html=True)

with fcol5:
    st.markdown("""
        <div class="flow-step">
            <div style="font-size:24px;">🖨️</div>
            <b>૩. ડાઉનલોડ / પ્રિન્ટ</b>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ── ACTION SECTION ────────────────────────────────────────────────
st.subheader("⚙️ વિકલ્પ પસંદ કરો")
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("📝 નવી અરજી ડ્રાફ્ટ કરો", use_container_width=True):
        st.success("ડ્રાફ્ટિંગ સેક્શન ખુલ્યું!")

with btn_col2:
    if st.button("🔍 સ્ટેટસ તપાસો (SMC/AMC)", use_container_width=True):
        st.info("સ્ટેટસ પોર્ટલ શરૂ થયું!")
