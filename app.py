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


# --------------------------------------------------
# LOAD DATABASES
# --------------------------------------------------

opportunities = pd.read_csv("data/opportunities.csv")
careers = pd.read_csv("data/careers.csv")


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def format_salary(value):

    if pd.isna(value):
        return "Data unavailable"

    try:
        return f"${int(float(value)):,}"
    except:
        return "Data unavailable"


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
# ONBOARDING
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
        "career recommendations, and opportunity matches."
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
    # INTERESTS
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
    # GOALS
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
            st.session_state.current_page = "Dashboard"

            st.rerun()


# --------------------------------------------------
# MAIN APP
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

        st.caption("MAIN")

        if st.button(
            "🏠 Dashboard",
            use_container_width=True
        ):
            st.session_state.current_page = "Dashboard"
            st.rerun()

        if st.button(
            "🧭 My STEM Pathway",
            use_container_width=True
        ):
            st.session_state.current_page = "My STEM Pathway"
            st.rerun()

        st.divider()

        st.caption("EXPLORE")

        if st.button(
            "💼 Opportunities",
            use_container_width=True
        ):
            st.session_state.current_page = "Opportunities"
            st.rerun()

        if st.button(
            "🛠️ Projects",
            use_container_width=True
        ):
            st.session_state.current_page = "Projects"
            st.rerun()

        if st.button(
            "📚 Resources",
            use_container_width=True
        ):
            st.session_state.current_page = "Resources"
            st.rerun()

        st.divider()

        st.caption("ACCOUNT")

        if st.button(
            "👤 My Profile",
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

        primary_interest = profile["interests"][0]

        st.header(
            "Your Current Direction"
        )

        with st.container(border=True):

            st.subheader(primary_interest)

            st.write(
                "This is currently your primary STEM interest based on your profile. "
                "Your pathway can change as you gain new experiences."
            )

            st.write(
                f"**Current exploration stage:** "
                f"{profile['exploration_stage']}"
            )

        st.divider()

        st.header(
            "Your Next Steps"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            with st.container(border=True):

                st.subheader(
                    "🧭 Explore Your Pathway"
                )

                st.write(
                    "Explore recommended majors, careers, skills, "
                    "salary information, and project ideas."
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

                st.subheader(
                    "🛠️ Build a Project"
                )

                st.write(
                    "Turn your interests into hands-on experience "
                    "through STEM projects."
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

                st.subheader(
                    "💼 Find Opportunities"
                )

                st.write(
                    "Discover programs, research, internships, "
                    "courses, competitions, and scholarships."
                )

                if st.button(
                    "Explore Opportunities",
                    key="dashboard_opportunities",
                    use_container_width=True
                ):
                    st.session_state.current_page = "Opportunities"
                    st.rerun()

    # --------------------------------------------------
    # MY STEM PATHWAY
    # --------------------------------------------------

    elif page == "My STEM Pathway":

        st.title(
            "My STEM Pathway"
        )

        st.write(
            "Explore which majors and careers may fit your interests. "
            "These recommendations are designed to guide exploration, "
            "not determine what you must study."
        )

        st.divider()

        st.header(
            "Discover Your STEM Direction"
        )

        st.write(
            "Answer these questions to receive more specific recommendations "
            "for majors, careers, and technical areas to explore."
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

        # --------------------------------------------------
        # MAJOR / CAREER MAPPING
        # --------------------------------------------------

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

        # --------------------------------------------------
        # FIELD SCORING
        # --------------------------------------------------

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

        scores["Computer Science"] += programming_score * 2
        scores["Computer Engineering"] += programming_score * 1.5
        scores["Artificial Intelligence"] += programming_score * 2
        scores["Data Science"] += programming_score * 1.5
        scores["Robotics"] += programming_score

        scores["Mechanical Engineering"] += hands_on_score * 2
        scores["Electrical Engineering"] += hands_on_score
        scores["Computer Engineering"] += hands_on_score
        scores["Robotics"] += hands_on_score * 2
        scores["Engineering"] += hands_on_score

        scores["Mathematics"] += math_score * 2
        scores["Physics"] += math_score * 1.5
        scores["Data Science"] += math_score
        scores["Artificial Intelligence"] += math_score
        scores["Electrical Engineering"] += math_score
        scores["Mechanical Engineering"] += math_score

        scores["Electrical Engineering"] += electronics_score * 2
        scores["Computer Engineering"] += electronics_score * 2
        scores["Robotics"] += electronics_score * 1.5

        scores["Biology"] += science_score * 2
        scores["Biomedical Engineering"] += science_score * 1.5
        scores["Physics"] += science_score * 1.5
        scores["Environmental Science"] += science_score * 1.5

        scores["Data Science"] += data_score * 2
        scores["Artificial Intelligence"] += data_score * 2
        scores["Computer Science"] += data_score
        scores["Mathematics"] += data_score

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
            scores[work_mapping[preferred_work]] += 25

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
            scores[activity_mapping[favorite_activity]] += 20

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
                environment_mapping[preferred_environment]
            ] += 15

        # --------------------------------------------------
        # GENERATE RECOMMENDATIONS
        # --------------------------------------------------

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

            top_three = ranked[:3]

            max_score_value = top_three[0][1]

            st.divider()

            st.header(
                "Your STEM Direction"
            )

            st.write(
                "Based on your responses, these fields may be "
                "strong areas for you to explore further."
            )

            for index, (
                field,
                score
            ) in enumerate(
                top_three,
                start=1
            ):

                if max_score_value > 0:

                    percentage = round(
                        (score / max_score_value) * 100
                    )

                else:
                    percentage = 0

                with st.container(border=True):

                    st.subheader(
                        f"#{index} {field}"
                    )

                    st.metric(
                        "Exploration Match",
                        f"{percentage}%"
                    )

                    major_info = career_database.get(
                        field,
                        career_database["Engineering"]
                    )

                    st.write(
                        "**Majors to explore:**"
                    )

                    for major in major_info["majors"]:
                        st.write(
                            f"• {major}"
                        )

            # --------------------------------------------------
            # TOP MAJOR
            # --------------------------------------------------

            top_field = top_three[0][0]

            top_info = career_database.get(
                top_field,
                career_database["Engineering"]
            )

            st.divider()

            st.header(
                "Recommended Major Direction"
            )

            st.subheader(
                top_info["majors"][0]
            )

            st.info(
                "This recommendation is a starting point for exploration. "
                "It is not a decision about what you must major in."
            )

            st.divider()

            # --------------------------------------------------
            # CAREER SALARY CARDS
            # --------------------------------------------------

            st.header(
                "Specific Careers to Explore"
            )

            st.write(
                f"These careers are commonly connected to "
                f"**{top_field}**."
            )

            st.caption(
                "Career-stage benchmarks use national BLS wage percentiles. "
                "The local average uses New York-area BLS wage data where available."
            )

            career_columns = st.columns(2)

            for index, career_name in enumerate(
                top_info["careers"]
            ):

                with career_columns[index % 2]:

                    with st.container(border=True):

                        st.subheader(
                            career_name
                        )

                        career_match = careers[
                            careers["career"]
                            .astype(str)
                            .str.lower()
                            == career_name.lower()
                        ]

                        if not career_match.empty:

                            career_data = (
                                career_match.iloc[0]
                            )

                            st.caption(
                                f"Recommended major: "
                                f"{career_data['recommended_major']}"
                            )

                            st.write(
                                career_data["description"]
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

                                local_salary_label = (
                                    "NYC Metro Average"
                                )

                                if (
                                    "salary_area"
                                    in career_data.index
                                    and
                                    pd.notna(
                                        career_data[
                                            "salary_area"
                                        ]
                                    )
                                ):

                                    if (
                                        "New York State"
                                        in str(
                                            career_data[
                                                "salary_area"
                                            ]
                                        )
                                    ):

                                        local_salary_label = (
                                            "New York Average"
                                        )

                                st.metric(
                                    local_salary_label,
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

                            skills = str(
                                career_data["skills"]
                            ).split(";")

                            for skill in skills:

                                st.write(
                                    f"• {skill.strip()}"
                                )

                            st.markdown(
                                "#### Data Details"
                            )

                            if (
                                "bls_occupation"
                                in career_data.index
                            ):

                                st.write(
                                    f"**BLS occupation:** "
                                    f"{career_data['bls_occupation']}"
                                )

                            if (
                                "soc_code"
                                in career_data.index
                            ):

                                st.write(
                                    f"**SOC code:** "
                                    f"{career_data['soc_code']}"
                                )

                            if (
                                "benchmark_area"
                                in career_data.index
                            ):

                                st.write(
                                    f"**Career benchmark area:** "
                                    f"{career_data['benchmark_area']}"
                                )

                            if (
                                "salary_area"
                                in career_data.index
                            ):

                                st.write(
                                    f"**Local salary area:** "
                                    f"{career_data['salary_area']}"
                                )

                            if (
                                "source_year"
                                in career_data.index
                            ):

                                st.write(
                                    f"**Data year:** "
                                    f"{career_data['source_year']}"
                                )

                            if (
                                "data_type"
                                in career_data.index
                            ):

                                st.write(
                                    f"**Data type:** "
                                    f"{career_data['data_type']}"
                                )

                            if (
                                "salary_mapping_note"
                                in career_data.index
                                and pd.notna(
                                    career_data[
                                        "salary_mapping_note"
                                    ]
                                )
                                and str(
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
                                "salary_source"
                                in career_data.index
                            ):

                                st.write(
                                    f"**Source:** "
                                    f"{career_data['salary_source']}"
                                )

                            if (
                                "source_url"
                                in career_data.index
                                and pd.notna(
                                    career_data["source_url"]
                                )
                            ):

                                st.link_button(
                                    "View Official BLS Source",
                                    career_data[
                                        "source_url"
                                    ],
                                    use_container_width=True
                                )

                        else:

                            st.caption(
                                f"Related field: {top_field}"
                            )

                            st.info(
                                "Detailed salary information for this "
                                "career is still being added."
                            )

            st.divider()

            st.info(
                "Salary note: Early-career and experienced benchmarks use "
                "the 25th and 75th percentile of workers in the occupation. "
                "They do not represent guaranteed salaries after a specific "
                "number of years. Actual compensation can vary by employer, "
                "experience, specialization, education, and location."
            )

        # --------------------------------------------------
        # SKILL PATHWAY
        # --------------------------------------------------

        st.divider()

        st.header(
            "Your Current Skill Pathway"
        )

        primary_interest = profile["interests"][0]

        skill_pathways = {

            "Electrical Engineering": [
                "Circuit fundamentals",
                "Breadboarding",
                "Digital logic",
                "Arduino",
                "Python",
                "Embedded systems"
            ],

            "Mechanical Engineering": [
                "CAD",
                "Engineering design",
                "Mechanics",
                "3D printing",
                "Prototyping",
                "Manufacturing"
            ],

            "Computer Engineering": [
                "Python",
                "Digital logic",
                "Circuit design",
                "Arduino",
                "Embedded systems",
                "Computer architecture"
            ],

            "Computer Science": [
                "Python",
                "Algorithms",
                "Data structures",
                "Git and GitHub",
                "Web development",
                "Databases"
            ],

            "Artificial Intelligence": [
                "Python",
                "Data analysis",
                "Statistics",
                "Machine learning",
                "Model evaluation",
                "Data visualization"
            ],

            "Data Science": [
                "Python",
                "Pandas",
                "Statistics",
                "Data visualization",
                "SQL",
                "Machine learning"
            ],

            "Biomedical Engineering": [
                "Biology",
                "Engineering design",
                "CAD",
                "Data analysis",
                "Prototyping",
                "Biomechanics"
            ],

            "Biology": [
                "Experimental design",
                "Biology fundamentals",
                "Scientific writing",
                "Data analysis",
                "Laboratory research",
                "Statistics"
            ],

            "Physics": [
                "Algebra and calculus",
                "Mechanics",
                "Electricity and magnetism",
                "Python",
                "Mathematical modeling",
                "Experimental physics"
            ],

            "Mathematics": [
                "Algebra",
                "Calculus",
                "Probability",
                "Statistics",
                "Mathematical modeling",
                "Programming"
            ],

            "Environmental Science": [
                "Environmental systems",
                "Data collection",
                "Statistics",
                "GIS concepts",
                "Data analysis",
                "Environmental modeling"
            ],

            "Robotics": [
                "Python",
                "Electronics",
                "Arduino",
                "CAD",
                "Sensors",
                "Control systems"
            ],

            "Engineering": [
                "Engineering design process",
                "Technical drawing",
                "CAD",
                "Data analysis",
                "Prototyping",
                "Technical communication"
            ],

            "Not sure yet": [
                "Explore different STEM fields",
                "Try beginner coding",
                "Try an engineering project",
                "Analyze a dataset",
                "Explore science research",
                "Reflect on what you enjoyed most"
            ]
        }

        skills = skill_pathways.get(
            primary_interest,
            [
                "Problem solving",
                "Technical communication",
                "Research",
                "Data analysis",
                "Project design"
            ]
        )

        st.write(
            f"Current pathway: **{primary_interest}**"
        )

        st.write(
            "Use this as a suggested sequence. "
            "You do not need to learn everything at once."
        )

        for number, skill in enumerate(
            skills,
            start=1
        ):

            with st.container(border=True):

                st.write(
                    f"**Step {number} — {skill}**"
                )

    # --------------------------------------------------
    # OPPORTUNITIES
    # --------------------------------------------------

    elif page == "Opportunities":

        st.title("Opportunities")

        st.write(
            "Discover STEM programs and experiences that match "
            "your grade, borough, interests, goals, and accessibility preferences."
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
                    opportunity[
                        "boroughs_served"
                    ]
                ).split(";")
            ]

            return (
                profile["grade"] in eligible_grades
                and
                profile["borough"] in boroughs_served
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
                    opportunity[
                        "boroughs_served"
                    ]
                ).split(";")
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
                    opportunity[
                        "opportunity_type"
                    ]
                ) in opportunity_types:

                    score += 20

                    reasons.append(
                        "This matches an opportunity type you selected."
                    )

            max_score += 15

            if profile["financial_support"]:

                cost = str(
                    opportunity["cost"]
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
                        "This opportunity is free or offers financial support."
                    )

            else:
                score += 15

            max_score += 15

            if profile["borough"] in boroughs_served:

                score += 15

                reasons.append(
                    f"This opportunity serves students in the "
                    f"{profile['borough']}."
                )

            if profile["borough"] == "Bronx":

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
                (score / max_score) * 100
            )

            return percentage, reasons

        if profile["borough"] == "Bronx":

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
                    "More Bronx-focused opportunities will be added as the database grows."
                )

            else:

                for _, opportunity in featured.head(3).iterrows():

                    with st.container(border=True):

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
                            opportunity["url"],
                            use_container_width=True
                        )

            st.divider()

        st.header(
            "Recommended for You"
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

        st.header(
            "Browse All Opportunities"
        )

        for _, opportunity in opportunities.iterrows():

            if (
                opportunity_types
                and
                str(
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
                    opportunity["description"]
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
                        f"**Eligible Grades:** "
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
            "Use hands-on projects to explore your interests, "
            "practice technical skills, and build experience."
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

            "Biomedical Engineering": [
                (
                    "Beginner",
                    "Research a healthcare problem and design a possible engineering solution."
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
                    "Investigate a biological question using public scientific data."
                ),
                (
                    "Intermediate",
                    "Design a small controlled experiment."
                ),
                (
                    "Advanced",
                    "Complete and document an independent research project."
                )
            ],

            "Physics": [
                (
                    "Beginner",
                    "Create a simple motion or energy simulation."
                ),
                (
                    "Intermediate",
                    "Model a real physical system using Python."
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

                st.header(interest)

                for level, project in (
                    project_library[interest]
                ):

                    with st.container(border=True):

                        st.caption(level)

                        st.subheader(project)

        if not shown_projects:

            st.info(
                "More project recommendations for your selected interests "
                "will be added as the platform grows."
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
            "Verified external learning resources will be added gradually."
        )

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.subheader(
                    "💻 Programming"
                )

                st.write(
                    "Python • GitHub • Web Development • Data Analysis"
                )

            with st.container(border=True):

                st.subheader(
                    "⚙️ Engineering"
                )

                st.write(
                    "CAD • Electronics • Circuit Design • Arduino • Prototyping"
                )

        with col2:

            with st.container(border=True):

                st.subheader(
                    "🔬 Research"
                )

                st.write(
                    "Experimental Design • Data Collection • "
                    "Scientific Writing • Analysis"
                )

            with st.container(border=True):

                st.subheader(
                    "🎓 Career Exploration"
                )

                st.write(
                    "STEM Majors • Engineering Fields • "
                    "Research Careers • Technical Careers"
                )

    # --------------------------------------------------
    # PROFILE
    # --------------------------------------------------

    elif page == "My Profile":

        st.title("My Profile")

        st.subheader(full_name)

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

            st.header(
                "STEM Interests"
            )

            for interest in profile["interests"]:
                st.write(
                    f"• {interest}"
                )

            st.header(
                "Previous Experience"
            )

            if profile["experience_areas"]:

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

        with col2:

            st.header(
                "Goals"
            )

            for goal in profile["goals"]:
                st.write(
                    f"• {goal}"
                )

            st.header(
                "Current Exploration Stage"
            )

            st.write(
                profile["exploration_stage"]
            )

            st.write(
                f"**Weekly STEM goal:** "
                f"{profile['weekly_time']}"
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
