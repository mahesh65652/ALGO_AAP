import io
import sqlite3
import hashlib
import streamlit as st
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import streamlit.components.v1 as components

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="ગુજરાત લીગલ, મ્યુનિસિપલ કોર્પોરેશન & સિવિલ સેવા પોર્ટલ",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 3CX STYLE ULTRA MODERN DARK NEON + 3D BUTTON CSS ───────────────
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #020b18 0%, #08142b 100%) !important;
        color: #ffffff !important;
        max-width: 100vw;
        overflow-x: hidden !important;
    }
    
    /* Global Typography Fixes */
    h1, h2, h3, h4, h5, h6, span, label, p, .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Header UI */
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
        margin-bottom: 25px;
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
    }
    .card-icon {
        font-size: 28px;
        margin-bottom: 10px;
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

    /* Workflow Styles */
    .workflow-container {
        background: rgba(13, 27, 54, 0.5);
        border: 1px solid #173b70;
        border-radius: 16px;
        padding: 15px 25px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .workflow-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .flow-step {
        background: #091a38;
        border: 1px solid #173b70;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        color: #ffffff;
    }
    .arrow-icon {
        font-size: 24px;
        color: #1890ff;
        text-align: center;
        line-height: 50px;
    }

    /* Streamlit Input Styling Override */
    .stTextInput input, .stTextArea textarea {
        color: #ffffff !important;
        background-color: #0b1930 !important;
        border: 1px solid #173b70 !important;
        border-radius: 8px !important;
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        background-color: #091a38;
        color: #ffffff !important;
        border: 1px solid #173b70;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1890ff !important;
        color: #ffffff !important;
    }

    /* Native Buttons Theme Override */
    div[data-testid="stButton"] > button {
        width: 100%;
        min-height: 48px;
        font-size: 15px !important;
        background-color: #0d1b36 !important;
        border: 1px solid #173b70 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #1890ff !important;
        color: #1890ff !important;
        box-shadow: 0 0 12px rgba(24, 144, 255, 0.3) !important;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #1890ff !important;
        border: 1px solid #40a9ff !important;
        color: #ffffff !important;
    }
    .cat-btn button {
        min-height: 44px !important;
        font-size: 14px !important;
    }

    /* ── 3D MULTICOLOR BUTTON CSS ── */
    .btn-3d-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    .btn-3d {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 14px 20px;
        font-size: 15px;
        font-weight: 700;
        color: #ffffff !important;
        text-decoration: none !important;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        transition: all 0.15s ease-in-out;
        box-shadow: 0 6px 0 rgba(0, 0, 0, 0.4), 0 8px 15px rgba(0, 0, 0, 0.3);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    .btn-3d:active {
        transform: translateY(4px);
        box-shadow: 0 2px 0 rgba(0, 0, 0, 0.4), 0 3px 6px rgba(0, 0, 0, 0.2);
    }
    .btn-blue {
        background: linear-gradient(145deg, #1e88e5, #1565c0);
        box-shadow: 0 6px 0 #0d47a1, 0 8px 15px rgba(21, 101, 192, 0.4);
    }
    .btn-green {
        background: linear-gradient(145deg, #43a047, #2e7d32);
        box-shadow: 0 6px 0 #1b5e20, 0 8px 15px rgba(46, 125, 50, 0.4);
    }
    .btn-purple {
        background: linear-gradient(145deg, #8e24aa, #6a1b9a);
        box-shadow: 0 6px 0 #4a148c, 0 8px 15px rgba(106, 27, 154, 0.4);
    }
    .btn-orange {
        background: linear-gradient(145deg, #fb8c00, #ef6c00);
        box-shadow: 0 6px 0 #e65100, 0 8px 15px rgba(239, 108, 0, 0.4);
    }
    .btn-red {
        background: linear-gradient(145deg, #e53935, #c62828);
        box-shadow: 0 6px 0 #b71c1c, 0 8px 15px rgba(198, 40, 40, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ── DATABASE SETUP ─────────────────────────────────────────────────
DB_FILE = "legal_drafts_secure_v8.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                doc_type TEXT NOT NULL,
                court_name TEXT,
                applicant_name TEXT,
                opposite_party TEXT,
                case_number TEXT,
                doc_body TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        """)
        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            admin_pass = hashlib.sha256("admin123_secure_salt".encode()).hexdigest()
            c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", ("admin", admin_pass, "admin"))

init_db()

def hash_password(password):
    return hashlib.sha256(f"{password}_secure_salt".encode()).hexdigest()

def verify_user(username, password):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        res = c.fetchone()
        if res and res[0] == hash_password(password):
            return res[1]
    return None

def register_user(username, password, role="client"):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                      (username, hash_password(password), role))
            return True
    except sqlite3.IntegrityError:
        return False

def save_user_draft(username, doc_type, court_name, applicant_name, opposite_party, case_number, doc_body):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO drafts (username, doc_type, court_name, applicant_name, opposite_party, case_number, doc_body)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, doc_type, court_name, applicant_name, opposite_party, case_number, doc_body))

def update_user_draft(draft_id, court_name, applicant_name, opposite_party, case_number, doc_body):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE drafts
            SET court_name = ?, applicant_name = ?, opposite_party = ?, case_number = ?, doc_body = ?
            WHERE id = ?
        """, (court_name, applicant_name, opposite_party, case_number, doc_body, draft_id))

def get_user_drafts(username, search_query="", is_admin=False):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        query = "%" + search_query + "%"
        if is_admin:
            c.execute("""
                SELECT id, username, doc_type, applicant_name, created_at, court_name, opposite_party, case_number, doc_body
                FROM drafts
                WHERE applicant_name LIKE ? OR doc_type LIKE ? OR case_number LIKE ?
                ORDER BY created_at DESC
            """, (query, query, query))
        else:
            c.execute("""
                SELECT id, username, doc_type, applicant_name, created_at, court_name, opposite_party, case_number, doc_body
                FROM drafts
                WHERE username = ? AND (applicant_name LIKE ? OR doc_type LIKE ? OR case_number LIKE ?)
                ORDER BY created_at DESC
            """, (username, query, query, query))
        return c.fetchall()

def delete_user_draft(draft_id, username, is_admin=False):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        if is_admin:
            c.execute("DELETE FROM drafts WHERE id = ?", (draft_id,))
        else:
            c.execute("DELETE FROM drafts WHERE id = ? AND username = ?", (draft_id, username))

# ── SESSION STATE ──────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "role" not in st.session_state:
    st.session_state["role"] = ""

# ── SIDEBAR ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏛️ સેવા સદન & લીગલ સેન્ટર")

    with st.expander("🔐 લોગિન / એકાઉન્ટ", expanded=not st.session_state["logged_in"]):
        if not st.session_state["logged_in"]:
            auth_mode = st.radio("પસંદ કરો:", ["લોગિન (Login)", "નવું એકાઉન્ટ"])

            if auth_mode == "લોગિન (Login)":
                user_input = st.text_input("યુઝરનામ")
                pass_input = st.text_input("પાસવર્ડ", type="password")
                if st.button("🔓 લોગિન કરો", use_container_width=True, type="primary"):
                    role = verify_user(user_input, pass_input)
                    if role:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_input
                        st.session_state["role"] = role
                        st.success(f"જી આયા થી, {user_input}!")
                        st.rerun()
                    else:
                        st.error("ખોટો યુઝરનામ અથવા પાસવર્ડ!")
            else:
                new_user = st.text_input("નવું યુઝરનામ")
                new_pass = st.text_input("નવો પાસવર્ડ", type="password")
                if st.button("📝 એકાઉન્ટ બનાવો", use_container_width=True):
                    if new_user and new_pass:
                        if register_user(new_user, new_pass):
                            st.success("એકાઉન્ટ બની ગયું! હવે લોગિન કરો.")
                        else:
                            st.error("આ યુઝરનામ ઉપલબ્ધ નથી!")
                    else:
                        st.warning("બધી વિગતો ભરો.")
        else:
            st.success(f"👤 **{st.session_state['username']}** ({'Admin' if st.session_state['role'] == 'admin' else 'Client'})")
            if st.button("🚪 લોગઆઉટ", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.session_state["role"] = ""
                st.rerun()

    # 🔎 ઈનવર્ડ નંબર / એપ્લિકેશન સ્ટેટસ ચેક સેક્શન
    with st.expander("🔎 ઈનવર્ડ નંબર / અરજી સ્ટેટસ ચેક"):
        st.write("તમારા ઈનવર્ડ / એપ્લિકેશન નંબર થી ડાયરેક્ટ અરજીનું સ્ટેટસ તપાસો:")
        st.link_button("🚫 લેન્ડ ગ્રેબિંગ અરજી સ્ટેટસ (iORA / Collector)", "https://iora.gujarat.gov.in/", use_container_width=True)
        st.link_button("🔍 SMC સુરત અરજી / ઈનવર્ડ સ્ટેટસ", "https://www.suratmunicipal.gov.in/Services/CheckApplicationStatus", use_container_width=True)
        st.link_button("🔍 AMC અમદાવાદ કોમ્પ્લેઇન્ટ/અરજી સ્ટેટસ", "https://ahmedabadcity.gov.in/", use_container_width=True)
        st.link_button("🔍 e-Dhara / iORA રેવન્યુ અરજી સ્ટેટસ", "https://iora.gujarat.gov.in/", use_container_width=True)
        st.link_button("🔍 e-Courts કેસ સ્ટેટસ (હાઇકોર્ટો & ડિસ્ટ્રિક્ટ)", "https://services.ecourts.gov.in/", use_container_width=True)

    # 🏢 ગુજરાતની તમામ 8 મહાનગરપાલિકાઓની વેબસાઈટ
    with st.expander("🏙️ ગુજરાત ની તમામ મહાનગરપાલિકાઓ (MNC)"):
        st.link_button("🏢 SMC સુરત મહાનગરપાલિકા", "https://www.suratmunicipal.gov.in/", use_container_width=True)
        st.link_button("🏢 AMC અમદાવાદ મહાનગરપાલિકા", "https://ahmedabadcity.gov.in/", use_container_width=True)
        st.link_button("🏢 VMC વડોદરા મહાનગરપાલિકા", "https://vmc.gov.in/", use_container_width=True)
        st.link_button("🏢 RMC રાજકોટ મહાનગરપાલિકા", "https://www.rmc.gov.in/", use_container_width=True)
        st.link_button("🏢 GMC ગાંધીનગર મહાનગરપાલિકા", "https://gmc.gujarat.gov.in/", use_container_width=True)
        st.link_button("🏢 BMC ભાવનગર મહાનગરપાલિકા", "https://bmcgujarat.com/", use_container_width=True)
        st.link_button("🏢 JMC જામનગર મહાનગરપાલિકા", "https://www.mcjamnagar.com/", use_container_width=True)
        st.link_button("🏢 JMC જૂનાગઢ મહાનગરપાલિકા", "https://junagadhmunicipal.org/", use_container_width=True)

    # 🌐 અન્ય મહેસૂલી અને કાનૂની પોર્ટલ
    with st.expander("🌐 મહત્વપૂર્ણ સરકારી લીંક"):
        st.link_button("🌐 AnyRoR Gujarat (૭/૧૨, ૮-અ)", "https://anyror.gujarat.gov.in/", use_container_width=True)
        st.link_button("🗺️ BhuNaksha Gujarat (જમીન નકશો)", "https://bhunaksha.gujarat.gov.in/", use_container_width=True)
        st.link_button("🏛️ iORA Gujarat (ઓનલાઈન રેવન્યુ અરજીઓ)", "https://iora.gujarat.gov.in/", use_container_width=True)
        st.link_button("📑 e-Dhara Gujarat (રેકોર્ડ અને ફેરફાર)", "https://edhara.gujarat.gov.in/", use_container_width=True)
        st.link_button("📜 GARVI Gujarat (દસ્તાવેજ નોંધણી & Index-2)", "https://garvigujarat.gov.in/", use_container_width=True)
        st.link_button("💻 e-Jamin Gujarat (જમીન સંબંધિત સેવાઓ)", "https://e-jamin.gujarat.gov.in/", use_container_width=True)
        st.link_button("📋 Digital Gujarat", "https://www.digitalgujarat.gov.in", use_container_width=True)
        st.link_button("📢 SWAGAT Online", "https://swagat.gujarat.gov.in/", use_container_width=True)

# ── HERO DASHBOARD SECTION (3CX STYLE) ─────────────────────────────
st.markdown('<div class="main-title">3CX Style - લીગલ & સિવિલ પોર્ટલ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">તમારા ડ્રાફ્ટિંગ અને સરકારી કામકાજ માટે મોર્ડન ડેશબોર્ડ</div>', unsafe_allow_html=True)

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

# ── 3D MULTICOLOR QUICK ACTION BUTTONS SECTION ──────────────────────
st.write("")
st.markdown("### 🚀 ક્વિક 3D એક્શન પોર્ટલ")
st.markdown("""
    <div class="btn-3d-grid">
        <a href="https://iora.gujarat.gov.in/" target="_blank" class="btn-3d btn-blue">
            🌐 iORA ઓનલાઇન અરજી
        </a>
        <a href="https://anyror.gujarat.gov.in/" target="_blank" class="btn-3d btn-green">
            📜 AnyRoR ૭/૧૨ & ૮-અ
        </a>
        <a href="https://services.ecourts.gov.in/" target="_blank" class="btn-3d btn-purple">
            ⚖️ e-Courts કેસ સ્ટેટસ
        </a>
        <a href="https://www.suratmunicipal.gov.in/" target="_blank" class="btn-3d btn-orange">
            🏢 SMC સુરત પોર્ટલ
        </a>
        <a href="https://garvigujarat.gov.in/" target="_blank" class="btn-3d btn-red">
            📑 GARVI દસ્તાવેજ નોંધણી
        </a>
    </div>
""", unsafe_allow_html=True)

# Workflow Banner
st.markdown("""
    <div class="workflow-container">
        <div class="workflow-title">અરજી બનાવવાની સરળ પ્રક્રિયા (Workflow)</div>
    </div>
""", unsafe_allow_html=True)

fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns([2, 0.5, 2, 0.5, 2])
with fcol1:
    st.markdown('<div class="flow-step"><div style="font-size:22px;">📝</div><b>૧. ફોર્મ ભરો</b></div>', unsafe_allow_html=True)
with fcol2:
    st.markdown('<div class="arrow-icon">➔</div>', unsafe_allow_html=True)
with fcol3:
    st.markdown('<div class="flow-step"><div style="font-size:22px;">📄</div><b>૨. ડ્રાફ્ટ તૈયાર થશે</b></div>', unsafe_allow_html=True)
with fcol4:
    st.markdown('<div class="arrow-icon">➔</div>', unsafe_allow_html=True)
with fcol5:
    st.markdown('<div class="flow-step"><div style="font-size:22px;">🖨️</div><b>૩. ડાઉનલોડ / પ્રિન્ટ</b></div>', unsafe_allow_html=True)

st.write("")
st.divider()

# ── TEMPLATES ──────────────────────────────────────────────────────
TEMPLATE_CATEGORIES = {
    "⚖️ CPC દીવાની અદાલત (૨૫ અરજીઓ)": {
        "૧. કામચલાઉ મનાઈહુકમ (Order 39 Rules 1 & 2)":
"""અરજી: કાયદાની દીવાની કાર્યરીતિ સંહિતા (CPC) ઓર્ડર ૩૯ રૂલ ૧ અને ૨ મુજબ કામચલાઉ મનાઈહુકમ (Temporary Injunction) મળવા બાબત.

સાહેબશ્રી,
વાદી સવિનય અર્જ કરે છે કે:
૧. વાદીની માલિકી તથા કબજા ભોગવટાની મિલકતમાં પ્રતિવાદી દ્વારા બિનકાયદેસર રીતે પ્રવેશ કરી/બાંધકામ કરી વાદીના હકોમાં અડચણ ઊભી કરવામાં આવે છે.
૨. સદર કેસનો આખરી નિકાલ ન થાય ત્યાં સુધી જો કામચલાઉ મનાઈહુકમ આપવામાં નહીં આવે તો વાદીને અપૂરણીય નુકસાન (Irreparable Loss) થશે.

માટે દાવો આખરી નિકાલ ન થાય ત્યાં સુધી પ્રતિવાદી સામે ગેરકાયદેસર પ્રવૃત્તિ રોકવા કામચલાઉ મનાઈહુકમ આપવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૨. એકતરફી વચગાળાનો મનાઈહુકમ (Order 39 Rule 3)":
"""અરજી: ઓર્ડર ૩૯ રૂલ ૩ મુજબ સામાવાળાને સાંભળ્યા વિના તાત્કાલિક એકતરફી વચગાળાનો મનાઈહુકમ (Ex-parte Ad-interim Injunction) આપવા બાબત.

સાહેબશ્રી,
વાદી સવિનય રજૂઆત કરે છે કે પ્રતિવાદી દ્વારા અત્યંત ઉતાવળે ગેરકાયદેસર કૃત્ય કરવામાં આવી રહ્યું છે. જો સામાવાળાને નોટિસ બજવણીની રાહ જોવામાં આવશે તો મનાઈહુકમનો મૂળ હેતુ માર્યો જશે અને વિલંબથી મોટું નુકસાન થશે. માટે તાત્કાલિક એકતરફી સ્ટે આપવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૩. રીસીવરની નિમણૂક (Order 40 Rule 1)":
"""અરજી: વિવાદાસપદ મિલકતની સંભાળ, ભાડું ઉઘરાવવા અને રક્ષણ માટે રીસીવર નીમવા બાબત. (Order 40 Rule 1)

સાહેબશ્રી,
સદર દાવેવાળી મિલકતમાંથી પ્રતિવાદી ગેરકાયદે લાભ મેળવી રહ્યા છે અને મિલકતને નુકસાન પહોંચાડી રહ્યા છે. મિલકતની યોગ્ય સંભાળ રહે તે માટે તટસ્થ રીસીવર નીમવા હુકમ કરવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૪. ચુકાદા પહેલાં અટકાયત / ધરપકડ (Order 38 Rule 1)":
"""અરજી: પ્રતિવાદી ભાગી ન જાય તે માટે નાણાકીય જામીન લેવા અથવા કસ્ટડીમાં મોકલવા બાબત. (Order 38 Rule 1)

સાહેબશ્રી,
પ્રતિવાદી અદાલતના अधिकारક્ષેત્રમાંથી ભાગી જવાની અને દાવાની રકમની વસુલાતમાં અડચણ ઊભી કરવાની તૈયારીમાં છે. માટે પ્રતિવાદી પાસે યોગ્ય જામીન લેવા અથવા અટકાયત કરવા હુકમ ફરમાવવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૫. ચુકાદા પહેલાં જપ્તી (Order 38 Rule 5)":
"""અરજી: દાવો ચાલુ હોય તે દરમિયાન મિલકત ટ્રાન્સફર/વેચાણ થતી રોકવા જપ્ત કરાવવા બાબત. (Order 38 Rule 5)

સાહેબશ્રી,
પ્રતિવાદી પોતાની મિલકતો વેચી દેવા અથવા ટ્રાન્સફર કરવા માંગે છે જેથી વાદીના દાવાનો હુકમનામું નિષ્ફળ જાય. માટે ચુકાદા પહેલાં જ મિલકત ટાંચ/જપ્ત કરવાનો હુકમ કરવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૬. દાવો મુલતવી રાખવો / સ્ટે ઓફ સૂટ (Section 10)":
"""અરજી: એક જ વિષય પર બે અલગ કોર્ટમાં કેસ ન ચાલે તે માટે પાછળનો કેસ અટકાવવા બાબત. (Section 10)

સાહેબશ્રી,
આ જ પક્ષકારો વચ્ચે અને આ જ વિષયવસ્તુ અંગેનો સમાન દાવો અન્ય સક્ષમ અદાલતમાં પણ પેન્ડિંગ છે. માટે કલમ ૧૦ ની જોગવાઈ મુજબ આ પાછળથી દાખલ કરેલ દાવો મુલતવી રાખવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૭. કેસ ટ્રાન્સફર કરવાની અરજી (Section 24)":
"""અરજી: વ્યાજબી કારણોસર કેસને એક અદાલતમાંથી બીજી અદાલતમાં ટ્રાન્સફર કરાવવા બાબત. (Section 24)

સાહેબશ્રી,
ન્યાયના હિતમાં અને તટસ્થ સુનાવણી અર્થે સદર કેસને વર્તમાન અદાલતમાંથી અન્ય સક્ષમ અદાલતમાં ટ્રાન્સફર કરવા હુકમ કરવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૮. પ્લીડીંગ્સમાં સુધારો (Order 6 Rule 17)":
"""અરજી: દાવપત્ર અથવા જવાબમાં થયેલી ટાઈપિંગ કે તથ્યની ભૂલો સુધારવા બાબત. (Order 6 Rule 17)

સાહેબશ્રી,
મુખ્ય દાવા/જવાબમાં કેટલીક મહત્વની વિગતો ઉમેરવી કે ભૂલો સુધારવી ન્યાયના હિતમાં જરૂરી છે, જેનાથી કેસનું સ્વરૂપ બદલાતું નથી. સદર સુધારો કરવાની મંજૂરી આપવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૯. પ્લેઈન્ટનો અસ્વીકાર / રદબાદલ (Order 7 Rule 11)":
"""અરજી: કાયદાકીય નિયમોનું પાલન ન થયું હોય ત્યારે શરૂઆતમાં જ દાવો રદ કરાવવા બાબત. (Order 7 Rule 11)

સાહેબશ્રી,
વાદીનો દાવો કોઈ યોગ્ય કારણ (Cause of Action) દર્શાવતો નથી અથવા કાયદાકીય મર્યાદા (Barred by Law) થી બાધિત છે. માટે ઓર્ડર ૭ રૂલ ૧૧ મુજબ દાવો રદબાતલ કરવા અરજી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૦. પ્લેઈન્ટ પરત કરવો (Order 7 Rule 10)":
"""અરજી: ખોટી અદાલતમાં દાખલ થયેલો કેસ યોગ્ય કોર્ટમાં રજૂ કરવા પરત મેળવવા બાબત. (Order 7 Rule 10)

સાહેબશ્રી,
આ અદાલતને સદર વિષયવસ્તુ કે આર્થિક અધિકારક્ષેત્ર (Jurisdiction) ન હોવાથી, વાદીને યોગ્ય કોર્ટમાં દાવો રજૂ કરવા માટે પ્લેઈન્ટ પરત આપવા નમ્ર વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૧. પક્ષકારો ઉમેરવા / ઈમ્પલીડમેન્ટ (Order 1 Rule 10)":
"""અરજી: કેસના ન્યાયી નિર્ણય માટે નવી વ્યક્તિને પક્ષકાર તરીકે જોડવા બાબત. (Order 1 Rule 10)

સાહેબશ્રી,
સદર કેસના નિર્ણયથી અરજદારના હકો પર સીધી અસર પડે તેમ છે. કાયદાકીય અને ન્યાયી ફેંસલા માટે અરજદારને પક્ષકાર તરીકે જોડવા હુકમ કરવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૨. દસ્તાવેજો રજૂ કરવાનો હુકમ (Order 11 Rule 14)":
"""અરજી: સામા પક્ષના કબ્જામાં રહેલા મહત્વના પુરાવા/દસ્તાવેજો રજૂ કરાવવા બાબત. (Order 11 Rule 14)

સાહેબશ્રી,
સદર કેસમાં સાચું સત્ય બહાર લાવવા સામાવાળા પાસે રહેલા મૂળ દસ્તાવેજો અદાલતમાં રજૂ કરાવવા ઓર્ડર કરવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૩. શોધ અને પ્રશ્નાવલી / ઈન્ટરોગેટેરીઝ (Order 11 Rules 1 & 2)":
"""અરજી: મુખ્ય ટ્રાયલ પહેલાં સોગંદનામા પર લેખિત જવાબ મેળવવા પ્રશ્નાવલી મોકલવા બાબત. (Order 11 Rules 1 & 2)

સાહેબશ્રી,
કેસના મુખ્ય મુદ્દાઓ સ્પષ્ટ કરવા અર્થે વાદી/પ્રતિવાદીને ચોક્કસ પ્રશ્નાવલીના જવાબો સોગંદનામા પર આપવા આદેશ કરવા અરજી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૪. મુદ્દાઓ ઘડવા / ફ્રેમિંગ ઓફ ઈશ્યુઝ (Order 14 Rule 1)":
"""અરજી: કયા મુખ્ય વિવાદિત મુદ્દાઓ પર પુરાવા લેવાના છે તેનું માળખું નક્કી કરવા બાબત. (Order 14 Rule 1)

સાહેબશ્રી,
દાવાના પ્લીડીંગ્સના આધારે બંને પક્ષો વચ્ચેના વિવાદિત મુદ્દાઓ (Issues) ઘડી આપવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૫. સ્થાનિક તપાસ માટે કમિશનર (Order 26 Rule 9)":
"""અરજી: સ્થળ તપાસ, માપણી કે અહેવાલ માટે કમિશનર નીમવા બાબત. (Order 26 Rule 9)

સાહેબશ્રી,
સ્થળ પરની વર્તમાન પરિસ્થિતિ, દબાણ કે માપણીનો સચોટ અહેવાલ મેળવવા અદાલતી કમિશનર (Court Commissioner) નીમવા હુકમ કરવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૬. નવો કેસ કરવાની છૂટ સાથે દાવો પાછો ખેંચવો (Order 23 Rule 1)":
"""અરજી: ખામીઓયુક્ત કેસ પાછો ખેંચી, તે જ વિષય પર નવો સુધારેલો કેસ કરવાની મંજૂરી મેળવવા બાબત. (Order 23 Rule 1)

સાહેબશ્રી,
ટેકનિકલ કે કાયદાકીય ત્રુટિના કારણે વર્તમાન દાવો પાછો ખેંચી, નવી સ્વતંત્ર અરજી/દાવો કરવાની રજા આપવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૭. સમજૂતી કે સમાધાન / સેટલમેન્ટ (Order 23 Rule 3)":
"""અરજી: આપસી સમાધાનના કરારને અદાલતમાં રજૂ કરી તેના આધારે હુકમ મેળવવા બાબત. (Order 23 Rule 3)

સાહેબશ્રી,
બંને પક્ષકારો વચ્ચે મુક્ત મનથી રાજીખુશીથી સેટલમેન્ટ થયેલ છે. સમાધાનની શરતો મુજબ આખરી હુકમનામું દોરવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૮. ખર્ચ સામે જામીનગીરી (Order 25 Rule 1)":
"""અરજી: વાદી કેસ હારી જાય તો પ્રતિવાદીનો ખર્ચ ભરપાઈ થઈ શકે તે માટે ડિપોઝિટ જમા કરાવવા બાબત. (Order 25 Rule 1)

સાહેબશ્રી,
વાદી અદાલતના ક્ષેત્ર બહાર રહે છે અને તેની પાસે કોઈ મિલકત નથી. જેથી દાવવાના સંભવિત ખર્ચ સામે જામીનગીરી લેવા અરજી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૧૯. ગેરહાજરી બદલ રદ થયેલો કેસ પુનઃસ્થાપિત કરવો (Order 9 Rule 9)":
"""અરજી: યોગ્ય કારણ દર્શાવી રદ થયેલા કેસને ફરીથી બોર્ડ પર લાવવા બાબત. (Order 9 Rule 9)

સાહેબશ્રી,
અરજદાર વ્યાજબી અને સબળ કારણોસર અદાલતમાં હાજર રહી શક્યા નહોતા. ગેરહાજરી બદલ રદ થયેલ દાવો પુનઃસ્થાપિત કરવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૨૦. અપીલમાં વધારાના પુરાવા (Order 41 Rule 27)":
"""અરજી: ટ્રાયલ કોર્ટમાં રજૂ ન થઈ શકેલા નવા અને મહત્વના પુરાવા અપીલ સ્ટેજે રજૂ કરવાની પરવાનગી. (Order 41 Rule 27)

સાહેબશ્રી,
નીચલી કોર્ટના સમયમાં પૂરતા પ્રયાસો છતાં સદર મહત્વનો પુરાવો મળી શક્યો નહોતો. ન્યાયહિતમાં અપીલ સાથે આ પુરાવો રેકર્ડ પર લેવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૨૧. હુકમનામાના અમલ પર મનાઈહુકમ (Order 41 Rule 5)":
"""અરજી: અપીલ પેન્ડિંગ હોય ત્યાં સુધી નીચલી કોર્ટના ચુકાદાના અમલીકરણ પર સ્ટે મેળવવા બાબત. (Order 41 Rule 5)

સાહેબશ્રી,
નીચલી કોર્ટના હુકમ સામે સક્ષમ અપીલ દાખલ કરવામાં આવેલ છે. અપીલનો ફેંસલો ન આવે ત્યાં સુધી ચુકાદાના અમલ પર સ્ટે આપવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૨૨. એક્ઝિક્યુશનમાં વાંધો / ક્લેમ (Order 21 Rule 58)":
"""અરજી: જપ્ત થયેલી મિલકત પર પોતાનો માલિકી હક સાબિત કરી મુક્ત કરાવવા બાબત. (Order 21 Rule 58)

સાહેબશ્રી,
અમલવારીની કાર્યવાહીમાં જપ્ત કરેલ મિલકત મૂળ નિર્ણયિત દેવાદારની નથી પરંતુ અરજદારની સ્વતંત્ર માલિકીની છે. જેથી મિલકત જપ્તીમાંથી મુક્ત કરવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૨૩. મુદત લંબાવવી / એક્સ્ટેન્શન ઓફ ટાઈમ (Section 148)":
"""અરજી: અદાલતે આપેલા સમયગાળામાં કામ પૂરું ન થઈ શકવા પર વધારાનો સમય મેળવવા બાબત. (Section 148)

સાહેબશ્રી,
સબળ કારણોસર અદાલતે આપેલ સમયમર્યાદામાં જરૂરી કાર્યવાહી થઈ શકી નથી. કલમ ૧૪૮ હેઠળ વધારાની મુદત ફાળવવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૨૪. પુનઃસમીક્ષા અરજી / રિવ્યુ પિટિશન (Order 47 Rule 1)":
"""અરજી: ઉપલી કોર્ટમાં ગયા વગર પોતાના ચુકાદાની ભૂલ સુધારવા પુનઃવિચારણા કરાવવી. (Order 47 Rule 1)

સાહેબશ્રી,
સદર ચુકાદામાં રેકોર્ડ પર દેખીતી ભૂલ (Error apparent on the face of record) રહી ગયેલ હોય, પોતાના ચુકાદા પર પુનઃવિચારણા કરી સુધારો કરવા અરજી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૨૫. કલમકીય કે ગણતરીની ભૂલો સુધારવી (Section 152)":
"""અરજી: ચુકાદા/હુકમનામામાં રહી ગયેલી લખાણ કે આંકડાકીય ભૂલો સુધારવી. (Section 152)

સાહેબશ્રી,
ચુકાદા અથવા હુકમનામામાં અકસ્માતે ટાઈપિંગ કે આંકડાકીય ભૂલ રહી ગયેલ છે. કલમ ૧૫૨ હેઠળ સદર ભૂલ સુધારી આપવા નમ્ર વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",
    },

    "🏢 મહાનગરપાલિકા (SMC / AMC / VMC...)": {
        "મહાનગરપાલિકા પ્રોપર્ટી ટેક્સ નામ ટ્રાન્સફર અરજી":
"""પ્રતિ,
શ્રીમાન ટેક્સ એસેસર સાહેબશ્રી,
____________ મહાનગરપાલિકા, ________ ઝોન / વોર્ડ: ________

વિષય: પ્રોપર્ટી ટેક્સ બિલમાં નામ ટ્રાન્સફર / નામ ફેર કરવા બાબત.
ટેનેમેન્ટ નંબર: ___________________________

સાહેબશ્રી,
સવિનય જણાવવાનું કે, સરનામું: ____________________________________________________________________ વાળી મિલકત મેં રજિસ્ટર્ડ વેચાણ દસ્તાવેજ નંબર: ________, તારીખ: __/__/૨૦૨૬ થી ખરીદ કરેલ છે / વારસાઈ અન્વયે મેળવેલ છે.

જૂના માલિકનું નામ: ____________________________________
નવા માલિકનું નામ: ____________________________________

સદર મિલકતના પ્રોપર્ટી ટેક્સ બિલમાં જૂના માલિકના નામને બદલે મારું નામ દર્શાવવા નમ્ર વિનંતી છે. દસ્તાવેજ, ઇન્ડેક્સ-૨, ટેક્સ બિલની નકલ તથા આધારકાર્ડ સાથે જોડેલ છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "જન્મ / મરણ પ્રમાણપત્રમાં નામ કે તારીખ સુધારા અરજી":
"""પ્રતિ,
શ્રીમાન રજિસ્ટ્રાર સાહેબશ્રી (જન્મ-મરણ વિભાગ),
____________ મહાનગરપાલિકા, ________ ઝોન / વોર્ડ: ________

વિષય: જન્મ / મરણ રજિસ્ટરમાં નામ / જન્મ તારીખ / અટકનો સુધારો કરવા બાબત.
નોંધણી નંબર: ____________, નોંધણી તારીખ: __/__/____

સાહેબશ્રી,
સવિનય જણાવવાનું કે મારા/મારા બાળકના જન્મ/મરણ રજિસ્ટરમાં ભૂલથી સરકારી ચોપડે નામ/તારીખ નીચે મુજબ ખોટી લખાયેલ છે:

૧. હાલ ચોપડે દર્શાવેલ ખોટી વિગત: ____________________________________
૨. સાચી વિગત (જે સુધારીને લખવાની છે): ____________________________________

આ અંગેના આધાર-પુરાવા (સોગંદનામું/શાળા છોડ્યાનું પ્રમાણપત્ર/આધારકાર્ડ) જોડેલ છે. સાચી વિગત અન્વયે નવું પ્રમાણપત્ર કાઢી આપવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "ગેરકાયદે બાંધકામ કે દબાણ દૂર કરવા અરજી":
"""પ્રતિ,
શ્રીમાન એસ્ટેટ ઓફિસર સાહેબશ્રી / કમિશનર સાહેબશ્રી,
____________ મહાનગરપાલિકા, ________ ઝોન કચેરી,

વિષય: ગેરકાયદે બાંધકામ તથા જાહેર રસ્તા પરનું દબાણ દૂર કરવા બાબત.

સાહેબશ્રી,
સવિનય જણાવવાનું કે વિસ્તાર: ____________________________________________________ ખાતે સામાવાળા ____________________________________ દ્વારા વિના પરવાનગીએ ગેરકાયદેસર બાંધકામ / દબાણ કરવામાં આવેલ છે. 

આ બાંધકામના કારણે જાહેર જનતા તથા આસપાસના રહીશોને અડચણ ઊભી થાય છે. સદર સ્થળની તાત્કાલિક તપાસ કરી ગેરકાયદે દબાણ દૂર કરવા કાયદેસરની કાર્યવાહી કરવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "ડ્રેનેજ / ગટર / પાણીના નિકાલ અંગેની ફરિયાદ અરજી":
"""પ્રતિ,
શ્રીમાન સિટી ઇજનેર સાહેબશ્રી (વોટર વર્ક્સ & ડ્રેનેજ વિભાગ),
____________ મહાનગરપાલિકા, ________ ઝોન કચેરી,

વિષય: ગંદુ પાણી, ડ્રેનેજ લાઈન બ્લોકેજ તથા પીવાના પાણીની સમસ્યા બાબતે.

સાહેબશ્રી,
સવિનય જણાવવાનું કે અમારા વિસ્તાર: __________________________________________________ માં છેલ્લા ________ દિવસોથી ડ્રેનેજ લાઈન ઉભરાવાની / ગંદા પાણીની ગંભીર સમસ્યા ઊભી થઈ છે. 

આના કારણે મચ્છર અને રોગચાળો ફેલાવાની ભીતિ છે. સદર લાઈનનું સબળ સમારકામ કરી સમસ્યાનું કાયમી નિવારણ લાવવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "ગુમાસ્તા ધારા (Shop & Establishment) લાયસન્સ અરજી":
"""પ્રતિ,
શ્રીમાન લેબર ઓફિસર / ઇન્સપેક્ટર સાહેબશ્રી,
____________ મહાનગરપાલિકા, ________ ઝોન કચેરી,

વિષય: દુકાન / સંસ્થાની નોંધણી (Shop Establishment Registration) માટેની અરજી.

સાહેબશ્રી,
હું નીચે સહી કરનાર, સરનામું: ____________________________________________________ ખાતે પેઢી/દુકાન નામ: ____________________________________ થી વેપાર/ધંધો શરૂ કરવા માંગુ છું. 

નિયમાનુસાર ફોર્મ ભરી જરૂરી પુરાવા અને ફી જોડેલ છે. સદર દુકાનનું રજિસ્ટ્રેશન પ્રમાણપત્ર ઇશ્યૂ કરી આપવા વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",
    },

    "🏡 સેવાસદન / જમીન & મહેસૂલી": {
        "૭/૧૨ અને ૮-અ માં વારસાઈ નોંધ દાખલ અરજી":
"""પ્રતિ,
શ્રીમાન મામલતદાર સાહેબશ્રી,
તાલુકા સેવા સદન, ____________

વિષય: મોજે ગામ: ________, સર્વે/બ્લોક નંબર: ________, ખાતા નંબર: ________ માં વારસાઈ નોંધ દાખલ કરવા બાબત.

સાહેબશ્રી,
ઉપરોક્ત જમીનના મૂળ ખાતેદાર શ્રી ____________________________________ નું તારીખ: __/__/____ ના રોજ અવસાન થયેલ છે. તેઓના કાયદેસરના વારસદારોના નામો મહેસૂલી રેકોર્ડ (૭/૧૨ અને ૮-અ) માં દર્શાવવા આ અરજી કરેલ છે.

સાથે પેઢીનામું, મરણ દાખલો તથા વારસદારોના આધારકાર્ડ રજૂ કરેલ છે. વારસાઈ નોંધ પ્રમાણિત કરવા નમ્ર વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "જમીન માપણી / હદ નિશાન (DILR) અરજી":
"""પ્રતિ,
શ્રીમાન DILR સાહેબશ્રી (જિલ્લા નિરીક્ષક જમીન દફતર),
તાલુકા સેવા સદન / કલેક્ટર કચેરી, ____________

વિષય: મોજે ગામ: ________, સર્વે/બ્લોક નંબર: ________ ની જમીનની સ્થળ માપણી કરી હદ નક્કી કરવા બાબત.

સાહેબશ્રી,
ઉપરોક્ત સર્વે નંબરની જમીન મારી માલિકી અને કબજા ભોગવટાની છે. મારી જમીનની ચતુર્દિશાની સરહદો અને હદ નિશાન નક્કી કરવા સ્થળ માપણી કરાવવી જરૂરી છે. સરકારી ફી ભરી અરજી સ્વીકારી માપણી તારીખ ફાળવવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "જમીનની ટીપ્પણી / ગામનો નકશો મેળવવાની અરજી":
"""પ્રતિ,
શ્રીમાન મામલતદાર સાહેબશ્રી / DILR સાહેબશ્રી,
તાલુકા સેવા સદન, ____________

વિષય: જમીનની ટીપ્પણી (Tippan) તથા ગામના નકશાની પ્રમાણિત નકલ મેળવવા બાબત.
જમીનની વિગત: મોજે ગામ: ________, સર્વે/બ્લોક નંબર: ________.

સાહેબશ્રી,
ઉપરોક્ત દર્શાવેલ જમીનની ટીપ્પણી / FMB નકશાની સત્તાવાર પ્રમાણિત નકલની સરકારી કામકાજ અર્થે જરૂરિયાત હોય, નિયત ફી વસૂલ કરી નકલ પૂરી પાડવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "૬ નંબરની ફેરફાર નોંધ સામે વાંધા અરજી":
"""પ્રતિ,
શ્રીમાન મામલતદાર સાહેબશ્રી,
તાલુકા સેવા સદન, ____________

વિષય: ઇ-ધરા કચેરીની ફેરફાર નોંધ નંબર: ______ સામે કાયદેસરનો વાંધો નોંધાવવા બાબત.

સાહેબશ્રી,
સવિનય જણાવવાનું કે, મોજે ગામ: ________ ની જમીન સર્વે/બ્લોક નંબર: ________ માં સામાવાળા દ્વારા રજૂ કરેલ વિગતો ખોટી અને ગેરમાર્ગે દોરનારી છે. સદર નોંધ પ્રમાણિત ન કરવા અને વાંધા અરજી રેકર્ડ પર લઈ રદ્દ કરવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "જમીન બિન-ખેતી (N.A.) કરવા માટેની અરજી":
"""પ્રતિ,
શ્રીમાન કલેક્ટર સાહેબશ્રી / પ્રાંત અધિકારી સાહેબશ્રી,
જિલ્લા કલેક્ટર કચેરી, ____________

વિષય: મોજે ગામ: ________ ના સર્વે નંબર: ________ ની ખેતીની જમીન બિન-ખેતી (N.A.) કરવા બાબત.

સાહેબશ્રી,
અરજદારની માલિકીની ખેતીની જમીન સર્વે નંબર: ________ ને રહેણાંક / વાણિજ્ય / ઔદ્યોગિક હેતુ માટે બિન-ખેતીમાં રૂપાંતરિત કરવા અર્થે બિન-ખેતી પરવાનગી આપવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",
    },

    "📢 RTI & ફરિયાદ અરજીઓ": {
        "RTI અરજી (માહિતી અધિકાર અધિનિયમ ૨૦૦૫)":
"""પ્રતિ,
જાહેર માહિતી અધિકારીશ્રી,
કચેરીનું નામ: ____________________________________

વિષય: માહિતી અધિકાર અધિનિયમ, ૨૦૦૫ ની કલમ ૬(૧) હેઠળ માહિતી મેળવવા બાબત.

સાહેબશ્રી,
હું, અરજદાર, નીચે મુજબની બાબતો અંગેની પ્રમાણિત માહિતી/દસ્તાવેજો મેળવવા માગું છું:

૧. ____________________________________________________________________
૨. ____________________________________________________________________

નિયમાનુસાર RTI ફી રૂ. ૨૦/- (પોસ્ટલ ઓર્ડર/રોકડા) સામેલ છે. નિયત સમયમર્યાદામાં (૩૦ દિવસમાં) માહિતી આપવા નમ્ર વિનંતી છે.

અરજદારનું નામ: ____________________________________
સરનામું: ____________________________________________________
મોબાઈલ નંબર: __________________
સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "સ્વાગત પોર્ટલ / કલેક્ટરશ્રીને સીધી ફરિયાદ અરજી":
"""પ્રતિ,
શ્રીમાન જિલ્લા કલેક્ટર સાહેબશ્રી,
જિલ્લા સેવા સદન, ____________

વિષય: ________________________________________________ બાબતે લોક સુનાવણી / સ્વાગત અરજી.

સાહેબશ્રી,
સવિનય આપ સાહેબને જણાવવાનું કે, નીચે દર્શાવેલ વિગતે મારી વારંવારની રજૂઆતો છતાં સંબંધિત કચેરી દ્વારા કોઈ નિરાકરણ લાવવામાં આવેલ નથી:

૧. બનાવ/સમસ્યાની વિગત: ____________________________________________________________________
૨. અગાઉ આપેલ અરજી નંબર: __________________

આ બાબતે રૂબરૂ તપાસ કરાવી યોગ્ય ન્યાય આપવા અને જવાબદારો સામે કાર્યવાહી કરવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",
    },

    "📝 સામાન્ય / કસ્ટમ ફોર્મેટ": {
        "સામાન્ય અરજી ફોર્મેટ (કોઈપણ સરકારી કામ માટે)":
"""પ્રતિ,
શ્રીમાન ____________________ સાહેબશ્રી,
કચેરીનું નામ: ____________________________________
સ્થળ: ________________________

વિષય: ____________________________________________________________

સાહેબશ્રી,
સવિનય જણાવવાનું કે,

____________________________________________________________________________
____________________________________________________________________________
____________________________________________________________________________

આ અંગે ઘટતી કાર્યવાહી કરવા નમ્ર વિનંતી છે.

અરજદારનું નામ: ____________________________________
સરનામું: ____________________________________________________
મોબાઈલ નંબર: __________________
સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",
    }
}

# Flat lookup table
TEMPLATES = {}
for _cat, _docs in TEMPLATE_CATEGORIES.items():
    TEMPLATES.update(_docs)

# ── WORD GENERATOR ─────────────────────────────────────────────────
def generate_docx(court_name, selected_doc, case_number, applicant_name, opposite_party, doc_body):
    doc = Document()

    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.5)
    section.right_margin = Cm(2.5)

    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_head = p_head.add_run(f"પ્રતિ, {court_name}\n")
    run_head.bold = True
    run_head.font.size = Pt(14)

    if case_number:
        p_case = doc.add_paragraph()
        p_case.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_case = p_case.add_run(f"નંબર / રેકોર્ડ: {case_number}\n")
        run_case.font.size = Pt(12)

    p_party = doc.add_paragraph()
    p_party.paragraph_format.line_spacing = 1.5
    run_party = p_party.add_run(f"અરજદાર / વાદી: {applicant_name}\nસામાવાળા / પ્રતિવાદી: {opposite_party}\n")
    run_party.font.size = Pt(13)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(f"\n:: {selected_doc.split('(')[0]} ::\n")
    run_title.bold = True
    run_title.font.size = Pt(14)

    p_body = doc.add_paragraph()
    p_body.paragraph_format.line_spacing = 1.5
    run_body = p_body.add_run(doc_body)
    run_body.font.size = Pt(13)

    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(30)
    run_sign = p_sign.add_run(f"\n\n_____________________\n({applicant_name})\nઅરજદાર / વકીલની સહી")
    run_sign.font.size = Pt(13)

    target_stream = io.BytesIO()
    doc.save(target_stream)
    return target_stream.getvalue()

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝 નવો ડ્રાફ્ટ બનાવો", "📁 સાચવેલા દસ્તાવેજો & એડિટિંગ"])

with tab1:
    st.subheader("📝 ૧. અરજીનો પ્રકાર પસંદ કરો")

    if "doc_category" not in st.session_state:
        st.session_state.doc_category = list(TEMPLATE_CATEGORIES.keys())[0]

    cat_cols = st.columns(len(TEMPLATE_CATEGORIES), gap="small")
    for col, cat_name in zip(cat_cols, TEMPLATE_CATEGORIES.keys()):
        with col:
            st.markdown('<div class="cat-btn">', unsafe_allow_html=True)
            is_sel = st.session_state.doc_category == cat_name
            if st.button(cat_name, key=f"cat_{cat_name}", use_container_width=True,
                         type="primary" if is_sel else "secondary"):
                st.session_state.doc_category = cat_name
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    current_cat_docs = TEMPLATE_CATEGORIES[st.session_state.doc_category]
    doc_names = list(current_cat_docs.keys())

    if "selected_doc" not in st.session_state or st.session_state.selected_doc not in TEMPLATES:
        st.session_state.selected_doc = doc_names[0]
    if st.session_state.selected_doc not in doc_names:
        st.session_state.selected_doc = doc_names[0]

    st.write("")
    doc_cols = st.columns(2, gap="medium")
    for i, doc_name in enumerate(doc_names):
        with doc_cols[i % 2]:
            is_sel_doc = st.session_state.selected_doc == doc_name
            if st.button(doc_name, key=f"doc_{doc_name}", use_container_width=True,
                         type="primary" if is_sel_doc else "secondary"):
                st.session_state.selected_doc = doc_name
                st.rerun()

    selected_doc = st.session_state.selected_doc
    st.success(f"✅ પસંદ કરેલ અરજી: **{selected_doc}**")

    st.divider()

    col_input, col_preview = st.columns([1.1, 0.9], gap="large")

    with col_input:
        st.subheader("🖊️ વિગતો ભરો (અથવા ખાલી રાખો)")

        court_name = st.text_input("કચેરી / અદાલતનું નામ:", "શ્રીમાન પ્રિન્સિપાલ સિવિલ જજ સાહેબશ્રીની અદાલત / સુરત મહાનગરપાલિકા / મામલતદાર કચેરી")

        c1, c2 = st.columns(2)
        with c1:
            applicant_name = st.text_input("અરજદાર / વાદીનું નામ:", "વાદી / અરજદારનું નામ")
        with c2:
            opposite_party = st.text_input("સામાવાળા / પ્રતિવાદીનું નામ:", "પ્રતિવાદી / સામાવાળાનું નામ")

        case_number = st.text_input("દાવો / ખાતા / સર્વે નંબર:", "દાવો નંબર: ____ / ૨૦૨૬")

        st.subheader("📄 કાનૂની લખાણ (ડ્રાફ્ટિંગ)")
        doc_body = st.text_area("મુખ્ય અરજીનું લખાણ:", value=TEMPLATES[selected_doc], height=350, key=f"body_{selected_doc}")

        if st.session_state["logged_in"]:
            if st.button("💾 એકાઉન્ટમાં સેવ કરો", use_container_width=True, type="primary"):
                save_user_draft(
                    st.session_state["username"], selected_doc, court_name,
                    applicant_name, opposite_party, case_number, doc_body
                )
                st.success("✅ અરજી સફળતાપૂર્વક સેવ થઈ ગઈ!")
        else:
            st.info("ℹ️ દસ્તાવેજ સેવ કરવા માટે સાઇડબારમાંથી લોગિન કરો.")

    with col_preview:
        st.subheader("👁️ પ્રિવ્યૂ અને ડાઉનલોડ")

        docx_data = generate_docx(court_name, selected_doc, case_number, applicant_name, opposite_party, doc_body)

        st.download_button(
            label="📥 ૧. Word (.docx) ફાઇલ ડાઉનલોડ કરો",
            data=docx_data,
            file_name=f"{selected_doc.split(' ')[0]}_Application.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

        st.divider()
        st.subheader("📄 ૨. ડાયરેક્ટ PDF પ્રિન્ટ કરો")

        title_clean = selected_doc.split('(')[0]
        formatted_body = doc_body.replace('\n', '<br/>')

        print_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .btn {{
                    background-color: #1890ff;
                    color: white;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    cursor: pointer;
                    width: 100%;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <button class="btn" onclick="printDoc()">🖨️ PDF પ્રિન્ટ / સેવ કરો (Print as PDF)</button>
            <script>
                function printDoc() {{
                    var printWindow = window.open('', '', 'height=600,width=800');
                    printWindow.document.write('<html><head><title>Application Print</title>');
                    printWindow.document.write('<style>');
                    printWindow.document.write('@page {{ size: A4; margin-top: 20mm; margin-bottom: 20mm; margin-left: 35mm; margin-right: 25mm; }}');
                    printWindow.document.write('body {{ font-family: sans-serif; font-size: 15px; line-height: 1.8; color: #000; }}');
                    printWindow.document.write('.center {{ text-align: center; }}');
                    printWindow.document.write('.right {{ text-align: right; margin-top: 40px; }}');
                    printWindow.document.write('.title {{ text-align: center; font-size: 18px; font-weight: bold; margin: 20px 0; }}');
                    printWindow.document.write('</style></head><body>');

                    printWindow.document.write('<div><b>પ્રતિ,</b><br/>{court_name}</div><br/>');
                    printWindow.document.write('<div class="center"><b>{case_number}</b></div><br/>');
                    printWindow.document.write('<div><b>અરજદાર/વાદી:</b> {applicant_name}<br/><b>સામાવાળા/પ્રતિવાદી:</b> {opposite_party}</div>');
                    printWindow.document.write('<div class="title">:: {title_clean} ::</div>');
                    printWindow.document.write('<div>{formatted_body}</div>');
                    printWindow.document.write('<div class="right">_____________________<br/>({applicant_name})<br/><b>અરજદાર / વકીલની સહી</b></div>');

                    printWindow.document.write('</body></html>');
                    printWindow.document.close();
                    printWindow.focus();
                    setTimeout(function() {{ printWindow.print(); }}, 500);
                }}
            </script>
        </body>
        </html>
        """
        components.html(print_html, height=80)

with tab2:
    st.subheader("🔒 તમારા સેવ કરેલા ડ્રાફ્ટ")
    if not st.session_state["logged_in"]:
        st.warning("🔒 સાચવેલા દસ્તાવેજો જોવા માટે સાઇડબારમાંથી **લોગિન** કરો.")
    else:
        is_admin = (st.session_state["role"] == "admin")
        search_q = st.text_input("🔍 શોધો:", "")
        drafts = get_user_drafts(st.session_state["username"], search_query=search_q, is_admin=is_admin)

        if not drafts:
            st.info("કોઈ સાચવેલા ડ્રાફ્ટ મળ્યા નથી.")
        else:
            for d in drafts:
                draft_id, user_owner, d_type, app_name, c_time, c_name, opp_p, c_num, d_body = d
                with st.expander(f"📜 {d_type} | અરજદાર: {app_name} | ({c_time})"):
                    st.write(f"**યુઝર:** {user_owner}")
                    edit_c_name = st.text_input("કચેરી:", value=c_name, key=f"cn_{draft_id}")

                    ec1, ec2 = st.columns(2)
                    with ec1:
                        edit_app_name = st.text_input("અરજદાર:", value=app_name, key=f"an_{draft_id}")
                    with ec2:
                        edit_opp_p = st.text_input("સામાવાળા:", value=opp_p, key=f"op_{draft_id}")

                    edit_c_num = st.text_input("રેકોર્ડ નંબર:", value=c_num, key=f"cnum_{draft_id}")
                    edit_d_body = st.text_area("લખાણ:", value=d_body, height=200, key=f"text_{draft_id}")

                    col_save_btn, col_dl_btn, col_del_btn = st.columns([1, 1, 1])

                    with col_save_btn:
                        if st.button("✏️ સુધારા સેવ કરો", key=f"up_{draft_id}", type="primary"):
                            update_update_user_draft(draft_id, edit_c_name, edit_app_name, edit_opp_p, edit_c_num, edit_d_body)
                            st.success("સુધારો સેવ થઈ ગયો!")
                            st.rerun()

                    with col_dl_btn:
                        saved_docx = generate_docx(edit_c_name, d_type, edit_c_num, edit_app_name, edit_opp_p, edit_d_body)
                        st.download_button(
                            label="📥 Word ડાઉનલોડ",
                            data=saved_docx,
                            file_name=f"Saved_{d_type.split(' ')[0]}_{draft_id}.docx",
                            key=f"dl_{draft_id}"
                        )

                    with col_del_btn:
                        if st.button("🗑️ ડિલીટ કરો", key=f"del_{draft_id}"):
                            delete_user_draft(draft_id, st.session_state["username"], is_admin=is_admin)
                            st.success("દસ્તાવેજ ડિલીટ થઈ ગયો!")
                            st.rerun()
