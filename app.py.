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
    page_title="ઓમ જનસેવા & ઓનલાઈન સોલ્યુશન સેન્ટર",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CLEAN DARK THEME CSS ───────────────────────────────────────────
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    
    h1, h2, h3, h4, h5, h6, span, label, p, .stMarkdown {
        color: #ffffff !important;
    }

    .main-title {
        color: #40a9ff;
        font-size: 28px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #8c8c8c;
        font-size: 14px;
        text-align: center;
        margin-bottom: 20px;
    }

    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        color: #ffffff !important;
        background-color: #1f242d !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0px 0px;
        padding: 8px 16px;
        background-color: #161b22;
        color: #ffffff !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f6feb !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── DATABASE SETUP ─────────────────────────────────────────────────
DB_FILE = "om_janseva_drafts.db"

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
                office_name TEXT,
                applicant_name TEXT,
                contact_no TEXT,
                doc_body TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
            c.execute("INSERT INTO users VALUES (?, ?, ?)", ("admin", admin_pass, "admin"))

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hash_password(password), role))
            return True
    except sqlite3.IntegrityError:
        return False

def save_user_draft(username, doc_type, office_name, applicant_name, contact_no, doc_body):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO drafts (username, doc_type, office_name, applicant_name, contact_no, doc_body)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, doc_type, office_name, applicant_name, contact_no, doc_body))

def get_user_drafts(username, search_query="", is_admin=False):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        query = "%" + search_query + "%"
        if is_admin:
            c.execute("SELECT * FROM drafts WHERE applicant_name LIKE ? OR doc_type LIKE ? ORDER BY created_at DESC", (query, query))
        else:
            c.execute("SELECT * FROM drafts WHERE username = ? AND (applicant_name LIKE ? OR doc_type LIKE ?) ORDER BY created_at DESC", (username, query, query))
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
    st.title("💻 ઓમ જનસેવા સેન્ટર")
    st.caption("સંચાલક: મહેશભાઈ રામાવત")

    with st.expander("🔐 લોગિન / એકાઉન્ટ", expanded=not st.session_state["logged_in"]):
        if not st.session_state["logged_in"]:
            auth_mode = st.radio("પસંદ કરો:", ["લોગિન (Login)", "નવું એકાઉન્ટ"])
            user_input = st.text_input("યુઝરનામ")
            pass_input = st.text_input("પાસવર્ડ", type="password")
            
            if auth_mode == "લોગિન (Login)":
                if st.button("🔓 લોગિન કરો", use_container_width=True, type="primary"):
                    role = verify_user(user_input, pass_input)
                    if role:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_input
                        st.session_state["role"] = role
                        st.rerun()
                    else:
                        st.error("ખોટો યુઝરનામ અથવા પાસવર્ડ!")
            else:
                if st.button("📝 એકાઉન્ટ બનાવો", use_container_width=True):
                    if user_input and pass_input:
                        if register_user(user_input, pass_input):
                            st.success("એકાઉન્ટ બની ગયું! હવે લોગિન કરો.")
                        else:
                            st.error("આ યુઝરનામ ઉપલબ્ધ નથી!")
        else:
            st.success(f"👤 **{st.session_state['username']}**")
            if st.button("🚪 લોગઆઉટ", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.rerun()

    with st.expander("🌐 મહત્વપૂર્ણ સરકારી લિંક્સ", expanded=True):
        st.link_button("🌐 AnyRoR (૭/૧૨, ૮-અ)", "https://anyror.gujarat.gov.in/", use_container_width=True)
        st.link_button("📜 Digital Gujarat પોર્ટલ", "https://www.digitalgujarat.gov.in", use_container_width=True)
        st.link_button("🏛️ iORA Gujarat", "https://iora.gujarat.gov.in/", use_container_width=True)
        st.link_button("📜 GARVI Gujarat (દસ્તાવેજ)", "https://garvi.gujarat.gov.in/", use_container_width=True)
        st.link_button("💳 આધાર પોર્ટલ (UIDAI)", "https://uidai.gov.in/", use_container_width=True)
        st.link_button("🆔 PAN કાર્ડ પોર્ટલ", "https://eportal.incometax.gov.in/", use_container_width=True)
        st.link_button("🏦 PF મેમ્બર પોર્ટલ", "https://unifiedportal-mem.epfindia.gov.in/", use_container_width=True)

# ── MAIN TITLE ─────────────────────────────────────────────────────
st.markdown('<div class="main-title">ઓમ જનસેવા & ઓનલાઈન સોલ્યુશન સેન્ટર</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">સરકારી તથા ઓનલાઈન કામકાજ માટે સાદી અને ઝડપી અરજી ટાઈપિંગ સિસ્ટમ</div>', unsafe_allow_html=True)

# ── TEMPLATES ──────────────────────────────────────────────────────
TEMPLATES = {
    "સાદી સામાન્ય અરજી (Manual Draft)": 
"""પ્રતિ,
શ્રીમાન ____________________ સાહેબશ્રી,
કચેરીનું નામ: ________________________
તાલુકો: ____________, જિલ્લો: ____________

વિષય: ________________________________________________ બાબત.

સાહેબશ્રી,
હું નીચે સહી કરનાર ____________________, રહેવાસી: ________________________ આથી વિનંતી કરું છું કે,

(અહીં તમારી અરજીની વિગત લખો)
____________________________________________________________________________________
____________________________________________________________________________________

આ સાથે જરૂરી તમામ પુરાવાઓ જોડેલ છે. ઘટતી કાર્યવાહી કરવા નમ્ર વિનંતી છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "જન્મ / મરણ સુધારા અરજી": 
"""પ્રતિ,
શ્રીમાન રજિસ્ટ્રાર સાહેબશ્રી (જન્મ-મરણ વિભાગ),
કચેરી: ________________________

વિષય: જન્મ / મરણ રજિસ્ટરમાં નામ / તારીખ સુધારો કરવા બાબત.

સાહેબશ્રી,
મારા / મારા બાળકના જન્મ/મરણ રજિસ્ટરમાં ભૂલથી વિગત ખોટી લખાયેલ છે:
૧. હાલની ખોટી વિગત: ____________________________________
૨. સાચી વિગત (જે સુધારવાની છે): ____________________________________

સાથે સોગંદનામું, એલસી અને આધારકાર્ડની નકલ જોડેલ છે. સુધારીને નવું પ્રમાણપત્ર આપવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "રેશનકાર્ડમાં નામ ઉમેરવા / કમી અરજી": 
"""પ્રતિ,
શ્રીમાન પુરવઠા અધિકારી સાહેબશ્રી / મામલતદાર સાહેબશ્રી,
તાલુકા કચેરી: ____________________

વિષય: રેશનકાર્ડમાં નામ ઉમેરવા / કમી કરવા બાબત.

સાહેબશ્રી,
અમારા રેશનકાર્ડ નંબર: ________________ માં નવા સભ્યનું નામ ઉમેરવા / લગ્ન-અવસાનના કારણે નામ કમી કરવા અર્થે અરજી રજૂ કરેલ છે. 

સાથે જરૂરી આધાર પુરાવા સામેલ છે. યોગ્ય કાર્યવાહી કરવા વિનંતી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "જમીન વારસાઈ નોંધ દાખલ અરજી": 
"""પ્રતિ,
શ્રીમાન મામલતદાર સાહેબશ્રી,
તાલુકા સેવા સદન: ____________________

વિષય: મોજે ગામ: ________, સર્વે/બ્લોક નંબર: ________ માં વારસાઈ નોંધ દાખલ કરવા બાબત.

સાહેબશ્રી,
ઉપરોક્ત જમીનના મૂળ ખાતેદાર શ્રી ____________________________________ નું અવસાન થયેલ હોય, તેઓના કાયદેસરના વારસદારોના નામ ૭/૧૨ અને ૮-અ માં ચડાવવા વિનંતી છે.

સાથે પેઢીનામું, મરણ દાખલો અને વારસદારોના આધારકાર્ડ રજૂ કરેલ છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬"""
}

# ── WORD GENERATOR (A4 SIZE SETTINGS) ──────────────────────────────
def generate_docx(office_name, selected_doc, applicant_name, contact_no, doc_body):
    doc = Document()
    section = doc.sections[0]
    
    # Standard A4 Page Dimensions
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.0)

    # Title
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_head = p_head.add_run(f"અરજી: {selected_doc}\n")
    run_head.bold = True
    run_head.font.size = Pt(14)

    # Party Info
    p_party = doc.add_paragraph()
    p_party.paragraph_format.line_spacing = 1.3
    run_party = p_party.add_run(f"કચેરી/વિભાગ: {office_name}\nઅરજદારનું નામ: {applicant_name}\nસંપર્ક નંબર: {contact_no}\n")
    run_party.font.size = Pt(11)

    # Body
    p_body = doc.add_paragraph()
    p_body.paragraph_format.line_spacing = 1.4
    run_body = p_body.add_run(doc_body)
    run_body.font.size = Pt(12)

    # Signature
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(25)
    run_sign = p_sign.add_run(f"\n\n_____________________\n({applicant_name})\nઅરજદારની સહી")
    run_sign.font.size = Pt(12)

    target_stream = io.BytesIO()
    doc.save(target_stream)
    return target_stream.getvalue()

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝 અરજી બનાવો", "📁 સાચવેલા દસ્તાવેજો"])

with tab1:
    col_input, col_preview = st.columns([1.1, 0.9], gap="large")

    with col_input:
        st.subheader("૧. અરજીનો પ્રકાર પસંદ કરો")
        selected_doc = st.selectbox("અરજી મોડેલ પસંદ કરો:", list(TEMPLATES.keys()))

        st.subheader("૨. વિગતો ભરો")
        office_name = st.text_input("કચેરી / વિભાગનું નામ:", "જનસેવા કેન્દ્ર / મામલતદાર કચેરી")

        c1, c2 = st.columns(2)
        with c1:
            applicant_name = st.text_input("અરજદારનું નામ:", "અરજદારનું નામ")
        with c2:
            contact_no = st.text_input("મોબાઈલ નંબર:", "૯૮૭૬૫XXXXX")

        st.subheader("૩. અરજીનું લખાણ (એડિટ કરી શકાશે)")
        doc_body = st.text_area("મુખ્ય લખાણ:", value=TEMPLATES[selected_doc], height=280, key=f"body_{selected_doc}")

        if st.session_state["logged_in"]:
            if st.button("💾 એકાઉન્ટમાં સેવ કરો", use_container_width=True, type="primary"):
                save_user_draft(
                    st.session_state["username"], selected_doc,
                    office_name, applicant_name, contact_no, doc_body
                )
                st.success("✅ અરજી સફળતાપૂર્વક સેવ થઈ ગઈ!")
        else:
            st.info("ℹ️ અરજી સેવ કરવા માટે સાઇડબારમાંથી લોગિન કરો.")

    with col_preview:
        st.subheader("📄 પ્રિન્ટ અને ડાઉનલોડ (A4 Size)")

        docx_data = generate_docx(office_name, selected_doc, applicant_name, contact_no, doc_body)

        st.download_button(
            label="📥 Word (.docx) ફાઇલ ડાઉનલોડ કરો",
            data=docx_data,
            file_name=f"{selected_doc.split(' ')[0]}_Application.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

        st.divider()

        # Perfectly styled A4 Print HTML Preview
        formatted_body = doc_body.replace('\n', '<br/>')
        print_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .btn {{ background-color: #1f6feb; color: white; padding: 12px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; width: 100%; font-weight: bold; }}
            </style>
        </head>
        <body>
            <button class="btn" onclick="printDoc()">🖨️ A4 પેજમાં ડાયરેક્ટ PDF પ્રિન્ટ કરો</button>
            <script>
                function printDoc() {{
                    var printWindow = window.open('', '', 'height=800,width=700');
                    printWindow.document.write('<html><head><title>Print Application</title>');
                    printWindow.document.write('<style>');
                    printWindow.document.write('@page {{ size: A4; margin: 20mm 15mm 20mm 20mm; }}');
                    printWindow.document.write('body {{ font-family: "Hind Vadodara", "Gopika", "Arial", sans-serif; font-size: 14px; line-height: 1.6; color: #000; padding: 10px; }}');
                    printWindow.document.write('.title {{ text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 15px; text-decoration: underline; }}');
                    printWindow.document.write('.info {{ margin-bottom: 15px; font-size: 13px; line-height: 1.4; }}');
                    printWindow.document.write('.content {{ font-size: 14px; text-align: justify; white-space: pre-line; }}');
                    printWindow.document.write('.right {{ text-align: right; margin-top: 50px; font-size: 14px; }}');
                    printWindow.document.write('</style></head><body>');
                    printWindow.document.write('<div class="title">અરજી: {selected_doc}</div>');
                    printWindow.document.write('<div class="info"><b>કચેરી/વિભાગ:</b> {office_name}<br/><b>અરજદાર:</b> {applicant_name} | <b>મોબાઈલ:</b> {contact_no}</div><hr/>');
                    printWindow.document.write('<div class="content">{formatted_body}</div>');
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
                draft_id, user_owner, d_type, off_name, app_name, cont_no, d_body, c_time = d
                with st.expander(f"📜 {d_type} | અરજદાર: {app_name} | ({c_time})"):
                    st.write(f"**યુઝર:** {user_owner} | **કચેરી:** {off_name} | **મોબાઈલ:** {cont_no}")
                    st.text_area("લખાણ:", value=d_body, height=150, key=f"text_{draft_id}")

                    c_dl, c_del = st.columns(2)
                    with c_dl:
                        saved_docx = generate_docx(off_name, d_type, app_name, cont_no, d_body)
                        st.download_button("📥 Word ડાઉનલોડ", data=saved_docx, file_name=f"Draft_{draft_id}.docx", key=f"dl_{draft_id}")
                    with c_del:
                        if st.button("🗑️ ડિલીટ કરો", key=f"del_{draft_id}"):
                            delete_user_draft(draft_id, st.session_state["username"], is_admin=is_admin)
                            st.success("દસ્તાવેજ ડિલીટ થઈ ગયો!")
                            st.rerun()
