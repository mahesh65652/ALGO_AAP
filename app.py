import io
import sqlite3
import streamlit as st
import urllib.parse
from PIL import Image

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="રામાવત જનસેવા - ગાડી અને જમીન લે-વેચ",
    page_icon="🚗",
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
        font-size: 30px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .sub-title {
        color: #94a3b8;
        font-size: 15px;
        text-align: center;
        margin-bottom: 25px;
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
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
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

# ── DATABASE SETUP (DIRECT STORAGE - NO LOGIN) ─────────────────────
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
    st.title("🚗 રામાવત જનસેવા કેન્દ્ર")
    st.caption("સંચાલક: મહેશભાઈ રામાવત")
    st.divider()
    st.markdown("### 📌 માર્ગદર્શિકા:")
    st.markdown("- ગ્રાહકોએ **કોઈપણ લોગિન કે એકાઉન્ટ બનાવવાની જરૂર નથી**.")
    st.markdown("- સીધા જ ફોટા સાથેની તમામ જાહેરાતો ગ્રાહકો જોઈ શકશે.")

# ── MAIN TITLE ─────────────────────────────────────────────────────     
st.markdown('<div class="main-title">રામાવત જનસેવા - ગાડી અને જમીન લે-વેચ સેન્ટર</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">વાહનો અને સ્થાવર મિલકત (જમીન/મકાન) ની ખરીદ-વેચાણ માટેનું પ્લેટફોર્મ (કોઈ લોગિન વગર સીધું જ જુઓ)</div>', unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 બધી જાહેરાતો જુઓ", "📢 નવી એડ બનાવો (પોસ્ટ કરો)", "🗑️ એડ મેનેજ / ડિલીટ કરો"])

with tab1:
    st.subheader("📋 ઉપલબ્ધ ખરીદ-વેચાણ જાહેરાતો (કોઈ લોગિન વગર)")
    
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
                
                # Show Image & Download Button for easy sharing
                if img_blob:
                    st.image(img_blob, caption="ગાડી/જમીનનો ફોટો", width=320)
                    st.download_button(
                        label="📥 ફોટો ડાઉનલોડ કરો (WhatsApp પર મોકલવા માટે)",
                        data=img_blob,
                        file_name=f"ramavat_ad_{ad_id}.jpg",
                        mime="image/jpeg",
                        key=f"dl_img_{ad_id}"
                    )

                # Full Text Share Template with Website Link included at the bottom
                website_link = "https://share.streamlit.io/"  # તમારી એપની લિંક અહીં બદલી શકો છો
                ad_text = f"🚗 *રામાવત જનસેવા એડ*\n\n📌 *{title}*\n📍 સ્થળ: {loc}\n💰 કિંમત: ₹ {price}\n📞 સંપર્ક: {cont}\n📝 વિગત: {desc}\n\n🌐 અમારી બધી જ એડ્સ જોવા માટે ક્લિક કરો:\n{website_link}"
                encoded_text = urllib.parse.quote(ad_text)
                
                st.markdown(f"""
                    <div style="margin-top: 10px;">
                        <a href="https://api.whatsapp.com/send?text={encoded_text}" target="_blank">
                            <button style="background-color:#25d366; color:white; padding:10px 16px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; width:100%; margin-bottom: 8px;">
                                🟢 WhatsApp પર આખી વિગત અને લિંક શેર કરો
                            </button>
                        </a>
                        <a href="https://t.me/share/url?url=&text={encoded_text}" target="_blank">
                            <button style="background-color:#0088cc; color:white; padding:10px 16px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; width:100%; margin-bottom: 8px;">
                                🔵 Telegram પર શેર કરો
                            </button>
                        </a>
                        <a href="https://www.facebook.com/sharer/sharer.php?u=&quote={encoded_text}" target="_blank">
                            <button style="background-color:#1877f2; color:white; padding:10px 16px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; width:100%;">
                                📘 Facebook પર શેર કરો
                            </button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
                
                st.divider()

with tab2:
    st.subheader("📢 નવી એડ બનાવો અને પોસ્ટ કરો")
    st.info("💡 અહીંથી વિગતો ભરીને નવી એડ તુરંત લાઈવ કરી શકો છો (કોઈ લોગિન વગર સીધી જ ગ્રાહકોને દેખાશે).")
    
    with st.form("ad_form", clear_on_submit=True):
        category = st.selectbox("જાહેરાતનો પ્રકાર:", ["🚗 ગાડી (વાહન)", "🏡 જમીન / પ્લોટ / મકાન"])
        title = st.text_input("જાહેરાતનું ટાઇટલ (દા.ત. Maruti Swift VXI 2020 વેચવાની છે / 3 વીઘા જમીન):")
        
        c1, c2 = st.columns(2)
        with c1:
            location = st.text_input("સ્થળ / ગામ / તાલુકો / જિલ્લો:")
        with c2:
            price = st.text_input("કિંમત (રૂપિયામાં, દા.ત. 5,50,000):")
            
        contact_no = st.text_input("સંપર્ક માટેનો મોબાઈલ નંબર:")
        description = st.text_area("વધારાની વિગત (મોડેલ, વર્ષ, કાગળો ક્લિયર છે કે નહીં વગેરે):")
        
        uploaded_file = st.file_uploader("📸 ગાડી અથવા જમીનનો ફોટો અપલોડ કરો (JPG/PNG):", type=["jpg", "jpeg", "png"])
        
        submit_btn = st.form_submit_button("🚀 એડ લાઈવ કરો (પોસ્ટ કરો)", use_container_width=True)
        
        if submit_btn:
            if title and location and price and contact_no and description:
                img_bytes = uploaded_file.read() if uploaded_file else None
                save_ad(category, title, location, price, contact_no, description, img_bytes)
                st.success("🎉 તમારી એડ સફળતાપૂર્વક લાઈવ થઈ ગઈ છે! હવે ગ્રાહકો વગર લોગિને સીધી જોઈ શકશે.")
            else:
                st.error("કૃપા કરીને બધી જ વિગતો સાચી રીતે ભરો.")

with tab3:
    st.subheader("🗑️ જુની એડ ડિલીટ કરો")
    st.info("જો ગાડી કે જમીન વેચાઈ જાય, તો અહીંથી તે એડ હટાવી શકો છો.")
    
    all_ads = get_ads(category_filter="બધા", search_query="")
    if not all_ads:
        st.info("હાલમાં કોઈ જાહેરાત ઉપલબ્ધ નથી.")
    else:
        for ad in all_ads:
            ad_id, cat, title, loc, price, cont, desc, img_blob, date = ad
            with st.expander(f"📌 {title} ({loc}) - કિંમત: ₹ {price}"):
                st.write(f"**કેટેગરી:** {cat} | **મોબાઈલ:** {cont}")
                st.write(f"**વિગત:** {desc}")
                if img_blob:
                    st.image(img_blob, width=200)
                
                if st.button("🗑️ આ એડ કાયમ માટે ડિલીટ કરો", key=f"del_ad_{ad_id}"):
                    delete_ad(ad_id)
                    st.success("એડ સફળતાપૂર્વક ડિલીટ થઈ ગઈ!")
                    st.rerun()
