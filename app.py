import streamlit as st
import pandas as pd


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="STEM Pathways NYC",
    page_icon="🚀",
    layout="centered"
)

opportunities = pd.read_csv("data/opportunities.csv")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🚀 STEM Pathways NYC")

st.write(
    "Helping NYC high school students discover STEM programs, "
    "projects, research, mentorship, and learning opportunities."
)

st.info(
    "STEM Pathways NYC is currently being developed with a focus "
    "on expanding STEM access for students in the Bronx."
)

st.divider()


# --------------------------------------------------
# STUDENT PROFILE
# --------------------------------------------------

st.header("Build Your STEM Pathway")

grade = st.selectbox(
    "What grade are you in?",
    ["9", "10", "11", "12"]
)

borough = st.selectbox(
    "What borough do you live in?",
    [
        "Bronx",
        "Manhattan",
        "Brooklyn",
        "Queens",
        "Staten Island"
    ]
)

interests = st.multiselect(
    "What STEM fields interest you?",
    [
        "Engineering",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Computer Science",
        "AI",
        "Data Science",
        "Biomedical Engineering",
        "Biology",
        "Physics",
        "Mathematics"
    ]
)

opportunity_types = st.multiselect(
    "What types of opportunities are you looking for?",
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
    "How much STEM experience do you currently have?",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

needs_financial_support = st.checkbox(
    "I prefer free opportunities or programs with financial aid"
)


# --------------------------------------------------
# ELIGIBILITY CHECK
# --------------------------------------------------

def is_eligible(opportunity):

    grades = [
        item.strip()
        for item in str(opportunity["grades"]).split(";")
    ]

    boroughs = [
        item.strip()
        for item in str(opportunity["boroughs_served"]).split(";")
    ]

    if grade not in grades:
        return False

    if borough not in boroughs:
        return False

    return True


# --------------------------------------------------
# MATCHING ALGORITHM
# --------------------------------------------------

def calculate_match(opportunity):

    score = 0
    max_score = 0
    reasons = []

    fields = [
        item.strip()
        for item in str(opportunity["fields"]).split(";")
    ]

    boroughs = [
        item.strip()
        for item in str(opportunity["boroughs_served"]).split(";")
    ]

    # Interest match
    max_score += 35

    matching_interests = [
        interest
        for interest in interests
        if interest in fields
    ]

    if matching_interests:
        score += 35

        reasons.append(
            "Your STEM interests match this opportunity."
        )

    # Opportunity type
    if opportunity_types:

        max_score += 20

        if (
            str(opportunity["opportunity_type"])
            in opportunity_types
        ):
            score += 20

            reasons.append(
                "This matches the type of opportunity you are looking for."
            )

    # Experience level
    max_score += 15

    if (
        experience.lower()
        == str(opportunity["experience_level"]).lower()
    ):
        score += 15

        reasons.append(
            "The experience level matches your current background."
        )

    # Financial accessibility
    if needs_financial_support:

        max_score += 15

        cost = str(opportunity["cost"]).lower()
        aid = str(opportunity["financial_aid"]).lower()

        if cost == "free" or aid == "available":

            score += 15

            reasons.append(
                "This opportunity is free or offers financial support."
            )

    # Borough match
    max_score += 10

    if borough in boroughs:

        score += 10

        reasons.append(
            f"This opportunity serves students in {borough}."
        )

    # Bronx priority
    if borough == "Bronx":

        max_score += 5

        if (
            str(opportunity["bronx_priority"]).lower()
            == "yes"
        ):
            score += 5

            reasons.append(
                "This opportunity specifically prioritizes Bronx students."
            )

    if max_score == 0:
        return 0, reasons

    percentage = round(
        (score / max_score) * 100
    )

    return percentage, reasons


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

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

            if not is_eligible(opportunity):
                continue

            score, reasons = calculate_match(
                opportunity
            )

            results.append({

                "name":
                    opportunity["name"],

                "organization":
                    opportunity["organization"],

                "score":
                    score,

                "fields":
                    opportunity["fields"],

                "type":
                    opportunity["opportunity_type"],

                "cost":
                    opportunity["cost"],

                "financial_aid":
                    opportunity["financial_aid"],

                "experience":
                    opportunity["experience_level"],

                "status":
                    opportunity["application_status"],

                "description":
                    opportunity["description"],

                "url":
                    opportunity["url"],

                "reasons":
                    reasons
            })

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        st.divider()

        st.header("🎯 Your Top STEM Matches")

        if not results:

            st.info(
                "We do not have an eligible opportunity "
                "for your profile yet. More opportunities "
                "will be added as the STEM Pathways NYC "
                "database grows."
            )

        else:

            for result in results:

                st.subheader(
                    result["name"]
                )

                st.caption(
                    result["organization"]
                )

                st.metric(
                    "Match Score",
                    f'{result["score"]}%'
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
                    f'**Experience Level:** '
                    f'{result["experience"]}'
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

                st.markdown(
                    "#### Why this matches you"
                )

                for reason in result["reasons"]:
                    st.write(
                        f"✅ {reason}"
                    )

                st.link_button(
                    "View Opportunity",
                    result["url"]
                )

                st.divider()


# --------------------------------------------------
# BRONX SECTION
# --------------------------------------------------

st.header("🏙️ Built With Bronx Students in Mind")

st.write(
    "STEM Pathways NYC aims to make it easier for students "
    "in the Bronx and throughout New York City to discover "
    "STEM opportunities that may otherwise be difficult to find."
)

st.write(
    "As the platform grows, it will include more local programs, "
    "research opportunities, mentorship, college courses, "
    "internships, competitions, and student engineering projects."
)

st.divider()

st.caption(
    "STEM Pathways NYC • Student-built STEM access platform"
)
