import streamlit as st
import pandas as pd


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="STEM Pathways NYC",
    page_icon="🧭",
    layout="wide"
)

opportunities = pd.read_csv("data/opportunities.csv")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "profile_completed" not in st.session_state:
    st.session_state.profile_completed = False

if "student_profile" not in st.session_state:
    st.session_state.student_profile = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"


# --------------------------------------------------
# ONBOARDING QUESTIONNAIRE
# --------------------------------------------------

if not st.session_state.profile_completed:

    st.title("STEM Pathways NYC")

    st.subheader(
        "Discover where your STEM interests can take you."
    )

    st.write(
        "STEM Pathways NYC helps high school students explore STEM fields, "
        "develop technical skills, build projects, and discover opportunities "
        "that align with their interests and goals."
    )

    st.info(
        "Complete your STEM Explorer Profile to create a personalized starting pathway."
    )

    st.divider()

    st.header("Create Your STEM Explorer Profile")

    st.write(
        "Your profile helps personalize your pathway, projects, resources, "
        "and opportunity recommendations. Your interests can always change later."
    )

    # --------------------------------------------------
    # SECTION 1: ABOUT YOU
    # --------------------------------------------------

    st.subheader("1. About You")

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input(
            "First name"
        )

    with col2:
        last_name = st.text_input(
            "Last name"
        )

    middle_name = st.text_input(
        "Middle name (optional)"
    )

    col3, col4, col5 = st.columns(3)

    with col3:
        age = st.number_input(
            "Age",
            min_value=13,
            max_value=19,
            value=15,
            step=1
        )

    with col4:
        grade = st.selectbox(
            "Grade",
            ["9", "10", "11", "12"]
        )

    with col5:
        borough = st.selectbox(
            "Borough",
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
    # SECTION 2: STEM INTERESTS
    # --------------------------------------------------

    st.subheader("2. Your STEM Interests")

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
    # SECTION 3: GOALS
    # --------------------------------------------------

    st.subheader("3. Your Goals")

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
        "Which statement best describes where you are right now?",
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
        "Prioritize free opportunities or programs offering financial aid"
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
            st.session_state.current_page = "Dashboard"

            st.rerun()


# --------------------------------------------------
# STUDENT DASHBOARD
# --------------------------------------------------

else:

    profile = st.session_state.student_profile

    # --------------------------------------------------
    # FULL NAME
    # --------------------------------------------------

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
    # SIDEBAR NAVIGATION
    # --------------------------------------------------

    with st.sidebar:

        st.title("STEM Pathways NYC")

        st.write(
            f"**{profile['first_name']} {profile['last_name']}**"
        )

        st.caption(
            f"Grade {profile['grade']} • {profile['borough']}"
        )

        st.divider()

        st.caption("MAIN")

        if st.button(
            "🏠  Dashboard",
            use_container_width=True
        ):
            st.session_state.current_page = "Dashboard"
            st.rerun()

        if st.button(
            "🧭  My STEM Pathway",
            use_container_width=True
        ):
            st.session_state.current_page = "My STEM Pathway"
            st.rerun()

        st.divider()

        st.caption("EXPLORE")

        if st.button(
            "💼  Opportunities",
            use_container_width=True
        ):
            st.session_state.current_page = "Opportunities"
            st.rerun()

        if st.button(
            "🛠️  Projects",
            use_container_width=True
        ):
            st.session_state.current_page = "Projects"
            st.rerun()

        if st.button(
            "📚  Resources",
            use_container_width=True
        ):
            st.session_state.current_page = "Resources"
            st.rerun()

        st.divider()

        st.caption("ACCOUNT")

        if st.button(
            "👤  My Profile",
            use_container_width=True
        ):
            st.session_state.current_page = "My Profile"
            st.rerun()

        st.divider()

        st.caption(
            "Explore • Build • Discover"
        )

    page = st.session_state.current_page


    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    if page == "Dashboard":

        st.title(
            f"Welcome, {profile['first_name']} 👋"
        )

        st.write(
            "Use your STEM Pathways dashboard to explore your interests, "
            "develop technical skills, build projects, and discover opportunities."
        )

        st.divider()

        # --------------------------------------------------
        # STEM SNAPSHOT
        # --------------------------------------------------

        st.header("Your STEM Snapshot")

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

        # --------------------------------------------------
        # PRIMARY INTEREST
        # --------------------------------------------------

        primary_interest = profile["interests"][0]

        st.header("Your Current Direction")

        with st.container(border=True):

            st.subheader(primary_interest)

            st.write(
                "This is currently your primary STEM interest based on your profile. "
                "Your pathway is flexible and can change as you gain new experiences."
            )

            st.write(
                f"**Current exploration stage:** {profile['exploration_stage']}"
            )

        st.divider()

        # --------------------------------------------------
        # NEXT STEPS
        # --------------------------------------------------

        st.header("Your Next Steps")

        col1, col2, col3 = st.columns(3)

        with col1:

            with st.container(border=True):

                st.subheader("🧭 Explore Your Pathway")

                st.write(
                    "See which skills, projects, and career areas connect "
                    "to your current STEM interests."
                )

                if st.button(
                    "Open My Pathway",
                    key="dashboard_pathway",
                    use_container_width=True
                ):
                    st.session_state.current_page = "My STEM Pathway"
                    st.rerun()

        with col2:

            with st.container(border=True):

                st.subheader("🛠️ Build a Project")

                st.write(
                    "Turn your interests into hands-on experience with "
                    "beginner, intermediate, and advanced project ideas."
                )

                if st.button(
                    "Explore Projects",
                    key="dashboard_projects",
                    use_container_width=True
                ):
                    st.session_state.current_page = "Projects"
                    st.rerun()

        with col3:

            with st.container(border=True):

                st.subheader("💼 Find Opportunities")

                st.write(
                    "Discover programs, research, internships, courses, "
                    "competitions, and scholarships."
                )

                if st.button(
                    "Explore Opportunities",
                    key="dashboard_opportunities",
                    use_container_width=True
                ):
                    st.session_state.current_page = "Opportunities"
                    st.rerun()

        st.divider()

        # --------------------------------------------------
        # INTERESTS
        # --------------------------------------------------

        st.header("Your STEM Interests")

        interest_columns = st.columns(3)

        for index, interest in enumerate(
            profile["interests"]
        ):

            with interest_columns[index % 3]:

                with st.container(border=True):

                    st.write(
                        f"**{interest}**"
                    )

        st.divider()

        # --------------------------------------------------
        # GOALS
        # --------------------------------------------------

        st.header("Your Current Goals")

        for goal in profile["goals"]:
            st.write(
                f"✓ {goal}"
            )


    # --------------------------------------------------
    # MY STEM PATHWAY
    # --------------------------------------------------

    elif page == "My STEM Pathway":

        st.title("My STEM Pathway")

        st.write(
            "Your pathway is a personalized starting point based on your interests. "
            "It is designed to help you explore skills, projects, and careers over time."
        )

        st.divider()

        primary_interest = profile["interests"][0]

        pathway_data = {

            "Electrical Engineering": {
                "description":
                    "Explore electricity, circuits, electronics, sensors, "
                    "digital systems, and embedded technology.",

                "skills": [
                    "Circuit fundamentals",
                    "Breadboarding",
                    "Digital logic",
                    "Arduino",
                    "Python",
                    "Embedded systems"
                ],

                "projects": [
                    "Build and test an LED circuit",
                    "Create a digital logic system",
                    "Build an environmental sensor",
                    "Create an Arduino-based device"
                ],

                "careers": [
                    "Electrical Engineer",
                    "Electronics Engineer",
                    "Embedded Systems Engineer",
                    "Hardware Engineer"
                ]
            },

            "Mechanical Engineering": {
                "description":
                    "Explore machines, product design, mechanics, CAD, "
                    "manufacturing, and physical systems.",

                "skills": [
                    "CAD",
                    "Engineering design",
                    "Mechanics",
                    "3D printing",
                    "Prototyping",
                    "Manufacturing"
                ],

                "projects": [
                    "Model a mechanical object in CAD",
                    "Create a 3D printed prototype",
                    "Design a simple mechanical system",
                    "Build an assistive device concept"
                ],

                "careers": [
                    "Mechanical Engineer",
                    "Product Design Engineer",
                    "Manufacturing Engineer",
                    "Robotics Engineer"
                ]
            },

            "Computer Engineering": {
                "description":
                    "Explore the connection between hardware and software, "
                    "including circuits, digital systems, programming, and embedded devices.",

                "skills": [
                    "Python",
                    "Digital logic",
                    "Circuit design",
                    "Arduino",
                    "Embedded systems",
                    "Computer architecture"
                ],

                "projects": [
                    "Build a digital logic circuit",
                    "Create an Arduino-based system",
                    "Build a hardware and software sensor project",
                    "Design a small embedded system"
                ],

                "careers": [
                    "Computer Engineer",
                    "Hardware Engineer",
                    "Embedded Systems Engineer",
                    "Firmware Engineer"
                ]
            },

            "Computer Science": {
                "description":
                    "Explore programming, algorithms, software development, "
                    "data, and computational problem solving.",

                "skills": [
                    "Python",
                    "Algorithms",
                    "Data structures",
                    "Git and GitHub",
                    "Web development",
                    "Databases"
                ],

                "projects": [
                    "Build a Python application",
                    "Create an interactive website",
                    "Build a data dashboard",
                    "Create a full web application"
                ],

                "careers": [
                    "Software Engineer",
                    "Data Engineer",
                    "Cybersecurity Engineer",
                    "Machine Learning Engineer"
                ]
            },

            "Artificial Intelligence": {
                "description":
                    "Explore how computers use data to recognize patterns, "
                    "make predictions, and support decision-making.",

                "skills": [
                    "Python",
                    "Data analysis",
                    "Statistics",
                    "Machine learning",
                    "Model evaluation",
                    "Data visualization"
                ],

                "projects": [
                    "Explore and visualize a dataset",
                    "Build a simple prediction model",
                    "Create a recommendation system",
                    "Compare model performance"
                ],

                "careers": [
                    "Machine Learning Engineer",
                    "AI Engineer",
                    "Data Scientist",
                    "Research Scientist"
                ]
            },

            "Data Science": {
                "description":
                    "Explore how data, statistics, and programming can be "
                    "used to understand real-world problems.",

                "skills": [
                    "Python",
                    "Pandas",
                    "Statistics",
                    "Data visualization",
                    "SQL",
                    "Machine learning"
                ],

                "projects": [
                    "Analyze an NYC public dataset",
                    "Create an interactive dashboard",
                    "Study trends in public data",
                    "Build a predictive model"
                ],

                "careers": [
                    "Data Scientist",
                    "Data Analyst",
                    "Data Engineer",
                    "Operations Research Analyst"
                ]
            },

            "Biomedical Engineering": {
                "description":
                    "Explore how engineering, biology, and technology can "
                    "be combined to improve healthcare and human health.",

                "skills": [
                    "Biology",
                    "Engineering design",
                    "CAD",
                    "Data analysis",
                    "Prototyping",
                    "Biomechanics"
                ],

                "projects": [
                    "Design an assistive device",
                    "Model a medical device concept",
                    "Analyze healthcare data",
                    "Create a low-cost health technology concept"
                ],

                "careers": [
                    "Biomedical Engineer",
                    "Medical Device Engineer",
                    "Biomechanical Engineer",
                    "Healthcare Data Scientist"
                ]
            },

            "Robotics": {
                "description":
                    "Explore systems that combine programming, electronics, "
                    "mechanics, sensors, and automation.",

                "skills": [
                    "Python",
                    "Electronics",
                    "Arduino",
                    "CAD",
                    "Sensors",
                    "Control systems"
                ],

                "projects": [
                    "Build a simple robot",
                    "Create a sensor-controlled device",
                    "Design a robotic arm concept",
                    "Build an automated system"
                ],

                "careers": [
                    "Robotics Engineer",
                    "Mechatronics Engineer",
                    "Automation Engineer",
                    "Controls Engineer"
                ]
            }
        }

        default_pathway = {
            "description":
                "Explore this STEM field through technical skills, "
                "projects, and real-world applications.",

            "skills": [
                "Problem solving",
                "Technical communication",
                "Research",
                "Data analysis",
                "Project design"
            ],

            "projects": [
                "Research a real-world STEM problem",
                "Build a beginner STEM project",
                "Analyze a public dataset",
                "Create a technical presentation"
            ],

            "careers": [
                "Engineer",
                "Scientist",
                "Researcher",
                "Technical Specialist"
            ]
        }

        pathway = pathway_data.get(
            primary_interest,
            default_pathway
        )

        st.subheader(primary_interest)

        st.write(
            pathway["description"]
        )

        st.divider()

        # --------------------------------------------------
        # SKILL ROADMAP
        # --------------------------------------------------

        st.header("Skill Roadmap")

        st.write(
            "You do not need to learn everything at once. "
            "Use this as a suggested order for exploring the field."
        )

        for number, skill in enumerate(
            pathway["skills"],
            start=1
        ):

            with st.container(border=True):

                st.write(
                    f"**Step {number} — {skill}**"
                )

        st.divider()

        # --------------------------------------------------
        # PROJECTS
        # --------------------------------------------------

        st.header("Projects to Try")

        for number, project in enumerate(
            pathway["projects"],
            start=1
        ):

            with st.container(border=True):

                st.caption(
                    f"Project {number}"
                )

                st.subheader(
                    project
                )

        st.divider()

        # --------------------------------------------------
        # CAREERS
        # --------------------------------------------------

        st.header("Careers to Explore")

        st.write(
            "These are examples of careers connected to this pathway."
        )

        career_columns = st.columns(2)

        for index, career in enumerate(
            pathway["careers"]
        ):

            with career_columns[index % 2]:

                with st.container(border=True):

                    st.write(
                        f"**{career}**"
                    )


    # --------------------------------------------------
    # OPPORTUNITIES
    # --------------------------------------------------

    elif page == "Opportunities":

        st.title("Opportunities")

        st.write(
            "Discover STEM programs and experiences that match your grade, "
            "borough, interests, goals, and accessibility preferences."
        )

        st.divider()

        opportunity_types = st.multiselect(
            "Filter by opportunity type",
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
                for item in str(
                    opportunity["grades"]
                ).split(";")
            ]

            boroughs_served = [
                item.strip()
                for item in str(
                    opportunity["boroughs_served"]
                ).split(";")
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
                for item in str(
                    opportunity["fields"]
                ).split(";")
            ]

            boroughs_served = [
                item.strip()
                for item in str(
                    opportunity["boroughs_served"]
                ).split(";")
            ]

            # Interest alignment
            max_score += 40

            if any(
                interest in fields
                for interest in profile["interests"]
            ):

                score += 40

                reasons.append(
                    "Your STEM interests align with this opportunity."
                )

            # Opportunity type
            if opportunity_types:

                max_score += 20

                if str(
                    opportunity["opportunity_type"]
                ) in opportunity_types:

                    score += 20

                    reasons.append(
                        "This matches an opportunity type you selected."
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
                        "This opportunity is free or offers financial support."
                    )

            else:

                score += 15

            # Borough access
            max_score += 15

            if profile["borough"] in boroughs_served:

                score += 15

                reasons.append(
                    f"This opportunity serves students in the "
                    f"{profile['borough']}."
                )

            # Bronx focus
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
        # FEATURED FOR BRONX STUDENTS
        # --------------------------------------------------

        if profile["borough"] == "Bronx":

            st.header("Featured for Bronx Students")

            st.write(
                "Opportunities in our database that have a specific Bronx focus."
            )

            featured = opportunities[
                opportunities[
                    "bronx_priority"
                ].astype(str).str.lower() == "yes"
            ]

            if featured.empty:

                st.info(
                    "More Bronx-focused opportunities will be added as the database grows."
                )

            else:

                for _, opportunity in featured.head(3).iterrows():

                    with st.container(border=True):

                        st.subheader(
                            opportunity["name"]
                        )

                        st.caption(
                            opportunity["organization"]
                        )

                        st.write(
                            opportunity["description"]
                        )

                        col1, col2 = st.columns(2)

                        with col1:
                            st.write(
                                f"**Type:** {opportunity['opportunity_type']}"
                            )

                        with col2:
                            st.write(
                                f"**Cost:** {opportunity['cost']}"
                            )

                        st.link_button(
                            "View Opportunity",
                            opportunity["url"],
                            use_container_width=True
                        )

            st.divider()

        # --------------------------------------------------
        # PERSONALIZED RECOMMENDATIONS
        # --------------------------------------------------

        st.header("Recommended for You")

        st.write(
            "Generate recommendations using the information in your STEM profile."
        )

        if st.button(
            "Generate My Recommendations",
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

            if not results:

                st.info(
                    "No eligible opportunities were found for your profile."
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
                                "Match Score",
                                f"{result['score']}%"
                            )

                        with col2:
                            st.metric(
                                "Opportunity Type",
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
                            "Why this opportunity matches your profile"
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

        st.divider()

        # --------------------------------------------------
        # BROWSE ALL
        # --------------------------------------------------

        st.header("Browse All Opportunities")

        st.write(
            "Explore everything currently available in the STEM Pathways NYC database."
        )

        for _, opportunity in opportunities.iterrows():

            if (
                opportunity_types
                and str(
                    opportunity["opportunity_type"]
                ) not in opportunity_types
            ):
                continue

            with st.expander(
                f"{opportunity['name']} — {opportunity['organization']}"
            ):

                st.write(
                    opportunity["description"]
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Type:** {opportunity['opportunity_type']}"
                    )

                    st.write(
                        f"**Fields:** {opportunity['fields']}"
                    )

                    st.write(
                        f"**Eligible Grades:** {opportunity['grades']}"
                    )

                with col2:

                    st.write(
                        f"**Cost:** {opportunity['cost']}"
                    )

                    st.write(
                        f"**Financial Aid:** {opportunity['financial_aid']}"
                    )

                    st.write(
                        f"**Status:** {opportunity['application_status']}"
                    )

                st.link_button(
                    "View Official Opportunity",
                    opportunity["url"]
                )


    # --------------------------------------------------
    # PROJECTS
    # --------------------------------------------------

    elif page == "Projects":

        st.title("Projects")

        st.write(
            "Use hands-on projects to explore your interests, practice technical skills, "
            "and build experience you can continue developing over time."
        )

        st.divider()

        project_library = {

            "Engineering": [
                (
                    "Beginner",
                    "Identify a problem in your school or community and design a possible solution."
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
                    "Model a real object using CAD."
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
                    "Build a simple digital logic circuit."
                ),
                (
                    "Intermediate",
                    "Create a hardware and software sensor project."
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

            "Robotics": [
                (
                    "Beginner",
                    "Design a simple robotic mechanism."
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

        for interest in profile["interests"]:

            if interest in project_library:

                shown_projects = True

                st.header(
                    interest
                )

                for level, project in project_library[interest]:

                    with st.container(border=True):

                        st.caption(
                            level
                        )

                        st.subheader(
                            project
                        )

        if not shown_projects:

            st.info(
                "Project recommendations for your selected interests will be added soon."
            )


    # --------------------------------------------------
    # RESOURCES
    # --------------------------------------------------

    elif page == "Resources":

        st.title("Resources")

        st.write(
            "Build the skills you need for your pathway using free and accessible "
            "learning resources."
        )

        st.divider()

        st.info(
            "Verified external learning resources will be added gradually."
        )

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.subheader("💻 Programming")

                st.write(
                    "Python • GitHub • Web Development • Data Analysis"
                )

            with st.container(border=True):

                st.subheader("⚙️ Engineering")

                st.write(
                    "CAD • Electronics • Circuit Design • Arduino • Prototyping"
                )

        with col2:

            with st.container(border=True):

                st.subheader("🔬 Research")

                st.write(
                    "Experimental Design • Data Collection • Scientific Writing • Analysis"
                )

            with st.container(border=True):

                st.subheader("🎓 Career Exploration")

                st.write(
                    "STEM Majors • Engineering Fields • Research Careers • Technical Careers"
                )


    # --------------------------------------------------
    # MY PROFILE
    # --------------------------------------------------

    elif page == "My Profile":

        st.title("My Profile")

        st.subheader(
            full_name
        )

        st.caption(
            "STEM Explorer Profile"
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

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

            st.header("STEM Interests")

            for interest in profile["interests"]:
                st.write(
                    f"• {interest}"
                )

            st.header("Previous Experience")

            if profile["experience_areas"]:

                for experience in profile["experience_areas"]:
                    st.write(
                        f"• {experience}"
                    )

            else:

                st.write(
                    "No previous STEM experience selected."
                )

        with col2:

            st.header("Goals")

            for goal in profile["goals"]:
                st.write(
                    f"• {goal}"
                )

            st.header("Current Exploration Stage")

            st.write(
                profile["exploration_stage"]
            )

            st.write(
                f"**Weekly STEM goal:** {profile['weekly_time']}"
            )

        st.divider()

        st.info(
            "Your profile is currently stored only during this browser session. "
            "Permanent accounts and saved profiles will be added later."
        )

        if st.button(
            "Edit My Profile",
            use_container_width=True
        ):

            st.session_state.profile_completed = False
            st.session_state.current_page = "Dashboard"
            st.rerun()


    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    st.divider()

    st.caption(
        "STEM Pathways NYC • Explore • Build • Discover"
    )
