import streamlit as st
import pandas as pd


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="STEM Pathways NYC",
    page_icon="🧭",
    layout="centered"
)

opportunities = pd.read_csv("data/opportunities.csv")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "profile_completed" not in st.session_state:
    st.session_state.profile_completed = False

if "student_profile" not in st.session_state:
    st.session_state.student_profile = {}


# --------------------------------------------------
# WELCOME + QUESTIONNAIRE
# --------------------------------------------------

if not st.session_state.profile_completed:

    st.title("STEM Pathways NYC")

    st.subheader(
        "Discover where your STEM interests can take you."
    )

    st.write(
        "STEM Pathways NYC helps high school students explore STEM fields, "
        "develop technical skills, discover projects, and find opportunities "
        "that match their interests and goals."
    )

    st.info(
        "Start by completing your STEM Explorer Profile. "
        "Your responses will help personalize your pathway."
    )

    st.divider()

    st.header("Create Your STEM Explorer Profile")

    st.write(
        "There are no right or wrong answers. "
        "This is designed to understand what you want to explore."
    )

    name = st.text_input(
        "First name"
    )

    grade = st.selectbox(
        "What grade are you in?",
        [
            "9",
            "10",
            "11",
            "12"
        ]
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
        "Which STEM fields currently interest you?",
        [
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
    )

    experience_areas = st.multiselect(
        "What STEM activities have you tried before?",
        [
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
    )

    goals = st.multiselect(
        "What would you like to do next?",
        [
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
    )

    exploration_stage = st.radio(
        "Which statement describes you best?",
        [
            "I am just starting to explore STEM.",
            "I have a few STEM interests but I am still exploring.",
            "I know which STEM fields interest me.",
            "I have experience and want to develop more advanced skills.",
            "I already have a specific STEM career or major in mind."
        ]
    )

    confidence = st.slider(
        "How confident are you about your current STEM interests?",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Still figuring it out, 5 = Very confident"
    )

    weekly_time = st.selectbox(
        "How much time would you realistically like to spend exploring STEM each week?",
        [
            "Less than 2 hours",
            "2–5 hours",
            "5–10 hours",
            "10+ hours"
        ]
    )

    financial_support = st.checkbox(
        "I would like free opportunities or programs that offer financial aid"
    )

    st.divider()

    if st.button(
        "Create My STEM Profile",
        type="primary",
        use_container_width=True
    ):

        if not name.strip():

            st.warning(
                "Please enter your first name."
            )

        elif not interests:

            st.warning(
                "Please select at least one STEM interest."
            )

        elif not goals:

            st.warning(
                "Please select at least one goal."
            )

        else:

            st.session_state.student_profile = {
                "name": name.strip(),
                "grade": grade,
                "borough": borough,
                "interests": interests,
                "experience_areas": experience_areas,
                "goals": goals,
                "exploration_stage": exploration_stage,
                "confidence": confidence,
                "weekly_time": weekly_time,
                "financial_support": financial_support
            }

            st.session_state.profile_completed = True

            st.rerun()


# --------------------------------------------------
# PERSONALIZED PLATFORM
# --------------------------------------------------

else:

    profile = st.session_state.student_profile

    st.title(
        f"Welcome, {profile['name']} 👋"
    )

    st.write(
        "Your STEM pathway begins with exploration. "
        "Use your profile to discover fields, skills, projects, "
        "and opportunities that can help you keep progressing."
    )

    st.divider()


    # --------------------------------------------------
    # PROFILE SUMMARY
    # --------------------------------------------------

    st.header("Your STEM Explorer Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Grade",
            profile["grade"]
        )

        st.metric(
            "Borough",
            profile["borough"]
        )

    with col2:

        st.metric(
            "Interest Confidence",
            f"{profile['confidence']}/5"
        )

        st.metric(
            "Weekly Exploration",
            profile["weekly_time"]
        )

    st.write("### Current STEM Interests")

    for interest in profile["interests"]:
        st.write(
            f"• {interest}"
        )

    st.write("### Your Goals")

    for goal in profile["goals"]:
        st.write(
            f"• {goal}"
        )

    st.write("### Exploration Stage")

    st.write(
        profile["exploration_stage"]
    )

    st.divider()


    # --------------------------------------------------
    # STARTING PATHWAY
    # --------------------------------------------------

    st.header("Your Starting Pathway")

    primary_interest = profile["interests"][0]

    pathway_data = {

        "Electrical Engineering": {
            "skill": "Circuit fundamentals",
            "project": "Build a simple environmental sensor",
            "explore": "Embedded systems and electronics"
        },

        "Mechanical Engineering": {
            "skill": "CAD and engineering design",
            "project": "Design a mechanical device in CAD",
            "explore": "Product design and robotics"
        },

        "Computer Engineering": {
            "skill": "Python and digital electronics",
            "project": "Build a small hardware + software project",
            "explore": "Embedded systems and computer architecture"
        },

        "Computer Science": {
            "skill": "Python programming",
            "project": "Build your first interactive web application",
            "explore": "Software engineering and algorithms"
        },

        "Artificial Intelligence": {
            "skill": "Python and data analysis",
            "project": "Build a simple prediction model",
            "explore": "Machine learning"
        },

        "Data Science": {
            "skill": "Python and data visualization",
            "project": "Analyze a real NYC dataset",
            "explore": "Statistics and machine learning"
        },

        "Biomedical Engineering": {
            "skill": "Engineering design and biology",
            "project": "Design an assistive technology concept",
            "explore": "Medical devices"
        },

        "Biology": {
            "skill": "Experimental design",
            "project": "Investigate a biological research question",
            "explore": "Biotechnology and research"
        },

        "Physics": {
            "skill": "Mathematical modeling",
            "project": "Build a physics simulation",
            "explore": "Engineering and applied physics"
        },

        "Mathematics": {
            "skill": "Problem solving and mathematical modeling",
            "project": "Use mathematics to model a real-world problem",
            "explore": "Applied mathematics and engineering"
        },

        "Engineering": {
            "skill": "Engineering design process",
            "project": "Identify a problem and prototype a solution",
            "explore": "Different engineering disciplines"
        },

        "Robotics": {
            "skill": "Programming and electronics",
            "project": "Build a simple robotic system",
            "explore": "Mechatronics and automation"
        },

        "Environmental Science": {
            "skill": "Data collection and analysis",
            "project": "Analyze an environmental issue in NYC",
            "explore": "Environmental engineering"
        },

        "Not sure yet": {
            "skill": "Explore multiple STEM disciplines",
            "project": "Complete three small projects from different STEM fields",
            "explore": "Engineering, computing, science, and mathematics"
        }
    }

    pathway = pathway_data.get(
        primary_interest,
        {
            "skill": "Problem solving",
            "project": "Complete a beginner STEM project",
            "explore": "Different STEM disciplines"
        }
    )

    with st.container(border=True):

        st.subheader(
            primary_interest
        )

        st.write(
            f"**Skill to explore next:** {pathway['skill']}"
        )

        st.write(
            f"**Suggested starter project:** {pathway['project']}"
        )

        st.write(
            f"**Area to explore:** {pathway['explore']}"
        )

    st.divider()


    # --------------------------------------------------
    # OPPORTUNITY FINDER
    # --------------------------------------------------

    st.header("Explore Opportunities")

    st.write(
        "Find opportunities based on the information in your STEM profile."
    )

    opportunity_types = st.multiselect(
        "What types of opportunities would you like to explore?",
        [
            "Summer Program",
            "Internship",
            "Research",
            "College Course",
            "Competition",
            "Scholarship"
        ]
    )


    # --------------------------------------------------
    # ELIGIBILITY
    # --------------------------------------------------

    def is_eligible(opportunity):

        eligible_grades = [
            item.strip()
            for item in str(opportunity["grades"]).split(";")
        ]

        boroughs_served = [
            item.strip()
            for item in str(opportunity["boroughs_served"]).split(";")
        ]

        if profile["grade"] not in eligible_grades:
            return False

        if profile["borough"] not in boroughs_served:
            return False

        return True


    # --------------------------------------------------
    # MATCHING
    # --------------------------------------------------

    def calculate_match(opportunity):

        score = 0
        max_score = 0
        reasons = []

        fields = [
            item.strip()
            for item in str(opportunity["fields"]).split(";")
        ]

        boroughs_served = [
            item.strip()
            for item in str(opportunity["boroughs_served"]).split(";")
        ]

        max_score += 40

        if any(
            interest in fields
            for interest in profile["interests"]
        ):

            score += 40

            reasons.append(
                "Your STEM interests align with this opportunity."
            )

        if opportunity_types:

            max_score += 20

            if str(
                opportunity["opportunity_type"]
            ) in opportunity_types:

                score += 20

                reasons.append(
                    "This matches the opportunity type you selected."
                )

        max_score += 15

        if profile["financial_support"]:

            cost = str(
                opportunity["cost"]
            ).lower()

            aid = str(
                opportunity["financial_aid"]
            ).lower()

            if cost == "free" or aid == "available":

                score += 15

                reasons.append(
                    "This opportunity is free or offers financial assistance."
                )

        else:

            score += 15

        max_score += 15

        if profile["borough"] in boroughs_served:

            score += 15

            reasons.append(
                f"This opportunity serves students in the {profile['borough']}."
            )

        if profile["borough"] == "Bronx":

            max_score += 10

            if str(
                opportunity["bronx_priority"]
            ).lower() == "yes":

                score += 10

                reasons.append(
                    "This opportunity has a specific focus on Bronx students."
                )

        percentage = round(
            (score / max_score) * 100
        )

        return percentage, reasons


    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    if st.button(
        "Find Opportunities",
        type="primary",
        use_container_width=True
    ):

        results = []

        for _, opportunity in opportunities.iterrows():

            if not is_eligible(opportunity):
                continue

            score, reasons = calculate_match(
                opportunity
            )

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
                "url": opportunity["url"],
                "reasons": reasons
            })

        results = sorted(
            results,
            key=lambda item: item["score"],
            reverse=True
        )

        st.divider()

        st.header("Recommended Opportunities")

        if not results:

            st.info(
                "No eligible opportunities are currently available "
                "for this profile in our database."
            )

        else:

            for result in results:

                with st.container(border=True):

                    st.subheader(
                        result["name"]
                    )

                    st.caption(
                        result["organization"]
                    )

                    st.metric(
                        "Match",
                        f"{result['score']}%"
                    )

                    st.write(
                        result["description"]
                    )

                    st.write(
                        f"**Type:** {result['type']}"
                    )

                    st.write(
                        f"**STEM Fields:** {result['fields']}"
                    )

                    st.write(
                        f"**Cost:** {result['cost']}"
                    )

                    st.write(
                        f"**Financial Aid:** {result['financial_aid']}"
                    )

                    st.write(
                        f"**Application Status:** {result['status']}"
                    )

                    with st.expander(
                        "Why this opportunity matches"
                    ):

                        for reason in result["reasons"]:

                            st.write(
                                f"• {reason}"
                            )

                    st.link_button(
                        "View Official Opportunity",
                        result["url"],
                        use_container_width=True
                    )


    # --------------------------------------------------
    # PROFILE CONTROLS
    # --------------------------------------------------

    st.divider()

    if st.button(
        "Edit My STEM Profile"
    ):

        st.session_state.profile_completed = False

        st.rerun()


    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    st.divider()

    st.caption(
        "STEM Pathways NYC • Explore • Build • Discover"
    )
