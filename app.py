import streamlit as st
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import sqlite3
import hashlib
import datetime
import streamlit.components.v1 as components

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="ગુજરાત હાઇકોર્ટ નિયમ મુજબ - લીગલ ડ્રાફ્ટિંગ સોફ્ટવેર (Secure All-in-One)",
    page_icon="⚖️",
    layout="wide"
)

# ── DATABASE SETUP (SQLite for User Isolation & Security) ─────────
DB_FILE = "legal_drafts_secure.db"

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
        admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", ("admin", admin_pass, "admin"))
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

def get_user_drafts(username, is_admin=False):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if is_admin:
        c.execute("SELECT id, username, doc_type, applicant_name, created_at, court_name, opposite_party, case_number, doc_body FROM drafts ORDER BY created_at DESC")
    else:
        c.execute("SELECT id, username, doc_type, applicant_name, created_at, court_name, opposite_party, case_number, doc_body FROM drafts WHERE username = ? ORDER BY created_at DESC", (username,))
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

# ── SIDEBAR (LOGIN & GOVERNMENT LINKS) ────────────────────────────
with st.sidebar:
    st.header("🔐 સાઇન-ઇન / એકાઉન્ટ સિક્યોરિટી")
    
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
    st.header("🔗 કાનૂની અને મહેસૂલી પોર્ટલ્સ")
    
    st.link_button(label="🌐 AnyRoR (૭/૧૨ અને ૮-અ)", url="https://anyror.gujarat.gov.in/", use_container_width=True)
    st.link_button(label="📜 Garvi (દસ્તાવેજ પોર્ટલ)", url="https://garvi.gujarat.gov.in/", use_container_width=True)
    st.link_button(label="⚖️ ગુજરાત હાઇકોર્ટ ઈ-કોર્ટ્સ", url="https://gujarathighcourt.nic.in/", use_container_width=True)
    
    st.divider()
    st.header("🏛️ મહત્વની અધિકૃત વેબસાઈટ")
    
    st.link_button(label="🌐 ગુજરાત સરકાર પોર્ટલ", url="https://www.gujaratindia.gov.in", use_container_width=True)
    st.link_button(label="ℹ️ માહિતીનો અધિકાર (RTI)", url="https://www.rtionline.gujarat.gov.in", use_container_width=True)
    st.link_button(label="🏡 ગુજરાત પંચાયત પોર્ટલ", url="https://www.panchayat.gujarat.gov.in", use_container_width=True)
    st.link_button(label="📋 સરકારી યોજના (Digital Gujarat)", url="https://www.digitalgujarat.gov.in", use_container_width=True)
    st.link_button(label="📢 ફરિયાદ નિવારણ પોર્ટલ (Grievance)", url="https://www.grievance.gujarat.gov.in", use_container_width=True)

# ── HEADER ─────────────────────────────────────────────────────────
st.title("⚖️ લીગલ દસ્તાવેજ ડ્રાફ્ટિંગ સોફ્ટવેર (Secure All-in-One)")
st.caption("🔒 પ્રાઇવેટ એક્સેસ | ગુજરાત હાઇકોર્ટના A4 માર્જિન અને ફોર્મેટિંગ પરિપત્ર મુજબ")
st.divider()

# ── DRAFT TEMPLATES ────────────────────────────────────────────────
TEMPLATES = {
    "વાંધા અરજી (Objection Application)": 
"""અરજદારશ્રી તરફથી નીચે મુજબની વાંધા અરજી સવિનય રજૂ કરવામાં આવે છે:

૧. એ કે, સામાવાળા તરફથી કરવામાં આવેલ રજૂઆત/અરજી કાયદાકીય રીતે ટકી શકે તેમ નથી અને તથ્ય વગરની છે.
૨. એ કે, સદર બાબતમાં અરજદારના કાયદેસરના હક્ક, હિસ્સા અને હિત રહેલા છે, જેને ધ્યાને લીધા વગર સામાવાળાએ એકતરફી કાર્યવાહી કરવાનો પ્રયાસ કરેલ છે.
૩. એ કે, આથી નામદાર કોર્ટ/ઓથોરિટીને નમ્ર વિનંતી છે કે સામાવાળાની અરજી રદ્દ કરવી અને અરજદારના વાંધાઓ ધ્યાને લઈ ન્યાયી હુકમ કરવો.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "બચાવ અરજી / બચાવ કથન (Written Statement / Defense)": 
"""અરજદાર/આરોપી/સામાવાળા તરફથી બચાવ અરજી રજૂ કરવામાં આવે છે:

૧. એ કે, મારા અસીમ સામે મૂકવામાં આવેલા તમામ આરોપો/દાવાઓ તદ્દન ખોટા, પાયાવિહોણા અને ઉપજાવી કાઢેલા છે.
૨. એ કે, બનાવ/ઘટનાના દિવસે અરજદાર/આરોપીની કોઈ ગેરકાયદેસર ભૂમિકા ન હતી અને તેમને ખોટી રીતે આ કેસમાં સાંકળી લેવામાં આવ્યા છે.
૩. એ કે, કેસના દસ્તાવેજી પુરાવા અને સંજોગો ધ્યાને લેતા મારા અસીમ બિનગુનાહિત છે.
૪. આથી નામદાર કોર્ટને વિનંતી છે કે આ બચાવ કથન દફતરે લઈ યોગ્ય ન્યાય આપવા કૃપા કરવી.

સ્થળ: ____________
તારીખ: __/__/૨૦૨૬""",

    "જમીન/મિલકત વેચાણ કરાર (Sale Agreement / Banaakhat)": 
"""આથી મિલકત વેચાણ કરાર/બનાખત આપનાર અને લેનાર વચ્ચે નીચે મુજબ નક્કી કરવામાં આવે છે:

૧. મિલકતની વિગત: ખાતા નંબર: ______, સર્વે/બ્લોક નંબર: ______, ક્ષેત્રફળ: ______, જે ગામ: ______, તાલુકો: ______, જીલ્લો: ______ માં આવેલ છે.
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

    "દાવો / સિવિલ સૂટ (Plaint / Civil Suit)": 
"""નામદાર કોર્ટ સમક્ષ વાદી તરફથી દાવો રજૂ કરવામાં આવે છે:

૧. વાદીની સદર સિવિલ બાબતમાં કાયદેસરની મિલકત/હક્ક રહેલ છે.
૨. પ્રતિવાદીએ ગેરકાયદેસર રીતે વાદીના હક્કોમાં દખલગીરી કરવાનો પ્રયાસ કરેલ છે.
૩. વાદીને થયેલ નુકસાની અને કાયદાકીય જોગવાઈઓ ધ્યાને લઈ આ દાવો સ્વીકારવા અને વાદીની તરફેણમાં મનાઈહુકમ/ચુકાદો આપવા વિનંતી છે.

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
tab1, tab2 = st.tabs(["📝 નવો ડ્રાફ્ટ બનાવો (Create Draft)", "📁 મારા સાચવેલા દસ્તાવેજો (My Private Saved Drafts)"])

with tab1:
    col_input, col_preview = st.columns([1.1, 0.9])

    with col_input:
        st.header("📝 વિગતો પસંદ કરો અને ભરો")
        
        selected_doc = st.selectbox(
            "દસ્તાવેજ / અરજીનો પ્રકાર પસંદ કરો:",
            list(TEMPLATES.keys())
        )
        
        if selected_doc in ["જમીન/મિલકત વેચાણ કરાર (Sale Agreement / Banaakhat)", "મકાન / દુકાન ભાડા કરાર (Rent Agreement)", "દાવો / સિવિલ સૂટ (Plaint / Civil Suit)"]:
            st.link_button("🌐 AnyRoR પરથી ૭/૧૨ અને ૮-અ ની વિગતો જુઓ", "https://anyror.gujarat.gov.in/")
        
        court_name = st.text_input("કોર્ટ / કચેરી / ઓથોરિટીનું નામ:", "ગુજરાત હાઇકોર્ટ, અમદાવાદ / સબ-રજિસ્ટ્રાર કચેરી")
        applicant_name = st.text_input("અરજદાર / પ્રથમ પક્ષકારનું નામ:", "મહેશભાઈ વિનોદભાઇ રામાવત")
        opposite_party = st.text_input("સામાવાળા / બીજા પક્ષકારનું નામ:", "ગુજરાત રાજ્ય / મહેશ ભાઈ રામાવત")
        case_number = st.text_input("કેસ / પિટિશન / ખાતા નંબર (જો હોય તો):", "C.A. No. 1024 of 2026")
        
        st.subheader("📄 કાનૂની લખાણ (ડ્રાફ્ટિંગ)")
        st.info("💡 નીચે આપેલ લખાણ ઓટોમેટિક આવ્યું છે. તમે જરૂર મુજબ બદલાવ કરી શકો છો.")
        
        doc_body = st.text_area(
            "મુખ્ય લખાણ:", 
            value=TEMPLATES[selected_doc], 
            height=280
        )

        st.caption("📌 A4 Size | Left/Right Margin: 4 cm | Top/Bottom Margin: 2 cm | 1.5 Line Spacing")

        # Save to Database option if logged in
        if st.session_state["logged_in"]:
            if st.button("💾 આ દસ્તાવેજ મારા પ્રાઇવેટ એકાઉન્ટમાં સેવ કરો", use_container_width=True):
                save_user_draft(
                    st.session_state["username"], selected_doc, court_name, 
                    applicant_name, opposite_party, case_number, doc_body
                )
                st.success("✅ દસ્તાવેજ સફળતાપૂર્વક તમારા પ્રાઇવેટ એકાઉન્ટમાં સેવ થઈ ગયો! (બીજા કોઈ યુઝરને દેખાશે નહીં)")

    with col_preview:
        st.header("👁️ પ્રિવ્યૂ અને ડાઉનલોડ")
        st.success("તમારો લીગલ દસ્તાવેજ હાઇકોર્ટના માપદંડો મુજબ તૈયાર છે.")
        
        docx_data = generate_docx(court_name, selected_doc, case_number, applicant_name, opposite_party, doc_body)
        
        # Word File Download
        st.download_button(
            label="📥 ૧. તૈયાર Word (.docx) ફાઇલ ડાઉનલોડ કરો",
            data=docx_data,
            file_name=f"{selected_doc.split(' ')[0]}_Legal_Document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        
        st.divider()
        st.subheader("📄 ૨. ડાયરેક્ટ PDF પ્રિન્ટ / ડાઉનલોડ કરો")
        st.caption("💡 નીચે આપેલા 'Print/Save to PDF' બટન પર ક્લિક કરવાથી ૧૦૦% શુદ્ધ ગુજરાતી અક્ષરો સાથે A4 PDF સેવ થઈ જશે.")
        
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
    st.header("🔒 તમારા સુરક્ષિત અને ખાનગી દસ્તાવેજો")
    if not st.session_state["logged_in"]:
        st.warning("🔒 તમારા સાચવેલા દસ્તાવેજો જોવા માટે કૃપા કરીને ડાબી બાજુ સાઇડબારમાંથી **લોગિન** કરો.")
    else:
        is_admin = (st.session_state["role"] == "admin")
        drafts = get_user_drafts(st.session_state["username"], is_admin=is_admin)
        
        if is_admin:
            st.info("👑 **એડમિન મોડ:** તમે સિસ્ટમના તમામ યુઝર્સના દસ્તાવેજો જોઈ શકો છો.")
        else:
            st.info(f"👤 **યુઝર લિમિટેડ મોડ:** અહીં માત્ર **{st.session_state['username']}** ના જ ડોક્યુમેન્ટ્સ સુરક્ષિત રીતે દેખાશે.")

        if not drafts:
            st.write("હજુ સુધી કોઈ સેવ કરેલા દસ્તાવેજો નથી.")
        else:
            for d in drafts:
                draft_id, user_owner, d_type, app_name, c_time, c_name, opp_p, c_num, d_body = d
                with st.expander(f"📜 {d_type} | અરજદાર: {app_name} | (તારીખ: {c_time})"):
                    st.write(f"**યુઝર:** {user_owner}")
                    st.write(f"**કોર્ટ/ઓથોરિટી:** {c_name}")
                    st.write(f"**સામાવાળા:** {opp_p}")
                    st.write(f"**કેસ/ખાતા નંબર:** {c_num}")
                    st.text_area("લખાણ:", value=d_body, height=150, key=f"text_{draft_id}")
                    
                    saved_docx = generate_docx(c_name, d_type, c_num, app_name, opp_p, d_body)
                    st.download_button(
                        label="📥 Word (.docx) ડાઉનલોડ કરો",
                        data=saved_docx,
                        file_name=f"Saved_{d_type.split(' ')[0]}_{draft_id}.docx",
                        key=f"dl_{draft_id}"
                    )
                    
                    if st.button("🗑️ ડિલીટ કરો", key=f"del_{draft_id}"):
                        delete_user_draft(draft_id, st.session_state["username"], is_admin=is_admin)
                        st.success("દસ્તાવેજ ડિલીટ થઈ ગયો!")
                        st.rerun()
