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
    page_title="ગામ પંચાયત & મહેસૂલી પોર્ટલ (Legal Draft Software)",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS FOR MOBILE OPTIMIZATION ─────────────────────────────
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    .stTabs [data-baseweb="tab"] { border-radius: 6px 6px 0px 0px; padding: 10px 20px; background-color: #1e222d; }
    div[role="radiogroup"] { background-color: #1e222d; padding: 15px; border-radius: 10px; max-height: 250px; overflow-y: auto; }
    </style>
""", unsafe_allow_html=True)

# ── DATABASE SETUP ─────────────────────────────────────────────────
DB_FILE = "gram_panchayat_legal_v3.db"

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

# ── ALL 50 APPLICATIONS DATA ───────────────────────────────────────
ALL_50_APPS = {
    "1. જન્મ નોંધણી કરાવવા": "તલાટી-કમ-મંત્રી",
    "2. જન્મ પ્રમાણપત્ર મેળવવા": "તલાટી-કમ-મંત્રી",
    "3. જન્મ પ્રમાણપત્રમાં સુધારો": "તલાટી-કમ-મંત્રી",
    "4. મરણ નોંધણી કરાવવા": "તલાટી-કમ-મંત્રી",
    "5. મરણ પ્રમાણપત્ર મેળવવા": "તલાટી-કમ-મંત્રી",
    "6. મરણ પ્રમાણપત્રમાં સુધારો": "તલાટી-કમ-મંત્રી",
    "7. લગ્ન નોંધણી અંગે માર્ગદર્શન": "લગ્ન નોંધણી અધિકારી",
    "8. રહેઠાણ પ્રમાણપત્ર મેળવવા": "ગ્રામ પંચાયત",
    "9. મહેલત વેરા આકારણી": "તલાટી-કમ-મંત્રી",
    "10. મહેલત વેરામાં નામ ફેરફાર": "તલાટી-કમ-મંત્રી",
    "11. મહેલત વેરાની બાકી રકમ માહિતી": "ગ્રામ પંચાયત",
    "12. મહેલત વેરાની રસીદ": "ગ્રામ પંચાયત",
    "13. મકાન બાંધકામની મંજૂરી": "ગ્રામ પંચાયત",
    "14. મકાન બાંધકામની નોંધ": "ગ્રામ પંચાયત",
    "15. ગામતળની જમીન માહિતી": "તલાટી-કમ-મંત્રી",
    "16. જૂના વાહનની નોંધ શોધવા": "તલાટી-કમ-મંત્રી",
    "17. વાહનાપત્રકની નકલ": "ગ્રામ પંચાયત",
    "18. જૂની પંચાયત નોંધ નકલ": "તલાટી-કમ-મંત્રી",
    "19. ગામ નમૂના રેકોર્ડ નકલ": "તલાટી-કમ-મંત્રી",
    "20. પંચાયત જમીન માહિતી": "તલાટી-કમ-મંત્રી",
    "21. જાહેર રસ્તા ઉપર દબાણ": "સરપંચ / તલાટી",
    "22. પંચાયત જમીન દબાણ": "ગ્રામ પંચાયત",
    "23. ગૌચાર જમીન દબાણ": "મામલતદાર",
    "24. જાહેર રસ્તો બંધ થયો હોય": "સરપંચ / તલાટી",
    "25. રસ્તાની હદ/રસ્તો ખુલ્લો કરો": "ગ્રામ પંચાયત",
    "26. રસ્તો રીપેર કરાવવા": "સરપંચ / ગ્રામ પંચાયત",
    "27. નવો રસ્તો બનાવવા": "સરપંચ / ગ્રામ પંચાયત",
    "28. ગટર બનાવવાની અરજી": "સરપંચ / ગ્રામ પંચાયત",
    "29. ગટર સફાઈ કરાવવા": "ગ્રામ પંચાયત",
    "30. પીવાના પાણીની સમસ્યા": "સરપંચ / તલાટી",
    "31. નવું પાણીનું નળ કનેક્શન": "ગ્રામ પંચાયત",
    "32. પાણી કનેક્શન નામ ફેરફાર": "ગ્રામ પંચાયત",
    "33. સ્ટ્રીટ લાઈટ લગાવવા": "સરપંચ / ગ્રામ પંચાયત",
    "34. બંધ સ્ટ્રીટ લાઈટ રીપેર": "ગ્રામ પંચાયત",
    "35. ગામમાં સફાઈ કરાવવા": "સરપંચ / ગ્રામ પંચાયત",
    "36. કચરો ઉપાડા વ્યવસ્થા": "ગ્રામ પંચાયત",
    "37. જાહેર સ્થળે ગંદકી ફરિયાદ": "ગ્રામ પંચાયત",
    "38. વૃક્ષ/હરિયાળી અંગે અરજી": "ગ્રામ પંચાયત",
    "39. શૌચાલય/સ્વચ્છતા યોજના": "ગ્રામ પંચાયત",
    "40. આવાસ યોજના અંગે અરજી": "ગ્રામ પંચાયત",
    "41. મનરેગા કામ/રોજગાર અરજી": "ગ્રામ પંચાયત",
    "42. મનરેગા કામ ન મળ્યા ફરિયાદ": "કાર્યક્રમ અધિકારી",
    "43. વિકાસ કામ અંગે માહિતી": "તલાટી-કમ-મંત્રી",
    "44. આવક-ખર્ચ ની માહિતી": "તલાટી-કમ-મંત્રી",
    "45. પંચાયત ઠરાવની નકલ": "તલાટી-કમ-મંત્રી",
    "46. કામાના ખર્ચ / બિલ માહિતી": "ગ્રામ પંચાયત",
    "47. કામ ન કર્યું હોય ફરિયાદ": "તાલુકા વિકાસ અધિકારી (TDO)",
    "48. તલાટી કાર્યવાહી ન કરે": "તાલુકા વિકાસ અધિકારી (TDO)",
    "49. માહિતી મેળવવા RTI": "જાહેર માહિતી અધિકારી",
    "50. જવાબ ન મળે / અપીલ": "પ્રથમ અપીલ અધિકારી"
}

app_keys_list = list(ALL_50_APPS.keys())

# ── SIDEBAR ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📜 ગામ પંચાયત પોર્ટલ")
    
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

    with st.expander("🗺️ ઉપયોગી સરકારી પોર્ટલ્સ"):
        st.link_button("🌐 AnyRoR (૭/૧૨, ૮-અ)", "https://anyror.gujarat.gov.in/", use_container_width=True)
        st.link_button("🏛️ i-ORA (N.A., માપણી)", "https://iora.gujarat.gov.in/", use_container_width=True)
        st.link_button("📋 Digital Gujarat", "https://www.digitalgujarat.gov.in", use_container_width=True)
        st.link_button("📢 SWAGAT Online", "https://swagat.gujarat.gov.in/", use_container_width=True)

# ── HEADER ─────────────────────────────────────────────────────────
st.title("🏛️ ગામ પંચાયતમાં આપી શકાય એવી ૫૦ મહત્વની અરજીઓ")
st.caption("🔒 ડ્રાફ્ટિંગ સોફ્ટવેર | કાયદેસર અને સત્તાવાર ફોર્મેટિંગ મુજબ")
st.divider()

# ── WORD GENERATOR ─────────────────────────────────────────────────
def generate_docx(authority_name, selected_app, applicant_name, village_info, doc_body):
    doc = Document()
    
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(3.0)
    
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_head = p_head.add_run(f"પ્રતિ,\nશ્રીમાન {authority_name} સાહેબશ્રી,\nગામ પંચાયત કચેરી / સંબંધિત કચેરી,\nગામ/તાલુકો: {village_info}\n")
    run_head.font.size = Pt(12)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(f"\nવિષય: {selected_app} બાબત.\n")
    run_title.bold = True
    run_title.font.size = Pt(13)
    
    p_body = doc.add_paragraph()
    p_body.paragraph_format.line_spacing = 1.5
    run_body = p_body.add_run(doc_body)
    run_body.font.size = Pt(12)
    
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(30)
    run_sign = p_sign.add_run(f"\n\nઆપનો/આપની વિશ્વાસુ,\n\n_____________________\n({applicant_name})\nઅરજદારની સહી")
    run_sign.font.size = Pt(12)
    
    target_stream = io.BytesIO()
    doc.save(target_stream)
    return target_stream.getvalue()

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝 ૫૦ અરજી ડ્રાફ્ટ બનાવો", "📁 સાચવેલા દસ્તાવેજો"])

with tab1:
    col_input, col_preview = st.columns([1.1, 0.9], gap="large")

    with col_input:
        st.subheader("📝 અરજી પસંદ કરો")
        
        # ── NO DROPDOWN - SMART SEARCH & SELECTION ──────────────────
        sel_method = st.radio("અરજી પસંદ કરવાની રીત:", ["અરજી નંબર ટાઈપ કરો (૧ થી ૫૦)", "અરજીનું નામ શોધો"], horizontal=True)
        
        selected_app = app_keys_list[0]
        
        if sel_method == "અરજી નંબર ટાઈપ કરો (૧ થી ૫૦)":
            app_num = st.number_input("અરજી નંબર લખો (૧ થી ૫૦):", min_value=1, max_value=50, value=22, step=1)
            selected_app = app_keys_list[app_num - 1]
            st.info(f"📌 પસંદ થયેલ અરજી: **{selected_app}**")
        else:
            search_str = st.text_input("અરજીનું નામ લખો (દા.ત. જમીન, દબાણ, જન્મ):", "દબાણ")
            filtered_apps = [app for app in app_keys_list if search_str.lower() in app.lower()]
            if filtered_apps:
                selected_app = st.radio("મળેલ અરજીઓમાંથી પસંદ કરો:", filtered_apps)
            else:
                st.warning("કોઈ અરજી મળી નથી, બધી અરજીઓ બતાવાય છે.")
                selected_app = st.radio("અરજી પસંદ કરો:", app_keys_list[:10])

        st.divider()
        st.subheader("✏️ અરજીની વિગતો ભરો")
        
        suggested_auth = ALL_50_APPS[selected_app]
        authority_name = st.text_input("કોને અરજી આપવી (ઓથોરિટી):", value=suggested_auth)
        
        c1, c2 = st.columns(2)
        with c1:
            applicant_name = st.text_input("અરજદારનું નામ:", "મહેશભાઈ વિનોદભાઇ રામાવત")
        with c2:
            village_info = st.text_input("ગામ / તાલુકો / જિલ્લો:", "મોજે ગામ: _______, તા.: _______")
            
        case_number = st.text_input("અરજી ક્રમાંક / આધાર નંબર (જો હોય તો):", "અરજી નંબર: ૨૦૨૬/GP/૧૦૧")
        
        default_body = f"""સવિનય જણાવવાનું કે હું અરજદાર શ્રી {applicant_name}, રહેવાસી {village_info} નો કાયમી રહવાસી છું.

ઉપરોક્ત દર્શાવેલ વિષય અન્વયે જણાવવાનું કે મારે "{selected_app.split('. ')[1]}" અંગેની કામગીરી જરૂરિયાત હોય, આ અંગેની સત્તાવાર અરજી આપ સાહેબશ્રી સમક્ષ રજૂ કરું છું.

આ બાબતે જરૂરી તમામ કાગળો અને પુરાવાઓ આ અરજી સાથે સામેલ રાખેલ છે. આથી નિયમાનુસાર ની સત્વરે ચકાસણી કરી યોગ્ય કાર્યવાહી કરી આપવા નમ્ર વિનંતી છે.

સાથે સામેલ:
૧. અરજદારના આધાર કાર્ડની નકલ.
૨. સંબંધિત પુરાવાઓની નકલ."""

        st.subheader("📄 કાનૂની લખાણ (ડ્રાફ્ટિંગ)")
        doc_body = st.text_area("મુખ્ય લખાણ (એડિટ કરી શકાય તેવું):", value=default_body, height=220)

        if st.session_state["logged_in"]:
            if st.button("💾 પ્રાઇવેટ એકાઉન્ટમાં સેવ કરો", use_container_width=True, type="primary"):
                save_user_draft(
                    st.session_state["username"], selected_app, authority_name, 
                    applicant_name, village_info, case_number, doc_body
                )
                st.success("✅ અરજી સફળતાપૂર્વક સેવ થઈ ગઈ!")
        else:
            st.info("ℹ️ અરજી સેવ કરવા માટે ડાબી બાજુ સાઇડબારમાંથી લોગિન કરો.")

    with col_preview:
        st.subheader("👁️ પ્રિવ્યૂ અને ડાઉનલોડ")
        
        docx_data = generate_docx(authority_name, selected_app, applicant_name, village_info, doc_body)
        
        st.download_button(
            label="📥 ૧. Word (.docx) ફાઇલ ડાઉનલોડ કરો",
            data=docx_data,
            file_name=f"{selected_app.split(' ')[1]}_Application.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        
        st.divider()
        st.subheader("📄 ૨. ડાયરેક્ટ PDF પ્રિન્ટ કરો")
        
        formatted_body = doc_body.replace('\n', '<br/>')
        
        print_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .btn {{
                    background-color: #2563eb;
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
            <button class="btn" onclick="printDoc()">🖨️ આ અરજી PDF તરીકે સેવ / પ્રિન્ટ કરો</button>
            <script>
                function printDoc() {{
                    var printWindow = window.open('', '', 'height=600,width=800');
                    printWindow.document.write('<html><head><title>Gram Panchayat Application</title>');
                    printWindow.document.write('<style>');
                    printWindow.document.write('@page {{ size: A4; margin-top: 25mm; margin-bottom: 25mm; margin-left: 30mm; margin-right: 30mm; }}');
                    printWindow.document.write('body {{ font-family: sans-serif; font-size: 15px; line-height: 1.8; color: #000; }}');
                    printWindow.document.write('.right {{ text-align: right; margin-top: 40px; }}');
                    printWindow.document.write('.title {{ text-align: center; font-size: 17px; font-weight: bold; margin: 20px 0; border-bottom: 1px solid #000; padding-bottom: 5px; }}');
                    printWindow.document.write('</style></head><body>');
                    
                    printWindow.document.write('<div><b>પ્રતિ,</b><br/><b>શ્રીમાન {authority_name} સાહેબશ્રી,</b><br/>ગામ પંચાયત કચેરી,<br/>{village_info}</div>');
                    printWindow.document.write('<div class="title">વિષય: {selected_app} બાબત.</div>');
                    printWindow.document.write('<div>{formatted_body}</div>');
                    printWindow.document.write('<div class="right">આપનો વિશ્વાસુ,<br/><br/><br/>_____________________<br/>({applicant_name})<br/><b>અરજદારની સહી</b></div>');
                    
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
    st.subheader("🔒 તમારા સેવ કરેલા દસ્તાવેજો")
    if not st.session_state["logged_in"]:
        st.warning("🔒 સાચવેલા દસ્તાવેજો જોવા માટે ડાબી બાજુ સાઇડબારમાંથી **લોગિન** કરો.")
    else:
        is_admin = (st.session_state["role"] == "admin")
        search_q = st.text_input("🔍 જૂની અરજી શોધો:", "")
        drafts = get_user_drafts(st.session_state["username"], search_query=search_q, is_admin=is_admin)

        if not drafts:
            st.info("કોઈ સાચવેલા ડ્રાફ્ટ મળ્યા નથી.")
        else:
            for d in drafts:
                draft_id, user_owner, d_type, app_name, c_time, c_name, opp_p, c_num, d_body = d
                with st.expander(f"📜 {d_type} | અરજદાર: {app_name} | ({c_time})"):
                    st.write(f"**યુઝર:** {user_owner}")
                    edit_c_name = st.text_input("ઓથોરિટી:", value=c_name, key=f"cn_{draft_id}")
                    
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        edit_app_name = st.text_input("અરજદાર:", value=app_name, key=f"an_{draft_id}")
                    with ec2:
                        edit_opp_p = st.text_input("ગામ/વિગત:", value=opp_p, key=f"op_{draft_id}")
                        
                    edit_c_num = st.text_input("અરજી ક્રમાંક:", value=c_num, key=f"cnum_{draft_id}")
                    edit_d_body = st.text_area("લખાણ:", value=d_body, height=180, key=f"text_{draft_id}")
                    
                    col_save_btn, col_dl_btn, col_del_btn = st.columns([1, 1, 1])
                    
                    with col_save_btn:
                        if st.button("✏️ સુધારા સેવ કરો", key=f"up_{draft_id}", type="primary"):
                            update_user_draft(draft_id, edit_c_name, edit_app_name, edit_opp_p, edit_c_num, edit_d_body)
                            st.success("સુધારો સેવ થઈ ગયો!")
                            st.rerun()

                    with col_dl_btn:
                        saved_docx = generate_docx(edit_c_name, d_type, edit_app_name, edit_opp_p, edit_d_body)
                        st.download_button(
                            label="📥 Word ડાઉનલોડ",
                            data=saved_docx,
                            file_name=f"Saved_{draft_id}.docx",
                            key=f"dl_{draft_id}"
                        )
                    
                    with col_del_btn:
                        if st.button("🗑️ ડિલીટ કરો", key=f"del_{draft_id}"):
                            delete_user_draft(draft_id, st.session_state["username"], is_admin=is_admin)
                            st.success("દસ્તાવેજ ડિલીટ થઈ ગયો!")
                            st.rerun()
