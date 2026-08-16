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
# ONBOARDING QUESTIONNAIRE
# --------------------------------------------------

if not st.session_state.profile_completed:

    st.title("STEM Pathways NYC")

    st.subheader(
        "Discover where your STEM interests can take you."
    )

    st.write(
        "STEM Pathways NYC helps high school students explore STEM fields, "
        "build technical skills, discover projects, and find opportunities "
        "that align with their interests and goals."
    )

    st.info(
        "Complete your STEM Explorer Profile to receive a personalized pathway."
    )

    st.divider()

    st.header("Create Your STEM Explorer Profile")

    st.write(
        "Tell us about yourself and what you want to explore. "
        "Your interests can change over time."
    )

    # --------------------------------------------------
    # ABOUT YOU
    # --------------------------------------------------

    st.subheader("About You")

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
            [
                "9",
                "10",
                "11",
                "12"
            ]
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
        help="1 = Still exploring, 10 = Very confident"
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
            st.session_state.current_page = "Home"

            st.rerun()


# --------------------------------------------------
# DASHBOARD
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
            f"Welcome, **{profile['first_name']}**"
        )

        st.caption(
            f"{profile['grade']}th Grade • {profile['borough']}"
        )

        st.divider()

        page = st.radio(
            "Navigation",
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
    # HOME PAGE
    # --------------------------------------------------

    if page == "Home":

        st.title(
            f"Welcome, {profile['first_name']} 👋"
        )

        st.write(
            "Your STEM journey is built around exploration. "
            "Use STEM Pathways NYC to discover fields, build skills, "
            "work on projects, and find opportunities."
        )

        st.divider()

        st.header("Your STEM Journey")

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
                "Weekly Exploration",
                profile["weekly_time"]
            )

        st.divider()

        st.header("Current Interests")

        interest_columns = st.columns(3)

        for index, interest in enumerate(
            profile["interests"]
        ):

            with interest_columns[
                index % 3
            ]:

                with st.container(
                    border=True
                ):

                    st.write(
                        f"**{interest}**"
                    )

        st.divider()

        st.header("Your Current Goals")

        for goal in profile["goals"]:

            st.write(
                f"✓ {goal}"
            )

        st.divider()

        st.header("Recommended Next Steps")

        with st.container(border=True):

            st.subheader(
                "1. Explore Your Pathway"
            )

            st.write(
                "Review the skills, fields, and project ideas "
                "recommended for your current interests."
            )

        with st.container(border=True):

            st.subheader(
                "2. Build Something"
            )

            st.write(
                "Choose a project that helps you turn an interest "
                "into hands-on experience."
            )

        with st.container(border=True):

            st.subheader(
                "3. Find Opportunities"
            )

            st.write(
                "Explore programs, research, internships, "
                "college courses, competitions, and scholarships."
            )


    # --------------------------------------------------
    # MY PATHWAY PAGE
    # --------------------------------------------------

    elif page == "My Pathway":

        st.title("My STEM Pathway")

        st.write(
            "Your pathway is not a fixed career plan. "
            "It is a starting point for exploring your interests "
            "through skills and projects."
        )

        st.divider()

        primary_interest = profile[
            "interests"
        ][0]

        pathway_data = {

            "Electrical Engineering": {
                "description":
                    "Explore how electricity, circuits, electronics, "
                    "and embedded systems are designed.",

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
                    "Explore machines, product design, mechanics, "
                    "manufacturing, and physical systems.",

                "skills": [
                    "CAD",
                    "Engineering design",
                    "Statics",
                    "Mechanics",
                    "3D printing",
                    "Prototyping"
                ],

                "projects": [
                    "Design a mechanical part in CAD",
                    "Create a 3D printed prototype",
                    "Design a small mechanical system",
                    "Build a simple assistive device"
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
                    "Explore the intersection of computer hardware "
                    "and software.",

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
                    "Build a sensor with software",
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
                    "Explore programming, algorithms, software, "
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
                    "Create a personal website",
                    "Build a data dashboard",
                    "Create a web application"
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
                    "Explore how computers can learn from data "
                    "and make predictions or decisions.",

                "skills": [
                    "Python",
                    "Data analysis",
                    "Statistics",
                    "Machine learning",
                    "Model evaluation",
                    "Data visualization"
                ],

                "projects": [
                    "Build a prediction model",
                    "Classify a dataset",
                    "Create a recommendation system",
                    "Analyze model performance"
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
                    "Explore how data can be analyzed to answer "
                    "questions and solve real problems.",

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
                    "Create an interactive dashboard",
                    "Study trends in public data",
                    "Build a basic predictive model"
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
                    "Explore how engineering can be used to improve "
                    "medicine, healthcare, and human health.",

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
                    "Explore systems that combine programming, "
                    "electronics, and mechanical design.",

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
                    "Create a sensor system",
                    "Design a robotic arm concept",
                    "Build an automated device"
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
                "Explore this STEM field through skills, "
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
                "Build a beginner project",
                "Analyze a public dataset",
                "Create a technical presentation"
            ],

            "careers": [
                "STEM Researcher",
                "Engineer",
                "Scientist",
                "Technical Specialist"
            ]
        }

        pathway = pathway_data.get(
            primary_interest,
            default_pathway
        )

        st.subheader(
            primary_interest
        )

        st.write(
            pathway["description"]
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.header("Skills to Explore")

            for number, skill in enumerate(
                pathway["skills"],
                start=1
            ):

                st.write(
                    f"**{number}. {skill}**"
                )

        with col2:

            st.header("Project Ideas")

            for project in pathway[
                "projects"
            ]:

                st.write(
                    f"• {project}"
                )

        st.divider()

        st.header(
            "Related Careers"
        )

        for career in pathway[
            "careers"
        ]:

            st.write(
                f"• {career}"
            )


    # --------------------------------------------------
    # OPPORTUNITIES PAGE
    # --------------------------------------------------

    elif page == "Opportunities":

        st.title(
            "STEM Opportunities"
        )

        st.write(
            "Discover opportunities based on your grade, "
            "borough, STEM interests, and goals."
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
        # ELIGIBILITY
        # --------------------------------------------------

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

            if (
                profile["grade"]
                not in eligible_grades
            ):

                return False

            if (
                profile["borough"]
                not in boroughs_served
            ):

                return False

            return True


        # --------------------------------------------------
        # MATCHING
        # --------------------------------------------------

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

            # Interest alignment

            max_score += 40

            if any(
                interest in fields
                for interest
                in profile["interests"]
            ):

                score += 40

                reasons.append(
                    "Your STEM interests align with this opportunity."
                )

            # Opportunity type

            if opportunity_types:

                max_score += 20

                if str(
                    opportunity[
                        "opportunity_type"
                    ]
                ) in opportunity_types:

                    score += 20

                    reasons.append(
                        "This matches an opportunity type you selected."
                    )

            # Financial access

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
                    or aid == "available"
                ):

                    score += 15

                    reasons.append(
                        "This opportunity is free or offers financial assistance."
                    )

            else:

                score += 15

            # Borough access

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

            # Bronx focus

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

            percentage = round(
                (
                    score /
                    max_score
                ) * 100
            )

            return (
                percentage,
                reasons
            )


        # --------------------------------------------------
        # FEATURED BRONX OPPORTUNITIES
        # --------------------------------------------------

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
                ].astype(str).str.lower()
                == "yes"
            ]

            if featured.empty:

                st.info(
                    "More Bronx-focused opportunities "
                    "will be added soon."
                )

            else:

                for _, opportunity in featured.head(
                    3
                ).iterrows():

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            opportunity["name"]
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

                        st.write(
                            f"**Type:** "
                            f"{opportunity['opportunity_type']}"
                        )

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

        # --------------------------------------------------
        # RECOMMENDATIONS
        # --------------------------------------------------

        st.header(
            "Recommended for You"
        )

        if st.button(
            "Generate Recommendations",
            type="primary",
            use_container_width=True
        ):

            results = []

            for _, opportunity in opportunities.iterrows():

                if not is_eligible(
                    opportunity
                ):

                    continue

                score, reasons = (
                    calculate_match(
                        opportunity
                    )
                )

                results.append({
                    "name":
                        opportunity["name"],

                    "organization":
                        opportunity[
                            "organization"
                        ],

                    "score":
                        score,

                    "fields":
                        opportunity["fields"],

                    "type":
                        opportunity[
                            "opportunity_type"
                        ],

                    "cost":
                        opportunity["cost"],

                    "financial_aid":
                        opportunity[
                            "financial_aid"
                        ],

                    "status":
                        opportunity[
                            "application_status"
                        ],

                    "description":
                        opportunity[
                            "description"
                        ],

                    "url":
                        opportunity["url"],

                    "reasons":
                        reasons
                })

            results = sorted(
                results,
                key=lambda item:
                    item["score"],
                reverse=True
            )

            if not results:

                st.info(
                    "No eligible opportunities are currently "
                    "available for this profile."
                )

            else:

                for result in results:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            result["name"]
                        )

                        st.caption(
                            result[
                                "organization"
                            ]
                        )

                        col1, col2 = (
                            st.columns(2)
                        )

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
                            result[
                                "description"
                            ]
                        )

                        st.write(
                            f"**STEM Fields:** "
                            f"{result['fields']}"
                        )

                        st.write(
                            f"**Cost:** "
                            f"{result['cost']}"
                        )

                        st.write(
                            f"**Financial Aid:** "
                            f"{result['financial_aid']}"
                        )

                        st.write(
                            f"**Application Status:** "
                            f"{result['status']}"
                        )

                        with st.expander(
                            "Why this matches"
                        ):

                            for reason in result[
                                "reasons"
                            ]:

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
        # EXPLORE ALL
        # --------------------------------------------------

        st.header(
            "Explore All Opportunities"
        )

        st.write(
            "Browse opportunities in the STEM Pathways NYC database."
        )

        for _, opportunity in opportunities.iterrows():

            if (
                opportunity_types
                and str(
                    opportunity[
                        "opportunity_type"
                    ]
                ) not in opportunity_types
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

                st.write(
                    f"**Cost:** "
                    f"{opportunity['cost']}"
                )

                st.write(
                    f"**Financial Aid:** "
                    f"{opportunity['financial_aid']}"
                )

                st.link_button(
                    "View Opportunity",
                    opportunity["url"]
                )


    # --------------------------------------------------
    # PROJECTS PAGE
    # --------------------------------------------------

    elif page == "Projects":

        st.title(
            "STEM Projects"
        )

        st.write(
            "Build hands-on projects that help you explore "
            "your interests and develop technical skills."
        )

        st.divider()

        st.info(
            "Personalized project tracking will be added "
            "in a future version."
        )

        project_library = {

            "Engineering": [
                (
                    "Beginner",
                    "Design a solution to a problem in your community."
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
                    "Model a household object using CAD."
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
                    "Explore and visualize a dataset."
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

        for interest in profile[
            "interests"
        ]:

            if interest in project_library:

                shown_projects = True

                st.header(
                    interest
                )

                for level, project in (
                    project_library[
                        interest
                    ]
                ):

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
                "More personalized project ideas "
                "for your interests will be added soon."
            )


    # --------------------------------------------------
    # RESOURCES PAGE
    # --------------------------------------------------

    elif page == "Resources":

        st.title(
            "Learning Resources"
        )

        st.write(
            "Use these sections to build the skills needed "
            "for your projects and future opportunities."
        )

        st.divider()

        st.info(
            "Verified learning resources will be added "
            "gradually as the platform grows."
        )

        with st.container(
            border=True
        ):

            st.subheader(
                "Programming"
            )

            st.write(
                "Python • GitHub • Web Development • Data Analysis"
            )

        with st.container(
            border=True
        ):

            st.subheader(
                "Engineering"
            )

            st.write(
                "CAD • Electronics • Circuit Design • Arduino • Prototyping"
            )

        with st.container(
            border=True
        ):

            st.subheader(
                "Science & Research"
            )

            st.write(
                "Experimental Design • Data Collection • "
                "Scientific Writing • Research Skills"
            )

        with st.container(
            border=True
        ):

            st.subheader(
                "Career Exploration"
            )

            st.write(
                "Engineering disciplines • STEM majors • "
                "Research careers • Technical careers"
            )


    # --------------------------------------------------
    # PROFILE PAGE
    # --------------------------------------------------

    elif page == "Profile":

        st.title(
            "My Profile"
        )

        st.subheader(
            full_name
        )

        st.divider()

        col1, col2, col3 = (
            st.columns(3)
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

        st.divider()

        st.header(
            "STEM Interests"
        )

        for interest in profile[
            "interests"
        ]:

            st.write(
                f"• {interest}"
            )

        st.header(
            "Experience"
        )

        if profile[
            "experience_areas"
        ]:

            for experience in profile[
                "experience_areas"
            ]:

                st.write(
                    f"• {experience}"
                )

        else:

            st.write(
                "No previous STEM experience selected."
            )

        st.header(
            "Goals"
        )

        for goal in profile[
            "goals"
        ]:

            st.write(
                f"• {goal}"
            )

        st.header(
            "Exploration Stage"
        )

        st.write(
            profile[
                "exploration_stage"
            ]
        )

        st.write(
            f"**Interest confidence:** "
            f"{profile['confidence']}/10"
        )

        st.write(
            f"**Weekly exploration goal:** "
            f"{profile['weekly_time']}"
        )

        st.divider()

        st.warning(
            "Profile information is currently stored only "
            "for this browser session. Account-based saving "
            "will be added later."
        )

        if st.button(
            "Edit My Profile",
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
