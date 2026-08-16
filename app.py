import streamlit as st
import pandas as pd
import json
import re
from datetime import datetime, timezone
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="STEM Pathways NYC",
    page_icon="🧭",
    layout="wide"
)


# ============================================================
# MODERN UI / BRAND STYLING
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --sp-bg: #f7f9fc;
        --sp-surface: #ffffff;
        --sp-surface-soft: #f0f4f8;
        --sp-border: #d9e2ec;
        --sp-text: #102a43;
        --sp-muted: #627d98;
        --sp-primary: #018FC7;
        --sp-primary-dark: #00658F;
        --sp-accent: #38BDF8;
        --sp-warning: #d97706;
        --sp-danger: #c2410c;
        --sp-success: #15803d;
        --sp-radius: 18px;
        --sp-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
    }

    /* Main app background */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top right, rgba(47, 128, 237, 0.08), transparent 28%),
            radial-gradient(circle at top left, rgba(1, 143, 199, 0.09), transparent 30%),
            var(--sp-bg);
        color: var(--sp-text);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1220px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #003F5C 0%, #00577D 55%, #003B57 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #f7fbfa;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #CBEAF6 !important;
        letter-spacing: 0.08em;
        font-weight: 700;
        font-size: 0.72rem;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.12);
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.06);
        color: white;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        min-height: 42px;
        font-weight: 600;
        transition: 0.18s ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.13);
        border-color: rgba(255,255,255,0.2);
        transform: translateY(-1px);
    }

    /* Typography */
    h1, h2, h3 {
        color: var(--sp-text) !important;
        letter-spacing: -0.02em;
    }

    h1 {
        font-weight: 800 !important;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 700 !important;
    }

    p, li, label {
        color: var(--sp-text);
    }

    /* Bordered Streamlit containers become cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.92);
        border: 1px solid var(--sp-border) !important;
        border-radius: var(--sp-radius) !important;
        box-shadow: var(--sp-shadow);
        overflow: hidden;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #b9c9d8 !important;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.09);
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.95);
        border: 1px solid var(--sp-border);
        border-radius: 16px;
        padding: 1rem 1.05rem;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: var(--sp-muted);
        font-weight: 700;
    }

    [data-testid="stMetricValue"] {
        color: var(--sp-text);
        font-weight: 800;
    }

    /* Main buttons */
    .stButton > button,
    .stLinkButton > a {
        border-radius: 12px !important;
        min-height: 42px;
        font-weight: 700 !important;
        transition: 0.18s ease !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #018FC7, #007EAF) !important;
        border: none !important;
        box-shadow: 0 6px 16px rgba(1, 143, 199, 0.22);
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 9px 22px rgba(1, 143, 199, 0.28);
    }

    .stLinkButton > a {
        border-color: var(--sp-border) !important;
        background: white !important;
        color: var(--sp-text) !important;
    }

    .stLinkButton > a:hover {
        border-color: var(--sp-accent) !important;
        color: var(--sp-accent) !important;
    }

    /* Inputs */
    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div,
    [data-baseweb="textarea"] > div {
        border-radius: 12px !important;
        border-color: var(--sp-border) !important;
        background: white !important;
    }

    [data-baseweb="tag"] {
        border-radius: 999px !important;
        background: #E6F6FC !important;
        color: var(--sp-primary-dark) !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        border: 1px solid var(--sp-border) !important;
        border-radius: 14px !important;
        background: rgba(255,255,255,0.9);
        overflow: hidden;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 14px !important;
        border-width: 1px !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid var(--sp-border);
    }

    /* Dividers */
    hr {
        border: none !important;
        border-top: 1px solid #dfe7ef !important;
        margin: 1.5rem 0 !important;
    }

    /* Progress bars */
    [data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, var(--sp-primary), var(--sp-accent)) !important;
    }

    /* Custom hero */
    .sp-hero {
        background:
            linear-gradient(135deg, rgba(0,63,92,0.99), rgba(1,143,199,0.95));
        border-radius: 24px;
        padding: 2.2rem 2.3rem;
        box-shadow: 0 18px 40px rgba(0, 63, 92, 0.20);
        margin: 0.4rem 0 1.5rem 0;
        position: relative;
        overflow: hidden;
    }

    .sp-hero::after {
        content: "";
        position: absolute;
        width: 240px;
        height: 240px;
        right: -70px;
        top: -90px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }

    .sp-hero h1 {
        color: white !important;
        margin: 0 0 0.45rem 0;
        font-size: 2.25rem;
        line-height: 1.05;
    }

    .sp-hero p {
        color: #E1F5FC !important;
        margin: 0;
        font-size: 1.02rem;
        max-width: 760px;
    }

    .sp-kicker {
        color: #BDEBFA !important;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        font-size: 0.74rem;
        font-weight: 800;
        margin-bottom: 0.7rem;
    }

    .sp-section-subtitle {
        color: var(--sp-muted);
        margin-top: -0.4rem;
        margin-bottom: 1rem;
    }

    .sp-pill {
        display: inline-block;
        padding: 0.32rem 0.62rem;
        margin: 0.15rem 0.15rem 0.15rem 0;
        border-radius: 999px;
        background: #E7F6FC;
        color: #00658F;
        border: 1px solid #B9E5F5;
        font-size: 0.82rem;
        font-weight: 700;
    }

    /* Mobile spacing */
    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"] {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .sp-hero {
            padding: 1.5rem;
            border-radius: 18px;
        }

        .sp-hero h1 {
            font-size: 1.7rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)



# ============================================================
# SUPABASE
# ============================================================

@st.cache_resource
def init_supabase():
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["service_key"]
    )


try:
    supabase = init_supabase()
    supabase_connected = True

except Exception as e:
    supabase = None
    supabase_connected = False
    supabase_error = str(e)


# ============================================================
# LOCAL DATABASES
# ============================================================

try:
    opportunities = pd.read_csv("data/opportunities.csv")
except Exception:
    opportunities = pd.DataFrame()


try:
    careers = pd.read_csv("data/careers.csv")
except Exception:
    careers = pd.DataFrame()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_salary(value):

    if pd.isna(value):
        return "Data unavailable"

    try:
        return f"${int(float(value)):,}"

    except Exception:
        return "Data unavailable"


def list_to_text(items):
    return json.dumps(
        items,
        ensure_ascii=False
    )


def text_to_list(value):

    if value is None:
        return []

    try:

        result = json.loads(value)

        if isinstance(result, list):
            return result

        return []

    except Exception:
        return []


def get_google_user():

    try:
        user_sub = st.user.get("sub")
    except Exception:
        user_sub = None

    try:
        email = st.user.get("email")
    except Exception:
        email = None

    try:
        google_name = st.user.get("name")
    except Exception:
        google_name = None

    return (
        str(user_sub) if user_sub else None,
        str(email) if email else "",
        str(google_name) if google_name else ""
    )


def load_profile(user_sub):

    if not supabase_connected:
        return None

    try:

        response = (
            supabase
            .table("student_profiles")
            .select("*")
            .eq("user_sub", user_sub)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        row = response.data[0]

        return {
            "id": row.get("id"),

            "first_name":
                row.get("first_name", ""),

            "middle_name":
                row.get("middle_name", ""),

            "last_name":
                row.get("last_name", ""),

            "age":
                row.get("age", 15),

            "grade":
                row.get("grade", "9"),

            "borough":
                row.get("borough", "Bronx"),

            "interests":
                text_to_list(
                    row.get("interests")
                ),

            "experience_areas":
                text_to_list(
                    row.get("experience_areas")
                ),

            "goals":
                text_to_list(
                    row.get("goals")
                ),

            "exploration_stage":
                row.get(
                    "exploration_stage",
                    "I am just starting to explore STEM."
                ),

            "confidence":
                row.get("confidence", 5),

            "weekly_time":
                row.get(
                    "weekly_time",
                    "2–5 hours"
                ),

            "financial_support":
                row.get(
                    "financial_support",
                    False
                )
        }

    except Exception as e:

        st.error(
            "We could not load your saved profile."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return None


def save_profile(
    user_sub,
    email,
    profile
):

    if not supabase_connected:
        return False

    now = datetime.now(
        timezone.utc
    ).isoformat()

    data = {

        "user_sub":
            user_sub,

        "email":
            email,

        "first_name":
            profile["first_name"],

        "middle_name":
            profile["middle_name"],

        "last_name":
            profile["last_name"],

        "age":
            int(profile["age"]),

        "grade":
            profile["grade"],

        "borough":
            profile["borough"],

        "interests":
            list_to_text(
                profile["interests"]
            ),

        "experience_areas":
            list_to_text(
                profile["experience_areas"]
            ),

        "goals":
            list_to_text(
                profile["goals"]
            ),

        "exploration_stage":
            profile["exploration_stage"],

        "confidence":
            int(profile["confidence"]),

        "weekly_time":
            profile["weekly_time"],

        "financial_support":
            bool(
                profile["financial_support"]
            ),

        "updated_at":
            now
    }

    try:

        existing = (
            supabase
            .table("student_profiles")
            .select("id")
            .eq("user_sub", user_sub)
            .limit(1)
            .execute()
        )

        if existing.data:

            profile_id = (
                existing.data[0]["id"]
            )

            (
                supabase
                .table("student_profiles")
                .update(data)
                .eq("id", profile_id)
                .execute()
            )

        else:

            data["created_at"] = now

            (
                supabase
                .table("student_profiles")
                .insert(data)
                .execute()
            )

        return True

    except Exception as e:

        st.error(
            "Your profile could not be saved."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return False


# ============================================================
# SAVED OPPORTUNITIES / APPLICATION TRACKER
# ============================================================

APPLICATION_STATUSES = [
    "Saved",
    "Planning to Apply",
    "Applying",
    "Applied",
    "Accepted",
    "Waitlisted",
    "Not Selected"
]


def load_saved_opportunities(user_sub):

    if not supabase_connected:
        return []

    try:

        response = (
            supabase
            .table("saved_opportunities")
            .select("*")
            .eq("user_sub", user_sub)
            .order("saved_at", desc=True)
            .execute()
        )

        return response.data or []

    except Exception as e:

        st.error(
            "We could not load your saved opportunities."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return []


def save_opportunity(user_sub, opportunity_name):

    if not supabase_connected:
        return False

    now = datetime.now(
        timezone.utc
    ).isoformat()

    try:

        existing = (
            supabase
            .table("saved_opportunities")
            .select("id")
            .eq("user_sub", user_sub)
            .eq("opportunity_name", opportunity_name)
            .limit(1)
            .execute()
        )

        if existing.data:

            return True

        (
            supabase
            .table("saved_opportunities")
            .insert({
                "user_sub":
                    user_sub,

                "opportunity_name":
                    opportunity_name,

                "status":
                    "Saved",

                "notes":
                    "",

                "saved_at":
                    now,

                "updated_at":
                    now
            })
            .execute()
        )

        return True

    except Exception as e:

        st.error(
            "This opportunity could not be saved."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return False


def update_saved_opportunity(
    saved_id,
    status,
    notes
):

    if not supabase_connected:
        return False

    try:

        (
            supabase
            .table("saved_opportunities")
            .update({
                "status":
                    status,

                "notes":
                    notes,

                "updated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            })
            .eq("id", saved_id)
            .execute()
        )

        return True

    except Exception as e:

        st.error(
            "Your application tracker could not be updated."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return False


def delete_saved_opportunity(saved_id):

    if not supabase_connected:
        return False

    try:

        (
            supabase
            .table("saved_opportunities")
            .delete()
            .eq("id", saved_id)
            .execute()
        )

        return True

    except Exception as e:

        st.error(
            "This opportunity could not be removed."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return False


def saved_opportunity_names(user_sub):

    saved = load_saved_opportunities(
        user_sub
    )

    return {
        str(item.get("opportunity_name", ""))
        for item in saved
    }



# ============================================================
# FAVORITE COLLEGES
# ============================================================

def load_favorite_colleges(user_sub):

    if not supabase_connected:
        return []

    try:

        response = (
            supabase
            .table("favorite_colleges")
            .select("*")
            .eq("user_sub", user_sub)
            .order("rank_order")
            .execute()
        )

        return response.data or []

    except Exception as e:

        st.error(
            "We could not load your favorite colleges."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return []


def add_favorite_college(
    user_sub,
    college_name
):

    if not supabase_connected:
        return False

    try:

        existing = (
            supabase
            .table("favorite_colleges")
            .select("id")
            .eq("user_sub", user_sub)
            .eq("college_name", college_name)
            .limit(1)
            .execute()
        )

        if existing.data:
            return True

        current = load_favorite_colleges(
            user_sub
        )

        next_rank = len(current) + 1

        now = datetime.now(
            timezone.utc
        ).isoformat()

        (
            supabase
            .table("favorite_colleges")
            .insert({
                "user_sub":
                    user_sub,

                "college_name":
                    college_name,

                "rank_order":
                    next_rank,

                "notes":
                    "",

                "saved_at":
                    now,

                "updated_at":
                    now
            })
            .execute()
        )

        return True

    except Exception as e:

        st.error(
            "This college could not be added to your favorites."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return False


def update_favorite_college_notes(
    favorite_id,
    notes
):

    if not supabase_connected:
        return False

    try:

        (
            supabase
            .table("favorite_colleges")
            .update({
                "notes":
                    notes,

                "updated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            })
            .eq("id", favorite_id)
            .execute()
        )

        return True

    except Exception as e:

        st.error(
            "Your college notes could not be updated."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return False


def reorder_favorite_colleges(
    user_sub,
    favorite_id,
    direction
):

    favorites = load_favorite_colleges(
        user_sub
    )

    if not favorites:
        return False

    current_index = next(
        (
            index
            for index, item
            in enumerate(favorites)
            if item["id"] == favorite_id
        ),
        None
    )

    if current_index is None:
        return False

    if (
        direction == "up"
        and
        current_index == 0
    ):
        return True

    if (
        direction == "down"
        and
        current_index
        == len(favorites) - 1
    ):
        return True

    swap_index = (
        current_index - 1
        if direction == "up"
        else current_index + 1
    )

    current_item = favorites[
        current_index
    ]

    swap_item = favorites[
        swap_index
    ]

    try:

        (
            supabase
            .table("favorite_colleges")
            .update({
                "rank_order":
                    swap_item[
                        "rank_order"
                    ],

                "updated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            })
            .eq(
                "id",
                current_item["id"]
            )
            .execute()
        )

        (
            supabase
            .table("favorite_colleges")
            .update({
                "rank_order":
                    current_item[
                        "rank_order"
                    ],

                "updated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            })
            .eq(
                "id",
                swap_item["id"]
            )
            .execute()
        )

        return True

    except Exception as e:

        st.error(
            "Your favorite college order could not be updated."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return False


def remove_favorite_college(
    user_sub,
    favorite_id
):

    if not supabase_connected:
        return False

    try:

        (
            supabase
            .table("favorite_colleges")
            .delete()
            .eq("id", favorite_id)
            .execute()
        )

        # Re-number remaining favorites so the order stays clean.
        remaining = load_favorite_colleges(
            user_sub
        )

        for index, item in enumerate(
            remaining,
            start=1
        ):

            if item.get(
                "rank_order"
            ) != index:

                (
                    supabase
                    .table("favorite_colleges")
                    .update({
                        "rank_order":
                            index,

                        "updated_at":
                            datetime.now(
                                timezone.utc
                            ).isoformat()
                    })
                    .eq(
                        "id",
                        item["id"]
                    )
                    .execute()
                )

        return True

    except Exception as e:

        st.error(
            "This college could not be removed from your favorites."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(str(e))

        return False



# ============================================================
# USER FEEDBACK / REVIEWS
# ============================================================

def load_user_feedback(user_sub):

    if not supabase_connected:
        return None

    try:

        response = (
            supabase
            .table("user_feedback")
            .select("*")
            .eq("user_sub", user_sub)
            .limit(1)
            .execute()
        )

        if response.data:
            return response.data[0]

        return None

    except Exception:
        return None


def save_user_feedback(
    user_sub,
    email,
    feedback
):

    if not supabase_connected:
        return False

    now = datetime.now(
        timezone.utc
    ).isoformat()

    data = {
        "user_sub":
            user_sub,

        "email":
            email,

        "rating":
            int(
                feedback[
                    "rating"
                ]
            ),

        "ease_of_use":
            int(
                feedback[
                    "ease_of_use"
                ]
            ),

        "overall_feeling":
            feedback[
                "overall_feeling"
            ],

        "favorite_features":
            list_to_text(
                feedback[
                    "favorite_features"
                ]
            ),

        "improvements":
            feedback[
                "improvements"
            ],

        "additional_comments":
            feedback[
                "additional_comments"
            ],

        "would_recommend":
            feedback[
                "would_recommend"
            ],

        "updated_at":
            now
    }

    try:

        existing = (
            supabase
            .table("user_feedback")
            .select("id")
            .eq("user_sub", user_sub)
            .limit(1)
            .execute()
        )

        if existing.data:

            (
                supabase
                .table("user_feedback")
                .update(data)
                .eq(
                    "id",
                    existing.data[0][
                        "id"
                    ]
                )
                .execute()
            )

        else:

            data[
                "created_at"
            ] = now

            (
                supabase
                .table("user_feedback")
                .insert(
                    data
                )
                .execute()
            )

        return True

    except Exception as e:

        st.error(
            "Your feedback could not be saved."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(
                str(e)
            )

        return False



# ============================================================
# ADMIN DASHBOARD
# ============================================================

def get_admin_emails():

    try:

        configured = st.secrets.get(
            "admin_emails",
            []
        )

        if isinstance(
            configured,
            str
        ):

            return {
                configured.strip().lower()
            }

        return {
            str(email).strip().lower()
            for email in configured
            if str(email).strip()
        }

    except Exception:

        return set()


def is_admin_user(email):

    admin_emails = get_admin_emails()

    return (
        str(email).strip().lower()
        in admin_emails
    )


def load_admin_metrics():

    if not supabase_connected:

        return {
            "profiles": [],
            "feedback": [],
            "saved_opportunities": [],
            "favorite_colleges": []
        }

    data = {
        "profiles": [],
        "feedback": [],
        "saved_opportunities": [],
        "favorite_colleges": []
    }

    table_map = {
        "profiles":
            "student_profiles",

        "feedback":
            "user_feedback",

        "saved_opportunities":
            "saved_opportunities",

        "favorite_colleges":
            "favorite_colleges"
    }

    for key, table_name in table_map.items():

        try:

            response = (
                supabase
                .table(
                    table_name
                )
                .select("*")
                .execute()
            )

            data[
                key
            ] = response.data or []

        except Exception:

            data[
                key
            ] = []

    return data



# ============================================================
# GOOGLE LOGIN
# ============================================================

if not st.user.is_logged_in:

    st.title(
        "STEM Pathways NYC"
    )

    st.subheader(
        "Explore your interests. Build your pathway. Discover what's next."
    )

    st.write(
        "A student-focused platform designed to help high school "
        "students explore STEM careers, majors, projects, skills, "
        "and opportunities."
    )

    st.divider()

    col1, col2, col3 = st.columns(
        [1, 1.4, 1]
    )

    with col2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Welcome"
            )

            st.write(
                "Sign in to create and save your personalized STEM pathway."
            )

            if st.button(
                "Continue with Google",
                type="primary",
                use_container_width=True
            ):
                st.login("google")

    st.stop()


# ============================================================
# LOGGED-IN USER
# ============================================================

user_sub, user_email, google_name = (
    get_google_user()
)


if not user_sub:

    st.error(
        "Google login succeeded, but the app could not retrieve "
        "your account identifier."
    )

    if st.button(
        "Sign Out"
    ):
        st.logout()

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "profile_loaded" not in st.session_state:
    st.session_state.profile_loaded = False

if "profile_completed" not in st.session_state:
    st.session_state.profile_completed = False

if "student_profile" not in st.session_state:
    st.session_state.student_profile = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "career_results" not in st.session_state:
    st.session_state.career_results = None


# ============================================================
# AUTOMATIC PROFILE LOAD
# ============================================================

if not st.session_state.profile_loaded:

    saved_profile = load_profile(
        user_sub
    )

    if saved_profile:

        st.session_state.student_profile = (
            saved_profile
        )

        st.session_state.profile_completed = (
            True
        )

    else:

        st.session_state.profile_completed = (
            False
        )

    st.session_state.profile_loaded = True


# ============================================================
# PROFILE FORM
# ============================================================

if not st.session_state.profile_completed:

    existing_profile = (
        st.session_state.student_profile
    )

    st.title(
        "Create Your STEM Explorer Profile"
    )

    st.write(
        f"Signed in as **{user_email}**"
    )

    st.write(
        "Answer a few questions so STEM Pathways NYC can personalize "
        "your career, major, project, and opportunity recommendations."
    )

    st.divider()

    # --------------------------------------------------------
    # ABOUT YOU
    # --------------------------------------------------------

    st.header(
        "1. About You"
    )

    col1, col2 = st.columns(2)

    with col1:

        first_name = st.text_input(
            "First name",
            value=existing_profile.get(
                "first_name",
                ""
            )
        )

    with col2:

        last_name = st.text_input(
            "Last name",
            value=existing_profile.get(
                "last_name",
                ""
            )
        )

    middle_name = st.text_input(
        "Middle name (optional)",
        value=existing_profile.get(
            "middle_name",
            ""
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        age = st.number_input(
            "Age",
            min_value=13,
            max_value=19,
            value=int(
                existing_profile.get(
                    "age",
                    15
                )
            ),
            step=1
        )

    grade_options = [
        "9",
        "10",
        "11",
        "12"
    ]

    current_grade = str(
        existing_profile.get(
            "grade",
            "9"
        )
    )

    with col2:

        grade = st.selectbox(
            "Grade",
            grade_options,
            index=(
                grade_options.index(
                    current_grade
                )
                if current_grade
                in grade_options
                else 0
            )
        )

    borough_options = [
        "Bronx",
        "Manhattan",
        "Brooklyn",
        "Queens",
        "Staten Island"
    ]

    current_borough = (
        existing_profile.get(
            "borough",
            "Bronx"
        )
    )

    with col3:

        borough = st.selectbox(
            "Borough",
            borough_options,
            index=(
                borough_options.index(
                    current_borough
                )
                if current_borough
                in borough_options
                else 0
            )
        )

    st.divider()

    # --------------------------------------------------------
    # INTERESTS
    # --------------------------------------------------------

    st.header(
        "2. Your STEM Interests"
    )

    interest_options = [
        "Engineering",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Computer Engineering",
        "Computer Science",
        "Artificial Intelligence",
        "Data Science",
        "Biomedical Engineering",
        "Biology",
        "Physics",
        "Mathematics",
        "Environmental Science",
        "Robotics",
        "Not sure yet"
    ]

    interests = st.multiselect(
        "Which STEM fields currently interest you?",
        interest_options,
        default=existing_profile.get(
            "interests",
            []
        )
    )

    experience_options = [
        "Coding",
        "Electronics",
        "Circuit Design",
        "CAD / 3D Design",
        "3D Printing",
        "Robotics",
        "Scientific Research",
        "Engineering Projects",
        "Data Analysis",
        "Math Competitions",
        "Science Competitions",
        "None yet"
    ]

    experience_areas = st.multiselect(
        "Which STEM activities have you tried?",
        experience_options,
        default=existing_profile.get(
            "experience_areas",
            []
        )
    )

    st.divider()

    # --------------------------------------------------------
    # GOALS
    # --------------------------------------------------------

    st.header(
        "3. Your Goals"
    )

    goal_options = [
        "Build STEM projects",
        "Learn technical skills",
        "Explore STEM careers",
        "Find summer programs",
        "Find internships",
        "Participate in research",
        "Take college courses",
        "Enter competitions",
        "Prepare for a STEM major"
    ]

    goals = st.multiselect(
        "What would you like to do next?",
        goal_options,
        default=existing_profile.get(
            "goals",
            []
        )
    )

    stage_options = [
        "I am just starting to explore STEM.",
        "I have a few STEM interests but I am still exploring.",
        "I know which STEM fields interest me.",
        "I have experience and want to develop more advanced skills.",
        "I already have a specific STEM career or major in mind."
    ]

    current_stage = (
        existing_profile.get(
            "exploration_stage",
            stage_options[0]
        )
    )

    exploration_stage = st.radio(
        "Where are you currently in your STEM journey?",
        stage_options,
        index=(
            stage_options.index(
                current_stage
            )
            if current_stage
            in stage_options
            else 0
        )
    )

    confidence = st.slider(
        "How confident are you about your current STEM interests?",
        1,
        10,
        int(
            existing_profile.get(
                "confidence",
                5
            )
        )
    )

    weekly_options = [
        "Less than 2 hours",
        "2–5 hours",
        "5–10 hours",
        "10+ hours"
    ]

    current_weekly = (
        existing_profile.get(
            "weekly_time",
            "2–5 hours"
        )
    )

    weekly_time = st.selectbox(
        "How much time would you like to spend exploring STEM each week?",
        weekly_options,
        index=(
            weekly_options.index(
                current_weekly
            )
            if current_weekly
            in weekly_options
            else 1
        )
    )

    financial_support = st.checkbox(
        "Prioritize free opportunities or programs offering financial aid",
        value=bool(
            existing_profile.get(
                "financial_support",
                False
            )
        )
    )

    st.divider()

    if st.button(
        "Save My STEM Profile",
        type="primary",
        use_container_width=True
    ):

        if not first_name.strip():

            st.warning(
                "Please enter your first name."
            )

        elif not last_name.strip():

            st.warning(
                "Please enter your last name."
            )

        elif not interests:

            st.warning(
                "Please choose at least one STEM interest."
            )

        elif not goals:

            st.warning(
                "Please choose at least one goal."
            )

        else:

            profile = {

                "first_name":
                    first_name.strip(),

                "middle_name":
                    middle_name.strip(),

                "last_name":
                    last_name.strip(),

                "age":
                    age,

                "grade":
                    grade,

                "borough":
                    borough,

                "interests":
                    interests,

                "experience_areas":
                    experience_areas,

                "goals":
                    goals,

                "exploration_stage":
                    exploration_stage,

                "confidence":
                    confidence,

                "weekly_time":
                    weekly_time,

                "financial_support":
                    financial_support
            }

            saved = save_profile(
                user_sub,
                user_email,
                profile
            )

            if saved:

                st.session_state.student_profile = (
                    profile
                )

                st.session_state.profile_completed = (
                    True
                )

                st.session_state.current_page = (
                    "Dashboard"
                )

                st.success(
                    "Your STEM profile has been saved."
                )

                st.rerun()

    st.divider()

    if st.button(
        "Sign Out"
    ):
        st.logout()

    st.stop()


# ============================================================
# PROFILE
# ============================================================

profile = st.session_state.student_profile


if profile.get("middle_name"):

    full_name = (
        f"{profile['first_name']} "
        f"{profile['middle_name']} "
        f"{profile['last_name']}"
    )

else:

    full_name = (
        f"{profile['first_name']} "
        f"{profile['last_name']}"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "STEM Pathways NYC"
    )

    st.write(
        f"**{full_name}**"
    )

    st.caption(
        f"Grade {profile['grade']} "
        f"• {profile['borough']}"
    )

    st.caption(
        user_email
    )

    st.divider()

    st.caption(
        "HOME"
    )

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "Dashboard"
        )

        st.rerun()

    if st.button(
        "🧭 My STEM Pathway",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "My STEM Pathway"
        )

        st.rerun()

    st.divider()

    st.caption(
        "DISCOVER"
    )

    if st.button(
        "💼 Opportunities",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "Opportunities"
        )

        st.rerun()

    if st.button(
        "📅 Deadline Calendar",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "Deadline Calendar"
        )

        st.rerun()

    if st.button(
        "🎓 College Suggestions",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "College Suggestions"
        )

        st.rerun()

    if st.button(
        "🛠️ Project Explorer",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "Projects"
        )

        st.rerun()

    if st.button(
        "📚 Resources",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "Resources"
        )

        st.rerun()

    st.divider()

    st.caption(
        "MY PROGRESS"
    )

    if st.button(
        "📌 My Applications",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "My Applications"
        )

        st.rerun()

    if st.button(
        "⭐ Favorite Colleges",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "My Favorite Colleges"
        )

        st.rerun()

    st.divider()

    st.caption(
        "TOOLS"
    )

    if st.button(
        "📊 GPA Calculator",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "GPA Calculator"
        )

        st.rerun()

    st.divider()

    st.caption(
        "ACCOUNT"
    )

    if st.button(
        "💬 Feedback",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "Feedback"
        )

        st.rerun()

    if st.button(
        "👤 My Profile",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "My Profile"
        )

        st.rerun()

    if st.button(
        "🚪 Sign Out",
        use_container_width=True
    ):

        st.logout()

    if is_admin_user(
        user_email
    ):

        st.divider()

        st.caption(
            "ADMIN"
        )

        if st.button(
            "⚙️ Admin Dashboard",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "Admin Dashboard"
            )

            st.rerun()

    st.divider()

    st.caption(
        "Explore • Build • Discover"
    )


page = st.session_state.current_page


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    # --------------------------------------------------------
    # LOAD PERSONAL DASHBOARD DATA
    # --------------------------------------------------------

    dashboard_saved_apps = load_saved_opportunities(
        user_sub
    )

    dashboard_favorites = load_favorite_colleges(
        user_sub
    )

    primary_interest = (
        profile["interests"][0]
        if profile.get(
            "interests"
        )
        else
        "Exploring STEM"
    )

    application_status_counts = {}

    for item in dashboard_saved_apps:

        status = str(
            item.get(
                "status",
                "Saved"
            )
        ).strip()

        application_status_counts[
            status
        ] = (
            application_status_counts.get(
                status,
                0
            )
            + 1
        )

    active_applications = sum(
        application_status_counts.get(
            status,
            0
        )
        for status in [
            "Planning to Apply",
            "Applying"
        ]
    )

    submitted_applications = sum(
        application_status_counts.get(
            status,
            0
        )
        for status in [
            "Applied",
            "Accepted",
            "Waitlisted",
            "Not Selected"
        ]
    )

    # --------------------------------------------------------
    # NEXT SAVED DEADLINE
    # --------------------------------------------------------

    def dashboard_parse_deadline(
        value
    ):

        if (
            value is None
            or
            pd.isna(
                value
            )
        ):

            return None

        raw = str(
            value
        ).strip()

        if not raw:

            return None

        try:

            parsed = pd.to_datetime(
                raw,
                errors="coerce"
            )

            if pd.notna(
                parsed
            ):

                return parsed.to_pydatetime()

        except Exception:

            pass

        month_pattern = (
            r"(January|February|March|April|May|June|July|August|"
            r"September|October|November|December)\s+\d{1,2},\s+\d{4}"
        )

        match = re.search(
            month_pattern,
            raw,
            flags=re.IGNORECASE
        )

        if match:

            parsed = pd.to_datetime(
                match.group(0),
                errors="coerce"
            )

            if pd.notna(
                parsed
            ):

                return parsed.to_pydatetime()

        return None


    next_saved_deadline = None

    if (
        dashboard_saved_apps
        and
        not opportunities.empty
    ):

        saved_name_set = {
            str(
                item.get(
                    "opportunity_name",
                    ""
                )
            )
            for item in dashboard_saved_apps
        }

        deadline_candidates = []

        for _, opportunity in opportunities.iterrows():

            opportunity_name = str(
                opportunity.get(
                    "name",
                    ""
                )
            )

            if (
                opportunity_name
                not in saved_name_set
            ):

                continue

            parsed_deadline = dashboard_parse_deadline(
                opportunity.get(
                    "deadline"
                )
            )

            if parsed_deadline is None:

                continue

            if parsed_deadline.tzinfo is None:

                parsed_deadline = (
                    parsed_deadline.replace(
                        tzinfo=timezone.utc
                    )
                )

            days_left = (
                parsed_deadline.date()
                -
                datetime.now(
                    timezone.utc
                ).date()
            ).days

            if days_left >= 0:

                deadline_candidates.append(
                    (
                        parsed_deadline,
                        days_left,
                        opportunity_name,
                        str(
                            opportunity.get(
                                "organization",
                                ""
                            )
                        )
                    )
                )

        if deadline_candidates:

            deadline_candidates.sort(
                key=lambda item:
                    item[0]
            )

            next_saved_deadline = (
                deadline_candidates[0]
            )

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="sp-hero">
            <div class="sp-kicker">Your personalized STEM workspace</div>
            <h1>Welcome back, {profile['first_name']} 👋</h1>
            <p>
                Explore careers, discover colleges and opportunities,
                build projects, and keep your STEM journey organized in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # JOURNEY SNAPSHOT
    # --------------------------------------------------------

    st.header(
        "Your STEM Journey"
    )

    st.markdown(
        '<div class="sp-section-subtitle">A quick snapshot of where you are right now.</div>',
        unsafe_allow_html=True
    )

    journey1, journey2, journey3, journey4 = (
        st.columns(4)
    )

    with journey1:

        st.metric(
            "Primary Interest",
            primary_interest
        )

    with journey2:

        st.metric(
            "Saved Programs",
            len(
                dashboard_saved_apps
            )
        )

    with journey3:

        st.metric(
            "Favorite Colleges",
            len(
                dashboard_favorites
            )
        )

    with journey4:

        st.metric(
            "Applications Submitted",
            submitted_applications
        )

    # --------------------------------------------------------
    # NEXT DEADLINE BANNER
    # --------------------------------------------------------

    if next_saved_deadline:

        deadline_dt, days_left, program_name, organization = (
            next_saved_deadline
        )

        if days_left == 0:

            deadline_message = (
                "Due today"
            )

        elif days_left == 1:

            deadline_message = (
                "1 day remaining"
            )

        else:

            deadline_message = (
                f"{days_left} days remaining"
            )

        with st.container(
            border=True
        ):

            deadline_col1, deadline_col2 = (
                st.columns(
                    [4, 1]
                )
            )

            with deadline_col1:

                st.subheader(
                    "📅 Your Next Saved Deadline"
                )

                st.write(
                    f"**{program_name}**"
                )

                if organization:

                    st.caption(
                        organization
                    )

                st.write(
                    deadline_dt.strftime(
                        "%B %d, %Y"
                    ).replace(
                        " 0",
                        " "
                    )
                )

            with deadline_col2:

                st.metric(
                    "Time Left",
                    deadline_message
                )

            if st.button(
                "Open Deadline Calendar",
                key="dashboard_deadline_calendar",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "Deadline Calendar"
                )

                st.rerun()

    elif dashboard_saved_apps:

        st.info(
            "You have saved opportunities, but none currently have a "
            "specific upcoming deadline in the database."
        )

    else:

        st.info(
            "Save opportunities you care about and their upcoming deadlines "
            "will appear here automatically."
        )

    st.divider()

    # --------------------------------------------------------
    # CONTINUE YOUR JOURNEY
    # --------------------------------------------------------

    st.header(
        "Continue Your Journey"
    )

    st.markdown(
        '<div class="sp-section-subtitle">Choose what you want to work on next.</div>',
        unsafe_allow_html=True
    )

    action_row1 = st.columns(3)

    with action_row1[0]:

        with st.container(
            border=True
        ):

            st.subheader(
                "🧭 Explore Your Path"
            )

            st.write(
                "Discover majors, careers, salary data, skills, and "
                "possible STEM directions."
            )

            if st.button(
                "Open My STEM Pathway",
                key="dashboard_pathway_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "My STEM Pathway"
                )

                st.rerun()

    with action_row1[1]:

        with st.container(
            border=True
        ):

            st.subheader(
                "🎓 Discover Colleges"
            )

            st.write(
                "Answer simple questions and find colleges connected "
                "to your interests and preferences."
            )

            if st.button(
                "Find College Matches",
                key="dashboard_colleges_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "College Suggestions"
                )

                st.rerun()

    with action_row1[2]:

        with st.container(
            border=True
        ):

            st.subheader(
                "🛠️ Build Something"
            )

            st.write(
                "Get personalized project ideas based on what you want "
                "to create and the tools you have."
            )

            if st.button(
                "Explore Projects",
                key="dashboard_projects_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "Projects"
                )

                st.rerun()

    action_row2 = st.columns(3)

    with action_row2[0]:

        with st.container(
            border=True
        ):

            st.subheader(
                "💼 Find Opportunities"
            )

            st.write(
                "Discover programs, research, internships, courses, "
                "and scholarships."
            )

            if st.button(
                "Browse Opportunities",
                key="dashboard_opportunities_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "Opportunities"
                )

                st.rerun()

    with action_row2[1]:

        with st.container(
            border=True
        ):

            st.subheader(
                "📌 Track Applications"
            )

            if active_applications:

                st.write(
                    f"You currently have **{active_applications}** "
                    f"application(s) in progress."
                )

            elif dashboard_saved_apps:

                st.write(
                    f"You have **{len(dashboard_saved_apps)}** saved "
                    "opportunity/opportunities."
                )

            else:

                st.write(
                    "Save opportunities and manage your application "
                    "progress in one place."
                )

            if st.button(
                "Open My Applications",
                key="dashboard_applications_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "My Applications"
                )

                st.rerun()

    with action_row2[2]:

        with st.container(
            border=True
        ):

            st.subheader(
                "⭐ Review Your College List"
            )

            if dashboard_favorites:

                top_favorite = (
                    dashboard_favorites[0].get(
                        "college_name",
                        "Your top college"
                    )
                )

                st.write(
                    f"Your current #1 favorite is **{top_favorite}**."
                )

            else:

                st.write(
                    "Save colleges you like and arrange them in your "
                    "personal order."
                )

            if st.button(
                "Open Favorite Colleges",
                key="dashboard_favorites_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "My Favorite Colleges"
                )

                st.rerun()

    st.divider()

    # --------------------------------------------------------
    # YOUR CURRENT DIRECTION
    # --------------------------------------------------------

    st.header(
        "Your Current Direction"
    )

    direction_col1, direction_col2 = (
        st.columns(
            [2, 1]
        )
    )

    with direction_col1:

        with st.container(
            border=True
        ):

            st.subheader(
                primary_interest
            )

            st.write(
                "This is currently your primary STEM interest. "
                "It can change as you explore new fields and experiences."
            )

            st.write(
                f"**Exploration stage:** "
                f"{profile['exploration_stage']}"
            )

            st.write(
                f"**Weekly STEM goal:** "
                f"{profile['weekly_time']}"
            )

    with direction_col2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Quick Profile"
            )

            st.write(
                f"**Grade:** {profile['grade']}"
            )

            st.write(
                f"**Borough:** {profile['borough']}"
            )

            st.write(
                f"**Interest confidence:** "
                f"{profile['confidence']}/10"
            )

            if profile.get(
                "financial_support"
            ):

                st.write(
                    "**Opportunity preference:** "
                    "Free / financially supported"
                )

    # --------------------------------------------------------
    # INTERESTS
    # --------------------------------------------------------

    st.divider()

    st.header(
        "Your STEM Interests"
    )

    if profile.get(
        "interests"
    ):

        interest_pills = "".join(
            [
                f'<span class="sp-pill">{interest}</span>'
                for interest
                in profile[
                    "interests"
                ]
            ]
        )

        st.markdown(
            interest_pills,
            unsafe_allow_html=True
        )

    if st.button(
        "Update My Profile",
        key="dashboard_edit_profile_v2"
    ):

        st.session_state.current_page = (
            "My Profile"
        )

        st.rerun()


# ============================================================
# STEM PATHWAY
# ============================================================

elif page == "My STEM Pathway":

    st.title(
        "My STEM Pathway"
    )

    st.write(
        "Answer the Career Explorer questions to discover "
        "STEM fields, majors, and careers that may fit you."
    )

    st.info(
        "These recommendations are designed to support exploration, "
        "not determine what you must study or become."
    )

    st.divider()

    st.header(
        "Discover Your STEM Direction"
    )

    preferred_work = st.selectbox(
        "Which type of work sounds most interesting?",
        [
            "Building physical machines or products",
            "Designing electronics and circuits",
            "Programming software",
            "Working with data and artificial intelligence",
            "Solving healthcare problems",
            "Conducting scientific research",
            "Working with mathematics and models",
            "Improving the environment",
            "Building robots and automated systems",
            "I am not sure yet"
        ]
    )

    favorite_activity = st.selectbox(
        "Which activity sounds most enjoyable?",
        [
            "Designing something in CAD",
            "Building a circuit",
            "Writing a program",
            "Analyzing a dataset",
            "Running an experiment",
            "Building a robot",
            "Solving difficult math problems",
            "Designing a healthcare device",
            "Studying the environment",
            "I am not sure yet"
        ]
    )

    programming_score = st.slider(
        "How much do you enjoy programming?",
        1,
        10,
        5
    )

    hands_on_score = st.slider(
        "How much do you enjoy building physical things?",
        1,
        10,
        5
    )

    math_score = st.slider(
        "How much do you enjoy mathematics?",
        1,
        10,
        5
    )

    electronics_score = st.slider(
        "How interested are you in electronics and circuits?",
        1,
        10,
        5
    )

    science_score = st.slider(
        "How interested are you in science and research?",
        1,
        10,
        5
    )

    data_score = st.slider(
        "How interested are you in data, statistics, or AI?",
        1,
        10,
        5
    )

    preferred_environment = st.selectbox(
        "Which environment sounds most appealing?",
        [
            "Technology company",
            "Engineering design company",
            "Engineering laboratory",
            "Research laboratory",
            "Hospital or healthcare technology",
            "Manufacturing company",
            "University or research institution",
            "Environmental organization",
            "I am not sure yet"
        ]
    )

    # ========================================================
    # CAREER DATABASE
    # ========================================================

    career_database = {

        "Engineering": {

            "majors": [
                "Engineering",
                "Industrial Engineering",
                "Civil Engineering",
                "Systems Engineering"
            ],

            "careers": [
                "Civil Engineer",
                "Industrial Engineer",
                "Systems Engineer",
                "Materials Engineer",
                "Aerospace Engineer"
            ]
        },

        "Electrical Engineering": {

            "majors": [
                "Electrical Engineering",
                "Electrical and Computer Engineering"
            ],

            "careers": [
                "Electrical Engineer",
                "Electronics Engineer",
                "Power Systems Engineer",
                "Controls Engineer",
                "RF Engineer",
                "Semiconductor Engineer",
                "Hardware Engineer"
            ]
        },

        "Mechanical Engineering": {

            "majors": [
                "Mechanical Engineering",
                "Aerospace Engineering",
                "Mechatronics"
            ],

            "careers": [
                "Mechanical Engineer",
                "Aerospace Engineer",
                "Automotive Engineer",
                "Manufacturing Engineer",
                "Product Design Engineer",
                "Mechatronics Engineer",
                "Robotics Engineer"
            ]
        },

        "Computer Engineering": {

            "majors": [
                "Computer Engineering",
                "Electrical and Computer Engineering"
            ],

            "careers": [
                "Computer Hardware Engineer",
                "Embedded Systems Engineer",
                "Firmware Engineer",
                "FPGA Engineer",
                "Hardware Engineer",
                "Robotics Engineer",
                "Systems Engineer"
            ]
        },

        "Computer Science": {

            "majors": [
                "Computer Science",
                "Software Engineering",
                "Cybersecurity"
            ],

            "careers": [
                "Software Developer",
                "Backend Developer",
                "Frontend Developer",
                "Full-Stack Developer",
                "Cybersecurity Analyst",
                "Cloud Engineer",
                "Database Architect",
                "Systems Developer"
            ]
        },

        "Artificial Intelligence": {

            "majors": [
                "Computer Science",
                "Artificial Intelligence",
                "Data Science"
            ],

            "careers": [
                "Machine Learning Engineer",
                "AI Engineer",
                "Data Scientist",
                "Computer Vision Engineer",
                "NLP Engineer",
                "AI Research Scientist",
                "Machine Learning Researcher"
            ]
        },

        "Data Science": {

            "majors": [
                "Data Science",
                "Statistics",
                "Computer Science",
                "Applied Mathematics"
            ],

            "careers": [
                "Data Scientist",
                "Data Analyst",
                "Data Engineer",
                "Operations Research Analyst",
                "Statistician",
                "Business Intelligence Analyst",
                "Quantitative Analyst"
            ]
        },

        "Biomedical Engineering": {

            "majors": [
                "Biomedical Engineering",
                "Bioengineering"
            ],

            "careers": [
                "Biomedical Engineer",
                "Medical Device Engineer",
                "Biomechanical Engineer",
                "Clinical Engineer",
                "Rehabilitation Engineer",
                "Healthcare Technology Engineer"
            ]
        },

        "Biology": {

            "majors": [
                "Biology",
                "Biochemistry",
                "Molecular Biology",
                "Biotechnology"
            ],

            "careers": [
                "Biologist",
                "Microbiologist",
                "Biochemist",
                "Biological Technician",
                "Geneticist",
                "Medical Scientist",
                "Biotechnology Researcher"
            ]
        },

        "Physics": {

            "majors": [
                "Physics",
                "Applied Physics",
                "Engineering Physics"
            ],

            "careers": [
                "Physicist",
                "Optical Engineer",
                "Nuclear Engineer",
                "Aerospace Engineer",
                "Research Scientist",
                "Medical Physicist"
            ]
        },

        "Mathematics": {

            "majors": [
                "Mathematics",
                "Applied Mathematics",
                "Statistics",
                "Actuarial Science"
            ],

            "careers": [
                "Mathematician",
                "Statistician",
                "Actuary",
                "Operations Research Analyst",
                "Data Scientist",
                "Quantitative Analyst"
            ]
        },

        "Environmental Science": {

            "majors": [
                "Environmental Science",
                "Environmental Engineering",
                "Earth Science"
            ],

            "careers": [
                "Environmental Scientist",
                "Environmental Engineer",
                "Hydrologist",
                "Conservation Scientist",
                "Environmental Consultant",
                "Climate Data Analyst"
            ]
        },

        "Robotics": {

            "majors": [
                "Robotics Engineering",
                "Mechanical Engineering",
                "Computer Engineering",
                "Electrical Engineering",
                "Mechatronics"
            ],

            "careers": [
                "Robotics Engineer",
                "Mechatronics Engineer",
                "Controls Engineer",
                "Automation Engineer",
                "Embedded Systems Engineer",
                "Computer Vision Engineer"
            ]
        }
    }

    # ========================================================
    # SCORING
    # ========================================================

    scores = {

        "Engineering": 0,
        "Electrical Engineering": 0,
        "Mechanical Engineering": 0,
        "Computer Engineering": 0,
        "Computer Science": 0,
        "Artificial Intelligence": 0,
        "Data Science": 0,
        "Biomedical Engineering": 0,
        "Biology": 0,
        "Physics": 0,
        "Mathematics": 0,
        "Environmental Science": 0,
        "Robotics": 0
    }

    for interest in profile["interests"]:

        if interest in scores:
            scores[interest] += 20

    scores["Computer Science"] += (
        programming_score * 2
    )

    scores["Computer Engineering"] += (
        programming_score * 1.5
    )

    scores["Artificial Intelligence"] += (
        programming_score * 2
    )

    scores["Data Science"] += (
        programming_score * 1.5
    )

    scores["Robotics"] += (
        programming_score
    )

    scores["Mechanical Engineering"] += (
        hands_on_score * 2
    )

    scores["Electrical Engineering"] += (
        hands_on_score
    )

    scores["Computer Engineering"] += (
        hands_on_score
    )

    scores["Robotics"] += (
        hands_on_score * 2
    )

    scores["Engineering"] += (
        hands_on_score
    )

    scores["Mathematics"] += (
        math_score * 2
    )

    scores["Physics"] += (
        math_score * 1.5
    )

    scores["Data Science"] += (
        math_score
    )

    scores["Artificial Intelligence"] += (
        math_score
    )

    scores["Electrical Engineering"] += (
        math_score
    )

    scores["Mechanical Engineering"] += (
        math_score
    )

    scores["Electrical Engineering"] += (
        electronics_score * 2
    )

    scores["Computer Engineering"] += (
        electronics_score * 2
    )

    scores["Robotics"] += (
        electronics_score * 1.5
    )

    scores["Biology"] += (
        science_score * 2
    )

    scores["Biomedical Engineering"] += (
        science_score * 1.5
    )

    scores["Physics"] += (
        science_score * 1.5
    )

    scores["Environmental Science"] += (
        science_score * 1.5
    )

    scores["Data Science"] += (
        data_score * 2
    )

    scores["Artificial Intelligence"] += (
        data_score * 2
    )

    scores["Computer Science"] += (
        data_score
    )

    scores["Mathematics"] += (
        data_score
    )

    work_mapping = {

        "Building physical machines or products":
            "Mechanical Engineering",

        "Designing electronics and circuits":
            "Electrical Engineering",

        "Programming software":
            "Computer Science",

        "Working with data and artificial intelligence":
            "Artificial Intelligence",

        "Solving healthcare problems":
            "Biomedical Engineering",

        "Conducting scientific research":
            "Biology",

        "Working with mathematics and models":
            "Mathematics",

        "Improving the environment":
            "Environmental Science",

        "Building robots and automated systems":
            "Robotics"
    }

    if preferred_work in work_mapping:

        scores[
            work_mapping[
                preferred_work
            ]
        ] += 25

    activity_mapping = {

        "Designing something in CAD":
            "Mechanical Engineering",

        "Building a circuit":
            "Electrical Engineering",

        "Writing a program":
            "Computer Science",

        "Analyzing a dataset":
            "Data Science",

        "Running an experiment":
            "Biology",

        "Building a robot":
            "Robotics",

        "Solving difficult math problems":
            "Mathematics",

        "Designing a healthcare device":
            "Biomedical Engineering",

        "Studying the environment":
            "Environmental Science"
    }

    if favorite_activity in activity_mapping:

        scores[
            activity_mapping[
                favorite_activity
            ]
        ] += 20

    environment_mapping = {

        "Technology company":
            "Computer Science",

        "Engineering design company":
            "Mechanical Engineering",

        "Engineering laboratory":
            "Electrical Engineering",

        "Research laboratory":
            "Physics",

        "Hospital or healthcare technology":
            "Biomedical Engineering",

        "Manufacturing company":
            "Mechanical Engineering",

        "University or research institution":
            "Biology",

        "Environmental organization":
            "Environmental Science"
    }

    if preferred_environment in environment_mapping:

        scores[
            environment_mapping[
                preferred_environment
            ]
        ] += 15

    # ========================================================
    # GENERATE RESULTS
    # ========================================================

    if st.button(
        "Generate My STEM Recommendations",
        type="primary",
        use_container_width=True
    ):

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        st.session_state.career_results = (
            ranked[:3]
        )

    if st.session_state.career_results:

        top_three = (
            st.session_state.career_results
        )

        max_score_value = (
            top_three[0][1]
        )

        st.divider()

        st.header(
            "Your STEM Direction"
        )

        for index, (
            field,
            score
        ) in enumerate(
            top_three,
            start=1
        ):

            percentage = round(
                (
                    score /
                    max_score_value
                ) * 100
            )

            major_info = (
                career_database[
                    field
                ]
            )

            with st.container(
                border=True
            ):

                st.subheader(
                    f"#{index} {field}"
                )

                st.metric(
                    "Exploration Match",
                    f"{percentage}%"
                )

                st.write(
                    "**Majors to explore:**"
                )

                for major in (
                    major_info["majors"]
                ):

                    st.write(
                        f"• {major}"
                    )

        top_field = (
            top_three[0][0]
        )

        top_info = (
            career_database[
                top_field
            ]
        )

        st.divider()

        st.header(
            "Recommended Major Direction"
        )

        st.subheader(
            top_info["majors"][0]
        )

        st.info(
            "This is a starting point for exploration, not a final decision."
        )

        st.divider()

        st.header(
            "Specific Careers to Explore"
        )

        career_columns = st.columns(2)

        for index, career_name in enumerate(
            top_info["careers"]
        ):

            with career_columns[
                index % 2
            ]:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        career_name
                    )

                    if careers.empty:

                        st.info(
                            "Career database unavailable."
                        )

                        continue

                    career_match = careers[
                        careers["career"]
                        .astype(str)
                        .str.lower()
                        == career_name.lower()
                    ]

                    if career_match.empty:

                        st.info(
                            "Detailed career data is being added."
                        )

                        continue

                    career_data = (
                        career_match.iloc[0]
                    )

                    st.caption(
                        f"Recommended major: "
                        f"{career_data['recommended_major']}"
                    )

                    st.write(
                        career_data[
                            "description"
                        ]
                    )

                    st.markdown(
                        "#### Salary & Career Pay"
                    )

                    salary_col1, salary_col2 = (
                        st.columns(2)
                    )

                    with salary_col1:

                        st.metric(
                            "Early-Career Benchmark",
                            format_salary(
                                career_data[
                                    "early_career_salary"
                                ]
                            )
                        )

                        st.caption(
                            "U.S. 25th percentile"
                        )

                    with salary_col2:

                        st.metric(
                            "Typical Salary",
                            format_salary(
                                career_data[
                                    "median_salary"
                                ]
                            )
                        )

                        st.caption(
                            "U.S. median"
                        )

                    salary_col3, salary_col4 = (
                        st.columns(2)
                    )

                    with salary_col3:

                        st.metric(
                            "Experienced Benchmark",
                            format_salary(
                                career_data[
                                    "experienced_salary"
                                ]
                            )
                        )

                        st.caption(
                            "U.S. 75th percentile"
                        )

                    with salary_col4:

                        st.metric(
                            "NYC / NY Average",
                            format_salary(
                                career_data[
                                    "average_salary"
                                ]
                            )
                        )

                        st.caption(
                            "Local mean annual wage"
                        )

                    st.markdown(
                        "#### Typical Education"
                    )

                    st.write(
                        career_data[
                            "education"
                        ]
                    )

                    st.markdown(
                        "#### Skills to Explore"
                    )

                    for skill in str(
                        career_data["skills"]
                    ).split(";"):

                        st.write(
                            f"• {skill.strip()}"
                        )

                    if (
                        "salary_mapping_note"
                        in career_data.index
                        and
                        pd.notna(
                            career_data[
                                "salary_mapping_note"
                            ]
                        )
                        and
                        str(
                            career_data[
                                "salary_mapping_note"
                            ]
                        ).strip()
                    ):

                        st.info(
                            career_data[
                                "salary_mapping_note"
                            ]
                        )

                    if (
                        "source_url"
                        in career_data.index
                        and
                        pd.notna(
                            career_data[
                                "source_url"
                            ]
                        )
                    ):

                        st.link_button(
                            "View Official BLS Source",
                            career_data[
                                "source_url"
                            ],
                            use_container_width=True
                        )

        st.divider()

        st.caption(
            "Salary benchmarks represent wage distributions, not "
            "guaranteed salaries after a specific number of years."
        )


# ============================================================
# OPPORTUNITIES
# ============================================================

elif page == "Opportunities":

    st.title(
        "Opportunities"
    )

    st.write(
        "Discover programs, internships, research, courses, "
        "competitions, and scholarships."
    )

    st.divider()

    if opportunities.empty:

        st.warning(
            "The opportunities database is currently unavailable."
        )

    else:

        opportunity_types = st.multiselect(
            "Filter by opportunity type",
            [
                "Summer Program",
                "Internship",
                "Research",
                "College Course",
                "Scholarship"
            ]
        )

        def is_eligible(
            opportunity
        ):

            eligible_grades = [
                item.strip()
                for item in str(
                    opportunity["grades"]
                ).split(";")
            ]

            boroughs_served = [
                item.strip()
                for item in str(
                    opportunity[
                        "boroughs_served"
                    ]
                ).split(";")
            ]

            return (
                profile["grade"]
                in eligible_grades
                and
                profile["borough"]
                in boroughs_served
            )

        def calculate_match(
            opportunity
        ):

            score = 0
            max_score = 0
            reasons = []

            fields = [
                item.strip()
                for item in str(
                    opportunity["fields"]
                ).split(";")
            ]

            boroughs_served = [
                item.strip()
                for item in str(
                    opportunity[
                        "boroughs_served"
                    ]
                ).split(";")
            ]

            max_score += 40

            if any(
                interest in fields
                for interest in profile[
                    "interests"
                ]
            ):

                score += 40

                reasons.append(
                    "Your STEM interests align with this opportunity."
                )

            max_score += 15

            if profile[
                "financial_support"
            ]:

                cost = str(
                    opportunity[
                        "cost"
                    ]
                ).lower()

                aid = str(
                    opportunity[
                        "financial_aid"
                    ]
                ).lower()

                if (
                    cost == "free"
                    or
                    aid == "available"
                ):

                    score += 15

                    reasons.append(
                        "This opportunity is free or offers financial support."
                    )

            else:

                score += 15

            max_score += 15

            if (
                profile["borough"]
                in boroughs_served
            ):

                score += 15

                reasons.append(
                    f"This opportunity serves students in the "
                    f"{profile['borough']}."
                )

            if (
                profile["borough"]
                == "Bronx"
            ):

                max_score += 10

                if str(
                    opportunity[
                        "bronx_priority"
                    ]
                ).lower() == "yes":

                    score += 10

                    reasons.append(
                        "This opportunity has a specific focus on Bronx students."
                    )

            return (
                round(
                    (
                        score /
                        max_score
                    ) * 100
                ),
                reasons
            )

        if (
            profile["borough"]
            == "Bronx"
        ):

            st.header(
                "Featured for Bronx Students"
            )

            featured = opportunities[
                opportunities[
                    "bronx_priority"
                ]
                .astype(str)
                .str.lower()
                == "yes"
            ]

            if featured.empty:

                st.info(
                    "More Bronx-focused opportunities will be added."
                )

            else:

                for _, opportunity in (
                    featured.head(3).iterrows()
                ):

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            opportunity[
                                "name"
                            ]
                        )

                        st.caption(
                            opportunity[
                                "organization"
                            ]
                        )

                        st.write(
                            opportunity[
                                "description"
                            ]
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write(
                                f"**Type:** "
                                f"{opportunity['opportunity_type']}"
                            )

                        with col2:

                            st.write(
                                f"**Cost:** "
                                f"{opportunity['cost']}"
                            )

                        st.link_button(
                            "View Opportunity",
                            opportunity[
                                "url"
                            ],
                            use_container_width=True
                        )

            st.divider()

        st.header(
            "Recommended for You"
        )

        if st.button(
            "Generate My Opportunity Matches",
            type="primary",
            use_container_width=True
        ):

            results = []

            for _, opportunity in (
                opportunities.iterrows()
            ):

                if not is_eligible(
                    opportunity
                ):
                    continue

                score, reasons = (
                    calculate_match(
                        opportunity
                    )
                )

                results.append(
                    (
                        score,
                        reasons,
                        opportunity
                    )
                )

            results.sort(
                key=lambda item: item[0],
                reverse=True
            )

            if not results:

                st.info(
                    "No eligible opportunities were found for your current profile."
                )

            for (
                score,
                reasons,
                opportunity
            ) in results:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        opportunity[
                            "name"
                        ]
                    )

                    st.caption(
                        opportunity[
                            "organization"
                        ]
                    )

                    st.metric(
                        "Match Score",
                        f"{score}%"
                    )

                    st.write(
                        opportunity[
                            "description"
                        ]
                    )

                    st.write(
                        f"**Fields:** "
                        f"{opportunity['fields']}"
                    )

                    st.write(
                        f"**Cost:** "
                        f"{opportunity['cost']}"
                    )

                    st.write(
                        f"**Application Status:** "
                        f"{opportunity['application_status']}"
                    )

                    with st.expander(
                        "Why this matches"
                    ):

                        for reason in reasons:

                            st.write(
                                f"• {reason}"
                            )

                    action_col1, action_col2 = st.columns(2)

                    with action_col1:

                        if st.button(
                            "📌 Save Opportunity",
                            key=f"save_recommended_{opportunity['name']}",
                            use_container_width=True
                        ):

                            if save_opportunity(
                                user_sub,
                                str(
                                    opportunity[
                                        "name"
                                    ]
                                )
                            ):

                                st.success(
                                    "Opportunity saved to My Applications."
                                )

                    with action_col2:

                        st.link_button(
                            "View Official Opportunity",
                            opportunity[
                                "url"
                            ],
                            use_container_width=True
                        )

        st.divider()

        st.header(
            "Browse All Opportunities"
        )

        for _, opportunity in (
            opportunities.iterrows()
        ):

            if (
                opportunity_types
                and
                str(
                    opportunity[
                        "opportunity_type"
                    ]
                )
                not in opportunity_types
            ):

                continue

            with st.expander(
                f"{opportunity['name']} — "
                f"{opportunity['organization']}"
            ):

                st.write(
                    opportunity[
                        "description"
                    ]
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Type:** "
                        f"{opportunity['opportunity_type']}"
                    )

                    st.write(
                        f"**Fields:** "
                        f"{opportunity['fields']}"
                    )

                    st.write(
                        f"**Grades:** "
                        f"{opportunity['grades']}"
                    )

                with col2:

                    st.write(
                        f"**Cost:** "
                        f"{opportunity['cost']}"
                    )

                    st.write(
                        f"**Financial Aid:** "
                        f"{opportunity['financial_aid']}"
                    )

                    st.write(
                        f"**Status:** "
                        f"{opportunity['application_status']}"
                    )

                browse_action1, browse_action2 = st.columns(2)

                with browse_action1:

                    if st.button(
                        "📌 Save Opportunity",
                        key=f"save_browse_{opportunity['name']}",
                        use_container_width=True
                    ):

                        if save_opportunity(
                            user_sub,
                            str(
                                opportunity[
                                    "name"
                                ]
                            )
                        ):

                            st.success(
                                "Opportunity saved to My Applications."
                            )

                with browse_action2:

                    st.link_button(
                        "View Official Opportunity",
                        opportunity[
                            "url"
                        ],
                        use_container_width=True
                    )


# ============================================================
# DEADLINE CALENDAR
# ============================================================

elif page == "Deadline Calendar":

    st.title(
        "Deadline Calendar"
    )

    st.write(
        "Track upcoming STEM program and application deadlines in one place."
    )

    st.info(
        "Dates come from the STEM Pathways NYC opportunities database. "
        "Always confirm the final deadline on the official program website before submitting."
    )

    st.divider()

    if opportunities.empty:

        st.warning(
            "The opportunities database is currently unavailable."
        )

    else:

        # ----------------------------------------------------
        # HELPERS
        # ----------------------------------------------------

        def parse_deadline_value(value):

            if value is None or pd.isna(value):
                return None

            raw = str(
                value
            ).strip()

            if not raw:
                return None

            lower = raw.lower()

            if any(
                phrase in lower
                for phrase in [
                    "not yet announced",
                    "future cycle",
                    "varies",
                    "typically",
                    "expected",
                    "check official",
                    "see official",
                    "closed"
                ]
            ):
                return None

            # Try direct parsing first.
            try:

                parsed = pd.to_datetime(
                    raw,
                    errors="coerce"
                )

                if pd.notna(
                    parsed
                ):

                    return parsed.to_pydatetime()

            except Exception:
                pass

            # Extract common date fragments from longer text.
            month_pattern = (
                r"(January|February|March|April|May|June|July|August|"
                r"September|October|November|December)\s+\d{1,2},\s+\d{4}"
            )

            match = re.search(
                month_pattern,
                raw,
                flags=re.IGNORECASE
            )

            if match:

                try:

                    parsed = pd.to_datetime(
                        match.group(0),
                        errors="coerce"
                    )

                    if pd.notna(
                        parsed
                    ):

                        return parsed.to_pydatetime()

                except Exception:
                    pass

            return None


        def deadline_status(
            deadline_dt,
            today_dt
        ):

            days_left = (
                deadline_dt.date()
                -
                today_dt.date()
            ).days

            if days_left < 0:
                return "Closed", days_left

            if days_left == 0:
                return "Due Today", days_left

            if days_left <= 7:
                return "Due Soon", days_left

            if days_left <= 30:
                return "This Month", days_left

            return "Upcoming", days_left


        def format_deadline_date(
            deadline_dt
        ):

            return deadline_dt.strftime(
                "%B %d, %Y"
            ).replace(
                " 0",
                " "
            )


        now_local = datetime.now(
            timezone.utc
        )

        # ----------------------------------------------------
        # SAVED APPLICATIONS
        # ----------------------------------------------------

        saved_items = load_saved_opportunities(
            user_sub
        )

        saved_names = {
            str(
                item.get(
                    "opportunity_name",
                    ""
                )
            )
            for item in saved_items
        }

        # ----------------------------------------------------
        # BUILD DEADLINE DATA
        # ----------------------------------------------------

        deadline_rows = []

        for _, opportunity in opportunities.iterrows():

            deadline_dt = parse_deadline_value(
                opportunity.get(
                    "deadline"
                )
            )

            if deadline_dt is None:
                continue

            # Make timezone-naive dates safe to compare.
            if deadline_dt.tzinfo is None:

                compare_deadline = deadline_dt.replace(
                    tzinfo=timezone.utc
                )

            else:

                compare_deadline = deadline_dt.astimezone(
                    timezone.utc
                )

            status, days_left = deadline_status(
                compare_deadline,
                now_local
            )

            deadline_rows.append(
                {
                    "name":
                        str(
                            opportunity.get(
                                "name",
                                "Opportunity"
                            )
                        ),

                    "organization":
                        str(
                            opportunity.get(
                                "organization",
                                ""
                            )
                        ),

                    "type":
                        str(
                            opportunity.get(
                                "opportunity_type",
                                ""
                            )
                        ),

                    "fields":
                        str(
                            opportunity.get(
                                "fields",
                                ""
                            )
                        ),

                    "deadline":
                        compare_deadline,

                    "deadline_text":
                        format_deadline_date(
                            compare_deadline
                        ),

                    "days_left":
                        days_left,

                    "status":
                        status,

                    "saved":
                        str(
                            opportunity.get(
                                "name",
                                ""
                            )
                        )
                        in saved_names,

                    "url":
                        str(
                            opportunity.get(
                                "url",
                                ""
                            )
                        ),

                    "cost":
                        str(
                            opportunity.get(
                                "cost",
                                ""
                            )
                        ),

                    "application_status":
                        str(
                            opportunity.get(
                                "application_status",
                                ""
                            )
                        )
                }
            )

        deadline_rows.sort(
            key=lambda item:
                item["deadline"]
        )

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        st.header(
            "Find Upcoming Deadlines"
        )

        filter_col1, filter_col2, filter_col3 = (
            st.columns(3)
        )

        with filter_col1:

            calendar_view = st.selectbox(
                "Show",
                [
                    "Upcoming deadlines",
                    "My saved opportunities",
                    "All dated opportunities",
                    "Past deadlines"
                ],
                key="deadline_calendar_view"
            )

        with filter_col2:

            type_options = sorted(
                {
                    item["type"]
                    for item in deadline_rows
                    if item["type"]
                }
            )

            selected_types = st.multiselect(
                "Opportunity type",
                type_options,
                key="deadline_calendar_types"
            )

        with filter_col3:

            field_filter = st.text_input(
                "Search field or keyword",
                placeholder="Engineering, AI, research...",
                key="deadline_calendar_search"
            )

        filtered_deadlines = []

        for item in deadline_rows:

            if (
                calendar_view
                ==
                "Upcoming deadlines"
                and
                item["days_left"] < 0
            ):
                continue

            if (
                calendar_view
                ==
                "My saved opportunities"
                and
                not item["saved"]
            ):
                continue

            if (
                calendar_view
                ==
                "Past deadlines"
                and
                item["days_left"] >= 0
            ):
                continue

            if (
                selected_types
                and
                item["type"]
                not in selected_types
            ):
                continue

            if field_filter.strip():

                search_text = (
                    item["name"]
                    +
                    " "
                    +
                    item["organization"]
                    +
                    " "
                    +
                    item["fields"]
                ).lower()

                if (
                    field_filter.strip().lower()
                    not in search_text
                ):
                    continue

            filtered_deadlines.append(
                item
            )

        # ----------------------------------------------------
        # SNAPSHOT
        # ----------------------------------------------------

        upcoming_only = [
            item
            for item in deadline_rows
            if item["days_left"] >= 0
        ]

        due_30 = [
            item
            for item in upcoming_only
            if item["days_left"] <= 30
        ]

        saved_upcoming = [
            item
            for item in upcoming_only
            if item["saved"]
        ]

        snapshot1, snapshot2, snapshot3, snapshot4 = (
            st.columns(4)
        )

        with snapshot1:

            st.metric(
                "Upcoming",
                len(
                    upcoming_only
                )
            )

        with snapshot2:

            st.metric(
                "Next 30 Days",
                len(
                    due_30
                )
            )

        with snapshot3:

            st.metric(
                "Saved With Deadlines",
                len(
                    saved_upcoming
                )
            )

        with snapshot4:

            if upcoming_only:

                st.metric(
                    "Next Deadline",
                    upcoming_only[0][
                        "deadline"
                    ].strftime(
                        "%b %d"
                    )
                )

            else:

                st.metric(
                    "Next Deadline",
                    "None listed"
                )

        st.divider()

        # ----------------------------------------------------
        # MONTHLY GROUPED CALENDAR
        # ----------------------------------------------------

        if not filtered_deadlines:

            st.info(
                "No deadlines match the filters you selected."
            )

        else:

            month_groups = {}

            for item in filtered_deadlines:

                month_key = (
                    item["deadline"].strftime(
                        "%Y-%m"
                    )
                )

                month_groups.setdefault(
                    month_key,
                    []
                ).append(
                    item
                )

            for month_key, month_items in month_groups.items():

                month_label = (
                    month_items[0][
                        "deadline"
                    ].strftime(
                        "%B %Y"
                    )
                )

                st.header(
                    month_label
                )

                for item in month_items:

                    with st.container(
                        border=True
                    ):

                        title_col, countdown_col = (
                            st.columns(
                                [4, 1]
                            )
                        )

                        with title_col:

                            saved_icon = (
                                "📌 "
                                if item["saved"]
                                else ""
                            )

                            st.subheader(
                                f"{saved_icon}{item['name']}"
                            )

                            st.caption(
                                f"{item['organization']} • {item['type']}"
                            )

                        with countdown_col:

                            if item["days_left"] < 0:

                                st.metric(
                                    "Status",
                                    "Closed"
                                )

                            elif item["days_left"] == 0:

                                st.metric(
                                    "Time Left",
                                    "Today"
                                )

                            elif item["days_left"] == 1:

                                st.metric(
                                    "Time Left",
                                    "1 day"
                                )

                            else:

                                st.metric(
                                    "Time Left",
                                    f"{item['days_left']} days"
                                )

                        details1, details2, details3 = (
                            st.columns(3)
                        )

                        with details1:

                            st.write(
                                f"**Deadline:** "
                                f"{item['deadline_text']}"
                            )

                        with details2:

                            st.write(
                                f"**Status:** "
                                f"{item['status']}"
                            )

                        with details3:

                            st.write(
                                f"**Cost:** "
                                f"{item['cost']}"
                            )

                        if item[
                            "application_status"
                        ]:

                            st.caption(
                                f"Program note: "
                                f"{item['application_status']}"
                            )

                        if item["fields"]:

                            st.write(
                                "**Fields:** "
                                +
                                item["fields"]
                            )

                        action1, action2 = (
                            st.columns(2)
                        )

                        with action1:

                            if not item["saved"]:

                                if st.button(
                                    "📌 Save to My Applications",
                                    key=f"calendar_save_{item['name']}",
                                    use_container_width=True
                                ):

                                    if save_opportunity(
                                        user_sub,
                                        item["name"]
                                    ):

                                        st.success(
                                            "Saved to My Applications."
                                        )

                                        st.rerun()

                            else:

                                st.success(
                                    "Saved in My Applications"
                                )

                        with action2:

                            if item["url"]:

                                st.link_button(
                                    "View Official Program",
                                    item["url"],
                                    use_container_width=True
                                )

                st.divider()

        # ----------------------------------------------------
        # UNDATED PROGRAMS
        # ----------------------------------------------------

        undated_count = len(
            opportunities
        ) - len(
            deadline_rows
        )

        if undated_count > 0:

            with st.expander(
                f"{undated_count} opportunities do not yet have a specific date"
            ):

                st.write(
                    "Some programs have future cycles, rolling dates, or deadlines "
                    "that have not yet been announced. They remain available on the "
                    "Opportunities page and should be checked on their official websites."
                )

        st.caption(
            "Deadline information may change. STEM Pathways NYC helps organize dates, "
            "but the official program website is always the final source."
        )





# ============================================================
# COLLEGE SUGGESTIONS
# ============================================================

elif page == "College Suggestions":

    st.title("College & Major Discovery")

    st.write(
        "Answer a few simple questions about what you enjoy. "
        "STEM Pathways NYC will suggest fields, majors, and colleges "
        "that may be worth exploring."
    )

    st.info(
        "Match score measures how well a college fits your interests and preferences. "
        "It is NOT your chance of admission."
    )

    st.divider()

    # --------------------------------------------------------
    # SIMPLE INTEREST QUESTIONS
    # --------------------------------------------------------

    st.header("1. Explore What You Might Like")

    q1 = st.multiselect(
        "What kinds of things sound interesting to you?",
        [
            "Building or fixing things",
            "Computers and technology",
            "Coding or making apps",
            "Robots and electronics",
            "Math and solving puzzles",
            "Science and experiments",
            "Medicine and the human body",
            "Nature, climate, and the environment",
            "Working with data and patterns",
            "Designing or creating new things",
            "I'm not sure yet"
        ],
        key="college_discovery_interests_v2"
    )

    q2 = st.selectbox(
        "Which school subject do you enjoy most?",
        [
            "I'm not sure",
            "Math",
            "Science",
            "Computer Science / Technology",
            "Biology",
            "Physics",
            "A mix of math and science"
        ],
        key="college_discovery_subject_v2"
    )

    q3 = st.selectbox(
        "What type of work sounds most enjoyable?",
        [
            "I'm not sure",
            "Building something with my hands",
            "Working on a computer",
            "Solving difficult problems",
            "Designing new products or systems",
            "Running experiments or doing research",
            "Helping people through science or technology",
            "Analyzing information and finding patterns"
        ],
        key="college_discovery_work_v2"
    )

    q4 = st.selectbox(
        "Would you rather work mostly with...",
        [
            "I'm not sure",
            "Hardware, machines, or physical objects",
            "Software and computers",
            "People and healthcare",
            "Numbers and data",
            "Science and research",
            "The environment",
            "A mix of hardware and software"
        ],
        key="college_discovery_environment_v2"
    )

    q5 = st.select_slider(
        "How much do you enjoy math?",
        options=[
            "Not much",
            "A little",
            "It's okay",
            "I like it",
            "I really like it"
        ],
        value="It's okay",
        key="college_discovery_math_v2"
    )

    # --------------------------------------------------------
    # OPTIONAL COLLEGE PREFERENCES
    # --------------------------------------------------------

    with st.expander("2. College Preferences (optional)"):

        college_location = st.selectbox(
            "Where would you be interested in going to college?",
            [
                "I'm open to anywhere",
                "NYC / close to home",
                "Northeast U.S.",
                "Anywhere in the U.S."
            ],
            key="college_discovery_location_v2"
        )

        college_setting = st.selectbox(
            "What kind of college environment sounds best?",
            [
                "I'm not sure",
                "City / urban",
                "Traditional college campus",
                "Small college",
                "Large university"
            ],
            key="college_discovery_setting_v2"
        )

        research_priority = st.checkbox(
            "Research opportunities are important to me",
            value=True,
            key="college_discovery_research_v2"
        )

        aid_priority = st.checkbox(
            "Financial aid / affordability is very important to me",
            value=bool(profile.get("financial_support", False)),
            key="college_discovery_aid_v2"
        )

    # --------------------------------------------------------
    # FIELD DISCOVERY SCORING
    # --------------------------------------------------------

    field_scores = {
        "Engineering": 0,
        "Electrical Engineering": 0,
        "Mechanical Engineering": 0,
        "Computer Engineering": 0,
        "Computer Science": 0,
        "Artificial Intelligence": 0,
        "Data Science": 0,
        "Biomedical Engineering": 0,
        "Biology": 0,
        "Physics": 0,
        "Mathematics": 0,
        "Environmental Science": 0,
        "Robotics": 0
    }

    def add_points(fields, points):
        for field in fields:
            if field in field_scores:
                field_scores[field] += points

    for answer in q1:
        if answer == "Building or fixing things":
            add_points(["Mechanical Engineering", "Engineering", "Robotics"], 5)
        elif answer == "Computers and technology":
            add_points(["Computer Science", "Computer Engineering", "Artificial Intelligence"], 5)
        elif answer == "Coding or making apps":
            add_points(["Computer Science", "Artificial Intelligence", "Data Science"], 6)
        elif answer == "Robots and electronics":
            add_points(["Robotics", "Electrical Engineering", "Computer Engineering"], 6)
        elif answer == "Math and solving puzzles":
            add_points(["Mathematics", "Physics", "Data Science", "Engineering"], 5)
        elif answer == "Science and experiments":
            add_points(["Biology", "Physics", "Biomedical Engineering", "Environmental Science"], 5)
        elif answer == "Medicine and the human body":
            add_points(["Biomedical Engineering", "Biology"], 6)
        elif answer == "Nature, climate, and the environment":
            add_points(["Environmental Science", "Biology"], 6)
        elif answer == "Working with data and patterns":
            add_points(["Data Science", "Artificial Intelligence", "Mathematics"], 6)
        elif answer == "Designing or creating new things":
            add_points(["Engineering", "Mechanical Engineering", "Robotics"], 5)

    subject_map = {
        "Math": ["Mathematics", "Data Science", "Engineering", "Physics"],
        "Science": ["Biology", "Physics", "Environmental Science", "Biomedical Engineering"],
        "Computer Science / Technology": ["Computer Science", "Computer Engineering", "Artificial Intelligence", "Robotics"],
        "Biology": ["Biology", "Biomedical Engineering", "Environmental Science"],
        "Physics": ["Physics", "Electrical Engineering", "Mechanical Engineering", "Engineering"],
        "A mix of math and science": ["Engineering", "Biomedical Engineering", "Physics", "Data Science"]
    }

    add_points(subject_map.get(q2, []), 4)

    work_map = {
        "Building something with my hands": ["Mechanical Engineering", "Robotics", "Engineering"],
        "Working on a computer": ["Computer Science", "Artificial Intelligence", "Data Science", "Computer Engineering"],
        "Solving difficult problems": ["Mathematics", "Physics", "Engineering", "Computer Science"],
        "Designing new products or systems": ["Mechanical Engineering", "Electrical Engineering", "Computer Engineering", "Engineering"],
        "Running experiments or doing research": ["Biology", "Physics", "Biomedical Engineering", "Environmental Science"],
        "Helping people through science or technology": ["Biomedical Engineering", "Biology", "Engineering"],
        "Analyzing information and finding patterns": ["Data Science", "Artificial Intelligence", "Mathematics"]
    }

    add_points(work_map.get(q3, []), 4)

    environment_map = {
        "Hardware, machines, or physical objects": ["Mechanical Engineering", "Electrical Engineering", "Robotics"],
        "Software and computers": ["Computer Science", "Artificial Intelligence", "Data Science"],
        "People and healthcare": ["Biomedical Engineering", "Biology"],
        "Numbers and data": ["Data Science", "Mathematics", "Artificial Intelligence"],
        "Science and research": ["Physics", "Biology", "Environmental Science"],
        "The environment": ["Environmental Science", "Biology"],
        "A mix of hardware and software": ["Computer Engineering", "Robotics", "Electrical Engineering"]
    }

    add_points(environment_map.get(q4, []), 4)

    math_points = {
        "Not much": 0,
        "A little": 1,
        "It's okay": 2,
        "I like it": 3,
        "I really like it": 4
    }[q5]

    add_points(
        [
            "Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Computer Engineering",
            "Computer Science",
            "Artificial Intelligence",
            "Data Science",
            "Physics",
            "Mathematics",
            "Robotics"
        ],
        math_points
    )

    # --------------------------------------------------------
    # COLLEGE DATABASE
    # --------------------------------------------------------

    college_catalog = [
        {
            "name": "MIT",
            "location": "Cambridge, MA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Physics", "Mathematics", "Robotics"
            ],
            "admit_rate": 4.5,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://ir.mit.edu/projects/2024-25-common-data-set/",
            "research": True
        },
        {
            "name": "Stanford University",
            "location": "Stanford, CA",
            "region": "West",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Data Science",
                "Biomedical Engineering", "Biology", "Physics", "Mathematics", "Robotics"
            ],
            "admit_rate": None,
            "rate_label": "See official Stanford CDS",
            "source_url": "https://irds.stanford.edu/data-findings/cds",
            "research": True
        },
        {
            "name": "Carnegie Mellon University",
            "location": "Pittsburgh, PA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Computer Engineering",
                "Computer Science", "Artificial Intelligence", "Data Science",
                "Mathematics", "Robotics"
            ],
            "admit_rate": 11.1,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.cmu.edu/ira/CDS/",
            "research": True
        },
        {
            "name": "UC Berkeley",
            "location": "Berkeley, CA",
            "region": "West",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Data Science",
                "Biomedical Engineering", "Biology", "Physics", "Mathematics",
                "Environmental Science"
            ],
            "admit_rate": 11.0,
            "rate_label": "2026 first-year overall",
            "source_url": "https://admissions.berkeley.edu/apply-to-berkeley/student-profile/",
            "research": True
        },
        {
            "name": "Georgia Tech",
            "location": "Atlanta, GA",
            "region": "South",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics", "Robotics"
            ],
            "admit_rate": 9.0,
            "rate_label": "2026 non-Georgia admit rate",
            "source_url": "https://admission.gatech.edu/",
            "research": True
        },
        {
            "name": "University of Michigan",
            "location": "Ann Arbor, MI",
            "region": "Midwest",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics",
                "Environmental Science", "Robotics"
            ],
            "admit_rate": 14.0,
            "rate_label": "Fall 2025 Michigan Engineering",
            "source_url": "https://www.engin.umich.edu/about/facts-figures/",
            "research": True
        },
        {
            "name": "Purdue University",
            "location": "West Lafayette, IN",
            "region": "Midwest",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics", "Robotics"
            ],
            "admit_rate": 34.7,
            "rate_label": "2025 College of Engineering",
            "source_url": "https://admissions.purdue.edu/become-student/class-profile/",
            "research": True
        },
        {
            "name": "Cornell University",
            "location": "Ithaca, NY",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science", "Robotics"
            ],
            "admit_rate": 7.9,
            "rate_label": "Fall 2023 overall",
            "source_url": "https://irp.cornell.edu/common-data-set",
            "research": True
        },
        {
            "name": "Columbia University",
            "location": "New York, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science"
            ],
            "admit_rate": 3.9,
            "rate_label": "Class of 2027 overall",
            "source_url": "https://undergrad.admissions.columbia.edu/",
            "research": True
        },
        {
            "name": "Princeton University",
            "location": "Princeton, NJ",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Small",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Physics",
                "Mathematics", "Biology", "Environmental Science"
            ],
            "admit_rate": 4.4,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://profile.princeton.edu/admission-and-costs",
            "research": True
        },
        {
            "name": "Harvard University",
            "location": "Cambridge, MA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science"
            ],
            "admit_rate": 4.2,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://college.harvard.edu/admissions/admissions-statistics",
            "research": True
        },
        {
            "name": "Duke University",
            "location": "Durham, NC",
            "region": "South",
            "setting": "Traditional college campus",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Data Science",
                "Biomedical Engineering", "Biology", "Mathematics"
            ],
            "admit_rate": 5.2,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://admissions.duke.edu/",
            "research": True
        },
        {
            "name": "Johns Hopkins University",
            "location": "Baltimore, MD",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science"
            ],
            "admit_rate": 4.2,
            "rate_label": "Class of 2029 Regular Decision",
            "source_url": "https://apply.jhu.edu/",
            "research": True
        },
        {
            "name": "Caltech",
            "location": "Pasadena, CA",
            "region": "West",
            "setting": "Small college",
            "size": "Small",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Physics",
                "Mathematics", "Biology"
            ],
            "admit_rate": 3.1,
            "rate_label": "Fall 2023 overall",
            "source_url": "https://iro.caltech.edu/",
            "research": True
        },
        {
            "name": "The Cooper Union",
            "location": "New York, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Small",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering"
            ],
            "admit_rate": 23.0,
            "rate_label": "2024-25 School of Engineering",
            "source_url": "https://cooper.edu/admissions/faq",
            "research": True
        },
        {
            "name": "NYU Tandon",
            "location": "Brooklyn, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Robotics"
            ],
            "admit_rate": 13.0,
            "rate_label": "NYU university-wide",
            "source_url": "https://bulletins.nyu.edu/nyu/enrollment-graduation-statistics/",
            "research": True
        },
        {
            "name": "Stevens Institute of Technology",
            "location": "Hoboken, NJ",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics",
                "Robotics"
            ],
            "admit_rate": 51.0,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.stevens.edu/discover-stevens/stevens-by-the-numbers/facts-statistics",
            "research": True
        },
        {
            "name": "CCNY",
            "location": "New York, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Biomedical Engineering",
                "Biology", "Physics", "Mathematics", "Environmental Science"
            ],
            "admit_rate": None,
            "rate_label": "See official CCNY admissions data",
            "source_url": "https://www.ccny.cuny.edu/admissions",
            "research": True
        },
        {
            "name": "Stony Brook University",
            "location": "Stony Brook, NY",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science"
            ],
            "admit_rate": None,
            "rate_label": "See official Stony Brook admissions data",
            "source_url": "https://www.stonybrook.edu/undergraduate-admissions/",
            "research": True
        }
    ]

    # --------------------------------------------------------
    # COMPETITIVENESS
    # --------------------------------------------------------

    def competitiveness_from_rate(rate):
        if rate is None:
            return None, "Not rated"

        if rate < 7:
            return 5, "Extremely Competitive"
        elif rate < 15:
            return 4, "Highly Competitive"
        elif rate < 30:
            return 3, "Competitive"
        elif rate < 50:
            return 2, "Moderately Competitive"
        else:
            return 1, "More Accessible"

    # --------------------------------------------------------
    # PERSONALIZED COLLEGE MATCH
    # --------------------------------------------------------

    def college_match_score(college, top_fields):

        score = 0
        max_score = 100
        reasons = []

        # Field fit: up to 50 points
        field_points = 0

        for rank, (field, field_score) in enumerate(top_fields, start=1):
            if field in college["fields"]:
                bonus = max(22 - ((rank - 1) * 5), 7)
                field_points += bonus

        field_points = min(field_points, 50)
        score += field_points

        if field_points >= 35:
            reasons.append("Very strong match with your top STEM interests.")
        elif field_points >= 20:
            reasons.append("Good match with several of your STEM interests.")

        # Location fit: up to 20 points
        if college_location == "NYC / close to home":
            if college["location"] in ["New York, NY", "Brooklyn, NY", "Hoboken, NJ"]:
                score += 20
                reasons.append("Matches your preference to stay in or near NYC.")
            elif college["region"] == "Northeast":
                score += 10

        elif college_location == "Northeast U.S.":
            if college["region"] == "Northeast":
                score += 20
                reasons.append("Matches your Northeast location preference.")

        elif college_location in ["I'm open to anywhere", "Anywhere in the U.S."]:
            score += 12

        # Campus setting: up to 15 points
        if college_setting == "I'm not sure":
            score += 8
        elif college_setting == college["setting"]:
            score += 15
            reasons.append("Matches the type of college environment you selected.")
        elif (
            college_setting == "Large university"
            and college["size"] == "Large"
        ):
            score += 15
        elif (
            college_setting == "Small college"
            and college["size"] == "Small"
        ):
            score += 15
        else:
            score += 4

        # Research: up to 10 points
        if research_priority:
            if college.get("research"):
                score += 10
                reasons.append("Offers a strong research-oriented environment.")
        else:
            score += 5

        # Affordability preference: 5 points for local public-ish option,
        # otherwise do not pretend to know individualized net price.
        if aid_priority:
            if college["name"] in ["CCNY", "Stony Brook University"]:
                score += 5
                reasons.append("May be worth exploring as a lower-cost public option.")
        else:
            score += 5

        return min(round(score), max_score), reasons

    if st.button(
        "Discover My Best-Fit Colleges",
        type="primary",
        use_container_width=True
    ):

        ranked_fields = sorted(
            field_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_fields = ranked_fields[:4]

        results = []

        for college in college_catalog:
            match_score, reasons = college_match_score(
                college,
                top_fields
            )

            stars, competitive_label = competitiveness_from_rate(
                college["admit_rate"]
            )

            results.append({
                "college": college,
                "match_score": match_score,
                "reasons": reasons,
                "stars": stars,
                "competitive_label": competitive_label
            })

        results.sort(
            key=lambda item: item["match_score"],
            reverse=True
        )

        st.session_state["college_discovery_results_v3"] = top_fields
        st.session_state["college_match_results_v3"] = results
        st.rerun()

    discovery_results = st.session_state.get(
        "college_discovery_results_v3"
    )

    college_results = st.session_state.get(
        "college_match_results_v3"
    )

    if discovery_results and college_results:

        st.divider()

        st.header("Your Top STEM Directions")

        top_field_score = max(
            discovery_results[0][1],
            1
        )

        field_columns = st.columns(4)

        for index, (field, score) in enumerate(discovery_results):

            with field_columns[index]:

                with st.container(border=True):

                    st.subheader(
                        f"#{index + 1}"
                    )

                    st.write(
                        f"**{field}**"
                    )

                    relative = round(
                        (score / top_field_score) * 100
                    )

                    st.metric(
                        "Interest Match",
                        f"{relative}%"
                    )

        st.divider()

        st.header("Best College Matches")

        st.write(
            "Schools are ordered by your personalized **match score**, "
            "not by prestige or acceptance rate."
        )

        for rank, result in enumerate(
            college_results[:15],
            start=1
        ):

            college = result["college"]
            match_score = result["match_score"]
            reasons = result["reasons"]
            stars = result["stars"]
            competitive_label = result["competitive_label"]

            with st.container(border=True):

                title_col, match_col = st.columns(
                    [3, 1]
                )

                with title_col:

                    st.subheader(
                        f"{rank}. {college['name']}"
                    )

                    st.caption(
                        f"{college['location']} • {college['setting']} • {college['size']}"
                    )

                with match_col:

                    st.metric(
                        "Your Match",
                        f"{match_score}%"
                    )

                info1, info2, info3 = st.columns(3)

                with info1:

                    if college["admit_rate"] is not None:

                        st.metric(
                            "Recent Admit Rate",
                            f"{college['admit_rate']:.1f}%"
                        )

                    else:

                        st.metric(
                            "Recent Admit Rate",
                            "See source"
                        )

                    st.caption(
                        college["rate_label"]
                    )

                with info2:

                    if stars is not None:

                        star_display = (
                            "★" * stars
                            +
                            "☆" * (5 - stars)
                        )

                        st.metric(
                            "Competition",
                            star_display
                        )

                        st.caption(
                            competitive_label
                        )

                    else:

                        st.metric(
                            "Competition",
                            "Not rated"
                        )

                with info3:

                    matching_fields = [
                        field
                        for field, _
                        in discovery_results
                        if field in college["fields"]
                    ]

                    st.write(
                        "**Matching fields**"
                    )

                    if matching_fields:
                        st.write(
                            " • ".join(
                                matching_fields[:4]
                            )
                        )
                    else:
                        st.write(
                            "General STEM option"
                        )

                with st.expander(
                    "Why this school matches you"
                ):

                    if reasons:
                        for reason in reasons:
                            st.write(
                                f"• {reason}"
                            )
                    else:
                        st.write(
                            "This school is included as a STEM option "
                            "but has fewer direct matches with your current answers."
                        )

                favorite_action1, favorite_action2 = st.columns(2)

                with favorite_action1:

                    if st.button(
                        "💾 Save College",
                        key=f"favorite_college_{college['name']}",
                        use_container_width=True
                    ):

                        if add_favorite_college(
                            user_sub,
                            college["name"]
                        ):

                            st.success(
                                "College saved to My Favorite Colleges."
                            )

                with favorite_action2:

                    st.link_button(
                        "View Admissions / Data Source",
                        college["source_url"],
                        use_container_width=True
                    )

        st.divider()

        st.caption(
            "Important: admit rates are recent institution- or school-level figures "
            "where official data was available. Some colleges admit by school or residency, "
            "so a single percentage may not describe every applicant. Competitiveness stars "
            "are a STEM Pathways NYC category based on the displayed admit rate. "
            "Match score reflects your interests and preferences only — it is not an admission chance."
        )


# ============================================================
# MY FAVORITE COLLEGES
# ============================================================

elif page == "My Favorite Colleges":

    st.title(
        "My Favorite Colleges"
    )

    st.write(
        "Build your own college list, keep the schools you like, "
        "and arrange them in your personal order."
    )

    st.info(
        "Your favorite order is based on your personal preferences. "
        "The competitiveness rating and admission data are informational "
        "and do not predict your individual chance of admission."
    )

    st.divider()

    # --------------------------------------------------------
    # COLLEGE DETAILS USED IN FAVORITES
    # --------------------------------------------------------

    favorite_college_catalog = {
        "MIT": {
            "location": "Cambridge, MA",
            "admit_rate": 4.5,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://ir.mit.edu/projects/2024-25-common-data-set/"
        },
        "Stanford University": {
            "location": "Stanford, CA",
            "admit_rate": None,
            "rate_label": "See official Stanford CDS",
            "source_url": "https://irds.stanford.edu/data-findings/cds"
        },
        "Carnegie Mellon University": {
            "location": "Pittsburgh, PA",
            "admit_rate": 11.1,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.cmu.edu/ira/CDS/"
        },
        "UC Berkeley": {
            "location": "Berkeley, CA",
            "admit_rate": 11.0,
            "rate_label": "2026 first-year overall",
            "source_url": "https://admissions.berkeley.edu/apply-to-berkeley/student-profile/"
        },
        "Georgia Tech": {
            "location": "Atlanta, GA",
            "admit_rate": 9.0,
            "rate_label": "2026 non-Georgia admit rate",
            "source_url": "https://admission.gatech.edu/"
        },
        "University of Michigan": {
            "location": "Ann Arbor, MI",
            "admit_rate": 14.0,
            "rate_label": "Fall 2025 Michigan Engineering",
            "source_url": "https://www.engin.umich.edu/about/facts-figures/"
        },
        "Purdue University": {
            "location": "West Lafayette, IN",
            "admit_rate": 34.7,
            "rate_label": "2025 College of Engineering",
            "source_url": "https://admissions.purdue.edu/become-student/class-profile/"
        },
        "Cornell University": {
            "location": "Ithaca, NY",
            "admit_rate": 7.9,
            "rate_label": "Fall 2023 overall",
            "source_url": "https://irp.cornell.edu/common-data-set"
        },
        "Columbia University": {
            "location": "New York, NY",
            "admit_rate": 3.9,
            "rate_label": "Class of 2027 overall",
            "source_url": "https://undergrad.admissions.columbia.edu/"
        },
        "Princeton University": {
            "location": "Princeton, NJ",
            "admit_rate": 4.4,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://profile.princeton.edu/admission-and-costs"
        },
        "Harvard University": {
            "location": "Cambridge, MA",
            "admit_rate": 4.2,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://college.harvard.edu/admissions/admissions-statistics"
        },
        "Duke University": {
            "location": "Durham, NC",
            "admit_rate": 5.2,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://admissions.duke.edu/"
        },
        "Johns Hopkins University": {
            "location": "Baltimore, MD",
            "admit_rate": 4.2,
            "rate_label": "Class of 2029 Regular Decision",
            "source_url": "https://apply.jhu.edu/"
        },
        "Caltech": {
            "location": "Pasadena, CA",
            "admit_rate": 3.1,
            "rate_label": "Fall 2023 overall",
            "source_url": "https://iro.caltech.edu/"
        },
        "The Cooper Union": {
            "location": "New York, NY",
            "admit_rate": 23.0,
            "rate_label": "2024-25 School of Engineering",
            "source_url": "https://cooper.edu/admissions/faq"
        },
        "NYU Tandon": {
            "location": "Brooklyn, NY",
            "admit_rate": 13.0,
            "rate_label": "NYU university-wide",
            "source_url": "https://bulletins.nyu.edu/nyu/enrollment-graduation-statistics/"
        },
        "Stevens Institute of Technology": {
            "location": "Hoboken, NJ",
            "admit_rate": 51.0,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.stevens.edu/discover-stevens/stevens-by-the-numbers/facts-statistics"
        },
        "CCNY": {
            "location": "New York, NY",
            "admit_rate": None,
            "rate_label": "See official CCNY admissions data",
            "source_url": "https://www.ccny.cuny.edu/admissions"
        },
        "Stony Brook University": {
            "location": "Stony Brook, NY",
            "admit_rate": None,
            "rate_label": "See official Stony Brook admissions data",
            "source_url": "https://www.stonybrook.edu/undergraduate-admissions/"
        }
    }

    def favorite_competitiveness(rate):

        if rate is None:
            return None, "Not rated"

        if rate < 7:
            return 5, "Extremely Competitive"
        elif rate < 15:
            return 4, "Highly Competitive"
        elif rate < 30:
            return 3, "Competitive"
        elif rate < 50:
            return 2, "Moderately Competitive"
        else:
            return 1, "More Accessible"

    # Recover the most recent personalized college matches from this session.
    last_match_lookup = {}

    for result in st.session_state.get(
        "college_match_results_v3",
        []
    ):

        college_info = result.get(
            "college",
            {}
        )

        college_name = college_info.get(
            "name"
        )

        if college_name:

            last_match_lookup[
                college_name
            ] = result.get(
                "match_score"
            )

    favorite_colleges = load_favorite_colleges(
        user_sub
    )

    if not favorite_colleges:

        st.header(
            "Your favorites list is empty"
        )

        st.write(
            "Go to **College Suggestions** and click "
            "**💾 Save College** on schools you want to remember."
        )

        if st.button(
            "Explore College Suggestions",
            type="primary",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "College Suggestions"
            )

            st.rerun()

    else:

        st.header(
            "Your Ranked College List"
        )

        st.caption(
            "Use the arrows to move schools up or down. "
            "#1 is currently your favorite."
        )

        for index, favorite in enumerate(
            favorite_colleges,
            start=1
        ):

            favorite_id = favorite[
                "id"
            ]

            college_name = favorite[
                "college_name"
            ]

            college_info = (
                favorite_college_catalog.get(
                    college_name,
                    {}
                )
            )

            admit_rate = (
                college_info.get(
                    "admit_rate"
                )
            )

            stars, competition_label = (
                favorite_competitiveness(
                    admit_rate
                )
            )

            personal_match = (
                last_match_lookup.get(
                    college_name
                )
            )

            with st.container(
                border=True
            ):

                title_col, rank_col = (
                    st.columns(
                        [4, 1]
                    )
                )

                with title_col:

                    st.subheader(
                        college_name
                    )

                    if college_info.get(
                        "location"
                    ):

                        st.caption(
                            college_info[
                                "location"
                            ]
                        )

                with rank_col:

                    st.metric(
                        "Your Rank",
                        f"#{index}"
                    )

                stat1, stat2, stat3 = (
                    st.columns(3)
                )

                with stat1:

                    if admit_rate is not None:

                        st.metric(
                            "Recent Admit Rate",
                            f"{admit_rate:.1f}%"
                        )

                    else:

                        st.metric(
                            "Recent Admit Rate",
                            "See source"
                        )

                    if college_info.get(
                        "rate_label"
                    ):

                        st.caption(
                            college_info[
                                "rate_label"
                            ]
                        )

                with stat2:

                    if stars is not None:

                        star_display = (
                            "★" * stars
                            +
                            "☆" * (
                                5 - stars
                            )
                        )

                        st.metric(
                            "Competition",
                            star_display
                        )

                        st.caption(
                            competition_label
                        )

                    else:

                        st.metric(
                            "Competition",
                            "Not rated"
                        )

                with stat3:

                    if personal_match is not None:

                        st.metric(
                            "Your Last Match",
                            f"{personal_match}%"
                        )

                        st.caption(
                            "Fit score, not admission chance"
                        )

                    else:

                        st.metric(
                            "Your Last Match",
                            "Run discovery"
                        )

                        st.caption(
                            "Use College Suggestions to calculate your fit"
                        )

                notes_value = st.text_area(
                    "Why do you like this school? (optional)",
                    value=(
                        favorite.get(
                            "notes",
                            ""
                        )
                        or
                        ""
                    ),
                    placeholder=(
                        "Example: Strong Computer Engineering, "
                        "close to NYC, research opportunities..."
                    ),
                    key=f"favorite_college_notes_{favorite_id}"
                )

                move_col1, move_col2, save_col, remove_col = (
                    st.columns(4)
                )

                with move_col1:

                    if st.button(
                        "⬆️ Move Up",
                        key=f"favorite_up_{favorite_id}",
                        disabled=(
                            index == 1
                        ),
                        use_container_width=True
                    ):

                        if reorder_favorite_colleges(
                            user_sub,
                            favorite_id,
                            "up"
                        ):

                            st.rerun()

                with move_col2:

                    if st.button(
                        "⬇️ Move Down",
                        key=f"favorite_down_{favorite_id}",
                        disabled=(
                            index
                            ==
                            len(
                                favorite_colleges
                            )
                        ),
                        use_container_width=True
                    ):

                        if reorder_favorite_colleges(
                            user_sub,
                            favorite_id,
                            "down"
                        ):

                            st.rerun()

                with save_col:

                    if st.button(
                        "💾 Save Notes",
                        key=f"favorite_save_notes_{favorite_id}",
                        use_container_width=True
                    ):

                        if update_favorite_college_notes(
                            favorite_id,
                            notes_value
                        ):

                            st.success(
                                "Notes saved."
                            )

                with remove_col:

                    if st.button(
                        "Remove",
                        key=f"favorite_remove_{favorite_id}",
                        use_container_width=True
                    ):

                        st.session_state[
                            "confirm_remove_favorite_college"
                        ] = favorite_id

                if college_info.get(
                    "source_url"
                ):

                    st.link_button(
                        "View Admissions / Data Source",
                        college_info[
                            "source_url"
                        ],
                        use_container_width=True
                    )

                if (
                    st.session_state.get(
                        "confirm_remove_favorite_college"
                    )
                    ==
                    favorite_id
                ):

                    st.warning(
                        f"Remove {college_name} from your favorites?"
                    )

                    confirm_col1, confirm_col2 = (
                        st.columns(2)
                    )

                    with confirm_col1:

                        if st.button(
                            "Yes, Remove",
                            key=f"favorite_confirm_remove_{favorite_id}",
                            use_container_width=True
                        ):

                            if remove_favorite_college(
                                user_sub,
                                favorite_id
                            ):

                                st.session_state.pop(
                                    "confirm_remove_favorite_college",
                                    None
                                )

                                st.rerun()

                    with confirm_col2:

                        if st.button(
                            "Cancel",
                            key=f"favorite_cancel_remove_{favorite_id}",
                            use_container_width=True
                        ):

                            st.session_state.pop(
                                "confirm_remove_favorite_college",
                                None
                            )

                            st.rerun()

        st.divider()

        st.caption(
            "Tip: Your favorites can change as you learn more. "
            "Move schools whenever your priorities change. "
            "Admission rates and competitiveness categories are informational only."
        )


# ============================================================
# MY APPLICATIONS
# ============================================================

elif page == "My Applications":

    st.title(
        "My Applications"
    )

    st.write(
        "Save opportunities you are interested in and track your "
        "progress from discovery through the application process."
    )

    st.info(
        "Your tracker is private to your signed-in account. "
        "Saving an opportunity does not submit an application."
    )

    st.divider()

    saved_items = load_saved_opportunities(
        user_sub
    )

    if not saved_items:

        st.header(
            "No saved opportunities yet"
        )

        st.write(
            "Go to the Opportunities page and select "
            "**Save Opportunity** on any program you want to track."
        )

        if st.button(
            "Explore Opportunities",
            type="primary",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "Opportunities"
            )

            st.rerun()

    else:

        # ----------------------------------------------------
        # APPLICATION SNAPSHOT
        # ----------------------------------------------------

        st.header(
            "Application Snapshot"
        )

        total_saved = len(
            saved_items
        )

        applied_count = sum(
            1
            for item in saved_items
            if item.get("status")
            in [
                "Applied",
                "Accepted",
                "Waitlisted",
                "Not Selected"
            ]
        )

        accepted_count = sum(
            1
            for item in saved_items
            if item.get("status")
            == "Accepted"
        )

        planning_count = sum(
            1
            for item in saved_items
            if item.get("status")
            in [
                "Planning to Apply",
                "Applying"
            ]
        )

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )

        with metric1:

            st.metric(
                "Saved",
                total_saved
            )

        with metric2:

            st.metric(
                "Planning / Applying",
                planning_count
            )

        with metric3:

            st.metric(
                "Submitted",
                applied_count
            )

        with metric4:

            st.metric(
                "Accepted",
                accepted_count
            )

        st.divider()

        # ----------------------------------------------------
        # STATUS FILTER
        # ----------------------------------------------------

        filter_status = st.multiselect(
            "Filter by application status",
            APPLICATION_STATUSES,
            default=[]
        )

        filtered_items = [
            item
            for item in saved_items
            if (
                not filter_status
                or
                item.get(
                    "status",
                    "Saved"
                )
                in filter_status
            )
        ]

        for saved_item in filtered_items:

            saved_name = str(
                saved_item.get(
                    "opportunity_name",
                    "Saved Opportunity"
                )
            )

            current_status = (
                saved_item.get(
                    "status",
                    "Saved"
                )
                or
                "Saved"
            )

            current_notes = (
                saved_item.get(
                    "notes",
                    ""
                )
                or
                ""
            )

            opportunity_match = (
                opportunities[
                    opportunities[
                        "name"
                    ]
                    .astype(str)
                    == saved_name
                ]
                if (
                    not opportunities.empty
                    and
                    "name"
                    in opportunities.columns
                )
                else pd.DataFrame()
            )

            with st.container(
                border=True
            ):

                st.subheader(
                    saved_name
                )

                if not opportunity_match.empty:

                    opportunity_data = (
                        opportunity_match.iloc[0]
                    )

                    st.caption(
                        str(
                            opportunity_data.get(
                                "organization",
                                ""
                            )
                        )
                    )

                    top1, top2, top3 = (
                        st.columns(3)
                    )

                    with top1:

                        st.write(
                            f"**Type:** "
                            f"{opportunity_data.get('opportunity_type', 'Not listed')}"
                        )

                    with top2:

                        st.write(
                            f"**Cost:** "
                            f"{opportunity_data.get('cost', 'Not listed')}"
                        )

                    with top3:

                        if (
                            "selectivity"
                            in opportunity_data.index
                            and
                            pd.notna(
                                opportunity_data[
                                    "selectivity"
                                ]
                            )
                        ):

                            try:

                                stars = (
                                    "★"
                                    * int(
                                        opportunity_data[
                                            "selectivity"
                                        ]
                                    )
                                    +
                                    "☆"
                                    * (
                                        5
                                        -
                                        int(
                                            opportunity_data[
                                                "selectivity"
                                            ]
                                        )
                                    )
                                )

                                st.write(
                                    f"**Selectivity:** {stars}"
                                )

                            except Exception:

                                pass

                    if (
                        "deadline"
                        in opportunity_data.index
                        and
                        pd.notna(
                            opportunity_data[
                                "deadline"
                            ]
                        )
                    ):

                        st.write(
                            f"**Deadline:** "
                            f"{opportunity_data['deadline']}"
                        )

                    if (
                        "application_status"
                        in opportunity_data.index
                        and
                        pd.notna(
                            opportunity_data[
                                "application_status"
                            ]
                        )
                    ):

                        st.write(
                            f"**Program status:** "
                            f"{opportunity_data['application_status']}"
                        )

                st.divider()

                status_col, notes_col = (
                    st.columns(
                        [1, 2]
                    )
                )

                with status_col:

                    selected_status = st.selectbox(
                        "Application Status",
                        APPLICATION_STATUSES,
                        index=(
                            APPLICATION_STATUSES.index(
                                current_status
                            )
                            if current_status
                            in APPLICATION_STATUSES
                            else 0
                        ),
                        key=f"application_status_{saved_item['id']}"
                    )

                with notes_col:

                    selected_notes = st.text_area(
                        "Notes",
                        value=current_notes,
                        placeholder=(
                            "Example: Ask teacher for recommendation, "
                            "finish essay, request transcript..."
                        ),
                        key=f"application_notes_{saved_item['id']}"
                    )

                action1, action2, action3 = (
                    st.columns(
                        [1, 1, 1]
                    )
                )

                with action1:

                    if st.button(
                        "Save Changes",
                        key=f"save_tracker_{saved_item['id']}",
                        type="primary",
                        use_container_width=True
                    ):

                        if update_saved_opportunity(
                            saved_item["id"],
                            selected_status,
                            selected_notes
                        ):

                            st.success(
                                "Application tracker updated."
                            )

                            st.rerun()

                with action2:

                    if not opportunity_match.empty:

                        opportunity_url = (
                            opportunity_match.iloc[0].get(
                                "url"
                            )
                        )

                        if (
                            pd.notna(
                                opportunity_url
                            )
                            and
                            str(
                                opportunity_url
                            ).strip()
                        ):

                            st.link_button(
                                "Official Website",
                                str(
                                    opportunity_url
                                ),
                                use_container_width=True
                            )

                with action3:

                    if st.button(
                        "Remove",
                        key=f"remove_tracker_{saved_item['id']}",
                        use_container_width=True
                    ):

                        st.session_state[
                            "confirm_remove_saved_id"
                        ] = saved_item[
                            "id"
                        ]

                if (
                    st.session_state.get(
                        "confirm_remove_saved_id"
                    )
                    ==
                    saved_item[
                        "id"
                    ]
                ):

                    st.warning(
                        "Remove this opportunity from My Applications?"
                    )

                    confirm1, confirm2 = (
                        st.columns(2)
                    )

                    with confirm1:

                        if st.button(
                            "Yes, Remove",
                            key=f"confirm_remove_{saved_item['id']}",
                            use_container_width=True
                        ):

                            if delete_saved_opportunity(
                                saved_item["id"]
                            ):

                                st.session_state.pop(
                                    "confirm_remove_saved_id",
                                    None
                                )

                                st.rerun()

                    with confirm2:

                        if st.button(
                            "Cancel",
                            key=f"cancel_remove_{saved_item['id']}",
                            use_container_width=True
                        ):

                            st.session_state.pop(
                                "confirm_remove_saved_id",
                                None
                            )

                            st.rerun()





# ============================================================
# PROJECTS
# ============================================================

elif page == "Projects":

    st.title("Project Explorer")

    st.write(
        "Not sure what to build? Tell us what sounds interesting and "
        "we'll suggest hands-on STEM projects that match what you want to create."
    )

    st.divider()

    # --------------------------------------------------------
    # PROJECT DATABASE
    # --------------------------------------------------------

    project_catalog = [
        {
            "title": "Smart Room Lighting System",
            "fields": ["Electrical Engineering", "Computer Engineering", "Robotics"],
            "create": ["A physical device", "Something that makes everyday life easier", "Something with lights or electronics"],
            "level": "Beginner",
            "time": "1–2 weeks",
            "hours": "5–10 hours",
            "style": ["Building with my hands", "Coding", "Testing and experimenting"],
            "equipment": ["Computer", "Arduino / microcontroller", "Breadboard / basic electronics"],
            "cost": "Low",
            "description": "Build a lighting system that reacts automatically to the amount of light in a room.",
            "skills": ["Circuits", "Sensors", "Arduino", "C/C++", "Prototyping"],
            "materials": ["Arduino-compatible board", "Photoresistor", "LEDs", "Resistors", "Breadboard", "Jumper wires"],
            "steps": [
                "Learn how a photoresistor changes with light.",
                "Build and test the sensor circuit.",
                "Read sensor values with the microcontroller.",
                "Program LEDs to react to different light levels.",
                "Test the system in multiple lighting conditions.",
                "Document the final design and what you would improve."
            ],
            "portfolio": "Designed and programmed an automatic lighting prototype using a light sensor, microcontroller, and custom circuit logic."
        },
        {
            "title": "1D LED Pong Game",
            "fields": ["Electrical Engineering", "Computer Engineering", "Computer Science"],
            "create": ["A game", "A physical device", "Something with lights or electronics"],
            "level": "Intermediate",
            "time": "1–2 weeks",
            "hours": "8–15 hours",
            "style": ["Building with my hands", "Coding", "Solving logic problems"],
            "equipment": ["Computer", "Arduino / microcontroller", "Breadboard / basic electronics"],
            "cost": "Low",
            "description": "Create a physical Pong-style game using a row of LEDs, buttons, timing logic, and scoring.",
            "skills": ["Digital logic", "Embedded programming", "Circuit design", "Debugging"],
            "materials": ["Microcontroller", "LEDs", "Push buttons", "Resistors", "Breadboard", "Jumper wires"],
            "steps": [
                "Design the rules and game states.",
                "Wire the LED playing field and buttons.",
                "Program the moving LED.",
                "Add player input and collision timing.",
                "Create scoring and reset logic.",
                "Test difficulty and document the final system."
            ],
            "portfolio": "Built a physical LED Pong game integrating circuit design, player inputs, timing logic, and embedded programming."
        },
        {
            "title": "Mini Smart Home Security System",
            "fields": ["Electrical Engineering", "Computer Engineering", "Cybersecurity", "Robotics"],
            "create": ["A physical device", "Something that makes everyday life easier", "Something with sensors"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Building with my hands", "Coding", "Testing and experimenting"],
            "equipment": ["Computer", "Arduino / microcontroller", "Breadboard / basic electronics"],
            "cost": "Low–Medium",
            "description": "Build a prototype alarm that detects motion or an opened door and triggers an alert.",
            "skills": ["Sensors", "Embedded systems", "Circuit design", "Programming", "System testing"],
            "materials": ["Microcontroller", "Motion or magnetic sensor", "Buzzer", "LED", "Breadboard", "Wires"],
            "steps": [
                "Define what the system should detect.",
                "Test the sensor independently.",
                "Build the alarm circuit.",
                "Program normal and alert states.",
                "Add a reset or arm/disarm feature.",
                "Test false alarms and document improvements."
            ],
            "portfolio": "Developed a sensor-based home security prototype with programmable alarm states and real-world system testing."
        },
        {
            "title": "Reaction-Time Tester",
            "fields": ["Electrical Engineering", "Computer Engineering", "Biomedical Engineering"],
            "create": ["A physical device", "Something related to health or the human body", "Something with lights or electronics"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "3–6 hours",
            "style": ["Building with my hands", "Coding", "Testing and experimenting"],
            "equipment": ["Computer", "Arduino / microcontroller", "Breadboard / basic electronics"],
            "cost": "Low",
            "description": "Build a device that measures how quickly a person reacts after a light turns on.",
            "skills": ["Timing", "Microcontrollers", "Data collection", "Circuits"],
            "materials": ["Microcontroller", "LED", "Button", "Breadboard", "Resistors"],
            "steps": [
                "Create a random delay before the LED turns on.",
                "Wire an LED and response button.",
                "Measure elapsed time after the signal.",
                "Display or record reaction times.",
                "Test multiple users.",
                "Analyze variation in the results."
            ],
            "portfolio": "Designed a microcontroller-based reaction-time tester and collected human response data for analysis."
        },
        {
            "title": "Assistive Grip Device",
            "fields": ["Mechanical Engineering", "Biomedical Engineering", "Engineering"],
            "create": ["A physical device", "Something related to health or the human body", "Something that helps people"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Building with my hands", "Designing in CAD", "Testing and experimenting"],
            "equipment": ["Computer", "CAD software", "3D printer"],
            "cost": "Low–Medium",
            "description": "Design an inexpensive device that makes gripping or holding an everyday object easier.",
            "skills": ["CAD", "Human-centered design", "Prototyping", "Mechanical design", "Iteration"],
            "materials": ["CAD software", "Cardboard or 3D-print material", "Fasteners", "Everyday test objects"],
            "steps": [
                "Choose a specific gripping challenge.",
                "Research existing assistive products.",
                "Sketch several concepts.",
                "Model the best concept in CAD.",
                "Prototype and test it.",
                "Use feedback to create an improved version."
            ],
            "portfolio": "Designed and iterated an assistive mechanical device using human-centered design, CAD, prototyping, and user testing."
        },
        {
            "title": "Rubber-Band Powered Car",
            "fields": ["Mechanical Engineering", "Physics", "Engineering"],
            "create": ["A physical device", "Something that moves", "Something I can build cheaply"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "2–5 hours",
            "style": ["Building with my hands", "Testing and experimenting", "Solving logic problems"],
            "equipment": ["Basic household materials"],
            "cost": "Very Low",
            "description": "Design a small vehicle powered only by stored elastic energy and optimize it for distance.",
            "skills": ["Mechanics", "Energy", "Design iteration", "Measurement"],
            "materials": ["Cardboard", "Rubber bands", "Bottle caps or wheels", "Axles", "Tape"],
            "steps": [
                "Sketch a drivetrain concept.",
                "Build the chassis and axles.",
                "Create the rubber-band drive.",
                "Measure travel distance.",
                "Change one design variable at a time.",
                "Graph your results and identify the best design."
            ],
            "portfolio": "Engineered and optimized a rubber-band powered vehicle through iterative testing and quantitative performance analysis."
        },
        {
            "title": "Robotic Gripper",
            "fields": ["Mechanical Engineering", "Robotics", "Electrical Engineering"],
            "create": ["A robot", "A physical device", "Something that moves"],
            "level": "Advanced",
            "time": "1–2 months",
            "hours": "20+ hours",
            "style": ["Building with my hands", "Designing in CAD", "Coding"],
            "equipment": ["Computer", "Arduino / microcontroller", "CAD software", "3D printer"],
            "cost": "Medium",
            "description": "Design a motorized gripper capable of picking up several differently shaped objects.",
            "skills": ["CAD", "Mechanisms", "Servo control", "Embedded programming", "Iteration"],
            "materials": ["Microcontroller", "Servo motor", "3D printed or laser-cut parts", "Fasteners", "Wires"],
            "steps": [
                "Study common gripper mechanisms.",
                "Define target objects and constraints.",
                "Design the mechanism in CAD.",
                "Fabricate and assemble the gripper.",
                "Program servo movement.",
                "Test grip strength and redesign weak points."
            ],
            "portfolio": "Designed, fabricated, and programmed a robotic gripper using CAD, servo control, and iterative mechanical testing."
        },
        {
            "title": "Personal Portfolio Website",
            "fields": ["Computer Science", "Web Development"],
            "create": ["A website or app", "Something useful for school or my future", "Something creative"],
            "level": "Beginner",
            "time": "1–2 weeks",
            "hours": "5–10 hours",
            "style": ["Coding", "Designing a user experience", "Working mostly on a computer"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Build a personal website that showcases your projects, skills, experiences, and goals.",
            "skills": ["HTML", "CSS", "Web design", "GitHub", "Communication"],
            "materials": ["Computer", "Code editor", "GitHub account"],
            "steps": [
                "Plan the pages and content.",
                "Create the HTML structure.",
                "Style the site with CSS.",
                "Add project cards and an About section.",
                "Make the layout mobile-friendly.",
                "Publish and ask others for feedback."
            ],
            "portfolio": "Designed and deployed a responsive personal portfolio website showcasing technical projects, skills, and experiences."
        },
        {
            "title": "Study Planner Web App",
            "fields": ["Computer Science", "Web Development", "Software Engineering"],
            "create": ["A website or app", "Something useful for school or my future", "Something that helps people"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Coding", "Designing a user experience", "Solving logic problems"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Create an app where students can enter assignments, deadlines, and study goals.",
            "skills": ["Python or JavaScript", "UI design", "Data storage", "Software design"],
            "materials": ["Computer", "Streamlit or web framework", "GitHub"],
            "steps": [
                "Interview students about planning problems.",
                "Choose the minimum useful features.",
                "Build assignment and deadline inputs.",
                "Create a dashboard.",
                "Add saving or persistent storage.",
                "Test with real users and improve the interface."
            ],
            "portfolio": "Developed a student planning web application with deadline tracking, persistent data, and user-centered interface design."
        },
        {
            "title": "Local Opportunity Finder",
            "fields": ["Computer Science", "Data Science", "Software Engineering"],
            "create": ["A website or app", "Something that helps people", "Something useful for school or my future"],
            "level": "Advanced",
            "time": "1–2 months",
            "hours": "20+ hours",
            "style": ["Coding", "Working with data", "Designing a user experience"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Build a searchable tool that helps students discover internships, programs, scholarships, or community resources.",
            "skills": ["Python", "Databases", "Search/filtering", "Product design", "Data cleaning"],
            "materials": ["Computer", "Python", "Database or CSV", "GitHub"],
            "steps": [
                "Define the target student group.",
                "Create a structured opportunity dataset.",
                "Build filters and search.",
                "Add eligibility and deadline fields.",
                "Test recommendations with students.",
                "Document limitations and future improvements."
            ],
            "portfolio": "Built a data-driven opportunity discovery platform with structured filtering and student-focused recommendation features."
        },
        {
            "title": "Movie Recommendation Engine",
            "fields": ["Data Science", "Artificial Intelligence", "Computer Science"],
            "create": ["An AI project", "A website or app", "Something with data"],
            "level": "Intermediate",
            "time": "1–2 weeks",
            "hours": "8–15 hours",
            "style": ["Coding", "Working with data", "Solving logic problems"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Create a program that recommends movies based on genres, ratings, or similarities between users.",
            "skills": ["Python", "Pandas", "Recommendation systems", "Data analysis"],
            "materials": ["Computer", "Python", "Public movie dataset"],
            "steps": [
                "Load and clean a movie dataset.",
                "Explore ratings and genres.",
                "Create a simple recommendation rule.",
                "Build a similarity-based recommender.",
                "Evaluate sample recommendations.",
                "Create a simple interface for users."
            ],
            "portfolio": "Developed a Python recommendation engine using structured movie data, similarity metrics, and interactive user preferences."
        },
        {
            "title": "Image Classification Model",
            "fields": ["Artificial Intelligence", "Computer Science", "Data Science"],
            "create": ["An AI project", "Something with data", "Something creative"],
            "level": "Advanced",
            "time": "2–4 weeks",
            "hours": "15–25 hours",
            "style": ["Coding", "Working with data", "Testing and experimenting"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Train a machine-learning model to recognize categories of images and evaluate where it makes mistakes.",
            "skills": ["Python", "Machine learning", "Model evaluation", "Data preparation"],
            "materials": ["Computer", "Python notebook environment", "Open image dataset"],
            "steps": [
                "Choose a safe public image dataset.",
                "Prepare training and test data.",
                "Build a baseline classifier.",
                "Train and evaluate the model.",
                "Analyze incorrect predictions.",
                "Explain limitations and possible improvements."
            ],
            "portfolio": "Trained and evaluated an image classification model, analyzing prediction errors and model limitations."
        },
        {
            "title": "NYC Data Story",
            "fields": ["Data Science", "Mathematics", "Environmental Science"],
            "create": ["Something with data", "Something that helps my community", "A research project"],
            "level": "Beginner",
            "time": "1–2 weeks",
            "hours": "5–10 hours",
            "style": ["Working with data", "Researching", "Working mostly on a computer"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Use a public NYC dataset to investigate a question about transportation, environment, education, or another community issue.",
            "skills": ["Python", "Data visualization", "Statistics", "Research questions", "Communication"],
            "materials": ["Computer", "Python or spreadsheet software", "NYC Open Data"],
            "steps": [
                "Choose a community question.",
                "Find a relevant public dataset.",
                "Clean the data.",
                "Create at least three visualizations.",
                "Interpret patterns carefully.",
                "Present a conclusion and limitations."
            ],
            "portfolio": "Analyzed a public NYC dataset using Python and data visualization to investigate a community-focused research question."
        },
        {
            "title": "Air Quality Data Dashboard",
            "fields": ["Environmental Science", "Data Science", "Computer Science"],
            "create": ["Something with data", "Something that helps my community", "A website or app"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Coding", "Working with data", "Researching"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Create an interactive dashboard that explores air-quality patterns across locations or time.",
            "skills": ["Python", "Data visualization", "Environmental analysis", "Dashboard design"],
            "materials": ["Computer", "Public air-quality dataset", "Streamlit"],
            "steps": [
                "Choose an air-quality dataset.",
                "Identify useful pollutants and measurements.",
                "Clean and summarize the data.",
                "Build charts and filters.",
                "Add explanations for nontechnical users.",
                "Publish the dashboard and document limitations."
            ],
            "portfolio": "Created an interactive air-quality dashboard using public environmental data, Python, and visual analytics."
        },
        {
            "title": "Plant Growth Experiment",
            "fields": ["Biology", "Environmental Science"],
            "create": ["A research project", "Something involving biology", "Something I can build cheaply"],
            "level": "Beginner",
            "time": "2–4 weeks",
            "hours": "5–10 hours",
            "style": ["Testing and experimenting", "Researching", "Working with data"],
            "equipment": ["Basic household materials"],
            "cost": "Very Low",
            "description": "Design a controlled experiment testing how one environmental variable affects plant growth.",
            "skills": ["Experimental design", "Measurement", "Biology", "Data analysis"],
            "materials": ["Seeds", "Containers", "Growing medium", "Ruler", "Chosen experimental variable"],
            "steps": [
                "Write a testable research question.",
                "Identify independent and dependent variables.",
                "Create control and experimental groups.",
                "Collect measurements consistently.",
                "Graph the results.",
                "Write a conclusion that discusses limitations."
            ],
            "portfolio": "Designed and conducted a controlled plant-growth experiment, collecting and analyzing quantitative biological data."
        },
        {
            "title": "Low-Cost Water Filter Investigation",
            "fields": ["Environmental Science", "Engineering", "Chemistry"],
            "create": ["A research project", "Something that helps my community", "A physical device"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "8–15 hours",
            "style": ["Building with my hands", "Testing and experimenting", "Researching"],
            "equipment": ["Basic household materials"],
            "cost": "Low",
            "description": "Compare safe model filtration materials to study how engineering design changes water clarity. Do not drink filtered test water.",
            "skills": ["Experimental design", "Environmental engineering", "Measurement", "Iteration"],
            "materials": ["Bottles", "Gravel", "Sand", "Filter material", "Prepared non-potable test water"],
            "steps": [
                "Research the purpose of filtration layers.",
                "Define a safe test method.",
                "Build multiple filter designs.",
                "Measure changes in clarity or another safe indicator.",
                "Compare designs.",
                "Explain why filtration alone does not necessarily make water safe to drink."
            ],
            "portfolio": "Investigated low-cost water filtration designs through controlled testing and comparative environmental engineering analysis."
        },
        {
            "title": "Heart-Rate Data Investigation",
            "fields": ["Biomedical Engineering", "Biology", "Data Science"],
            "create": ["Something related to health or the human body", "Something with data", "A research project"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "3–6 hours",
            "style": ["Working with data", "Testing and experimenting", "Researching"],
            "equipment": ["Computer", "Phone sensors / wearable (optional)"],
            "cost": "Free",
            "description": "Explore how heart rate changes during safe everyday activities using your own measurements or a public dataset.",
            "skills": ["Physiology", "Data collection", "Statistics", "Visualization"],
            "materials": ["Timer or wearable", "Computer or spreadsheet"],
            "steps": [
                "Choose a simple question about heart rate.",
                "Create a consistent measurement procedure.",
                "Collect or obtain non-sensitive sample data.",
                "Calculate summary statistics.",
                "Graph the results.",
                "Discuss variation without making medical conclusions."
            ],
            "portfolio": "Conducted a quantitative heart-rate investigation using structured data collection, visualization, and statistical analysis."
        },
        {
            "title": "Bridge Design Challenge",
            "fields": ["Civil Engineering", "Mechanical Engineering", "Physics"],
            "create": ["A physical device", "Something I can build cheaply", "A research project"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "3–6 hours",
            "style": ["Building with my hands", "Testing and experimenting", "Solving logic problems"],
            "equipment": ["Basic household materials"],
            "cost": "Very Low",
            "description": "Design a lightweight model bridge and test how much load it can support.",
            "skills": ["Structures", "Forces", "Engineering design", "Testing"],
            "materials": ["Craft sticks or paper", "Glue or tape", "Weights", "Scale"],
            "steps": [
                "Research basic bridge structures.",
                "Set size and material constraints.",
                "Sketch your design.",
                "Build the bridge.",
                "Test increasing loads safely.",
                "Calculate strength-to-weight performance and redesign."
            ],
            "portfolio": "Designed and load-tested a model bridge, applying structural concepts and iterative engineering optimization."
        },
        {
            "title": "Solar Oven Optimization",
            "fields": ["Environmental Science", "Mechanical Engineering", "Physics"],
            "create": ["A physical device", "Something involving energy", "Something I can build cheaply"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "3–6 hours",
            "style": ["Building with my hands", "Testing and experimenting", "Working with data"],
            "equipment": ["Basic household materials"],
            "cost": "Very Low",
            "description": "Build a small solar heating device and test how design choices affect temperature.",
            "skills": ["Energy", "Heat transfer", "Experimental design", "Optimization"],
            "materials": ["Cardboard box", "Foil", "Clear covering", "Dark paper", "Thermometer"],
            "steps": [
                "Research heat absorption and reflection.",
                "Build a baseline solar oven.",
                "Measure temperature over time.",
                "Change one design feature.",
                "Compare performance.",
                "Document the most effective design."
            ],
            "portfolio": "Built and optimized a solar heating prototype using experimental data and heat-transfer principles."
        },
        {
            "title": "Interactive Physics Simulator",
            "fields": ["Physics", "Computer Science", "Mathematics"],
            "create": ["A website or app", "Something useful for school or my future", "A simulation"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Coding", "Solving logic problems", "Designing a user experience"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Build an interactive simulation for projectile motion, collisions, circuits, or another physics concept.",
            "skills": ["Python", "Physics modeling", "Mathematics", "Visualization"],
            "materials": ["Computer", "Python", "Streamlit or plotting library"],
            "steps": [
                "Choose one physics model.",
                "Write the governing equations.",
                "Verify calculations with sample values.",
                "Build adjustable user inputs.",
                "Visualize the simulated result.",
                "Explain assumptions and limitations."
            ],
            "portfolio": "Developed an interactive physics simulation translating mathematical models into adjustable visual software."
        },
        {
            "title": "Budget Optimization Tool",
            "fields": ["Industrial Engineering", "Data Science", "Mathematics", "Computer Science"],
            "create": ["A website or app", "Something with data", "Something that solves an optimization problem"],
            "level": "Advanced",
            "time": "2–4 weeks",
            "hours": "15–25 hours",
            "style": ["Coding", "Working with data", "Solving logic problems"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Create a tool that allocates a limited budget across competing needs while respecting user-defined constraints.",
            "skills": ["Optimization", "Python", "Linear programming", "Data modeling", "UI design"],
            "materials": ["Computer", "Python", "Optimization library"],
            "steps": [
                "Define a realistic allocation problem.",
                "Identify decision variables and constraints.",
                "Write an objective function.",
                "Implement the optimization model.",
                "Build inputs for different scenarios.",
                "Explain tradeoffs and test edge cases."
            ],
            "portfolio": "Built an optimization tool using mathematical programming to allocate limited resources under real-world constraints."
        },
        {
            "title": "Emergency Response Location Model",
            "fields": ["Industrial Engineering", "Data Science", "Mathematics"],
            "create": ["Something with data", "Something that helps my community", "Something that solves an optimization problem"],
            "level": "Advanced",
            "time": "1–2 months",
            "hours": "20+ hours",
            "style": ["Coding", "Working with data", "Solving logic problems"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Build a simplified model that chooses service locations to improve coverage or response time using public or synthetic data.",
            "skills": ["Operations research", "Optimization", "Python", "Data analysis", "Model assumptions"],
            "materials": ["Computer", "Python", "Public or synthetic location data"],
            "steps": [
                "Define the service-area problem.",
                "Create or clean location data.",
                "Choose a coverage or distance objective.",
                "Implement a simplified optimization model.",
                "Compare multiple scenarios.",
                "Explain ethical limitations and what real deployment would require."
            ],
            "portfolio": "Developed a facility-location optimization model to evaluate service coverage and resource-allocation tradeoffs."
        }
    ]

    # --------------------------------------------------------
    # DISCOVERY QUESTIONS
    # --------------------------------------------------------

    st.header("What do you want to create?")

    create_choices = st.multiselect(
        "Choose anything that sounds exciting.",
        [
            "A physical device",
            "A robot",
            "A game",
            "A website or app",
            "An AI project",
            "Something with data",
            "A research project",
            "Something related to health or the human body",
            "Something involving biology",
            "Something involving energy",
            "Something with sensors",
            "Something with lights or electronics",
            "Something that moves",
            "A simulation",
            "Something that solves an optimization problem",
            "Something that helps people",
            "Something that helps my community",
            "Something that makes everyday life easier",
            "Something useful for school or my future",
            "Something creative",
            "Something I can build cheaply",
            "Surprise me"
        ],
        key="project_create_choices"
    )

    project_field = st.multiselect(
        "Are there any STEM areas you want to explore?",
        [
            "I'm not sure yet",
            "Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Computer Engineering",
            "Civil Engineering",
            "Industrial Engineering",
            "Biomedical Engineering",
            "Robotics",
            "Computer Science",
            "Software Engineering",
            "Web Development",
            "Artificial Intelligence",
            "Data Science",
            "Cybersecurity",
            "Biology",
            "Environmental Science",
            "Physics",
            "Mathematics",
            "Chemistry"
        ],
        key="project_field_choices"
    )

    project_style = st.multiselect(
        "How would you like to spend most of your time?",
        [
            "Building with my hands",
            "Coding",
            "Working with data",
            "Designing in CAD",
            "Testing and experimenting",
            "Researching",
            "Solving logic problems",
            "Designing a user experience",
            "Working mostly on a computer"
        ],
        key="project_style_choices"
    )

    col1, col2 = st.columns(2)

    with col1:
        project_level = st.selectbox(
            "How challenging should the project be?",
            [
                "Any level",
                "Beginner",
                "Intermediate",
                "Advanced"
            ],
            key="project_level_choice"
        )

    with col2:
        project_time = st.selectbox(
            "How long do you want to work on it?",
            [
                "Any amount of time",
                "Weekend",
                "1–2 weeks",
                "2–4 weeks",
                "1–2 months"
            ],
            key="project_time_choice"
        )

    with st.expander("What equipment do you have? (optional)"):

        equipment = st.multiselect(
            "Select everything you can access.",
            [
                "Computer",
                "Basic household materials",
                "Arduino / microcontroller",
                "Breadboard / basic electronics",
                "CAD software",
                "3D printer",
                "Raspberry Pi",
                "Phone sensors / wearable (optional)"
            ],
            key="project_equipment_choices"
        )

        budget = st.selectbox(
            "How much would you prefer to spend?",
            [
                "Any budget",
                "Free only",
                "Very low cost",
                "Low cost",
                "Low–Medium is okay",
                "Medium is okay"
            ],
            key="project_budget_choice"
        )

    # --------------------------------------------------------
    # MATCHING
    # --------------------------------------------------------

    def project_match(project):

        score = 0
        reasons = []

        if create_choices:
            overlap = len(
                set(create_choices)
                &
                set(project["create"])
            )

            score += min(
                overlap * 14,
                42
            )

            if overlap:
                reasons.append(
                    "Matches what you said you want to create."
                )

        selected_fields = [
            item
            for item in project_field
            if item != "I'm not sure yet"
        ]

        if selected_fields:
            overlap = len(
                set(selected_fields)
                &
                set(project["fields"])
            )

            score += min(
                overlap * 12,
                30
            )

            if overlap:
                reasons.append(
                    "Connects to STEM fields you want to explore."
                )

        if project_style:
            overlap = len(
                set(project_style)
                &
                set(project["style"])
            )

            score += min(
                overlap * 8,
                24
            )

            if overlap:
                reasons.append(
                    "Fits the way you said you like to work."
                )

        if (
            project_level == "Any level"
            or project_level == project["level"]
        ):
            score += 12

        if (
            project_time == "Any amount of time"
            or project_time == project["time"]
        ):
            score += 10

        if equipment:
            required = set(
                project["equipment"]
            )

            available = set(
                equipment
            )

            equipment_overlap = len(
                required & available
            )

            if required:
                score += round(
                    12
                    *
                    equipment_overlap
                    /
                    len(required)
                )

        # If the user hasn't made many selections yet, keep useful
        # projects visible rather than producing meaningless zeroes.
        if not create_choices:
            score += 10

        if not selected_fields:
            score += 8

        if not project_style:
            score += 6

        return score, reasons

    if st.button(
        "Find Projects for Me",
        type="primary",
        use_container_width=True
    ):

        ranked_projects = []

        for project in project_catalog:

            score, reasons = project_match(
                project
            )

            ranked_projects.append(
                {
                    "project": project,
                    "score": score,
                    "reasons": reasons
                }
            )

        ranked_projects.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        st.session_state[
            "project_recommendations"
        ] = ranked_projects

        st.rerun()

    recommendations = st.session_state.get(
        "project_recommendations"
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if recommendations:

        st.divider()

        st.header("Your Best Project Matches")

        st.caption(
            "Projects are ordered by how closely they match your answers. "
            "You can still explore any project that sounds interesting."
        )

        top_score = max(
            recommendations[0]["score"],
            1
        )

        for rank, item in enumerate(
            recommendations[:12],
            start=1
        ):

            project = item["project"]

            relative_match = min(
                round(
                    item["score"]
                    /
                    top_score
                    *
                    100
                ),
                100
            )

            with st.container(
                border=True
            ):

                title_col, match_col = (
                    st.columns(
                        [4, 1]
                    )
                )

                with title_col:

                    st.subheader(
                        f"{rank}. {project['title']}"
                    )

                    st.caption(
                        " • ".join(
                            project["fields"][:3]
                        )
                    )

                with match_col:

                    st.metric(
                        "Project Match",
                        f"{relative_match}%"
                    )

                meta1, meta2, meta3, meta4 = (
                    st.columns(4)
                )

                with meta1:
                    st.write(
                        f"**Level**\n\n{project['level']}"
                    )

                with meta2:
                    st.write(
                        f"**Timeline**\n\n{project['time']}"
                    )

                with meta3:
                    st.write(
                        f"**Workload**\n\n{project['hours']}"
                    )

                with meta4:
                    st.write(
                        f"**Cost**\n\n{project['cost']}"
                    )

                st.write(
                    project["description"]
                )

                st.write(
                    "**Skills you'll build:** "
                    +
                    " • ".join(
                        project["skills"]
                    )
                )

                with st.expander(
                    "See materials and project roadmap"
                ):

                    st.write(
                        "**What you'll need**"
                    )

                    for material in project[
                        "materials"
                    ]:
                        st.write(
                            f"• {material}"
                        )

                    st.write(
                        "**Suggested roadmap**"
                    )

                    for step_number, step in enumerate(
                        project["steps"],
                        start=1
                    ):
                        st.write(
                            f"{step_number}. {step}"
                        )

                    st.write(
                        "**Possible portfolio description**"
                    )

                    st.write(
                        project["portfolio"]
                    )

                if item["reasons"]:

                    st.caption(
                        "Why it matches: "
                        +
                        " ".join(
                            item["reasons"]
                        )
                    )

        st.divider()

        st.info(
            "Next upgrade: students will be able to save a project, press "
            "'Start Project,' track milestones, and move completed projects "
            "into a personal STEM portfolio."
        )

    else:

        st.divider()

        st.header("Examples of What You Can Build")

        example_cols = st.columns(3)

        for index, project in enumerate(
            project_catalog[:6]
        ):

            with example_cols[
                index % 3
            ]:

                with st.container(
                    border=True
                ):

                    st.caption(
                        project["level"]
                    )

                    st.subheader(
                        project["title"]
                    )

                    st.write(
                        project["description"]
                    )

                    st.caption(
                        f"{project['time']} • {project['cost']} cost"
                    )

    st.divider()

    st.caption(
        "STEM Pathways NYC • Explore • Build • Discover"
    )


# ============================================================
# RESOURCES
# ============================================================

elif page == "Resources":

    st.title(
        "Resources"
    )

    st.write(
        "Build the skills you need using free and accessible "
        "learning resources."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        with st.container(
            border=True
        ):

            st.subheader(
                "💻 Programming"
            )

            st.write(
                "Python • GitHub • Web Development • Data Analysis"
            )

            st.caption(
                "Build programming skills that can support software, "
                "data science, AI, and engineering projects."
            )

        with st.container(
            border=True
        ):

            st.subheader(
                "⚙️ Engineering"
            )

            st.write(
                "CAD • Electronics • Circuit Design • Arduino • Prototyping"
            )

            st.caption(
                "Develop practical engineering skills through design "
                "and hands-on experimentation."
            )

    with col2:

        with st.container(
            border=True
        ):

            st.subheader(
                "🔬 Research"
            )

            st.write(
                "Experimental Design • Data Collection • "
                "Scientific Writing • Analysis"
            )

            st.caption(
                "Learn the fundamentals needed to investigate questions "
                "and communicate scientific findings."
            )

        with st.container(
            border=True
        ):

            st.subheader(
                "🎓 Career Exploration"
            )

            st.write(
                "STEM Majors • Engineering Fields • "
                "Research Careers • Technical Careers"
            )

            st.caption(
                "Compare possible majors and careers before deciding "
                "which directions you want to explore further."
            )


# ============================================================
# GPA CALCULATOR & CONVERTER
# ============================================================

elif page == "GPA Calculator":

    # --------------------------------------------------------
    # GPA SESSION STATE + RESET HELPERS
    # --------------------------------------------------------

    if "gpa_calculation_result" not in st.session_state:
        st.session_state.gpa_calculation_result = None

    if "gpa_results_confirmed" not in st.session_state:
        st.session_state.gpa_results_confirmed = False

    if "gpa_show_restart_confirmation" not in st.session_state:
        st.session_state.gpa_show_restart_confirmation = False

    def reset_gpa_tools():
        keys_to_remove = [
            key
            for key in list(st.session_state.keys())
            if key.startswith("gpa_")
        ]

        for key in keys_to_remove:
            del st.session_state[key]

    st.title(
        "📊 GPA Calculator & Converter"
    )

    st.write(
        "Estimate your unweighted and weighted GPA, then convert between "
        "a 4.0 scale and a 100-point average."
    )

    st.info(
        "GPA policies vary by high school, college, and university. "
        "Weighted GPA and scale conversions on this page are estimates "
        "for planning purposes, not official transcript calculations."
    )

    st.divider()

    calculator_tab, converter_tab = st.tabs(
        [
            "🧮 Course GPA Calculator",
            "🔄 GPA Scale Converter"
        ]
    )

    # --------------------------------------------------------
    # COURSE GPA CALCULATOR
    # --------------------------------------------------------

    with calculator_tab:

        st.header(
            "Calculate Your GPA"
        )

        st.write(
            "Enter your courses, letter grades, course levels, and credits. "
            "The calculator will estimate both unweighted and weighted GPA."
        )

        # Dynamic course list: starts with 5 courses and allows up to 15.
        if "gpa_course_ids" not in st.session_state:
            st.session_state.gpa_course_ids = [0, 1, 2, 3, 4]

        if "gpa_next_course_id" not in st.session_state:
            st.session_state.gpa_next_course_id = 5

        course_control_col1, course_control_col2 = st.columns([1, 2])

        with course_control_col1:
            if st.button(
                "➕ Add Course",
                use_container_width=True,
                key="gpa_add_course",
                disabled=len(st.session_state.gpa_course_ids) >= 15
            ):
                new_course_id = st.session_state.gpa_next_course_id
                st.session_state.gpa_course_ids.append(new_course_id)
                st.session_state.gpa_next_course_id += 1
                st.session_state.gpa_results_confirmed = False
                st.rerun()

        with course_control_col2:
            st.caption(
                f"{len(st.session_state.gpa_course_ids)} of 15 courses added"
            )

        if len(st.session_state.gpa_course_ids) >= 15:
            st.info(
                "You reached the 15-course maximum. Remove a course if you want to add a different one."
            )

        grade_points = {
            "A+": 4.0,
            "A": 4.0,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "C-": 1.7,
            "D+": 1.3,
            "D": 1.0,
            "F": 0.0
        }

        level_bonus = {
            "Regular": 0.0,
            "Honors": 0.5,
            "AP / IB": 1.0,
            "Dual Enrollment": 1.0
        }

        course_rows = []

        st.markdown(
            "#### Your Courses"
        )

        for display_index, course_id in enumerate(
            list(st.session_state.gpa_course_ids),
            start=1
        ):

            with st.container(
                border=True
            ):

                title_col, remove_col = st.columns([4, 1])

                with title_col:
                    st.caption(
                        f"Course {display_index}"
                    )

                with remove_col:
                    if st.button(
                        "Remove",
                        key=f"gpa_remove_course_{course_id}",
                        use_container_width=True,
                        disabled=len(st.session_state.gpa_course_ids) <= 1
                    ):
                        st.session_state.gpa_course_ids.remove(course_id)

                        for course_key in [
                            f"gpa_course_name_{course_id}",
                            f"gpa_letter_grade_{course_id}",
                            f"gpa_course_level_{course_id}",
                            f"gpa_credits_{course_id}",
                        ]:
                            st.session_state.pop(course_key, None)

                        st.session_state.gpa_calculation_result = None
                        st.session_state.gpa_results_confirmed = False
                        st.rerun()

                name_col, grade_col, level_col, credit_col = st.columns(
                    [2.4, 1, 1.6, 1]
                )

                with name_col:

                    course_name = st.text_input(
                        "Course",
                        value="",
                        placeholder="e.g. AP Biology",
                        key=f"gpa_course_name_{course_id}"
                    )

                with grade_col:

                    letter_grade = st.selectbox(
                        "Grade",
                        list(grade_points.keys()),
                        index=1,
                        key=f"gpa_letter_grade_{course_id}"
                    )

                with level_col:

                    course_level = st.selectbox(
                        "Level",
                        list(level_bonus.keys()),
                        key=f"gpa_course_level_{course_id}"
                    )

                with credit_col:

                    credits = st.number_input(
                        "Credits",
                        min_value=0.25,
                        max_value=4.0,
                        value=1.0,
                        step=0.25,
                        key=f"gpa_credits_{course_id}"
                    )

                course_rows.append(
                    {
                        "name": course_name.strip() or f"Course {display_index}",
                        "grade": letter_grade,
                        "level": course_level,
                        "credits": float(credits)
                    }
                )

        if st.button(
            "Calculate My GPA",
            type="primary",
            use_container_width=True,
            key="gpa_calculate_course_gpa"
        ):

            total_credits = sum(
                course["credits"]
                for course in course_rows
            )

            if total_credits <= 0:

                st.warning(
                    "Please enter at least one course with credits."
                )

            else:

                unweighted_quality_points = sum(
                    grade_points[course["grade"]]
                    * course["credits"]
                    for course in course_rows
                )

                weighted_quality_points = sum(
                    (
                        grade_points[course["grade"]]
                        + level_bonus[course["level"]]
                    )
                    * course["credits"]
                    for course in course_rows
                )

                unweighted_gpa = (
                    unweighted_quality_points
                    / total_credits
                )

                weighted_gpa = (
                    weighted_quality_points
                    / total_credits
                )

                if unweighted_gpa >= 4.0:
                    estimated_100 = "93–100"
                elif unweighted_gpa >= 3.7:
                    estimated_100 = "90–92"
                elif unweighted_gpa >= 3.3:
                    estimated_100 = "87–89"
                elif unweighted_gpa >= 3.0:
                    estimated_100 = "83–86"
                elif unweighted_gpa >= 2.7:
                    estimated_100 = "80–82"
                elif unweighted_gpa >= 2.3:
                    estimated_100 = "77–79"
                elif unweighted_gpa >= 2.0:
                    estimated_100 = "73–76"
                elif unweighted_gpa >= 1.7:
                    estimated_100 = "70–72"
                elif unweighted_gpa >= 1.3:
                    estimated_100 = "67–69"
                elif unweighted_gpa >= 1.0:
                    estimated_100 = "65–66"
                else:
                    estimated_100 = "Below 65"

                calculation_rows = []

                for course in course_rows:

                    base = grade_points[
                        course["grade"]
                    ]

                    weighted = (
                        base
                        + level_bonus[
                            course["level"]
                        ]
                    )

                    calculation_rows.append(
                        {
                            "Course": course["name"],
                            "Grade": course["grade"],
                            "Level": course["level"],
                            "Credits": course["credits"],
                            "Unweighted Points": round(base, 2),
                            "Weighted Points": round(weighted, 2)
                        }
                    )

                st.session_state.gpa_calculation_result = {
                    "unweighted_gpa": unweighted_gpa,
                    "weighted_gpa": weighted_gpa,
                    "estimated_100": estimated_100,
                    "calculation_rows": calculation_rows
                }

                st.session_state.gpa_results_confirmed = False

        if st.session_state.gpa_calculation_result:

            result = st.session_state.gpa_calculation_result

            st.divider()

            st.subheader(
                "Your Estimated Results"
            )

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:

                st.metric(
                    "Unweighted GPA",
                    f"{result['unweighted_gpa']:.2f} / 4.00"
                )

            with result_col2:

                st.metric(
                    "Estimated Weighted GPA",
                    f"{result['weighted_gpa']:.2f}"
                )

            with result_col3:

                st.metric(
                    "Approx. 100-Point Range",
                    result["estimated_100"]
                )

            st.caption(
                "Weighted estimate used here: Regular +0.0, Honors +0.5, "
                "AP/IB +1.0, Dual Enrollment +1.0. Your school may use a different system."
            )

            with st.expander(
                "See course-by-course calculation"
            ):

                st.dataframe(
                    pd.DataFrame(
                        result["calculation_rows"]
                    ),
                    use_container_width=True,
                    hide_index=True
                )

            st.divider()

            if st.session_state.gpa_results_confirmed:

                st.success(
                    "✅ GPA results confirmed. You can still restart the calculator "
                    "below if you want to try different courses or grades."
                )

            else:

                st.write(
                    "If these courses and grades look correct, confirm your results. "
                    "Nothing is saved to your official school record."
                )

                if st.button(
                    "✅ Confirm My GPA Results",
                    type="primary",
                    use_container_width=True,
                    key="gpa_confirm_results"
                ):

                    st.session_state.gpa_results_confirmed = True
                    st.rerun()

    # --------------------------------------------------------
    # GPA SCALE CONVERTER
    # --------------------------------------------------------

    with converter_tab:

        st.header(
            "GPA Scale Converter"
        )

        st.write(
            "Use this tool when you know your GPA on one scale and want an "
            "approximate equivalent on another."
        )

        conversion_direction = st.radio(
            "Convert from",
            [
                "4.0 GPA → 100-Point Scale",
                "100-Point Average → 4.0 GPA"
            ],
            horizontal=True,
            key="gpa_conversion_direction"
        )

        st.divider()

        if conversion_direction == "4.0 GPA → 100-Point Scale":

            four_point_gpa = st.number_input(
                "Enter your GPA on a 4.0 scale",
                min_value=0.0,
                max_value=4.0,
                value=3.50,
                step=0.01,
                format="%.2f",
                key="gpa_four_point_input"
            )

            if four_point_gpa >= 4.0:
                hundred_range = "93–100"
                letter_equivalent = "A / A+"
            elif four_point_gpa >= 3.7:
                hundred_range = "90–92"
                letter_equivalent = "A-"
            elif four_point_gpa >= 3.3:
                hundred_range = "87–89"
                letter_equivalent = "B+"
            elif four_point_gpa >= 3.0:
                hundred_range = "83–86"
                letter_equivalent = "B"
            elif four_point_gpa >= 2.7:
                hundred_range = "80–82"
                letter_equivalent = "B-"
            elif four_point_gpa >= 2.3:
                hundred_range = "77–79"
                letter_equivalent = "C+"
            elif four_point_gpa >= 2.0:
                hundred_range = "73–76"
                letter_equivalent = "C"
            elif four_point_gpa >= 1.7:
                hundred_range = "70–72"
                letter_equivalent = "C-"
            elif four_point_gpa >= 1.3:
                hundred_range = "67–69"
                letter_equivalent = "D+"
            elif four_point_gpa >= 1.0:
                hundred_range = "65–66"
                letter_equivalent = "D"
            else:
                hundred_range = "Below 65"
                letter_equivalent = "F"

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    "Estimated 100-Point Equivalent",
                    hundred_range
                )

            with result_col2:

                st.metric(
                    "Approximate Letter Grade",
                    letter_equivalent
                )

        else:

            hundred_average = st.number_input(
                "Enter your average on a 100-point scale",
                min_value=0.0,
                max_value=100.0,
                value=90.0,
                step=0.1,
                format="%.1f",
                key="gpa_hundred_point_input"
            )

            if hundred_average >= 93:
                converted_gpa = 4.0
                letter_equivalent = "A / A+"
            elif hundred_average >= 90:
                converted_gpa = 3.7
                letter_equivalent = "A-"
            elif hundred_average >= 87:
                converted_gpa = 3.3
                letter_equivalent = "B+"
            elif hundred_average >= 83:
                converted_gpa = 3.0
                letter_equivalent = "B"
            elif hundred_average >= 80:
                converted_gpa = 2.7
                letter_equivalent = "B-"
            elif hundred_average >= 77:
                converted_gpa = 2.3
                letter_equivalent = "C+"
            elif hundred_average >= 73:
                converted_gpa = 2.0
                letter_equivalent = "C"
            elif hundred_average >= 70:
                converted_gpa = 1.7
                letter_equivalent = "C-"
            elif hundred_average >= 67:
                converted_gpa = 1.3
                letter_equivalent = "D+"
            elif hundred_average >= 65:
                converted_gpa = 1.0
                letter_equivalent = "D"
            else:
                converted_gpa = 0.0
                letter_equivalent = "F"

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    "Estimated 4.0 GPA",
                    f"{converted_gpa:.1f} / 4.0"
                )

            with result_col2:

                st.metric(
                    "Approximate Letter Grade",
                    letter_equivalent
                )

        st.divider()

        st.markdown(
            "#### Approximate Conversion Guide"
        )

        conversion_table = pd.DataFrame(
            [
                ["93–100", "A / A+", "4.0"],
                ["90–92", "A-", "3.7"],
                ["87–89", "B+", "3.3"],
                ["83–86", "B", "3.0"],
                ["80–82", "B-", "2.7"],
                ["77–79", "C+", "2.3"],
                ["73–76", "C", "2.0"],
                ["70–72", "C-", "1.7"],
                ["67–69", "D+", "1.3"],
                ["65–66", "D", "1.0"],
                ["Below 65", "F", "0.0"]
            ],
            columns=[
                "100-Point Range",
                "Letter Grade",
                "Approx. 4.0 GPA"
            ]
        )

        st.dataframe(
            conversion_table,
            use_container_width=True,
            hide_index=True
        )

        st.warning(
            "There is no universal official conversion between a 4.0 GPA "
            "and a 100-point average. Colleges may recalculate grades using "
            "their own methods, so use these results only as an estimate."
        )

    # --------------------------------------------------------
    # CONFIRM / RESTART AREA
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Finished?"
    )

    st.write(
        "If you entered something incorrectly or want to test a different set "
        "of grades, you can restart the GPA tools without affecting your profile."
    )

    if not st.session_state.gpa_show_restart_confirmation:

        if st.button(
            "↻ Start Over",
            use_container_width=True,
            key="gpa_restart_request"
        ):

            st.session_state.gpa_show_restart_confirmation = True
            st.rerun()

    else:

        st.warning(
            "Start over? This will clear the courses, grades, calculator results, "
            "and converter inputs on this page."
        )

        restart_col1, restart_col2 = st.columns(2)

        with restart_col1:

            if st.button(
                "Yes, Start Over",
                type="primary",
                use_container_width=True,
                key="gpa_restart_confirm",
                on_click=reset_gpa_tools
            ):
                pass

        with restart_col2:

            if st.button(
                "Cancel",
                use_container_width=True,
                key="gpa_restart_cancel"
            ):

                st.session_state.gpa_show_restart_confirmation = False
                st.rerun()


# ============================================================
# ADMIN DASHBOARD
# ============================================================

elif page == "Admin Dashboard":

    if not is_admin_user(
        user_email
    ):

        st.error(
            "You do not have permission to view this page."
        )

        st.stop()

    st.title(
        "Admin Dashboard"
    )

    st.write(
        "Review platform activity, user feedback, and early usage trends "
        "for STEM Pathways NYC."
    )

    st.warning(
        "This dashboard contains user-submitted information. "
        "Use it only to improve the platform and avoid sharing personally identifiable data publicly."
    )

    st.divider()

    admin_data = load_admin_metrics()

    profiles = admin_data[
        "profiles"
    ]

    feedback_rows = admin_data[
        "feedback"
    ]

    saved_rows = admin_data[
        "saved_opportunities"
    ]

    favorite_rows = admin_data[
        "favorite_colleges"
    ]

    # --------------------------------------------------------
    # PLATFORM OVERVIEW
    # --------------------------------------------------------

    st.header(
        "Platform Overview"
    )

    review_count = len(
        feedback_rows
    )

    avg_rating = 0

    if review_count:

        ratings = [
            int(
                row.get(
                    "rating",
                    0
                )
                or 0
            )
            for row in feedback_rows
            if row.get(
                "rating"
            )
            is not None
        ]

        if ratings:

            avg_rating = (
                sum(
                    ratings
                )
                /
                len(
                    ratings
                )
            )

    recommend_yes = sum(
        1
        for row in feedback_rows
        if str(
            row.get(
                "would_recommend",
                ""
            )
        ).strip().lower()
        ==
        "yes"
    )

    recommend_rate = (
        round(
            (
                recommend_yes
                /
                review_count
            )
            * 100
        )
        if review_count
        else 0
    )

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )

    with metric1:

        st.metric(
            "Student Profiles",
            len(
                profiles
            )
        )

    with metric2:

        st.metric(
            "Feedback Responses",
            review_count
        )

    with metric3:

        st.metric(
            "Average Rating",
            (
                f"{avg_rating:.1f} / 5"
                if review_count
                else "No data"
            )
        )

    with metric4:

        st.metric(
            "Would Recommend",
            (
                f"{recommend_rate}%"
                if review_count
                else "No data"
            )
        )

    metric5, metric6 = (
        st.columns(2)
    )

    with metric5:

        st.metric(
            "Saved Opportunities",
            len(
                saved_rows
            )
        )

    with metric6:

        st.metric(
            "Favorite Colleges",
            len(
                favorite_rows
            )
        )

    st.divider()

    # --------------------------------------------------------
    # FEEDBACK ANALYTICS
    # --------------------------------------------------------

    st.header(
        "Feedback Analytics"
    )

    if not feedback_rows:

        st.info(
            "No feedback has been submitted yet."
        )

    else:

        ease_scores = [
            int(
                row.get(
                    "ease_of_use",
                    0
                )
                or 0
            )
            for row in feedback_rows
            if row.get(
                "ease_of_use"
            )
            is not None
        ]

        avg_ease = (
            sum(
                ease_scores
            )
            /
            len(
                ease_scores
            )
            if ease_scores
            else 0
        )

        rating_counts = {
            rating: 0
            for rating in range(
                1,
                6
            )
        }

        for row in feedback_rows:

            try:

                rating_counts[
                    int(
                        row.get(
                            "rating",
                            0
                        )
                    )
                ] += 1

            except Exception:

                pass

        feedback_col1, feedback_col2 = (
            st.columns(2)
        )

        with feedback_col1:

            st.metric(
                "Average Ease of Use",
                f"{avg_ease:.1f} / 5"
            )

            st.markdown(
                "#### Rating Distribution"
            )

            for rating in range(
                5,
                0,
                -1
            ):

                stars = (
                    "★"
                    * rating
                    +
                    "☆"
                    * (
                        5 - rating
                    )
                )

                st.write(
                    f"**{stars}** — "
                    f"{rating_counts[rating]} response(s)"
                )

        with feedback_col2:

            st.markdown(
                "#### Recommendation"
            )

            recommend_counts = {
                "Yes": 0,
                "Maybe": 0,
                "No": 0
            }

            for row in feedback_rows:

                answer = str(
                    row.get(
                        "would_recommend",
                        ""
                    )
                ).strip()

                if answer in recommend_counts:

                    recommend_counts[
                        answer
                    ] += 1

            for answer, count in recommend_counts.items():

                st.write(
                    f"**{answer}:** {count}"
                )

        st.divider()

        # ----------------------------------------------------
        # POPULAR FEATURES
        # ----------------------------------------------------

        st.header(
            "Most Useful Features"
        )

        feature_counts = {}

        for row in feedback_rows:

            features = text_to_list(
                row.get(
                    "favorite_features"
                )
            )

            for feature in features:

                feature_counts[
                    feature
                ] = (
                    feature_counts.get(
                        feature,
                        0
                    )
                    + 1
                )

        if feature_counts:

            feature_rankings = sorted(
                feature_counts.items(),
                key=lambda item:
                    item[1],
                reverse=True
            )

            for rank, (
                feature,
                count
            ) in enumerate(
                feature_rankings,
                start=1
            ):

                st.write(
                    f"**#{rank} {feature}** — "
                    f"{count} vote(s)"
                )

        else:

            st.info(
                "Users have not selected favorite features yet."
            )

        st.divider()

        # ----------------------------------------------------
        # WRITTEN FEEDBACK
        # ----------------------------------------------------

        st.header(
            "Recent Written Feedback"
        )

        sorted_feedback = sorted(
            feedback_rows,
            key=lambda row:
                str(
                    row.get(
                        "updated_at",
                        row.get(
                            "created_at",
                            ""
                        )
                    )
                ),
            reverse=True
        )

        for row in sorted_feedback[:20]:

            rating = int(
                row.get(
                    "rating",
                    0
                )
                or 0
            )

            stars = (
                "★"
                * rating
                +
                "☆"
                * (
                    5 - rating
                )
            )

            with st.container(
                border=True
            ):

                feedback_top1, feedback_top2 = (
                    st.columns(2)
                )

                with feedback_top1:

                    st.write(
                        f"**Rating:** {stars}"
                    )

                with feedback_top2:

                    st.write(
                        f"**Recommend:** "
                        f"{row.get('would_recommend', 'Not answered')}"
                    )

                improvement_text = str(
                    row.get(
                        "improvements",
                        ""
                    )
                    or
                    ""
                ).strip()

                comments_text = str(
                    row.get(
                        "additional_comments",
                        ""
                    )
                    or
                    ""
                ).strip()

                if improvement_text:

                    st.markdown(
                        "**What should improve**"
                    )

                    st.write(
                        improvement_text
                    )

                if comments_text:

                    st.markdown(
                        "**Additional comments**"
                    )

                    st.write(
                        comments_text
                    )

                if (
                    not improvement_text
                    and
                    not comments_text
                ):

                    st.caption(
                        "No written comments submitted."
                    )

    st.divider()

    # --------------------------------------------------------
    # APPLICATION / COLLEGE ACTIVITY
    # --------------------------------------------------------

    st.header(
        "Student Activity"
    )

    application_status_counts = {}

    for row in saved_rows:

        status = str(
            row.get(
                "status",
                "Saved"
            )
        ).strip()

        application_status_counts[
            status
        ] = (
            application_status_counts.get(
                status,
                0
            )
            + 1
        )

    if application_status_counts:

        st.markdown(
            "#### Application Tracker Status"
        )

        for status, count in sorted(
            application_status_counts.items(),
            key=lambda item:
                item[1],
            reverse=True
        ):

            st.write(
                f"**{status}:** {count}"
            )

    else:

        st.info(
            "No saved application activity yet."
        )

    st.divider()

    # --------------------------------------------------------
    # PRIVACY-SAFE EXPORT VIEW
    # --------------------------------------------------------

    with st.expander(
        "View feedback data"
    ):

        if feedback_rows:

            feedback_df = pd.DataFrame(
                feedback_rows
            )

            safe_columns = [
                column
                for column in [
                    "rating",
                    "ease_of_use",
                    "overall_feeling",
                    "favorite_features",
                    "improvements",
                    "additional_comments",
                    "would_recommend",
                    "created_at",
                    "updated_at"
                ]
                if column
                in feedback_df.columns
            ]

            st.dataframe(
                feedback_df[
                    safe_columns
                ],
                use_container_width=True,
                hide_index=True
            )

            csv_export = (
                feedback_df[
                    safe_columns
                ]
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                )
            )

            st.download_button(
                "Download Feedback CSV",
                data=csv_export,
                file_name="stem_pathways_feedback.csv",
                mime="text/csv",
                use_container_width=True
            )

        else:

            st.write(
                "No feedback data available."
            )

    st.caption(
        "Admin dashboard data is intended for product improvement and should be handled responsibly."
    )





# ============================================================
# FEEDBACK
# ============================================================

elif page == "Feedback":

    st.title(
        "Share Your Feedback"
    )

    st.write(
        "Help improve STEM Pathways NYC by telling us what worked, "
        "what felt confusing, and what you would like to see next."
    )

    st.info(
        "Your feedback is used to improve the platform. "
        "You can return and update your response later."
    )

    st.divider()

    existing_feedback = load_user_feedback(
        user_sub
    ) or {}

    # --------------------------------------------------------
    # STAR RATING
    # --------------------------------------------------------

    st.header(
        "Overall Experience"
    )

    rating_options = {
        "★☆☆☆☆  1 — Poor": 1,
        "★★☆☆☆  2 — Fair": 2,
        "★★★☆☆  3 — Good": 3,
        "★★★★☆  4 — Very Good": 4,
        "★★★★★  5 — Excellent": 5
    }

    existing_rating = int(
        existing_feedback.get(
            "rating",
            5
        )
        or 5
    )

    default_rating_label = next(
        (
            label
            for label, value
            in rating_options.items()
            if value
            ==
            existing_rating
        ),
        "★★★★★  5 — Excellent"
    )

    rating_label = st.radio(
        "How would you rate STEM Pathways NYC overall?",
        list(
            rating_options.keys()
        ),
        index=list(
            rating_options.keys()
        ).index(
            default_rating_label
        ),
        key="feedback_rating"
    )

    rating = rating_options[
        rating_label
    ]

    st.metric(
        "Your Rating",
        "★" * rating
        +
        "☆" * (
            5 - rating
        )
    )

    # --------------------------------------------------------
    # EASE OF USE / FEELING
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        existing_ease = int(
            existing_feedback.get(
                "ease_of_use",
                4
            )
            or 4
        )

        ease_of_use = st.slider(
            "How easy is the website to use?",
            1,
            5,
            existing_ease,
            help=(
                "1 = very difficult to navigate, "
                "5 = very easy to navigate"
            ),
            key="feedback_ease"
        )

    with col2:

        feeling_options = [
            "I really like it",
            "I like it",
            "It's okay",
            "I'm unsure about it",
            "I don't like it yet"
        ]

        saved_feeling = (
            existing_feedback.get(
                "overall_feeling",
                "I really like it"
            )
            or
            "I really like it"
        )

        overall_feeling = st.selectbox(
            "How do you feel about the website overall?",
            feeling_options,
            index=(
                feeling_options.index(
                    saved_feeling
                )
                if saved_feeling
                in feeling_options
                else 0
            ),
            key="feedback_feeling"
        )

    st.divider()

    # --------------------------------------------------------
    # FAVORITE FEATURES
    # --------------------------------------------------------

    st.header(
        "What Is Working?"
    )

    feature_options = [
        "Dashboard",
        "My STEM Pathway",
        "Career recommendations",
        "Salary information",
        "Opportunities",
        "Deadline Calendar",
        "College Suggestions",
        "College match scores",
        "Favorite Colleges",
        "Application Tracker",
        "Project Explorer",
        "GPA Calculator",
        "Resources",
        "Profile"
    ]

    saved_features = text_to_list(
        existing_feedback.get(
            "favorite_features"
        )
    )

    favorite_features = st.multiselect(
        "Which parts of STEM Pathways NYC have been most useful to you?",
        feature_options,
        default=[
            feature
            for feature
            in saved_features
            if feature
            in feature_options
        ],
        key="feedback_features"
    )

    st.divider()

    # --------------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------------

    st.header(
        "What Should We Improve?"
    )

    improvements = st.text_area(
        "What felt confusing, difficult, missing, or could be better?",
        value=(
            existing_feedback.get(
                "improvements",
                ""
            )
            or
            ""
        ),
        placeholder=(
            "Example: I want more filters for colleges, "
            "the sidebar feels crowded, or I want more beginner projects..."
        ),
        height=140,
        key="feedback_improvements"
    )

    additional_comments = st.text_area(
        "Anything else you want us to know? (optional)",
        value=(
            existing_feedback.get(
                "additional_comments",
                ""
            )
            or
            ""
        ),
        placeholder=(
            "Share ideas, feature requests, or anything you liked."
        ),
        height=120,
        key="feedback_comments"
    )

    recommend_options = [
        "Yes",
        "Maybe",
        "No"
    ]

    saved_recommend = (
        existing_feedback.get(
            "would_recommend",
            "Yes"
        )
        or
        "Yes"
    )

    would_recommend = st.radio(
        "Would you recommend STEM Pathways NYC to another student?",
        recommend_options,
        index=(
            recommend_options.index(
                saved_recommend
            )
            if saved_recommend
            in recommend_options
            else 0
        ),
        horizontal=True,
        key="feedback_recommend"
    )

    st.divider()

    if st.button(
        "Submit Feedback",
        type="primary",
        use_container_width=True
    ):

        feedback_payload = {
            "rating":
                rating,

            "ease_of_use":
                ease_of_use,

            "overall_feeling":
                overall_feeling,

            "favorite_features":
                favorite_features,

            "improvements":
                improvements.strip(),

            "additional_comments":
                additional_comments.strip(),

            "would_recommend":
                would_recommend
        }

        if save_user_feedback(
            user_sub,
            user_email,
            feedback_payload
        ):

            st.success(
                "Thank you — your feedback has been saved."
            )

            st.balloons()

    if existing_feedback:

        st.caption(
            "You have already submitted feedback before. "
            "Submitting again will update your existing response."
        )





# ============================================================
# PROFILE
# ============================================================

elif page == "My Profile":

    st.title(
        "My Profile"
    )

    st.subheader(
        full_name
    )

    st.caption(
        "STEM Explorer Profile"
    )

    st.success(
        "Your profile is saved to your account."
    )

    st.divider()

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Age",
            profile["age"]
        )

    with col2:

        st.metric(
            "Grade",
            profile["grade"]
        )

    with col3:

        st.metric(
            "Borough",
            profile["borough"]
        )

    with col4:

        st.metric(
            "Confidence",
            f"{profile['confidence']}/10"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        with st.container(
            border=True
        ):

            st.header(
                "STEM Interests"
            )

            for interest in (
                profile["interests"]
            ):

                st.write(
                    f"• {interest}"
                )

        with st.container(
            border=True
        ):

            st.header(
                "Previous Experience"
            )

            if profile[
                "experience_areas"
            ]:

                for experience in (
                    profile[
                        "experience_areas"
                    ]
                ):

                    st.write(
                        f"• {experience}"
                    )

            else:

                st.write(
                    "No previous STEM experience selected."
                )

    with col2:

        with st.container(
            border=True
        ):

            st.header(
                "Goals"
            )

            for goal in (
                profile["goals"]
            ):

                st.write(
                    f"• {goal}"
                )

        with st.container(
            border=True
        ):

            st.header(
                "Current Exploration Stage"
            )

            st.write(
                profile[
                    "exploration_stage"
                ]
            )

            st.write(
                f"**Weekly STEM goal:** "
                f"{profile['weekly_time']}"
            )

            if profile[
                "financial_support"
            ]:

                st.write(
                    "**Opportunity preference:** "
                    "Prioritize free or financially supported programs"
                )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Edit My Profile",
            use_container_width=True
        ):

            st.session_state.profile_completed = (
                False
            )

            st.rerun()

    with col2:

        if st.button(
            "Sign Out",
            use_container_width=True
        ):

            st.logout()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "STEM Pathways NYC • Explore • Build • Discover"
)
