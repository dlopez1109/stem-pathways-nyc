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
# WELCOME + STEM EXPLORER QUESTIONNAIRE
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
        "Your responses will help personalize your experience."
    )

    st.divider()

    st.header("Create Your STEM Explorer Profile")

    st.write(
        "Tell us about yourself, your interests, and what you hope to explore. "
        "There are no right or wrong answers."
    )

    # --------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------

    st.subheader("About You")

    first_name = st.text_input(
        "First name"
    )

    middle_name = st.text_input(
        "Middle name (optional)"
    )

    last_name = st.text_input(
        "Last name"
    )

    age = st.number_input(
        "Age",
        min_value=13,
        max_value=19,
        value=15,
        step=1
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

    st.divider()

    # --------------------------------------------------
    # STEM INTERESTS
    # --------------------------------------------------

    st.subheader("Your STEM Interests")

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

    st.divider()

    # --------------------------------------------------
    # GOALS
    # --------------------------------------------------

    st.subheader("Your Goals")

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
        max_value=10,
        value=5,
        help="1 = Still exploring, 10 = Very confident in my current interests"
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

    # --------------------------------------------------
    # CREATE PROFILE
    # --------------------------------------------------

    if st.button(
        "Create My STEM Profile",
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
                "Please select at least one STEM interest."
            )

        elif not goals:

            st.warning(
                "Please select at least one goal."
            )

        else:

            st.session_state.student_profile = {
                "first_name": first_name.strip(),
                "middle_name": middle_name.strip(),
                "last_name": last_name.strip(),
                "age": age,
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
# PERSONALIZED STUDENT PLATFORM
# --------------------------------------------------

else:

    profile = st.session_state.student_profile

    # Create full name

    if profile["middle_name"]:

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

    # --------------------------------------------------
    # DASHBOARD HEADER
    # --------------------------------------------------

    st.title(
        f"Welcome, {profile['first_name']} 👋"
    )

    st.write(
        "Your STEM pathway begins with exploration. "
        "Use your profile to discover fields, develop skills, build projects, "
        "and find opportunities that can help you continue progressing."
    )

    st.divider()

    # --------------------------------------------------
    # PROFILE SUMMARY
    # --------------------------------------------------

    st.header("Your STEM Explorer Profile")

    st.subheader(full_name)

    col1, col2, col3 = st.columns(3)

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

    col4, col5 = st.columns(2)

    with col4:

        st.metric(
            "Interest Confidence",
            f"{profile['confidence']}/10"
        )

    with col5:

        st.metric(
            "Weekly Exploration",
            profile["weekly_time"]
        )

    st.write("### Current STEM Interests")

    for interest in profile["interests"]:

        st.write(
            f"• {interest}"
        )

    st.write("### Previous STEM Experience")

    if profile["experience_areas"]:

        for activity in profile["experience_areas"]:

            st.write(
                f"• {activity}"
            )

    else:

        st.write(
            "No previous experience selected."
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
    # STARTING STEM PATHWAY
    # --------------------------------------------------

    st.header("Your Starting STEM Pathway")

    st.write(
        "Based on your current interests, here is one area you can begin "
        "exploring. Your pathway can change as you discover new interests."
    )

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
            "project": "Build a small hardware and software system",
            "explore": "Embedded systems and computer architecture"
        },

        "Computer Science": {
            "skill": "Python programming",
            "project": "Build an interactive web application",
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
            "explore": "Biotechnology and scientific research"
        },

        "Physics": {
            "skill": "Mathematical modeling",
            "project": "Build a physics simulation",
            "explore": "Applied physics and engineering"
        },

        "Mathematics": {
            "skill": "Problem solving and mathematical modeling",
            "project": "Use mathematics to model a real-world problem",
            "explore": "Applied mathematics"
        },

        "Engineering": {
            "skill": "The engineering design process",
            "project": "Identify a real problem and prototype a solution",
            "explore": "Different engineering disciplines"
        },

        "Robotics": {
            "skill": "Programming and electronics",
            "project": "Build a simple robotic system",
            "explore": "Mechatronics and automation"
        },

        "Environmental Science": {
            "skill": "Data collection and analysis",
            "project": "Analyze an environmental issue affecting NYC",
            "explore": "Environmental engineering and sustainability"
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
            f"**Suggested project:** {pathway['project']}"
        )

        st.write(
            f"**Explore further:** {pathway['explore']}"
        )

    st.divider()

    # --------------------------------------------------
    # OPPORTUNITIES
    # --------------------------------------------------

    st.header("Explore Opportunities")

    st.write(
        "Discover STEM opportunities that match your grade, borough, "
        "interests, goals, and accessibility preferences."
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
    # ELIGIBILITY CHECK
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

        boroughs_served = [
            item.strip()
            for item in str(opportunity["boroughs_served"]).split(";")
        ]

        # STEM interest alignment

        max_score += 40

        if any(
            interest in fields
            for interest in profile["interests"]
        ):

            score += 40

            reasons.append(
                "Your STEM interests align with this opportunity."
            )

        # Opportunity type alignment

        if opportunity_types:

            max_score += 20

            if str(
                opportunity["opportunity_type"]
            ) in opportunity_types:

                score += 20

                reasons.append(
                    "This matches the opportunity type you selected."
                )

        # Financial accessibility

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

        # Borough accessibility

        max_score += 15

        if profile["borough"] in boroughs_served:

            score += 15

            reasons.append(
                f"This opportunity is available to students in the "
                f"{profile['borough']}."
            )

        # Bronx-focused opportunities

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
    # OPPORTUNITY RESULTS
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
                "for this profile in our database. "
                "The STEM Pathways NYC database is still growing."
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

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Match",
                            f"{result['score']}%"
                        )

                    with col2:

                        st.metric(
                            "Type",
                            result["type"]
                        )

                    st.write(
                        result["description"]
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
    # ABOUT
    # --------------------------------------------------

    st.divider()

    st.header("About STEM Pathways NYC")

    st.write(
        "STEM Pathways NYC is a student-built platform designed to help "
        "high school students explore STEM beyond the classroom and discover "
        "pathways they can continue pursuing over time."
    )

    st.write(
        "The platform is being developed with a particular focus on expanding "
        "access for students in the Bronx while remaining available to "
        "students throughout New York City."
    )

    st.caption(
        "STEM Pathways NYC • Explore • Build • Discover"
    )
