import streamlit as st
import pandas as pd

# -----------------------------
# PAGE SETUP
# -----------------------------

st.set_page_config(
    page_title="STEM Pathways NYC",
    page_icon="🚀",
    layout="centered"
)

# Load database
opportunities = pd.read_csv("data/opportunities.csv")


# -----------------------------
# HEADER
# -----------------------------

st.title("🚀 STEM Pathways NYC")

st.write(
    "Discover STEM programs, internships, research opportunities, "
    "college programs, and more based on your interests and goals."
)

st.divider()


# -----------------------------
# STUDENT PROFILE
# -----------------------------

st.header("Build Your STEM Pathway")

grade = st.selectbox(
    "What grade are you in?",
    ["9", "10", "11", "12"]
)

location = st.selectbox(
    "Where are you located?",
    ["NYC", "Other"]
)

interests = st.multiselect(
    "What STEM fields interest you?",
    [
        "Engineering",
        "Computer Science",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Biomedical Engineering",
        "AI",
        "Data Science",
        "Biology",
        "Physics",
        "Mathematics"
    ]
)

opportunity_types = st.multiselect(
    "What kinds of opportunities are you looking for?",
    [
        "Summer Program",
        "Internship",
        "Research",
        "College Course",
        "Competition",
        "Scholarship",
        "Mentorship"
    ]
)

experience = st.selectbox(
    "What is your experience level?",
    ["Beginner", "Intermediate", "Advanced"]
)

needs_financial_support = st.checkbox(
    "I prefer free programs or programs with financial aid"
)


# -----------------------------
# ELIGIBILITY
# -----------------------------

def is_eligible(opportunity):

    eligible_grades = str(opportunity["grades"]).split(";")

    # Student must be in an eligible grade
    if grade not in eligible_grades:
        return False

    # Location restrictions
    program_location = str(opportunity["location"]).lower()

    if program_location == "nyc" and location.lower() != "nyc":
        return False

    return True


# -----------------------------
# MATCHING ALGORITHM
# -----------------------------

def calculate_match(opportunity):

    score = 0
    maximum_score = 0

    fields = [
        field.strip()
        for field in str(opportunity["fields"]).split(";")
    ]

    # STEM interest match
    maximum_score += 40

    if any(interest in fields for interest in interests):
        score += 40

    # Opportunity type match
    if opportunity_types:

        maximum_score += 25

        if opportunity["opportunity_type"] in opportunity_types:
            score += 25

    # Experience match
    maximum_score += 15

    if (
        experience.lower()
        == str(opportunity["experience_level"]).lower()
    ):
        score += 15

    # Financial accessibility
    if needs_financial_support:

        maximum_score += 20

        cost = str(opportunity["cost"]).lower()
        aid = str(opportunity["financial_aid"]).lower()

        if cost == "free" or aid == "available":
            score += 20

    # Convert score to percentage
    if maximum_score == 0:
        return 0

    percentage = round(
        (score / maximum_score) * 100
    )

    return percentage


# -----------------------------
# RESULTS
# -----------------------------

if st.button(
    "Find My Opportunities",
    type="primary"
):

    if not interests:

        st.warning(
            "Please select at least one STEM interest."
        )

    else:

        results = []

        for _, opportunity in opportunities.iterrows():

            # First check eligibility
            if not is_eligible(opportunity):
                continue

            score = calculate_match(opportunity)

            results.append({
                "name": opportunity["name"],
                "organization": opportunity["organization"],
                "score": score,
                "fields": opportunity["fields"],
                "type": opportunity["opportunity_type"],
                "cost": opportunity["cost"],
                "financial_aid": opportunity["financial_aid"],
                "status": opportunity["application_status"],
                "description": opportunity["description"],
                "url": opportunity["url"]
            })

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        st.divider()

        st.header("🎯 Your Top Matches")

        if not results:

            st.info(
                "No eligible opportunities were found yet. "
                "As the STEM Pathways database grows, "
                "more opportunities will appear here."
            )

        else:

            for result in results:

                st.subheader(
                    f'{result["name"]}'
                )

                st.metric(
                    "Match Score",
                    f'{result["score"]}%'
                )

                st.write(
                    f'**Organization:** '
                    f'{result["organization"]}'
                )

                st.write(
                    f'**Opportunity Type:** '
                    f'{result["type"]}'
                )

                st.write(
                    f'**STEM Fields:** '
                    f'{result["fields"]}'
                )

                st.write(
                    f'**Cost:** '
                    f'{result["cost"]}'
                )

                st.write(
                    f'**Financial Aid:** '
                    f'{result["financial_aid"]}'
                )

                st.write(
                    f'**Application Status:** '
                    f'{result["status"]}'
                )

                st.write(
                    result["description"]
                )

                st.link_button(
                    "View Official Opportunity",
                    result["url"]
                )

                st.divider()
