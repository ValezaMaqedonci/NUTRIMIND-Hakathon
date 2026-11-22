import streamlit as st
from groq import Groq
import base64
import sqlite3
import hashlib
import secrets
import hmac
from pathlib import Path

if "theme" not in st.session_state:
    st.session_state["theme"] = "Dark Mode"



if not st.session_state.get("logged_in", False):
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #0B1911;
    color: #F2F7F3;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #102418;
    border-right: 1px solid #244A33;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #DCE9DF;
}

/* Headings */
h1, h2, h3 {
    color: #F2F7F3 !important;
}

/* Cards */
[data-testid="stMetric"],
div.st-key-card {
    background-color: #163020;
    border: 1px solid #244A33;
    border-radius: 14px;
    padding: 18px;
}

/* Buttons */
.stButton > button {
    background-color: #34D375;
    color: #0B1911;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 20px;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #27B963;
    color: #0B1911;
    border: none;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #163020;
    border-color: #244A33;
    color: white;
}

/* Dividers */
hr {
    border-color: #244A33;
}

/* Footer */
.nutri-footer {
    background-color: #102418;
    border-top: 1px solid #244A33;
    padding: 22px;
    border-radius: 12px;
    margin-top: 55px;
    text-align: center;
}

.nutri-footer h4 {
    color: #34D375;
    margin-bottom: 7px;
}

.nutri-footer p {
    color: #A8BBAE;
    font-size: 13px;
    margin: 0;
}

/* Text areas */
.stTextArea textarea {
    background-color: #163020 !important;
    color: #F2F7F3 !important;
    border: 1px solid #244A33 !important;
    border-radius: 10px !important;
    -webkit-text-fill-color: #F2F7F3 !important;
}

/* Placeholder */
.stTextArea textarea::placeholder {
    color: #A8BBAE !important;
    -webkit-text-fill-color: #A8BBAE !important;
}

/* Focus */
.stTextArea textarea:focus {
    border: 1px solid #34D375 !important;
    box-shadow: 0 0 0 1px #34D375 !important;
}

/* Select boxes */
[data-baseweb="select"] > div {
    background-color: #163020 !important;
    border: 1px solid #244A33 !important;
    color: #F2F7F3 !important;
    border-radius: 10px !important;
}

/* Selected text */
[data-baseweb="select"] span {
    color: #F2F7F3 !important;
}

/* Dropdown menu */
[data-baseweb="popover"] {
    background-color: #163020 !important;
}

[data-baseweb="menu"] {
    background-color: #163020 !important;
}

/* Dropdown options */
[role="option"] {
    background-color: #163020 !important;
    color: #F2F7F3 !important;
}

[role="option"]:hover {
    background-color: #244A33 !important;
}

/* SIDEBAR DESIGN */
[data-testid="stSidebar"] {
    background: #102418 !important;
    border-right: 1px solid #244A33;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 28px 16px;
}

/* Sidebar header */
.sidebar-brand {
    padding: 12px 10px 24px 10px;
    border-bottom: 1px solid #244A33;
    margin-bottom: 25px;
}

.sidebar-brand h2 {
    color: #34D375;
    font-size: 21px;
    margin: 0;
    letter-spacing: 1px;
}

.sidebar-brand p {
    color: #8DAA96;
    font-size: 10px;
    letter-spacing: 2px;
    margin: 5px 0 0 0;
}

/* Navigation title */
.sidebar-label {
    color: #789582;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 0 10px;
    margin-bottom: 12px;
}

/* Navigation items */
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 7px;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent;
    border-radius: 10px;
    padding: 11px 13px;
    transition: 0.2s;
    border: 1px solid transparent;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #163020;
    border-color: #244A33;
}

/* Selected navigation item */
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: #163020;
    border: 1px solid #34D375;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #34D375 !important;
    font-weight: 700;
}

/* Radio accent */
[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #34D375;
}

/* Hide navigation label */
[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
    display: none;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] section {
    background-color: #163020 !important;
    border: 1px dashed #34D375 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] section > div {
    background-color: transparent !important;
}

[data-testid="stFileUploader"] button {
    background-color: #34D375 !important;
    color: #0B1911 !important;
    border: none !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] label {
    color: #DCE9DF !important;
}

[data-testid="stFileUploader"] section:hover {
    border-color: #34D375 !important;
    background-color: #1B3A27 !important;
}

/* ALL SELECTBOXES */
[data-baseweb="select"] > div {
    background-color: #163020 !important;
    border: 1px solid #244A33 !important;
}

[data-baseweb="select"] input {
    color: #F2F7F3 !important;
}

[data-baseweb="select"] svg {
    fill: #34D375 !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background-color: #163020 !important;
}

[role="option"] {
    background-color: #163020 !important;
    color: #F2F7F3 !important;
}

[role="option"]:hover,
[aria-selected="true"] {
    background-color: #244A33 !important;
    color: #34D375 !important;
}

/* NUMBER INPUT - NutriScan */
[data-testid="stNumberInput"] input {
    background-color: #163020 !important;
    color: #F2F7F3 !important;
    -webkit-text-fill-color: #F2F7F3 !important;
    border: 1px solid #244A33 !important;
    border-radius: 10px !important;
}

/* Number input buttons */
[data-testid="stNumberInput"] button {
    background-color: #163020 !important;
    color: #34D375 !important;
    border: 1px solid #244A33 !important;
}

/* Hover */
[data-testid="stNumberInput"] button:hover {
    background-color: #244A33 !important;
}
/* HIDE SIDEBAR RADIO BUTTONS */
[data-testid="stSidebar"] input[type="radio"] {
    display: none !important;
}

[data-testid="stSidebar"] label > div:first-child {
    display: none !important;
}

/* PAGE FADE IN */
@keyframes pageFade {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.block-container {
    animation: pageFade 0.7s ease-out;
}

/* CARD HOVER ANIMATION */
div.st-key-card,
[data-testid="stMetric"] {
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: #34D375;
    box-shadow: 0 8px 22px #00000035;
}

/* BUTTON ANIMATION */
.stButton > button {
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 16px #34D37540;
}

/* SIDEBAR ANIMATION */
[data-testid="stSidebar"] div[role="radiogroup"] label {
    transition: all 0.25s ease;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    transform: translateX(5px);
}

/* HERO ANIMATION */
@keyframes heroGlow {
    0%, 100% {
        box-shadow: 0 0 10px #34D37510;
    }
    50% {
        box-shadow: 0 0 25px #34D37530;
    }
}

/* SMOOTH HEADINGS */
h1, h2, h3 {
    animation: pageFade 0.8s ease-out;
}

/* MODULE CARDS */
.module-card {
    transition: all 0.35s ease !important;
    position: relative;
    overflow: hidden;
}

.module-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: #34D375 !important;
    box-shadow: 0 12px 30px #34D37525;
    background: #1B3A27 !important;
}

/* GLOW EFFECT */
.module-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        110deg,
        transparent,
        #34D37515,
        transparent
    );
    transition: left 0.6s ease;
}

.module-card:hover::before {
    left: 100%;
}

/* HERO FLOATING EFFECT */
@keyframes heroFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-5px);
    }
}

/* HERO GLOW */
@keyframes heroGlow {
    0%, 100% {
        box-shadow: 0 0 10px #34D37510;
    }
    50% {
        box-shadow: 0 0 25px #34D37530;
    }
}

/* SMOOTH PAGE TRANSITION */
.block-container {
    animation: pageFade 0.7s ease-out;
}

/* INPUT FOCUS */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #34D375 !important;
    box-shadow: 0 0 10px #34D37525 !important;
}

/* BUTTON GLOW */
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 18px #34D37550;
}

/* REDUCE MOTION FOR ACCESSIBILITY */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================
# NUTRIMIND AI - LOGIN & SIGN UP SYSTEM
# =====================================

def get_db_connection():
    db_path = Path(__file__).resolve().parent / "nutrimind_users.db"
    conn = sqlite3.connect(db_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    return conn

def init_favourites_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS favourite_recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            recipe_name TEXT NOT NULL,
            recipe_content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_favourite_recipe(user_email, recipe):
    recipe_name = recipe.strip().split("\n")[0][:100]

    conn = get_db_connection()

    existing = conn.execute("""
        SELECT id FROM favourite_recipes
        WHERE user_email = ? AND recipe_content = ?
    """, (user_email, recipe)).fetchone()

    if not existing:
        conn.execute("""
            INSERT INTO favourite_recipes
            (user_email, recipe_name, recipe_content)
            VALUES (?, ?, ?)
        """, (user_email, recipe_name, recipe))

    conn.commit()
    conn.close()


init_favourites_table()


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        310000
    ).hex()


# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"


# Handle Login / Sign Up navigation
requested_auth_page = st.query_params.get("auth")

if requested_auth_page in ("login", "signup"):
    st.session_state.auth_page = requested_auth_page


# =====================================
# AUTHENTICATION SCREEN
# =====================================

if not st.session_state.logged_in:

    # Hide sidebar
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }

    .auth-container {
        max-width: 460px;
        margin: auto;
    }

    .auth-title {
        text-align: center;
        padding: 35px 0 20px 0;
    }

    .auth-title h1 {
        color: #34D375 !important;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .auth-title p {
        color: #A8BBAE !important;
        letter-spacing: 2px;
        font-size: 12px;
    }

    [data-testid="stForm"] {
        background: #102418;
        border: 1px solid #244A33;
        border-radius: 16px;
        padding: 25px;
    }

    .stTextInput input {
        background-color: #163020 !important;
        color: #F2F7F3 !important;
        border: 1px solid #244A33 !important;
        border-radius: 9px !important;
    }

    .stTextInput input:focus {
        border-color: #34D375 !important;
        box-shadow: 0 0 0 1px #34D375 !important;
    }

    .stTextInput input::placeholder {
        color: #8DAA96 !important;
    }

    [data-testid="stFormSubmitButton"] button {
        background: #34D375 !important;
        color: #0B1911 !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        min-height: 44px;
    }

    .auth-switch {
        text-align: center;
        color: #A8BBAE;
        margin-top: 22px;
        font-size: 14px;
    }

    .auth-switch a {
        color: #34D375 !important;
        font-weight: 700;
        text-decoration: none;
    }

    .auth-switch a:hover {
        text-decoration: underline;
    }

    </style>
    """, unsafe_allow_html=True)

    # Light Mode for authentication
    if st.session_state.theme == "Light Mode":
        st.markdown("""
        <style>
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background-color: #F4F8F5 !important;
            color: #183326 !important;
        }

        .auth-title h1 {
            color: #26834D !important;
        }

        .auth-title p,
        .auth-switch {
            color: #526B5D !important;
        }

        [data-testid="stForm"] {
            background: #FFFFFF !important;
            border: 1px solid #D5E5DA !important;
        }

        .stTextInput input {
            background: #F4F8F5 !important;
            color: #183326 !important;
            -webkit-text-fill-color: #183326 !important;
            border-color: #C8DCCF !important;
        }

        .stTextInput input::placeholder {
            color: #789582 !important;
        }

        .auth-switch a {
            color: #26834D !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Brand
    st.markdown("""
<div style="text-align:center; padding: 25px 10px;">
    <h1 style="color:#237A45; font-size:42px;">
        🥗 NUTRIMIND AI
    </h1>
    <h3 style="color:#176535; letter-spacing:3px;">
        SMART FOOD. SMARTER CHOICES.
    </h3>
    <p style="color:#315E40; font-size:17px;">
        Your intelligent food companion starts here.
    </p>
</div>
""", unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.3, 1])

    with center:

        # =====================================
        # LOGIN
        # =====================================

        if st.session_state.auth_page == "login":

            st.subheader("Welcome Back")
            st.caption("Log in to continue to NUTRIMIND AI.")

            with st.form("login_form"):

                login_email = st.text_input(
                    "Email",
                    placeholder="Enter your email"
                )

                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_button = st.form_submit_button(
                    "Login",
                    use_container_width=True
                )

            if login_button:

                if not login_email.strip() or not login_password:
                    st.warning("Please enter your email and password.")

                else:
                    conn = get_db_connection()

                    user = conn.execute(
                        """
                        SELECT id, name, email, password_hash, salt
                        FROM users
                        WHERE email = ?
                        """,
                        (login_email.strip().lower(),)
                    ).fetchone()

                    conn.close()

                    if user:
                        entered_hash = hash_password(
                            login_password,
                            user[4]
                        )

                        if hmac.compare_digest(entered_hash, user[3]):

                            st.session_state.logged_in = True
                            st.session_state.user_name = user[1]
                            st.session_state.user_email = user[2]

                            st.query_params.clear()
                            st.rerun()

                        else:
                            st.error("Incorrect email or password.")

                    else:
                        st.error("Incorrect email or password.")

            st.markdown("""
            <div class="auth-switch">
                Don't have an account?
                <a href="?auth=signup" target="_self">Sign Up</a>
            </div>
            """, unsafe_allow_html=True)

        # =====================================
        # SIGN UP
        # =====================================

        else:

            st.subheader("Create Your Account")
            st.caption("Join NUTRIMIND AI and explore all its features.")

            with st.form("signup_form"):

                signup_name = st.text_input(
                    "Full Name",
                    placeholder="Enter your name"
                )

                signup_email = st.text_input(
                    "Email",
                    placeholder="Enter your email"
                )

                signup_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm your password"
                )

                signup_button = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

            if signup_button:

                if (
                    not signup_name.strip()
                    or not signup_email.strip()
                    or not signup_password
                    or not confirm_password
                ):
                    st.warning("Please complete all fields.")

                elif "@" not in signup_email or "." not in signup_email:
                    st.warning("Please enter a valid email address.")

                elif len(signup_password) < 8:
                    st.warning("Password must contain at least 8 characters.")

                elif signup_password != confirm_password:
                    st.error("Passwords do not match.")

                else:
                    salt = secrets.token_hex(16)

                    password_hash = hash_password(
                        signup_password,
                        salt
                    )

                    conn = get_db_connection()

                    try:
                        conn.execute(
                            """
                            INSERT INTO users
                            (name, email, password_hash, salt)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                signup_name.strip(),
                                signup_email.strip().lower(),
                                password_hash,
                                salt
                            )
                        )

                        conn.commit()

                        st.session_state.logged_in = True
                        st.session_state.user_name = signup_name.strip()
                        st.session_state.user_email = signup_email.strip().lower()

                        st.success("Account created successfully!")
                        st.query_params.clear()
                        st.rerun()

                    except sqlite3.IntegrityError:
                        st.error("An account with this email already exists.")

                    finally:
                        conn.close()

            st.markdown("""
            <div class="auth-switch">
                Already have an account?
                <a href="?auth=login" target="_self">Log In</a>
            </div>
            """, unsafe_allow_html=True)

    st.stop()


# =====================================
# USER IS LOGGED IN - SHOW THE APP
# =====================================


# SIDEBAR BRAND
st.sidebar.markdown("""
<div class="sidebar-brand">
    <h2>🥗NUTRIMIND AI</h2>
    <p>FOOD INTELLIGENCE</p>
</div>

<div class="sidebar-label">
    WORKSPACE
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Appearance")

st.sidebar.radio(
    "Choose theme",
    ["Dark Mode", "Light Mode"],
    key="theme",
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# NAVIGATION
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

selected_page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🍽️ FoodVision",
        "👨‍🍳 RecipeMentor",
        "🥗 NutriScan",
        "🍃 FreshCheck",
        "💬 FoodChat",
        "📅 MealPlanner"
    ],
    label_visibility="collapsed"
)

page = "👤 Profile" if st.session_state.show_profile else selected_page

# TOP RIGHT PROFILE ICON

header_left, header_right = st.columns([12, 1])

with header_right:
    if st.button("👤", key="profile_icon", help="Open Profile"):
        st.session_state.show_profile = True
        st.rerun()

# SIDEBAR FOOTER
st.sidebar.markdown("""
<div style="
    position: relative;
    margin-top: 45px;
    padding: 16px 10px;
    border-top: 1px solid #244A33;
">
    <p style="
color:#DCE9DF;
        font-size:12px;
        font-weight:600;
        margin:0;
    ">NUTRIMIND AI</p>

<p style="
    color:#789582;
    font-size:10px;
    margin-top:5px;
">Smart Food. Smarter Choices.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    <p style="color:#DCE9DF; font-size:14px; font-weight:600;">
        Welcome, {st.session_state.user_name}
    </p>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("Log Out", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.auth_page = "login"
    st.rerun()

if page == "🏠 Home":

    st.title("NUTRIMIND AI")
    st.caption("Your intelligent food companion")

    if st.session_state.theme == "Light Mode":
        hero_bg = "linear-gradient(135deg, #D5E8D7, #EAF3E9, #C9DEC9)"
        hero_title = "#294333"
        hero_text = "#526B58"
        hero_label = "#34794A"
        hero_border = "#BDD5C0"
    else:
        hero_bg = "linear-gradient(135deg, #17251d, #101a16, #17202a)"
        hero_title = "#FFFFFF"
        hero_text = "#D0D8D2"
        hero_label = "#9FCEA9"
        hero_border = "#34483B"

    st.markdown(f"""
    <div style="
        background: {hero_bg};
        padding: 38px;
        border-radius: 18px;
        border: 1px solid {hero_border};
        margin: 15px 0 25px 0;
        animation: heroGlow 4s ease-in-out infinite;
    ">
        <p style="color:{hero_label}; font-size:14px; letter-spacing:2px;">
            THE FUTURE OF SMART NUTRITION
        </p>
        <h1 style="color:{hero_title}; font-size:38px; margin-bottom:12px;">
            Smart Food.<br>Smarter Choices.
        </h1>
        <p style="color:{hero_text}; font-size:17px;">
            Discover what's on your plate, explore new recipes
            and make smarter food choices with AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your AI-powered food platform")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("AI Modules", "06")

    with col2:
        st.metric("Food Assistance", "24/7")

    with col3:
        st.metric("Smart Platform", "AI Powered")

    st.divider()

    st.subheader("Explore our AI modules")
    st.write("Choose a tool and discover what NUTRIMIND can do.")

    modules = [
        ("FoodVision", "Identify food through images and camera."),
        ("RecipeMentor", "Create recipes using your ingredients."),
        ("NutriScan", "Discover nutritional information."),
        ("FreshCheck", "Explore visible signs of food freshness."),
        ("FoodChat", "Chat with your intelligent food assistant."),
        ("MealPlanner", "Generate personalized meal plans.")
    ]

    cols = st.columns(3)

    for i, (name, description) in enumerate(modules):

        with cols[i % 3]:

            st.markdown(f"""
            <div class="module-card" style="
                background:#163020;
                border:1px solid #244A33;
                border-radius:14px;
                padding:22px;
                min-height:155px;
                margin-bottom:15px;
                transition: all 0.3s ease;
            ">
                <h3 style="color:#a8d5b2; margin-bottom:12px;">
                    {name}
                </h3>
                <p style="color:#d0d0d0; font-size:14px;">
                    {description}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # st.markdown("""
    # <div style="text-align:center; padding:20px;">
    #     <h3 style="color:#a8d5b2;">Eat Smart. Live Smart.</h3>
    #     <p style="color:#999;">
    #         NUTRIMIND AI — Making food intelligence accessible to everyone.
    #     </p>
    # </div>
    # """, unsafe_allow_html=True)



elif page == "🍽️ FoodVision":

    st.title("FoodVision")
    st.caption("AI-powered food recognition")
    st.divider()

    st.subheader("Discover what's on your plate")

    upload_tab, camera_tab = st.tabs(["Upload Image", "Take Photo"])

    with upload_tab:
        uploaded_image = st.file_uploader(
            "Upload a food image",
            type=["jpg", "jpeg", "png"],
            key="foodvision_file_upload"
        )

    with camera_tab:
        camera_image = st.camera_input(
            "Take a food photo",
            key="foodvision_camera"
        )

    if camera_image is not None:
        uploaded_image = camera_image

    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Your uploaded food",
            width=400
        )

        if st.button("Identify Food"):

            with st.spinner("FoodVision is analyzing your image..."):

                try:
                    image_bytes = uploaded_image.getvalue()

                    base64_image = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    mime_type = uploaded_image.type

                    groq_client = Groq(
                        api_key=st.secrets["GROQ_API_KEY"]
                    )

                    response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {
                                "role": "system",
                                "content": """
                                You are FoodVision, an AI food recognition assistant.
                                Identify foods carefully and explain what is visible.
                                Never invent ingredients that cannot be identified.
                                """
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """
                                        Analyze this food image.

                                        Include:
                                        1. Food name
                                        2. Visible ingredients
                                        3. Short description
                                        4. Possible cooking method
                                        5. General nutritional information

                                        If you are uncertain about the food,
                                        clearly mention that.
                                        """
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:{mime_type};base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_completion_tokens=1200,
                        temperature=0.4
                    )

                    result = response.choices[0].message.content
                    st.session_state.foodvision_result = result

                except Exception as e:
                    st.error(f"Food recognition failed: {e}")

    if "foodvision_result" in st.session_state:
        st.divider()
        st.subheader("FoodVision Analysis")
        st.markdown(st.session_state.foodvision_result)


elif page == "👨‍🍳 RecipeMentor":

    st.title("RecipeMentor")
    st.caption("Turn your ingredients into delicious recipes.")
    st.divider()

    st.subheader("What ingredients do you have?")

    ingredients = st.text_area(
        "Enter your ingredients",
        placeholder="Example: eggs, milk, flour, cheese, tomatoes..."
    )

    meal_type = st.selectbox(
        "Choose meal type",
        ["Any", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]
    )

    difficulty = st.selectbox(
        "Cooking difficulty",
        ["Easy", "Medium", "Advanced"]
    )

    if st.button("Generate Recipe"):

        if not ingredients.strip():
            st.warning("Please enter at least one ingredient.")

        else:
            with st.spinner("RecipeMentor is creating your recipe..."):

                try:
                    groq_client = Groq(
                        api_key=st.secrets["GROQ_API_KEY"]
                    )

                    prompt = f"""
                    Create an original and practical recipe.

                    Available ingredients: {ingredients}
                    Meal type: {meal_type}
                    Difficulty: {difficulty}

                    Include:
                    1. Recipe name
                    2. Short description
                    3. Preparation time
                    4. Cooking time
                    5. Ingredients with quantities
                    6. Step-by-step instructions
                    7. Helpful cooking tips

                    Keep the instructions clear and easy to follow.
                    Mention any additional ingredients that are needed.
                    """

                    response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are RecipeMentor, a creative and helpful cooking assistant."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        max_tokens=1500,
                        temperature=0.7
                    )

                    recipe = response.choices[0].message.content

                    st.session_state.recipe_result = recipe

                except Exception as e:
                    st.error(f"Could not generate recipe: {e}")

    if "recipe_result" in st.session_state:
        st.divider()
        st.subheader("Your AI Recipe")

        st.markdown(st.session_state.recipe_result)

        user_email = st.session_state.get("user_email", "")

        if st.button("♡ Save to Favourites", key="save_recipe"):
            try:
                save_favourite_recipe(
                    user_email,
                    st.session_state.recipe_result
                )

                st.success("Recipe saved to your favourites!")

            except Exception as e:
                st.error(f"Could not save recipe: {e}")

    st.subheader("Your AI Recipe")
    st.markdown(st.session_state.recipe_result)

    st.divider()

    if st.button("♡ Save to Favourites", key="save_recipe"):
        user_email = st.session_state.get("user_email")

        if user_email:
            save_favourite_recipe(
                user_email,
                st.session_state.recipe_result
            )

            st.success("Recipe saved to your favourites!")

        else:
            st.error("Please log in to save recipes.")


elif page == "🥗 NutriScan":

    st.title("NutriScan")
    st.caption("Explore the nutritional information of your food.")
    st.divider()

    st.subheader("Analyze your food")

    food = st.text_input(
        "Food name",
        placeholder="Example: Banana, rice, chicken..."
    )

    portion = st.number_input(
        "Portion size (grams)",
        min_value=1,
        max_value=2000,
        value=100
    )

    if st.button("Analyze Nutrition"):

        if not food.strip():
            st.warning("Please enter a food name.")

        else:
            with st.spinner("NutriScan is analyzing your food..."):

                try:
                    groq_client = Groq(
                        api_key=st.secrets["GROQ_API_KEY"]
                    )

                    prompt = f"""
                    Provide estimated nutritional information for:
                    Food: {food}
                    Portion: {portion} grams

                    Include:
                    - Calories (kcal)
                    - Protein (g)
                    - Carbohydrates (g)
                    - Fat (g)
                    - Fiber (g)
                    - Main vitamins and minerals

                    Also provide a short explanation of the nutritional
                    benefits of this food.

                    Use realistic approximate values.
                    Clearly state that values vary by preparation,
                    brand and ingredients.
                    Do not give medical advice.
                    """

                    response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are NutriScan, an informative food nutrition assistant."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        max_tokens=1200,
                        temperature=0.3
                    )

                    nutrition_result = response.choices[0].message.content

                    st.session_state.nutrition_result = nutrition_result

                except Exception as e:
                    st.error(f"Could not analyze food: {e}")

    if "nutrition_result" in st.session_state:
        st.divider()
        st.subheader("Nutrition Results")
        st.markdown(st.session_state.nutrition_result)



elif page == "🍃 FreshCheck":

    st.title("FreshCheck")
    st.caption("AI-powered visual freshness analysis")
    st.divider()

    st.subheader("Check your food")

    upload_tab, camera_tab = st.tabs(["Upload Image", "Take Photo"])

    with upload_tab:
        uploaded_image = st.file_uploader(
            "Upload a food image",
            type=["jpg", "jpeg", "png"],
            key="freshcheck_upload"
        )

    with camera_tab:
        camera_image = st.camera_input(
            "Take a food photo",
            key="freshcheck_camera"
        )

    if camera_image is not None:
        uploaded_image = camera_image

    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Uploaded food",
            width=400
        )

        if st.button("Analyze Freshness"):

            with st.spinner("FreshCheck is analyzing your food..."):

                try:
                    image_bytes = uploaded_image.getvalue()

                    base64_image = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    groq_client = Groq(
                        api_key=st.secrets["GROQ_API_KEY"]
                    )

                    response = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {
                                "role": "system",
                                "content": """
                                You are FreshCheck, an AI visual food
                                freshness assistant.
                                Analyze only visible characteristics.
                                Never claim that food is definitely safe
                                or unsafe based only on an image.
                                """
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """
                                        Analyze this fruit or vegetable.

                                        Include:
                                        1. Identify the food.
                                        2. Describe its visible appearance.
                                        3. Look for visible discoloration,
                                           bruising, wrinkles or damage.
                                        4. Give a cautious visual assessment.
                                        5. Suggest appropriate storage advice.

                                        Use these assessment labels:
                                        - Appears fresh
                                        - Possible signs of aging
                                        - Visible signs of spoilage

                                        Explain your observations.

                                        Important: A photograph cannot
                                        determine whether food is safe
                                        to eat.
                                        """
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:{uploaded_image.type};base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_completion_tokens=1200,
                        temperature=0.4
                    )

                    result = response.choices[0].message.content
                    st.session_state.fresh_result = result

                except Exception as e:
                    st.error(f"Freshness analysis failed: {e}")

    if "fresh_result" in st.session_state:
        st.divider()
        st.subheader("FreshCheck Results")
        st.markdown(st.session_state.fresh_result)


elif page == "💬 FoodChat":

    st.title("🥗NUTRIMIND AI")
    st.caption("Your intelligent food assistant")

    st.divider()

    if "food_chat_history" not in st.session_state:
        st.session_state.food_chat_history = []

    if not st.session_state.food_chat_history:
        st.markdown("## How can I help you today?")
        st.write("Ask me anything about food, recipes or nutrition.")

    for message in st.session_state.food_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask NUTRIMIND anything...")

    if question:

        st.session_state.food_chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("NUTRIMIND is thinking..."):

            try:
                history = st.session_state.food_chat_history[:-1]

                prompt = """
                You are NUTRIMIND AI, a helpful food assistant.
                Answer clearly about food, recipes and general nutrition.
                Do not provide medical diagnoses or extreme dieting advice.
                """

                groq_client = Groq(
                    api_key=st.secrets["GROQ_API_KEY"]
                )

                messages = [
                    {"role": "system", "content": prompt}
                ]

                messages.extend(history)

                messages.append({
                    "role": "user",
                    "content": question
                })

                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=messages,
                    max_tokens=3000,
                    temperature=0.6
                )

                answer = response.choices[0].message.content

            except Exception as e:
                answer = "AI is temporarily unavailable. Please try again."
                st.error(str(e))

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.food_chat_history.append({
            "role": "assistant",
            "content": answer
        })


elif page == "📅 MealPlanner":

    st.title("MealPlanner")
    st.caption("Your personal AI meal planner")
    st.divider()

    st.subheader("Create your meal plan")

    goal = st.selectbox(
        "What kind of meal plan do you want?",
        [
            "Balanced everyday meals",
            "Vegetarian meals",
            "Quick and easy meals",
            "Budget-friendly meals"
        ]
    )

    preferences = st.text_area(
        "Food preferences or allergies",
        placeholder="Example: I like pasta, rice and vegetables..."
    )

    days = st.selectbox(
        "Choose duration",
        ["1 day", "3 days", "5 days", "7 days"]
    )

    if st.button("Generate Meal Plan"):

        with st.spinner("Creating your meal plan..."):

            try:
                groq_client = Groq(
                    api_key=st.secrets["GROQ_API_KEY"]
                )

                prompt = f"""
Create a complete meal plan for {days}.

Type: {goal}
Preferences: {preferences}

IMPORTANT:
- Include EVERY requested day.
- Clearly label them Day 1, Day 2, etc.
- Include breakfast, lunch and dinner for EACH day.
- Give different meals for every day.
- Keep descriptions short and clear.
- Use balanced meals and ordinary ingredients.
"""

                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are NUTRIMIND AI, a helpful meal planning assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=1500,
                    temperature=0.6
                )

                meal_plan = response.choices[0].message.content
                st.session_state.meal_plan = meal_plan

            except Exception as e:
                st.error(f"Could not generate meal plan: {e}")

        if "meal_plan" in st.session_state:
            st.divider()
            st.subheader("Your AI Meal Plan")
            st.markdown(st.session_state.meal_plan)


elif page == "👤 Profile":

    st.title("My Profile")
    st.caption("Your personal NUTRIMIND AI space.")
    st.divider()

    user_email = st.session_state.get("user_email", "")

    st.subheader("Account Information")

    st.write(f"**Name:** {st.session_state.get('user_name', 'User')}")
    st.write(f"**Email:** {user_email}")

    st.divider()

    if  st.button("← Back to Home"):
        st.session_state.show_profile = False
        st.rerun()

    st.subheader("My Favourite Recipes")

    conn = get_db_connection()

    favourites = conn.execute("""
        SELECT id, recipe_name, recipe_content
        FROM favourite_recipes
        WHERE user_email = ?
        ORDER BY created_at DESC
    """, (user_email,)).fetchall()

    conn.close()

    if favourites:

        for recipe_id, recipe_name, recipe_content in favourites:

            with st.container(border=True):

                st.subheader(recipe_name)
                st.markdown(recipe_content)

                if st.button(
                    "Remove from Favourites",
                    key=f"remove_fav_{recipe_id}"
                ):

                    conn = get_db_connection()

                    conn.execute("""
                        DELETE FROM favourite_recipes
                        WHERE id = ? AND user_email = ?
                    """, (recipe_id, user_email))

                    conn.commit()
                    conn.close()

                    st.rerun()

    else:
        st.info("You haven't saved any recipes yet.")
        st.write("Go to RecipeMentor and save your favourite recipes!")

if "recipe_result" in st.session_state:
        st.divider()

        st.subheader("Your AI Recipe")
        st.markdown(st.session_state.recipe_result)

        st.divider()

        if st.button("♡ Save to Favourites", key="save_recipe"):
            user_email = st.session_state.get("user_email")

            if user_email:
                save_favourite_recipe(
                    user_email,
                    st.session_state.recipe_result
                )

                st.success("Recipe saved to your favourites!")

            else:
                st.error("Please log in to save recipes.")


# # GLOBAL FOOTER
# st.markdown("""
# <div class="nutri-footer">
#     <h4>NUTRIMIND AI</h4>
#     <p>Smart Food. Smarter Choices.</p>
#     <p style="margin-top:10px;">
#         AI-powered food intelligence
#     </p>
#     <p style="margin-top:10px;">
#         © 2026 NUTRIMIND AI. All rights reserved.
#     </p>
# </div>
# """, unsafe_allow_html=True)



# =====================================
# GLOBAL LIGHT MODE - NUTRIMIND AI
# =====================================

if st.session_state.get("theme") == "Light Mode":

    st.markdown("""
    <style>

    /* MAIN BACKGROUND */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background: #E7F1E7 !important;
        color: #294333 !important;
    }

    /* ALL TEXT */
    h1, h2, h3, h4, h5, p, label, span, li,
    .stMarkdown, .stCaption {
        color: #294333 !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #D8E9D9 !important;
        border-right: 1px solid #BBD4BE !important;
    }

    [data-testid="stSidebar"] * {
        color: #294333 !important;
    }

    /* TEXT INPUTS */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stDateInput input,
    .stTimeInput input,
    [data-testid="stChatInput"] textarea {
        background: #D8E9D9 !important;
        color: #294333 !important;
        -webkit-text-fill-color: #294333 !important;
        border: 1px solid #B5D0B9 !important;
        border-radius: 11px !important;
        box-shadow: none !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #718D76 !important;
        -webkit-text-fill-color: #718D76 !important;
    }

    /* INPUT FOCUS */
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {
        border: 1px solid #72A77B !important;
        box-shadow: 0 0 0 2px #72A77B25 !important;
    }

    /* SELECT BOXES */
    [data-baseweb="select"] > div,
    [data-baseweb="select"] input {
        background: #D8E9D9 !important;
        color: #294333 !important;
        border-color: #B5D0B9 !important;
    }

    [data-baseweb="select"] span {
        color: #294333 !important;
    }

    /* DROPDOWN MENUS */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"],
    [role="option"] {
        background: #D8E9D9 !important;
        color: #294333 !important;
    }

    [role="option"]:hover,
    [aria-selected="true"] {
        background: #BBD9BF !important;
        color: #23442D !important;
    }

    /* FILE UPLOADER */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] section > div {
        background: #D8E9D9 !important;
        border-color: #A9CBAF !important;
        border-radius: 13px !important;
    }

    [data-testid="stFileUploader"] section {
        border: 1px dashed #83B38C !important;
    }

    [data-testid="stFileUploader"] button {
        background: #B8D8BC !important;
        color: #294333 !important;
        border: 1px solid #A9CBAF !important;
    }

    [data-testid="stFileUploader"] * {
        color: #294333 !important;
    }

    /* CAMERA INPUT */
    [data-testid="stCameraInput"] {
        background: #D8E9D9 !important;
        border-radius: 13px !important;
    }

    /* BUTTONS */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] button {
        background: #A9CDAE !important;
        color: #23442D !important;
        border: 1px solid #91BB98 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        background: #91BD99 !important;
        color: #1E3C27 !important;
        border-color: #78A982 !important;
    }

    /* CARDS */
    [data-testid="stMetric"],
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stExpander"],
    [data-testid="stChatMessage"],
    [data-testid="stForm"] {
        background: #D8E9D9 !important;
        border: 1px solid #BDD5C0 !important;
        border-radius: 14px !important;
        color: #294333 !important;
    }

    /* CUSTOM MODULE CARDS */
    .module-card {
        background: #D8E9D9 !important;
        border-color: #BDD5C0 !important;
    }

    .module-card h3 {
        color: #34794A !important;
    }

    .module-card p {
        color: #526B58 !important;
    }

    .module-card:hover {
        background: #C9E1CC !important;
        border-color: #8DB995 !important;
    }

    /* TABS */
    [data-baseweb="tab-list"] {
        background: #D8E9D9 !important;
        border-radius: 10px !important;
    }

    [data-baseweb="tab"] {
        color: #294333 !important;
    }

    [aria-selected="true"][data-baseweb="tab"] {
        color: #34794A !important;
    }

    /* CHAT */
    [data-testid="stChatMessage"] {
        background: #D8E9D9 !important;
        border: 1px solid #BDD5C0 !important;
    }

    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div {
        background: #D8E9D9 !important;
        border-color: #B5D0B9 !important;
    }

    /* FOOTER */
    .nutri-footer {
        background: #D8E9D9 !important;
        border-color: #BDD5C0 !important;
    }

    .nutri-footer h4 {
        color: #34794A !important;
    }

    .nutri-footer p {
        color: #526B58 !important;
    }

    /* DIVIDERS */
    hr {
        border-color: #BDD5C0 !important;
    }

    /* NUMBER INPUT BUTTONS */
    [data-testid="stNumberInput"] button {
        background: #C5DEC8 !important;
        color: #294333 !important;
        border-color: #B5D0B9 !important;
    }

    /* CHECKBOXES AND RADIO */
    [data-testid="stCheckbox"],
    [data-testid="stRadio"] {
        color: #294333 !important;
    }

    /* SLIDERS */
    [data-testid="stSlider"] {
        color: #34794A !important;
    }

    </style>
    """, unsafe_allow_html=True)
