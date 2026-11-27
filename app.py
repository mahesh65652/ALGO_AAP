import sqlite3
import urllib.parse
import streamlit as st

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAMAVAT HOME CARE",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── COLORFUL 3D THEME CSS ──────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 10%, #1e1b4b 0%, #0f172a 45%, #060b14 100%) !important;
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, span, label, p, .stMarkdown {
        color: #ffffff !important;
    }

    /* Colorful 3D Hero Header */
    .hero-3d {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.22), rgba(139, 92, 246, 0.22), rgba(16, 185, 129, 0.18));
        border: 1px solid rgba(125, 211, 252, 0.45);
        border-radius: 22px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow:
            0 20px 38px -12px rgba(0, 0, 0, 0.7),
            0 0 28px rgba(56, 189, 248, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.22);
    }
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #34d399, #f472b6, #facc15);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 34px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }
    .sub-title {
        color: #e2e8f0 !important;
        font-size: 14.5px;
        text-align: center;
        margin-bottom: 0px;
    }

    /* Colorful 3D Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 55%, #090d16 100%) !important;
        border-right: 1px solid rgba(167, 139, 250, 0.28);
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        color: #ffffff !important;
        background: linear-gradient(145deg, #0b1324, #172542) !important;
        border: 1px solid rgba(99, 102, 241, 0.45) !important;
        border-radius: 12px !important;
    }

    /* Colorful 3D Cards */
    .card-cyan {
        background: linear-gradient(145deg, rgba(14, 116, 144, 0.35), rgba(15, 23, 42, 0.94));
        border: 1px solid rgba(34, 211, 238, 0.45);
        border-left: 6px solid #22d3ee;
        padding: 18px 22px;
        border-radius: 18px;
        margin-bottom: 16px;
        box-shadow: 0 14px 28px -8px rgba(0, 0, 0, 0.65);
    }
    .card-purple {
        background: linear-gradient(145deg, rgba(109, 40, 217, 0.32), rgba(15, 23, 42, 0.94));
        border: 1px solid rgba(192, 132, 252, 0.45);
        border-left: 6px solid #c084fc;
        padding: 18px 22px;
        border-radius: 18px;
        margin-bottom: 16px;
        box-shadow: 0 14px 28px -8px rgba(0, 0, 0, 0.65);
    }

    /* Colorful Metric Cards (nth-child colors) */
    div[data-testid="stMetric"] {
        border-radius: 16px;
        padding: 12px 14px;
        box-shadow: 0 12px 22px -6px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255,255,255,0.18);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #0284c7, #0c4a6e);
    }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #7c3aed, #3b0764);
    }
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #059669, #064e3b);
    }
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #d97706, #78350f);
    }
    div[data-testid="column"]:nth-of-type(5) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #db2777, #831843);
    }
    div[data-testid="column"]:nth-of-type(6) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #4f46e5, #1e1b4b);
    }

    /* 3D Buttons */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(145deg, #6366f1, #0284c7) !important;
        color: #ffffff !important;
        border: 1px solid rgba(165, 243, 252, 0.45) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        box-shadow: 0 7px 16px rgba(79, 70, 229, 0.4) !important;
    }

    /* Vibrant WhatsApp 3D Button */
    .wa-btn-3d {
        background: linear-gradient(145deg, #22c55e, #15803d);
        color: #ffffff;
        padding: 11px 16px;
        border: 1px solid rgba(187, 247, 208, 0.5);
        border-radius: 12px;
        font-weight: 900;
        cursor: pointer;
        width: 100%;
        margin-top: 8px;
        margin-bottom: 6px;
        box-shadow: 0 8px 18px rgba(21, 128, 61, 0.45);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 6px 6px;
        padding: 10px 18px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(148, 163, 184, 0.25);
        color: #e2e8f0 !important;
        font-weight: 800;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #ec4899, #8b5cf6) !important;
        color: #ffffff !important;
        border-color: rgba(251, 207, 232, 0.55) !important;
    }

    div[data-testid="stExpander"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.82), rgba(15, 23, 42, 0.92));
        border: 1px solid rgba(129, 140, 248, 0.3);
        border-radius: 14px;
        margin-bottom: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ── DATABASE SETUP ─────────────────────────────────────────────────
DB_FILE = "ramavat_home_care.db"

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

    # Tenant master table (added once; ledger spans any year)
    c.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                unit_no TEXT NOT NULL,
                monthly_rent REAL NOT NULL DEFAULT 0,
                deposit_amount REAL NOT NULL DEFAULT 0,
                start_date TEXT,
                notes TEXT
            )
        """)

    # Backward-compatible migration if old table had rent_year
    cols = [row[1] for row in c.execute("PRAGMA table_info(tenants)").fetchall()]
    if "rent_year" in cols and "start_date" in cols:
      # Keep existing rows safely
      pass

    c.execute("""
            CREATE TABLE IF NOT EXISTS rent_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                ledger_year INTEGER NOT NULL DEFAULT 2026,
                month_num INTEGER NOT NULL,
                rent_paid REAL NOT NULL DEFAULT 0,
                light_bill REAL NOT NULL DEFAULT 0,
                water_bill REAL NOT NULL DEFAULT 0,
                paid_date TEXT,
                status TEXT NOT NULL DEFAULT 'બાકી',
                UNIQUE(tenant_id, ledger_year, month_num),
                FOREIGN KEY (tenant_id) REFERENCES tenants (id) ON DELETE CASCADE
            )
        """)

    c.execute("""
            CREATE TABLE IF NOT EXISTS tenant_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                doc_type TEXT NOT NULL,
                file_name TEXT NOT NULL,
                mime_type TEXT NOT NULL,
                file_blob BLOB NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tenant_id) REFERENCES tenants (id) ON DELETE CASCADE
            )
        """)


init_db()


def ensure_year_ledger(tenant_id, ledger_year):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    for m in range(1, 13):
      c.execute(
          """
                INSERT OR IGNORE INTO rent_ledger (tenant_id, ledger_year, month_num, rent_paid, light_bill, water_bill, paid_date, status)
                VALUES (?, ?, ?, 0, 0, 0, '', 'બાકી')
            """,
          (tenant_id, int(ledger_year), m),
      )


def add_tenant_once(
    tenant_name, phone, unit_no, monthly_rent, deposit_amount, start_date, notes
):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute(
        """
            INSERT INTO tenants (tenant_name, phone, unit_no, monthly_rent, deposit_amount, start_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            tenant_name.strip(),
            phone.strip(),
            unit_no.strip(),
            monthly_rent,
            deposit_amount,
            start_date.strip(),
            notes.strip(),
        ),
    )
    tenant_id = c.lastrowid
  for yr in [2025, 2026, 2027, 2028]:
    ensure_year_ledger(tenant_id, yr)


def get_tenants(search_q=""):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    like_q = f"%{search_q}%"
    c.execute(
        """
            SELECT id, tenant_name, phone, unit_no, monthly_rent, deposit_amount, start_date, notes
            FROM tenants
            WHERE tenant_name LIKE ? OR unit_no LIKE ? OR phone LIKE ?
            ORDER BY id ASC
        """,
        (like_q, like_q, like_q),
    )
    return c.fetchall()


def get_ledger(tenant_id, ledger_year):
  ensure_year_ledger(tenant_id, ledger_year)
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            SELECT id, month_num, rent_paid, light_bill, water_bill, paid_date, status
            FROM rent_ledger
            WHERE tenant_id = ? AND ledger_year = ?
            ORDER BY month_num ASC
        """,
        (tenant_id, int(ledger_year)),
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


def update_tenant_details(
    tenant_id, tenant_name, phone, unit_no, monthly_rent, deposit_amount, notes
):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            UPDATE tenants
            SET tenant_name = ?, phone = ?, unit_no = ?, monthly_rent = ?, deposit_amount = ?, notes = ?
            WHERE id = ?
        """,
        (
            tenant_name.strip(),
            phone.strip(),
            unit_no.strip(),
            monthly_rent,
            deposit_amount,
            notes.strip(),
            tenant_id,
        ),
    )


def delete_tenant(tenant_id):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute("DELETE FROM tenant_documents WHERE tenant_id = ?", (tenant_id,))
    c.execute("DELETE FROM rent_ledger WHERE tenant_id = ?", (tenant_id,))
    c.execute("DELETE FROM tenants WHERE id = ?", (tenant_id,))


def add_tenant_document(tenant_id, doc_type, file_name, mime_type, file_blob):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            INSERT INTO tenant_documents (tenant_id, doc_type, file_name, mime_type, file_blob)
            VALUES (?, ?, ?, ?, ?)
        """,
        (tenant_id, doc_type, file_name, mime_type, file_blob),
    )


def get_tenant_documents(tenant_id):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        """
            SELECT id, doc_type, file_name, mime_type, file_blob, uploaded_at
            FROM tenant_documents WHERE tenant_id = ? ORDER BY id DESC
        """,
        (tenant_id,),
    )
    return c.fetchall()


def delete_tenant_document(doc_id):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("DELETE FROM tenant_documents WHERE id = ?", (doc_id,))


def build_whatsapp_url(phone, message):
  clean_phone = "".join(ch for ch in str(phone or "") if ch.isdigit())
  if len(clean_phone) == 10:
    clean_phone = "91" + clean_phone
  encoded_msg = urllib.parse.quote(message)
  if clean_phone:
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"
  return f"https://api.whatsapp.com/send?text={encoded_msg}"


# ── SIDEBAR (ONE-TIME ADD + LINE-BY-LINE DIRECTORY) ───────────────
with st.sidebar:
  st.markdown("## 🏠 RAMAVAT HOME CARE")
  st.caption("એકવાર ભાડુઆત એડ કરો • કાયમી હિસાબ અને રસીદ")
  st.divider()

  st.markdown("### 📋 ભાડુઆતોની લાઈનસર યાદી:")
  sidebar_tenants = get_tenants()
  if not sidebar_tenants:
    st.caption("હજુ કોઈ ભાડુઆત નોંધાયેલ નથી.")
  else:
    for idx, t in enumerate(sidebar_tenants, start=1):
      st.markdown(f"{idx}. **{t[1]}** — રૂમ: `{t[3]}` (₹{t[4]:,.0f})")

  st.divider()
  st.markdown("### 📌 સરળ નિયમ:")
  st.markdown("• ભાડુઆત **એક જ વાર** ઉમેરવાના રહેશે.")
  st.markdown("• દર વર્ષે અને દર મહિને ફક્ત હિસાબ ભરવાનો.")
  st.markdown("• આધાર કાર્ડ / ID અહીં સુરક્ષિત રહેશે.")
  st.markdown("• WhatsApp રસીદ એક ક્લિકમાં મોકલો.")

# ── COLORFUL 3D HEADER ─────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-3d">
        <div class="main-title">✨ RAMAVAT HOME CARE ✨</div>
        <div class="sub-title">એકવાર ભાડુઆત નોંધણી • ઓટોમેટિક કુલ સરવાળો • આધાર/ID ડોક્યુમેન્ટ્સ • માસિક WhatsApp રસીદ</div>
    </div>
""",
    unsafe_allow_html=True,
)

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "👥 ભાડુઆતોની યાદી અને હિસાબ",
    "🪪 ડોક્યુમેન્ટ્સ (આધાર / ID)",
    "🧾 માસિક રસીદ મોકલો",
])

# ── TAB 1: TENANTS LIST, GRAND TOTAL & YEARLY LEDGER ──────────────
with tab1:
  with st.expander("➕ નવા ભાડુઆત ઉમેરો (ફક્ત એક જ વાર એડ કરવાના)"):
    with st.form("add_tenant_once_form", clear_on_submit=True):
      c1, c2, c3 = st.columns(3)
      with c1:
        t_name = st.text_input("ભાડુઆતનું પૂરું નામ:")
        t_phone = st.text_input("મોબાઈલ નંબર:")
      with c2:
        t_unit = st.text_input("મકાન / રૂમ નંબર:")
        t_start = st.text_input("શરૂઆતની તારીખ (દા.ત. 01/01/2026):")
      with c3:
        t_rent = st.number_input(
            "મહિનાનું નક્કી ભાડું (₹):", min_value=0.0, step=100.0
        )
        t_deposit = st.number_input(
            "ડિપોઝીટ રકમ (₹):", min_value=0.0, step=500.0
        )

      t_notes = st.text_input("નોંધ (લાઈટ/પાણી/ડિપોઝીટ વિગત):")

      if st.form_submit_button(
          "✅ ભાડુઆત કાયમી યાદીમાં ઉમેરો", use_container_width=True
      ):
        if t_name and t_unit:
          add_tenant_once(
              t_name, t_phone, t_unit, t_rent, t_deposit, t_start, t_notes
          )
          st.success(
              f"'{t_name}' ({t_unit}) કાયમી યાદીમાં ઉમેરાઈ ગયા છે! હવે ફરી એડ"
              " કરવાની જરૂર નથી."
          )
          st.rerun()
        else:
          st.error("કૃપા કરીને ભાડુઆતનું નામ અને મકાન/રૂમ નંબર લખો.")

  st.divider()

  f1, f2, f3 = st.columns([1, 1, 2])
  with f1:
    selected_year = st.selectbox(
        "📅 હિસાબનું વર્ષ:", [2025, 2026, 2027, 2028], index=1
    )
  with f2:
    search_tenant = st.text_input("🔍 નામ / રૂમ / મોબાઈલ શોધો:", "")

  all_tenants_for_total = get_tenants()
  if all_tenants_for_total:
    all_dep_sum = sum(t[5] for t in all_tenants_for_total)
    all_rent_sum = 0.0
    all_light_sum = 0.0
    all_water_sum = 0.0

    for item in all_tenants_for_total:
      l_items = get_ledger(item[0], selected_year)
      all_rent_sum += sum(r[2] for r in l_items)
      all_light_sum += sum(r[3] for r in l_items)
      all_water_sum += sum(r[4] for r in l_items)

    all_grand_sum = all_rent_sum + all_light_sum + all_water_sum

    st.markdown(f"### 📊 બધા ભાડુઆતોનો કુલ સરવાળો ({selected_year})")
    g1, g2, g3, g4, g5, g6 = st.columns(6)
    g1.metric("👥 કુલ ભાડુઆત", f"{len(all_tenants_for_total)}")
    g2.metric("🔒 કુલ ડિપોઝીટ", f"₹ {all_dep_sum:,.0f}")
    g3.metric("🏠 કુલ ભાડું", f"₹ {all_rent_sum:,.0f}")
    g4.metric("💡 કુલ લાઈટ", f"₹ {all_light_sum:,.0f}")
    g5.metric("💧 કુલ પાણી", f"₹ {all_water_sum:,.0f}")
    g6.metric("💰 કુલ જમા", f"₹ {all_grand_sum:,.0f}")
    st.divider()

  filtered_tenants = get_tenants(search_q=search_tenant)

  if not filtered_tenants:
    st.info("હાલમાં કોઈ ભાડુઆત નોંધાયેલ નથી. ઉપરથી નવા ભાડુઆત ઉમેરો.")
  else:
    tenant_map = {f"{t[1]} — રૂમ/મકાન: {t[3]}": t for t in filtered_tenants}
    with f3:
      selected_label = st.selectbox(
          "👤 ભાડુઆત પસંદ કરો:", list(tenant_map.keys())
      )

    t_row = tenant_map[selected_label]
    t_id, t_name, t_phone, t_unit, t_rent, t_deposit, t_start, t_notes = t_row

    st.markdown(
        f"""
        <div class="card-cyan">
            <h3 style="color:#67e8f9; margin-bottom:6px;">👤 {t_name} &nbsp;|&nbsp; 🏡 મકાન/રૂમ: {t_unit}</h3>
            <p style="margin:4px 0;"><b>📞 મોબાઈલ:</b> {t_phone or "—"} &nbsp;|&nbsp; <b>🗓️ શરૂઆત:</b> {t_start or "—"} &nbsp;|&nbsp; <b>📅 વર્ષ:</b> {selected_year}</p>
            <p style="margin:4px 0; color:#6ee7b7;"><b>માસિક ભાડું:</b> ₹ {t_rent:,.0f} &nbsp;|&nbsp; <b>ડિપોઝીટ:</b> ₹ {t_deposit:,.0f}</p>
            <p style="margin:6px 0 0 0; color:#e2e8f0;"><b>નોંધ:</b> {t_notes or "—"}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("✏️ ભાડુઆતની વિગત / ડિપોઝીટ / માસિક ભાડું બદલો"):
      with st.form(f"upd_tenant_{t_id}"):
        u1, u2, u3 = st.columns(3)
        with u1:
          upd_name = st.text_input("નામ:", value=t_name)
          upd_phone = st.text_input("મોબાઈલ:", value=t_phone or "")
        with u2:
          upd_unit = st.text_input("મકાન/રૂમ નંબર:", value=t_unit)
          upd_rent = st.number_input(
              "માસિક ભાડું (₹):", value=float(t_rent), step=100.0
          )
        with u3:
          upd_dep = st.number_input(
              "ડિપોઝીટ રકમ (₹):", value=float(t_deposit), step=500.0
          )
          upd_notes = st.text_input("નોંધ:", value=t_notes or "")

        if st.form_submit_button("💾 વિગત અપડેટ કરો", use_container_width=True):
          update_tenant_details(
              t_id, upd_name, upd_phone, upd_unit, upd_rent, upd_dep, upd_notes
          )
          st.success("વિગતો અપડેટ થઈ ગઈ!")
          st.rerun()

    ledger_rows = get_ledger(t_id, selected_year)
    total_rent_paid = sum(r[2] for r in ledger_rows)
    total_light = sum(r[3] for r in ledger_rows)
    total_water = sum(r[4] for r in ledger_rows)
    grand_total = total_rent_paid + total_light + total_water

    st.markdown(f"### 📈 {t_name} નો {selected_year} વાર્ષિક સરવાળો")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("🔒 ડિપોઝીટ", f"₹ {t_deposit:,.0f}")
    m2.metric("🏠 કુલ ભરેલ ભાડું", f"₹ {total_rent_paid:,.0f}")
    m3.metric("💡 કુલ લાઈટ બિલ", f"₹ {total_light:,.0f}")
    m4.metric("💧 કુલ પાણી બિલ", f"₹ {total_water:,.0f}")
    m5.metric("📊 કુલ જમા", f"₹ {grand_total:,.0f}")

    st.markdown(f"### 📅 {selected_year} મહિનાવાર ભાડું, લાઈટ અને પાણી ભરવાની નોંધ")

    for l_id, m_num, r_paid, l_bill, w_bill, p_date, status in ledger_rows:
      month_name = GUJARATI_MONTHS[m_num]
      month_sum = r_paid + l_bill + w_bill
      badge = (
          "✅ ભરેલ"
          if status == "ભરેલ"
          else ("🌓 અંશતઃ" if status == "અંશતઃ ભરેલ" else "⏳ બાકી")
      )

      with st.expander(
          f"{month_name} {selected_year} — {badge} | ભાડું: ₹{r_paid:,.0f} |"
          f" લાઈટ: ₹{l_bill:,.0f} | પાણી: ₹{w_bill:,.0f} | કુલ:"
          f" ₹{month_sum:,.0f}"
      ):
        with st.form(f"m_form_{l_id}"):
          fc1, fc2, fc3 = st.columns(3)
          with fc1:
            in_rent = st.number_input(
                "મકાન ભાડું (₹):",
                value=float(r_paid if r_paid > 0 else t_rent),
                step=100.0,
                key=f"r_{l_id}",
            )
            st_opts = ["બાકી", "ભરેલ", "અંશતઃ ભરેલ"]
            in_status = st.selectbox(
                "સ્થિતિ:",
                st_opts,
                index=st_opts.index(status) if status in st_opts else 0,
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
            st.success(f"{month_name} નો હિસાબ સાચવાઈ ગયો!")
            st.rerun()

    with st.expander("🗑️ આ ભાડુઆતને યાદીમાંથી કાયમ માટે ડિલીટ કરો"):
      if st.button("🗑️ ડિલીટ કરો", key=f"del_t_{t_id}"):
        delete_tenant(t_id)
        st.success("ભાડુઆત ડિલીટ થઈ ગયા!")
        st.rerun()

# ── TAB 2: TENANT DOCUMENTS (AADHAAR / ID / ETC.) ─────────────────
with tab2:
  st.subheader("🪪 ભાડુઆતે આપેલ ડોક્યુમેન્ટ્સ (આધાર કાર્ડ, ID પ્રૂફ વિગેરે)")

  all_tenants_doc = get_tenants()
  if not all_tenants_doc:
    st.info("પહેલા 'ભાડુઆતોની યાદી અને હિસાબ' ટેબમાં ભાડુઆત ઉમેરો.")
  else:
    doc_t_map = {f"{t[1]} — રૂમ/મકાન: {t[3]}": t for t in all_tenants_doc}
    doc_sel_label = st.selectbox(
        "👤 ભાડુઆત પસંદ કરો:", list(doc_t_map.keys()), key="doc_t_sel"
    )
    dt_row = doc_t_map[doc_sel_label]
    dt_id, dt_name, _, dt_unit, *_ = dt_row

    with st.form(f"upload_doc_form_{dt_id}", clear_on_submit=True):
      d_col1, d_col2 = st.columns(2)
      with d_col1:
        doc_type = st.selectbox(
            "ડોક્યુમેન્ટનો પ્રકાર:",
            [
                "આધાર કાર્ડ (Aadhaar Card)",
                "ચૂંટણી કાર્ડ / ID પ્રૂફ",
                "ડ્રાઇવિંગ લાયસન્સ / પાસપોર્ટ",
                "ભાડા કરાર / અન્ય ડોક્યુમેન્ટ",
            ],
        )
      with d_col2:
        uploaded_doc = st.file_uploader(
            "📎 ફાઈલ અપલોડ કરો (JPG, PNG, PDF):",
            type=["jpg", "jpeg", "png", "pdf"],
        )

      if st.form_submit_button("💾 ડોક્યુમેન્ટ સાચવો", use_container_width=True):
        if uploaded_doc is not None:
          add_tenant_document(
              tenant_id=dt_id,
              doc_type=doc_type,
              file_name=uploaded_doc.name,
              mime_type=uploaded_doc.type or "application/octet-stream",
              file_blob=uploaded_doc.read(),
          )
          st.success(
              f"'{dt_name}' ({dt_unit}) માટે '{doc_type}' સફળતાપૂર્વક સેવ થઈ"
              " ગયું!"
          )
          st.rerun()
        else:
          st.error("કૃપા કરીને ડોક્યુમેન્ટ ફાઈલ પસંદ કરો.")

    st.divider()
    st.markdown(f"### 📂 {dt_name} ({dt_unit}) ના સાચવેલ ડોક્યુમેન્ટ્સ")

    docs_list = get_tenant_documents(dt_id)
    if not docs_list:
      st.info("આ ભાડુઆત માટે હજુ સુધી કોઈ ડોક્યુમેન્ટ સાચવેલ નથી.")
    else:
      for doc_id, d_type, f_name, m_type, f_blob, up_at in docs_list:
        st.markdown(
            f"""
            <div class="card-purple">
                <h4 style="color:#e9d5ff; margin-bottom:4px;">📄 {d_type}</h4>
                <p style="margin:2px 0; color:#e2e8f0;"><b>ફાઈલ:</b> {f_name} &nbsp;|&nbsp; <b>તારીખ:</b> {up_at}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "image" in (m_type or "").lower() or f_name.lower().endswith((
            ".jpg",
            ".jpeg",
            ".png",
        )):
          st.image(f_blob, caption=f"{d_type} - {f_name}", width=360)

        b_col1, b_col2 = st.columns([2, 1])
        with b_col1:
          st.download_button(
              label="📥 ડોક્યુમેન્ટ ડાઉનલોડ કરો",
              data=f_blob,
              file_name=f_name,
              mime=m_type or "application/octet-stream",
              key=f"dl_doc_{doc_id}",
          )
        with b_col2:
          if st.button("🗑️ ડિલીટ કરો", key=f"del_doc_{doc_id}"):
            delete_tenant_document(doc_id)
            st.success("ડોક્યુમેન્ટ ડિલીટ થઈ ગયું!")
            st.rerun()
        st.divider()

# ── TAB 3: MONTHLY RECEIPT MESSAGE ─────────────────────────────────
with tab3:
  st.subheader("🧾 દર મહિને ભાડાની રસીદ મેસેજ મોકલો")

  all_tenants = get_tenants()
  if not all_tenants:
    st.info("પહેલા 'ભાડુઆતોની યાદી અને હિસાબ' ટેબમાં ભાડુઆત ઉમેરો.")
  else:
    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
      r_tenant_map = {f"{t[1]} — રૂમ/મકાન: {t[3]}": t for t in all_tenants}
      r_sel_label = st.selectbox(
          "👤 ભાડુઆત પસંદ કરો:", list(r_tenant_map.keys()), key="rec_t_sel"
      )
    with r_col2:
      r_year = st.selectbox(
          "📅 વર્ષ:", [2025, 2026, 2027, 2028], index=1, key="rec_y_sel"
      )
    with r_col3:
      r_month_num = st.selectbox(
          "🗓️ મહિનો:",
          list(GUJARATI_MONTHS.keys()),
          format_func=lambda m: GUJARATI_MONTHS[m],
          index=10,
      )

    rt_row = r_tenant_map[r_sel_label]
    rt_id, rt_name, rt_phone, rt_unit, rt_rent, rt_deposit, rt_start, rt_notes = (
        rt_row
    )
    r_ledger = {row[1]: row for row in get_ledger(rt_id, r_year)}
    m_row = r_ledger.get(r_month_num)

    r_paid = m_row[2] if m_row else 0.0
    l_bill = m_row[3] if m_row else 0.0
    w_bill = m_row[4] if m_row else 0.0
    p_date = m_row[5] if m_row else ""
    m_status = m_row[6] if m_row else "બાકી"
    m_total = r_paid + l_bill + w_bill
    month_guj = GUJARATI_MONTHS[r_month_num]

    receipt_text = (
        f"🧾 *RAMAVAT HOME CARE - માસિક રસીદ*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 મહિનો: *{month_guj} {r_year}*\n"
        f"👤 ભાડુઆત: *{rt_name}*\n"
        f"🏡 મકાન/રૂમ: *{rt_unit}*\n"
        f"📌 સ્થિતિ: *{m_status}*\n"
        f"🗓️ તારીખ: *{p_date or '—'}*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏠 મકાન ભાડું: ₹{r_paid:,.0f}\n"
        f"💡 લાઈટ બિલ: ₹{l_bill:,.0f}\n"
        f"💧 પાણી બિલ: ₹{w_bill:,.0f}\n"
        f"💰 *કુલ રકમ: ₹{m_total:,.0f}*\n"
        f"🔒 ડિપોઝીટ: ₹{rt_deposit:,.0f}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"આભાર — *RAMAVAT HOME CARE*"
    )

    st.markdown("### 📄 રસીદ મેસેજ પ્રીવ્યુ")
    custom_receipt = st.text_area(
        "જરૂર પડે તો મેસેજમાં ફેરફાર કરી શકો છો:",
        value=receipt_text,
        height=310,
    )

    wa_receipt_link = build_whatsapp_url(rt_phone, custom_receipt)
    st.markdown(
        f"""
        <a href="{wa_receipt_link}" target="_blank" style="text-decoration:none;">
            <button class="wa-btn-3d">
                🟢 WhatsApp પર રસીદ મેસેજ મોકલો
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )
