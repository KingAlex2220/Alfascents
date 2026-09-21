from datetime import datetime
import os
import random
import sqlite3
import string
import pandas as pd
import streamlit as st

# Email imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Default image path resolved directly on the root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
DEFAULT_PRODUCT_IMAGE = os.path.join(ROOT_DIR, "image.png")

# ==========================================
# FRAGRANCES DICTIONARY (CHANEL IMPRESSIONS)
# ==========================================
fragrances = {
    # ---------------- MEN'S COLLECTION ----------------
    "bleu_de_chanel_edp": {
        "name": "Bleu de Chanel Impression (EDP)",
        "impression_of": "Chanel - Bleu de Chanel Eau de Parfum",
        "designer": "Chanel",
        "gender": "Men",
        "badge_primary": "Signature",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Grapefruit", "Lemon", "Mint", "Pink Pepper"],
            "heart_notes": ["Ginger", "Iso E Super"],
            "base_notes": ["Cedar", "Sandalwood"],
        },
        "description": "A refined, fresh woody-aromatic fragrance blending vibrant citrus, spicy ginger, and rich cedar sandalwood undertones.",
    },
    "bleu_de_chanel_parfum": {
        "name": "Bleu de Chanel Parfum Impression",
        "impression_of": "Chanel - Bleu de Chanel Parfum",
        "designer": "Chanel",
        "gender": "Men",
        "badge_primary": "Intense",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Lemon Zest", "Bergamot", "Mint"],
            "heart_notes": ["Lavender", "Pineapple"],
            "base_notes": ["Cedar", "Sandalwood"],
        },
        "description": "An intense and deep interpretation featuring crisp lemon zest, aromatic lavender, and smooth, velvety woods.",
    },
    "allure_homme_sport": {
        "name": "Allure Homme Sport Impression",
        "impression_of": "Chanel - Allure Homme Sport",
        "designer": "Chanel",
        "gender": "Men",
        "badge_primary": "Sport",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Orange", "Sea Notes", "Mandarin"],
            "heart_notes": ["Pepper", "Neroli"],
            "base_notes": ["Cedar", "Tonka Bean", "Vanilla"],
        },
        "description": "An invigorating aquatic-fresh blend accented by crisp citrus, spicy pepper, and a warm tonka bean vanilla finish.",
    },
    "egoiste_platinum": {
        "name": "Égoïste Platinum Impression",
        "impression_of": "Chanel - Égoïste Platinum",
        "designer": "Chanel",
        "gender": "Men",
        "badge_primary": "Fresh Aromatic",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Lavender", "Rosemary", "Neroli", "Petitgrain"],
            "heart_notes": ["Geranium", "Clary Sage"],
            "base_notes": ["Cedarwood"],
        },
        "description": "A crisp, herbal, and metallic-fresh composition highlighting alpine lavender, clary sage, and structured cedarwood.",
    },
    "allure_homme_edition_blanche": {
        "name": "Allure Homme Édition Blanche Impression",
        "impression_of": "Chanel - Allure Homme Édition Blanche",
        "designer": "Chanel",
        "gender": "Men",
        "badge_primary": "Citrus Oriental",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Lemon", "Bergamot"],
            "heart_notes": ["Sandalwood"],
            "base_notes": ["Madagascar Vanilla", "Vetiver", "Amber"],
        },
        "description": "A creamy citrus-gourmand balance of sparkling lemon, buttery sandalwood, and sweet Madagascar vanilla.",
    },
    "antaeus_pour_homme": {
        "name": "Antaeus Pour Homme Impression",
        "impression_of": "Chanel - Antaeus Pour Homme",
        "designer": "Chanel",
        "gender": "Men",
        "badge_primary": "Classic Bold",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Myrrh", "Clary Sage", "Thyme", "Basil"],
            "heart_notes": ["Coriander", "Rose"],
            "base_notes": ["Patchouli", "Oakmoss"],
        },
        "description": "A powerful, masculine leather-chypre scent driven by aromatic myrrh, dark patchouli, and earthy oakmoss.",
    },
    # ---------------- WOMEN'S COLLECTION ----------------
    "coco_mademoiselle": {
        "name": "Coco Mademoiselle Impression",
        "impression_of": "Chanel - Coco Mademoiselle",
        "designer": "Chanel",
        "gender": "Women",
        "badge_primary": "Best Seller",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Orange", "Mandarin Orange", "Bergamot"],
            "heart_notes": ["Turkish Rose", "Jasmine"],
            "base_notes": ["Patchouli", "Vetiver"],
        },
        "description": "An elegant, modern oriental blend featuring bright citrus blossoms, delicate Turkish rose, and deep patchouli.",
    },
    "chanel_no5": {
        "name": "Chanel N°5 Impression",
        "impression_of": "Chanel - Chanel N°5",
        "designer": "Chanel",
        "gender": "Women",
        "badge_primary": "Iconic Classic",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Aldehydes", "Ylang-Ylang", "Neroli", "Bergamot"],
            "heart_notes": ["Iris", "Jasmine", "Rose"],
            "base_notes": ["Sandalwood"],
        },
        "description": "A timeless floral-aldehyde masterpiece with rich ylang-ylang, powdery iris, velvet jasmine, and smooth sandalwood.",
    },
    "chance_eau_tendre": {
        "name": "Chance Eau Tendre Impression",
        "impression_of": "Chanel - Chance Eau Tendre",
        "designer": "Chanel",
        "gender": "Women",
        "badge_primary": "Floral Fruity",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Quince", "Grapefruit"],
            "heart_notes": ["Rose", "Jasmine"],
            "base_notes": ["White Musk"],
        },
        "description": "A soft, romantic fruity-floral fragrance radiating juicy quince, delicate jasmine petals, and clean white musk.",
    },
    "chance_eau_fraiche": {
        "name": "Chance Eau Fraîche Impression",
        "impression_of": "Chanel - Chance Eau Fraîche",
        "designer": "Chanel",
        "gender": "Women",
        "badge_primary": "Zesty Fresh",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Citron"],
            "heart_notes": ["Jasmine"],
            "base_notes": ["Cedar", "Teakwood", "Amber", "Patchouli"],
        },
        "description": "A sparkling, energetic floral-sparkle composition built on zesty citron, airy jasmine, and warm teakwood.",
    },
    "coco_noir": {
        "name": "Coco Noir Impression",
        "impression_of": "Chanel - Coco Noir",
        "designer": "Chanel",
        "gender": "Women",
        "badge_primary": "Night Collection",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Grapefruit", "Bergamot"],
            "heart_notes": ["Rose", "Jasmine", "Geranium"],
            "base_notes": ["Patchouli", "Tonka Bean", "Vanilla"],
        },
        "description": "A luminous, seductive night scent fusing dark rose floral notes with magnetic patchouli and rich tonka vanilla.",
    },
    "gabrielle_chanel": {
        "name": "Gabrielle Chanel Impression",
        "impression_of": "Chanel - Gabrielle Chanel",
        "designer": "Chanel",
        "gender": "Women",
        "badge_primary": "Radiant Floral",
        "badge_secondary": "60ml Polymer",
        "scent_profile": {
            "top_notes": ["Grapefruit", "Mandarin", "Blackcurrant"],
            "heart_notes": ["Orange Blossom", "Jasmine", "Ylang-Ylang"],
            "base_notes": ["White Musk"],
        },
        "description": "A luminous solar floral arrangement woven around creamy white orange blossom, exotic ylang-ylang, and jasmine.",
    },
}

# ==========================================
# AUTOMATICALLY BUILD STREAMLINED CATALOG (POLYMER ONLY)
# ==========================================
FRAGRANCE_CATALOG = []
for key, data in fragrances.items():
    sp = data.get("scent_profile", {})

    FRAGRANCE_CATALOG.append({
        "id": f"{key}_polymer",
        "name": data['name'],
        "designer": data.get('designer', 'Chanel'),
        "gender": data["gender"],
        "badge_primary": data["badge_primary"],
        "badge_secondary": data.get("badge_secondary", "60ml Polymer"),
        "category": f"60ml Shatter-Proof Precision Polymer • Impression of {data['impression_of']}",
        "price": 30.0,
        "edition_type": "Precision Polymer",
        "bottle_type": "60ml Shatter-Proof Precision Polymer",
        "notes": f"60ml Featherlight Precision-Crafted Polymer (Shatter-Proof Bottle). {data['description']}",
        "scent_profile": sp,
        "image_url": DEFAULT_PRODUCT_IMAGE
    })

# ==========================================
# PAGE CONFIGURATION & LUXURY BOUTIQUE STYLING
# ==========================================
st.set_page_config(
    page_title="ALFA SCENTS | Luxury Boutique Marketplace",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <!-- Safari UI Blending Tags -->
    <meta name="theme-color" content="#0d0f12">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-capable" content="yes">

    <style>
    /* HIDE STREAMLIT TOP HEADER TOOLBAR */
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0rem !important;
    }
    
    :root {
        --bg-color: #0d0f12;
        --card-bg: #161a22;
        --gold-primary: #d4af37;
        --gold-light: #f3e5ab;
        --text-main: #f0f2f5;
        --text-muted: #9aa0a6;
        --border-color: rgba(212, 175, 55, 0.2);
    }
    
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-main);
    }

    .market-nav-bar {
        background-color: #111418;
        padding: 18px 20px;
        border-bottom: 2px solid var(--gold-primary);
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .market-sub-banner {
        background: linear-gradient(135deg, #1a1e28 0%, #111418 100%);
        border: 1px solid var(--border-color);
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }

    .luxury-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .luxury-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.15);
        border-color: rgba(212, 175, 55, 0.5);
    }

    .badge-signature {
        background-color: #d4af37;
        color: #000000;
        padding: 3px 8px;
        font-weight: bold;
        font-size: 0.70rem;
        border-radius: 4px;
        letter-spacing: 1px;
    }
    .badge-offer {
        background-color: #2c3e50;
        color: #f3e5ab;
        border: 1px solid #d4af37;
        padding: 3px 8px;
        font-weight: bold;
        font-size: 0.70rem;
        border-radius: 4px;
    }

    .luxury-impression-stamp {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.12) 0%, rgba(26, 30, 40, 0.6) 100%);
        border: 1px dashed rgba(212, 175, 55, 0.4);
        padding: 10px 14px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.3);
    }
    .luxury-impression-stamp span {
        font-family: 'Cinzel', serif;
        color: #f3e5ab;
        font-size: 0.82rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 600;
    }

    .stTextInput input, .stTextArea textarea, div[data-baseweb="input"] input, div[data-baseweb="select"] span {
        color: var(--text-main) !important;
        -webkit-text-fill-color: var(--text-main) !important;
        background-color: #1a1e28 !important;
        border-color: var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d4af37 0%, #aa8c2c 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        letter-spacing: 0.8px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 100%) !important;
        box-shadow: 0 6px 16px rgba(212, 175, 55, 0.5);
    }

    [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
        background-color: var(--card-bg) !important;
        border-radius: 10px;
        border: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid var(--border-color);
    }
    </style>

    <div class="market-nav-bar">
        <div style="width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
            <div style="font-family: 'Cinzel', serif; color: var(--gold-primary); font-size: 2.2rem; font-weight: bold; line-height: 1; margin-bottom: 4px;">
                ALFA SCENTS
            </div>
            <div style="font-family: 'Cinzel', serif; color: var(--gold-primary); font-size: 1.8rem; font-weight: bold; letter-spacing: 2px; line-height: 1;">
                LUXURY BOUTIQUE <span style="font-size: 0.85rem; color: #9aa0a6; font-weight: normal; display: inline-block; margin-left: 8px; font-family: sans-serif; letter-spacing: 0px;">| Marketplace</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# DATABASE SETUP & AUTO-MIGRATION
# ==========================================
DB_FILE = "alfa_scents.db"
DEFAULT_STOCK_PER_ITEM = 5


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        try:
            c.execute("SELECT item_id FROM inventory LIMIT 1")
        except sqlite3.OperationalError:
            c.execute("DROP TABLE IF EXISTS inventory")
            c.execute("DROP TABLE IF EXISTS orders")

        c.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_date TEXT,
                customer_name TEXT,
                customer_email TEXT,
                customer_phone TEXT,
                shipping_address TEXT,
                items_summary TEXT,
                total_qty INTEGER,
                subtotal REAL,
                discount_applied REAL,
                final_total REAL,
                payment_method TEXT,
                status TEXT,
                is_priority INTEGER DEFAULT 0,
                cycle_id TEXT,
                notes TEXT,
                referral_code TEXT
            )
        """)

        c.execute("PRAGMA table_info(orders)")
        existing_cols = [col[1] for col in c.fetchall()]

        if "is_priority" not in existing_cols:
            c.execute("ALTER TABLE orders ADD COLUMN is_priority INTEGER DEFAULT 0")
        if "cycle_id" not in existing_cols:
            c.execute("ALTER TABLE orders ADD COLUMN cycle_id TEXT")
        if "notes" not in existing_cols:
            c.execute("ALTER TABLE orders ADD COLUMN notes TEXT")
        if "referral_code" not in existing_cols:
            c.execute("ALTER TABLE orders ADD COLUMN referral_code TEXT")

        c.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item_id TEXT PRIMARY KEY,
                item_name TEXT,
                stock_level INTEGER,
                initial_stock INTEGER
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS gift_cards (
                code TEXT PRIMARY KEY,
                initial_value REAL,
                current_balance REAL,
                purchaser_name TEXT,
                recipient_email TEXT,
                status TEXT,
                created_date TEXT,
                payment_method TEXT
            )
        """)

        c.execute("PRAGMA table_info(gift_cards)")
        existing_gc_cols = [col[1] for col in c.fetchall()]
        if "payment_method" not in existing_gc_cols:
            c.execute("ALTER TABLE gift_cards ADD COLUMN payment_method TEXT")

        c.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_date TEXT,
                customer_name TEXT,
                rating INTEGER,
                item_id TEXT,
                review_text TEXT,
                is_approved INTEGER DEFAULT 1
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS marketing_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                name TEXT,
                phone TEXT,
                source_tag TEXT,
                captured_date TEXT,
                status TEXT DEFAULT 'Subscriber'
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS campaign_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_name TEXT,
                recipient_email TEXT,
                sent_date TEXT,
                status TEXT
            )
        """)


init_db()


def switch_to_checkout_tab():
    st.session_state["target_tab"] = "🛒 Checkout & Invoice"
    st.session_state["main_navigation_radio"] = "🛒 Checkout & Invoice"
    st.toast("Redirecting to Secure Boutique Checkout... 🛍️", icon="💳")
    st.rerun()


# ==========================================
# GLOBAL DISCLAIMERS & HELPERS
# ==========================================
DISCLAIMER_TEXT = (
    "ALFA SCENTS offers proprietary, independently formulated scents"
    " inspired by popular fragrance profiles. Any reference to scent families or"
    " style impressions is strictly for descriptive purposes to give"
    " customers an idea of the olfactory notes. ALFA SCENTS does not use"
    " third-party trademarked names, nor are our products affiliated with,"
    " endorsed by, or sponsored by any third-party brands or manufacturers."
)

ALLERGY_DISCLAIMER_TEXT = (
    "⚠️ ALLERGY & SKIN SENSITIVITY NOTICE: ALFA SCENTS products contain"
    " concentrated fragrance oils, essential oils, and aromatic compounds."
    " Please perform a patch test on a small area of skin before full"
    " application. Discontinue use immediately if redness, irritation, or"
    " itching occurs. Avoid contact with eyes, damaged skin, or open wounds."
    " Do not ingest. Keep out of reach of children and pets. ALFA SCENTS"
    " assumes no liability for adverse allergic reaction or skin sensitivities."
)


def sync_inventory_defaults():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        for item in FRAGRANCE_CATALOG:
            c.execute("SELECT stock_level FROM inventory WHERE item_id = ?", (item["id"],))
            row = c.fetchone()
            if not row:
                c.execute(
                    "INSERT INTO inventory (item_id, item_name, stock_level, initial_stock) VALUES (?, ?, ?, ?)",
                    (item["id"], item["name"], DEFAULT_STOCK_PER_ITEM, DEFAULT_STOCK_PER_ITEM),
                )


sync_inventory_defaults()


def get_current_30_day_cycle():
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    days_passed = (now - start_of_year).days
    cycle_num = (days_passed // 30) + 1
    return f"CYCLE-{now.year}-30D-{cycle_num:02d}"


def save_order_to_db(
    name, email, phone, address, items_summary, qty, subtotal, discount, total,
    payment_method, is_priority, notes, cart_items, referral_code=""
):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cycle_id = get_current_30_day_cycle()
        status = "Payment Sent / Pending Verification" if is_priority else "Pending"

        c.execute(
            """
            INSERT INTO orders (
                order_date, customer_name, customer_email, customer_phone, 
                shipping_address, items_summary, total_qty, subtotal, 
                discount_applied, final_total, payment_method, status, is_priority, cycle_id, notes, referral_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                order_date, name, email, phone, address, items_summary, qty, subtotal,
                discount, total, payment_method, status, int(is_priority), cycle_id, notes, referral_code
            ),
        )

        for item_id, item_qty in cart_items.items():
            c.execute(
                "UPDATE inventory SET stock_level = stock_level - ? WHERE item_id = ?",
                (item_qty, item_id),
            )
            
        if email:
            c.execute("""
                INSERT OR IGNORE INTO marketing_leads (email, name, phone, source_tag, captured_date)
                VALUES (?, ?, ?, ?, ?)
            """, (email, name, phone, referral_code, order_date))


def search_orders(query, is_admin=False):
    with sqlite3.connect(DB_FILE) as conn:
        q = f"%{query}%"
        if is_admin:
            df = pd.read_sql_query(
                "SELECT * FROM orders WHERE id LIKE ? OR customer_name LIKE ? OR customer_email LIKE ? OR customer_phone LIKE ? ORDER BY id DESC",
                conn, params=(q, q, q, q),
            )
        else:
            df = pd.read_sql_query(
                "SELECT id, order_date, customer_name, items_summary, total_qty, final_total, status, is_priority, cycle_id, referral_code FROM orders WHERE customer_email LIKE ? OR customer_phone LIKE ? ORDER BY id DESC",
                conn, params=(q, q),
            )
    return df


def get_inventory_status():
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM inventory", conn)
    return df


def update_item_stock(item_id, new_stock):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE inventory SET stock_level = ? WHERE item_id = ?", (new_stock, item_id))


def get_gift_card(code):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM gift_cards WHERE code = ?", (code,))
        row = c.fetchone()
    return row


def save_review(customer_name, rating, item_id, review_text):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        review_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO reviews (review_date, customer_name, rating, item_id, review_text, is_approved) VALUES (?, ?, ?, ?, ?, 1)",
            (review_date, customer_name, rating, item_id, review_text),
        )


def get_approved_reviews(item_id=None):
    with sqlite3.connect(DB_FILE) as conn:
        if item_id and item_id != "All":
            df = pd.read_sql_query("SELECT * FROM reviews WHERE is_approved = 1 AND item_id = ? ORDER BY id DESC", conn, params=(item_id,))
        else:
            df = pd.read_sql_query("SELECT * FROM reviews WHERE is_approved = 1 ORDER BY id DESC", conn)
    return df


@st.cache_data(ttl=600)
def load_google_sheet_inventory(sheet_name):
    sheet_id = "1YIW7pgSdBxmhToYChyPJmlplw2qljcOJ4zpGMbUF2aQ"
    import urllib.parse
    encoded_name = urllib.parse.quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
    try:
        df = pd.read_csv(url).fillna("")
        return df
    except Exception as e:
        print(f"Sheet Importer Debug Alert: {e}")
        return None

# ==========================================
# SESSION STATE & CART MANAGEMENT
# ==========================================
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "applied_gift_card" not in st.session_state:
    st.session_state.applied_gift_card = None
if "gift_card_discount" not in st.session_state:
    st.session_state.gift_card_discount = 0.0


def add_to_cart(item_id):
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id] += 1
    else:
        st.session_state.cart[item_id] = 1
    
    curr_qty = sum(st.session_state.cart.values())
    st.toast(f"Added to Shopping Bag! ({curr_qty} item(s) in bag)", icon="🛍️")


# ==========================================
# AFFILIATE & PAYMENT MAPPING
# ==========================================
PARTNER_MAPPING = {
    "alex": "Alexander Thompson",
    "jameka": "Jameka Hatton",
    "ray": "Ira Ray Thompson",
    "eq": "Eric Dior",
    "eric": "Eric Dior",
}

ZELLE_ACCOUNTS = {
    "ray": {"name": "Ira Ray Thompson", "identifier": "4079126043"},
}
DEFAULT_ZELLE_KEY = "ray"

VENMO_ACCOUNTS = {}
DEFAULT_VENMO_KEY = "ray"

CASHAPP_ACCOUNTS = {}
DEFAULT_CASHAPP_KEY = "ray"

APPLEPAY_ACCOUNTS = {
    "ray": {"name": "Ira Ray Thompson", "identifier": "407-912-6043"},
}
DEFAULT_APPLEPAY_KEY = "ray"

query_params = st.query_params
raw_ref = query_params.get("ref", "").strip().lower()

if raw_ref in PARTNER_MAPPING:
    st.session_state["active_ref_key"] = raw_ref
    st.session_state["active_ref"] = PARTNER_MAPPING[raw_ref]
elif raw_ref:
    st.session_state["active_ref_key"] = raw_ref
    st.session_state["active_ref"] = raw_ref
else:
    if "active_ref" not in st.session_state:
        st.session_state["active_ref_key"] = DEFAULT_ZELLE_KEY
        st.session_state["active_ref"] = ""

current_ref_key = st.session_state.get("active_ref_key", DEFAULT_ZELLE_KEY)
current_ref_tag = st.session_state.get("active_ref", "")

active_zelle = ZELLE_ACCOUNTS.get(current_ref_key, ZELLE_ACCOUNTS.get(DEFAULT_ZELLE_KEY, {"name": "Boutique Account", "identifier": "Contact for payment"}))
active_venmo = VENMO_ACCOUNTS.get(current_ref_key, VENMO_ACCOUNTS.get(DEFAULT_VENMO_KEY, {"name": "Boutique Account", "identifier": "Contact for payment"}))
active_cashapp = CASHAPP_ACCOUNTS.get(current_ref_key, CASHAPP_ACCOUNTS.get(DEFAULT_CASHAPP_KEY, {"name": "Boutique Account", "identifier": "Contact for payment"}))
active_applepay = APPLEPAY_ACCOUNTS.get(current_ref_key, APPLEPAY_ACCOUNTS.get(DEFAULT_APPLEPAY_KEY, {"name": "Boutique Account", "identifier": "Contact for payment"}))


def send_order_emails(customer_name, customer_email, total_due, items_summary, payment_method, referral_tag):
    SENDER_EMAIL = "alfascents@gmail.com"
    APP_PASSWORD = st.secrets.get("SMTP_PASSWORD", "dkif qgwv psyr qiig")
    ADMIN_EMAIL = "alfascents@gmail.com"
    
    msg_customer = MIMEMultipart()
    msg_customer["From"] = SENDER_EMAIL
    msg_customer["To"] = customer_email
    msg_customer["Subject"] = "✨ ALFA SCENTS - Luxury Boutique Order Receipt"
    
    customer_html = f"""
    <h3>Hi {customer_name}, thank you for your luxury purchase!</h3>
    <p>We have successfully received your order processing request in our system.</p>
    <hr/>
    <p><b>Items Ordered:</b> {items_summary}</p>
    <p><b>Total Balance Due:</b> ${total_due:.2f}</p>
    <p><b>Selected Payment Channel:</b> {payment_method}</p>
    <hr/>
    <p>If you selected Venmo, Cash App, or Apple Pay, please verify that your mobile transaction has been completed.</p>
    <p>Thank you for choosing luxury impressions!</p>
    """
    msg_customer.attach(MIMEText(customer_html, "html"))

    msg_admin = MIMEMultipart()
    msg_admin["From"] = SENDER_EMAIL
    msg_admin["To"] = ADMIN_EMAIL
    msg_admin["Subject"] = f"🚨 NEW BOUTIQUE ORDER RECEIVED - Ref: {referral_tag}"
    
    admin_html = f"""
    <h3>New Order Details for Production Ledger:</h3>
    <p><b>Customer Name:</b> {customer_name}</p>
    <p><b>Contact Inbox:</b> {customer_email}</p>
    <p><b>Purchased Items:</b> {items_summary}</p>
    <p><b>Final Invoice Total:</b> ${total_due:.2f}</p>
    <p><b>Payment Platform:</b> {payment_method}</p>
    <p><b>Attributed Affiliate Partner Link:</b> {referral_tag if referral_tag else 'Direct Storefront'}</p>
    """
    msg_admin.attach(MIMEText(admin_html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, customer_email, msg_customer.as_string())
            server.sendmail(SENDER_EMAIL, ADMIN_EMAIL, msg_admin.as_string())
    except Exception as e:
        print(f"SMTP Automation Error: {e}")


# ==========================================
# AUTOMATED MARKETING CAMPAIGN FUNCTIONS
# ==========================================
def send_marketing_campaign_email(recipient_email, recipient_name, campaign_type):
    SENDER_EMAIL = "alfascents@gmail.com"
    APP_PASSWORD = st.secrets.get("SMTP_PASSWORD", "dkif qgwv psyr qiig")
    
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    
    if campaign_type == "abandoned_cart":
        msg["Subject"] = "✨ Complete Your ALFA SCENTS Order – Exclusive Perks Inside!"
        html_content = f"""
        <h3>Hi {recipient_name},</h3>
        <p>We noticed you left some luxury impressions in your shopping bag at ALFA SCENTS.</p>
        <p>Complete your order today and use code <b>LUXURY10</b> for an extra special touch on your bespoke scents!</p>
        <p><a href="https://alfascents.streamlit.app/" style="background: #d4af37; color: #000; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 5px;">Return to Checkout</a></p>
        <p>Warm regards,<br><b>ALFA SCENTS Boutique Team</b></p>
        """
    elif campaign_type == "winback":
        msg["Subject"] = "✨ Discover Our Latest Impressions at ALFA SCENTS"
        html_content = f"""
        <h3>Hello {recipient_name},</h3>
        <p>It's been a while since your last sensory journey with ALFA SCENTS. Explore our 60ml Shatter-Proof Precision Polymer Editions!</p>
        <p><b>Special Offer:</b> Buy 3 bottles and pick a 4th bottle for free across our entire catalog.</p>
        <p><a href="https://alfascents.streamlit.app/" style="background: #d4af37; color: #000; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 5px;">Explore Collection</a></p>
        """
    else:
        return False

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
            
            with sqlite3.connect(DB_FILE) as conn_log:
                c_log = conn_log.cursor()
                c_log.execute(
                    "INSERT INTO campaign_logs (campaign_name, recipient_email, sent_date, status) VALUES (?, ?, ?, ?)",
                    (campaign_type, recipient_email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Sent Successfully")
                )
        return True
    except Exception as e:
        print(f"Marketing Email Error: {e}")
        return False


# ==========================================
# SIDEBAR NAVIGATION & CONTROLS
# ==========================================
st.sidebar.title("✨ Luxury Boutique Hub")
st.sidebar.caption("All Bottles $30 • Special Buy 3 Get 1 Free")

if current_ref_tag:
    st.sidebar.success(f"🔗 Partner Tracking Ref: **{current_ref_tag}**")

search_term = st.sidebar.text_input("🔍 Search Boutique Catalog...", "").lower()
selected_gender = st.sidebar.radio("Department Filter", ["All", "Men", "Women", "Unisex"])
priority_only = st.sidebar.checkbox("🔥 Show Priority Preorders Only")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 Quick Payment Options")

pay_tab1, pay_tab2, pay_tab3, pay_tab4 = st.sidebar.tabs(["Cash App", "Venmo", "Zelle", "Apple Pay"])

with pay_tab1:
    st.markdown(f"**{active_cashapp['name']}**")
    st.markdown("Please submit payment using Cash App.")

with pay_tab2:
    st.markdown(f"**{active_venmo['name']}**")
    st.markdown("Please submit payment using Venmo.")

with pay_tab3:
    st.markdown(f"**{active_zelle['name']}**")
    if active_zelle.get("identifier") and active_zelle["identifier"] != "Contact for payment":
        st.markdown(f"Phone/ID: `{active_zelle['identifier']}`")
    else:
        st.markdown("Please submit payment using Zelle.")

with pay_tab4:
    st.markdown(f"**{active_applepay['name']}**")
    if active_applepay.get("identifier") and active_applepay["identifier"] != "Contact for payment":
        st.markdown(f"Apple Pay Number: `{active_applepay['identifier']}`")
    else:
        st.markdown("Please submit payment using Apple Pay.")

# ==========================================
# SIDEBAR - SHOPPING BAG SUMMARY
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("🛒 Shopping Bag Summary")

total_qty = sum(st.session_state.cart.values())

raw_subtotal = 0.0
bottle_count = 0

for i_id, qty in st.session_state.cart.items():
    bottle_count += qty

sets = bottle_count // 4
remainder = bottle_count % 4
raw_subtotal = ((sets * 3) + remainder) * 30.0

discount_labels = []
if sets > 0:
    discount_labels.append(f"Buy 3 Get 1 Free: {sets} Free Bottle(s) Applied")

shipping_fee = 0.0
if 0 < raw_subtotal < 60.0:
    shipping_fee = 5.0

final_subtotal = max(0.0, raw_subtotal + shipping_fee - st.session_state.gift_card_discount)
discount_summary_str = " | ".join(discount_labels) if discount_labels else "Standard Pricing ($30 ea.)"

st.sidebar.write(f"**Items in Bag:** {total_qty} bottle(s)")
st.sidebar.write(f"**Promotions:** {discount_summary_str}")
if raw_subtotal >= 60.0:
    st.sidebar.write("**Shipping:** 🎉 **FREE SHIPPING ($60+ order)**")
elif raw_subtotal > 0:
    st.sidebar.write("**Shipping:** $5.00 fee ($30 order)")
else:
    st.sidebar.write("**Shipping:** $0.00")

if st.session_state.applied_gift_card:
    st.sidebar.write(f"**Gift Card Applied:** -${st.session_state.gift_card_discount:.2f}")
st.sidebar.subheader(f"Total: ${final_subtotal:.2f}")

if total_qty > 0:
    st.sidebar.button(
        "⚡ Proceed to Checkout",
        key="sidebar_checkout_fast_btn",
        type="primary",
        use_container_width=True,
        on_click=switch_to_checkout_tab
    )

# ==========================================
# MAIN INTERFACE HERO & TOP TAB CONTROLLER
# ==========================================
filtered_catalog = FRAGRANCE_CATALOG

if selected_gender != "All":
    filtered_catalog = [x for x in filtered_catalog if x["gender"] == selected_gender]

if search_term:
    filtered_catalog = [
        x for x in filtered_catalog
        if search_term in x["name"].lower()
        or search_term in x["notes"].lower()
        or search_term in x["category"].lower()
    ]

inventory_df = get_inventory_status().set_index("item_id")

if priority_only:
    filtered_catalog = [
        x for x in filtered_catalog
        if (inventory_df.loc[x["id"], "stock_level"] if x["id"] in inventory_df.index else 5) <= 0
    ]

all_tab_names = [
    "✨ Signature Blends",
    "📦 Full Inventory",
    "🎁 Gift Cards",
    "⭐ Reviews & Testimonials",
    "🛒 Checkout & Invoice",
    "🔍 Customer Order Lookup",
]

if "target_tab" in st.session_state and st.session_state["target_tab"] in all_tab_names:
    active_tab = st.session_state["target_tab"]
else:
    active_tab = all_tab_names[0]

selected_nav = st.radio(
    "Navigation Bar",
    all_tab_names,
    index=all_tab_names.index(active_tab),
    horizontal=True,
    key="main_navigation_radio",
    label_visibility="collapsed"
)

st.session_state["target_tab"] = selected_nav

# ------------------------------------------
# TAB 1: SIGNATURE BLENDS
# ------------------------------------------
if selected_nav == "✨ Signature Blends":
    st.markdown("""
    <div class="market-sub-banner">
        <h4 style='color: #d4af37; margin-top: 0; margin-bottom: 8px;'>✨ Special Store Offers & Shipping</h4>
        <ul style='margin-bottom: 0; padding-left: 20px; line-height: 1.6; color: #f0f2f5;'>
            <li><b>Flat Bottle Price:</b> All luxury bottles are <b>$30.00</b> each.</li>
            <li><b>Special Offer (Buy 3, Get 1 Free):</b> Add 4 bottles to your bag and pay for only 3.</li>
            <li><b>Free Shipping:</b> Automatically applied on orders of <b>$60.00 or more</b> (only a $5 shipping fee applies for single $30 orders).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "💡 **Looking for something else?** Head over to the **📦 Full Inventory** tab above to explore our full scent library, request custom impressions, or browse our **Home Scents** collection!"
    )

    with st.expander("ℹ️ Legal, Brand & Allergy Notices"):
        st.write(f"**Trademark Notice:** {DISCLAIMER_TEXT}")
        st.write("---")
        st.warning(ALLERGY_DISCLAIMER_TEXT)

    # Added the collection designer name after the hyphen
    active_designer = filtered_catalog[0].get("designer", "Chanel") if filtered_catalog else "Chanel"
    st.header(f"ALFA SCENTS Signature Collection - {active_designer} Impressions")
    st.caption("Featured in 60ml shatter-proof precision polymer bottles.")

    if total_qty > 0:
        c_banner1, c_banner2 = st.columns([3, 1])
        with c_banner1:
            st.info(f"🛒 **Bag Summary:** {total_qty} bottle(s) selected | **Current Total:** ${final_subtotal:.2f}")
        with c_banner2:
            st.button(
                "⚡ Pay & Checkout Now",
                key="top_fast_checkout_btn",
                type="primary",
                use_container_width=True,
                on_click=switch_to_checkout_tab
            )

    if not filtered_catalog:
        st.info("✨ Our new Signature Collection is coming soon! You can still browse or request custom scents in the 📦 Full Inventory tab.")
    else:
        for idx, item in enumerate(filtered_catalog):
            stock_level = (
                inventory_df.loc[item["id"], "stock_level"]
                if item["id"] in inventory_df.index
                else 5
            )

            with st.container():
                st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
                
                # Side-by-side layout: Product Image on left, Scent Details on right
                img_col, details_col = st.columns([1, 2])

                with img_col:
                    if item.get("image_url") and os.path.exists(item["image_url"]):
                        st.image(item["image_url"], use_container_width=True)

                with details_col:
                    badge_col1, badge_col2 = st.columns([1, 1])
                    with badge_col1:
                        st.markdown(f'<span class="badge-signature">{item.get("badge_primary", "Signature")}</span>', unsafe_allow_html=True)
                    with badge_col2:
                        st.markdown(f'<span class="badge-offer">{item.get("badge_secondary", "Special Offer")}</span>', unsafe_allow_html=True)

                    designer_name = item.get("designer", "Chanel")
                    st.markdown(f"### {item['name']} ({designer_name} Collection) Impression")
                    st.caption(f"**{item['gender']}'s** • {item['category']}")
                    
                    st.markdown(f'<div class="luxury-impression-stamp"><span>✨ ALFA SCENTS {designer_name} Collection Impression • Artisanal Craft Blend ✨</span></div>', unsafe_allow_html=True)

                    st.write(f"*{item['notes']}*")
                    
                    if item.get("scent_profile"):
                        sp = item["scent_profile"]
                        st.markdown(f"**Top Notes:** {', '.join(sp.get('top_notes', []))}")
                        st.markdown(f"**Heart Notes:** {', '.join(sp.get('heart_notes', []))}")
                        st.markdown(f"**Base Notes:** {', '.join(sp.get('base_notes', []))}")
                    
                    price_box_html = (
                        "<div style='background-color: rgba(212, 175, 55, 0.08); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(212, 175, 55, 0.3); margin: 6px 0; font-weight: 600; font-size: 0.85rem; color: #f3e5ab;'>"
                        "✨ $30.00 ea. • <span style='font-weight: bold; color: #d4af37;'>Buy 3 bottles and pick a 4th bottle for free</span>"
                        "</div>"
                    )
                    st.markdown(price_box_html, unsafe_allow_html=True)

                    if stock_level <= 0:
                        st.error("🔥 Out of Stock")
                    else:
                        st.caption(f"Stock: {stock_level} available")

                    st.button(
                        "🛍️ Add to Bag",
                        key=f"btn_{item['id']}",
                        on_click=add_to_cart,
                        args=(item["id"],),
                        use_container_width=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.button(
        "🛍️ Ready to Purchase? Click Here to Proceed to Checkout & Invoice",
        key="bottom_checkout_redirect_trigger",
        type="primary",
        use_container_width=True,
        on_click=switch_to_checkout_tab
    )

# ------------------------------------------
# TAB 2: FULL INVENTORY
# ------------------------------------------
elif selected_nav == "📦 Full Inventory":
    st.header("📦 Full Inventory Impression & Home Scents Request Portal")
    st.markdown("""
    <div class="market-sub-banner">
        <b>Pricing & Shipping Summary:</b> Every bottle is <b>$30.00</b> (60ml Shatter-Proof Precision Polymer). Buy 3 bottles and pick a 4th bottle for free! 
        Enjoy <b>Free Shipping</b> on orders of $60 or more ($5 shipping fee for single $30 orders).
    </div>
    """, unsafe_allow_html=True)

    if total_qty > 0:
        c_inv_b1, c_inv_b2 = st.columns([3, 1])
        with c_inv_b1:
            st.info(f"🛒 **Bag Summary:** {total_qty} item(s) in bag | **Current Total:** ${final_subtotal:.2f}")
        with c_inv_b2:
            st.button(
                "⚡ Proceed to Checkout",
                key="full_inv_top_checkout_btn",
                type="primary",
                use_container_width=True,
                on_click=switch_to_checkout_tab
            )

    st.subheader("📚 Browse Our Full Inventory List")
    st.write("Check the 'Add to Cart' box next to any item below to add it directly to your shopping bag:")

    sub_cat1, sub_cat2, sub_cat3 = st.tabs(["✨ More Men's Scents", "🌸 More Women's Scents", "🏡 Home Scents Collection"])

    def process_checked_items(df, unique_key):
        if df is not None and not df.empty:
            if "Add to Cart" not in df.columns:
                df.insert(0, "Add to Cart", False)
                
            target_col = 'Item Name' if 'Item Name' in df.columns else df.columns[1]
            
            edited_df = st.data_editor(
                df,
                hide_index=True,
                use_container_width=True,
                disabled=[col for col in df.columns if col != "Add to Cart"],
                key=f"editor_{unique_key}"
            )
            
            newly_checked = edited_df[edited_df["Add to Cart"]]
            
            if not newly_checked.empty:
                if st.button("🛒 Add Selected Items to My Bag", key=f"btn_bulk_{unique_key}", type="primary", use_container_width=True):
                    added_count = 0
                    btype_label = "60ml Shatter-Proof Precision Polymer"

                    for _, row in newly_checked.iterrows():
                        item_name = str(row[target_col]).strip()
                        custom_cart_id = f"custom_req_{item_name.lower().replace(' ', '_')}_polymer"
                        
                        if custom_cart_id in st.session_state.cart:
                            st.session_state.cart[custom_cart_id] += 1
                        else:
                            st.session_state.cart[custom_cart_id] = 1
                            
                        if not any(p["id"] == custom_cart_id for p in FRAGRANCE_CATALOG):
                            FRAGRANCE_CATALOG.append({
                                "id": custom_cart_id,
                                "name": f"Custom Request: {item_name}",
                                "gender": "Unisex",
                                "badge_primary": "Custom Pick",
                                "badge_secondary": "Special Request",
                                "category": f"{btype_label} • Custom Impression / Home Scent",
                                "price": 30.0,
                                "edition_type": "Precision Polymer",
                                "bottle_type": btype_label,
                                "notes": "Custom item requested dynamically via spreadsheet checkbox toggle selector.",
                                "image_url": DEFAULT_PRODUCT_IMAGE
                            })
                        added_count += 1
                        
                    st.toast(f"Successfully added {added_count} custom items ({btype_label}) to your bag! 🛍️")
                    st.rerun()

    with sub_cat1:
        mens_sheet_df = load_google_sheet_inventory("Mens_Scents")
        process_checked_items(mens_sheet_df, "mens")

    with sub_cat2:
        womens_sheet_df = load_google_sheet_inventory("Womens_Scents")
        process_checked_items(womens_sheet_df, "womens")

    with sub_cat3:
        home_sheet_df = load_google_sheet_inventory("Home_Scents")
        process_checked_items(home_sheet_df, "home")

    st.markdown("---")
    st.button(
        "🛍️ Ready to Purchase? Click Here to Proceed to Checkout & Invoice",
        key="full_inv_bottom_checkout_btn",
        type="primary",
        use_container_width=True,
        on_click=switch_to_checkout_tab
    )

    st.markdown("---")
    st.subheader("📝 Submit Your Custom Request Below")
    
    with st.form("qr_request_line_form"):
        qr_cust_name = st.text_input("Your Full Name *")
        qr_cust_contact = st.text_input("Email Address or Phone Number *")
        qr_shipping_address = st.text_input("Delivery / Shipping Address *")

        st.markdown("---")
        qr_item_requests = st.text_area("What impressions or home scents would you like to request? *")
        qr_total_qty = st.number_input("Total Number of Items Requested", min_value=1, value=1)
        qr_payment_method = st.selectbox("Preferred Settlement Method", ["Cash App", "Zelle", "Venmo", "Apple Pay", "Cash POS (In-Person)"])
        qr_notes = st.text_area("Additional Request Notes / Custom Preferences / Home Scent Details")

        qr_submit = st.form_submit_button("Submit Request & Send Notification")

        if qr_submit:
            if not (qr_cust_name and qr_cust_contact and qr_shipping_address):
                st.error("Please fill in your name, contact details, and shipping address.")
            elif not qr_item_requests:
                st.error("Please specify the impressions or home scents you want to request.")
            else:
                qr_sets = qr_total_qty // 4
                qr_rem = qr_total_qty % 4
                qr_sub = ((qr_sets * 3) + qr_rem) * 30.0
                qr_ship = 5.0 if qr_sub < 60.0 else 0.0
                qr_final_total = qr_sub + qr_ship
                
                full_request_summary = f"{qr_item_requests} (Bottle Type: 60ml Shatter-Proof Precision Polymer)"

                save_order_to_db(
                    name=qr_cust_name,
                    email=qr_cust_contact,
                    phone=qr_cust_contact,
                    address=qr_shipping_address,
                    items_summary=full_request_summary,
                    qty=qr_total_qty,
                    subtotal=qr_sub,
                    discount=0.0,
                    total=qr_final_total,
                    payment_method=qr_payment_method,
                    is_priority=1,
                    notes=f"Full Inventory Custom Request Order. Desired Items: {full_request_summary}. {qr_notes if qr_notes else ''}",
                    cart_items={},
                    referral_code=current_ref_tag,
                )

                send_order_emails(qr_cust_name, qr_cust_contact, qr_final_total, full_request_summary, qr_payment_method, current_ref_tag)

                st.success(f"Success! Your request for {qr_total_qty} item(s) has been submitted for {qr_cust_name}.")
                st.info(f"Please complete your settlement of **${qr_final_total:.2f}** via **{qr_payment_method}** using the payment details in the sidebar.")

# ------------------------------------------
# TAB 3: GIFT CARDS
# ------------------------------------------
elif selected_nav == "🎁 Gift Cards":
    st.header("🎁 Digital Gift Cards & Store Credit")
    gc_tab1, gc_tab2 = st.tabs(["Purchase Gift Card", "Redeem Gift Card Code"])

    with gc_tab1:
        with st.form("purchase_gc_form"):
            gc_purchaser = st.text_input("Your Name *")
            gc_recipient = st.text_input("Recipient Email or Name *")
            gc_value = st.number_input("Gift Card Amount ($)", min_value=10.0, value=60.0, step=5.0)
            gc_payment_method = st.selectbox("Settlement Method Used *", ["Cash App", "Zelle", "Venmo", "Apple Pay", "Cash POS (In-Person)"])
            gc_payment_confirmed = st.checkbox("✅ I confirm that payment has been sent/collected via the selected method.")
            gc_submit = st.form_submit_button("Generate Gift Card Code")

            if gc_submit:
                if not (gc_purchaser and gc_recipient):
                    st.error("Please fill in both your name and recipient's details.")
                elif not gc_payment_confirmed:
                    st.error("⚠️ You must confirm that payment has been sent before generating a code.")
                else:
                    random_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    gc_code = f"AS-GC-{random_str}"
                    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    with sqlite3.connect(DB_FILE) as conn:
                        c = conn.cursor()
                        c.execute(
                            "INSERT OR REPLACE INTO gift_cards (code, initial_value, current_balance, purchaser_name, recipient_email, status, created_date, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (gc_code, gc_value, gc_value, gc_purchaser, gc_recipient, "Pending Verification", created_date, gc_payment_method),
                        )

                    st.success("🎉 Gift Card Created (Pending Verification)!")
                    st.info(f"**Gift Card Code:** `{gc_code}` | **Value:** ${gc_value:.2f} | **Via:** {gc_payment_method}")

    with gc_tab2:
        with st.form("redeem_gc_form"):
            entered_code = st.text_input("Enter Gift Card Code (e.g., AS-GC-XXXXXX)").strip()
            redeem_submit = st.form_submit_button("Apply Gift Card to Order")

            if redeem_submit:
                card_data = get_gift_card(entered_code.upper())
                if not card_data:
                    st.error("Invalid gift card code.")
                else:
                    balance = card_data[2]
                    status = card_data[5]
                    if status != "Active" or balance <= 0:
                        st.warning("⚠️ This gift card is either pending admin verification, has a zero balance, or is inactive.")
                    else:
                        st.session_state.applied_gift_card = entered_code.upper()
                        st.session_state.gift_card_discount = balance
                        st.success(f"✅ Gift card applied! Available Balance: ${balance:.2f}")
                        st.rerun()

# ------------------------------------------
# TAB 4: REVIEWS & TESTIMONIALS
# ------------------------------------------
elif selected_nav == "⭐ Reviews & Testimonials":
    st.header("⭐ Customer Reviews & Testimonials")
    rev_sub_tab1, rev_sub_tab2 = st.tabs(["Browse Reviews", "Leave a Review"])

    with rev_sub_tab1:
        catalog_options = ["All"] + [item["name"] for item in FRAGRANCE_CATALOG]
        filter_item_name = st.selectbox("Filter Reviews by Product Blend", catalog_options)

        selected_item_id_for_review = "All"
        if filter_item_name != "All":
            selected_item_id_for_review = next(item["id"] for item in FRAGRANCE_CATALOG if item["name"] == filter_item_name)

        reviews_df = get_approved_reviews(selected_item_id_for_review)

        if reviews_df.empty:
            st.info("No reviews found for this selection yet. Be the first to leave one!")
        else:
            avg_rating = reviews_df["rating"].mean()
            st.metric("Average Community Rating", f"{avg_rating:.1f} / 5.0 ⭐", f"{len(reviews_df)} total review(s)")
            st.markdown("---")

            for _, row in reviews_df.iterrows():
                stars = "⭐" * int(row["rating"])
                match_blend = next((item["name"] for item in FRAGRANCE_CATALOG if item["id"] == row["item_id"]), "General Store Review")
                with st.container(border=True):
                    st.markdown(f"**{row['customer_name']}** — {stars}")
                    st.caption(f"Product: {match_blend} | Date: {row['review_date']}")
                    st.write(f'"{row["review_text"]}"')

    with rev_sub_tab2:
        with st.form("leave_review_form"):
            st.markdown("### Share Your Experience")
            rev_name = st.text_input("Your Name *")
            rev_rating = st.slider("Rating (1 to 5 Stars)", min_value=1, max_value=5, value=5)
            blend_choices = {item["name"]: item["id"] for item in FRAGRANCE_CATALOG}
            blend_choices["General Store / Inventory Experience"] = "general"
            chosen_blend_name = st.selectbox("Select Fragrance / Product", list(blend_choices.keys()))
            rev_text = st.text_area("Your Review / Testimonial *")
            submit_review = st.form_submit_button("Submit Review")

            if submit_review:
                if not (rev_name and rev_text):
                    st.error("Please provide your name and your review message.")
                else:
                    target_blend_id = blend_choices[chosen_blend_name]
                    save_review(rev_name, rev_rating, target_blend_id, rev_text)
                    st.success("🎉 Thank you! Your review has been successfully submitted.")

# ------------------------------------------
# TAB 5: CHECKOUT & INVOICE GENERATOR
# ------------------------------------------
elif selected_nav == "🛒 Checkout & Invoice":
    st.header("🛒 Secure Boutique Checkout & Invoice")

    if not st.session_state.cart:
        st.info("Your shopping bag is currently empty. Add items from the catalog to proceed.")
    else:
        st.subheader("Bag Summary & Breakdown")
        cart_table_data = []
        summary_list = []

        for item_id, qty in st.session_state.cart.items():
            if str(item_id).startswith("custom_req_"):
                raw_item_name = str(item_id).replace("custom_req_", "").replace("_polymer", "").replace("_", " ").title()
                product = {
                    "name": f"Custom Request: {raw_item_name}",
                    "category": "Custom Impression / Home Scent",
                    "price": 30.0,
                    "bottle_type": "60ml Shatter-Proof Precision Polymer"
                }
            else:
                try:
                    product = next(p for p in FRAGRANCE_CATALOG if p["id"] == item_id)
                except StopIteration:
                    clean_name = str(item_id).replace("custom_req_", "").replace("_", " ").title()
                    product = {
                        "name": f"Custom Request: {clean_name}",
                        "category": "Custom Impression / Home Scent",
                        "bottle_type": "60ml Shatter-Proof Precision Polymer"
                    }

            bottle_type_display = product.get("bottle_type", "60ml Shatter-Proof Precision Polymer")

            cart_table_data.append({
                "Product Name": product["name"],
                "Bottle Type": bottle_type_display,
                "Category": product["category"],
                "Qty": qty,
                "Price": "$30.00",
                "Total": f"${30.0 * qty:.2f}",
            })
            summary_list.append(f"{qty}x {product['name']} [{bottle_type_display}]")

        st.table(cart_table_data)

        # Promotional code calculation
        promo_code_input = st.text_input("🏷️ Promotional Code / Campaign Coupon (Optional)", key="checkout_promo_input").strip().upper()
        promo_discount_amount = 0.0
        if promo_code_input == "LUXURY10":
            promo_discount_amount = raw_subtotal * 0.10
            st.success("🎉 Promo Code 'LUXURY10' Applied: 10% Off Subtotal!")
        elif promo_code_input != "":
            st.warning("⚠️ Invalid promotional code.")

        final_subtotal = max(0.0, raw_subtotal + shipping_fee - st.session_state.gift_card_discount - promo_discount_amount)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Total Items:** {total_qty}")
            st.markdown(f"**Promotions:** {discount_summary_str}")
            if shipping_fee > 0:
                st.markdown(f"**Shipping:** ${shipping_fee:.2f} ($5 fee for $30 orders)")
            else:
                st.markdown("**Shipping:** 🎉 **FREE SHIPPING ($60+ order)**")

            if st.session_state.applied_gift_card:
                st.markdown(f"**Gift Card Credit Active:** {st.session_state.applied_gift_card} (-${st.session_state.gift_card_discount:.2f})")
            if promo_discount_amount > 0:
                st.markdown(f"**Promo Code ({promo_code_input}):** -${promo_discount_amount:.2f}")
                
        with c2:
            if st.button("Clear Bag"):
                st.session_state.cart = {}
                st.session_state.applied_gift_card = None
                st.session_state.gift_card_discount = 0.0
                st.rerun()

        st.markdown("---")
        st.markdown("### 📄 Generated Customer Invoice")
        invoice_container = st.container(border=True)
        with invoice_container:
            inv_col1, inv_col2 = st.columns(2)
            with inv_col1:
                st.markdown("**ALFA SCENTS Boutique**")
                st.markdown("100% Oil-Based Luxury Impressions")
                st.markdown(f"**Invoice Date:** {datetime.now().strftime('%Y-%m-%d')}")
                st.markdown(f"**Cycle:** {get_current_30_day_cycle()}")
                if current_ref_tag:
                    st.markdown(f"**Partner Referral:** {current_ref_tag}")
            with inv_col2:
                st.markdown(f"**Promotions:** {discount_summary_str}")
                if shipping_fee > 0:
                    st.markdown(f"**Shipping Fee:** ${shipping_fee:.2f}")
                else:
                    st.markdown("**Shipping:** **FREE**")
                if st.session_state.applied_gift_card:
                    st.markdown(f"**Gift Card Credit:** -${st.session_state.gift_card_discount:.2f}")
                if promo_discount_amount > 0:
                    st.markdown(f"**Promo Code Discount:** -${promo_discount_amount:.2f}")
                st.markdown(f"### **Total Due: ${final_subtotal:.2f}**")

            st.markdown("---")
            pay_info_col1, pay_info_col2, pay_info_col3, pay_info_col4 = st.columns(4)
            with pay_info_col1:
                st.markdown("**Cash App**")
                st.markdown(f"Name: **{active_cashapp['name']}**")
                st.markdown("Contact for handle")
                
            with pay_info_col2:
                st.markdown("**Venmo**")
                st.markdown(f"Name: **{active_venmo['name']}**")
                st.markdown("Contact for handle")
                
            with pay_info_col3:
                st.markdown("**Zelle**")
                st.markdown(f"Name: **{active_zelle['name']}**")
                if active_zelle.get("identifier") and active_zelle["identifier"] != "Contact for payment":
                    st.markdown(f"Phone/ID: `{active_zelle['identifier']}`")
                else:
                    st.markdown("Contact for phone/ID")

            with pay_info_col4:
                st.markdown("**Apple Pay**")
                st.markdown(f"Name: **{active_applepay['name']}**")
                if active_applepay.get("identifier") and active_applepay["identifier"] != "Contact for payment":
                    st.markdown(f"Phone: `{active_applepay['identifier']}`")
                else:
                    st.markdown("Contact for phone/ID")

        st.markdown("---")
        st.subheader("Customer Shipping & Payment Submission Form")

        with st.form("checkout_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Full Name *")
                email = st.text_input("Email Address *")
            with col_b:
                phone = st.text_input("Phone Number *")
                address = st.text_input("Shipping Address *")

            manual_ref = st.text_input("Partner / Affiliate Referral Tag (Optional)", value=current_ref_tag)
            payment_method = st.radio("Select Settlement Channel Used", ["Cash App", "Zelle", "Venmo", "Apple Pay", "Cash POS (In-Person)"])
            is_priority = st.checkbox("🔥 Mark as Priority Order")
            notes = st.text_area("Special Delivery Instructions / Scent Preferences")

            st.markdown("---")
            payment_confirmed = st.checkbox(f"✅ I confirm that I have sent the exact payment total of ${final_subtotal:.2f} to the designated payment handle above.")
            allergy_ack = st.checkbox("I acknowledge that I have read the Safety & Allergy Disclaimer.")

            if st.form_submit_button("Submit Order & Send Email Confirmation"):
                if not (name and email and phone and address):
                    st.error("Please fill in all required customer fields.")
                elif not payment_confirmed:
                    st.error("⚠️ You must check the confirmation box verifying payment.")
                elif not allergy_ack:
                    st.error("Please acknowledge the Safety & Allergy Disclaimer.")
                else:
                    items_str = ", ".join(summary_list)
                    final_tag_to_save = manual_ref.strip().lower() if manual_ref else current_ref_tag
                    combined_notes = f"Promo Code Used: {promo_code_input} (-${promo_discount_amount:.2f}). {notes}" if promo_discount_amount > 0 else notes

                    save_order_to_db(
                        name, email, phone, address, items_str, total_qty, raw_subtotal, promo_discount_amount,
                        final_subtotal, payment_method, is_priority, combined_notes, st.session_state.cart, referral_code=final_tag_to_save
                    )
                    
                    send_order_emails(name, email, final_subtotal, items_str, payment_method, final_tag_to_save)

                    st.success("Order successfully submitted and email notifications sent!")
                    
                    if st.session_state.applied_gift_card:
                        with sqlite3.connect(DB_FILE) as conn_gc:
                            c_gc = conn_gc.cursor()
                            c_gc.execute("UPDATE gift_cards SET current_balance = 0, status = 'Redeemed' WHERE code = ?", (st.session_state.applied_gift_card,))

                    st.session_state.cart = {}
                    st.session_state.applied_gift_card = None
                    st.session_state.gift_card_discount = 0.0

# ------------------------------------------
# TAB 6: CUSTOMER ORDER LOOKUP
# ------------------------------------------
elif selected_nav == "🔍 Customer Order Lookup":
    st.header("🔍 Customer Order Lookup Portal")
    user_query = st.text_input("Enter your registered Email Address or Phone Number:")
    if st.button("Lookup Order Status") and user_query:
        results = search_orders(user_query, is_admin=False)
        if results.empty:
            st.warning("No matching orders found. Please verify your details.")
        else:
            st.subheader(f"Found {len(results)} Order(s)")
            for idx, row in results.iterrows():
                with st.expander(f"Order #{row['id']} — Status: {row['status']} ({row['order_date']})"):
                    st.write(f"**30-Day Cycle ID:** {row['cycle_id']}")
                    st.write(f"**Purchased Items:** {row['items_summary']}")
                    st.write(f"**Total Bottles:** {row['total_qty']}")
                    st.write(f"**Total Amount:** ${row['final_total']:.2f}")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.caption(f"**Legal Disclaimer:** {DISCLAIMER_TEXT}")
st.caption(f"{ALLERGY_DISCLAIMER_TEXT}")

# ==========================================
# SIDEBAR SETTINGS & ADMIN CONTROL
# ==========================================
with st.sidebar:
    st.markdown("<br><br><br>" * 3, unsafe_allow_html=True) 
    st.divider() 
    
    with st.expander("⋮ System Settings & Options", expanded=False):
        st.write("🎨 **Appearance & Theme**")
        theme_choice = st.selectbox("Select Theme Mode", options=["Dark Mode", "Light Mode"], key="app_theme_selection")
        
        if theme_choice == "Dark Mode":
            st.markdown("""
                <style>
                .stApp { background-color: #0d0f12 !important; color: #FAFAFA !important; }
                section[data-testid="stSidebar"] { background-color: #111418 !important; }
                </style>
            """, unsafe_allow_html=True)
            
        elif theme_choice == "Light Mode":
            st.markdown("""
                <style>
                .stApp { background-color: #FFFFFF !important; color: #31333F !important; }
                section[data-testid="stSidebar"] { background-color: #F0F2F6 !important; }
                </style>
            """, unsafe_allow_html=True)

        st.divider()
        st.write("🛠️ **Admin & Inventory Controls**")
        
        if "admin_unlocked" not in st.session_state:
            st.session_state["admin_unlocked"] = False

        admin_passcode = st.text_input("Admin Passcode", type="password", key="sidebar_admin_passkey")
        
        expected_admin_pass = st.secrets.get("ADMIN_PASSCODE", "Safe9uard-tf80")
        
        if admin_passcode == expected_admin_pass:
            st.session_state["admin_unlocked"] = True
            st.success("Admin Access Granted!")
        elif admin_passcode != "":
            st.session_state["admin_unlocked"] = False
            st.error("Incorrect Passcode")

        st.divider()
        if st.button("Clear App Cache", key="sidebar_clear_cache"):
            st.cache_data.clear()
            st.toast("Cache cleared!")
          
        if st.button("Rerun App Session", key="sidebar_rerun"):
            st.rerun()

# ==========================================
# ADMIN PANEL BLOCK (WITH ORDER MANAGEMENT & MARKETING SUITE)
# ==========================================
if st.session_state.get("admin_unlocked", False):
    st.markdown("---")
    with st.container(border=True):
        st.header("🛠️ Admin & Order Management Suite")

        admin_sub_tabs = st.tabs([
            "📊 Affiliate Performance", 
            "📦 Inventory Restocking", 
            "📋 Order Management & Status",
            "📢 Automated Marketing Campaigns"
        ])

        with admin_sub_tabs[0]:
            st.subheader("🤝 Partner & Affiliate Performance Tracker")
            with sqlite3.connect(DB_FILE) as conn_aff:
                aff_df = pd.read_sql_query("SELECT referral_code, final_total, total_qty FROM orders WHERE referral_code IS NOT NULL AND referral_code != ''", conn_aff)

            if not aff_df.empty:
                partner_summary = aff_df.groupby("referral_code").agg(
                    Total_Orders=("final_total", "count"),
                    Total_Bottles=("total_qty", "sum"),
                    Total_Revenue=("final_total", "sum")
                ).reset_index()
                partner_summary.columns = ["Partner Tag", "Orders Generated", "Bottles Sold", "Gross Revenue ($)"]
                st.dataframe(partner_summary, use_container_width=True)
            else:
                st.info("No partner referral data recorded yet.")

        with admin_sub_tabs[1]:
            st.subheader("📦 Inventory Tracking & Restocking Tool")
            inv_df = get_inventory_status()
            st.dataframe(inv_df, use_container_width=True)

            if not inv_df.empty:
                with st.form("restock_form_admin"):
                    selected_item_id = st.selectbox("Select Blend to Restock", inv_df["item_id"] + " - " + inv_df["item_name"])
                    new_qty = st.number_input("Set New Stock Level", min_value=0, value=5)
                    restock_submit = st.form_submit_button("Apply Restock Level")
                    if restock_submit:
                        target_id = selected_item_id.split(" - ")[0]
                        update_item_stock(target_id, new_qty)
                        st.success("Stock level updated successfully for the item!")
                        st.rerun()
            else:
                st.info("No items in inventory to restock.")

        with admin_sub_tabs[2]:
            st.subheader("📋 Comprehensive Order Management Suite")
            st.write("Review, verify payments, update fulfillment statuses, or cancel customer orders below.")

            with sqlite3.connect(DB_FILE) as conn_orders:
                all_orders_df = pd.read_sql_query("SELECT * FROM orders ORDER BY id DESC", conn_orders)

            if all_orders_df.empty:
                st.info("No orders found in the database.")
            else:
                st.dataframe(all_orders_df[["id", "order_date", "customer_name", "customer_email", "total_qty", "final_total", "payment_method", "status"]], use_container_width=True)

                st.markdown("---")
                st.markdown("#### ⚡ Individual Order Actions (Verify / Update Status / Cancel)")
                
                z_form = st.form("admin_single_order_form")
                with z_form:
                    order_ids = all_orders_df["id"].tolist()
                    selected_order_id = z_form.selectbox("Select Order ID", order_ids)
                    
                    current_row = all_orders_df[all_orders_df["id"] == selected_order_id].iloc[0]
                    z_form.write(f"**Customer:** {current_row['customer_name']} | **Email:** {current_row['customer_email']} | **Total:** ${current_row['final_total']:.2f}")
                    z_form.write(f"**Items:** {current_row['items_summary']}")
                    z_form.write(f"**Current Status:** `{current_row['status']}`")

                    new_status_choice = z_form.selectbox(
                        "Change Status to:",
                        [
                            "Pending",
                            "Payment Sent / Pending Verification",
                            "Verified & Paid",
                            "Processing / Being Crafted",
                            "Shipped / Out for Delivery",
                            "Completed",
                            "Cancelled"
                        ]
                    )

                    col_act1, col_act2 = z_form.columns(2)
                    with col_act1:
                        update_status_btn = z_form.form_submit_button("💾 Update Order Status", type="primary")
                    with col_act2:
                        cancel_order_btn = z_form.form_submit_button("❌ Cancel & Void Order")

                    if update_status_btn:
                        with sqlite3.connect(DB_FILE) as conn_up:
                            c_up = conn_up.cursor()
                            c_up.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status_choice, selected_order_id))
                        st.success(f"Order #{selected_order_id} status updated to '{new_status_choice}'!")
                        st.rerun()

                    if cancel_order_btn:
                        with sqlite3.connect(DB_FILE) as conn_canc:
                            c_canc = conn_canc.cursor()
                            c_canc.execute("UPDATE orders SET status = 'Cancelled' WHERE id = ?", (selected_order_id,))
                        st.error(f"Order #{selected_order_id} has been marked as Cancelled.")
                        st.rerun()

        with admin_sub_tabs[3]:
            st.subheader("📢 Automated Marketing & Email Campaigns")
            st.write("Send targeted promotional broadcasts, abandoned cart recovery sequences, or win-back campaigns to your customer database.")

            with sqlite3.connect(DB_FILE) as conn_leads:
                leads_df = pd.read_sql_query("SELECT DISTINCT customer_email, customer_name, customer_phone FROM orders", conn_leads)

            if leads_df.empty:
                st.info("No customer lead emails found in order history yet.")
            else:
                st.write(f"Total Unique Customer Leads Available: **{len(leads_df)}**")
                
                campaign_choice = st.selectbox(
                    "Select Marketing Campaign Type",
                    ["abandoned_cart", "winback"]
                )
                
                if st.button("🚀 Broadcast Campaign to All Customers", type="primary"):
                    success_count = 0
                    for _, lead in leads_df.iterrows():
                        email = lead["customer_email"]
                        name = lead["customer_name"] if lead["customer_name"] else "Valued Customer"
                        
                        if email and "@" in email:
                            if send_marketing_campaign_email(email, name, campaign_choice):
                                success_count += 1
                                
                    st.success(f"Successfully broadcasted '{campaign_choice}' campaign to {success_count} customer(s)!")

