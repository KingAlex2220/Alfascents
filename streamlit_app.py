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

# Automatically unlock admin panel by default so Back Office never disappears
if "admin_unlocked" not in st.session_state:
    st.session_state["admin_unlocked"] = True

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
# AUTOMATICALLY BUILD STREAMLINED CATALOG
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
    /* PIN SIDEBAR TOGGLE BUTTON FIXED IN TOP LEFT */
    header[data-testid="stHeader"] {
        background: transparent !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 999999 !important;
    }
    [data-testid="stHeader"] > div:first-child {
        visibility: hidden !important;
    }
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: block !important;
        color: #d4af37 !important;
        background-color: #161a22 !important;
        border: 2px solid #d4af37 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(212, 175, 55, 0.4) !important;
        margin: 10px !important;
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
        border-radius: 8px !important;
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
# DATABASE SETUP
# ==========================================
DB_FILE = "alfa_scents.db"
DEFAULT_STOCK_PER_ITEM = 5


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
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


init_db()


def switch_to_checkout_tab():
    st.session_state["target_tab"] = "🛒 Checkout & Invoice"
    st.session_state["main_navigation_radio"] = "🛒 Checkout & Invoice"
    st.toast("Redirecting to Secure Boutique Checkout... 🛍️", icon="💳")
    st.rerun()


# ==========================================
# GLOBAL HELPERS & PAYMENT ACCOUNTS
# ==========================================
DISCLAIMER_TEXT = "ALFA SCENTS offers proprietary, independently formulated scents inspired by popular fragrance profiles."
ALLERGY_DISCLAIMER_TEXT = "⚠️ ALLERGY NOTICE: ALFA SCENTS products contain concentrated fragrance oils. Perform a patch test before use."

ZELLE_ACCOUNTS = {"ray": {"name": "Ira Ray Thompson", "identifier": "4079126043"}}
VENMO_ACCOUNTS = {"ray": {"name": "Ira Ray Thompson", "identifier": "Contact for Venmo handle"}}
CASHAPP_ACCOUNTS = {"ray": {"name": "Ira Ray Thompson", "identifier": "Contact for Cash App handle"}}
APPLEPAY_ACCOUNTS = {"ray": {"name": "Ira Ray Thompson", "identifier": "407-912-6043"}}

active_zelle = ZELLE_ACCOUNTS["ray"]
active_venmo = VENMO_ACCOUNTS["ray"]
active_cashapp = CASHAPP_ACCOUNTS["ray"]
active_applepay = APPLEPAY_ACCOUNTS["ray"]


def get_current_30_day_cycle():
    now = datetime.now()
    return f"CYCLE-{now.year}-30D-01"


def get_inventory_status():
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM inventory", conn)
    return df


def update_item_stock(item_id, new_stock):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE inventory SET stock_level = ? WHERE item_id = ?", (new_stock, item_id))


def save_order_to_db(name, email, phone, address, items_summary, qty, subtotal, discount, total, payment_method, is_priority, notes, cart_items, referral_code=""):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cycle_id = get_current_30_day_cycle()
        status = "Payment Sent / Pending Verification" if is_priority else "Pending"

        c.execute(
            "INSERT INTO orders (order_date, customer_name, customer_email, customer_phone, shipping_address, items_summary, total_qty, subtotal, discount_applied, final_total, payment_method, status, is_priority, cycle_id, notes, referral_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_date, name, email, phone, address, items_summary, qty, subtotal, discount, total, payment_method, status, int(is_priority), cycle_id, notes, referral_code),
        )


def send_order_emails(customer_name, customer_email, total_due, items_summary, payment_method, referral_tag, notification_recipient=""):
    SENDER_EMAIL = "alfascents@gmail.com"
    APP_PASSWORD = st.secrets.get("SMTP_PASSWORD", "dkif qgwv psyr qiig")
    ADMIN_EMAIL = notification_recipient if notification_recipient else "alfascents@gmail.com"
    
    msg_customer = MIMEMultipart()
    msg_customer["From"] = SENDER_EMAIL
    msg_customer["To"] = customer_email
    msg_customer["Subject"] = "✨ ALFA SCENTS - Luxury Boutique Order Receipt"
    
    customer_html = f"<h3>Hi {customer_name}, thank you for your order!</h3><p>Total: ${total_due:.2f}</p>"
    msg_customer.attach(MIMEText(customer_html, "html"))

    msg_admin = MIMEMultipart()
    msg_admin["From"] = SENDER_EMAIL
    msg_admin["To"] = ADMIN_EMAIL
    msg_admin["Subject"] = f"🚨 NEW ORDER - Representative: {referral_tag}"
    
    admin_html = f"<h3>New Order Received</h3><p>Customer: {customer_name}</p><p>Total: ${total_due:.2f}</p>"
    msg_admin.attach(MIMEText(admin_html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, customer_email, msg_customer.as_string())
            server.sendmail(SENDER_EMAIL, ADMIN_EMAIL, msg_admin.as_string())
    except Exception as e:
        print(f"SMTP Error: {e}")


# ==========================================
# SESSION STATE & CART MANAGEMENT
# ==========================================
if "cart" not in st.session_state:
    st.session_state.cart = {}


def add_to_cart(item_id):
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id] += 1
    else:
        st.session_state.cart[item_id] = 1
    st.toast("Added to Shopping Bag! 🛍️")


# ==========================================
# SIDEBAR NAVIGATION & CONTROLS
# ==========================================
st.sidebar.title("✨ Luxury Boutique Hub")
st.sidebar.caption("All Bottles $30 • Special Buy 3 Get 1 Free")
st.sidebar.success("🔗 Representative: **Ira Ray Thompson**")

search_term = st.sidebar.text_input("🔍 Search Catalog...", "").lower()
selected_gender = st.sidebar.radio("Department Filter", ["All", "Men", "Women", "Unisex"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 Quick Payment Options (Ira Thompson)")

pay_tab1, pay_tab2, pay_tab3, pay_tab4 = st.sidebar.tabs(["Cash App", "Venmo", "Zelle", "Apple Pay"])

with pay_tab1:
    st.markdown(f"**{active_cashapp['name']}**")
    st.markdown("Submit payment via Cash App.")

with pay_tab2:
    st.markdown(f"**{active_venmo['name']}**")
    st.markdown("Submit payment via Venmo.")

with pay_tab3:
    st.markdown(f"**{active_zelle['name']}**")
    st.markdown(f"Zelle Phone/ID: `{active_zelle['identifier']}`")

with pay_tab4:
    st.markdown(f"**{active_applepay['name']}**")
    st.markdown(f"Apple Pay Number: `{active_applepay['identifier']}`")

st.sidebar.markdown("---")
st.sidebar.subheader("🛒 Shopping Bag Summary")
total_qty = sum(st.session_state.cart.values())
st.sidebar.write(f"**Items in Bag:** {total_qty} bottle(s)")

if total_qty > 0:
    st.sidebar.button("⚡ Proceed to Checkout", key="sidebar_checkout_btn", type="primary", use_container_width=True, on_click=switch_to_checkout_tab)

# ==========================================
# MAIN PAGE INTERFACE
# ==========================================
all_tab_names = [
    "✨ Signature Blends",
    "📦 Full Inventory",
    "🎁 Gift Cards",
    "⭐ Reviews & Testimonials",
    "🛒 Checkout & Invoice",
]

if "target_tab" in st.session_state and st.session_state["target_tab"] in all_tab_names:
    active_tab = st.session_state["target_tab"]
else:
    active_tab = all_tab_names[0]

selected_nav = st.radio("Navigation", all_tab_names, index=all_tab_names.index(active_tab), horizontal=True, key="main_navigation_radio", label_visibility="collapsed")
st.session_state["target_tab"] = selected_nav

if selected_nav == "✨ Signature Blends":
    st.header("ALFA SCENTS Signature Collection - Chanel Impressions")
    st.caption("Featured in 60ml shatter-proof precision polymer bottles.")

    for item in FRAGRANCE_CATALOG:
        with st.container():
            st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
            st.markdown(f"### {item['name']}")
            st.write(f"*{item['notes']}*")
            st.button("🛍️ Add to Bag", key=f"btn_{item['id']}", on_click=add_to_cart, args=(item["id"],), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

elif selected_nav == "🛒 Checkout & Invoice":
    st.header("🛒 Secure Boutique Checkout")
    if not st.session_state.cart:
        st.info("Your shopping bag is empty.")
    else:
        st.write(f"Total Items: {total_qty}")
        with st.form("checkout_form"):
            name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")
            address = st.text_input("Shipping Address *")
            payment_method = st.radio("Payment Method", ["Cash App", "Zelle", "Venmo", "Apple Pay"])
            
            if st.form_submit_button("Submit Order"):
                save_order_to_db(name, email, phone, address, f"{total_qty} items", total_qty, 30.0*total_qty, 0.0, 30.0*total_qty, payment_method, 0, "", st.session_state.cart, "Ira Ray Thompson")
                send_order_emails(name, email, 30.0*total_qty, f"{total_qty} items", payment_method, "Ira Ray Thompson", st.session_state.get("restock_admin_email", ""))
                st.success("Order submitted successfully!")
                st.session_state.cart = {}

# ==========================================
# ADMINISTRATIVE BACK OFFICE SUITE (PERMANENTLY VISIBLE AT BOTTOM)
# ==========================================
if st.session_state.get("admin_unlocked", True):
    st.markdown("---")
    with st.container(border=True):
        st.header("⚙️ Administrative Back Office Suite")

        admin_sub_tabs = st.tabs([
            "📦 Inventory Restocking Tool",
            "📧 Email Order Confirmations",
            "📊 Representative Ledger", 
            "📋 Order Management & Status",
        ])

        with admin_sub_tabs[0]:
            st.subheader("📦 Inventory Tracking & Restocking Tool")
            inv_df = get_inventory_status()
            st.dataframe(inv_df, use_container_width=True)

        with admin_sub_tabs[1]:
            st.subheader("📧 Email Order Confirmation & Notification Dispatcher")
            st.write("Configure your back office email address below to receive new order confirmations.")
            
            with st.form("admin_email_config_form"):
                admin_notif_email = st.text_input(
                    "Back Office Notification Email Address",
                    value=st.session_state.get("restock_admin_email", ""),
                    placeholder="Enter email address to receive order alerts"
                )
                if st.form_submit_button("💾 Save Notification Email"):
                    st.session_state["restock_admin_email"] = admin_notif_email.strip()
                    st.success(f"Saved notification email address: `{admin_notif_email.strip()}`")

        with admin_sub_tabs[2]:
            st.subheader("🤝 Representative Performance Ledger (Ira Ray Thompson)")
            st.info("Representative Ira Ray Thompson account is active.")

        with admin_sub_tabs[3]:
            st.subheader("📋 Comprehensive Order Management Suite")
            with sqlite3.connect(DB_FILE) as conn_orders:
                all_orders_df = pd.read_sql_query("SELECT * FROM orders ORDER BY id DESC", conn_orders)
            st.dataframe(all_orders_df, use_container_width=True)
