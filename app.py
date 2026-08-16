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
    st.session_state.current_page = "Home"


# --------------------------------------------------
# ONBOARDING
# --------------------------------------------------

if not st.session_state.profile_completed:

    st.title("STEM Pathways NYC")

    st.subheader(
        "Explore your interests. Build your skills. Find your next opportunity."
    )

    st.write(
        "STEM Pathways NYC helps high school students discover STEM fields, "
        "develop technical skills, build projects, and find programs that "
        "match their interests and goals."
    )

    st.info(
        "Complete your STEM Explorer Profile to personalize your experience."
    )

    st.divider()

    st.header("STEM Explorer Profile")

    st.caption(
        "Your answers help us recommend pathways, projects, resources, and opportunities."
    )

    # --------------------------------------------------
    # ABOUT YOU
    # --------------------------------------------------

    st.subheader("1. About You")

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input("First name")

    with col2:
        last_name = st.text_input("Last name")

    middle_name = st.text_input("Middle name (optional)")

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
    # INTERESTS
    # --------------------------------------------------

    st.subheader("2. STEM Interests")

    interests = st.multiselect(
        "Which fields are you interested in?",
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
        "What have you tried before?",
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

    st.subheader("3. Goals")

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
        "Where are you in your STEM journey?",
        [
            "I am just starting to explore STEM.",
            "I have a few interests but I am still exploring.",
            "I know which STEM fields interest me.",
            "I have experience and want to build advanced skills.",
            "I already have a specific STEM career or major in mind."
        ]
    )

    confidence = st.slider(
        "How confident are you in your current STEM interests?",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = Still exploring, 10 = Very confident"
    )

    weekly_time = st.selectbox(
        "How much time would you like to spend on STEM each week?",
        [
            "Less than 2 hours",
            "2–5 hours",
            "5–10 hours",
            "10+ hours"
        ]
    )

    financial_support = st.checkbox(
        "Prioritize free opportunities or programs with financial aid"
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
            st.warning("Please enter your first name.")

        elif not last_name.strip():
            st.warning("Please enter your last name.")

        elif not interests:
            st.warning("Please select at least one STEM interest.")

        elif not goals:
            st.warning("Please select at least one goal.")

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
            st.session_state.current_page = "Home"

            st.rerun()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

else:

    profile = st.session_state.student_profile

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
    # SIDEBAR
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

        page = st.radio(
            "Menu",
            [
                "Home",
                "My Pathway",
                "Opportunities",
                "Projects",
                "Resources",
                "Profile"
            ],
            index=[
                "Home",
                "My Pathway",
                "Opportunities",
                "Projects",
                "Resources",
                "Profile"
            ].index(
                st.session_state.current_page
            )
        )

        st.session_state.current_page = page

        st.divider()

        st.caption(
            "Explore • Build • Discover"
        )


    # --------------------------------------------------
    # HOME
    # --------------------------------------------------

    if page == "Home":

        st.title(
            f"Welcome back, {profile['first_name']} 👋"
        )

        st.write(
            "Use your dashboard to explore STEM, build skills, "
            "start projects, and discover opportunities."
        )

        st.divider()

        # PROFILE SNAPSHOT

        st.header("Your Snapshot")

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
                "Confidence",
                f"{profile['confidence']}/10"
            )

        with col4:
            st.metric(
                "Weekly Goal",
                profile["weekly_time"]
            )

        st.divider()

        # MAIN INTEREST

        primary_interest = profile["interests"][0]

        st.header("Current Direction")

        with st.container(border=True):

            st.subheader(primary_interest)

            st.write(
                "This is currently your primary STEM interest. "
                "You can continue exploring it or update your profile as your interests change."
            )

        st.divider()

        # NEXT STEPS

        st.header("What to Do Next")

        col1, col2, col3 = st.columns(3)

        with col1:

            with st.container(border=True):

                st.subheader("🧭 Explore")

                st.write(
                    "Review your STEM pathway and learn which skills to develop next."
                )

        with col2:

            with st.container(border=True):

                st.subheader("🛠️ Build")

                st.write(
                    "Choose a project and turn your interests into hands-on experience."
                )

        with col3:

            with st.container(border=True):

                st.subheader("💼 Discover")

                st.write(
                    "Find programs, research, internships, courses, and competitions."
                )

        st.divider()

        # GOALS

        st.header("Your Goals")

        for goal in profile["goals"]:
            st.write(f"✓ {goal}")


    # --------------------------------------------------
    # MY PATHWAY
    # --------------------------------------------------

    elif page == "My Pathway":

        st.title("My STEM Pathway")

        st.write(
            "A suggested roadmap based on your current interests. "
            "Your pathway can change as you explore."
        )

        st.divider()

        primary_interest = profile["interests"][0]

        pathway_data = {

            "Electrical Engineering": {
                "description":
                    "Learn how circuits, electronics, sensors, and embedded systems work.",

                "skills": [
                    "Circuit fundamentals",
                    "Breadboarding",
                    "Digital logic",
                    "Arduino",
                    "Python",
                    "Embedded systems"
                ],

                "projects": [
                    "Build an LED circuit",
                    "Create a digital logic system",
                    "Build an environmental sensor",
                    "Create an Arduino device"
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
                    "Explore machines, physical systems, CAD, product design, and prototyping.",

                "skills": [
                    "CAD",
                    "Engineering design",
                    "Mechanics",
                    "3D printing",
                    "Prototyping",
                    "Manufacturing"
                ],

                "projects": [
                    "Model an object in CAD",
                    "Create a 3D printed prototype",
                    "Design a mechanical system",
                    "Build an assistive device"
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
                    "Explore the connection between hardware, electronics, and software.",

                "skills": [
                    "Python",
                    "Digital logic",
                    "Circuit design",
                    "Arduino",
                    "Computer architecture",
                    "Embedded systems"
                ],

                "projects": [
                    "Build a digital logic circuit",
                    "Create an Arduino system",
                    "Build a sensor-based project",
                    "Design an embedded system"
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
                    "Develop programming, algorithms, software, data, and computational thinking skills.",

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
                    "Create a website",
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
                    "Learn how computers use data to make predictions and decisions.",

                "skills": [
                    "Python",
                    "Data analysis",
                    "Statistics",
                    "Machine learning",
                    "Model evaluation",
                    "Data visualization"
                ],

                "projects": [
                    "Explore a dataset",
                    "Build a prediction model",
                    "Create a recommendation system",
                    "Evaluate model performance"
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
                    "Use data, statistics, and programming to study real-world problems.",

                "skills": [
                    "Python",
                    "Pandas",
                    "Statistics",
                    "Data visualization",
                    "SQL",
                    "Machine learning"
                ],

                "projects": [
                    "Analyze an NYC dataset",
                    "Create a data dashboard",
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
                    "Combine engineering, biology, and healthcare to design solutions for human health.",

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
                    "Model a medical device",
                    "Analyze healthcare data",
                    "Create a health technology concept"
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
                    "Combine programming, electronics, mechanics, and automation.",

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
                    "Design a robotic arm",
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
                "Explore this STEM field through skills, projects, and real-world applications.",

            "skills": [
                "Problem solving",
                "Technical communication",
                "Research",
                "Data analysis",
                "Project design"
            ],

            "projects": [
                "Research a STEM problem",
                "Build a beginner project",
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

        st.write(pathway["description"])

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.header("Skills to Learn")

            for number, skill in enumerate(
                pathway["skills"],
                start=1
            ):

                st.write(
                    f"**{number}. {skill}**"
                )

        with col2:

            st.header("Project Ideas")

            for project in pathway["projects"]:

                st.write(
                    f"• {project}"
                )

        st.divider()

        st.header("Careers to Explore")

        for career in pathway["careers"]:

            st.write(
                f"• {career}"
            )


    # --------------------------------------------------
    # OPPORTUNITIES
    # --------------------------------------------------

    elif page == "Opportunities":

        st.title("Opportunities")

        st.write(
            "Find STEM opportunities that match your grade, borough, interests, and goals."
        )

        st.divider()

        opportunity_types = st.multiselect(
            "Filter by type",
            [
                "Summer Program",
                "Internship",
                "Research",
                "College Course",
                "Competition",
                "Scholarship"
            ]
        )

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

            return (
                profile["grade"] in eligible_grades
                and profile["borough"] in boroughs_served
            )


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

            max_score += 40

            if any(
                interest in fields
                for interest in profile["interests"]
            ):
                score += 40
                reasons.append(
                    "Matches your STEM interests."
                )

            if opportunity_types:

                max_score += 20

                if str(
                    opportunity["opportunity_type"]
                ) in opportunity_types:

                    score += 20
                    reasons.append(
                        "Matches your selected opportunity type."
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
                        "Free or offers financial support."
                    )

            else:
                score += 15

            max_score += 15

            if profile["borough"] in boroughs_served:
                score += 15
                reasons.append(
                    f"Available to students in the {profile['borough']}."
                )

            if profile["borough"] == "Bronx":

                max_score += 10

                if str(
                    opportunity["bronx_priority"]
                ).lower() == "yes":

                    score += 10
                    reasons.append(
                        "Has a specific focus on Bronx students."
                    )

            percentage = round(
                (score / max_score) * 100
            )

            return percentage, reasons


        # FEATURED

        if profile["borough"] == "Bronx":

            st.header("Featured for Bronx Students")

            featured = opportunities[
                opportunities[
                    "bronx_priority"
                ].astype(str).str.lower() == "yes"
            ]

            if featured.empty:

                st.info(
                    "More Bronx-focused opportunities will be added soon."
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

        # RECOMMENDED

        st.header("Recommended for You")

        if st.button(
            "Generate Recommendations",
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
                            f"**Fields:** {result['fields']}"
                        )

                        st.write(
                            f"**Cost:** {result['cost']}"
                        )

                        st.write(
                            f"**Financial Aid:** {result['financial_aid']}"
                        )

                        st.write(
                            f"**Status:** {result['status']}"
                        )

                        with st.expander(
                            "Why this matches"
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

        # ALL OPPORTUNITIES

        st.header("Browse All")

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

                st.write(
                    f"**Type:** {opportunity['opportunity_type']}"
                )

                st.write(
                    f"**Fields:** {opportunity['fields']}"
                )

                st.write(
                    f"**Grades:** {opportunity['grades']}"
                )

                st.write(
                    f"**Cost:** {opportunity['cost']}"
                )

                st.link_button(
                    "View Opportunity",
                    opportunity["url"]
                )


    # --------------------------------------------------
    # PROJECTS
    # --------------------------------------------------

    elif page == "Projects":

        st.title("Projects")

        st.write(
            "Build projects that turn your interests into practical experience."
        )

        st.divider()

        project_library = {

            "Engineering": [
                ("Beginner", "Solve a small problem in your community."),
                ("Intermediate", "Create and test a physical prototype."),
                ("Advanced", "Build and document a complete engineering system.")
            ],

            "Electrical Engineering": [
                ("Beginner", "Build and test an LED circuit."),
                ("Intermediate", "Create an Arduino environmental sensor."),
                ("Advanced", "Design an embedded monitoring system.")
            ],

            "Mechanical Engineering": [
                ("Beginner", "Model an object in CAD."),
                ("Intermediate", "Design and 3D print a prototype."),
                ("Advanced", "Design and test a functional mechanical system.")
            ],

            "Computer Engineering": [
                ("Beginner", "Build a digital logic circuit."),
                ("Intermediate", "Create a hardware and software sensor project."),
                ("Advanced", "Build a small embedded system.")
            ],

            "Computer Science": [
                ("Beginner", "Build a Python application."),
                ("Intermediate", "Create an interactive web application."),
                ("Advanced", "Build a full-stack app with a database.")
            ],

            "Artificial Intelligence": [
                ("Beginner", "Explore and visualize a dataset."),
                ("Intermediate", "Build a simple machine-learning model."),
                ("Advanced", "Build and evaluate a recommendation system.")
            ],

            "Data Science": [
                ("Beginner", "Analyze an NYC public dataset."),
                ("Intermediate", "Build an interactive dashboard."),
                ("Advanced", "Create a predictive analysis project.")
            ],

            "Robotics": [
                ("Beginner", "Design a simple robotic mechanism."),
                ("Intermediate", "Build a sensor-controlled device."),
                ("Advanced", "Create an autonomous robotic system.")
            ]
        }

        shown_projects = False

        for interest in profile["interests"]:

            if interest in project_library:

                shown_projects = True

                st.header(interest)

                for level, project in project_library[interest]:

                    with st.container(border=True):

                        st.caption(level)

                        st.subheader(project)

        if not shown_projects:

            st.info(
                "Project recommendations for your interests will be added soon."
            )


    # --------------------------------------------------
    # RESOURCES
    # --------------------------------------------------

    elif page == "Resources":

        st.title("Resources")

        st.write(
            "Build the skills you need using free and accessible STEM learning resources."
        )

        st.divider()

        st.info(
            "Verified external resources will be added gradually."
        )

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.subheader("Programming")

                st.write(
                    "Python, GitHub, web development, and data analysis."
                )

            with st.container(border=True):

                st.subheader("Engineering")

                st.write(
                    "CAD, electronics, circuit design, Arduino, and prototyping."
                )

        with col2:

            with st.container(border=True):

                st.subheader("Research")

                st.write(
                    "Experimental design, data collection, scientific writing, and analysis."
                )

            with st.container(border=True):

                st.subheader("Career Exploration")

                st.write(
                    "Learn about STEM majors, engineering fields, research careers, and technical roles."
                )


    # --------------------------------------------------
    # PROFILE
    # --------------------------------------------------

    elif page == "Profile":

        st.title("Profile")

        st.subheader(full_name)

        st.caption(
            "Your STEM Explorer Profile"
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

            st.header("Interests")

            for interest in profile["interests"]:
                st.write(
                    f"• {interest}"
                )

            st.header("Experience")

            if profile["experience_areas"]:

                for experience in profile["experience_areas"]:
                    st.write(
                        f"• {experience}"
                    )

            else:
                st.write(
                    "No previous experience selected."
                )

        with col2:

            st.header("Goals")

            for goal in profile["goals"]:
                st.write(
                    f"• {goal}"
                )

            st.header("Current Stage")

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
            "Edit Profile",
            use_container_width=True
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
