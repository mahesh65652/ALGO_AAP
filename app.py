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
    page_title="ગુજરાત લીગલ ડ્રાફ્ટિંગ અને મહેસૂલી પોર્ટલ 2026 (Pro Version)",
    page_icon="⚖️",
    layout="wide"
)

# ── DATABASE SETUP (SQLite with Update Capabilities) ──────────────
DB_FILE = "legal_drafts_secure_v2.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
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
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(f"{password}_secure_salt".encode()).hexdigest()

def verify_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
    res = c.fetchone()
    conn.close()
    if res and res[0] == hash_password(password):
        return res[1]
    return None

def register_user(username, password, role="client"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                  (username, hash_password(password), role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def save_user_draft(username, doc_type, court_name, applicant_name, opposite_party, case_number, doc_body):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO drafts (username, doc_type, court_name, applicant_name, opposite_party, case_number, doc_body)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, doc_type, court_name, applicant_name, opposite_party, case_number, doc_body))
    conn.commit()
    conn.close()

def update_user_draft(draft_id, court_name, applicant_name, opposite_party, case_number, doc_body):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        UPDATE drafts 
        SET court_name = ?, applicant_name = ?, opposite_party = ?, case_number = ?, doc_body = ?
        WHERE id = ?
    """, (court_name, applicant_name, opposite_party, case_number, doc_body, draft_id))
    conn.commit()
    conn.close()

def get_user_drafts(username, search_query="", is_admin=False):
    conn = sqlite3.connect(DB_FILE)
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
    rows = c.fetchall()
    conn.close()
    return rows

def delete_user_draft(draft_id, username, is_admin=False):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if is_admin:
        c.execute("DELETE FROM drafts WHERE id = ?", (draft_id,))
    else:
        c.execute("DELETE FROM drafts WHERE id = ? AND username = ?", (draft_id, username))
    conn.commit()
    conn.close()

# ── SESSION STATE FOR LOGIN ───────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "role" not in st.session_state:
    st.session_state["role"] = ""

# ── SIDEBAR (LOGIN & EXTENDED GOVERNMENT LINKS) ───────────────────
with st.sidebar:
    st.header("🔐 સુરક્ષિત લોગિન / એકાઉન્ટ")
    
    if not st.session_state["logged_in"]:
        auth_mode = st.radio("પસંદ કરો:", ["લોગિન (Login)", "નવું એકાઉન્ટ બનાવો (Register)"])
        
        if auth_mode == "લોગિન (Login)":
            user_input = st.text_input("યુઝરનામ (Username)")
            pass_input = st.text_input("પાસવર્ડ (Password)", type="password")
            if st.button("🔓 લોગિન કરો", use_container_width=True):
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
                        st.success("એકાઉન્ટ સફળતાપૂર્વક બની ગયું! હવે લોગિન કરો.")
                    else:
                        st.error("આ યુઝરનામ પહેલાથી અસ્તિત્વમાં છે!")
                else:
                    st.warning("કૃપા કરીને બધી વિગતો ભરો.")
    else:
        st.success(f"👤 યુઝર: **{st.session_state['username']}** ({'Admin' if st.session_state['role'] == 'admin' else 'Client'})")
        if st.button("🚪 લોગઆઉટ (Logout)", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["role"] = ""
            st.rerun()

    st.divider()
    st.header("🔗 જમીન, મહેસૂલ અને ઈ-કોર્ટ્સ")
    
    st.link_button(label="🌐 AnyRoR (૭/૧૨ અને ૮-અ રેકોર્ડ)", url="https://anyror.gujarat.gov.in/", use_container_width=True)
    st.link_button(label="📜 Garvi 2.0 (દસ્તાવેજ નોંધણી)", url="https://garvi.gujarat.gov.in/", use_container_width=True)
    st.link_button(label="⚖️ e-Courts India Services", url="https://services.ecourts.gov.in/", use_container_width=True)
    st.link_button(label="🏛️ ગુજરાત હાઇકોર્ટ ઈ-ફાઇલિંગ", url="https://gujarathighcourt.nic.in/", use_container_width=True)
    st.link_button(label="💳 Cyber Treasury (સ્ટેમ્પ ચુકવણી)", url="https://www.treasury.gujarat.gov.in/", use_container_width=True)

    st.divider()
    st.header("🏢 ગુજરાત સરકારના અન્ય પોર્ટલ")
    st.link_button(label="🌐 ગુજરાત સરકાર પોર્ટલ", url="https://www.gujaratindia.gov.in", use_container_width=True)
    st.link_button(label="📋 Digital Gujarat (સરકારી સેવાઓ)", url="https://www.digitalgujarat.gov.in", use_container_width=True)
    st.link_button(label="🏡 i-Khedut (ખેડૂત યોજનાઓ)", url="https://ikhedut.gujarat.gov.in/", use_container_width=True)
    st.link_button(label="ℹ️ RTI Online Gujarat", url="https://www.rtionline.gujarat.gov.in", use_container_width=True)
    st.link_button(label="📢 SWAGAT online (ફરિયાદ નિવારણ)", url="https://swagat.gujarat.gov.in/", use_container_width=True)

# ── HEADER ─────────────────────────────────────────────────────────
st.title("⚖️ ગુજરાત હાઇકોર્ટ & મહેસૂલી લીગલ ડ્રાફ્ટિંગ સોફ્ટવેર (Pro Ultimate)")
st.caption("🔒 પ્રાઇવેટ એક્સેસ | ગુજરાત હાઇકોર્ટ નિયમ અનુસાર A4 માર્જિન, ફોર્મેટિંગ અને ઓટોમેશન સાથે")
st.divider()

# ── EXTENDED DRAFT TEMPLATES ───────────────────────────────────────
TEMPLATES = {
    "વાંધા અરજી (Objection Application)": 
"""અરજદારશ્રી તરફથી નીચે મુજબની વાંધા અરજી સવિનય રજૂ કરવામાં આવે છે:

૧. એ કે, સામાવાળા તરફથી કરવામાં આવેલ રજૂઆત/અરજી કાયદાકીય રીતે ટકી શકે તેમ નથી અને તથ્ય વગરની છે.
૨. એ કે, સદર બાબતમાં અરજદારના કાયદેસરના હક્ક, હિસ્સા અને હિત રહેલા છે, જેને ધ્યાને લીધા વગર સામાવાળાએ એકતરફી કાર્યવાહી કરવાનો પ્રયાસ કરેલ છે.
૩. એ કે, આથી નામદાર કોર્ટ/ઓથોરિટીને નમ્ર વિનંતી છે કે સામાવાળાની અરજી રદ્દ કરવી અને અરજદારના વાંધાઓ ધ્યાને લઈ ન્યાયી હુકમ કરવો.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "મુખત્યારનામું / પાવર ઓફ એટોર્ની (Power of Attorney)":
"""આથી હું નીચે સહી કરનાર _____________________, રહેવાસી: ___________________________________, આથી મારા પ્રતિનિધિ તરીકે શ્રી/શ્રીમતી _____________________, રહેવાસી: ___________________________________ ને મારો કાયદેસરનો મુખત્યાર (Power of Attorney) નીમું છું.

૧. મારા વતી સદર મિલકત/કેસ સંબંધિત તમામ સરકારી/અધિસરકારી કચેરીઓ, કોર્ટ અને રેવન્યુ ઓથોરિટી સમક્ષ હાજર રહેવાની અને સહી-સિક્કા કરવાની સત્તા આપું છું.
૨. મારા મુખત્યાર દ્વારા કરવામાં આવેલ તમામ કાર્યો મને સ્વયં મંજૂર અને કબૂલ રહેશે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "લીગલ નોટિસ (Legal Notice)":
"""મારા અસીમ શ્રી ____________________ તરફથી તમને આથી કાયદાકીય નોટિસ આપવામાં આવે છે કે:

૧. તમે મારા અસીમ સાથે કરેલ કરાર/વચન અનુસાર રૂ. ____________/- ચૂકવવાના થાય છે.
૨. આ નોટિસ મળ્યાના ૧૫ દિવસની અંદર સદર રકમ ચૂકવી આપવી અથવા યોગ્ય ખુલાસો કરવો.
૩. જો આપ નિષ્ફળ જશો તો આપની સામે સિવિલ તથા ક્રિમિનલ કોર્ટમાં યોગ્ય કાયદાકીય કાર્યવાહી કરવામાં આવશે, જેની સંપૂર્ણ જવાબદારી આપની રહેશે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "જમીન/મિલકત વેચાણ કરાર (Sale Agreement / Banaakhat)": 
"""આથી મિલકત વેચાણ કરાર/બનાખત આપનાર અને લેનાર વચ્ચે નીચે મુજબ નક્કી કરવામાં આવે છે:

૧. મિલકતની વિગત: ખાતા નંબર: ______, સર્વે/બ્લોક નંબર: ______, ક્ષેત્રફળ: ______, ગામ: ______, તાલુકો: ______, જીલ્લો: ______.
૨. કુલ વેચાણ કિંમત રૂ. ____________/- (અંકે રૂપિયા ________________________ પૂરા) નક્કી કરવામાં આવેલ છે.
૩. જે પૈકી બાના પેટે રૂ. ____________/- આજે ચૂકવી આપેલ છે, અને બાકીની રકમ રજિસ્ટર્ડ વેચાણ દસ્તાવેજ વખતે ચૂકવવાની રહેશે.
૪. સદર મિલકત તમામ પ્રકારના બોજા, કરજ કે વિવાદથી મુક્ત હોવાની ખાતરી પ્રથમ પક્ષકાર આપે છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "મકાન / દુકાન ભાડા કરાર (Rent Agreement)": 
"""આથી પ્રથમ પક્ષકાર (મકાન માલિક) અને દ્વિતિય પક્ષકાર (ભાડુઆત) વચ્ચે નીચે મુજબ ભાડા કરાર થાય છે:

૧. ભાડે આપેલ મિલકત: __________________________________________________
૨. ભાડાની મુદત: સમયગાળો ______ મહિના માટેનો રહેશે.
૩. માસિક ભાડું: રૂ. ________/- દર મહિનાની ______ તારીખ સુધીમાં ચૂકવવાનું રહેશે.
૪. ડિપોઝિટ રકમ: રૂ. ________/- એડવાન્સ ડિપોઝિટ તરીકે જમા રાખેલ છે, જે મુદત પૂરી થતાં પરત મળવાપાત્ર રહેશે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "સોગંદનામું / બાંહેધરી પત્ર (Affidavit)": 
"""હું નીચે સહી કરનાર __________________________________, ઉંમર: _____, ધંધો: ____________, રહેવાસી: __________________________________________________, આથી સોગંદ ઉપર નીચે મુજબ આપું છું:

૧. એ કે, હું આ સોગંદનામું મારા પોતાના જ્ઞાન અને વિશ્વાસ મુજબ સાચું રજૂ કરું છું.
૨. એ કે, ઉપર દર્શાવેલ વિગતોમાં કોઈ તથ્ય છુપાવવામાં આવેલ નથી.
૩. આ સોગંદનામું મારે ________________________ કચેરી/ઓથોરિટીમાં રજૂ કરવા માટે આપેલ છે.

જે અંગે મારું આ સોગંદનામું સાચું છે.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "જામીન અરજી (Bail Application)": 
"""નામદાર કોર્ટ સમક્ષ અરજદાર/આરોપીની જામીન મુક્તિ માટેની અરજી:

૧. એ કે, આરોપી સામે ગુનો રજિસ્ટર નંબર: ______/૨૦૨૬ પોલીસ સ્ટેશન: ____________ ખાતે નોંધાયેલ છે.
૨. એ કે, આરોપી નિષ્દોષ છે અને તેને ખોટી રીતે અટકાયતમાં લેવામાં આવ્યો છે.
૩. એ કે, આરોપી કોર્ટના તમામ નિયમો અને શરતોનું પાલન કરવા તથા યોગ્ય જામીનદાર રજૂ કરવા તૈયાર છે.
૪. આથી નામદાર કોર્ટને નમ્ર વિનંતી છે કે આરોપીને યોગ્ય શરતોએ જામીન મુક્ત કરવા હુકમ કરવો.

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

# ── WORD DOCUMENT GENERATOR ────────────────────────────────────────
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

# ── TABS LAYOUT ────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝 નવો ડ્રાફ્ટ બનાવો (Create Draft)", "📁 મારા સાચવેલા દસ્તાવેજો & એડિટિંગ (Saved & Edit)"])

with tab1:
    col_input, col_preview = st.columns([1.1, 0.9])

    with col_input:
        st.header("📝 વિગતો પસંદ કરો અને ભરો")
        
        selected_doc = st.selectbox(
            "દસ્તાવેજ / અરજીનો પ્રકાર પસંદ કરો:",
            list(TEMPLATES.keys())
        )
        
        if selected_doc in ["જમીન/મિલકત વેચાણ કરાર (Sale Agreement / Banaakhat)", "મકાન / દુકાન ભાડા કરાર (Rent Agreement)"]:
            st.link_button("🌐 AnyRoR પરથી ૭/૧૨ અને ૮-અ ની વિગતો જુઓ", "https://anyror.gujarat.gov.in/")
        
        court_name = st.text_input("કોર્ટ / કચેરી / ઓથોરિટીનું નામ:", "ગુજરાત હાઇકોર્ટ / સબ-રજિસ્ટ્રાર કચેરી")
        applicant_name = st.text_input("અરજદાર / પ્રથમ પક્ષકારનું નામ:", "મહેશભાઈ વિનોદભાઇ રામાવત")
        opposite_party = st.text_input("સામાવાળા / બીજા પક્ષકારનું નામ:", "ગુજરાત રાજ્ય / સામાવાળાનું નામ")
        case_number = st.text_input("કેસ / પિટિશન / ખાતા નંબર (જો હોય તો):", "C.A. No. 1024 of 2026")
        
        st.subheader("📄 કાનૂની લખાણ (ડ્રાફ્ટિંગ)")
        doc_body = st.text_area(
            "મુખ્ય લખાણ:", 
            value=TEMPLATES[selected_doc], 
            height=280
        )

        st.caption("📌 A4 Size | Left/Right Margin: 4 cm | Top/Bottom Margin: 2 cm | 1.5 Line Spacing")

        if st.session_state["logged_in"]:
            if st.button("💾 આ દસ્તાવેજ મારા પ્રાઇવેટ એકાઉન્ટમાં સેવ કરો", use_container_width=True):
                save_user_draft(
                    st.session_state["username"], selected_doc, court_name, 
                    applicant_name, opposite_party, case_number, doc_body
                )
                st.success("✅ દસ્તાવેજ સફળતાપૂર્વક તમારા પ્રાઇવેટ એકાઉન્ટમાં સેવ થઈ ગયો!")

    with col_preview:
        st.header("👁️ પ્રિવ્યૂ અને ડાઉનલોડ")
        st.success("તમારો લીગલ દસ્તાવેજ પ્રિન્ટ અને ડાઉનલોડ માટે તૈયાર છે.")
        
        docx_data = generate_docx(court_name, selected_doc, case_number, applicant_name, opposite_party, doc_body)
        
        st.download_button(
            label="📥 ૧. Word (.docx) ફાઇલ ડાઉનલોડ કરો",
            data=docx_data,
            file_name=f"{selected_doc.split(' ')[0]}_Document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        
        st.divider()
        st.subheader("📄 ૨. ડાયરેક્ટ PDF પ્રિન્ટ / ડાઉનલોડ કરો")
        
        title_clean = selected_doc.split('(')[0]
        formatted_body = doc_body.replace('\n', '<br/>')
        
        print_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: sans-serif; padding: 5px; }}
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
                .btn:hover {{ background-color: #d33; }}
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
                    if("{case_number}") {{
                        printWindow.document.write('<div class="center"><b>{case_number}</b></div><br/>');
                    }}
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
    st.header("🔒 તમારા સુરક્ષિત દસ્તાવેજો અને લાઈવ એડિટિંગ")
    if not st.session_state["logged_in"]:
        st.warning("🔒 તમારા સાચવેલા દસ્તાવેજો જોવા માટે ડાબી બાજુ સાઇડબારમાંથી **લોગિન** કરો.")
    else:
        is_admin = (st.session_state["role"] == "admin")
        
        search_q = st.text_input("🔍 જૂના કાગળો શોધો (અરજદારનું નામ, દસ્તાવેજનો પ્રકાર કે કેસ નંબર લખો):", "")
        drafts = get_user_drafts(st.session_state["username"], search_query=search_q, is_admin=is_admin)

        if not drafts:
            st.write("કોઈ ડ્રાફ્ટ મળ્યા નથી.")
        else:
            for d in drafts:
                draft_id, user_owner, d_type, app_name, c_time, c_name, opp_p, c_num, d_body = d
                with st.expander(f"📜 {d_type} | અરજદાર: {app_name} | (તારીખ: {c_time})"):
                    st.write(f"**યુઝર:** {user_owner}")
                    
                    # Live Edit Form
                    edit_c_name = st.text_input("કોર્ટ/ઓથોરિટી:", value=c_name, key=f"cn_{draft_id}")
                    edit_app_name = st.text_input("અરજદાર:", value=app_name, key=f"an_{draft_id}")
                    edit_opp_p = st.text_input("સામાવાળા:", value=opp_p, key=f"op_{draft_id}")
                    edit_c_num = st.text_input("કેસ/ખાતા નંબર:", value=c_num, key=f"cnum_{draft_id}")
                    edit_d_body = st.text_area("લખાણ:", value=d_body, height=180, key=f"text_{draft_id}")
                    
                    col_save_btn, col_dl_btn, col_del_btn = st.columns([1, 1, 1])
                    
                    with col_save_btn:
                        if st.button("✏️ સુધારા સેવ કરો (Update)", key=f"up_{draft_id}"):
                            update_user_draft(draft_id, edit_c_name, edit_app_name, edit_opp_p, edit_c_num, edit_d_body)
                            st.success("સુધારો સફળતાપૂર્વક સેવ થઈ ગયો!")
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
