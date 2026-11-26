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

# ── 3D THEME CSS ───────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 50%, #070b14 100%) !important;
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, span, label, p, .stMarkdown {
        color: #ffffff !important;
    }

    .hero-3d {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.94), rgba(15, 23, 42, 0.98));
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 20px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow:
            0 18px 35px -10px rgba(0, 0, 0, 0.65),
            0 0 24px rgba(56, 189, 248, 0.14),
            inset 0 1px 0 rgba(255, 255, 255, 0.14);
    }
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #34d399, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 4px;
        letter-spacing: 0.8px;
    }
    .sub-title {
        color: #cbd5e1 !important;
        font-size: 14px;
        text-align: center;
        margin-bottom: 0px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #162032 0%, #0d1422 100%) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.18);
    }

    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        color: #ffffff !important;
        background: linear-gradient(145deg, #0b1220, #131e33) !important;
        border: 1px solid rgba(148, 163, 184, 0.28) !important;
        border-radius: 12px !important;
    }

    .card-3d {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.96));
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding: 18px 22px;
        border-radius: 18px;
        margin-bottom: 16px;
        box-shadow:
            0 14px 28px -8px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 12px 14px;
        box-shadow: 0 10px 20px -6px rgba(0, 0, 0, 0.55);
    }

    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(145deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(125, 211, 252, 0.35) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 14px rgba(2, 132, 199, 0.35) !important;
    }

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
        box-shadow: 0 7px 16px rgba(22, 163, 74, 0.38);
    }

    div[data-testid="stExpander"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.75), rgba(15, 23, 42, 0.88));
        border: 1px solid rgba(148, 163, 184, 0.2);
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


def get_tenants(year_filter="બધા", search_q=""):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    like_q = f"%{search_q}%"
    if year_filter and year_filter != "બધા":
      c.execute(
          """
                SELECT * FROM tenants
                WHERE rent_year = ? AND (tenant_name LIKE ? OR unit_no LIKE ? OR phone LIKE ?)
                ORDER BY id DESC
            """,
          (int(year_filter), like_q, like_q, like_q),
      )
    else:
      c.execute(
          """
                SELECT * FROM tenants
                WHERE tenant_name LIKE ? OR unit_no LIKE ? OR phone LIKE ?
                ORDER BY id DESC
            """,
          (like_q, like_q, like_q),
      )
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


# ── SIDEBAR (LINE-BY-LINE QUICK DIRECTORY) ─────────────────────────
with st.sidebar:
  st.markdown("## 🏠 RAMAVAT HOME CARE")
  st.caption("ભાડુઆત યાદી, ડોક્યુમેન્ટ્સ અને માસિક રસીદ")
  st.divider()

  st.markdown("### 📋 ભાડુઆતોની લાઈનસર યાદી:")
  sidebar_tenants = get_tenants()
  if not sidebar_tenants:
    st.caption("હજુ કોઈ ભાડુઆત નોંધાયેલ નથી.")
  else:
    for idx, t in enumerate(sidebar_tenants, start=1):
      st.markdown(f"{idx}. **{t[1]}** — રૂમ/મકાન: `{t[3]}` (₹{t[5]:,.0f})")

  st.divider()
  st.markdown("### 📌 ઉપયોગ માર્ગદર્શિકા:")
  st.markdown("1. નવા ભાડુઆત અને ડિપોઝીટ ઉમેરો.")
  st.markdown("2. દર મહિનાનું ભાડું, લાઈટ અને પાણી ભરો.")
  st.markdown("3. આધાર કાર્ડ / ID ડોક્યુમેન્ટ્સ સાચવો.")
  st.markdown("4. WhatsApp પર માસિક રસીદ મોકલો.")

# ── HEADER ─────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-3d">
        <div class="main-title">RAMAVAT HOME CARE</div>
        <div class="sub-title">ભાડુઆતોની યાદી, કુલ ઓટોમેટિક સરવાળો, ડિપોઝીટ, ડોક્યુમેન્ટ્સ અને માસિક રસીદ</div>
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

# ── TAB 1: TENANTS LIST, ALL-TENANTS TOTAL & ANNUAL LEDGER ────────
with tab1:
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
        t_start = st.text_input("શરૂઆતની તારીખ (દા.ત. 01/11/2026):")
      with c5:
        t_notes = st.text_input("નોંધ (લાઈટ/પાણી/ડિપોઝીટ):")

      if st.form_submit_button("✅ ભાડુઆત યાદીમાં ઉમેરો", use_container_width=True):
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
          st.success(f"'{t_name}' ({t_unit}) યાદીમાં ઉમેરાઈ ગયા છે!")
          st.rerun()
        else:
          st.error("કૃપા કરીને ભાડુઆતનું નામ અને મકાન/રૂમ નંબર લખો.")

  st.divider()

  f1, f2, f3 = st.columns([1, 1, 2])
  with f1:
    year_choice = st.selectbox(
        "📅 વર્ષ:", ["બધા", "2025", "2026", "2027", "2028"]
    )
  with f2:
    search_tenant = st.text_input("🔍 નામ / રૂમ / મોબાઈલ શોધો:", "")

  # All tenants automatic grand summary for selected year
  all_year_tenants = get_tenants(year_filter=year_choice, search_q="")
  if all_year_tenants:
    all_dep_sum = sum(t[6] for t in all_year_tenants)
    all_rent_sum = 0.0
    all_light_sum = 0.0
    all_water_sum = 0.0

    for item in all_year_tenants:
      l_items = get_ledger(item[0])
      all_rent_sum += sum(r[2] for r in l_items)
      all_light_sum += sum(r[3] for r in l_items)
      all_water_sum += sum(r[4] for r in l_items)

    all_grand_sum = all_rent_sum + all_light_sum + all_water_sum

    st.markdown("### 📊 બધા ભાડુઆતોનો કુલ સરવાળો")
    g1, g2, g3, g4, g5, g6 = st.columns(6)
    g1.metric("👥 કુલ ભાડુઆત", f"{len(all_year_tenants)}")
    g2.metric("🔒 કુલ ડિપોઝીટ", f"₹ {all_dep_sum:,.0f}")
    g3.metric("🏠 કુલ ભાડું", f"₹ {all_rent_sum:,.0f}")
    g4.metric("💡 કુલ લાઈટ", f"₹ {all_light_sum:,.0f}")
    g5.metric("💧 કુલ પાણી", f"₹ {all_water_sum:,.0f}")
    g6.metric("💰 કુલ જમા", f"₹ {all_grand_sum:,.0f}")
    st.divider()

  tenants_list = get_tenants(year_filter=year_choice, search_q=search_tenant)

  if not tenants_list:
    st.info("હાલમાં કોઈ ભાડુઆત નોંધાયેલ નથી. ઉપરથી નવા ભાડુઆત ઉમેરો.")
  else:
    tenant_map = {
        f"{t[1]} — રૂમ/મકાન: {t[3]} ({t[4]})": t for t in tenants_list
    }
    with f3:
      selected_label = st.selectbox(
          "👤 ભાડુઆત પસંદ કરો:", list(tenant_map.keys())
      )

    t_row = tenant_map[selected_label]
    t_id, t_name, t_phone, t_unit, t_year, t_rent, t_deposit, t_start, t_notes = (
        t_row
    )

    st.markdown(
        f"""
        <div class="card-3d">
            <h3 style="color:#38bdf8; margin-bottom:6px;">👤 {t_name} &nbsp;|&nbsp; 🏡 મકાન/રૂમ: {t_unit}</h3>
            <p style="margin:4px 0;"><b>📞 મોબાઈલ:</b> {t_phone or "—"} &nbsp;|&nbsp; <b>📅 વર્ષ:</b> {t_year} &nbsp;|&nbsp; <b>🗓️ શરૂઆત:</b> {t_start or "—"}</p>
            <p style="margin:4px 0; color:#4ade80;"><b>માસિક ભાડું:</b> ₹ {t_rent:,.0f} &nbsp;|&nbsp; <b>ડિપોઝીટ:</b> ₹ {t_deposit:,.0f}</p>
            <p style="margin:6px 0 0 0; color:#cbd5e1;"><b>નોંધ:</b> {t_notes or "—"}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("💰 ડિપોઝીટ / માસિક ભાડું / નોંધ અપડેટ કરો"):
      with st.form(f"upd_tenant_{t_id}"):
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

        if st.form_submit_button("💾 અપડેટ કરો", use_container_width=True):
          update_tenant_details(t_id, upd_rent, upd_dep, upd_notes)
          st.success("વિગતો અપડેટ થઈ ગઈ!")
          st.rerun()

    ledger_rows = get_ledger(t_id)
    total_rent_paid = sum(r[2] for r in ledger_rows)
    total_light = sum(r[3] for r in ledger_rows)
    total_water = sum(r[4] for r in ledger_rows)
    grand_total = total_rent_paid + total_light + total_water

    st.markdown(f"### 📈 {t_name} નો વાર્ષિક સરવાળો")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("🔒 ડિપોઝીટ", f"₹ {t_deposit:,.0f}")
    m2.metric("🏠 કુલ ભરેલ ભાડું", f"₹ {total_rent_paid:,.0f}")
    m3.metric("💡 કુલ લાઈટ બિલ", f"₹ {total_light:,.0f}")
    m4.metric("💧 કુલ પાણી બિલ", f"₹ {total_water:,.0f}")
    m5.metric("📊 કુલ જમા", f"₹ {grand_total:,.0f}")

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

    with st.expander("🗑️ આ ભાડુઆતને યાદીમાંથી ડિલીટ કરો"):
      if st.button("🗑️ કાયમ માટે ડિલીટ કરો", key=f"del_t_{t_id}"):
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
    doc_t_map = {
        f"{t[1]} — રૂમ/મકાન: {t[3]} ({t[4]})": t for t in all_tenants_doc
    }
    doc_sel_label = st.selectbox(
        "👤 ભાડુઆત પસંદ કરો:", list(doc_t_map.keys()), key="doc_t_sel"
    )
    dt_row = doc_t_map[doc_sel_label]
    dt_id, dt_name, _, dt_unit, dt_year, *_ = dt_row

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
            <div class="card-3d">
                <h4 style="color:#38bdf8; margin-bottom:4px;">📄 {d_type}</h4>
                <p style="margin:2px 0; color:#cbd5e1;"><b>ફાઈલ:</b> {f_name} &nbsp;|&nbsp; <b>તારીખ:</b> {up_at}</p>
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
    r_col1, r_col2 = st.columns(2)
    with r_col1:
      r_tenant_map = {f"{t[1]} — રૂમ/મકાન: {t[3]} ({t[4]})": t for t in all_tenants}
      r_sel_label = st.selectbox(
          "👤 ભાડુઆત પસંદ કરો:", list(r_tenant_map.keys()), key="rec_t_sel"
      )
    with r_col2:
      r_month_num = st.selectbox(
          "📅 મહિનો પસંદ કરો:",
          list(GUJARATI_MONTHS.keys()),
          format_func=lambda m: GUJARATI_MONTHS[m],
          index=10,
      )

    rt_row = r_tenant_map[r_sel_label]
    rt_id, rt_name, rt_phone, rt_unit, rt_year, rt_rent, rt_deposit, rt_start, rt_notes = (
        rt_row
    )
    r_ledger = {row[1]: row for row in get_ledger(rt_id)}
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
        f"📅 મહિનો: *{month_guj} {rt_year}*\n"
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
