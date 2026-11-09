import io
import sqlite3
import streamlit as st
import urllib.parse
from PIL import Image

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="રામાવત જનસેવા - ગાડી, જમીન અને લીગલ સહાય",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── FANCY MODERN DARK THEME CSS ────────────────────────────────────
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #0e1117 100%) !important;
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, span, label, p, .stMarkdown {
        color: #ffffff !important;
    }
    .main-title {
        color: #38bdf8;
        font-size: 28px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .sub-title {
        color: #94a3b8;
        font-size: 14px;
        text-align: center;
        margin-bottom: 20px;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        color: #ffffff !important;
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    .ad-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 8px 16px;
        background-color: #1e293b;
        color: #ffffff !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── DATABASE SETUP (DIRECT STORAGE) ────────────────────────────────
DB_FILE = "ramavat_direct_ads.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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

init_db()

def save_ad(category, title, location, price, contact_no, description, image_blob):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO ads (category, title, location, price, contact_no, description, image_blob)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (category, title, location, price, contact_no, description, image_blob))

def get_ads(category_filter="બધા", search_query=""):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        query = "%" + search_query + "%"
        if category_filter == "બધા":
            c.execute("SELECT id, category, title, location, price, contact_no, description, image_blob, created_at FROM ads WHERE title LIKE ? OR location LIKE ? OR description LIKE ? ORDER BY created_at DESC", (query, query, query))
        else:
            c.execute("SELECT id, category, title, location, price, contact_no, description, image_blob, created_at FROM ads WHERE category = ? AND (title LIKE ? OR location LIKE ? OR description LIKE ?) ORDER BY created_at DESC", (category_filter, query, query, query))
        return c.fetchall()

def delete_ad(ad_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM ads WHERE id = ?", (ad_id,))

# ── SIDEBAR ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚖️ રામાવત જનસેવા કેન્દ્ર")
    st.caption("સંચાલક: મહેશભાઈ રામાવત")
    st.divider()
    st.markdown("### 📌 માર્ગદર્શિકા:")
    st.markdown("- અહીંથી ગાડી અને જમીનની એડ લાઈવ કરી શકો છો.")
    st.markdown("- નવા લીગલ સેクションમાં કેસની વિગતો અને કલમો ચકાસી શકો છો.")

# ── MAIN TITLE ─────────────────────────────────────────────────────     
st.markdown('<div class="main-title">રામાવત જનસેવા - ગાડી, જમીન અને લીગલ સહાય પ્લેટફોર્મ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">વાહનો, સ્થાવર મિલકત ખરીદ-વેચાણ તેમજ કાનૂની માર્ગદર્શન હબ</div>', unsafe_allow_html=True)

# ── TABS (ADDED LEGAL AI TAB) ──────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 બધી જાહેરાતો જુઓ", 
    "📢 નવી એડ બનાવો", 
    "🗑️ એડ મેનેજ / ડિલીટ", 
    "⚖️ લીગલ AI સહાયક (કેસ અને ડ્રાફ્ટ)"
])

with tab1:
    st.subheader("📋 ઉપલબ્ધ ખરીદ-વેચાણ જાહેરાતો")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cat_filter = st.selectbox("કેટેગરી ફિલ્ટર:", ["બધા", "🚗 ગાડી (વાહન)", "🏡 જમીન / પ્લોટ / મકાન"])
    with col_f2:
        search_kw = st.text_input("🔍 વિસ્તાર કે નામથી શોધો:", "")

    ads_list = get_ads(category_filter=cat_filter, search_query=search_kw)

    if not ads_list:
        st.info("હાલમાં કોઈ જાહેરાત ઉપલબ્ધ નથી. 'નવી એડ બનાવો' ટેબમાંથી એડ ઉમેરો.")
    else:
        for ad in ads_list:
            ad_id, cat, title, loc, price, cont, desc, img_blob, date = ad
            with st.container():
                st.markdown(f"""
                <div class="ad-card">
                    <h3 style="color: #38bdf8; margin-bottom: 5px;">{title}</h3>
                    <p style="margin: 3px 0;"><b>કેટેગરી:</b> {cat} &nbsp;|&nbsp; <b>સ્થળ:</b> {loc}</p>
                    <p style="margin: 3px 0; font-size: 17px; color: #4ade80;"><b>કિંમત:</b> ₹ {price}</p>
                    <p style="margin: 3px 0; color: #f43f5e;"><b>સંપર્ક:</b> {cont}</p>
                    <p style="margin: 8px 0 3px 0;"><b>વિગત:</b> {desc}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if img_blob:
                    st.image(img_blob, caption="ફોટો", width=300)
                    st.download_button(
                        label="📥 ફોટો ડાઉનલોડ કરો",
                        data=img_blob,
                        file_name=f"ramavat_ad_{ad_id}.jpg",
                        mime="image/jpeg",
                        key=f"dl_img_{ad_id}"
                    )

                app_link = "https://share.streamlit.io/"
                ad_text = f"🚗 *રામાવત જનસેવા એડ*\n\n📌 *{title}*\n📍 સ્થળ: {loc}\n💰 કિંમત: ₹ {price}\n📞 સંપર્ક: {cont}\n📝 વિગત: {desc}\n\n🌐 વધુ માહિતી માટે:\n{app_link}"
                encoded_text = urllib.parse.quote(ad_text)
                
                st.markdown(f"""
                    <div style="margin-top: 10px;">
                        <a href="https://api.whatsapp.com/send?text={encoded_text}" target="_blank">
                            <button style="background-color:#25d366; color:white; padding:8px 14px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; width:100%; margin-bottom: 6px;">
                                🟢 WhatsApp પર શેર કરો
                            </button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
                st.divider()

with tab2:
    st.subheader("📢 નવી એડ બનાવો અને પોસ્ટ કરો")
    with st.form("ad_form", clear_on_submit=True):
        category = st.selectbox("જાહેરાતનો પ્રકાર:", ["🚗 ગાડી (વાહન)", "🏡 જમીન / પ્લોટ / મકાન"])
        title = st.text_input("જાહેરાતનું ટાઇટલ:")
        
        c1, c2 = st.columns(2)
        with c1:
            location = st.text_input("સ્થળ / ગામ / તાલુકો:")
        with c2:
            price = st.text_input("કિંમત (₹):")
            
        contact_no = st.text_input("મોબાઈલ નંબર:")
        description = st.text_area("વધારાની વિગત:")
        uploaded_file = st.file_uploader("📸 ફોટો અપલોડ કરો:", type=["jpg", "jpeg", "png"])
        
        submit_btn = st.form_submit_button("🚀 એડ લાઈવ કરો", use_container_width=True)
        
        if submit_btn:
            if title and location and price and contact_no and description:
                img_bytes = uploaded_file.read() if uploaded_file else None
                save_ad(category, title, location, price, contact_no, description, img_bytes)
                st.success("🎉 તમારી એડ સફળતાપૂર્વક લાઈવ થઈ ગઈ છે!")
            else:
                st.error("કૃપા કરીને બધી જ વિગતો ભરો.")

with tab3:
    st.subheader("🗑️ જુની એડ ડિલીટ કરો")
    all_ads = get_ads(category_filter="બધા", search_query="")
    if not all_ads:
        st.info("હાલમાં કોઈ જાહેરાત ઉપલબ્ધ નથી.")
    else:
        for ad in all_ads:
            ad_id, cat, title, loc, price, cont, desc, img_blob, date = ad
            with st.expander(f"📌 {title} ({loc}) - ₹ {price}"):
                st.write(f"**વિગત:** {desc}")
                if st.button("🗑️ ડિલીટ કરો", key=f"del_ad_{ad_id}"):
                    delete_ad(ad_id)
                    st.success("એડ ડિલીટ થઈ ગઈ!")
                    st.rerun()

with tab4:
    st.subheader("⚖️ લીગલ AI સહાયક (કેસ અને ડ્રાફ્ટ)")
    st.info("અહીં તમે તમારા કાનૂની કેસ (જેમ કે જમીન પચાવી પાડવા બાબતના કેસ કે લેન્ડ ગ્રેબિંગ અરજીઓ) ની નોંધ અથવા વિગતો સેવ કરી શકો છો.")
    
    legal_title = st.text_input("કેસ અથવા અરજીનું શીર્ષક (દા.ત. હિતેશભાઈ રામાવત જમીન કેસ):")
    legal_dept = st.text_input("સંબંધિત વિભાગ / કચેરી (દા.ત. કલેક્ટર કચેરી, મોરબી / CPGRAMS):")
    legal_desc = st.text_area("કેસની વિગત / કલમો / નોંધ (A to Z માહિતી અહીં લખી શકો છો):")
    
    if st.button("💾 લીગલ નોટ સેવ કરો", use_container_width=True):
        if legal_title and legal_desc:
            st.success(f"'{legal_title}' ની વિગતો સફળતાપૂર્વક રેકોર્ડ થઈ ગઈ છે! તમે તેને ભવિષ્યના સંદર્ભ માટે વાપરી શકો છો.")
        else:
            st.error("કૃપા કરીને શીર્ષક અને વિગત બંને ભરો.")
