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
    page_title="ગુજરાત લીગલ & AMC સેવા પોર્ટલ",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117 !important;
        color: #ffffff !important;
        max-width: 100vw;
        overflow-x: hidden !important;
    }
    h1, h2, h3, h4, h5, h6, span, label, p {
        color: #ffffff !important;
    }
    .stTextInput input, .stTextArea textarea {
        color: #ffffff !important;
        background-color: #1e222d !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0px 0px;
        padding: 10px 20px;
        background-color: #1e222d;
        color: #ffffff !important;
    }
    div[data-testid="stButton"] > button {
        width: 100%;
        min-height: 56px;
        font-size: 15px !important;
        white-space: normal;
        line-height: 1.3;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #16a34a !important;
        border: 2px solid #4ade80 !important;
        color: #ffffff !important;
    }
    .cat-btn button {
        min-height: 46px !important;
        font-size: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── DATABASE SETUP ─────────────────────────────────────────────────
DB_FILE = "legal_drafts_secure_v7.db"

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
    st.title("🏛️ સેવા સદન & AMC સેન્ટર")

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

    with st.expander("🌐 મહત્વપૂર્ણ સરકારી લીંક"):
        st.link_button("🏢 AMC અમદાવાદ પોર્ટલ", "https://ahmedabadcity.gov.in/", use_container_width=True)
        st.link_button("🌐 AnyRoR (૭/૧૨, ૮-અ)", "https://anyror.gujarat.gov.in/", use_container_width=True)
        st.link_button("🏛️ i-ORA (N.A., જમીન માપણી)", "https://iora.gujarat.gov.in/", use_container_width=True)
        st.link_button("📜 Garvi 2.0 (દસ્તાવેજ નોંધણી)", "https://garvi.gujarat.gov.in/", use_container_width=True)
        st.link_button("📑 ઇ-ધરા (૬ નંબર નોંધો)", "https://edhara.gujarat.gov.in/", use_container_width=True)
        st.link_button("📋 Digital Gujarat", "https://www.digitalgujarat.gov.in", use_container_width=True)
        st.link_button("📢 SWAGAT Online", "https://swagat.gujarat.gov.in/", use_container_width=True)

# ── HEADER ─────────────────────────────────────────────────────────
st.title("🏛️ સેવા સદન અને મહાનગરપાલિકા (AMC) અરજી સેન્ટર 🏛️")
st.caption("📝 જમીન, મિલકત, ટેક્સ અને AMC ના તમામ કામો માટે મુદ્દાસર અરજી ડ્રાફ્ટિંગ સોફ્ટવેર")
st.divider()

# ── TEMPLATES (LAND & AMC CATEGORIZED) ─────────────────────────────
TEMPLATE_CATEGORIES = {
    "🏢 AMC / મ્યુનિસિપલ કચેરી": {
        "AMC પ્રોપર્ટી ટેક્સ નામ ટ્રાન્સફર અરજી":
"""પ્રતિ,
શ્રીમાન ટેક્સ એસેસર સાહેબશ્રી,
અમદાવાદ મહાનગરપાલિકા (AMC), ________ ઝોન / વોર્ડ: ________

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
અમદાવાદ મહાનગરપાલિકા (AMC), ________ ઝોન / વોર્ડ: ________

વિષય: જન્મ / મરણ રજિસ્ટરમાં નામ / જન્મ તારીખ / અટકનો સુધારો કરવા બાબત.
નોંધણી નંબર: ____________, નોંધણી તારીખ: __/__/____

સાહેબશ્રી,
સવિનય જણાવવાનું કે મારા/મારા બાળકના જન્મ/મરણ રજિસ્ટરમાં ભૂલથી સરકારી ચોપડે નામ/તારીખ નીચે મુજબ ખોટી લખાયેલ છે:

૧. હાલ ચોપડે દર્શાવેલ ખોટી વિગત: ____________________________________
૨. સાચી વિગત (જે સુધારીને લખવાની છે): ____________________________________

આ અંગેના આધાર-પુરાવા (સોગંદનામું/શાળા છોડ્યાનું પ્રમાણપત્ર/આધારકાર્ડ) જોડેલ છે. સાચી વિગત અન્વયે નવું પ્રમાણપત્ર કાઢી આપવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "AMC ગેરકાયદે બાંધકામ કે દબાણ દૂર કરવા અરજી":
"""પ્રતિ,
શ્રીમાન એસ્ટેટ ઓફિસર સાહેબશ્રી / કમિશનર સાહેબશ્રી,
અમદાવાદ મહાનગરપાલિકા (AMC), ________ ઝોન કચેરી,

વિષય: ગેરકાયદે બાંધકામ તથા જાહેર રસ્તા પરનું દબાણ દૂર કરવા બાબત.

સાહેબશ્રી,
સવિનય જણાવવાનું કે વિસ્તાર: ____________________________________________________ ખાતે સામાવાળા ____________________________________ દ્વારા વિના પરવાનગીએ ગેરકાયદેસર બાંધકામ / દબાણ કરવામાં આવેલ છે. 

આ બાંધકામના કારણે જાહેર જનતા તથા આસપાસના રહીશોને અડચણ ઊભી થાય છે. સદર સ્થળની તાત્કાલિક તપાસ કરી ગેરકાયદે દબાણ દૂર કરવા કાયદેસરની કાર્યવાહી કરવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "AMC ડ્રેનેજ / ગટર / પાણીના નિકાલ અંગેની ફરિયાદ અરજી":
"""પ્રતિ,
શ્રીમાન સિટી ઇજનેર સાહેબશ્રી (વોટર વર્ક્સ & ડ્રેનેજ વિભાગ),
અમદાવાદ મહાનગરપાલિકા (AMC), ________ ઝોન કચેરી,

વિષય: ગંદુ પાણી, ડ્રેનેજ લાઈન બ્લોકેજ તથા પીવાના પાણીની સમસ્યા બાબતે.

સાહેબશ્રી,
સવિનય જણાવવાનું કે અમારા વિસ્તાર: __________________________________________________ માં છેલ્લા ________ દિવસોથી ડ્રેનેજ લાઈન ઉભરાવાની / ગંદા પાણીની ગંભીર સમસ્યા ઊભી થઈ છે. 

આના કારણે મચ્છર અને રોગચાળો ફેલાવાની ભીતિ છે. સદર લાઈનનું સબળ સમારકામ કરી સમસ્યાનું કાયમી નિવારણ લાવવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

        "ગુમાસ્તા ધારા (Shop & Establishment) લાયસન્સ અરજી":
"""પ્રતિ,
શ્રીમાન લેબર ઓફિસર / ઇન્સપેક્ટર સાહેબશ્રી,
અમદાવાદ મહાનગરપાલિકા (AMC), ________ ઝોન કચેરી,

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

# Flat lookup table for background templates
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
    run_party = p_party.add_run(f"અરજદાર / પક્ષકાર: {applicant_name}\nસામાવાળા / વિરુદ્ધ: {opposite_party}\n")
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
    run_sign = p_sign.add_run(f"\n\n_____________________\n({applicant_name})\nઅરજદારની સહી")
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

        court_name = st.text_input("કચેરી / ઓથોરિટીનું નામ:", "મામલતદાર કચેરી / AMC ઝોન કચેરી")

        c1, c2 = st.columns(2)
        with c1:
            applicant_name = st.text_input("અરજદારનું નામ:", "અરજદારનું નામ")
        with c2:
            opposite_party = st.text_input("સામાવાળાનું નામ (જો હોય તો):", "સામાવાળાનું નામ / કચેરી")

        case_number = st.text_input("ખાતા / સર્વે / ટેનેમેન્ટ નંબર:", "ટેનેમેન્ટ/સર્વે નંબર: ________")

        st.subheader("📄 કાનૂની લખાણ (ડ્રાફ્ટિંગ)")
        doc_body = st.text_area("મુખ્ય અરજીનું લખાણ:", value=TEMPLATES[selected_doc], height=320, key=f"body_{selected_doc}")

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
                    background-color: #ff4b4b;
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
                    printWindow.document.write('<div><b>અરજદાર:</b> {applicant_name}<br/><b>સામાવાળા:</b> {opposite_party}</div>');
                    printWindow.document.write('<div class="title">:: {title_clean} ::</div>');
                    printWindow.document.write('<div>{formatted_body}</div>');
                    printWindow.document.write('<div class="right">_____________________<br/>({applicant_name})<br/><b>અરજદારની સહી</b></div>');

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
                            update_user_draft(draft_id, edit_c_name, edit_app_name, edit_opp_p, edit_c_num, edit_d_body)
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
