import sqlite3
import urllib.parse
import streamlit as st

# ── DATABASE SETUP (ADS + TENANT RENT LEDGER) ──────────────────────
DB_FILE = "ramavat_direct_ads.db"


def init_db():
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
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
    # 2. Tenants Master Table
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
    # 3. Monthly Rent, Light & Water Ledger Table
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
    # 12 મહિના માટે ખાલી લેજર એન્ટ્રી તૈયાર કરવી
    for m in range(1, 13):
      c.execute(
          """
                INSERT OR IGNORE INTO rent_ledger (tenant_id, month_num, rent_paid, light_bill, water_bill, paid_date, status)
                VALUES (?, ?, 0, 0, 0, '', 'બાકી')
            """,
          (tenant_id, m),
      )


def get_tenants(year_filter=None):
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


def update_deposit(tenant_id, new_deposit):
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute(
        "UPDATE tenants SET deposit_amount = ? WHERE id = ?",
        (new_deposit, tenant_id),
    )
