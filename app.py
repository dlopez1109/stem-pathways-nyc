import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="STEM Pathways NYC",
    page_icon="🚀",
    layout="centered"
)

# Load opportunity database
opportunities = pd.read_csv("data/opportunities.csv")

# Header
st.title("🚀 STEM Pathways NYC")

st.write(
    "Find STEM programs and opportunities that match your "
    "interests, experience, and goals."
)

st.divider()

# Student questionnaire
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
        "AI",
        "Biology",
        "Biomedical Engineering"
    ]
)

experience = st.selectbox(
    "What is your experience level?",
    ["Beginner", "Intermediate", "Advanced"]
)

needs_free = st.checkbox(
    "I am looking for free opportunities"
)


# Matching algorithm
def calculate_match(opportunity):

    score = 0

    grades = str(opportunity["grades"]).split(";")
    fields = str(opportunity["fields"]).split(";")

    if grade in grades:
        score += 25

    if location.lower() == str(opportunity["location"]).lower():
        score += 20

    if any(interest in fields for interest in interests):
        score += 25

    if experience.lower() == str(
        opportunity["experience_level"]
    ).lower():
        score += 15

    if needs_free and str(opportunity["cost"]).lower() == "free":
        score += 15

    return score


# Recommendation button
if st.button("Find My Opportunities", type="primary"):

    if not interests:

        st.warning("Please select at least one STEM interest.")

    else:

        results = []

        for _, opportunity in opportunities.iterrows():

            score = calculate_match(opportunity)

            results.append({
                "name": opportunity["name"],
                "score": score,
                "fields": opportunity["fields"],
                "cost": opportunity["cost"],
                "deadline": opportunity["deadline"],
                "url": opportunity["url"]
            })

        # Highest match first
        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        st.divider()

        st.header("🎯 Your Top Matches")

        for result in results:

            st.subheader(
                f'{result["name"]} — {result["score"]}% Match'
            )

            st.write(f'**Fields:** {result["fields"]}')
            st.write(f'**Cost:** {result["cost"]}')
            st.write(f'**Deadline:** {result["deadline"]}')

            st.link_button(
                "View Opportunity",
                result["url"]
            )

            st.divider()
