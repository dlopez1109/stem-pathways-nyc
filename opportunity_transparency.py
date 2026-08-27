"""Source-confidence eligibility, cost, stipend, and acceptance data.

Applied onto extra_opportunities in app.py. Does not change scoring logic.
last_verified: 2026-08-19
"""

TRANSPARENCY_DEFAULTS = {
    "eligibility_summary": "Check official eligibility",
    "eligible_grades": "",
    "age_requirements": "Not stated",
    "nyc_residency_required": "Not stated",
    "nyc_school_required": "Not stated",
    "borough_restrictions": "None stated",
    "citizenship_requirement": "Not stated",
    "income_requirement": "Not stated",
    "underrepresented_preference": "Not stated",
    "required_coursework": "Not stated",
    "gpa_requirement": "Not stated",
    "prior_program_requirement": "Not stated",
    "school_nomination_required": "No",
    "other_restrictions": "",
    "cost_category": "Unknown / check official site",
    "tuition_cost": "",
    "financial_aid_status": "Unknown / check official site",
    "scholarship_availability": "No aid stated",
    "stipend_status": "Unknown",
    "stipend_amount": "",
    "stipend_display": "Check official site",
    "acceptance_rate_confidence": "Not available",
    "acceptance_rate_source": "Not publicly reported",
    "last_verified": "2026-08-21",
}

# Card-facing source labels derived from acceptance_rate_confidence.
CONFIDENCE_SOURCE_LABEL = {
    "Official": "Official",
    "Calculated": "Calculated from official data",
    "Estimated — High confidence": "Unofficial estimate",
    "Estimated — Moderate confidence": "Unofficial estimate",
    "Estimated — Low confidence": "Unofficial estimate",
    "Not available": "",
}


def _free_funded():
    return {
        "cost": "Free",
        "cost_category": "Free",
        "tuition_cost": "None — program is free",
        "financial_aid": "Not needed — fully funded",
        "financial_aid_status": "Not needed — fully funded",
        "scholarship_availability": "Not needed — program is fully funded",
    }


def _not_reported():
    return {
        "acceptance_rate": "Not publicly reported",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not publicly reported",
    }


def _arise_fields():
    return {
        **_free_funded(),
        "financial_aid": "Not needed — program is fully funded / full scholarship",
        "financial_aid_status": "Not needed — program is fully funded / full scholarship",
        "scholarship_availability": "Not needed — program is fully funded / full scholarship",
        "eligibility_summary": "NYC high school students; rising juniors/seniors; full-time NYC residents; STEM interest required",
        "eligible_grades": "10;11",
        "grades": "10;11",
        "age_requirements": "Rising juniors and seniors",
        "age_range": "Rising juniors and seniors",
        "nyc_residency_required": "Yes — must be a full-time NYC resident",
        "nyc_school_required": "Yes — must attend an NYC school",
        "borough_restrictions": "None — all five boroughs",
        "citizenship_requirement": "Not stated as a separate published cutoff beyond NYC residency and NYC school enrollment",
        "income_requirement": "Not stated as a hard cutoff",
        "underrepresented_preference": "Program strongly encourages students from historically excluded groups in STEM",
        "required_coursework": "At least one year of high school science and one year of high school math",
        "gpa_requirement": "Not stated as a numeric cutoff",
        "prior_program_requirement": "Not required",
        "school_nomination_required": "No",
        "other_restrictions": "Must commit to the full 10-week program. Free Pinkerton-funded program. 2026 cohort: approximately 75 students.",
        "stipend_status": "Paid",
        "stipend_amount": "$2,000",
        "stipend": "$2,000 upon successful completion",
        "stipend_display": "$2,000 upon successful completion",
        "paid_status": "$2,000 stipend upon successful completion",
        "deadline": "February 27, 2026 at 5 PM",
        "internship_potential": "Yes — approximately 150 hours of mentored NYU lab research",
        "format": "Hybrid + in person — NYU Tandon, Brooklyn, NYC",
        "acceptance_rate": "Estimated 5–10%",
        "acceptance_rate_confidence": "Estimated — Moderate confidence",
        "acceptance_rate_source": "Not officially reported; highly competitive research program. Unofficial estimate based on the reported ~75-student cohort and secondary applicant reporting.",
        "requirements": "Rising junior or senior; full-time NYC resident; must attend an NYC school; at least one year of high school science and one year of high school math; full 10-week commitment.",
        "last_verified": "2026-08-23",
        "financial_aid": "Free program; provides support for accepted students (verify details)",
        "financial_aid_status": "Free program; provides support for accepted students (verify details)",
        "scholarship_availability": "Not needed — program is fully funded / full scholarship",
    }


TRANSPARENCY_UPDATES = {
    "Research Science Institute (RSI) at MIT": {
        **_free_funded(),
        "eligibility_summary": "Current 11th graders (rising seniors) • No NYC residency requirement",
        "eligible_grades": "11",
        "age_requirements": "No simple age cutoff published — current 11th graders only",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "International students may apply through CEE/country processes; U.S. applicants apply through CEE",
        "income_requirement": "Not stated",
        "required_coursework": "Strong STEM coursework expected; no single published course list",
        "gpa_requirement": "Not stated as a numeric cutoff",
        "school_nomination_required": "No",
        "other_restrictions": "High school seniors are not eligible. Current juniors only.",
        "stipend_status": "Not paid",
        "stipend_amount": "",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        "acceptance_rate": "~3% calculated",
        "acceptance_rate_confidence": "Calculated",
        "acceptance_rate_source": "Calculated from CEE guidance: about 50 U.S. students selected from 1,500+ U.S. applicants. CEE does not currently publish a single official rate.",
        "requirements": "Current 11th grader (rising senior); application, recommendations, and transcript; seniors are not eligible",
        "internship_potential": "Yes — full-time mentored lab research",
        "deadline": "Summer 2027 date not yet announced; 2026 deadline was December 10, 2025",
    },
    "Carnegie Mellon SAMS": {
        **_free_funded(),
        "eligibility_summary": "Current 11th graders • U.S. citizen or permanent resident • Age 16+",
        "eligible_grades": "11",
        "age_requirements": "16+ by program start",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or permanent resident",
        "income_requirement": "Not stated as a hard cutoff",
        "underrepresented_preference": "Program emphasizes students historically underrepresented in STEM",
        "school_nomination_required": "No",
        "other_restrictions": "Students typically cover travel to Pittsburgh",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        **_not_reported(),
        "acceptance_rate_source": "Carnegie Mellon does not publish an official SAMS acceptance rate.",
        "requirements": "Current 11th grader; age 16+ by start; U.S. citizen or permanent resident",
    },
    "Columbia Engineering the Next Generation (ENG)": {
        **_free_funded(),
        "eligibility_summary": "NYC students • Rising seniors • Work authorization required",
        "eligible_grades": "11",
        "age_requirements": "Must meet NYC work-eligibility requirements",
        "nyc_residency_required": "Yes — NYC students",
        "nyc_school_required": "Yes",
        "citizenship_requirement": "Must be legally allowed to work in NYC",
        "underrepresented_preference": "Bronx and NYC public-school students are a core audience",
        "prior_program_requirement": "FoR track requires prior work or volunteer experience",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_amount": "$17/hour (FoR track, 25 hours/week)",
        "stipend_display": "$17/hour stipend (FoR track)",
        "paid_status": "Paid — 2026 FoR stipend listed at $17/hour, 25 hours/week",
        **_not_reported(),
        "acceptance_rate_source": "Columbia ENG does not publish an official acceptance rate.",
        "requirements": "Current 11th grader/rising NYC senior; NYC school; legally allowed to work in NYC; FoR requires prior work or volunteer experience",
    },
    "Rockefeller University Jumpstart + SSRP": {
        **_free_funded(),
        "eligibility_summary": "NYC high school juniors and seniors • Age 16+",
        "eligible_grades": "11;12",
        "age_requirements": "16+ by program start",
        "nyc_residency_required": "Yes — NYC high school students",
        "nyc_school_required": "Yes",
        "citizenship_requirement": "Not stated as a separate published cutoff beyond school eligibility",
        "school_nomination_required": "No",
        "other_restrictions": "Full spring and summer commitment; selected applicants interview. Jumpstart supports 16 students.",
        "stipend_status": "Paid",
        "stipend_amount": "$3,750 total ($500 spring + $3,250 summer)",
        "stipend_display": "$3,750 stipend ($500 spring + $3,250 summer)",
        "paid_status": "Paid — official Jumpstart FAQ lists $500 spring and $3,250 summer",
        **_not_reported(),
        "acceptance_rate_source": "Rockefeller publishes a Jumpstart cohort of 16 students but does not publish applicant counts or an official acceptance rate.",
        "requirements": "NYC high school junior or senior; age 16+ at start; full spring/summer commitment; selected applicants interview",
    },
    "Columbia University Science Honors Program (SHP)": {
        "cost": "$900/year for new students beginning Fall 2026",
        "cost_category": "Tuition required",
        "tuition_cost": "$900/year for incoming students; $700/year for returning students (Fall 2026)",
        "financial_aid": "Available",
        "financial_aid_status": "Need-based program fee waivers available for documented financial hardship",
        "scholarship_availability": "Fee waivers may be granted after admission; applications considered regardless of need",
        "eligibility_summary": "Grades 10–12 • Live within 75 miles of Columbia",
        "eligible_grades": "10;11;12",
        "age_requirements": "Grade-based — apply while in grades 9–11 for the following year",
        "nyc_residency_required": "No — NY/NJ/CT students within 75 miles",
        "nyc_school_required": "No",
        "citizenship_requirement": "Not stated",
        "income_requirement": "Not required; hardship waivers available",
        "required_coursework": "Background in algebra, geometry, trigonometry, and probability plus elementary science",
        "school_nomination_required": "No — teacher recommendation required",
        "other_restrictions": "In-person Saturdays; students provide their own transportation. Entrance exam required.",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid",
        **_not_reported(),
        "acceptance_rate_source": "Columbia SHP does not publish an official acceptance rate.",
        "requirements": "Apply in grades 9–11 for the following year; live within 75 miles of campus; application, essay, transcript, recommendation, entrance exam; $50 application fee with hardship waiver option",
    },
    "AMNH Science Research Mentoring Program (SRMP)": {
        **_free_funded(),
        "eligibility_summary": "NYC students • Current 10th or 11th graders • Prior AMNH/partner pathway required",
        "eligible_grades": "10;11",
        "age_requirements": "Current 10th or 11th graders",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Yes",
        "prior_program_requirement": "Must meet AMNH prior-program or partner-school/program eligibility",
        "school_nomination_required": "Partner-program eligibility required",
        "stipend_status": "Paid",
        "stipend_amount": "$2,500",
        "stipend_display": "$2,500 stipend",
        "paid_status": "$2,500 stipend upon completion of research and program requirements",
        **_not_reported(),
        "acceptance_rate_source": "AMNH does not publish an official SRMP acceptance rate.",
        "requirements": "NYC student in current grade 10 or 11; passing classes; must meet AMNH prior-program or partner-school/program eligibility",
    },
    "New York Academy of Sciences Junior Academy": {
        **_free_funded(),
        "eligibility_summary": "Ages 13–17 • Open globally (virtual)",
        "eligible_grades": "9;10;11;12",
        "age_requirements": "13–17 during the program",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "Open internationally",
        "school_nomination_required": "No",
        "other_restrictions": "Comfortable communicating in English; parental/guardian consent; ~3–4 hours per week",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        **_not_reported(),
        "acceptance_rate_source": "NYAS states it receives thousands of applications worldwide but does not publish an official acceptance rate.",
        "requirements": "Age 13–17 during the program; strong STEM interest; comfortable reading, writing, and communicating in English; parental/guardian consent; ability to work on an international team",
        "internship_potential": "No — international team-based STEM innovation, research, design, and mentorship",
        "deadline": "Fall 2026 applications: April 1–July 9, 2026; future recruitment dates should be confirmed with NYAS",
    },
    "MITES Summer": {
        **_free_funded(),
        "eligibility_summary": "Current 11th graders (rising seniors) • U.S. citizen or permanent resident",
        "eligible_grades": "11",
        "age_requirements": "No simple published age cutoff — rising seniors",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or permanent resident",
        "underrepresented_preference": "Program is designed to broaden access to MIT for students from underrepresented and underserved backgrounds",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Unpaid / Free Program",
        **_not_reported(),
        "acceptance_rate_source": "MIT does not publish an official MITES Summer acceptance rate.",
        "requirements": "Current 11th grader / rising senior; U.S. citizen or permanent resident; application, recommendations, and academic information",
        "internship_potential": "No — academic STEM enrichment",
        "deadline": "Typically early February; 2027 date not yet announced",
    },
    "Columbia Engineering SHAPE": {
        "cost": "Tuition required: $6,241",
        "cost_category": "Tuition required",
        "tuition_cost": "$6,241 total program cost (2026)",
        "financial_aid": "Available",
        "financial_aid_status": "Need-based full scholarships available for domestic students",
        "scholarship_availability": "Limited full-cost need-based scholarships; NYC school Districts 5 and 6 prioritized",
        "eligibility_summary": "Rising sophomores through recent graduates • Open beyond NYC",
        "eligible_grades": "9;10;11;12",
        "age_requirements": "Typically 14–18; rising sophomores, juniors, seniors, and recent graduates",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "Financial aid is only available to domestic students and families",
        "income_requirement": "Aid is need-based for domestic students",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid",
        **_not_reported(),
        "acceptance_rate_source": "Columbia SHAPE does not publish an official acceptance rate.",
        "requirements": "Rising sophomore through recent high school graduate; application, essays, transcript/report card, recommendation, resume",
    },
    "NASA GISS / CCRI High School Research": {
        **_free_funded(),
        "eligibility_summary": "High school students • Project-specific eligibility",
        "eligible_grades": "10;11;12",
        "age_requirements": "Varies by project — check official eligibility",
        "nyc_residency_required": "Not required for all projects; NYC-area placements exist",
        "nyc_school_required": "No",
        "citizenship_requirement": "Some opportunities require U.S. citizenship",
        "gpa_requirement": "Some opportunities list GPA eligibility",
        "school_nomination_required": "No",
        "stipend_status": "Unknown",
        "stipend_display": "Varies by GISS/CCRI project; some placements are unpaid research",
        "paid_status": "Varies by project",
        **_not_reported(),
        "acceptance_rate_source": "NASA GISS / CCRI does not publish a single official high school acceptance rate.",
        "requirements": "Project-specific; some opportunities require U.S. citizenship and GPA eligibility",
    },
    "NASA Glenn High School Engineering Institute": {
        **_free_funded(),
        "eligibility_summary": "Upcoming juniors and seniors • Age 16+ • U.S. citizen or LPR",
        "eligible_grades": "11;12",
        "age_requirements": "16+ by program start",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or lawful permanent resident",
        "gpa_requirement": "GPA threshold listed on official materials — confirm current cycle",
        "school_nomination_required": "No — recommendation required",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid",
        **_not_reported(),
        "acceptance_rate_source": "NASA Glenn does not publish an official High School Engineering Institute acceptance rate.",
        "requirements": "Upcoming junior or senior; age requirement; GPA threshold; recommendation; U.S. citizenship or LPR",
    },
    "Learn & Earn": {
        **_free_funded(),
        "eligibility_summary": "NYC students • Ages 16–21 • Income/eligibility rules apply",
        "eligible_grades": "11;12",
        "age_requirements": "16–21",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Yes",
        "citizenship_requirement": "Must meet NYC work-eligibility rules",
        "income_requirement": "Income/eligibility requirements apply",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_amount": "",
        "stipend_display": "Paid internship — amount not published",
        "paid_status": "Paid internship component",
        **_not_reported(),
        "acceptance_rate_source": "DYCD does not publish an official Learn & Earn acceptance rate; placement is eligibility-based.",
        "requirements": "NYC junior/senior; age 16–21; income and work-eligibility requirements apply",
    },
    "Work, Learn & Grow": {
        **_free_funded(),
        "eligibility_summary": "NYC youth • Ages 16–21 • Prior-program eligibility can apply",
        "eligible_grades": "10;11;12",
        "age_requirements": "16–21",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Often required — confirm current cycle",
        "income_requirement": "Program-specific eligibility can apply",
        "prior_program_requirement": "Prior-program eligibility can apply",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_display": "Paid — amount not published",
        "paid_status": "Paid",
        **_not_reported(),
        "acceptance_rate_source": "DYCD does not publish an official Work, Learn & Grow acceptance rate.",
        "requirements": "NYC youth; age, school, and prior-program eligibility can apply",
    },
    "NYC Summer Youth Employment Program (SYEP)": {
        **_free_funded(),
        "eligibility_summary": "NYC residents • Ages 14–24 • Legally authorized to work",
        "eligible_grades": "9;10;11;12",
        "age_requirements": "14–24",
        "nyc_residency_required": "Yes — must live in one of the five boroughs",
        "nyc_school_required": "No for community-based SYEP; some school-based options require NYC DOE enrollment",
        "citizenship_requirement": "Must be legally allowed to work in the United States / NYC",
        "school_nomination_required": "No",
        "other_restrictions": "Community-based SYEP uses a randomized lottery. Additional requirements apply to Ladders for Leaders.",
        "stipend_status": "Paid",
        "stipend_amount": "New York State minimum wage",
        "stipend_display": "Paid — NYS minimum wage",
        "paid_status": "Paid",
        **_not_reported(),
        "acceptance_rate_source": "DYCD does not publish a single official SYEP acceptance rate; community-based placement is lottery-based.",
        "requirements": "Permanent NYC resident; age 14–24; legally allowed to work; required identity and eligibility documents",
    },
    "STEM Matters NYC": {
        **_free_funded(),
        "eligibility_summary": "NYC public school students • Eligibility varies by program",
        "eligible_grades": "9;10;11;12",
        "age_requirements": "Varies by individual STEM Matters offering",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Yes",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid",
        **_not_reported(),
        "acceptance_rate_source": "NYC Public Schools does not publish a single official STEM Matters acceptance rate; offerings vary.",
        "requirements": "NYC student; eligibility varies by individual program",
    },
    "NYU Tandon ARISE": {
        **_arise_fields()
    },
    "NYU ARISE": {
        **_arise_fields()
    },
    "Simons Summer Research Program": {
        "cost": "Free",
        "cost_category": "Free",
        "tuition_cost": "No tuition; residential housing/dining estimated at about $2,450 for summer 2026 if living on campus",
        "financial_aid": "Not needed — fully funded",
        "financial_aid_status": "Not needed — fully funded (tuition). Housing/dining billed separately for residential students.",
        "scholarship_availability": "Not needed for tuition — program is fully funded",
        "eligibility_summary": "Current 11th graders • U.S. citizen or permanent resident • School nomination required",
        "eligible_grades": "11",
        "age_requirements": "16+ by program start (no exceptions)",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or permanent resident",
        "school_nomination_required": "Yes — school nomination required; typically maximum of 2 nominees per school",
        "other_restrictions": "Students apply in 11th grade and participate the summer before senior year.",
        "stipend_status": "Paid",
        "stipend_amount": "",
        "stipend_display": "Stipend provided — amount not published",
        "paid_status": "Paid — stipend awarded at closing poster symposium; amount not published",
        "acceptance_rate": "about <5%",
        "acceptance_rate_confidence": "Official",
        "acceptance_rate_source": "Stony Brook Simons application guidelines: “Percentage of students admitted: about <5%”.",
        "requirements": "Current 11th grader; U.S. citizen or permanent resident; age 16+ by program start; school nomination required",
        "internship_potential": "Yes — full-time mentored university research",
        "deadline": "Summer 2027 date not yet announced; 2026 deadline was February 5, 2026",
    },
    "MSK HOPP Summer Student Program": {
        **_free_funded(),
        "eligibility_summary": "Current juniors • Live within 25 miles of MSK (NY/NJ/CT) • 3.5 science GPA",
        "eligible_grades": "11",
        "age_requirements": "14+ by program start (2026 materials specified 14+ by June 2026)",
        "nyc_residency_required": "No — NY/NJ/CT within 25 miles of MSK Manhattan campus",
        "nyc_school_required": "No",
        "citizenship_requirement": "Must be legally authorized to work in the U.S.",
        "gpa_requirement": "3.5 science GPA",
        "school_nomination_required": "No",
        "other_restrictions": "Full eight-week commitment. HOPP reports sponsoring over 20 students annually.",
        "stipend_status": "Paid",
        "stipend_amount": "$1,200",
        "stipend_display": "$1,200 stipend",
        "paid_status": "Paid — 2026 stipend was $1,200",
        "acceptance_rate": "~2% calculated",
        "acceptance_rate_confidence": "Calculated",
        "acceptance_rate_source": "Calculated from MSK reporting: about 20 interns selected from 1,000+ applications.",
        "requirements": "Current high school junior; live in NY/NJ/CT within 25 miles of MSK main campus; legally authorized to work in U.S.; 3.5 science GPA; full eight-week commitment",
    },
    "Columbia BRAINYAC": {
        **_free_funded(),
        "eligibility_summary": "NYC students • Grades 10–11 • Eligible partner program/school required",
        "eligible_grades": "10;11",
        "age_requirements": "Grade-based eligibility",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Yes — through an eligible partner program/school",
        "prior_program_requirement": "Must be enrolled in an eligible partner program/school such as S-PREP, BioBus, Lang Youth Medical, Columbia Secondary School, or Double Discovery Center",
        "school_nomination_required": "Partner-program pathway required",
        "stipend_status": "Paid",
        "stipend_amount": "",
        "stipend_display": "Stipend provided — amount not published",
        "paid_status": "Paid stipend — amount not publicly listed on current program page",
        **_not_reported(),
        "acceptance_rate_source": "Columbia BRAINYAC does not publish an official acceptance rate.",
        "requirements": "NYC resident in grade 10 or 11 and enrolled in an eligible partner program/school such as S-PREP, BioBus, Lang Youth Medical, Columbia Secondary School, or Double Discovery Center",
    },
    "MSK Bridge to Biostats Summer Program": {
        **_free_funded(),
        "eligibility_summary": "NYC students • Rising sophomores through seniors",
        "eligible_grades": "9;10;11",
        "age_requirements": "Rising sophomore through rising senior",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Yes",
        "required_coursework": "Interest in math, computing, or data science; recommendation and transcript required",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_amount": "",
        "stipend_display": "Stipend provided — amount not published",
        "paid_status": "Paid — current program page confirms paid participation; amount not publicly listed",
        **_not_reported(),
        "acceptance_rate_source": "MSK does not publish an official Bridge to Biostats acceptance rate.",
        "requirements": "NYC resident attending school in NYC; rising sophomore through rising senior; interest in math/computing/data science; recommendation and transcript",
        "internship_potential": "Yes — paid experiential learning in biostatistics and cancer data science",
        "deadline": "Summer 2027 date not yet announced; 2026 application closed February 27, 2026",
    },
    "Columbia YES in THE HEIGHTS": {
        **_free_funded(),
        "eligibility_summary": "High school students • Verify current neighborhood/grade eligibility",
        "eligible_grades": "10;11;12",
        "age_requirements": "High school students — check current cycle requirements",
        "nyc_residency_required": "Typically yes — confirm current neighborhood eligibility",
        "nyc_school_required": "Confirm current cycle",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_display": "Paid — 8 weeks full-time (35 hours/week); stipend amount not published",
        "paid_status": "Paid internship — 8 weeks at 35 hours/week; amount not published on the official page",
        **_not_reported(),
        "acceptance_rate_source": "Columbia YES in THE HEIGHTS does not publish an official acceptance rate.",
        "requirements": "Application materials include cover letter, resume, and full summer commitment; verify grade and neighborhood eligibility for current cycle",
    },
    "Columbia Secondary School Field Research Program (SSFRP)": {
        **_free_funded(),
        "eligibility_summary": "Current high school students • Age 16+ • Able to commute to Lamont",
        "eligible_grades": "9;10;11;12",
        "age_requirements": "16+ by internship start",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "school_nomination_required": "No",
        "other_restrictions": "Must be able to commute to Lamont-Doherty Earth Observatory in Palisades, NY; full six-week commitment",
        "stipend_status": "Unknown",
        "stipend_display": "Amount not published on the official SSFRP page",
        "paid_status": "Amount not published on the official SSFRP page",
        **_not_reported(),
        "acceptance_rate_source": "Columbia SSFRP does not publish an official acceptance rate.",
        "requirements": "Currently enrolled high school student; age 16+ by start; able to commute; full six-week commitment",
    },
    "Columbia BrainSTORM Mentorship Program": {
        **_free_funded(),
        "eligibility_summary": "High school students in grades 9–12 • Open nationwide",
        "eligible_grades": "9;10;11;12",
        "age_requirements": "High school students nationwide",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not publicly listed as a paid program",
        **_not_reported(),
        "acceptance_rate_source": "Columbia BrainSTORM does not publish an official acceptance rate.",
        "requirements": "High school student in grades 9–12; application includes research interests, personal statement, and resume/CV",
    },
    "MSK Science Enrichment Program (SEP)": {
        **_free_funded(),
        "eligibility_summary": "High school juniors • Partner-school nomination required • Biology completed",
        "eligible_grades": "11",
        "age_requirements": "High school juniors",
        "nyc_residency_required": "Typically NYC partner-school students",
        "nyc_school_required": "Yes — MSK SEP partner school",
        "required_coursework": "Completed a full year of biology",
        "school_nomination_required": "Yes — nominated by an MSK SEP partner school",
        "stipend_status": "Paid",
        "stipend_amount": "$4,200",
        "stipend_display": "$4,200 stipend",
        "paid_status": "Paid — current program page lists a total $4,200 stipend",
        **_not_reported(),
        "acceptance_rate_source": "MSK does not publish an official SEP acceptance rate.",
        "requirements": "High school junior; completed a full year of biology; must be nominated by an MSK SEP partner school",
    },
    "Rockefeller Summer Neuroscience Program (SNP)": {
        **_free_funded(),
        "eligibility_summary": "NYC public high school students • Age 16+",
        "eligible_grades": "10;11;12",
        "age_requirements": "16+ by program start",
        "nyc_residency_required": "Yes — NYC public high school students",
        "nyc_school_required": "Yes — NYC public high school",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        "internship_potential": "Research-focused program — students design experiments with mentors",
        **_not_reported(),
        "acceptance_rate_source": "Rockefeller SNP does not publish an official acceptance rate.",
        "requirements": "Must attend an NYC public high school and be at least 16 years old by program start",
    },
    "CUNY STEM Research Academy": {
        **_free_funded(),
        "eligibility_summary": "NYC public high school students • Campus-specific GPA/Regents rules",
        "eligible_grades": "10;11",
        "age_requirements": "Grade-based eligibility varies by CUNY campus",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Yes — NYC public high school",
        "gpa_requirement": "Varies by campus; may include GPA and Regents scores",
        "school_nomination_required": "No",
        "stipend_status": "Unknown",
        "stipend_display": "Check campus — amount not consistently published",
        "paid_status": "Check individual CUNY campus for current stipend details",
        **_not_reported(),
        "acceptance_rate_source": "CUNY does not publish a systemwide official acceptance rate. Campus cohort sizes (for example CCNY selecting 25 students for Spring 2026) are not the same as an acceptance rate.",
        "requirements": "NYC public high school student; requirements vary by campus and may include GPA, Regents scores, transcript, and writing sample",
    },
    "BioBus High School Junior Scientist Internship": {
        **_free_funded(),
        "eligibility_summary": "NYC high school students • Location-specific placements",
        "eligible_grades": "9;10;11;12",
        "age_requirements": "High school students — program-specific eligibility applies",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Yes",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_amount": "",
        "stipend_display": "Paid hourly — amount not published",
        "paid_status": "Paid hourly internship",
        **_not_reported(),
        "acceptance_rate_source": "BioBus reported a record number of 2026–27 applications but does not publish an official acceptance rate.",
        "requirements": "NYC high school student; specific location/program eligibility applies",
    },
    "Princeton AI4ALL": {
        **_free_funded(),
        "eligibility_summary": "Rising 11th graders • Low-income criteria • U.S. or Puerto Rico",
        "eligible_grades": "10",
        "age_requirements": "Rising 11th graders",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "Must live and attend high school in the U.S. or Puerto Rico",
        "income_requirement": "Must meet Princeton AI4ALL low-income criteria",
        "underrepresented_preference": "Low-income students; program aims to broaden participation in AI",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        **_not_reported(),
        "acceptance_rate_source": "Princeton AI4ALL does not publish an official acceptance rate.",
        "requirements": "Rising 11th grader living and attending high school in U.S. or Puerto Rico; must meet Princeton AI4ALL low-income criteria",
    },
    "NASA GeneLab for High Schools (GL4HS)": {
        **_free_funded(),
        "eligibility_summary": "Rising juniors/seniors • U.S. citizen or permanent resident • 3.0+ GPA",
        "eligible_grades": "10;11;12",
        "age_requirements": "Rising juniors, rising seniors, and eligible incoming college freshmen",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or permanent resident attending a U.S. high school",
        "required_coursework": "At least one high school biology course",
        "gpa_requirement": "3.0+ unweighted GPA",
        "school_nomination_required": "No",
        "other_restrictions": "Reliable computer and internet required (virtual program)",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        **_not_reported(),
        "acceptance_rate_source": "NASA GeneLab for High Schools does not publish an official acceptance rate.",
        "requirements": "U.S. citizen or permanent resident attending a U.S. high school; rising junior/senior; 3.0+ unweighted GPA; at least one high school biology course; reliable computer/internet",
    },
    "NASA STEM Enhancement in Earth Science (SEES) High School Summer Intern": {
        "cost": "Varies — scholarships and a $2,000 tuition option",
        "cost_category": "Varies — scholarships or $2,000 tuition",
        "tuition_cost": "Virtual: no cost. Scholarship on-site: tuition/housing/meals covered. Paid on-site option: $2,000 tuition including meals, housing, tours, and local travel.",
        "financial_aid": "Available",
        "financial_aid_status": "Full scholarships available (tuition, housing, meals); travel scholarships available; virtual participation is free",
        "scholarship_availability": "Full scholarships available; travel scholarships available and do not affect selection",
        "eligibility_summary": "Current sophomores and juniors • U.S. citizens only • Age 16+",
        "eligible_grades": "10;11",
        "age_requirements": "16 by July 5, 2026 (no exceptions for that cycle)",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizens only",
        "income_requirement": "Need is considered; students with limited STEM access are encouraged to apply",
        "underrepresented_preference": "Students with limited STEM access are encouraged to apply",
        "prior_program_requirement": "Previous SEES interns are not eligible to repeat as interns",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / scholarship or tuition-based internship",
        "acceptance_rate": "~11%",
        "acceptance_rate_confidence": "Calculated",
        "acceptance_rate_source": "Calculated from official SEES FAQ figures: about 215 accepted of ~2,000 applicants in 2024 (215 / 2,000 × 100 ≈ 10.8%).",
        "requirements": "U.S. citizen; current high school sophomore or junior (rising junior/senior); at least 16 by the on-site start date; cannot have been a SEES intern previously",
    },
    "Boston University RISE Internship": {
        "cost": "Tuition required: $5,930",
        "cost_category": "Tuition required",
        "tuition_cost": "2026: $5,930 tuition + $485 service fees; $75 application fee; residential room and board extra (about $3,978–$4,320)",
        "financial_aid": "Available",
        "financial_aid_status": "Limited need-based financial aid available",
        "scholarship_availability": "Limited need-based aid; not a full-scholarship program for all students",
        "eligibility_summary": "Rising seniors • U.S. citizen or permanent resident",
        "eligible_grades": "11",
        "age_requirements": "Entering senior year of high school",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or legal permanent resident",
        "income_requirement": "Aid is need-based and limited",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Tuition-based Program",
        **_not_reported(),
        "acceptance_rate_source": "BU states RISE places up to about 100 students in STEM labs but does not publish an official acceptance rate or applicant count.",
        "requirements": "Current high school junior entering senior year; U.S. citizen or permanent resident; application, transcript, essay, and recommendation",
    },
    "George Mason Aspiring Scientists Summer Internship Program (ASSIP)": {
        "cost": "Tuition required: $1,299",
        "cost_category": "Tuition required",
        "tuition_cost": "$1,299 tuition for 3 college credits (2025–2026 undergraduate tuition basis)",
        "financial_aid": "No aid stated",
        "financial_aid_status": "No aid stated on the official tuition page — confirm with the program",
        "scholarship_availability": "No aid stated",
        "eligibility_summary": "Age 15+ (16+ for wet lab) • High school and undergraduate",
        "eligible_grades": "10;11;12",
        "age_requirements": "15+ overall; 16+ typically required for in-person wet-lab placements",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "Not stated as a published cutoff on the main program page",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Tuition-based Program",
        **_not_reported(),
        "acceptance_rate_source": "George Mason ASSIP does not publish an official acceptance rate.",
        "requirements": "Students age 15+ (16+ for many wet-lab placements); application and mentor matching; exact eligibility varies by research placement",
    },
    "Stanford Institutes of Medicine Summer Research Program (SIMR)": {
        **_free_funded(),
        "financial_aid_status": "Not needed — fully funded. Limited need-based stipends for some students; $50 application fee with waivers if family income is under $80,000 or for special circumstances.",
        "eligibility_summary": "Current juniors and seniors • U.S. citizen or permanent resident • Age 16+",
        "eligible_grades": "11;12",
        "age_requirements": "16+ by program start (must also be a current junior or senior)",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or permanent resident living in the U.S. and attending high school in the U.S.",
        "income_requirement": "Need-based stipends considered if family AGI is under $80,000 or for other circumstances",
        "underrepresented_preference": "Strong preference for local Bay Area students (within about a 1-hour drive); commuter program with no housing",
        "school_nomination_required": "No",
        "other_restrictions": "Commuter only — no housing provided.",
        "stipend_status": "Limited / not guaranteed",
        "stipend_amount": "",
        "stipend_display": "Needs-based stipend possible — not guaranteed",
        "paid_status": "Limited need-based stipends; official 2026 materials say most students will not receive a stipend",
        **_not_reported(),
        "acceptance_rate_source": "Stanford SIMR does not publish an official acceptance rate.",
        "requirements": "High school junior or senior; 16+ by program start; living and attending high school in the U.S.; U.S. citizen or permanent resident",
    },
    "UCSB Research Mentorship Program (RMP)": {
        "cost": "Tuition required: $5,600",
        "cost_category": "Tuition required",
        "tuition_cost": "2026: $5,600 tuition and program fees; residential housing/meals about $7,599 extra; $75 application fee",
        "financial_aid": "Available",
        "financial_aid_status": "Limited need-based scholarships available; California residents prioritized",
        "scholarship_availability": "Limited need-based scholarships; not guaranteed",
        "eligibility_summary": "Grades 10–11 (exceptional 9th considered) • 3.80+ weighted GPA",
        "eligible_grades": "9;10;11",
        "age_requirements": "Primarily current 10th and 11th graders; exceptional 9th graders considered",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "Open to qualified students, including international applicants, per UCSB pre-college materials",
        "gpa_requirement": "Minimum 3.80 weighted academic GPA",
        "income_requirement": "Scholarships are need-based and limited",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Tuition-based Program",
        **_not_reported(),
        "acceptance_rate_source": "UCSB RMP does not publish an official acceptance rate.",
        "requirements": "High school student in grade 10 or 11; outstanding 9th graders may be considered; minimum 3.80 weighted academic GPA; full program commitment",
    },
    "Princeton Laboratory Learning Program (LLP)": {
        **_free_funded(),
        "eligibility_summary": "Local New Jersey high school students • Commuter only",
        "eligible_grades": "10;11;12",
        "age_requirements": "Project-specific age requirements apply",
        "nyc_residency_required": "No — local New Jersey students",
        "nyc_school_required": "No",
        "school_nomination_required": "No",
        "other_restrictions": "No housing or transportation provided; commuter research experience",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Unpaid / Free Research Experience",
        **_not_reported(),
        "acceptance_rate_source": "Princeton LLP does not publish an official acceptance rate.",
        "requirements": "Local New Jersey high school student; no housing or transportation provided; project-specific requirements apply",
    },
    "Brookhaven National Laboratory High School Research Program (HSRP)": {
        **_free_funded(),
        "eligibility_summary": "Typically after 11th grade • Age 16+ • U.S. citizen or permanent resident",
        "eligible_grades": "11;12",
        "age_requirements": "16+ by program start",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or lawful permanent resident",
        "school_nomination_required": "No — two recommendations required",
        "other_restrictions": "Commuter program; housing and transportation are not provided. Active health insurance required.",
        "stipend_status": "Unknown",
        "stipend_display": "None / Not paid — official HSRP page does not list a stipend",
        "paid_status": "None / Not paid — official HSRP page does not list a stipend",
        **_not_reported(),
        "acceptance_rate_source": "Brookhaven National Laboratory does not publish an official HSRP acceptance rate.",
        "requirements": "Recommended after completion of 11th grade; age 16+; U.S. citizen or permanent resident; health insurance; two recommendations; able to commute daily",
    },
    "Cold Spring Harbor Laboratory Partners for the Future": {
        **_free_funded(),
        "eligibility_summary": "Long Island students entering senior year • School nomination required",
        "eligible_grades": "11;12",
        "age_requirements": "Students entering senior year",
        "nyc_residency_required": "No — Long Island high school students",
        "nyc_school_required": "No",
        "school_nomination_required": "Yes — school science chair may nominate up to two students",
        "stipend_status": "Unknown",
        "stipend_display": "None / Not paid — official page does not list a stipend",
        "paid_status": "None / Not paid — official page does not list a stipend",
        **_not_reported(),
        "acceptance_rate_source": "CSHL does not publish an official acceptance rate. Each participating school science chair may nominate up to two students.",
        "requirements": "Long Island high school student entering senior year; must be nominated by school science chairperson",
    },
    "Cooper Union Summer STEM": {
        "cost": "3-week course $3,150; 6-week course $5,150",
        "cost_category": "Tuition required",
        "tuition_cost": "3-week course: $3,150; 6-week course: $5,150",
        "financial_aid": "Yes — full and partial need-based fee waivers available",
        "financial_aid_status": "Yes — full and partial need-based fee waivers available. Full waiver: household income at or below 100% of NYC Area Median Income. Partial or full waiver may be available up to 120% of NYC AMI. Priority for NYC public-school students and NYC residents. Aid is limited and not guaranteed.",
        "scholarship_availability": "Need-based full and partial fee waivers; limited and not guaranteed; priority for NYC public-school students and NYC residents",
        "eligibility_summary": "Students who completed grades 9, 10, or 11; international students may apply, but Cooper does not sponsor visas",
        "eligible_grades": "9;10;11",
        "grades": "9;10;11",
        "age_requirements": "Completed grades 9, 10, or 11; rising 9th graders and high school graduates are not eligible",
        "age_range": "Completed grades 9, 10, or 11",
        "nyc_residency_required": "No — open worldwide; NYC residents receive priority, especially for aid",
        "nyc_school_required": "No — NYC public-school enrollment helps with financial-aid priority",
        "citizenship_requirement": "International students may apply, but Cooper Union does not sponsor visas",
        "income_requirement": "Required only if applying for financial aid: full waiver at or below 100% NYC AMI; partial/full possible up to 120% NYC AMI",
        "school_nomination_required": "No",
        "other_restrictions": "In person at 41 Cooper Square; no housing provided. Cooper does not sponsor visas.",
        "stipend_status": "Not paid",
        "stipend_amount": "",
        "stipend": "None / Not paid",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "deadline": "March 27, 2026 at 11:59 PM ET",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "internship_potential": "No — college-level engineering and computer science courses and projects",
        "format": "In person — The Cooper Union, Manhattan, NYC",
        "acceptance_rate": "Not publicly reported",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Cooper Union does not publish applicant counts or an official Summer STEM acceptance rate. Official FAQs say typical classes enroll about 20–25 students (some lab sections 8–10).",
        "requirements": "Completed grades 9, 10, or 11; application and cycle-specific materials; some courses have additional math/science prerequisites. International students may apply, but Cooper does not sponsor visas.",
        "last_verified": "2026-08-21",
    },
    "Regeneron Science Talent Search": {
        **_free_funded(),
        "eligibility_summary": "U.S. high school seniors submitting original independent research",
        "eligible_grades": "12",
        "grades": "12",
        "age_requirements": "High school seniors",
        "age_range": "High school seniors",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "Must meet Society for Science Regeneron STS eligibility; confirm current-cycle rules on the official site",
        "school_nomination_required": "No",
        "other_restrictions": "Requires substantial original independent research, a research report, essays, transcript, and recommendations.",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid — awards up to $250,000 for top winners",
        "paid_status": "Not paid / Competition awards",
        "deadline": "November 5, 2026 at 8 PM ET",
        "internship_potential": "No — national independent-research competition",
        "format": "National competition",
        "acceptance_rate": "~12%",
        "acceptance_rate_confidence": "Calculated",
        "acceptance_rate_source": "Calculated from official 2026 Regeneron STS reporting: about 300 scholars named from around 2,600 entrants (300 / 2,600 × 100 ≈ 11.5%). Scholar selection is not the same as the later finalist round.",
        "requirements": "Original independent research; research report; application essays; transcript; recommendations",
    },
    "Congressional App Challenge": {
        **_free_funded(),
        "eligibility_summary": "Middle and high school students in a participating congressional district",
        "eligible_grades": "9;10;11;12",
        "grades": "9;10;11;12",
        "age_requirements": "Middle and high school students; confirm district rules",
        "age_range": "Middle and high school students",
        "nyc_residency_required": "No — compete in your congressional district",
        "nyc_school_required": "No",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Competition",
        "deadline": "October 26, 2026 at 12 PM ET",
        "internship_potential": "No — nationwide student app-building competition",
        "format": "Congressional district / national",
        **_not_reported(),
        "acceptance_rate_source": "The Congressional App Challenge does not publish a single national acceptance rate; students compete within participating districts.",
        "requirements": "Build an original app; register in a participating congressional district; follow district and competition rules",
    },
    "Diamond Challenge": {
        **_free_funded(),
        "eligibility_summary": "High school teams of 2–4 students ages 14–18 with an adult advisor",
        "eligible_grades": "9;10;11;12",
        "grades": "9;10;11;12",
        "age_requirements": "Ages 14–18",
        "age_range": "14–18",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid — awards available to advancing teams",
        "paid_status": "Not paid / Competition awards",
        "deadline": "January 14, 2027",
        "internship_potential": "No — global high school entrepreneurship competition",
        "format": "Global / virtual and live pitch options",
        **_not_reported(),
        "acceptance_rate_source": "The Diamond Challenge does not publish an official overall acceptance rate.",
        "requirements": "Team of 2–4 students ages 14–18; adult advisor; original venture concept and competition submission",
    },
    "MITES Semester": {
        **_free_funded(),
        "eligibility_summary": "Current 11th graders (rising seniors) • U.S. citizen or permanent resident",
        "eligible_grades": "11",
        "grades": "11",
        "age_requirements": "Rising seniors",
        "age_range": "Rising seniors",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or permanent resident",
        "underrepresented_preference": "Program is designed to broaden access to MIT for students from underrepresented and underserved backgrounds",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Unpaid / Free Program",
        "deadline": "Typically early February; 2027 date not yet announced",
        "internship_potential": "No — hybrid academic STEM enrichment",
        "format": "Hybrid — MIT",
        **_not_reported(),
        "acceptance_rate_source": "MIT does not publish an official MITES Semester acceptance rate. MITES Semester shares an application with MITES Summer.",
        "requirements": "Current 11th grader / rising senior; U.S. citizen or permanent resident; shares MITES Summer application requirements",
    },
    "MIT Beaver Works Summer Institute": {
        "cost": "Varies — free for qualifying families; otherwise tuition may apply",
        "cost_category": "Varies — free for qualifying families; otherwise tuition may apply",
        "tuition_cost": "Confirm current-cycle tuition on the official BWSI site; need-based support is offered",
        "financial_aid": "Available",
        "financial_aid_status": "Need-based support available; the program can be free for qualifying families",
        "scholarship_availability": "Need-based aid / free participation for qualifying families",
        "eligibility_summary": "Students entering senior year • Prerequisite online coursework required",
        "eligible_grades": "11",
        "grades": "11",
        "age_requirements": "Students entering 12th grade",
        "age_range": "Entering senior year",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "school_nomination_required": "No",
        "other_restrictions": "Students must register for and complete required online prerequisite coursework before the summer application.",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid",
        "deadline": "Summer application follows required prerequisite coursework",
        "internship_potential": "No — four-week project-based STEM institute",
        "format": "In person — MIT / MIT Lincoln Laboratory",
        **_not_reported(),
        "acceptance_rate_source": "MIT Beaver Works does not publish an official BWSI acceptance rate.",
        "requirements": "Register for prerequisite course; complete required online work; submit summer application and essays",
    },
    "Summer Science Program": {
        "cost": "Varies by family income",
        "cost_category": "Varies by family income",
        "tuition_cost": "Sliding-scale cost based on family income; SSP states that cost should not be a barrier",
        "financial_aid": "Available",
        "financial_aid_status": "Need-based / sliding-scale pricing; stipends may be available for students with high financial need",
        "scholarship_availability": "Need-based support and possible cash stipends for high financial need",
        "eligibility_summary": "Current 11th graders • Track-specific academic prerequisites",
        "eligible_grades": "11",
        "grades": "11",
        "age_requirements": "High school juniors",
        "age_range": "High school juniors",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "required_coursework": "Academic prerequisites depend on the research track",
        "school_nomination_required": "School nomination may be part of the process — confirm current cycle",
        "stipend_status": "Limited / not guaranteed",
        "stipend_display": "Need-based stipend possible — not guaranteed",
        "paid_status": "Limited need-based stipends possible",
        "deadline": "2027 application date not yet announced",
        "internship_potential": "Yes — intensive residential scientific research",
        "format": "Residential — multiple university campuses",
        **_not_reported(),
        "acceptance_rate_source": "SSP does not publish an official acceptance rate.",
        "requirements": "Current junior; track-specific academic prerequisites; full application and supporting materials",
    },
    "Garcia Summer Research Program": {
        "cost": "Tuition required: $4,000 lab fee",
        "cost_category": "Tuition required",
        "tuition_cost": "$4,000 laboratory usage fee (2026); housing extra",
        "financial_aid": "No aid stated",
        "financial_aid_status": "No aid stated",
        "scholarship_availability": "No aid stated",
        "eligibility_summary": "Ages 16+ • About 3.8 unweighted GPA • Strong STEM coursework",
        "eligible_grades": "10;11;12",
        "grades": "10;11;12",
        "age_requirements": "16+",
        "age_range": "16+",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "gpa_requirement": "Approximately 3.8 unweighted GPA",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Fee-based research program",
        "deadline": "Future cycle date not yet announced",
        "internship_potential": "Yes — intensive materials-science laboratory research",
        "format": "In person — Stony Brook University",
        **_not_reported(),
        "acceptance_rate_source": "The Garcia Center does not publish an official acceptance rate.",
        "requirements": "Age 16+; approximately 3.8 unweighted GPA; strong coursework; qualifying standardized scores; transcript; three recommendations",
    },
    "Rockefeller Summer Science Research Program": {
        **_free_funded(),
        "eligibility_summary": "Current juniors and seniors • Age 16+ • Full-time summer commitment",
        "eligible_grades": "11;12",
        "grades": "11;12",
        "age_requirements": "16+ by program start",
        "age_range": "16+ by program start",
        "nyc_residency_required": "Not required for all SSRP seats; Jumpstart pathway is NYC-focused",
        "nyc_school_required": "No",
        "school_nomination_required": "No",
        "stipend_status": "Unknown",
        "stipend_display": "Not publicly stated on the main SSRP page — Jumpstart students receive a published stipend",
        "paid_status": "Check official SSRP cycle details",
        "deadline": "2026 deadline was January 2, 2026; 2027 date not yet announced",
        "internship_potential": "Yes — full-time mentored laboratory research",
        "format": "In person — Rockefeller University, NYC",
        **_not_reported(),
        "acceptance_rate_source": "Rockefeller SSRP does not publish an official acceptance rate.",
        "requirements": "Current junior or senior; age 16+ by program start; full-time availability; application; recommendation",
    },
    "RockEDU Jumpstart": {
        **_free_funded(),
        "eligibility_summary": "NYC high school juniors and seniors • Age 16+",
        "eligible_grades": "11;12",
        "grades": "11;12",
        "age_requirements": "16+ by program start",
        "age_range": "16+ by program start",
        "nyc_residency_required": "Yes — NYC high school students",
        "nyc_school_required": "Yes",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_amount": "$3,750 total ($500 spring + $3,250 summer)",
        "stipend_display": "$3,750 stipend ($500 spring + $3,250 summer)",
        "paid_status": "Paid — official Jumpstart FAQ lists $500 spring and $3,250 summer",
        "deadline": "2026 Jumpstart deadline was January 2; 2027 date not yet announced",
        "internship_potential": "Yes — spring laboratory preparation plus full-time summer research",
        "format": "In person — Rockefeller University, NYC",
        **_not_reported(),
        "acceptance_rate_source": "Rockefeller publishes a Jumpstart cohort of 16 students but does not publish applicant counts or an official acceptance rate.",
        "requirements": "NYC high school junior or senior; age 16+ at start; full spring/summer commitment",
    },
    "Columbia SHAPE": {
        "cost": "Tuition required",
        "cost_category": "Tuition required",
        "tuition_cost": "About $6,241 total program cost (2026)",
        "financial_aid": "Available",
        "financial_aid_status": "Need-based full scholarships available for domestic students",
        "scholarship_availability": "Limited full-cost need-based scholarships; NYC school Districts 5 and 6 prioritized",
        "eligibility_summary": "Rising sophomores through recent graduates • Open beyond NYC",
        "eligible_grades": "9;10;11;12",
        "grades": "9;10;11;12",
        "age_requirements": "Typically 14–18; rising sophomores, juniors, seniors, and recent graduates",
        "age_range": "14–18",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "Financial aid is only available to domestic students and families",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid",
        "deadline": "2026 final deadline was March 2; 2027 date not yet announced",
        "internship_potential": "No — project-based pre-college engineering program",
        "format": "Commuter / residential — Columbia University",
        **_not_reported(),
        "acceptance_rate_source": "Columbia SHAPE does not publish an official acceptance rate.",
        "requirements": "Rising sophomore through recent high school graduate; application, essays, transcript/report card, recommendation, resume",
    },
    "Columbia Science Honors Program": {
        "cost": "Tuition required",
        "cost_category": "Tuition required",
        "tuition_cost": "$900/year for incoming students; $700/year for returning students (Fall 2026)",
        "financial_aid": "Available",
        "financial_aid_status": "Need-based program fee waivers available for documented financial hardship",
        "scholarship_availability": "Fee waivers may be granted after admission",
        "eligibility_summary": "Grades 10–12 • Live within 75 miles of Columbia",
        "eligible_grades": "10;11;12",
        "grades": "10;11;12",
        "age_requirements": "Grade-based — apply while in grades 9–11 for the following year",
        "age_range": "Grades 10–12",
        "nyc_residency_required": "No — NY/NJ/CT students within 75 miles",
        "nyc_school_required": "No",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid",
        "deadline": "Applications typically open in early February; next cycle date not yet announced",
        "internship_potential": "No — advanced Saturday academic enrichment",
        "format": "In person — Saturdays at Columbia University",
        **_not_reported(),
        "acceptance_rate_source": "Columbia SHP does not publish an official acceptance rate.",
        "requirements": "Apply in grades 9–11 for the following year; live within 75 miles of campus; application, essay, transcript, recommendation, entrance exam",
    },
    "MSK Summer Student Program": {
        **_free_funded(),
        "eligibility_summary": "Current juniors • Live within 25 miles of MSK (NY/NJ/CT) • 3.5 science GPA",
        "eligible_grades": "11",
        "grades": "11",
        "age_requirements": "14+ by program start",
        "age_range": "14+ by program start",
        "nyc_residency_required": "No — NY/NJ/CT within 25 miles of MSK Manhattan campus",
        "nyc_school_required": "No",
        "citizenship_requirement": "Must be legally authorized to work in the U.S.",
        "gpa_requirement": "3.5 science GPA",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_amount": "$1,200",
        "stipend_display": "$1,200 stipend",
        "paid_status": "Paid — 2026 stipend was $1,200",
        "deadline": "2026 application closed February 6, 2026; next cycle date not yet announced",
        "internship_potential": "Yes — independent mentored cancer research project",
        "format": "In person — Memorial Sloan Kettering, Manhattan, NYC",
        **_not_reported(),
        "acceptance_rate_source": "MSK reports sponsoring over 20 HOPP summer students annually but does not publish applicant counts or an official acceptance rate.",
        "requirements": "Current high school junior; live in NY/NJ/CT within 25 miles of MSK main campus; legally authorized to work in U.S.; 3.5 science GPA; full eight-week commitment",
    },
    "NASA GeneLab for High Schools": {
        **_free_funded(),
        "eligibility_summary": "Rising juniors/seniors • U.S. citizen or permanent resident • 3.0+ GPA",
        "eligible_grades": "10;11;12",
        "grades": "10;11;12",
        "age_requirements": "Rising juniors, rising seniors, and eligible incoming college freshmen",
        "age_range": "Rising juniors, rising seniors, or eligible incoming freshmen",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or permanent resident attending a U.S. high school",
        "required_coursework": "At least one high school biology course",
        "gpa_requirement": "3.0+ unweighted GPA",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        "deadline": "2026 closed March 15 or when 1,000 applications were reached; 2027 date not yet announced",
        "internship_potential": "Research training — space-biology and bioinformatics analysis",
        "format": "Virtual",
        **_not_reported(),
        "acceptance_rate_source": "NASA GeneLab for High Schools does not publish an official acceptance rate.",
        "requirements": "U.S. citizen or permanent resident attending a U.S. high school; rising junior/senior; 3.0+ unweighted GPA; at least one high school biology course; reliable computer/internet",
    },
    "Boston University RISE": {
        "cost": "Tuition required",
        "cost_category": "Tuition required",
        "tuition_cost": "2026: $5,930 tuition + $485 service fees; $75 application fee; residential room and board extra",
        "financial_aid": "Available",
        "financial_aid_status": "Limited need-based financial aid available",
        "scholarship_availability": "Limited need-based aid; not a full-scholarship program for all students",
        "eligibility_summary": "Rising seniors • U.S. citizen or permanent resident",
        "eligible_grades": "11",
        "grades": "11",
        "age_requirements": "Entering senior year of high school",
        "age_range": "Rising seniors",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "citizenship_requirement": "U.S. citizen or legal permanent resident",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Tuition-based Program",
        "deadline": "2026 application deadline was February 4, 2026; 2027 date not yet announced",
        "internship_potential": "Yes — approximately 40 hours/week of mentored research",
        "format": "Residential or commuter — Boston University",
        **_not_reported(),
        "acceptance_rate_source": "BU states RISE places up to about 100 students in STEM labs but does not publish an official acceptance rate or applicant count.",
        "requirements": "Current high school junior entering senior year; U.S. citizen or permanent resident; application, transcript, essay, and recommendation",
    },
    "CCNY STEM Research Academy": {
        **_free_funded(),
        "eligibility_summary": "NYC public high school 10th or 11th graders • Campus academic eligibility",
        "eligible_grades": "10;11",
        "grades": "10;11",
        "age_requirements": "Grade-based eligibility",
        "age_range": "Grades 10–11",
        "nyc_residency_required": "Yes",
        "nyc_school_required": "Yes — NYC public high school",
        "gpa_requirement": "Campus academic eligibility; transcript required",
        "school_nomination_required": "No",
        "stipend_status": "Paid",
        "stipend_amount": "$1,575 for 2026 summer researchers",
        "stipend_display": "$1,575 stipend for selected summer researchers",
        "paid_status": "Paid for selected summer researchers — 2026 amount was $1,575",
        "deadline": "2026 deadline was January 16; 2027 campus dates not yet announced",
        "internship_potential": "Yes — selected students conduct summer research with CUNY/CCNY faculty",
        "format": "In person — City College of New York",
        **_not_reported(),
        "acceptance_rate_source": "CCNY does not publish an official STEM Research Academy acceptance rate. Campus cohort sizes are not the same as an acceptance rate.",
        "requirements": "NYC public high school 10th or 11th grader; academic eligibility; transcript; 300–350 word essay; teacher recommendation",
    },
    "CCNY STEM Institute": {
        **_free_funded(),
        "eligibility_summary": "Middle and high school students • Eligibility varies by CCNY course",
        "eligible_grades": "9;10;11;12",
        "grades": "9;10;11;12",
        "age_requirements": "Varies by course or program",
        "age_range": "Varies by course",
        "nyc_residency_required": "Typically NYC students — confirm course listing",
        "nyc_school_required": "Often yes — confirm current offering",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        "deadline": "Varies by semester",
        "internship_potential": "No — STEM coursework and test-preparation enrichment",
        "format": "In person — City College of New York",
        **_not_reported(),
        "acceptance_rate_source": "CCNY STEM Institute offerings vary by semester and do not publish a single official acceptance rate.",
        "requirements": "Eligibility varies by course or program; application required",
    },
    "Baruch STEP Academy": {
        **_free_funded(),
        "eligibility_summary": "NYS students in grades 7–12 • Underrepresented in STEM or economically disadvantaged",
        "eligible_grades": "7;8;9;10;11;12",
        "grades": "7;8;9;10;11;12",
        "age_requirements": "Grades 7–12",
        "age_range": "Grades 7–12",
        "nyc_residency_required": "No — New York State resident",
        "nyc_school_required": "No — public, private, charter, or parochial schools accepted",
        "citizenship_requirement": "Must meet NYS STEP eligibility",
        "income_requirement": "Economically disadvantaged students may qualify via NYS opportunity-program income criteria",
        "underrepresented_preference": "African American, Latino, Native American, or Alaska Native students, or economically disadvantaged students",
        "gpa_requirement": "About 80–83 average in math, science, English, and cumulative GPA; research seminars may require a higher GPA",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Free Program",
        "deadline": "Summer 2026 deadline listed as May 15 (rolling to June 1); fall dates announced on the STEP site",
        "internship_potential": "Some research-course options; primarily STEM enrichment",
        "format": "In person — Baruch College, NYC",
        **_not_reported(),
        "acceptance_rate_source": "Baruch STEP does not publish an official acceptance rate.",
        "requirements": "NYS resident in grades 7–12; academic record; essays; transcript/report card; teacher evaluation; eligibility documentation",
    },
    "Einstein Enrichment Program": {
        **_free_funded(),
        "eligibility_summary": "Bronx students in grades 7–12 who live and attend school in the Bronx",
        "eligible_grades": "7;8;9;10;11;12",
        "grades": "7;8;9;10;11;12",
        "age_requirements": "Grades 7–12",
        "age_range": "Grades 7–12",
        "nyc_residency_required": "Yes — Bronx",
        "nyc_school_required": "Yes — must attend school in the Bronx",
        "borough_restrictions": "Bronx",
        "underrepresented_preference": "NYS STEP program for students historically underrepresented in STEM/health sciences",
        "school_nomination_required": "No",
        "stipend_status": "Unknown",
        "stipend_display": "Program-dependent — confirm current cycle",
        "paid_status": "Program-dependent",
        "deadline": "Varies — check Einstein pathway programs for current recruitment",
        "internship_potential": "STEM and health-science enrichment; research exposure varies by pathway",
        "format": "In person — Bronx / Albert Einstein College of Medicine",
        **_not_reported(),
        "acceptance_rate_source": "Einstein does not publish an official Enrichment Program acceptance rate.",
        "requirements": "Live and attend school in the Bronx; grades 7–12; must meet STEP/program eligibility",
    },
    "Einstein–Montefiore Summer High School Research Program": {
        "cost": "Confirm current cycle on the official Einstein page",
        "cost_category": "Confirm current cycle on the official Einstein page",
        "tuition_cost": "Not published on the current pathway listing",
        "financial_aid": "Not stated",
        "financial_aid_status": "Not stated on the current Einstein pathway listing",
        "scholarship_availability": "No aid stated",
        "eligibility_summary": "High school students age 16+ interested in science and medicine",
        "eligible_grades": "9;10;11;12",
        "grades": "9;10;11;12",
        "age_requirements": "16+",
        "age_range": "16+",
        "nyc_residency_required": "Not stated as a hard cutoff on the pathway listing; confirm current cycle",
        "nyc_school_required": "Confirm current cycle",
        "school_nomination_required": "No",
        "stipend_status": "Unknown",
        "stipend_display": "Amount not published on the current Einstein pathway listing",
        "paid_status": "Check current cycle",
        "deadline": "Dates vary by cycle; confirm on the official Einstein pathway page",
        "internship_potential": "Yes — five-week full-time summer laboratory research",
        "format": "In person — Albert Einstein College of Medicine / Montefiore",
        **_not_reported(),
        "acceptance_rate_source": "Einstein does not publish an official summer high school research acceptance rate.",
        "requirements": "Age 16+; program-specific application requirements",
    },
    "PROMYS": {
        "cost": "Tuition required: about $8,000",
        "cost_category": "Tuition required",
        "tuition_cost": "Up to about $8,000 before aid for the six-week residential program",
        "financial_aid": "Available",
        "financial_aid_status": "Full and partial need-based aid available; free for U.S. families with annual income under $80,000",
        "scholarship_availability": "Full/partial need-based aid plus named fellowships; international aid considered case by case",
        "eligibility_summary": "Ages 14–18 • Completed grade 9 • Not a full-time college student",
        "eligible_grades": "9;10;11;12",
        "grades": "9;10;11;12",
        "age_requirements": "14–18; must have completed grade 9",
        "age_range": "14–18",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "income_requirement": "Aid is need-based; U.S. families under $80,000 AGI attend free",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Tuition-based Program",
        "deadline": "February 27, 2026 for the 2026 cycle; 2027 date not yet announced",
        "internship_potential": "No — intensive residential mathematics program",
        "format": "Residential — Boston University",
        **_not_reported(),
        "acceptance_rate_source": "PROMYS does not publish an official acceptance rate.",
        "requirements": "Age 14–18; completed grade 9; challenging application problem set; transcript; short answers; mathematics recommendation",
    },
    "Stanford University Mathematics Camp (SUMaC)": {
        "cost": "Tuition required: $8,950 residential / $3,750 online",
        "cost_category": "Tuition required",
        "tuition_cost": "2026: $8,950 residential; $3,750 online",
        "financial_aid": "Available",
        "financial_aid_status": "Need-based financial aid available",
        "scholarship_availability": "Need-based aid; not guaranteed",
        "eligibility_summary": "Rising juniors and seniors with advanced mathematical preparation",
        "eligible_grades": "10;11",
        "grades": "10;11",
        "age_requirements": "Rising juniors and seniors",
        "age_range": "Rising juniors and seniors",
        "nyc_residency_required": "No",
        "nyc_school_required": "No",
        "required_coursework": "Advanced mathematical preparation beyond a typical high school curriculum",
        "school_nomination_required": "No",
        "stipend_status": "Not paid",
        "stipend_display": "Not paid",
        "paid_status": "Not paid / Tuition-based Program",
        "deadline": "2026 deadline was February 2; 2027 date not yet announced",
        "internship_potential": "No — intensive advanced mathematics camp",
        "format": "Residential or online — Stanford Pre-Collegiate Studies",
        **_not_reported(),
        "acceptance_rate_source": "Stanford SUMaC does not publish an official acceptance rate.",
        "requirements": "Advanced mathematical preparation; application and admissions assessment/materials as required by Stanford",
    },
    "CCNY CREST HIRES": {
        "eligibility_summary": "Must live in and attend school in NYC; entering 10th, 11th, or 12th grade",
        "financial_aid": "Not needed — fully funded",
        "financial_aid_status": "Not needed — fully funded / full scholarship",
        "stipend": "$1,000 stipend",
        "stipend_display": "$1,000 stipend plus 3 college credits",
        "paid_status": "$1,000 stipend upon completion",
        "acceptance_rate": "~25% calculated",
        "acceptance_rate_confidence": "Calculated",
        "acceptance_rate_source": "Calculated from the official HIRES FAQ: about 25 students are selected from a pool of nearly 100 NYC applications.",
        "deadline": "Typically January–March; 2026 deadline was March 15, 2026; 2027 date not yet announced",
        "last_verified": "2026-08-21"
    },
    "NYU Tandon ieSoSC": {
        "eligibility_summary": "NYC residents in grades 9–11",
        "cost": "Free",
        "cost_category": "Free",
        "financial_aid": "Not needed — fully funded / full scholarship",
        "financial_aid_status": "Not needed — fully funded / full scholarship",
        "stipend": "None / Not paid",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not publicly reported",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "NYU does not publish an official ieSoSC acceptance rate. A 2026 NYU Tandon announcement said the program served 38 NYC high school students; applicant count was not published.",
        "deadline": "Summer 2026 deadline was May 15, 2026; 2027 date not yet announced",
        "last_verified": "2026-08-21"
    },
    "New York Botanical Garden Science Internship": {
        "cost": "Free",
        "cost_category": "Free",
        "eligibility_summary": "NYC high school or undergraduate students; interest in plant science; ~5 hours/week during the school year",
        "stipend_display": "Paid hourly: $17/hour",
        "stipend_status": "Paid",
        "stipend_amount": "$17/hour",
        "paid_status": "Paid hourly: $17/hour — NYBG Science Intern posting",
        "financial_aid": "Not applicable",
        "financial_aid_status": "Not applicable — this is a paid internship",
        "acceptance_rate": "Not publicly reported",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "NYBG does not publish applicant counts or an official Science Internship acceptance rate. Seasonal paid postings are limited.",
        "deadline": "Postings vary by season; check NYBG careers and Sci Network NYC",
        "last_verified": "2026-08-21"
    },
    "GLOBE Program": {
        "cost": "Free",
        "cost_category": "Free",
        "financial_aid": "Not needed — program is fully funded",
        "financial_aid_status": "Not needed — program is fully funded",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not applicable — open citizen-science program",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "GLOBE is an open education and citizen-science program rather than a selective admissions process.",
        "deadline": "Ongoing; GLOBE Virtual Science Symposium cycles are posted on globe.gov",
        "last_verified": "2026-08-21"
    },
    "Perimeter Institute GoPhysics!": {
        "cost": "Free",
        "cost_category": "Free",
        "financial_aid": "Not needed — program is fully funded",
        "financial_aid_status": "Not needed — program is fully funded",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not publicly reported",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Perimeter Institute does not publish a GoPhysics! admissions rate. Its 2024/25 report says 21 GoPhysics! and Physica Phantastica workshops reached 548 students, without applicant counts.",
        "deadline": "Workshop dates are announced on the Perimeter site; July 2026 Gravity & Black Holes applications have closed",
        "last_verified": "2026-08-21"
    },
    "International Astronomical Search Collaboration (IASC)": {
        "cost": "Free",
        "cost_category": "Free",
        "financial_aid": "Not needed — program is fully funded",
        "financial_aid_status": "Not needed — program is fully funded",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not applicable — open campaign registration",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "IASC provides no-cost campaign participation rather than a published admissions rate.",
        "deadline": "Campaign-based; register on the official IASC site for upcoming search campaigns",
        "last_verified": "2026-08-21"
    },
    "Qubit by Qubit National High School Research Program": {
        "eligibility_summary": "Incoming 10th–12th graders or rising college freshmen",
        "cost": "Free for accepted Maryland students; $3,995 for students in other states",
        "cost_category": "Varies — free for Maryland students; otherwise tuition required",
        "tuition_cost": "Free for accepted students located in Maryland; $3,995 for students in other states (2026)",
        "financial_aid": "Yes — limited need-based scholarships available",
        "financial_aid_status": "Limited need-based scholarships available; Maryland students accepted to the quantum track attend free",
        "stipend": "None / Not paid",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not publicly reported",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Qubit by Qubit / The Coding School does not publish an official National High School Research Program acceptance rate. Offers are rolling until the course reaches capacity.",
        "deadline": "2026 priority deadline February 1, 2026; second priority deadline March 15, 2026; 2027 dates not yet announced",
        "last_verified": "2026-08-21"
    },
    "Canada/USA Mathcamp": {
        "cost": "Tuition required: $7,500 base fee before aid",
        "cost_category": "Tuition required",
        "tuition_cost": "$7,500 USD for Mathcamp 2026 before financial aid; final fee is $0–$7,500",
        "financial_aid": "Yes — need-based; Mathcamp meets 100% of demonstrated need",
        "financial_aid_status": "Need-based aid; Mathcamp states it meets 100% of demonstrated need. Free for U.S. and Canadian families with household income under $100,000 and typical assets.",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "~8% or below for new applicants",
        "acceptance_rate_confidence": "Official",
        "acceptance_rate_source": "Mathcamp’s published admissions statistic: in the last three years, 8% or below of new applicants were offered admission. About 65 new students and 55 returning alumni enroll each summer.",
        "deadline": "Mathcamp 2026 applications closed February 23, 2026 at 11:59 PM ET; 2027 date not yet announced",
        "last_verified": "2026-08-21"
    },
    "Ross Mathematics Program": {
        "cost": "Tuition required: $7,500",
        "cost_category": "Tuition required",
        "tuition_cost": "$7,500 program fee covering six weeks of tuition, room, and board",
        "financial_aid": "Yes — need-based aid for accepted students",
        "financial_aid_status": "Yes — Ross says it hopes to provide enough support for every accepted student who needs aid to attend",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "~15% estimated",
        "acceptance_rate_confidence": "Estimated — Moderate confidence",
        "acceptance_rate_source": "Ross has stated that in 2023 about 15% of applicants with complete applications were accepted. Ross does not currently publish a single official rate.",
        "deadline": "2026 deadline was March 8; 2027 date not yet announced",
        "last_verified": "2026-08-21"
    },
    "Hampshire College Summer Studies in Mathematics (HCSSiM)": {
        "cost": "Tuition required: $7,208 for 2026",
        "cost_category": "Tuition required",
        "tuition_cost": "$7,208 for the 2026 session",
        "financial_aid": "Yes — substantial need-based aid",
        "financial_aid_status": "Yes — need-based. Free for domestic students with household income under $85,000, including travel grants when needed. Aid is also considered for higher incomes and international students.",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "~5–7% calculated",
        "acceptance_rate_confidence": "Calculated",
        "acceptance_rate_source": "Calculated from the official Yellow Pig Math Foundation letter (Nov. 17, 2025): 51 students attended HCSSiM 2025 from over 1,100 applicants (~5%) and more than 700 Interesting Tests (~7%). HCSSiM does not publish a single official rate.",
        "deadline": "2026 new applications closed April 17, 2026 at 11:59 PM ET; Interesting Test due April 25, 2026; 2027 date not yet announced",
        "last_verified": "2026-08-21"
    },
    "MathILy": {
        "cost": "Tuition required: $6,175",
        "cost_category": "Tuition required",
        "tuition_cost": "$6,175 ($1,235/week) for 2026",
        "financial_aid": "Yes — MathILy states it will meet demonstrated financial need of every admitted student for 2026",
        "financial_aid_status": "Need-based; entire fee may be waived for significant need. Aid forms are given only after admission.",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "~9%",
        "acceptance_rate_confidence": "Official",
        "acceptance_rate_source": "MathILy 2025 Final Report: 62 students admitted from 690 completed applications, an admissions rate of about 9%.",
        "deadline": "2026 full-consideration deadline was April 28, 2026; 2027 date not yet announced",
        "last_verified": "2026-08-21"
    },
    "AMC 10": {
        "cost": "School registration: $55 early bird / $75 regular / $115 late, plus $30 per 10-student license bundle (2026–27). Many schools cover the student cost.",
        "cost_category": "School registration fee; often free to students",
        "tuition_cost": "Early bird $55 by Sept 30, 2026; regular $75 by Oct 15, 2026; late $115 by Oct 28, 2026; $30 per bundle of 10 student licenses",
        "financial_aid": "Schools may absorb fees; students usually do not pay MAA directly",
        "financial_aid_status": "No separate student aid form; many schools cover contest fees. Confirm with your competition manager.",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not applicable — contest, not an admissions program",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. AIME invitations typically go to at least the top 2.5% of AMC 10 A and B scorers.",
        "deadline": "AMC 10 A: November 5, 2026; AMC 10 B: November 13, 2026. School early-bird registration: September 30, 2026; regular: October 15, 2026.",
        "last_verified": "2026-08-21"
    },
    "AMC 12": {
        "cost": "School registration: $55 early bird / $75 regular / $115 late, plus $30 per 10-student license bundle (2026–27). Many schools cover the student cost.",
        "cost_category": "School registration fee; often free to students",
        "tuition_cost": "Early bird $55 by Sept 30, 2026; regular $75 by Oct 15, 2026; late $115 by Oct 28, 2026; $30 per bundle of 10 student licenses",
        "financial_aid": "Schools may absorb fees; students usually do not pay MAA directly",
        "financial_aid_status": "No separate student aid form; many schools cover contest fees. Confirm with your competition manager.",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not applicable — contest, not an admissions program",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. AIME invitations typically go to at least the top 5% of AMC 12 A and B scorers.",
        "deadline": "AMC 12 A: November 5, 2026; AMC 12 B: November 13, 2026. School early-bird registration: September 30, 2026; regular: October 15, 2026.",
        "last_verified": "2026-08-21"
    },
    "AIME": {
        "cost": "Free for invited students at participating schools",
        "cost_category": "Free for invited students",
        "financial_aid": "Not needed",
        "financial_aid_status": "Not needed — invited students take AIME through their school",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Invitation only after qualifying AMC 10/12 scores",
        "acceptance_rate_confidence": "Official",
        "acceptance_rate_source": "Invitation is based on official AMC 10/12 cutoffs (at least top 2.5% on AMC 10 and top 5% on AMC 12).",
        "deadline": "AIME I and AIME II 2027 dates are listed as TBD on the official MAA registration page",
        "last_verified": "2026-08-21"
    },
    "USAJMO": {
        "cost": "Free for invited students",
        "cost_category": "Free",
        "financial_aid": "Not needed",
        "financial_aid_status": "Not needed — invitation-only olympiad",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Invitation only — MAA selects about 500 students for USAMO and USAJMO combined",
        "acceptance_rate_confidence": "Official",
        "acceptance_rate_source": "Invitation-only. The MAA selects approximately 500 students for USAMO and USAJMO combined.",
        "deadline": "USAMO/USAJMO: March 20–21, 2027 (invite only)",
        "last_verified": "2026-08-21"
    },
    "USAMO": {
        "cost": "Free for invited students",
        "cost_category": "Free",
        "financial_aid": "Not needed",
        "financial_aid_status": "Not needed — invitation-only olympiad",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Invitation only — MAA selects about 500 students for USAMO and USAJMO combined",
        "acceptance_rate_confidence": "Official",
        "acceptance_rate_source": "Invitation-only. The MAA selects approximately 500 students for USAMO and USAJMO combined.",
        "deadline": "USAMO/USAJMO: March 20–21, 2027 (invite only)",
        "last_verified": "2026-08-21"
    },
    "Regeneron International Science and Engineering Fair (ISEF)": {
        "cost": "Free to compete at ISEF if selected by an affiliated fair; local fairs may charge registration fees",
        "cost_category": "Free at ISEF for selected finalists",
        "financial_aid": "Not needed at ISEF for selected finalists",
        "financial_aid_status": "Not needed at ISEF for selected finalists; check local-fair fees",
        "stipend_display": "None / Not paid — Regeneron ISEF 2026 awards exceeded $7 million",
        "paid_status": "Not paid / Competition awards",
        "acceptance_rate": "Not applicable — qualify through an affiliated fair",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Students do not apply to ISEF directly. ISEF 2026 gathered more than 1,700 finalists from 365 affiliate fairs.",
        "deadline": "NYC students must first enter the Terra NYC STEM Fair. Confirm 2027 ISEF dates on the official site.",
        "last_verified": "2026-08-21"
    },
    "Terra New York City STEM Fair": {
        "cost": "$50 regular student registration",
        "cost_category": "Registration fee required",
        "tuition_cost": "$50 regular registration; schools may pay by purchase order",
        "financial_aid": "Schools may cover the $50 registration fee by purchase order",
        "financial_aid_status": "No separate need-based waiver is published; schools may pay the $50 fee by purchase order",
        "stipend_display": "None / Not paid — awards and ISEF advancement",
        "paid_status": "Not paid / Competition",
        "acceptance_rate": "Not applicable — competition / ISEF qualifier",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. Advancement to Regeneron ISEF depends on placement and the fair’s ISEF allocation.",
        "deadline": "Cycle dates are posted on the Terra NYC ZFairs portal",
        "last_verified": "2026-08-21"
    },
    "NYC Envirothon": {
        "cost": "Free",
        "cost_category": "Free",
        "financial_aid": "Not needed — program is fully funded",
        "financial_aid_status": "Not needed — NYC covers state-competition travel/lodging for borough winners",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not applicable — school-team competition",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. Teams of 3–5 students represent a high school and advance by winning their borough, then the state.",
        "deadline": "NYC Envirothon 2026 was April 17, 2026; 2027 registration dates should be confirmed with NYC Soil & Water",
        "last_verified": "2026-08-21"
    },
    "Stockholm Junior Water Prize (U.S.)": {
        "cost": "Free",
        "cost_category": "Free",
        "financial_aid": "Not needed",
        "financial_aid_status": "Not needed — no entry fee published",
        "stipend_display": "None / Not paid — U.S. national winner receives a $10,000 scholarship and trip to Stockholm",
        "paid_status": "Not paid / Competition awards",
        "acceptance_rate": "Not applicable — state/national/international competition",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. One U.S. project is selected to compete internationally.",
        "deadline": "State deadlines vary. Confirm 2027 dates on the WEF SJWP page.",
        "last_verified": "2026-08-21"
    },
    "U.S. Physics Olympiad (F=ma / USAPhO)": {
        "cost": "School/proctor registration fee required; confirm current F=ma fee on the AAPT Physics Team site",
        "cost_category": "School registration fee",
        "financial_aid": "No separate student aid form is published; schools typically register and may cover fees",
        "financial_aid_status": "No published student fee-waiver form; ask your school contest manager whether the school covers F=ma registration",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not applicable — contest sequence",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. Roughly the top several hundred F=ma students are invited to USAPhO; about 20 students are invited to U.S. Physics Team camp.",
        "deadline": "2026 F=ma registration closed January 21, 2026 (exam February 12, 2026); USAPhO was April 10, 2026. Confirm 2027 dates on aapt.org/physicsteam.",
        "last_verified": "2026-08-21"
    },
    "AAPT PhysicsBowl": {
        "cost": "School registration required; student cost depends on the school",
        "cost_category": "School registration fee",
        "financial_aid": "No separate student aid form is published; schools typically register teams",
        "financial_aid_status": "No published student fee-waiver form; ask your physics teacher whether the school covers PhysicsBowl registration",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not applicable — school-team contest",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. Schools register teams and compete regionally.",
        "deadline": "2026 registration closed February 25, 2026; exam window was March 18–April 3, 2026. Confirm 2027 dates on the AAPT PhysicsBowl page.",
        "last_verified": "2026-08-21"
    },
    "Math Prize for Girls": {
        "eligibility_summary": "Female students in 11th grade or below (as of March 1 of the contest year) living in the U.S. or Canada who took an official AMC 10/12; top 300 applicants are invited",
        "cost": "Free to apply and compete",
        "cost_category": "Free",
        "tuition_cost": "None — no registration fee",
        "financial_aid": "Not needed — contest is free",
        "financial_aid_status": "Not needed — no registration fee",
        "stipend_display": "None / Not paid — contest prizes and recognition",
        "paid_status": "Not paid / Competition awards",
        "acceptance_rate": "About 300 contestants invited from applicants",
        "acceptance_rate_confidence": "Official",
        "acceptance_rate_source": "Official Math Prize site: the program invites the top 300 applicants based on AMC and related scores.",
        "deadline": "Math Prize 2026 application deadline was May 31, 2026. For 2027, take AMC 10/12 in November 2026, then apply when the official form opens.",
        "last_verified": "2026-08-21"
    },
    "Junior Science and Humanities Symposium (JSHS)": {
        "cost": "Free",
        "cost_category": "Free",
        "financial_aid": "Not needed — program is fully funded",
        "financial_aid_status": "Not needed — regional and national JSHS do not charge a student entry fee",
        "stipend_display": "None / Not paid — scholarships and awards at regional and national levels",
        "paid_status": "Not paid / Competition awards",
        "acceptance_rate": "Not applicable — regional research symposium",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. Students advance from regional symposia to National JSHS.",
        "deadline": "Regional deadlines vary; use the JSHS regional directory for New York dates",
        "last_verified": "2026-08-21"
    },
    "Science Olympiad": {
        "cost": "School/team membership and tournament fees set by the state chapter",
        "cost_category": "School/team fees",
        "financial_aid": "Varies by state chapter and school; many schools cover membership",
        "financial_aid_status": "Aid is school- and state-chapter-specific; ask your coach whether the school covers membership and tournament fees",
        "stipend_display": "None / Not paid",
        "paid_status": "None / Not paid",
        "acceptance_rate": "Not applicable — school-team competition",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. Division C is grades 9–12; teams qualify through invitational, regional, and state tournaments.",
        "deadline": "New York tournament dates are posted by the NY Science Olympiad chapter each year",
        "last_verified": "2026-08-21"
    },
    "eCYBERMISSION": {
        "cost": "Free",
        "cost_category": "Free",
        "financial_aid": "Not needed — program is fully funded",
        "financial_aid_status": "Not needed — no student entry fee",
        "stipend_display": "None / Not paid — mission-year prizes listed on the official AEOP/eCYBERMISSION site",
        "paid_status": "Not paid / Competition awards",
        "acceptance_rate": "Not applicable — open team competition",
        "acceptance_rate_confidence": "Not available",
        "acceptance_rate_source": "Not an admissions program. Teams of 2–4 students in grades 6–9 register with an adult advisor.",
        "deadline": "Mission-year dates are posted on usaeop.com/program/ecybermission",
        "last_verified": "2026-08-21"
    }
}


def _elig(
    summary,
    grades,
    age,
    nyc_res="No",
    nyc_school="No",
    citizen="Not stated as a published cutoff",
    income="Not stated as a hard cutoff",
    gpa="Not stated as a numeric cutoff",
    courses="Not stated as a published course list",
    nomination="No",
    **extra
):
    data = {
        "eligibility_summary": summary,
        "eligible_grades": grades,
        "grades": grades,
        "age_requirements": age,
        "age_range": age,
        "nyc_residency_required": nyc_res,
        "nyc_school_required": nyc_school,
        "citizenship_requirement": citizen,
        "income_requirement": income,
        "gpa_requirement": gpa,
        "required_coursework": courses,
        "school_nomination_required": nomination,
        "last_verified": "2026-08-21",
    }
    data.update(extra)
    return data


# Complete structured eligibility for every catalog program.
# Overlay values win over placeholders; they do not change scoring.
STRUCTURED_ELIGIBILITY = {
    "Research Science Institute (RSI) at MIT": _elig(
        "Current 11th graders (rising seniors) • No NYC residency requirement",
        "11", "No simple age cutoff published — current 11th graders only",
        citizen="International students may apply through CEE/country processes; U.S. applicants apply through CEE",
        courses="Strong STEM coursework expected; no single published course list",
        extra_restrictions="High school seniors are not eligible. Current juniors only.",
    ),
    "Carnegie Mellon SAMS": _elig(
        "Current 11th graders • U.S. citizen or permanent resident • Age 16+",
        "11", "16+ by program start",
        citizen="U.S. citizen or permanent resident",
        extra_underrepresented="Program emphasizes students historically underrepresented in STEM",
    ),
    "Columbia Engineering the Next Generation (ENG)": _elig(
        "NYC students • Rising seniors • Work authorization required",
        "11", "Must meet NYC work-eligibility requirements",
        nyc_res="Yes — NYC students", nyc_school="Yes",
        citizen="Must be legally allowed to work in NYC",
    ),
    "Rockefeller University Jumpstart + SSRP": _elig(
        "NYC high school juniors and seniors • Age 16+",
        "11;12", "16+ by program start",
        nyc_res="Yes — NYC high school students", nyc_school="Yes",
    ),
    "Columbia University Science Honors Program (SHP)": _elig(
        "Grades 10–12 • Live within 75 miles of Columbia",
        "10;11;12", "Grades 10–12",
        nyc_res="No — students may live within 75 miles of Columbia",
        courses="Strong science and math preparation expected",
    ),
    "AMNH Science Research Mentoring Program (SRMP)": _elig(
        "NYC students • Current 10th or 11th graders • Prior AMNH/partner pathway required",
        "10;11", "Current 10th or 11th graders",
        nyc_res="Yes — NYC students", nyc_school="Yes",
    ),
    "New York Academy of Sciences Junior Academy": _elig(
        "Students ages 13–17 worldwide; STEM interest required",
        "8;9;10;11;12", "Ages 13–17",
    ),
    "MITES Summer": _elig(
        "Current 11th graders; U.S. citizen, permanent resident, or MITES-eligible noncitizen",
        "11", "Current 11th graders / rising seniors",
        citizen="U.S. citizen, permanent resident, or eligible noncitizen as defined by MITES",
    ),
    "Columbia Engineering SHAPE": _elig(
        "Rising sophomores through recent graduates • Open beyond NYC",
        "9;10;11;12", "Rising sophomores through recent high school graduates",
    ),
    "NASA GISS / CCRI High School Research": _elig(
        "High school students; U.S. citizenship typically required for NASA research placements",
        "10;11;12", "High school; confirm current NASA age/grade rules",
        citizen="U.S. citizen preferred / confirm current NASA cycle",
    ),
    "NASA Glenn High School Engineering Institute": _elig(
        "U.S. high school students; U.S. citizenship required",
        "9;10;11;12", "High school",
        citizen="U.S. citizen",
    ),
    "Learn & Earn": _elig(
        "NYC youth • Work-eligible • Age and program-track rules apply",
        "9;10;11;12", "NYC youth employment age rules — typically 16+",
        nyc_res="Yes — NYC residency required", nyc_school="See current DYCD/provider rules",
        citizen="Must be eligible to work in NYC",
    ),
    "Work, Learn & Grow": _elig(
        "NYC youth • Ages 16–21 • Prior-program eligibility can apply",
        "10;11;12", "Ages 16–21",
        nyc_res="Yes — NYC youth",
        citizen="Must meet NYC youth-employment work-eligibility rules",
    ),
    "NYC Summer Youth Employment Program (SYEP)": _elig(
        "NYC youth ages 14–24 • Must be eligible to work in the U.S.",
        "9;10;11;12", "Ages 14–24",
        nyc_res="Yes — NYC residency required",
        citizen="Must be eligible to work in the U.S.",
    ),
    "STEM Matters NYC": _elig(
        "NYC public school students • Eligibility varies by program",
        "9;10;11;12", "NYC public school students — program-specific ages",
        nyc_res="Yes — NYC students", nyc_school="Yes — NYC public school required",
    ),
    "NYU Tandon ARISE": _elig(
        "Rising juniors and seniors; must be a full-time NYC resident and attend an NYC school",
        "10;11", "Rising juniors and seniors",
        nyc_res="Yes — must be a full-time NYC resident", nyc_school="Yes — must attend an NYC school",
        courses="At least one year of high school science and one year of high school math",
        extra_underrepresented="Program strongly encourages students from historically excluded groups in STEM",
    ),
    "Simons Summer Research Program": _elig(
        "Current 11th graders • U.S. citizen or permanent resident • School nomination required",
        "11", "Current 11th graders",
        citizen="U.S. citizen or permanent resident",
        nomination="Yes",
    ),
    "MSK HOPP Summer Student Program": _elig(
        "High school students age 14+ (18+ for some labs) • Strong science interest",
        "10;11;12", "Minimum age 14; some research groups require 18+",
        citizen="Must be authorized to work in the U.S.; confirm current MSK cycle rules",
        gpa="Strong academic record expected; confirm current numeric cutoff on the MSK page",
    ),
    "Columbia BRAINYAC": _elig(
        "NYC students • Grades 10–11 • Eligible partner program/school required",
        "10;11", "Grades 10–11",
        nyc_res="Yes — NYC students", nyc_school="Yes — partner program/school required",
    ),
    "MSK Bridge to Biostats Summer Program": _elig(
        "Rising seniors interested in biostatistics and quantitative biology",
        "11", "Rising seniors",
        courses="Interest in biostatistics / quantitative biology; confirm current MSK prerequisites",
    ),
    "Columbia YES in THE HEIGHTS": _elig(
        "High school students • Verify current neighborhood/grade eligibility",
        "9;10;11;12", "High school",
        nyc_res="Yes — NYC students; neighborhood eligibility can apply",
    ),
    "Columbia Secondary School Field Research Program (SSFRP)": _elig(
        "Current high school students • Age 16+ • Able to commute to Lamont",
        "10;11;12", "Age 16+",
    ),
    "Columbia BrainSTORM Mentorship Program": _elig(
        "High school students in grades 9–12 • Open nationwide",
        "9;10;11;12", "Grades 9–12",
    ),
    "MSK Science Enrichment Program (SEP)": _elig(
        "NYC-area high school students interested in cancer science; confirm current MSK cycle",
        "9;10;11;12", "High school",
    ),
    "Rockefeller Summer Neuroscience Program (SNP)": _elig(
        "NYC public high school students • Age 16+",
        "10;11;12", "Age 16+",
        nyc_res="Yes — NYC students", nyc_school="Yes — NYC public high school",
    ),
    "CUNY STEM Research Academy": _elig(
        "NYC public high school 10th or 11th graders • Campus academic eligibility",
        "10;11", "10th or 11th grade",
        nyc_res="Yes — NYC students", nyc_school="Yes — NYC public high school",
    ),
    "BioBus High School Junior Scientist Internship": _elig(
        "NYC high school students • Location-specific placements",
        "9;10;11;12", "High school",
        nyc_res="Yes — NYC high school students", nyc_school="Yes",
    ),
    "Princeton AI4ALL": _elig(
        "Rising 11th graders • Low-income criteria • U.S. or Puerto Rico",
        "10", "Rising 11th graders",
        citizen="U.S. or Puerto Rico",
        income="Low-income eligibility criteria apply",
        extra_underrepresented="Program is designed for students underrepresented in AI",
    ),
    "NASA GeneLab for High Schools (GL4HS)": _elig(
        "U.S. high school students; U.S. citizenship required",
        "9;10;11;12", "High school",
        citizen="U.S. citizen",
        courses="Biology and interest in space biology / bioinformatics; confirm current NASA prerequisites",
    ),
    "NASA STEM Enhancement in Earth Science (SEES) High School Summer Intern": _elig(
        "U.S. high school students; U.S. citizenship required",
        "9;10;11;12", "High school",
        citizen="U.S. citizen",
    ),
    "Boston University RISE Internship": _elig(
        "Rising seniors • U.S. citizen or permanent resident",
        "11", "Rising seniors",
        citizen="U.S. citizen or permanent resident",
    ),
    "George Mason Aspiring Scientists Summer Internship Program (ASSIP)": _elig(
        "Age 15+ (16+ for wet lab) • High school and undergraduate",
        "10;11;12", "Age 15+; 16+ for wet lab",
    ),
    "Stanford Institutes of Medicine Summer Research Program (SIMR)": _elig(
        "Current juniors and seniors • U.S. citizen or permanent resident • Age 16+",
        "11;12", "Age 16+",
        citizen="U.S. citizen or permanent resident",
        income="Application-fee waiver if family income is under $80,000 or for special circumstances",
    ),
    "UCSB Research Mentorship Program (RMP)": _elig(
        "Grades 10–11 (exceptional 9th considered) • 3.80+ weighted GPA",
        "10;11", "Grades 10–11; exceptional 9th graders may be considered",
        gpa="3.80+ weighted GPA",
    ),
    "Princeton Laboratory Learning Program (LLP)": _elig(
        "Local New Jersey high school students • Commuter only",
        "10;11;12", "High school",
        nyc_res="No — local New Jersey students",
    ),
    "Brookhaven National Laboratory High School Research Program (HSRP)": _elig(
        "Typically after 11th grade • Age 16+ • U.S. citizen or permanent resident",
        "11", "Age 16+",
        citizen="U.S. citizen or permanent resident",
    ),
    "Cold Spring Harbor Laboratory Partners for the Future": _elig(
        "Long Island students entering senior year • School nomination required",
        "11", "Entering senior year",
        nomination="Yes",
        nyc_res="No — Long Island students",
    ),
    "Cooper Union Summer STEM": _elig(
        "Students who completed grades 9, 10, or 11; international students may apply, but Cooper does not sponsor visas",
        "9;10;11", "Completed grades 9, 10, or 11; rising 9th graders and graduates are not eligible",
        nyc_res="No — open worldwide; NYC residents receive aid priority",
        nyc_school="No — NYC public-school enrollment helps with financial-aid priority",
        citizen="International students may apply; Cooper Union does not sponsor visas",
        income="Aid only: full waiver at or below 100% NYC AMI; partial/full possible up to 120% NYC AMI",
        courses="Course-specific math/science prerequisites; confirm the current Summer STEM course list",
        gpa="No published overall GPA cutoff; some courses have subject-specific achievement expectations",
    ),
    "Regeneron Science Talent Search": _elig(
        "U.S. high school seniors submitting original independent research",
        "12", "High school seniors",
        citizen="Must meet Society for Science Regeneron STS eligibility; confirm current-cycle rules",
    ),
    "Congressional App Challenge": _elig(
        "Middle and high school students in a participating congressional district",
        "9;10;11;12", "Middle and high school students; confirm district rules",
    ),
    "Diamond Challenge": _elig(
        "High school teams of 2–4 students ages 14–18 with an adult advisor",
        "9;10;11;12", "Ages 14–18",
    ),
    "MITES Semester": _elig(
        "Current 11th graders; shares the MITES application",
        "11", "Current 11th graders / rising seniors",
        citizen="U.S. citizen, permanent resident, or eligible noncitizen as defined by MITES",
    ),
    "MIT Beaver Works Summer Institute": _elig(
        "Students entering 12th grade; required online prerequisite coursework before summer selection",
        "11", "Entering senior year",
    ),
    "Summer Science Program": _elig(
        "Current 11th graders • Track-specific academic prerequisites",
        "11", "Current 11th graders",
        courses="Track-specific academic prerequisites",
    ),
    "Garcia Summer Research Program": _elig(
        "Ages 16+ • About 3.8 unweighted GPA • Strong STEM coursework",
        "10;11;12", "Ages 16+",
        gpa="About 3.8 unweighted GPA expected",
        courses="Strong STEM coursework",
    ),
    "Rockefeller Summer Science Research Program": _elig(
        "Current juniors and seniors • Age 16+ • Full-time summer commitment",
        "11;12", "Age 16+",
        nyc_res="See current Rockefeller eligibility; Jumpstart is NYC-focused",
    ),
    "CCNY STEM Institute": _elig(
        "Middle and high school students • Eligibility varies by CCNY course",
        "6;7;8;9;10;11;12", "Middle and high school — course-specific",
        nyc_res="Typically NYC students; confirm the current CCNY course",
    ),
    "Baruch STEP Academy": _elig(
        "NYS students in grades 7–12 • Underrepresented in STEM or economically disadvantaged",
        "7;8;9;10;11;12", "Grades 7–12",
        nyc_res="No — New York State students",
        income="Must be underrepresented in STEM or economically disadvantaged under NYS STEP rules",
        extra_underrepresented="NYS STEP eligibility: underrepresented in STEM or economically disadvantaged",
    ),
    "Einstein Enrichment Program": _elig(
        "Bronx students in grades 7–12 who live and attend school in the Bronx",
        "7;8;9;10;11;12", "Grades 7–12",
        nyc_res="Yes — Bronx residency required",
        nyc_school="Yes — Bronx school required",
    ),
    "Einstein–Montefiore Summer High School Research Program": _elig(
        "High school students age 16+ interested in science and medicine",
        "10;11;12", "Age 16+",
    ),
    "PROMYS": _elig(
        "Ages 14–18 • Completed grade 9 • Not a full-time college student",
        "9;10;11;12", "Ages 14–18; completed grade 9",
        citizen="Open to students worldwide; confirm current-cycle details",
        income="No income cutoff to apply; free for U.S. families with annual income under $80,000",
        courses="Problem-solving and algebra readiness; no calculus prerequisite",
    ),
    "Stanford University Mathematics Camp (SUMaC)": _elig(
        "Rising juniors and seniors with advanced mathematical preparation",
        "10;11", "Rising juniors and seniors",
        courses="Advanced mathematical preparation beyond a typical high school curriculum",
    ),
    "CCNY CREST HIRES": _elig(
        "Must live in and attend school in NYC; entering 10th, 11th, or 12th grade",
        "10;11;12", "Entering 10th, 11th, or 12th grade",
        nyc_res="Yes — must live in NYC", nyc_school="Yes — must attend school in NYC",
    ),
    "NYU Tandon ieSoSC": _elig(
        "NYC residents in grades 9–11",
        "9;10;11", "NYC residents entering grades 9–11; recent NYU materials also describe students ages 15+",
        nyc_res="Yes — NYC residents",
        nyc_school="Not stated separately beyond NYC residency",
    ),
    "New York Botanical Garden Science Internship": _elig(
        "NYC high school or undergraduate students; interest in plant science; ~5 hours/week during the school year",
        "9;10;11;12", "High school or undergraduate",
        nyc_res="Yes — NYC students", nyc_school="Yes — enrolled in a NYC high school or undergraduate program",
        courses="Interest in plant science; lab roles require safety training",
    ),
    "GLOBE Program": _elig(
        "Join through a GLOBE school, teacher, or community program; students worldwide may participate",
        "6;7;8;9;10;11;12", "K–12 through a GLOBE school or community program",
    ),
    "Perimeter Institute GoPhysics!": _elig(
        "High school students; Gravity & Black Holes requires completion of or enrollment in Grade 11 Physics",
        "9;10;11;12", "Grade-based: Exoplanets & the Universe for grades 9–10; Gravity & Black Holes for grades 11–12",
        citizen="Open internationally for online workshops",
        courses="Gravity & Black Holes requires completion of or enrollment in Grade 11 Physics",
    ),
    "International Astronomical Search Collaboration (IASC)": _elig(
        "Student or school citizen-science teams can register for asteroid-search campaigns",
        "9;10;11;12", "High school and college students; teacher- or group-led teams are the usual entry path",
    ),
    "Qubit by Qubit National High School Research Program": _elig(
        "Incoming 10th–12th graders or rising college freshmen",
        "10;11;12", "Incoming 10th–12th graders and rising college freshmen",
        income="Maryland students attend free; limited need-based scholarships for other states",
        courses="No published course prerequisite; 200+ word statement of interest required",
    ),
    "Canada/USA Mathcamp": _elig(
        "Students ages 13–18 worldwide; Qualifying Quiz, recommendations, and essays required",
        "8;9;10;11;12", "Ages 13–18; for 2026, birth dates between August 2, 2007 and June 28, 2013",
        citizen="Open worldwide",
        income="No income cutoff to apply; free for U.S./Canadian families under $100,000 with typical assets",
        courses="Comfort with high-school algebra, geometry, trigonometry, exponents, and logarithms; calculus is not required",
    ),
    "Ross Mathematics Program": _elig(
        "Pre-college students passionate about mathematics; typically ages 15–18",
        "9;10;11;12", "Typically 15–18 for first-year students",
        income="No income cutoff to apply; need-based aid available after admission",
        courses="Strong high-school math preparation; English fluency for international students",
    ),
    "Hampshire College Summer Studies in Mathematics (HCSSiM)": _elig(
        "Talented, highly motivated high school students; application plus the HCSSiM Interesting Test",
        "9;10;11;12", "Talented, highly motivated high school students",
        income="No income cutoff to apply; free for domestic students with household income under $85,000",
        courses="The HCSSiM Interesting Test is the academic screen; no published course list",
    ),
    "MathILy": _elig(
        "Mathematically talented high school students",
        "9;10;11;12", "High school students; others may be considered but high-school students take precedence",
        income="No income cutoff to apply; MathILy states it will meet demonstrated need of every admitted student",
        courses="Exam Assessing Readiness; no single published high-school course list",
    ),
    "AMC 10": _elig(
        "Grade 10 or below and under 17.5 on contest day; U.S./Canada students must be enrolled full-time at an accredited school or homeschool",
        "9;10", "Grade 10 or below and under 17.5 years old on contest day",
        citizen="U.S./Canada students must be enrolled full-time at an accredited school or homeschool",
        courses="Contest mathematics through geometry and algebra 2; no calculus",
    ),
    "AMC 12": _elig(
        "Grade 12 or below and under 19.5 on contest day; U.S./Canada students must be enrolled full-time at an accredited school or homeschool",
        "9;10;11;12", "Grade 12 or below and under 19.5 years old on contest day",
        citizen="U.S./Canada students must be enrolled full-time at an accredited school or homeschool",
        courses="Full high-school math curriculum except calculus",
    ),
    "AIME": _elig(
        "Invitation only after qualifying AMC 10 or AMC 12 scores",
        "9;10;11;12", "Must first qualify from AMC 10 or AMC 12 under MAA age/grade rules",
        citizen="Same school-enrollment rules as AMC 10/12",
        courses="Invitation based on AMC performance",
    ),
    "USAJMO": _elig(
        "Invitation only; U.S. or Canada full-time accredited school or homeschool enrollment required",
        "9;10", "Must qualify through AMC/AIME; generally via AMC 10",
        citizen="U.S. or Canada full-time accredited school or homeschool enrollment required",
    ),
    "USAMO": _elig(
        "Invitation only; U.S. or Canada full-time accredited school or homeschool enrollment required",
        "9;10;11;12", "Must qualify through AMC/AIME under MAA rules",
        citizen="U.S. or Canada enrollment required for the contest; U.S. citizen/PR needed later for IMO/MOP selection",
    ),
    "Regeneron International Science and Engineering Fair (ISEF)": _elig(
        "Grades 9–12; not age 20 by May 1 preceding ISEF; must be selected by an ISEF-affiliated fair",
        "9;10;11;12", "Grades 9–12 or equivalent and not yet age 20 on or before May 1 preceding ISEF",
        nomination="No — qualify through an affiliated fair rather than a school nomination form",
        extra_restrictions="NYC students typically qualify through Terra NYC STEM Fair. Team projects may have at most three members.",
    ),
    "Terra New York City STEM Fair": _elig(
        "Grades 9–12 attending school in NYC (all five boroughs), including homeschool",
        "9;10;11;12", "Grades 9–12",
        nyc_res="Not a separate residency rule; students must attend school in NYC",
        nyc_school="Yes — NYC school (including homeschool in NYC)",
    ),
    "NYC Envirothon": _elig(
        "NYC high school teams; typically grades 9–12 through a school or club",
        "9;10;11;12", "High school",
        nyc_res="Yes — NYC students", nyc_school="Yes — NYC school team",
    ),
    "Stockholm Junior Water Prize (U.S.)": _elig(
        "U.S. public, private, or independent high school students in grades 9–12",
        "9;10;11;12", "Grades 9–12",
        citizen="U.S. public, private, or independent high school students",
    ),
    "U.S. Physics Olympiad (F=ma / USAPhO)": _elig(
        "F=ma: U.S. citizen, permanent resident, or currently attending a U.S. school, and meet AAPT age/grade rules",
        "9;10;11;12", "High school; confirm current AAPT Physics Team age rules",
        citizen="U.S. citizen, permanent resident, or currently attending a U.S. school — confirm current AAPT Physics Team rules",
        courses="Physics contest; calculus-based mechanics appears on later USAPhO rounds",
    ),
    "AAPT PhysicsBowl": _elig(
        "High school students taking physics; school team registration required",
        "9;10;11;12", "High school physics students",
        courses="Currently taking or have taken a high school physics course",
        nomination="No — school registers a team",
    ),
    "Math Prize for Girls": _elig(
        "High school girls in the U.S. and Canada; contest-day grade/age rules apply",
        "9;10;11;12", "High school; confirm current Advantage Testing Foundation rules",
        extra_underrepresented="Contest is for girls",
    ),
    "Junior Science and Humanities Symposium (JSHS)": _elig(
        "High school students with original STEM research; enter through the regional JSHS",
        "9;10;11;12", "High school",
        nomination="No — school or teacher sponsorship is typical for regional entry",
    ),
    "Science Olympiad": _elig(
        "Join a school Science Olympiad team; Division C is grades 9–12",
        "9;10;11;12", "Division C: grades 9–12",
        nomination="No — school team membership",
    ),
    "eCYBERMISSION": _elig(
        "Students in grades 6–9; teams of 2–4 with an adult Team Advisor",
        "6;7;8;9", "Grades 6–9",
    ),
}

# Move helper-only keys onto schema fields.
for _name, _row in list(STRUCTURED_ELIGIBILITY.items()):
    if "extra_restrictions" in _row:
        _row["other_restrictions"] = _row.pop("extra_restrictions")
    if "extra_underrepresented" in _row:
        _row["underrepresented_preference"] = _row.pop("extra_underrepresented")


NAME_ALIASES = {
    "NYU ARISE": "NYU Tandon ARISE",
    "Columbia SHAPE": "Columbia Engineering SHAPE",
    "Columbia Science Honors Program": "Columbia University Science Honors Program (SHP)",
    "Rockefeller Summer Neuroscience Program": "Rockefeller Summer Neuroscience Program (SNP)",
    "RockEDU Jumpstart": "Rockefeller University Jumpstart + SSRP",
    "MSK Summer Student Program": "MSK HOPP Summer Student Program",
    "NASA GeneLab for High Schools": "NASA GeneLab for High Schools (GL4HS)",
    "Boston University RISE": "Boston University RISE Internship",
    "CCNY STEM Research Academy": "CUNY STEM Research Academy",
}


PLACEHOLDER_VALUES = {
    "",
    "nan",
    "none",
    "check official eligibility",
    "unknown / check official site",
    "not publicly reported",
    "check official site",
    "not specified",
    "no aid stated",
    "not stated",
    "check official cycle details",
    "check official current-cycle details",
    "check official 2027 cycle details",
}


def _lookup_transparency_update(name):
    if name in TRANSPARENCY_UPDATES:
        return TRANSPARENCY_UPDATES[name]

    alias = NAME_ALIASES.get(name)
    if alias and alias in TRANSPARENCY_UPDATES:
        return TRANSPARENCY_UPDATES[alias]

    return {}


def _est(rate, confidence, source):
    return {
        "acceptance_rate": rate,
        "acceptance_rate_confidence": confidence,
        "acceptance_rate_source": source,
    }


# Unofficial rates compiled from secondary reporting, program-quoted
# cohort/applicant figures, and commonly cited estimates. These are
# applied only when an official or calculated rate is not already set.
ACCEPTANCE_ESTIMATES = {
    "MITES Summer": _est(
        "~1.5–4% estimated",
        "Estimated — Moderate confidence",
        "Unofficial estimate from secondary reports, including a commonly cited ~62 of ~4,100 figure; MIT does not publish an official rate."
    ),
    "MITES Semester": _est(
        "~1.5–4% estimated",
        "Estimated — Moderate confidence",
        "Shares the MITES Summer application. Unofficial MITES Summer estimates are typically ~1.5–4%; MIT does not publish an official rate."
    ),
    "Research Science Institute (RSI) at MIT": _est(
        "~2–4% estimated",
        "Estimated — High confidence",
        "Unofficial estimate based on CEE’s ~100-student cohort and commonly reported applicant volumes of about 3,000; CEE does not publish a current official rate."
    ),
    "Carnegie Mellon SAMS": _est(
        "~5–10% estimated",
        "Estimated — Low confidence",
        "Unofficial secondary estimates around ~7%; Carnegie Mellon does not publish an official SAMS rate."
    ),
    "Summer Science Program": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "Secondary sources disagree (about 4–5% in some guides, 10–15% in others); SSP does not publish an official rate."
    ),
    "MIT Beaver Works Summer Institute": _est(
        "~10–20% estimated",
        "Estimated — Low confidence",
        "Selectivity varies by BWSI course. Unofficial reporting places many courses in a roughly 10–20% range; MIT does not publish a single official rate."
    ),
    "PROMYS": _est(
        "~8–12% estimated",
        "Estimated — Moderate confidence",
        "Unofficial estimate based on a commonly cited cohort of about 80 students and secondary reports around 10%; PROMYS does not publish an official rate."
    ),
    "Stanford University Mathematics Camp (SUMaC)": _est(
        "~5–10% estimated",
        "Estimated — Moderate confidence",
        "Unofficial secondary estimates commonly fall around 5–7%; Stanford does not publish an official SUMaC rate."
    ),
    "Garcia Summer Research Program": _est(
        "~10–15% estimated",
        "Estimated — Moderate confidence",
        "Unofficial secondary estimates commonly cite about 10–15%; Garcia does not publish an official rate."
    ),
    "Stanford Institutes of Medicine Summer Research Program (SIMR)": _est(
        "~3–5% estimated",
        "Estimated — Moderate confidence",
        "Multiple secondary sources commonly estimate SIMR around 3–5%; Stanford does not publish an official rate."
    ),
    "UCSB Research Mentorship Program (RMP)": _est(
        "~3–5% estimated",
        "Estimated — Moderate confidence",
        "Secondary reporting describes a cohort of about 75–100 and an implied rate under 5%; UCSB does not publish an official rate."
    ),
    "Boston University RISE Internship": _est(
        "~8–15% estimated",
        "Estimated — Moderate confidence",
        "Unofficial secondary estimates commonly fall around 8–15%; BU does not publish an official rate."
    ),
    "Boston University RISE": _est(
        "~8–15% estimated",
        "Estimated — Moderate confidence",
        "Unofficial secondary estimates commonly fall around 8–15%; BU does not publish an official rate."
    ),
    "George Mason Aspiring Scientists Summer Internship Program (ASSIP)": _est(
        "~8–12% estimated",
        "Estimated — Low confidence",
        "Unofficial secondary estimates commonly cite about 10%; George Mason does not publish an official rate."
    ),
    "Columbia Engineering SHAPE": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "No official rate. Wide unofficial estimate for this tuition-based pre-college program based on secondary descriptions of selectivity."
    ),
    "Columbia SHAPE": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "No official rate. Wide unofficial estimate for this tuition-based pre-college program based on secondary descriptions of selectivity."
    ),
    "Columbia University Science Honors Program (SHP)": _est(
        "~15–25% estimated",
        "Estimated — Low confidence",
        "SHP is highly selective and historically enrolls a few hundred students; Columbia does not publish applicant counts or an official rate."
    ),
    "Columbia Science Honors Program": _est(
        "~15–25% estimated",
        "Estimated — Low confidence",
        "SHP is highly selective and historically enrolls a few hundred students; Columbia does not publish applicant counts or an official rate."
    ),
    "AMNH Science Research Mentoring Program (SRMP)": _est(
        "~15–30% estimated",
        "Estimated — Low confidence",
        "AMNH has reported selecting about 60 mentoring students from a larger preparatory pipeline; no current official applicant-to-admit rate is published."
    ),
    "Columbia BRAINYAC": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Official materials describe a small cohort (about 14–20 students) drawn only from partner programs; Columbia does not publish an official rate."
    ),
    "Columbia Engineering the Next Generation (ENG)": _est(
        "~10–20% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this selective paid NYC engineering research program; Columbia does not publish an official rate."
    ),
    "Rockefeller University Jumpstart + SSRP": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "Jumpstart supports 16 students. Unofficial estimate from cohort size and selectivity reporting; Rockefeller does not publish applicant counts."
    ),
    "RockEDU Jumpstart": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "Jumpstart supports 16 students. Unofficial estimate from cohort size and selectivity reporting; Rockefeller does not publish applicant counts."
    ),
    "Rockefeller Summer Science Research Program": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for Rockefeller SSRP; the university does not publish an official rate."
    ),
    "Rockefeller Summer Neuroscience Program": _est(
        "~15–30% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this short NYC public-school neuroscience program; Rockefeller does not publish an official rate."
    ),
    "Rockefeller Summer Neuroscience Program (SNP)": _est(
        "~15–30% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this short NYC public-school neuroscience program; Rockefeller does not publish an official rate."
    ),
    "MSK HOPP Summer Student Program": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "MSK reports sponsoring over 20 students annually. Unofficial estimate from cohort size; applicant count is not published."
    ),
    "MSK Summer Student Program": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "MSK reports sponsoring over 20 students annually. Unofficial estimate from cohort size; applicant count is not published."
    ),
    "MSK Bridge to Biostats Summer Program": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this selective paid NYC data-science program; MSK does not publish an official rate."
    ),
    "MSK Science Enrichment Program (SEP)": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Partner-school nomination required. Unofficial estimate among nominated students; MSK does not publish an official rate."
    ),
    "NASA Glenn High School Engineering Institute": _est(
        "~10–15% estimated",
        "Estimated — High confidence",
        "Unofficial/official-adjacent: an OAI report said 60 of 400+ applicants were selected, and a 2026 NASA STEM Engagement quote put the rate around 10% with about 700 applicants."
    ),
    "NASA GISS / CCRI High School Research": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "Project-based NASA research placements are typically very selective; NASA GISS does not publish a single official rate."
    ),
    "NASA GeneLab for High Schools": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "The 2026 cycle capped applications around 1,000. Unofficial estimate; NASA does not publish an official GL4HS rate."
    ),
    "NASA GeneLab for High Schools (GL4HS)": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "The 2026 cycle capped applications around 1,000. Unofficial estimate; NASA does not publish an official GL4HS rate."
    ),
    "New York Academy of Sciences Junior Academy": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "NYAS says it receives thousands of applications worldwide. Unofficial estimate; no official rate is published."
    ),
    "Princeton AI4ALL": _est(
        "~5–15% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this free, income-restricted residential AI program; Princeton does not publish an official rate."
    ),
    "Princeton Laboratory Learning Program (LLP)": _est(
        "~10–20% estimated",
        "Estimated — Low confidence",
        "Local New Jersey commuter research placements are limited. Unofficial estimate; Princeton does not publish an official rate."
    ),
    "Brookhaven National Laboratory High School Research Program (HSRP)": _est(
        "~10–20% estimated",
        "Estimated — Low confidence",
        "Secondary reports describe a small cohort of about 20–25 students. Unofficial estimate; BNL does not publish an official rate."
    ),
    "Cold Spring Harbor Laboratory Partners for the Future": _est(
        "~20–50% estimated",
        "Estimated — Low confidence",
        "Each participating school may nominate up to two students. Unofficial estimate among nominees; CSHL does not publish an official rate."
    ),
    "CCNY STEM Research Academy": _est(
        "~20–40% estimated",
        "Estimated — Low confidence",
        "Campus materials have cited small spring cohorts (for example 25 students). Unofficial estimate; no official rate is published."
    ),
    "CUNY STEM Research Academy": _est(
        "~20–40% estimated",
        "Estimated — Low confidence",
        "Campus cohorts are small and vary. Unofficial estimate; CUNY does not publish a systemwide official rate."
    ),
    "CCNY STEM Institute": _est(
        "~40–70% estimated",
        "Estimated — Low confidence",
        "More accessible CCNY enrichment with course-by-course capacity. Unofficial estimate; no official rate is published."
    ),
    "Baruch STEP Academy": _est(
        "~20–40% estimated",
        "Estimated — Low confidence",
        "NYS STEP programs are selective on academics and eligibility. Unofficial estimate; Baruch does not publish an official rate."
    ),
    "Einstein Enrichment Program": _est(
        "~20–40% estimated",
        "Estimated — Low confidence",
        "Bronx STEP program with academic/eligibility screens. Unofficial estimate; Einstein does not publish an official rate."
    ),
    "Einstein–Montefiore Summer High School Research Program": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this 16+ summer lab research program; Einstein does not publish an official rate."
    ),
    "BioBus High School Junior Scientist Internship": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "BioBus reported a record number of applications. Unofficial estimate; no official rate is published."
    ),
    "Columbia YES in THE HEIGHTS": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this selective Columbia cancer-research internship; no official rate is published."
    ),
    "Columbia Secondary School Field Research Program (SSFRP)": _est(
        "~15–30% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this Lamont field/lab research program; Columbia does not publish an official rate."
    ),
    "Columbia BrainSTORM Mentorship Program": _est(
        "~15–30% estimated",
        "Estimated — Low confidence",
        "Unofficial estimate for this nationwide high school neurology mentorship; Columbia does not publish an official rate."
    ),
    "Learn & Earn": _est(
        "~40–80% estimated",
        "Estimated — Low confidence",
        "Primarily eligibility-based NYC DYCD placement rather than a national research contest. Unofficial estimate; no official rate is published."
    ),
    "Work, Learn & Grow": _est(
        "~40–80% estimated",
        "Estimated — Low confidence",
        "Primarily eligibility-based NYC DYCD placement. Unofficial estimate; no official rate is published."
    ),
    "NYC Summer Youth Employment Program (SYEP)": _est(
        "~50–75% estimated",
        "Estimated — Low confidence",
        "Community-based SYEP is lottery/placement-based and capacity varies by year. Unofficial estimate; DYCD does not publish a single official rate."
    ),
    "STEM Matters NYC": _est(
        "~30–70% estimated",
        "Estimated — Low confidence",
        "Acceptance varies widely by individual STEM Matters offering. Unofficial blended estimate; NYC Public Schools does not publish a single rate."
    ),
    "Congressional App Challenge": _est(
        "1 winner per participating district",
        "Estimated — High confidence",
        "Official contest structure: students compete in their congressional district and one winning app is selected per participating district. There is no single national percentage."
    ),
    "Diamond Challenge": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "First round is relatively open; advancing to later pitch rounds is more selective. Unofficial estimate; no official overall rate is published."
    ),
    "Cooper Union Summer STEM": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Cooper FAQs say typical classes enroll about 20–25 students (some lab sections 8–10). Unofficial estimate based on small cohort size and competitive NYC STEM demand."
    ),
    "NYU Tandon ieSoSC": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Not officially reported. A 2026 NYU Tandon announcement said the program served 38 NYC high school students; applicant count was not published. Unofficial estimate for this free selective STEM enrichment program."
    ),
    "New York Botanical Garden Science Internship": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Seasonal paid NYBG postings are limited. Unofficial estimate based on competitiveness of NYC paid science internships."
    ),
    "Perimeter Institute GoPhysics!": _est(
        "~20–40% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Perimeter’s 2024/25 report says 21 GoPhysics! and Physica Phantastica workshops reached 548 students, without applicant counts. Unofficial estimate."
    ),
    "Qubit by Qubit National High School Research Program": _est(
        "~25–50% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Offers are rolling until the course reaches capacity. Unofficial estimate for a competitive online research course rather than a tiny residential cohort."
    ),
    "MIT PRIMES-USA": _est(
        "~5–15% estimated",
        "Estimated — Moderate confidence",
        "Not officially reported. PRIMES-USA is a highly competitive remote research program with a limited cohort for students outside Greater Boston. Unofficial estimate based on MIT PRIMES selectivity."
    ),
    "ACS Project SEED": _est(
        "~20–40% estimated",
        "Estimated — Low confidence",
        "Not officially reported. SEED placements depend on local lab capacity and income eligibility. Unofficial estimate for this national paid research fellowship."
    ),
    "Urban Barcode Research Program (UBRP)": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "Not officially reported. UBRP is a competitive paid NYC DNA-barcode research program with a limited summer cohort. Unofficial estimate."
    ),
    "Urban Barcode Project (UBP)": _est(
        "~30–60% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Team-based NYC-metro classroom research with free lab access for selected teams. Unofficial estimate based on capacity rather than ultra-elite admissions."
    ),
    "Barcode Long Island": _est(
        "~30–60% estimated",
        "Estimated — Low confidence",
        "Not officially reported. School-team DNA barcoding program for Brooklyn/Queens/Long Island. Unofficial estimate based on training-slot capacity."
    ),
    "New York Bioforce": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Competitive NYCDOE biotech pathway with a paid summer internship via SYEP. Unofficial estimate."
    ),
    "Jackson Laboratory Summer Student Program": _est(
        "~5–12% estimated",
        "Estimated — Moderate confidence",
        "Not officially reported. Highly competitive residential biomedical research program with stipend, room, board, and travel. Unofficial estimate based on national research-internship competitiveness."
    ),
    "NYU GSTEM Summer Research Program": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Selective NYU Tandon summer research program for current juniors; tuition-based with need-based aid. Unofficial estimate."
    ),
    "Navy Science and Engineering Apprenticeship Program (SEAP)": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Competitive DoD lab apprenticeships for U.S. citizen high school students; capacity varies by lab. Unofficial estimate."
    ),
    "AEOP High School Internships": _est(
        "~10–30% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Army Educational Outreach Program placements depend on open lab slots students can commute to. Unofficial estimate."
    ),
    "UC Santa Cruz Science Internship Program (SIP)": _est(
        "~10–20% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Competitive UCSC campus research internship with limited lab placements. Unofficial estimate."
    ),
    "Wave Hill Woodland Ecology Research Mentorship (WERM)": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Competitive paid Bronx ecology research mentorship with college credit. Unofficial estimate."
    ),
    "RISE Environmentor Internship": _est(
        "~20–40% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Paid Rockaway environmental research internship with a limited local cohort. Unofficial estimate."
    ),
    "Genspace Biorocket Research Internship": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Competitive paid Brooklyn community-lab research internship ($2,000). Unofficial estimate."
    ),
    "BEYOND ALBERT High School Research Program": _est(
        "~10–25% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Competitive paid Bronx biomedical research program with a limited summer cohort. Unofficial estimate."
    ),
    "Project TRUE (Teens Researching Urban Ecology)": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Bronx Zoo urban-ecology research program for Bronx sophomores/juniors. Unofficial estimate."
    ),
    "Bronx River EELS Internship": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Competitive paid Bronx River environmental internship with college credit. Unofficial estimate."
    ),
    "Hudson River Park Science Leadership Program": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Pathway-based paid science internship; eligibility depends on partner programs. Unofficial estimate."
    ),
    "Wave Hill Forest Project": _est(
        "~20–45% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Paid SYEP forest ecology internship at Wave Hill with age and work-eligibility screens. Unofficial estimate."
    ),
    "Hk Maker Lab": _est(
        "~15–35% estimated",
        "Estimated — Low confidence",
        "Not officially reported. Free Columbia biomedical engineering maker program for rising juniors/seniors. Unofficial estimate."
    ),
    "NYU Tandon ARISE": _est(
        "Estimated 5–10%",
        "Estimated — Moderate confidence",
        "Not officially reported; highly competitive research program. Unofficial estimate based on the reported ~75-student cohort and secondary applicant reporting."
    ),
    "NYU ARISE": _est(
        "Estimated 5–10%",
        "Estimated — Moderate confidence",
        "Not officially reported; highly competitive research program. Unofficial estimate based on the reported ~75-student cohort and secondary applicant reporting."
    ),
}


def _selectivity_fallback_estimate(record):
    """Educated acceptance-rate estimate when no program-specific figure exists."""

    stars = record.get("selectivity_stars")
    try:
        stars = int(stars)
    except Exception:
        stars = None

    selectivity = str(record.get("selectivity", "")).strip().lower()
    opportunity_type = str(record.get("opportunity_type", "")).strip().lower()
    name = str(record.get("name", "")).strip()

    if opportunity_type == "competition" or "not applicable" in str(
        record.get("acceptance_rate", "")
    ).lower():
        existing = str(record.get("acceptance_rate", "")).strip()
        if existing and "not publicly reported" not in existing.lower():
            return None

    if stars == 5 or "extremely competitive" in selectivity:
        rate = "~3–10% estimated"
        note = "highly competitive"
    elif stars == 4 or "highly competitive" in selectivity:
        rate = "~10–25% estimated"
        note = "highly selective"
    elif stars == 3 or "moderately competitive" in selectivity:
        rate = "~20–40% estimated"
        note = "moderately selective"
    elif stars == 2 or "eligibility" in selectivity:
        rate = "~40–70% estimated"
        note = "primarily eligibility- or capacity-based"
    elif stars == 1 or "accessible" in selectivity or "lottery" in selectivity:
        rate = "~50–90% estimated"
        note = "accessible, lottery, or placement-based"
    else:
        rate = "~15–35% estimated"
        note = "selective STEM program"

    return _est(
        rate,
        "Estimated — Low confidence",
        (
            f"Not officially reported. Educated estimate for {name or 'this program'} "
            f"based on published competitiveness ({note}) and typical applicant volume "
            "for similar opportunities."
        ),
    )


def apply_opportunity_transparency(records):
    """Merge source-confidence fields onto each opportunity dict.

    Real values already on a record are kept. Overlay values win when they
    are non-placeholder. Defaults fill only remaining empty/placeholder keys.
    """

    def is_real(value):
        if value is None:
            return False
        text = str(value).strip()
        if not text:
            return False
        return text.lower() not in PLACEHOLDER_VALUES

    def rate_needs_estimate(record):
        rate = str(record.get("acceptance_rate", "")).strip().lower()
        confidence = str(record.get("acceptance_rate_confidence", "")).strip()
        if confidence in ("Official", "Calculated"):
            return False
        if not rate:
            return True
        if rate == "not publicly reported" or rate.startswith("not publicly reported"):
            return True
        return False

    for record in records:
        name = str(record.get("name", "")).strip()
        update = _lookup_transparency_update(name)

        merged = dict(TRANSPARENCY_DEFAULTS)
        for key, value in record.items():
            if is_real(value):
                merged[key] = value
        if update:
            for key, value in update.items():
                if is_real(value):
                    merged[key] = value
        structured = STRUCTURED_ELIGIBILITY.get(name)
        if structured is None:
            alias = NAME_ALIASES.get(name)
            if alias:
                structured = STRUCTURED_ELIGIBILITY.get(alias)
        if structured:
            for key, value in structured.items():
                if is_real(value):
                    merged[key] = value
        record.update(merged)

        if rate_needs_estimate(record):
            estimate = ACCEPTANCE_ESTIMATES.get(name)
            if estimate is None:
                alias = NAME_ALIASES.get(name)
                if alias:
                    estimate = ACCEPTANCE_ESTIMATES.get(alias)
            if estimate is None:
                estimate = _selectivity_fallback_estimate(record)
            if estimate:
                record.update(estimate)

        hydrate_opportunity_record_from_existing_fields(record)

        name = str(record.get("name", "")).strip()
        if name in (
            "NYU ARISE",
            "NYU Tandon ARISE"
        ):
            record.update(_arise_fields())
            # Keep the user-facing estimated rate label after ARISE overlay.
            arise_estimate = ACCEPTANCE_ESTIMATES.get(name) or ACCEPTANCE_ESTIMATES.get(
                "NYU Tandon ARISE"
            )
            if arise_estimate:
                record.update(arise_estimate)

    return records


def hydrate_opportunity_record_from_existing_fields(record):
    """Fill new card fields from older record columns when the new field is empty or a placeholder."""

    def raw_text(value):
        if value is None:
            return ""
        text = str(value).strip()
        if not text or text.lower() in {"nan", "none"}:
            return ""
        return text

    def is_placeholder_value(value):
        text = raw_text(value)
        return text == "" or text.lower() in PLACEHOLDER_VALUES

    def first_real(*keys):
        for key in keys:
            text = raw_text(record.get(key))
            if text and text.lower() not in PLACEHOLDER_VALUES:
                return text
        return ""

    eligibility = first_real(
        "eligibility_summary",
        "requirements",
        "application_requirements"
    )
    if eligibility:
        record["eligibility_summary"] = eligibility

    cost = first_real(
        "cost",
        "cost_category"
    )
    if cost:
        record["cost"] = cost
        if is_placeholder_value(record.get("cost_category")):
            record["cost_category"] = "Free" if cost.lower() == "free" else cost

    aid = first_real(
        "financial_aid_status",
        "financial_aid"
    )
    if aid:
        if (
            aid.lower() in {
                "not needed",
                "not needed — program is free",
                "not needed — program is completely free",
            }
            and raw_text(record.get("cost")).lower() == "free"
        ):
            aid = "Not needed — program is fully funded"
        record["financial_aid"] = aid
        record["financial_aid_status"] = aid

    stipend = first_real(
        "stipend_display",
        "stipend",
        "paid_status"
    )
    if stipend:
        record["stipend_display"] = stipend
        if is_placeholder_value(record.get("paid_status")):
            record["paid_status"] = stipend

    internship = first_real(
        "internship_potential"
    )
    if internship:
        record["internship_potential"] = internship

    return record
