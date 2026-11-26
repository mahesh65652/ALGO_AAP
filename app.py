import sqlite3
import urllib.parse
import streamlit as st

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="રામાવત જનસેવા - ગાડી, જમીન, ભાડા હિસાબ અને લીગલ સહાય",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 3D MODERN DARK THEME CSS ───────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 45%, #070b14 100%) !important;
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, span, label, p, .stMarkdown {
        color: #ffffff !important;
    }

    /* 3D Hero Header */
    .hero-3d {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.92), rgba(15, 23, 42, 0.96));
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 20px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow:
            0 18px 35px -10px rgba(0, 0, 0, 0.65),
            0 0 25px rgba(56, 189, 248, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.14);
        transform: perspective(1000px) rotateX(1.5deg);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .hero-3d:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-2px);
        box-shadow:
            0 24px 42px -12px rgba(0, 0, 0, 0.75),
            0 0 32px rgba(56, 189, 248, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 30px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 6px;
        letter-spacing: 0.3px;
    }
    .sub-title {
        color: #cbd5e1 !important;
        font-size: 14.5px;
        text-align: center;
        margin-bottom: 0px;
    }

    /* 3D Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #162032 0%, #0d1422 100%) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 8px 0 24px rgba(0, 0, 0, 0.45);
    }

    /* 3D Inputs */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        color: #ffffff !important;
        background: linear-gradient(145deg, #0b1220, #131e33) !important;
        border: 1px solid rgba(148, 163, 184, 0.28) !important;
        border-radius: 12px !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.45), 0 2px 6px rgba(0, 0, 0, 0.2) !important;
    }

    /* 3D Ad & Info Cards */
    .card-3d {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.88), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-top: 1px solid rgba(255, 255, 255, 0.16);
        padding: 20px 22px;
        border-radius: 18px;
        margin-bottom: 16px;
        box-shadow:
            0 14px 28px -8px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    }
    .card-3d:hover {
        transform: translateY(-4px) scale(1.006);
        border-color: rgba(56, 189, 248, 0.45);
        box-shadow:
            0 22px 38px -10px rgba(0, 0, 0, 0.75),
            0 0 22px rgba(56, 189, 248, 0.14),
            inset 0 1px 0 rgba(255, 255, 255, 0.16);
    }

    /* 3D Metric Boxes */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow:
            0 10px 20px -6px rgba(0, 0, 0, 0.55),
            inset 0 1px 0 rgba(255, 255, 255, 0.12);
        transition: transform 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
    }

    /* 3D Buttons */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(145deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(125, 211, 252, 0.35) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow:
            0 6px 14px rgba(2, 132, 199, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow:
            0 10px 20px rgba(2, 132, 199, 0.48),
            inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
    }
    .stButton > button:active, .stFormSubmitButton > button:active {
        transform: translateY(1px) !important;
    }

    /* 3D WhatsApp Button */
    .wa-btn-3d {
        background: linear-gradient(145deg, #25d366, #16a34a);
        color: #ffffff;
        padding: 10px 16px;
        border: 1px solid rgba(187, 247, 208, 0.4);
        border-radius: 12px;
        font-weight: 800;
        cursor: pointer;
        width: 100%;
        margin-top: 8px;
        margin-bottom: 6px;
        box-shadow:
            0 7px 16px rgba(22, 163, 74, 0.38),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .wa-btn-3d:hover {
        transform: translateY(-2px);
        box-shadow: 0 11px 22px rgba(22, 163, 74, 0.52);
    }

    /* 3D Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 6px 6px;
        padding: 10px 18px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #e2e8f0 !important;
        font-weight: 700;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.35);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #0ea5e9, #0284c7) !important;
        border-color: rgba(186, 230, 253, 0.5) !important;
        color: #ffffff !important;
        box-shadow:
            0 8px 18px rgba(2, 132, 199, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }

    /* Expander 3D */
    div[data-testid="stExpander"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.72), rgba(15, 23, 42, 0.85));
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 14px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.35);
        margin-bottom: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ── DATABASE SETUP ─────────────────────────────────────────────────
DB_FILE = "ramavat_direct_ads.db"

GUJARATI_MONTHS = {
    1: "જાન્યુઆરી",
    2: "ફેબ્રુઆરી",
    3: "માર્ચ",
    4: "એપ્રિલ",
    5: "મે",
    6: "જૂન",
    7: "જુલાઈ",
    8: "ઓગસ્ટ",
    9: "સપ્ટેમ્બર",
    10: "ઓક્ટોબર",
    11: "નવેમ્બર",
    12: "ડિસેમ્બર",
}


def init_db():
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    # 1. Ads Table
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

    # 2. Legal Notes Table
    c.execute("""
            CREATE TABLE IF NOT EXISTS legal_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                department TEXT,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    # 3. Tenants Master Table
    c.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                unit_no TEXT NOT NULL,
                rent_year INTEGER NOT NULL,
                monthly_rent REAL NOT NULL DEFAULT 0,
                deposit_amount REAL NOT NULL DEFAULT 0,
                start_date TEXT,
                notes TEXT
            )
        """)

    # 4. Monthly Rent, Light & Water Ledger Table
    c.execute("""
            CREATE TABLE IF NOT EXISTS rent_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                month_num INTEGER NOT NULL,
                rent_paid REAL NOT NULL DEFAULT 0,
                light_bill REAL NOT NULL DEFAULT 0,
                water_bill REAL NOT NULL DEFAULT 0,
                paid_date TEXT,
                status TEXT NOT NULL DEFAULT 'બાકી',
                UNIQUE(tenant_id, month_num),
                FOREIGN KEY (tenant_id) REFERENCES tenants (id) ON DELETE CASCADE
            )
        """)


init_db()


# ── ADS HELPERS ────────────────────────────────────────────────────
def save_ad(
    category, title, location, price, contact_no, description, image_blob
):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            INSERT INTO ads (category, title, location, price, contact_no, description, image_blob)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (category, title, location, price, contact_no, description, image_blob),
    )


def get_ads(category_filter="બધા", search_query=""):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    query = "%" + search_query + "%"
    if category_filter == "બધા":
      c.execute(
          """
                SELECT id, category, title, location, price, contact_no, description, image_blob, created_at
                FROM ads
                WHERE title LIKE ? OR location LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
            """,
          (query, query, query),
      )
    else:
      c.execute(
          """
                SELECT id, category, title, location, price, contact_no, description, image_blob, created_at
                FROM ads
                WHERE category = ? AND (title LIKE ? OR location LIKE ? OR description LIKE ?)
                ORDER BY created_at DESC
            """,
          (category_filter, query, query, query),
      )
    return c.fetchall()


def delete_ad(ad_id):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("DELETE FROM ads WHERE id = ?", (ad_id,))


# ── LEGAL NOTES HELPERS ────────────────────────────────────────────
def save_legal_note(title, department, description):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            INSERT INTO legal_notes (title, department, description)
            VALUES (?, ?, ?)
        """,
        (title, department, description),
    )


def get_legal_notes():
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        "SELECT id, title, department, description, created_at FROM legal_notes"
        " ORDER BY created_at DESC"
    )
    return c.fetchall()


def delete_legal_note(note_id):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("DELETE FROM legal_notes WHERE id = ?", (note_id,))


# ── TENANT & RENT LEDGER HELPERS ───────────────────────────────────
def add_tenant(
    tenant_name,
    phone,
    unit_no,
    rent_year,
    monthly_rent,
    deposit_amount,
    start_date,
    notes,
):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute(
        """
            INSERT INTO tenants (tenant_name, phone, unit_no, rent_year, monthly_rent, deposit_amount, start_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            tenant_name,
            phone,
            unit_no,
            rent_year,
            monthly_rent,
            deposit_amount,
            start_date,
            notes,
        ),
    )
    tenant_id = c.lastrowid
    for m in range(1, 13):
      c.execute(
          """
                INSERT OR IGNORE INTO rent_ledger (tenant_id, month_num, rent_paid, light_bill, water_bill, paid_date, status)
                VALUES (?, ?, 0, 0, 0, '', 'બાકી')
            """,
          (tenant_id, m),
      )


def get_tenants(year_filter="બધા"):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    if year_filter and year_filter != "બધા":
      c.execute(
          "SELECT * FROM tenants WHERE rent_year = ? ORDER BY id DESC",
          (int(year_filter),),
      )
    else:
      c.execute("SELECT * FROM tenants ORDER BY id DESC")
    return c.fetchall()


def get_ledger(tenant_id):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            SELECT id, month_num, rent_paid, light_bill, water_bill, paid_date, status
            FROM rent_ledger WHERE tenant_id = ? ORDER BY month_num ASC
        """,
        (tenant_id,),
    )
    return c.fetchall()


def update_month_entry(
    ledger_id, rent_paid, light_bill, water_bill, paid_date, status
):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            UPDATE rent_ledger
            SET rent_paid = ?, light_bill = ?, water_bill = ?, paid_date = ?, status = ?
            WHERE id = ?
        """,
        (rent_paid, light_bill, water_bill, paid_date, status, ledger_id),
    )


def update_tenant_details(tenant_id, monthly_rent, deposit_amount, notes):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            UPDATE tenants
            SET monthly_rent = ?, deposit_amount = ?, notes = ?
            WHERE id = ?
        """,
        (monthly_rent, deposit_amount, notes, tenant_id),
    )


def delete_tenant(tenant_id):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute("DELETE FROM rent_ledger WHERE tenant_id = ?", (tenant_id,))
    c.execute("DELETE FROM tenants WHERE id = ?", (tenant_id,))


# ── SIDEBAR ────────────────────────────────────────────────────────
with st.sidebar:
  st.markdown("## ⚖️ રામાવત જનસેવા કેન્દ્ર")
  st.caption("સંચાલક: મહેશભાઈ રામાવત")
  st.divider()
  st.markdown("### 📌 માર્ગદર્શિકા:")
  st.markdown("- **ગાડી અને જમીન:** નવી એડ લાઈવ કરો, શોધો અને WhatsApp પર શેર કરો.")
  st.markdown(
      "- **ભાડુઆત વાર્ષિક હિસાબ:** દર મહિનાનું ભાડું, લાઈટ, પાણી અને ડિપોઝીટ"
      " ભરો."
  )
  st.markdown("- **લીગલ AI સહાયક:** કેસ અને અરજીની વિગતો સાચવો.")

# ── 3D MAIN HEADER ─────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-3d">
        <div class="main-title">રામાવત જનસેવા - ગાડી, જમીન, ભાડા હિસાબ અને લીગલ સહાય</div>
        <div class="sub-title">વાહનો, સ્થાવર મિલકત ખરીદ-વેચાણ, ભાડુઆત વાર્ષિક લેજર તેમજ કાનૂની માર્ગદર્શન હબ</div>
    </div>
""",
    unsafe_allow_html=True,
)

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 બધી જાહેરાતો જુઓ",
    "📢 નવી એડ બનાવો",
    "🗑️ એડ મેનેજ / ડિલીટ",
    "⚖️ લીગલ AI સહાયક",
    "🏠 ભાડુઆત વાર્ષિક હિસાબ",
])

# ── TAB 1: VIEW ADS ────────────────────────────────────────────────
with tab1:
  st.subheader("📋 ઉપલબ્ધ ખરીદ-વેચાણ જાહેરાતો")

  col_f1, col_f2 = st.columns(2)
  with col_f1:
    cat_filter = st.selectbox(
        "કેટેગરી ફિલ્ટર:", ["બધા", "🚗 ગાડી (વાહન)", "🏡 જમીન / પ્લોટ / મકાન"]
    )
  with col_f2:
    search_kw = st.text_input("🔍 વિસ્તાર કે નામથી શોધો:", "")

  ads_list = get_ads(category_filter=cat_filter, search_query=search_kw)

  if not ads_list:
    st.info(
        "હાલમાં કોઈ જાહેરાત ઉપલબ્ધ નથી. 'નવી એડ બનાવો' ટેબમાંથી એડ ઉમેરો."
    )
  else:
    for ad in ads_list:
      ad_id, cat, title, loc, price, cont, desc, img_blob, date = ad
      st.markdown(
          f"""
            <div class="card-3d">
                <h3 style="color: #38bdf8; margin-bottom: 6px;">{title}</h3>
                <p style="margin: 4px 0;"><b>કેટેગરી:</b> {cat} &nbsp;|&nbsp; <b>સ્થળ:</b> {loc}</p>
                <p style="margin: 4px 0; font-size: 18px; color: #4ade80;"><b>કિંમત:</b> ₹ {price}</p>
                <p style="margin: 4px 0; color: #fb7185;"><b>સંપર્ક:</b> {cont}</p>
                <p style="margin: 10px 0 4px 0;"><b>વિગત:</b> {desc}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

      if img_blob:
        st.image(img_blob, caption="ફોટો", width=300)
        st.download_button(
            label="📥 ફોટો ડાઉનલોડ કરો",
            data=img_blob,
            file_name=f"ramavat_ad_{ad_id}.jpg",
            mime="image/jpeg",
            key=f"dl_img_{ad_id}",
        )

      app_link = "https://share.streamlit.io/"
      ad_text = (
          f"🚗 *રામાવત જનસેવા એડ*\n\n📌 *{title}*\n📍 સ્થળ: {loc}\n💰"
          f" કિંમત: ₹ {price}\n📞 સંપર્ક: {cont}\n📝 વિગત: {desc}\n\n🌐 વધુ"
          f" માહિતી માટે:\n{app_link}"
      )
      encoded_text = urllib.parse.quote(ad_text)

      st.markdown(
          f"""
                <a href="https://api.whatsapp.com/send?text={encoded_text}" target="_blank" style="text-decoration:none;">
                    <button class="wa-btn-3d">
                        🟢 WhatsApp પર શેર કરો
                    </button>
                </a>
            """,
          unsafe_allow_html=True,
      )
      st.divider()

# ── TAB 2: CREATE AD ───────────────────────────────────────────────
with tab2:
  st.subheader("📢 નવી એડ બનાવો અને પોસ્ટ કરો")
  with st.form("ad_form", clear_on_submit=True):
    category = st.selectbox(
        "જાહેરાતનો પ્રકાર:", ["🚗 ગાડી (વાહન)", "🏡 જમીન / પ્લોટ / મકાન"]
    )
    title = st.text_input("જાહેરાતનું ટાઇટલ:")

    c1, c2 = st.columns(2)
    with c1:
      location = st.text_input("સ્થળ / ગામ / તાલુકો:")
    with c2:
      price = st.text_input("કિંમત (₹):")

    contact_no = st.text_input("મોબાઈલ નંબર:")
    description = st.text_area("વધારાની વિગત:")
    uploaded_file = st.file_uploader(
        "📸 ફોટો અપલોડ કરો:", type=["jpg", "jpeg", "png"]
    )

    submit_btn = st.form_submit_button(
        "🚀 એડ લાઈવ કરો", use_container_width=True
    )

    if submit_btn:
      if title and location and price and contact_no and description:
        img_bytes = uploaded_file.read() if uploaded_file else None
        save_ad(
            category, title, location, price, contact_no, description, img_bytes
        )
        st.success("🎉 તમારી એડ સફળતાપૂર્વક લાઈવ થઈ ગઈ છે!")
      else:
        st.error("કૃપા કરીને બધી જ વિગતો ભરો.")

# ── TAB 3: MANAGE / DELETE ADS ─────────────────────────────────────
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

# ── TAB 4: LEGAL AI ASSISTANT ──────────────────────────────────────
with tab4:
  st.subheader("⚖️ લીગલ AI સહાયક (કેસ અને ડ્રાફ્ટ)")
  st.info(
      "અહીં તમે તમારા કાનૂની કેસ (જેમ કે જમીન પચાવી પાડવા બાબતના કેસ કે લેન્ડ"
      " ગ્રેબિંગ અરજીઓ) ની નોંધ અથવા વિગતો સાચવી શકો છો."
  )

  with st.form("legal_form", clear_on_submit=True):
    legal_title = st.text_input(
        "કેસ અથવા અરજીનું શીર્ષક (દા.ત. હિતેશભાઈ રામાવત જમીન કેસ):"
    )
    legal_dept = st.text_input(
        "સંબંધિત વિભાગ / કચેરી (દા.ત. કલેક્ટર કચેરી, મોરબી / CPGRAMS):"
    )
    legal_desc = st.text_area(
        "કેસની વિગત / કલમો / નોંધ (A to Z માહિતી અહીં લખી શકો છો):"
    )

    if st.form_submit_button("💾 લીગલ નોટ સેવ કરો", use_container_width=True):
      if legal_title and legal_desc:
        save_legal_note(legal_title, legal_dept, legal_desc)
        st.success(f"'{legal_title}' ની વિગતો સફળતાપૂર્વક રેકોર્ડ થઈ ગઈ છે!")
        st.rerun()
      else:
        st.error("કૃપા કરીને શીર્ષક અને વિગત બંને ભરો.")

  st.divider()
  st.markdown("### 📂 સાચવેલ લીગલ નોંધો")
  notes_list = get_legal_notes()
  if not notes_list:
    st.caption("હજુ સુધી કોઈ લીગલ નોંધ સાચવેલ નથી.")
  else:
    for n_id, n_title, n_dept, n_desc, n_date in notes_list:
      st.markdown(
          f"""
            <div class="card-3d">
                <h4 style="color:#38bdf8; margin-bottom:4px;">⚖️ {n_title}</h4>
                <p style="color:#94a3b8; font-size:13px; margin:2px 0;"><b>વિભાગ:</b> {n_dept or "—"} &nbsp;|&nbsp; <b>તારીખ:</b> {n_date}</p>
                <p style="margin-top:8px; white-space:pre-line;">{n_desc}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )
      if st.button("🗑️ નોંધ ડિલીટ કરો", key=f"del_legal_{n_id}"):
        delete_legal_note(n_id)
        st.rerun()

# ── TAB 5: TENANT ANNUAL RENT LEDGER ──────────────────────────────
with tab5:
  st.subheader(
      "🏠 મકાન ભાડુઆત વાર્ષિક યાદી (મહિનાવાર ભાડું, લાઈટ, પાણી અને ડિપોઝીટ)"
  )

  # 1. Add New Tenant Form
  with st.expander("➕ નવા ભાડુઆત અને ડિપોઝીટ ઉમેરો"):
    with st.form("add_tenant_form", clear_on_submit=True):
      c1, c2, c3 = st.columns(3)
      with c1:
        t_name = st.text_input("ભાડુઆતનું પૂરું નામ:")
        t_phone = st.text_input("મોબાઈલ નંબર:")
      with c2:
        t_unit = st.text_input("મકાન / રૂમ નંબર:")
        t_year = st.number_input(
            "વર્ષ:", min_value=2020, max_value=2035, value=2026, step=1
        )
      with c3:
        t_rent = st.number_input(
            "મહિનાનું નક્કી ભાડું (₹):", min_value=0.0, step=100.0
        )
        t_deposit = st.number_input(
            "ડિપોઝીટ રકમ (₹):", min_value=0.0, step=500.0
        )

      c4, c5 = st.columns(2)
      with c4:
        t_start = st.text_input("શરૂઆતની તારીખ (દા.ત. 01/01/2026):")
      with c5:
        t_notes = st.text_input("નોંધ (લાઈટ/પાણી/ડિપોઝીટ શરતો):")

      if st.form_submit_button("✅ ભાડુઆત સેવ કરો", use_container_width=True):
        if t_name and t_unit:
          add_tenant(
              t_name,
              t_phone,
              t_unit,
              t_year,
              t_rent,
              t_deposit,
              t_start,
              t_notes,
          )
          st.success(f"'{t_name}' ({t_unit}) નો વાર્ષિક હિસાબ શરૂ થઈ ગયો છે!")
          st.rerun()
        else:
          st.error("કૃપા કરીને ભાડુઆતનું નામ અને મકાન/રૂમ નંબર લખો.")

  st.divider()

  # 2. Filter by Year & Select Tenant
  f_col1, f_col2 = st.columns([1, 2])
  with f_col1:
    year_choice = st.selectbox(
        "📅 વર્ષ પસંદ કરો:", ["બધા", "2025", "2026", "2027", "2028"]
    )

  tenants_list = get_tenants(year_filter=year_choice)

  if not tenants_list:
    st.info(
        "આ પસંદગી મુજબ કોઈ ભાડુઆત નોંધાયેલ નથી. ઉપરથી નવા ભાડુઆત ઉમેરો."
    )
  else:
    tenant_options = {
        f"{t[1]} — રૂમ/મકાન: {t[3]} ({t[4]})": t for t in tenants_list
    }
    with f_col2:
      selected_label = st.selectbox(
          "👤 ભાડુઆત પસંદ કરો:", list(tenant_options.keys())
      )

    t_row = tenant_options[selected_label]
    t_id, t_name, t_phone, t_unit, t_year, t_rent, t_deposit, t_start, t_notes = (
        t_row
    )

    # Tenant Profile Card
    st.markdown(
        f"""
        <div class="card-3d">
            <h3 style="color:#38bdf8; margin-bottom:6px;">👤 {t_name} &nbsp;|&nbsp; 🏡 મકાન/રૂમ: {t_unit}</h3>
            <p style="margin:4px 0;"><b>📞 મોબાઈલ:</b> {t_phone or "—"} &nbsp;|&nbsp; <b>📅 વર્ષ:</b> {t_year} &nbsp;|&nbsp; <b>🗓️ શરૂઆત:</b> {t_start or "—"}</p>
            <p style="margin:4px 0; color:#4ade80;"><b>નક્કી માસિક ભાડું:</b> ₹ {t_rent:,.0f} &nbsp;|&nbsp; <b>ડિપોઝીટ:</b> ₹ {t_deposit:,.0f}</p>
            <p style="margin:6px 0 0 0; color:#cbd5e1;"><b>નોંધ:</b> {t_notes or "—"}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Update Deposit / Monthly Rent / Notes
    with st.expander("💰 ડિપોઝીટ / માસિક ભાડું / નોંધ અપડેટ કરો"):
      with st.form(f"upd_tenant_form_{t_id}"):
        u1, u2, u3 = st.columns(3)
        with u1:
          upd_rent = st.number_input(
              "માસિક ભાડું (₹):", value=float(t_rent), step=100.0
          )
        with u2:
          upd_dep = st.number_input(
              "ડિપોઝીટ રકમ (₹):", value=float(t_deposit), step=500.0
          )
        with u3:
          upd_notes = st.text_input("નોંધ:", value=t_notes or "")

        if st.form_submit_button("💾 વિગત અપડેટ કરો", use_container_width=True):
          update_tenant_details(t_id, upd_rent, upd_dep, upd_notes)
          st.success("ડિપોઝીટ અને વિગતો અપડેટ થઈ ગઈ!")
          st.rerun()

    ledger_rows = get_ledger(t_id)

    total_rent_paid = sum(r[2] for r in ledger_rows)
    total_light = sum(r[3] for r in ledger_rows)
    total_water = sum(r[4] for r in ledger_rows)
    grand_total = total_rent_paid + total_light + total_water
    paid_months_count = sum(1 for r in ledger_rows if r[6] == "ભરેલ")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("🔒 ડિપોઝીટ", f"₹ {t_deposit:,.0f}")
    m2.metric("🏠 કુલ ભરેલ ભાડું", f"₹ {total_rent_paid:,.0f}")
    m3.metric("💡 કુલ લાઈટ બિલ", f"₹ {total_light:,.0f}")
    m4.metric("💧 કુલ પાણી બિલ", f"₹ {total_water:,.0f}")
    m5.metric("📊 કુલ જમા રકમ", f"₹ {grand_total:,.0f}")

    st.caption(f"ભરેલ પૂર્ણ મહિનાઓ: {paid_months_count} / 12")
    st.markdown("### 📅 મહિનાવાર ભાડું, લાઈટ અને પાણી ભરવાની નોંધ")

    for l_id, m_num, r_paid, l_bill, w_bill, p_date, status in ledger_rows:
      month_name = GUJARATI_MONTHS[m_num]
      month_sum = r_paid + l_bill + w_bill
      badge = (
          "✅ ભરેલ"
          if status == "ભરેલ"
          else ("🌓 અંશતઃ" if status == "અંશતઃ ભરેલ" else "⏳ બાકી")
      )

      with st.expander(
          f"{month_name} {t_year} — {badge} | ભાડું: ₹{r_paid:,.0f} | લાઈટ:"
          f" ₹{l_bill:,.0f} | પાણી: ₹{w_bill:,.0f} | કુલ: ₹{month_sum:,.0f}"
      ):
        with st.form(f"month_form_{l_id}"):
          fc1, fc2, fc3 = st.columns(3)
          with fc1:
            in_rent = st.number_input(
                "મકાન ભાડું (₹):",
                value=float(r_paid if r_paid > 0 else t_rent),
                step=100.0,
                key=f"r_{l_id}",
            )
            st_options = ["બાકી", "ભરેલ", "અંશતઃ ભરેલ"]
            in_status = st.selectbox(
                "સ્થિતિ:",
                st_options,
                index=st_options.index(status) if status in st_options else 0,
                key=f"s_{l_id}",
            )
          with fc2:
            in_light = st.number_input(
                "લાઈટ બિલ (₹):",
                value=float(l_bill),
                step=50.0,
                key=f"l_{l_id}",
            )
            in_date = st.text_input(
                "ભરેલ તારીખ:", value=p_date or "", key=f"d_{l_id}"
            )
          with fc3:
            in_water = st.number_input(
                "પાણી બિલ (₹):",
                value=float(w_bill),
                step=50.0,
                key=f"w_{l_id}",
            )

          if st.form_submit_button(
              f"💾 {month_name} નો હિસાબ સાચવો", use_container_width=True
          ):
            update_month_entry(
                l_id, in_rent, in_light, in_water, in_date, in_status
            )
            st.success(f"{month_name} મહિનાનો હિસાબ અપડેટ થઈ ગયો!")
            st.rerun()

    # WhatsApp Annual Summary
    summary_msg = (
        f"🏠 *વાર્ષિક ભાડા હિસાબ ({t_year})*\n"
        f"👤 ભાડુઆત: {t_name} ({t_unit})\n"
        f"🔒 ડિપોઝીટ: ₹{t_deposit:,.0f}\n"
        f"🏠 કુલ ભરેલ ભાડું: ₹{total_rent_paid:,.0f}\n"
        f"💡 કુલ લાઈટ બિલ: ₹{total_light:,.0f}\n"
        f"💧 કુલ પાણી બિલ: ₹{total_water:,.0f}\n"
        f"📊 *કુલ જમા રકમ: ₹{grand_total:,.0f}*"
    )
    wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(summary_msg)}"
    st.markdown(
        f"""
        <a href="{wa_url}" target="_blank" style="text-decoration:none;">
            <button class="wa-btn-3d">
                🟢 WhatsApp પર વાર્ષિક હિસાબ મોકલો
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    with st.expander("🗑️ આ ભાડુઆતનો સંપૂર્ણ રેકોર્ડ ડિલીટ કરો"):
      st.warning("ચેતવણી: આ ભાડુઆત અને તેના 12 મહિનાનો હિસાબ કાયમ માટે ભૂંસાઈ જશે.")
      if st.button("🗑️ કાયમ માટે ડિલીટ કરો", key=f"del_tenant_{t_id}"):
        delete_tenant(t_id)
        st.success("ભાડુઆતનો રેકોર્ડ ડિલીટ થઈ ગયો!")
        st.rerun()
