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
    page_title="ગુજરાત હાઇકોર્ટ & મહેસૂલી પોર્ટલ (Legal Software)",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    .stTabs [data-baseweb="tab"] { border-radius: 6px 6px 0px 0px; padding: 10px 20px; background-color: #1e222d; }
    </style>
""", unsafe_allow_html=True)

# ── DATABASE SETUP ─────────────────────────────────────────────────
DB_FILE = "legal_drafts_secure_v3.db"

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
    st.title("⚖️ લીગલ સોફ્ટવેર")
    
    with st.expander("🔐 સાઇન-ઇન / એકાઉન્ટ", expanded=not st.session_state["logged_in"]):
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

    with st.expander("🗺️ જમીન & મહેસૂલી પોર્ટલ્સ"):
        st.link_button("🌐 AnyRoR (૭/૧૨, ૮-અ)", "https://anyror.gujarat.gov.in/", use_container_width=True)
        st.link_button("🏛️ i-ORA (N.A., જમીન માપણી)", "https://iora.gujarat.gov.in/", use_container_width=True)
        st.link_button("📜 Garvi 2.0 (ઇન્ડેક્સ-૨)", "https://garvi.gujarat.gov.in/", use_container_width=True)
        st.link_button("📑 ઇ-ધરા (૬ નંબર નોંધો)", "https://edhara.gujarat.gov.in/", use_container_width=True)
        st.link_button("💳 Cyber Treasury", "https://www.treasury.gujarat.gov.in/", use_container_width=True)

    with st.expander("⚖️ ઈ-કોર્ટ્સ & સરકારી પોર્ટલ"):
        st.link_button("⚖️ e-Courts India", "https://services.ecourts.gov.in/", use_container_width=True)
        st.link_button("🏛️ ગુજરાત હાઇકોર્ટ", "https://gujarathighcourt.nic.in/", use_container_width=True)
        st.link_button("📢 સરકાર વિજ્ઞાપન પોર્ટલ (Gudip)", "https://gudip.gujarat.gov.in/", use_container_width=True)
        st.link_button("📋 Digital Gujarat", "https://www.digitalgujarat.gov.in", use_container_width=True)
        st.link_button("🌾 i-Khedut પોર્ટલ", "https://ikhedut.gujarat.gov.in/", use_container_width=True)
        st.link_button("📢 SWAGAT Online", "https://swagat.gujarat.gov.in/", use_container_width=True)

# ── HEADER ─────────────────────────────────────────────────────────
st.title("⚖️ ગુજરાત હાઇકોર્ટ & મહેસૂલી લીગલ ડ્રાફ્ટિંગ સોફ્ટવેર")
st.caption("🔒 પ્રાઇવેટ એક્સેસ | A4 સાઇઝ અને ગુજરાત હાઇકોર્ટના સત્તાવાર ફોર્મેટિંગ મુજબ")
st.divider()

# ── TEMPLATES ──────────────────────────────────────────────────────
TEMPLATES = {
    "જમીન ટાઇટલ ક્લીયર અને ૨૫% સફળતા ફી કરારપત્રક (Land Title Clearance Agreement)":
"""જમીન કામગીરી તથા ૨૫% મહેનતાણા ફી અંગેનો સમજૂતી કરારપત્રક

આજ રોજ તારીખ: __/__/૨૦૨૬ ના દિવસે લખાણ કરી આપનાર:

પ્રથમ પક્ષકાર (જમીન માલિક): ________________________________________
સરનામું: ___________________________________________________________

બીજા પક્ષકાર (કામગીરી કરનાર કન્સલ્ટન્ટ/એજન્ટ): _____________________
સરનામું: ___________________________________________________________

આથી અમો બંને પક્ષકારોએ આપસી સંમતિથી નીચે મુજબની શરતોએ આ કરારપત્રક કરેલ છે:

૧. જમીનની વિગત: મોજે ગામ: ____________, તાલુકો: ____________, જિલ્લો: ____________ માં આવેલ સર્વે/બ્લોક નંબર: ____________, ખાતા નંબર: ____________ વાળી જમીન પ્રથમ પક્ષકારની માલિકી/કબજાની છે.

૨. કામની વિગત: સદર જમીન પર રહેલા તમામ કાનૂની/મહેસુલી વિવાદો, ફેરફાર નોંધોના વાંધા, અથવા ટાઇટલ સંબંધિત અટકાયતી કામગીરી પૂર્ણ કરી જમીનનું ટાઇટલ સંપૂર્ણપણે કલીયર (Clear) કરી આપવાનું કામ બીજા પક્ષકારે સોંપવામાં આવેલ છે.

૩. મહેનતાણા (ફી) ની શરત: સદર કામગીરી સફળતાપૂર્વક પૂર્ણ થઈ જમીનનું ટાઇટલ ક્લિયર થઈ જાય, ત્યાર બાદ પ્રથમ પક્ષકારે બીજા પક્ષકારને તેમની મહેનત/સેવા બદલ સદર જમીનની નક્કી કરેલ કિંમત અથવા વેચાણ રકમના ૨૫% (પચીસ ટકા) હિસ્સો / રકમ પેટે રૂ. ________/- ચૂકવવાના રહેશે.

૪. ચૂકવણીની જવાબદારી: કામગીરી સફળતાપૂર્વક પૂર્ણ થયા બાદ પ્રથમ પક્ષકાર બીજા પક્ષકારને આ ૨૫% રકમ આપવાની ના પાડી શકશે નહીં અને સમયસર ચૂકવણી કરવા માટે કાયદેસર રીતે બંધાયેલા રહેશે.

૫. આ કરાર બંને પક્ષકારોએ વાંચી, સમજી, વિચારીને કોઈના પણ દબાણ વગર પોતાની રાજીખુશીથી સહી કરી આપેલ છે.

સાક્ષીઓ:
૧. _____________________ (સહી)
૨. _____________________ (સહી)

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "વ્યાજે નાણા આપવા અને ગીરવે લખાણનો કરાર (Money Lending & Pledge Agreement)":
"""ઉછીના નાણાં લીધા અંગેનું ગેરંટી તથા ગીરવે લખાણ કરારપત્રક

નાણા આપનાર (પ્રથમ પક્ષકાર/લેણદાર): ____________
નાણા લેનાર (બીજો પક્ષકાર/દેવાદાર): ____________

આજ રોજ તારીખ: __/__/૨૦૨૬ ના દિવસે અમો કરાર કરનાર બીજો પક્ષકાર (નાણા લેનાર) આથી લખાણ કરી આપું છું કે:

૧. અમોને મારા અંગત/ધંધાકીય કામ અર્થે નાણાંની જરૂરિયાત હોવાથી અમોએ પ્રથમ પક્ષકાર પાસેથી રૂ. ________/- (અક્ષરે રૂ. ____________________________) વ્યાજે/ઉછીના રોકડા/ચેક/UPI મારફતે મેળવેલ છે.

૨. આ રકમ ઉપર માસિક ____% (અથવા વાર્ષિક ____%) લેખે દર મહિને નિયમિત વ્યાજ ચૂકવવાનું નક્કી કરેલ છે.

૩. ગેરંટી અને સિક્યુરિટી પેટે અમોએ નીચે મુજબની વસ્તુ/મિલકત પ્રથમ પક્ષકાર પાસે ગીરવે/કબજામાં રાખેલ છે:
   - ગીરવે મુકેલ વસ્તુ/મિલકતની વિગત: _____________________________________
   - વસ્તુનું વજન / દસ્તાવેજ વિગત / વાહન નંબર: _____________________________________
   - સિક્યુરિટી ચેક નંબર (જો હોય તો): _____________________________________

૪. જો અમો કરાર મુજબ સમયસર વ્યાજ કે મૂળ રકમ પરત કરવામાં નિષ્ફળ જઈશું, તો પ્રથમ પક્ષકારને ગીરવે મુકેલ વસ્તુ/મિલકત દ્વારા પોતાની લેણી રકમ વસૂલ કરવાનો અથવા કાયદેસરની કાર્યવાહી કરવાનો પૂર્ણ અધિકાર રહેશે.

૫. આ કરાર અમોએ કોઈપણ જાતના દાબ-દબાણ વગર, સાજા-નરવા મગજે, વાંચી-સમજીને સહી કરી આપેલ છે.

સાક્ષીઓ:
૧. _____________________ (સહી)
૨. _____________________ (સહી)

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "ટીપ્પણી / ગામનો નકશો મેળવવાની અરજી (Application for Tippan & Map)": 
"""શ્રીમાન DILR સાહેબશ્રી / મામલતદાર સાહેબશ્રી,
તાલુકા સેવા સદન, ____________

વિષય: જમીનની ટીપ્પણી (Tippan) તથા ગામનો નકશો મેળવવા બાબત.
જમીનની વિગત: મોજે ગામ: ________, સર્વે/બ્લોક નંબર: ________, ખાતા નંબર: ________.

સાહેબશ્રી,
ઉપરોક્ત દર્શાવેલ જમીન મારી સ્વતંત્ર/સંયુક્ત માલિકી અને કબજા ભોગવટાની આવેલ છે. સદર જમીનની હદ, સીમાડા અને માપણીની ખાતરી કરવા માટે મારે કચેરીના રેકોર્ડ પરથી ટીપ્પણી / FMB નકશાની પંચાયત/સરકારી પ્રમાણિત નકલની જરૂરિયાત છે.

આથી નિયમ અનુસારની સત્તાવાર ફી વસૂલ લઈ સદર સર્વે નંબરની ટીપ્પણી તથા નકશાની પ્રમાણિત નકલ આપવા વિનંતી છે.

સાથે સામેલ:
૧. ૭/૧૨ અને ૮-અ ની તાજી નકલ.
૨. અરજદારના આધાર કાર્ડની નકલ.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "જમીન માપણી / પુનઃ માપણી અરજી (Re-survey / Land Measurement)": 
"""શ્રીમાન DILR સાહેબશ્રી (જિલ્લા નિરીક્ષક જમીન દફતર),
કચેરી સરનામું: ____________

વિષય: મોજે ગામ: ________ ના સર્વે/બ્લોક નંબર: ________ ની જમીન માપણી કરવા બાબત.

સવિનય જણાવવાનું કે,
૧. ઉપરોક્ત સર્વે નંબરની જમીન અરજદારની માલિકીની છે.
૨. સદર જમીનના સીમાડા અને શેઢા-પાળાઓની ચોક્કસ હદ નક્કી કરવા તથા શેજમીન ચકાસવા માટે સ્થળ પર માપણી કરાવવી જરૂરી છે.
૩. આથી સદર જમીનની સ્થળ માપણી કરી માપણી સીટ/નકશો તૈયાર કરવા માટે નિયમાનુસારની માપણી ફી ભરી અરજી સ્વીકારવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "૬ નંબરની નોંધ સામે વાંધા અરજી (Objection to Revenue Entry No. 6)": 
"""શ્રીમાન મામલતદાર સાહેબશ્રી,
તાલુકા સેવા સદન, ____________

વિષય: ઇ-ધરા કચેરીની ફેરફાર નોંધ નંબર: ______ સામે વાંધો નોંધાવવા બાબત.

સવિનય જણાવવાનું કે,
૧. મોજે ગામ: ________ ની જમીન સર્વે/બ્લોક નંબર: ________ માં સામાવાળાએ ખોટી રીતે કે હકીકત છુપાવીને ફેરફાર નોંધ નંબર: ______ પડાવેલ છે.
૨. સદર જમીનમાં અરજદારનો કાયદેસરનો હક્ક, હિસ્સો અને માલિકી આવેલ છે, જે અંગે અરજદારને કોઈ પૂર્વ નોટિસ આપ્યા વગર આ નોંધ પાડવામાં આવેલ છે.
૩. આથી સદર નોંધ પ્રમાણિત (Certify) ન કરવા અને કેસ વિવાદે લઈ અરજદારને સાંભળીને સદર નોંધ રદ્દ કરવાનો હુકમ કરવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "બિન-ખેતી (N.A.) પરવાનગી અરજી (Non-Agricultural Application)": 
"""શ્રીમાન કલેક્ટર સાહેબશ્રી / પ્રાંત અધિકારી સાહેબશ્રી,
જિલ્લા કલેક્ટર કચેરી, ____________

વિષય: મોજે ગામ: ________ ના સર્વે નંબર: ________ ની જમીન બિન-ખેતી (N.A.) કરવા બાબત.

સાહેબશ્રી,
અરજદારની માલિકીની મોજે ગામ: ________ ની ખેતીની જમીન જેનો સર્વે/બ્લોક નંબર: ________ છે, તેને રહેણાંક / વાણિજ્ય / ઔદ્યોગિક હેતુ માટે બિન-ખેતીમાં રૂપાંતરિત કરવાની જરૂરિયાત ઊભી થયેલ છે.

સદર જમીન તમામ બોજાઓથી મુક્ત છે અને તેના તમામ મહેસૂલી રેકોર્ડ (૭/૧૨, ૮-અ, ૬ નંબર નોંધો, ટીપ્પણી) આ સાથે સામેલ છે. નિયમ મુજબનો એન.એ. પ્રીમિયમ/ચાર્જ વસૂલ કરી બિન-ખેતી પરવાનગી આપવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "વાંધા અરજી (Objection Application)": 
"""અરજદારશ્રી તરફથી નીચે મુજબની વાંધા અરજી સવિનય રજૂ કરવામાં આવે છે:

૧. એ કે, સામાવાળા તરફથી કરવામાં આવેલ રજૂઆત/અરજી કાયદાકીય રીતે ટકી શકે તેમ નથી અને તથ્ય વગરની છે.
૨. એ કે, સદર બાબતમાં અરજદારના કાયદેસરના હક્ક, હિસ્સા અને હિત રહેલા છે, જેને ધ્યાને લીધા વગર સામાવાળાએ એકતરફી કાર્યવાહી કરવાનો પ્રયાસ કરેલ છે.
૩. એ કે, આથી નામદાર કોર્ટ/ઓથોરિટીને નમ્ર વિનંતી છે કે સામાવાળાની અરજી રદ્દ કરવી અને અરજદારના વાંધાઓ ધ્યાને લઈ ન્યાયી હુકમ કરવો.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "સામાન્ય અરજી (General Application)": 
"""આદરણીય સાહેબશ્રી,

વિષય: __________________________________________________ અંગે.

સવિનય જણાવવાનું કે, ઉપર જણાવેલ વિષય અન્વયે નીચે મુજબ રજૂઆત કરવામાં આવે છે:

૧. ____________________________________________________________________
૨. ____________________________________________________________________

આથી સાહેબશ્રીને નમ્ર વિનંતી છે કે સદર બાબતે યોગ્ય ત્વરિત કાર્યવાહી કરવા કૃપા કરશો.

આપનો વિનમ્ર,
(અરજદારની સહી)"""
}

# ── WORD GENERATOR ─────────────────────────────────────────────────
def generate_docx(court_name, selected_doc, case_number, applicant_name, opposite_party, doc_body):
    doc = Document()
    
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(4.0)
    section.right_margin = Cm(4.0)
    
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_head = p_head.add_run(f"મેહરબાન {court_name} માં\n")
    run_head.bold = True
    run_head.font.size = Pt(14)
    
    if case_number:
        p_case = doc.add_paragraph()
        p_case.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_case = p_case.add_run(f"{case_number}\n")
        run_case.font.size = Pt(12)
    
    p_party = doc.add_paragraph()
    p_party.paragraph_format.line_spacing = 1.5
    run_party = p_party.add_run(f"અરજદાર / પ્રથમ પક્ષકાર: {applicant_name}\nવિરુદ્ધ / અને\nસામાવાળા / બીજો પક્ષકાર: {opposite_party}\n")
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
    run_sign = p_sign.add_run(f"\n\n_____________________\n({applicant_name})\nઅરજદાર / પક્ષકારની સહી")
    run_sign.font.size = Pt(13)
    
    target_stream = io.BytesIO()
    doc.save(target_stream)
    return target_stream.getvalue()

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝 નવો ડ્રાફ્ટ બનાવો", "📁 સાચવેલા દસ્તાવેજો & એડિટિંગ"])

with tab1:
    col_input, col_preview = st.columns([1.1, 0.9], gap="large")

    with col_input:
        st.subheader("📝 વિગતો પસંદ કરો અને ભરો")
        
        selected_doc = st.selectbox("દસ્તાવેજ / અરજીનો પ્રકાર પસંદ કરો:", list(TEMPLATES.keys()))
        court_name = st.text_input("કોર્ટ / કચેરી / ઓથોરિટીનું નામ:", "DILR કચેરી / મામલતદાર કચેરી / ગુજરાત હાઇકોર્ટ")
        
        c1, c2 = st.columns(2)
        with c1:
            applicant_name = st.text_input("અરજદાર / નાણા આપનારનું નામ:", "મહેશભાઈ વિનોદભાઇ રામાવત")
        with c2:
            opposite_party = st.text_input("સામાવાળા / નાણા લેનારનું નામ:", "સામાવાળાનું નામ")
            
        case_number = st.text_input("કેસ / નોટિસ / રેકોર્ડ નંબર:", "સર્વે/કરાર નંબર: ૧૨૩/૧")
        
        st.subheader("📄 કાનૂની લખાણ (ડ્રાફ્ટિંગ)")
        doc_body = st.text_area("મુખ્ય લખાણ:", value=TEMPLATES[selected_doc], height=280)

        if st.session_state["logged_in"]:
            if st.button("💾 પ્રાઇવેટ એકાઉન્ટમાં સેવ કરો", use_container_width=True, type="primary"):
                save_user_draft(
                    st.session_state["username"], selected_doc, court_name, 
                    applicant_name, opposite_party, case_number, doc_body
                )
                st.success("✅ દસ્તાવેજ સફળતાપૂર્વક સેવ થઈ ગયો!")
        else:
            st.info("ℹ️ દસ્તાવેજ સેવ કરવા માટે ડાબી બાજુથી લોગિન કરો.")

    with col_preview:
        st.subheader("👁️ પ્રિવ્યૂ અને ડાઉનલોડ")
        
        docx_data = generate_docx(court_name, selected_doc, case_number, applicant_name, opposite_party, doc_body)
        
        st.download_button(
            label="📥 ૧. Word (.docx) ફાઇલ ડાઉનલોડ કરો",
            data=docx_data,
            file_name=f"{selected_doc.split(' ')[0]}_Document.docx",
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
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    width: 100%;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <button class="btn" onclick="printDoc()">🖨️ આ દસ્તાવેજ PDF તરીકે સેવ કરો (Print / Save as PDF)</button>
            <script>
                function printDoc() {{
                    var printWindow = window.open('', '', 'height=600,width=800');
                    printWindow.document.write('<html><head><title>Legal Document</title>');
                    printWindow.document.write('<style>');
                    printWindow.document.write('@page {{ size: A4; margin-top: 20mm; margin-bottom: 20mm; margin-left: 40mm; margin-right: 40mm; }}');
                    printWindow.document.write('body {{ font-family: sans-serif; font-size: 15px; line-height: 1.8; color: #000; }}');
                    printWindow.document.write('.center {{ text-align: center; }}');
                    printWindow.document.write('.right {{ text-align: right; margin-top: 40px; }}');
                    printWindow.document.write('.title {{ text-align: center; font-size: 18px; font-weight: bold; margin: 20px 0; }}');
                    printWindow.document.write('</style></head><body>');
                    
                    printWindow.document.write('<div class="center"><h3>મેહરબાન {court_name} માં</h3></div>');
                    printWindow.document.write('<div class="center"><b>{case_number}</b></div><br/>');
                    printWindow.document.write('<div><b>અરજદાર / પ્રથમ પક્ષકાર:</b> {applicant_name}<br/><b>વિરુદ્ધ / અને</b><br/><b>સામાવાળા / બીજો પક્ષકાર:</b> {opposite_party}</div>');
                    printWindow.document.write('<div class="title">:: {title_clean} ::</div>');
                    printWindow.document.write('<div>{formatted_body}</div>');
                    printWindow.document.write('<div class="right">_____________________<br/>({applicant_name})<br/><b>અરજદાર / પક્ષકારની સહી</b></div>');
                    
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
    st.subheader("🔒 તમારા સુરક્ષિત દસ્તાવેજો")
    if not st.session_state["logged_in"]:
        st.warning("🔒 સાચવેલા દસ્તાવેજો જોવા માટે ડાબી બાજુ સાઇડબારમાંથી **લોગિન** કરો.")
    else:
        is_admin = (st.session_state["role"] == "admin")
        search_q = st.text_input("🔍 જૂના કાગળો શોધો:", "")
        drafts = get_user_drafts(st.session_state["username"], search_query=search_q, is_admin=is_admin)

        if not drafts:
            st.info("કોઈ સાચવેલા ડ્રાફ્ટ મળ્યા નથી.")
        else:
            for d in drafts:
                draft_id, user_owner, d_type, app_name, c_time, c_name, opp_p, c_num, d_body = d
                with st.expander(f"📜 {d_type} | અરજદાર: {app_name} | ({c_time})"):
                    st.write(f"**યુઝર:** {user_owner}")
                    edit_c_name = st.text_input("કોર્ટ/ઓથોરિટી:", value=c_name, key=f"cn_{draft_id}")
                    
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        edit_app_name = st.text_input("અરજદાર:", value=app_name, key=f"an_{draft_id}")
                    with ec2:
                        edit_opp_p = st.text_input("સામાવાળા:", value=opp_p, key=f"op_{draft_id}")
                        
                    edit_c_num = st.text_input("કેસ/ખાતા/સર્વે નંબર:", value=c_num, key=f"cnum_{draft_id}")
                    edit_d_body = st.text_area("લખાણ:", value=d_body, height=180, key=f"text_{draft_id}")
                    
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
