import streamlit as st
import pandas as pd
import json
from datetime import datetime, timezone
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="STEM Pathways NYC",xa
    page_icon="🧭",
    layout="wide"
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
        "MAIN"
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
        "EXPLORE"
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
        "🎓 College Suggestions",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "College Suggestions"
        )

        st.rerun()

    if st.button(
        "⭐ My Favorite Colleges",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "My Favorite Colleges"
        )

        st.rerun()

    if st.button(
        "🛠️ Projects",
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

    if st.button(
        "📌 My Applications",
        use_container_width=True
    ):

        st.session_state.current_page = (
            "My Applications"
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

    st.divider()

    st.caption(
        "Explore • Build • Discover"
    )


page = st.session_state.current_page


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title(
        f"Welcome, {profile['first_name']} 👋"
    )

    st.write(
        "Your personalized STEM dashboard brings together your "
        "interests, pathway, careers, projects, and opportunities."
    )

    st.divider()

    # --------------------------------------------------------
    # SNAPSHOT
    # --------------------------------------------------------

    st.header(
        "Your STEM Snapshot"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Grade",
            profile["grade"]
        )

    with col2:

        st.metric(
            "Borough",
            profile["borough"]
        )

    with col3:

        st.metric(
            "Interest Confidence",
            f"{profile['confidence']}/10"
        )

    with col4:

        st.metric(
            "Weekly Goal",
            profile["weekly_time"]
        )

    st.divider()

    # --------------------------------------------------------
    # CURRENT DIRECTION
    # --------------------------------------------------------

    primary_interest = (
        profile["interests"][0]
    )

    st.header(
        "Your Current Direction"
    )

    with st.container(
        border=True
    ):

        st.subheader(
            primary_interest
        )

        st.write(
            "This is currently your primary STEM interest. "
            "Your pathway can evolve as you gain new experiences."
        )

        st.write(
            f"**Exploration stage:** "
            f"{profile['exploration_stage']}"
        )

    st.divider()

    # --------------------------------------------------------
    # NEXT STEPS
    # --------------------------------------------------------

    st.header(
        "Your Next Steps"
    )

    st.write(
        "Choose where you want to continue exploring."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(
            border=True
        ):

            st.subheader(
                "🧭 Explore Your Pathway"
            )

            st.write(
                "Discover majors, careers, salary data, skills, "
                "and possible directions."
            )

            if st.button(
                "Open My Pathway",
                key="dashboard_pathway",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "My STEM Pathway"
                )

                st.rerun()

    with col2:

        with st.container(
            border=True
        ):

            st.subheader(
                "🛠️ Build a Project"
            )

            st.write(
                "Turn your interests into hands-on experience "
                "through projects."
            )

            if st.button(
                "Explore Projects",
                key="dashboard_projects",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "Projects"
                )

                st.rerun()

    with col3:

        with st.container(
            border=True
        ):

            st.subheader(
                "💼 Find Opportunities"
            )

            st.write(
                "Discover programs, research, internships, courses, "
                "competitions, and scholarships."
            )

            if st.button(
                "Explore Opportunities",
                key="dashboard_opportunities",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "Opportunities"
                )

                st.rerun()

    # --------------------------------------------------------
    # YOUR STEM INTERESTS - IMPROVED
    # --------------------------------------------------------

    st.divider()

    st.header(
        "Your STEM Interests"
    )

    st.write(
        "Explore the fields you selected when creating your profile. "
        "Each field includes skills and majors you can investigate next."
    )

    interest_info = {

        "Engineering": {
            "description":
                "Design systems, products, and solutions to real-world problems.",

            "skills": [
                "Engineering design",
                "CAD",
                "Prototyping",
                "Data analysis"
            ],

            "majors": [
                "Mechanical Engineering",
                "Electrical Engineering",
                "Industrial Engineering"
            ]
        },

        "Electrical Engineering": {
            "description":
                "Explore circuits, electronics, power systems, signals, and hardware.",

            "skills": [
                "Circuit design",
                "Electronics",
                "Digital logic",
                "Arduino"
            ],

            "majors": [
                "Electrical Engineering",
                "Computer Engineering",
                "Electrical & Computer Engineering"
            ]
        },

        "Mechanical Engineering": {
            "description":
                "Design machines, products, mechanisms, and physical systems.",

            "skills": [
                "CAD",
                "Mechanics",
                "3D printing",
                "Prototyping"
            ],

            "majors": [
                "Mechanical Engineering",
                "Aerospace Engineering",
                "Mechatronics"
            ]
        },

        "Computer Engineering": {
            "description":
                "Combine computer hardware, electronics, and programming.",

            "skills": [
                "Digital logic",
                "Circuit design",
                "C / C++",
                "Embedded systems"
            ],

            "majors": [
                "Computer Engineering",
                "Electrical Engineering",
                "Computer Science"
            ]
        },

        "Computer Science": {
            "description":
                "Build software, algorithms, applications, and computing systems.",

            "skills": [
                "Python",
                "Algorithms",
                "Data structures",
                "Git & GitHub"
            ],

            "majors": [
                "Computer Science",
                "Software Engineering",
                "Cybersecurity"
            ]
        },

        "Artificial Intelligence": {
            "description":
                "Create systems that learn from data and make intelligent decisions.",

            "skills": [
                "Python",
                "Machine learning",
                "Statistics",
                "Data analysis"
            ],

            "majors": [
                "Computer Science",
                "Artificial Intelligence",
                "Data Science"
            ]
        },

        "Data Science": {
            "description":
                "Use data, statistics, and programming to solve real-world problems.",

            "skills": [
                "Python",
                "Pandas",
                "Statistics",
                "SQL"
            ],

            "majors": [
                "Data Science",
                "Statistics",
                "Applied Mathematics"
            ]
        },

        "Biomedical Engineering": {
            "description":
                "Use engineering to solve problems in medicine, healthcare, and biology.",

            "skills": [
                "Biology",
                "Engineering design",
                "CAD",
                "Biomechanics"
            ],

            "majors": [
                "Biomedical Engineering",
                "Bioengineering",
                "Mechanical Engineering"
            ]
        },

        "Biology": {
            "description":
                "Study living organisms, biological systems, and scientific research.",

            "skills": [
                "Experimental design",
                "Laboratory skills",
                "Data analysis",
                "Scientific writing"
            ],

            "majors": [
                "Biology",
                "Biochemistry",
                "Biotechnology"
            ]
        },

        "Physics": {
            "description":
                "Study matter, energy, forces, motion, and the physical universe.",

            "skills": [
                "Calculus",
                "Mechanics",
                "Programming",
                "Mathematical modeling"
            ],

            "majors": [
                "Physics",
                "Applied Physics",
                "Engineering Physics"
            ]
        },

        "Mathematics": {
            "description":
                "Use mathematical reasoning and models to understand complex problems.",

            "skills": [
                "Calculus",
                "Statistics",
                "Probability",
                "Mathematical modeling"
            ],

            "majors": [
                "Mathematics",
                "Applied Mathematics",
                "Statistics"
            ]
        },

        "Environmental Science": {
            "description":
                "Study environmental systems and develop solutions to environmental challenges.",

            "skills": [
                "Environmental analysis",
                "GIS",
                "Statistics",
                "Data collection"
            ],

            "majors": [
                "Environmental Science",
                "Environmental Engineering",
                "Earth Science"
            ]
        },

        "Robotics": {
            "description":
                "Combine mechanics, electronics, programming, and automation.",

            "skills": [
                "Robotics",
                "Arduino",
                "Sensors",
                "Control systems"
            ],

            "majors": [
                "Robotics Engineering",
                "Mechanical Engineering",
                "Computer Engineering"
            ]
        },

        "Not sure yet": {
            "description":
                "Explore several STEM areas before deciding which directions interest you most.",

            "skills": [
                "Try coding",
                "Build a beginner project",
                "Explore research",
                "Compare STEM fields"
            ],

            "majors": [
                "Explore multiple majors",
                "Try introductory courses",
                "Use the Career Explorer"
            ]
        }
    }

    interest_columns = st.columns(2)

    for index, interest in enumerate(
        profile["interests"]
    ):

        info = interest_info.get(
            interest,
            {
                "description":
                    "Explore this STEM field and discover possible skills and careers.",

                "skills": [],

                "majors": []
            }
        )

        with interest_columns[
            index % 2
        ]:

            with st.container(
                border=True
            ):

                st.subheader(
                    interest
                )

                st.write(
                    info["description"]
                )

                left_col, right_col = st.columns(2)

                with left_col:

                    st.markdown(
                        "**Skills to Build**"
                    )

                    for skill in info["skills"]:

                        st.write(
                            f"• {skill}"
                        )

                with right_col:

                    st.markdown(
                        "**Majors to Explore**"
                    )

                    for major in info["majors"]:

                        st.write(
                            f"• {major}"
                        )

                if st.button(
                    f"Explore {interest}",
                    key=f"interest_{index}",
                    use_container_width=True
                ):

                    st.session_state.current_page = (
                        "My STEM Pathway"
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
                        "⭐ Add to Favorites",
                        key=f"favorite_college_{college['name']}",
                        use_container_width=True
                    ):

                        if add_favorite_college(
                            user_sub,
                            college["name"]
                        ):

                            st.success(
                                "Added to My Favorite Colleges."
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
        "Build your own college list and arrange schools in the "
        "order you personally like them."
    )

    st.info(
        "Your ranking is your personal preference list. "
        "It does not represent an admissions ranking."
    )

    st.divider()

    favorite_colleges = load_favorite_colleges(
        user_sub
    )

    if not favorite_colleges:

        st.header(
            "Your favorites list is empty"
        )

        st.write(
            "Go to **College Suggestions** and click "
            "**⭐ Add to Favorites** on schools you want to remember."
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

                with rank_col:

                    st.metric(
                        "Your Rank",
                        f"#{index}"
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
            "Tip: Your favorite list can change as you learn more. "
            "Move schools whenever your priorities change."
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

    st.title(
        "Projects"
    )

    st.write(
        "Build hands-on projects that help you explore your "
        "interests and develop real technical skills."
    )

    st.divider()

    project_library = {

        "Engineering": [
            (
                "Beginner",
                "Identify a community problem and design a possible solution."
            ),
            (
                "Intermediate",
                "Create and test a physical prototype."
            ),
            (
                "Advanced",
                "Build and document a complete engineering system."
            )
        ],

        "Electrical Engineering": [
            (
                "Beginner",
                "Build and test an LED circuit."
            ),
            (
                "Intermediate",
                "Create an Arduino environmental sensor."
            ),
            (
                "Advanced",
                "Design an embedded monitoring system."
            )
        ],

        "Mechanical Engineering": [
            (
                "Beginner",
                "Model an object using CAD."
            ),
            (
                "Intermediate",
                "Design and 3D print a mechanical prototype."
            ),
            (
                "Advanced",
                "Design and test a functional mechanical system."
            )
        ],

        "Computer Engineering": [
            (
                "Beginner",
                "Build a digital logic circuit."
            ),
            (
                "Intermediate",
                "Create a hardware/software sensor system."
            ),
            (
                "Advanced",
                "Build a small embedded system."
            )
        ],

        "Computer Science": [
            (
                "Beginner",
                "Build a Python application."
            ),
            (
                "Intermediate",
                "Create an interactive web application."
            ),
            (
                "Advanced",
                "Build a full-stack application with a database."
            )
        ],

        "Artificial Intelligence": [
            (
                "Beginner",
                "Explore and visualize a real dataset."
            ),
            (
                "Intermediate",
                "Build a simple machine-learning model."
            ),
            (
                "Advanced",
                "Build and evaluate a recommendation system."
            )
        ],

        "Data Science": [
            (
                "Beginner",
                "Analyze an NYC public dataset."
            ),
            (
                "Intermediate",
                "Build an interactive data dashboard."
            ),
            (
                "Advanced",
                "Create a predictive analysis project."
            )
        ],

        "Biomedical Engineering": [
            (
                "Beginner",
                "Research a healthcare problem and design an engineering solution."
            ),
            (
                "Intermediate",
                "Create an assistive-device prototype."
            ),
            (
                "Advanced",
                "Design and evaluate a medical technology concept."
            )
        ],

        "Biology": [
            (
                "Beginner",
                "Investigate a biological question using scientific data."
            ),
            (
                "Intermediate",
                "Design a controlled experiment."
            ),
            (
                "Advanced",
                "Complete an independent research project."
            )
        ],

        "Physics": [
            (
                "Beginner",
                "Create a motion or energy simulation."
            ),
            (
                "Intermediate",
                "Model a physical system using Python."
            ),
            (
                "Advanced",
                "Build and analyze a physics-based engineering project."
            )
        ],

        "Mathematics": [
            (
                "Beginner",
                "Use mathematics to model a real-world problem."
            ),
            (
                "Intermediate",
                "Build a probability or optimization model."
            ),
            (
                "Advanced",
                "Create a mathematical analysis using real data."
            )
        ],

        "Environmental Science": [
            (
                "Beginner",
                "Analyze an environmental issue affecting NYC."
            ),
            (
                "Intermediate",
                "Create an environmental data dashboard."
            ),
            (
                "Advanced",
                "Develop a data-driven environmental solution."
            )
        ],

        "Robotics": [
            (
                "Beginner",
                "Design a robotic mechanism."
            ),
            (
                "Intermediate",
                "Build a sensor-controlled device."
            ),
            (
                "Advanced",
                "Create an autonomous robotic system."
            )
        ]
    }

    shown_projects = False

    for interest in profile[
        "interests"
    ]:

        if interest in project_library:

            shown_projects = True

            st.header(
                interest
            )

            project_columns = st.columns(3)

            for index, (
                level,
                project
            ) in enumerate(
                project_library[
                    interest
                ]
            ):

                with project_columns[
                    index % 3
                ]:

                    with st.container(
                        border=True
                    ):

                        st.caption(
                            level
                        )

                        st.subheader(
                            project
                        )

    if not shown_projects:

        st.info(
            "More project recommendations for your interests will be added."
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
