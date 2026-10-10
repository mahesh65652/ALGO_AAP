import io
import sqlite3
import hashlib
import streamlit as st

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="ઓમ જનસેવા - ગાડી અને જમીન લે-વેચ",
    page_icon="🚗",
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
        margin-bottom: 25px;
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
    .ad-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
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
DB_FILE = "om_janseva_classifieds.db"

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
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                price TEXT NOT NULL,
                contact_no TEXT NOT NULL,
                description TEXT NOT NULL,
                image_blob BLOB,
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

def save_ad(username, category, title, location, price, contact_no, description, image_blob):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO ads (username, category, title, location, price, contact_no, description, image_blob)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, category, title, location, price, contact_no, description, image_blob))

def get_ads(category_filter="બધા", search_query=""):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        query = "%" + search_query + "%"
        if category_filter == "બધા":
            c.execute("SELECT id, username, category, title, location, price, contact_no, description, image_blob, created_at FROM ads WHERE title LIKE ? OR location LIKE ? OR description LIKE ? ORDER BY created_at DESC", (query, query, query))
        else:
            c.execute("SELECT id, username, category, title, location, price, contact_no, description, image_blob, created_at FROM ads WHERE category = ? AND (title LIKE ? OR location LIKE ? OR description LIKE ?) ORDER BY created_at DESC", (category_filter, query, query, query))
        return c.fetchall()

def delete_ad(ad_id, username, is_admin=False):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        if is_admin:
            c.execute("DELETE FROM ads WHERE id = ?", (ad_id,))
        else:
            c.execute("DELETE FROM ads WHERE id = ? AND username = ?", (ad_id, username))

# ── SESSION STATE ──────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "role" not in st.session_state:
    st.session_state["role"] = ""

# ── SIDEBAR ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🚗 ઓમ જનસેવા કેન્દ્ર")
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
                            st.error("આ યુઝરનામ પહેલેથી જ ઉપલબ્ધ છે!")
        else:
            st.success(f"👤 **{st.session_state['username']}**")
            if st.button("🚪 લોગઆઉટ", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.rerun()

    st.divider()
    st.markdown("### 📌 માર્ગદર્શિકા:")
    st.markdown("- અહીં તમારી જૂની ગાડી, બાઈક, પ્લોટ કે જમીન વેચવા માટે એડ મૂકી શકાય છે.")
    st.markdown("- ફોટો સાથે એડ મૂકવાથી ગ્રાહકો ઝડપથી સંપર્ક કરશે.")

# ── MAIN TITLE ─────────────────────────────────────────────────────
st.markdown('<div class="main-title">ઓમ જનસેવા - ગાડી અને જમીન લે-વેચ સેન્ટર</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">વાહનો અને સ્થાવર મિલકત (જમીન/મકાન) ની ખરીદ-વેચાણ માટેનું ઓનલાઈન પ્લેટફોર્મ</div>', unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 બધી જાહેરાતો જુઓ", "📢 નવી જાહેરાત મૂકો", "👤 મારી જાહેરાતો"])

with tab1:
    st.subheader("📋 ઉપલબ્ધ ખરીદ-વેચાણ જાહેરાતો")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cat_filter = st.selectbox("કેટેગરી ફિલ્ટર:", ["બધા", "🚗 ગાડી (વાહન)", "🏡 જમીન / પ્લોટ / મકાન"])
    with col_f2:
        search_kw = st.text_input("🔍 વિસ્તાર કે નામથી શોધો:", "")

    ads_list = get_ads(category_filter=cat_filter, search_query=search_kw)

    if not ads_list:
        st.info("હાલમાં કોઈ જાહેરાત ઉપલબ્ધ નથી.")
    else:
        for ad in ads_list:
            ad_id, usr, cat, title, loc, price, cont, desc, img_blob, date = ad
            with st.container():
                st.markdown(f"""
                <div class="ad-card">
                    <h3>{title}</h3>
                    <p><b>કેટેગરી:</b> {cat} &nbsp;|&nbsp; <b>સ્થળ/વિસ્તાર:</b> {loc}</p>
                    <p><b>અંદાજિત કિંમત:</b> ₹ {price}</p>
                    <p><b>સંપૂર્ણ વિગત:</b> {desc}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show Image if available
                if img_blob:
                    st.image(img_blob, caption="ગાડી/જમીનનો ફોટો", width=300)

                # WhatsApp Share Button
                wa_text = f"ઓમ જનસેવા એડ:\n*{title}*\nસ્થળ: {loc}\nકિંમત: ₹ {price}\nવિગત: {desc}\nસંપર્ક: {cont}"
                import urllib.parse
                encoded_wa_text = urllib.parse.quote(wa_text)
                st.markdown(f'<a href="https://api.whatsapp.com/send?text={encoded_wa_text}" target="_blank"><button style="background-color:#25d366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">📲 WhatsApp પર શેર કરો</button></a>', unsafe_allow_html=True)
                st.divider()

with tab2:
    st.subheader("📢 નવી જાહેરાત ઉમેરો")
    if not st.session_state["logged_in"]:
        st.warning("⚠️ જાહેરાત મૂકવા માટે કૃપા કરીને સાઇડબારમાંથી **લોગિન** કરો.")
    else:
        with st.form("ad_form"):
            category = st.selectbox("જાહેરાતનો પ્રકાર:", ["🚗 ગાડી (વાહન)", "🏡 જમીન / પ્લોટ / મકાન"])
            title = st.text_input("જાહેરાતનું ટાઇટલ (દા.ᱛ. Maruti Swift VXI 2020 વેચવાની છે / 3 વીઘા ખેતીની જમીન):")
            
            c1, c2 = st.columns(2)
            with c1:
                location = st.text_input("સ્થળ / ગામ / તાલુકો / જિલ્લો:")
            with c2:
                price = st.text_input("કિંમત (રૂપિયામાં, દા.ત. 5,50,000):")
                
            contact_no = st.text_input("સંપર્ક માટેનો મોબાઈલ નંબર:")
            description = st.text_area("વધારાની વિગત (મોડેલ, વર્ષ, કાગળો ક્લિયર છે કે નહીં વગેરે):")
            
            uploaded_file = st.file_uploader("📸 ગાડી અથવા જમીનનો ફોટો અપલોડ કરો (JPG/PNG):", type=["jpg", "jpeg", "png"])
            
            submit_btn = st.form_submit_button("🚀 જાહેરાત લાઈવ કરો", use_container_width=True)
            
            if submit_btn:
                if title and location and price and contact_no and description:
                    img_bytes = uploaded_file.read() if uploaded_file else None
                    save_ad(st.session_state["username"], category, title, location, price, contact_no, description, img_bytes)
                    st.success("🎉 તમારી જાહેરાત સફળતાપૂર્વક લાઈવ થઈ ગઈ છે!")
                else:
                    st.error("કૃપા કરીને બધી જ વિગતો સાચી રીતે ભરો.")

with tab3:
    st.subheader("👤 મારી પોસ્ટ કરેલી જાહેરાતો")
    if not st.session_state["logged_in"]:
        st.warning("🔒 તમારી જાહેરાતો જોવા માટે લોગિન કરો.")
    else:
        is_admin = (st.session_state["role"] == "admin")
        my_ads = get_ads(category_filter="બધા", search_query="")
        if not is_admin:
            my_ads = [ad for ad in my_ads if ad[1] == st.session_state["username"]]

        if not my_ads:
            st.info("તમે હજુ સુધી કોઈ જાહેરાત મૂકી નથી.")
        else:
            for ad in my_ads:
                ad_id, usr, cat, title, loc, price, cont, desc, img_blob, date = ad
                with st.expander(f"📌 {title} ({loc})"):
                    st.write(f"**કેટેગરી:** {cat} | **કિંમત:** ₹ {price} | **મોબાઈલ:** {cont}")
                    st.write(f"**વિગત:** {desc}")
                    if img_blob:
                        st.image(img_blob, width=200)
                    if st.button("🗑️ આ જાહેરાત ડિલીટ કરો", key=f"del_ad_{ad_id}"):
                        delete_ad(ad_id, st.session_state["username"], is_admin=is_admin)
                        st.success("જાહેરાત સફળતાપૂર્વક ડિલીટ થઈ ગઈ!")
                        st.rerun()
