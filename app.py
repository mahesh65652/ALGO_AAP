import streamlit as st
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import sqlite3
import hashlib
import streamlit.components.v1 as components

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="ગુજરાત લીગલ પોર્ટલ",
    page_icon="⚖️",
    layout="wide"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main-title { color: #1e222d; text-align: center; font-weight: bold; }
    .sidebar .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ── DATABASE & LOGIC ────────────────────────────────────────────────
DB_FILE = "legal_drafts_v6.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT, role TEXT)")
        c.execute("""
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT, doc_type TEXT, court_name TEXT, 
                applicant_name TEXT, opposite_party TEXT, case_number TEXT, doc_body TEXT
            )
        """)
init_db()

# (સુરક્ષા માટે પાસવર્ડ અને અન્ય ફંક્શન્સ અહીં તમારા જૂના કોડ મુજબ જ રહેશે, 
# મેં અહીં ટૂંકમાં દર્શાવ્યા છે)
def hash_password(p): return hashlib.sha256(f"{p}_salt".encode()).hexdigest()

# ── TEMPLATES (તમારા સ્ક્રીનશોટ મુજબના તમામ ડ્રાફ્ટ) ──────────────────
TEMPLATES = {
    "જમીન / મકાન બાનાખત કરારપત્ર (Banakhat)": "આથી અમો વેચાણ રાખનાર અને વેચાણ આપનાર પક્ષકારો વચ્ચે જમીન/મકાનના સોદા અંગેનો બાનાખત કરાર કરવામાં આવે છે...",
    "મકાન / દુકાન ભાડા કરારપત્ર (Rent Agreement)": "આથી મકાન માલિક અને ભાડુઆત વચ્ચે રહેણાંક/વ્યાપારી હેતુ માટે ભાડા કરારની શરતો નક્કી કરવામાં આવે છે...",
    "જમીન ટાઈટલ ક્લીયર અને ૨૫% સફળતા ફી કરારપત્ર": "સદર જમીનના ટાઈટલ ક્લીયરન્સની કામગીરી અને તે બદલની ફીની શરતોનો કરાર...",
    "વ્યાજે નાણા આપવા અને ગીરવે લખાણનો કરાર": "નાણા લેનાર અને દેવાદાર વચ્ચેની નાણાકીય વ્યવહારની શરતો...",
    "ટીપ્પણી / ગામનો નકશો મેળવવાની અરજી": "DILR કચેરીમાં ટીપ્પણી અને નકશા મેળવવા બાબતની અરજી...",
    "જમીન માપણી / પુનઃ માપણી અરજી": "સીમાડા નક્કી કરવા અને સ્થળ માપણી કરવા બાબતની અરજી...",
    "૬ નંબરની નોંધ સામે વાંધા અરજી": "ઈ-ધરા રેકોર્ડમાં ખોટી નોંધ સામે વાંધો નોંધાવવા બાબત...",
    "બિન-ખેતી (N.A.) પરવાનગી અરજી": "ખેતીની જમીનને બિન-ખેતીમાં ફેરવવા અંગેની અરજી...",
    "વાંધા અરજી (Objection Application)": "કાયદાકીય નોટિસ કે કાર્યવાહી સામે વાંધો રજૂ કરવા બાબત..."
}

# ── MAIN INTERFACE ─────────────────────────────────────────────────
st.markdown("<h2 class='main-title'>🏛️ ગુજરાત લીગલ પોર્ટલ 🏛️</h2>", unsafe_allow_html=True)
st.caption("⚖️ ગુજરાત હાઇકોર્ટ & મહેસૂલી ડ્રાફ્ટિંગ પોર્ટલ | A4 સાઇઝ અને સત્તાવાર કાનૂની ફોર્મેટિંગ મુજબ | Updated v6.0")
st.divider()

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📝 દસ્તાવેજ પસંદ કરો")
    selected_doc = st.selectbox("તમારો ડ્રાફ્ટ પસંદ કરો:", list(TEMPLATES.keys()))
    
    court_name = st.text_input("કોર્ટ / કચેરીનું નામ:", "મામલતદાર કચેરી / DILR કચેરી")
    applicant = st.text_input("અરજદારનું નામ:")
    opposite = st.text_input("સામાવાળાનું નામ:")
    case_num = st.text_input("કેસ / સર્વે નંબર:")
    
    doc_body = st.text_area("મુખ્ય લખાણ:", value=TEMPLATES[selected_doc], height=300)

with col_right:
    st.subheader("👁️ પ્રિવ્યૂ અને ડાઉનલોડ")
    # Generate Docx logic here (using your existing generate_docx function)
    st.info("તમે ડાબી બાજુ વિગતો ભરીને નીચેથી ફાઈલ ડાઉનલોડ કરી શકશો.")
    
    if st.button("📥 Word (.docx) ફાઇલ ડાઉનલોડ કરો", use_container_width=True):
        st.success("ડ્રાફ્ટ તૈયાર છે! (ડાઉનલોડ લોજિક અહીં કામ કરશે)")

# ── SIDEBAR LINKS ──────────────────────────────────────────────────
with st.sidebar:
    st.subheader("🌐 ક્વિક લિંક્સ")
    st.link_button("AnyRoR (૭/૧૨, ૮-અ)", "https://anyror.gujarat.gov.in/")
    st.link_button("i-ORA (N.A. જમીન)", "https://iora.gujarat.gov.in/")
    st.link_button("Garvi 2.0 (ઇન્ડેક્સ-૨)", "https://garvi.gujarat.gov.in/")
