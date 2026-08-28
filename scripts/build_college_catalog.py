#!/usr/bin/env python3
"""Build data/college_catalog.json from College Scorecard + curated STEM metadata.

Does not invent statistics. Admission rates and tuition come from Scorecard
(IPEDS-backed). Existing CDS overrides may replace Scorecard admit rates when
an official Common Data Set URL is supplied.
"""

from __future__ import annotations

import json
import math
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "college_catalog.json"
API = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
API_KEY = "DEMO_KEY"
NYC = (40.7128, -74.0060)
SCORECARD_SOURCE = "https://collegescorecard.ed.gov/data/"
SCORECARD_YEAR_LABEL = "College Scorecard latest (IPEDS)"

FIELDS = ",".join(
    [
        "id",
        "school.name",
        "school.city",
        "school.state",
        "school.school_url",
        "school.ownership",
        "school.degrees_awarded.predominant",
        "school.minority_serving.hbcu",
        "school.minority_serving.hispanic",
        "school.locale",
        "latest.admissions.admission_rate.overall",
        "latest.cost.tuition.in_state",
        "latest.cost.tuition.out_of_state",
        "latest.cost.avg_net_price.public",
        "latest.cost.avg_net_price.private",
        "latest.student.size",
        "location.lat",
        "location.lon",
    ]
)

STEM_DEFAULT = [
    "Computer Science",
    "Engineering",
    "Biology",
    "Mathematics",
    "Chemistry",
    "Physics",
    "Data Science",
]

# display_name, scorecard_query, curated extras
# unitid optional exact match when query is ambiguous
CURATED = [
    # Existing 28 (keep CDS admit overrides where noted)
    {"name": "MIT", "query": "Massachusetts Institute of Technology", "unitid": 166683, "region": "Northeast", "research": True, "fields": ["Engineering", "Electrical Engineering", "Mechanical Engineering", "Computer Engineering", "Computer Science", "Artificial Intelligence", "Data Science", "Physics", "Mathematics", "Robotics", "Biology", "Chemistry"], "cds": {"admit_rate": 4.5, "rate_label": "Fall 2024 overall", "source_url": "https://ir.mit.edu/projects/2024-25-common-data-set/", "source_year": "2024-25"}},
    {"name": "Stanford University", "query": "Stanford University", "unitid": 243744, "region": "West", "research": True, "fields": ["Engineering", "Computer Science", "Artificial Intelligence", "Data Science", "Biology", "Physics", "Mathematics"], "cds": {"admit_rate": 3.8, "rate_label": "Fall 2025 overall", "source_url": "https://irds.stanford.edu/data-findings/cds", "source_year": "2025"}},
    {"name": "Carnegie Mellon University", "query": "Carnegie Mellon University", "unitid": 211440, "region": "Northeast", "research": True, "fields": ["Computer Science", "Artificial Intelligence", "Engineering", "Robotics", "Data Science", "Mathematics"], "cds": {"admit_rate": 11.1, "rate_label": "Fall 2025 overall", "source_url": "https://www.cmu.edu/ira/CDS/", "source_year": "2025"}},
    {"name": "UC Berkeley", "query": "University of California-Berkeley", "unitid": 110635, "region": "West", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Biology", "Physics", "Environmental Science"], "cds": {"admit_rate": 11.0, "rate_label": "2026 first-year overall", "source_url": "https://admissions.berkeley.edu/apply-to-berkeley/student-profile/", "source_year": "2026"}},
    {"name": "Georgia Tech", "query": "Georgia Institute of Technology-Main Campus", "unitid": 139755, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Artificial Intelligence", "Data Science", "Robotics"], "cds": {"admit_rate": 13.3, "rate_label": "Fall 2025 overall", "source_url": "https://irp.gatech.edu/files/CDS/CDS_2025-2026_FINAL_R4_03JUN2026.pdf", "source_year": "2025-26"}},
    {"name": "University of Michigan", "query": "University of Michigan-Ann Arbor", "unitid": 170976, "region": "Midwest", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Biology", "Public Health"], "cds": {"admit_rate": 16.4, "rate_label": "Fall 2025 overall", "source_url": "https://obp.umich.edu/wp-content/uploads/pubdata/factsfigures/firstyearsprofile_umaa_2025.pdf", "source_year": "2025"}},
    {"name": "Purdue University", "query": "Purdue University-Main Campus", "unitid": 243780, "region": "Midwest", "research": True, "fields": ["Engineering", "Computer Science", "Aerospace Engineering", "Data Science"], "cds": {"admit_rate": 49.9, "rate_label": "Fall 2024 overall", "source_url": "https://www.purdue.edu/idata/wp-content/uploads/2025/06/CDS_2024-2025.pdf", "source_year": "2024-25"}},
    {"name": "Cornell University", "query": "Cornell University", "unitid": 190415, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Agriculture / Plant Science", "Data Science"], "cds": {"admit_rate": 7.9, "rate_label": "Fall 2023 overall", "source_url": "https://irp.cornell.edu/common-data-set", "source_year": "2023"}},
    {"name": "Columbia University", "query": "Columbia University in the City of New York", "unitid": 190150, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Biology", "Physics"], "cds": {"admit_rate": 3.9, "rate_label": "Class of 2027 overall", "source_url": "https://undergrad.admissions.columbia.edu/", "source_year": "2027"}},
    {"name": "Princeton University", "query": "Princeton University", "unitid": 186131, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Physics", "Mathematics", "Biology"], "cds": {"admit_rate": 4.4, "rate_label": "Class of 2029 overall", "source_url": "https://profile.princeton.edu/admission-and-costs", "source_year": "2029"}},
    {"name": "Harvard University", "query": "Harvard University", "unitid": 166027, "region": "Northeast", "research": True, "fields": ["Computer Science", "Biology", "Physics", "Mathematics", "Data Science"], "cds": {"admit_rate": 4.2, "rate_label": "Class of 2029 overall", "source_url": "https://college.harvard.edu/admissions/admissions-statistics", "source_year": "2029"}},
    {"name": "Duke University", "query": "Duke University", "unitid": 198419, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Biomedical Engineering", "Data Science"], "cds": {"admit_rate": 5.2, "rate_label": "Class of 2029 overall", "source_url": "https://admissions.duke.edu/", "source_year": "2029"}},
    {"name": "Johns Hopkins University", "query": "Johns Hopkins University", "unitid": 162928, "region": "Northeast", "research": True, "fields": ["Biomedical Engineering", "Biology", "Computer Science", "Public Health", "Engineering"], "cds": {"admit_rate": 6.4, "rate_label": "Fall 2024 overall", "source_url": "https://oira.jhu.edu/wp-content/uploads/CDS_2024-2025_JHU-2.pdf", "source_year": "2024-25"}},
    {"name": "Caltech", "query": "California Institute of Technology", "unitid": 110404, "region": "West", "research": True, "fields": ["Physics", "Engineering", "Computer Science", "Chemistry", "Mathematics"], "cds": {"admit_rate": 3.1, "rate_label": "Fall 2023 overall", "source_url": "https://iro.caltech.edu/", "source_year": "2023"}},
    {"name": "The Cooper Union", "query": "Cooper Union for the Advancement of Science and Art", "unitid": 190372, "region": "Northeast", "research": False, "fields": ["Engineering", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Architecture"], "cds": {"admit_rate": 13.0, "rate_label": "2024-25 overall", "source_url": "https://cooper.edu/admissions/faq", "source_year": "2024-25"}},
    {"name": "NYU Tandon", "query": "New York University", "unitid": 193900, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Cybersecurity", "Robotics"], "cds": {"admit_rate": 13.0, "rate_label": "NYU university-wide overall", "source_url": "https://bulletins.nyu.edu/nyu/enrollment-graduation-statistics/", "source_year": "2024"}, "notes": "Admit rate is NYU university-wide; Tandon may differ by program."},
    {"name": "Stevens Institute of Technology", "query": "Stevens Institute of Technology", "unitid": 186867, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Cybersecurity", "Data Science", "Robotics"], "cds": {"admit_rate": 51.0, "rate_label": "Fall 2025 overall", "source_url": "https://www.stevens.edu/discover-stevens/stevens-by-the-numbers/facts-statistics", "source_year": "2025"}},
    {"name": "CCNY", "query": "CUNY City College", "unitid": 190567, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Architecture", "Chemistry"], "cds": {"admit_rate": 60.0, "rate_label": "Fall 2024 overall", "source_url": "https://www.ccny.cuny.edu/sites/default/files/2025-03/20250324_FINAL%20CDS-2024-2025.pdf", "source_year": "2024-25"}},
    {"name": "Stony Brook University", "query": "Stony Brook University", "unitid": 196097, "region": "Northeast", "research": True, "fields": ["Computer Science", "Engineering", "Biology", "Physics", "Marine Science"], "cds": {"admit_rate": 48.2, "rate_label": "Fall 2025 overall", "source_url": "https://www.stonybrook.edu/irpe/factbook/common-data-set.html", "source_year": "2025"}},
    {"name": "CUNY City Tech", "query": "CUNY New York City College of Technology", "unitid": 190655, "region": "Northeast", "research": False, "fields": ["Computer Science", "Engineering", "Information Technology / Information Science", "Architecture", "Data Science"], "cds": {"admit_rate": 80.3, "rate_label": "Fall 2024 overall", "source_url": "https://www.citytech.cuny.edu/consumer-info/", "source_year": "2024"}},
    {"name": "UMass Lowell", "query": "University of Massachusetts-Lowell", "unitid": 166513, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Physics"], "cds": {"admit_rate": 83.0, "rate_label": "Fall 2024 overall", "source_url": "https://www.uml.edu/docs/CDS_2024-2025%20Final_tcm18-403507.pdf", "source_year": "2024-25"}},
    {"name": "Western New England University", "query": "Western New England University", "unitid": 168254, "region": "Northeast", "research": False, "fields": ["Engineering", "Computer Science", "Biology", "Pharmacy / Pharmaceutical Science"], "cds": {"admit_rate": 83.5, "rate_label": "Fall 2024 overall", "source_url": "https://wne.edu/institutional-research/doc/WNE-CDS-2024-25-FINAL.pdf", "source_year": "2024-25"}},
    {"name": "UMass Boston", "query": "University of Massachusetts-Boston", "unitid": 166638, "region": "Northeast", "research": True, "fields": ["Computer Science", "Biology", "Environmental Science", "Data Science"], "cds": {"admit_rate": 85.5, "rate_label": "Fall 2025 overall", "source_url": "https://www.umb.edu/media/umassboston/editor-uploads/institutional-research-assessment-planning/TABLE7-Undergraduate--Admissions.pdf", "source_year": "2025"}},
    {"name": "Wentworth Institute of Technology", "query": "Wentworth Institute of Technology", "unitid": 168227, "region": "Northeast", "research": False, "fields": ["Engineering", "Computer Science", "Architecture", "Construction Engineering"], "cds": {"admit_rate": 87.8, "rate_label": "Fall 2025 overall", "source_url": "https://wit.edu/sites/default/files/2026-02/Common%20Data%20Set%202025-2026%20%281%29.pdf", "source_year": "2025-26"}},
    {"name": "University of New Hampshire", "query": "University of New Hampshire-Main Campus", "unitid": 183044, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Environmental Science", "Biology"], "cds": {"admit_rate": 88.2, "rate_label": "Fall 2024 overall", "source_url": "https://www.unh.edu/institutional-research/sites/default/files/media/2025-07/CDS-2024-2025_7.18.25.pdf", "source_year": "2024-25"}},
    {"name": "UMass Dartmouth", "query": "University of Massachusetts-Dartmouth", "unitid": 167987, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Marine Science"], "cds": {"admit_rate": 90.6, "rate_label": "Fall 2024 overall", "source_url": "https://www.umassd.edu/media/umassdartmouth/institutional-research/Data_Book_Fall24_Final-v2_6.26.25.pdf", "source_year": "2024"}},
    {"name": "Wilkes University", "query": "Wilkes University", "unitid": 216852, "region": "Northeast", "research": False, "fields": ["Engineering", "Computer Science", "Biology", "Pharmacy / Pharmaceutical Science"], "cds": {"admit_rate": 94.0, "rate_label": "Fall 2025 overall", "source_url": "https://www.wilkes.edu/about-wilkes/offices-and-administration/institutional-research/_assets/fact-book-2025-26.pdf", "source_year": "2025-26"}},
    {"name": "University of Pittsburgh at Johnstown", "query": "University of Pittsburgh-Johnstown", "unitid": 215266, "region": "Northeast", "research": False, "fields": ["Engineering", "Computer Science", "Biology", "Chemistry"], "cds": {"admit_rate": 94.8, "rate_label": "Fall 2024 overall", "source_url": "https://ir.pitt.edu/sites/default/files/assets/2024-2025_CDS_Johnstown.pdf", "source_year": "2024-25"}},
    # CUNY senior colleges
    {"name": "CUNY Baruch College", "query": "CUNY Bernard M Baruch College", "unitid": 190512, "region": "Northeast", "research": False, "fields": ["Computer Science", "Data Science", "Mathematics", "Statistics", "Business Analytics", "Economics"]},
    {"name": "CUNY Brooklyn College", "query": "CUNY Brooklyn College", "unitid": 190549, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Physics", "Mathematics", "Psychology / Cognitive Science"]},
    {"name": "CUNY Hunter College", "query": "CUNY Hunter College", "unitid": 190594, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Nursing", "Public Health", "Psychology / Cognitive Science"]},
    {"name": "CUNY John Jay College", "query": "CUNY John Jay College of Criminal Justice", "unitid": 190600, "region": "Northeast", "research": False, "fields": ["Computer Science", "Cybersecurity", "Forensic Science", "Data Science", "Psychology / Cognitive Science"]},
    {"name": "CUNY Lehman College", "query": "CUNY Lehman College", "unitid": 190637, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Mathematics", "Nursing", "Environmental Science"]},
    {"name": "CUNY Medgar Evers College", "query": "CUNY Medgar Evers College", "unitid": 190646, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Nursing", "Mathematics"]},
    {"name": "CUNY Queens College", "query": "CUNY Queens College", "unitid": 190664, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Physics", "Mathematics", "Psychology / Cognitive Science"]},
    {"name": "CUNY College of Staten Island", "query": "CUNY College of Staten Island", "unitid": 190558, "region": "Northeast", "research": False, "fields": ["Computer Science", "Engineering", "Biology", "Chemistry", "Physics"]},
    {"name": "CUNY York College", "query": "CUNY York College", "unitid": 190691, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Mathematics", "Nursing"]},
    # CUNY community colleges (affordable)
    {"name": "BMCC", "query": "CUNY Borough of Manhattan Community College", "unitid": 190521, "region": "Northeast", "research": False, "school_type_override": "Community College", "fields": ["Computer Science", "Engineering", "Biology", "Nursing", "Data Science"]},
    {"name": "LaGuardia Community College", "query": "CUNY LaGuardia Community College", "unitid": 190628, "region": "Northeast", "research": False, "school_type_override": "Community College", "fields": ["Computer Science", "Biology", "Engineering", "Nursing"]},
    {"name": "Queensborough Community College", "query": "CUNY Queensborough Community College", "unitid": 190673, "region": "Northeast", "research": False, "school_type_override": "Community College", "fields": ["Computer Science", "Engineering", "Biology", "Chemistry"]},
    {"name": "Bronx Community College", "query": "CUNY Bronx Community College", "unitid": 190530, "region": "Northeast", "research": False, "school_type_override": "Community College", "fields": ["Computer Science", "Engineering", "Biology", "Nursing"]},
    {"name": "Kingsborough Community College", "query": "CUNY Kingsborough Community College", "unitid": 190619, "region": "Northeast", "research": False, "school_type_override": "Community College", "fields": ["Computer Science", "Biology", "Nursing", "Marine Science"]},
    # SUNY
    {"name": "University at Buffalo", "query": "University at Buffalo", "unitid": 196088, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Pharmacy / Pharmaceutical Science", "Data Science"]},
    {"name": "Binghamton University", "query": "Binghamton University", "unitid": 196079, "region": "Northeast", "research": True, "fields": ["Computer Science", "Engineering", "Biology", "Chemistry", "Mathematics"]},
    {"name": "University at Albany", "query": "University at Albany", "unitid": 196060, "region": "Northeast", "research": True, "fields": ["Computer Science", "Biology", "Public Health", "Atmospheric Science", "Data Science"]},
    {"name": "SUNY Geneseo", "query": "SUNY College at Geneseo", "unitid": 196167, "region": "Northeast", "research": False, "fields": ["Biology", "Chemistry", "Physics", "Mathematics", "Psychology / Cognitive Science"]},
    {"name": "SUNY New Paltz", "query": "State University of New York at New Paltz", "unitid": 196176, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Engineering", "Psychology / Cognitive Science"]},
    {"name": "SUNY Farmingdale", "query": "Farmingdale State College", "unitid": 196158, "region": "Northeast", "research": False, "fields": ["Computer Science", "Engineering", "Aviation / Aeronautics", "Biology", "Cybersecurity"]},
    {"name": "SUNY Polytechnic Institute", "query": "SUNY Polytechnic Institute", "unitid": 196112, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Nanotechnology", "Cybersecurity", "Data Science"]},
    {"name": "SUNY Oswego", "query": "State University of New York at Oswego", "unitid": 196194, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Psychology / Cognitive Science", "Data Science"]},
    {"name": "SUNY Oneonta", "query": "SUNY Oneonta", "unitid": 196185, "region": "Northeast", "research": False, "fields": ["Biology", "Chemistry", "Earth Science / Geoscience", "Computer Science"]},
    {"name": "Fashion Institute of Technology", "query": "Fashion Institute of Technology", "unitid": 196264, "region": "Northeast", "research": False, "fields": ["Computer Science", "Data Science", "Architecture"]},
    {"name": "SUNY Maritime College", "query": "SUNY Maritime College", "unitid": 196291, "region": "Northeast", "research": False, "fields": ["Engineering", "Marine Science", "Mechanical Engineering", "Electrical Engineering"]},
    {"name": "Buffalo State University", "query": "SUNY Buffalo State University", "unitid": 196130, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Engineering", "Mathematics"]},
    # Nearby NY / Northeast
    {"name": "RPI", "query": "Rensselaer Polytechnic Institute", "unitid": 194824, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Artificial Intelligence", "Physics", "Architecture"]},
    {"name": "Rochester Institute of Technology", "query": "Rochester Institute of Technology", "unitid": 195003, "region": "Northeast", "research": True, "fields": ["Computer Science", "Engineering", "Cybersecurity", "Data Science", "Game Design / Development"]},
    {"name": "University of Rochester", "query": "University of Rochester", "unitid": 195030, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Optics", "Data Science"]},
    {"name": "Syracuse University", "query": "Syracuse University", "unitid": 196413, "region": "Northeast", "research": True, "fields": ["Computer Science", "Engineering", "Information Technology / Information Science", "Architecture", "Data Science"]},
    {"name": "Fordham University", "query": "Fordham University", "unitid": 191241, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Mathematics", "Psychology / Cognitive Science", "Data Science"]},
    {"name": "Hofstra University", "query": "Hofstra University", "unitid": 191630, "region": "Northeast", "research": False, "fields": ["Computer Science", "Engineering", "Biology", "Physician Assistant / Allied Health"]},
    {"name": "Pace University", "query": "Pace University", "unitid": 194310, "region": "Northeast", "research": False, "fields": ["Computer Science", "Cybersecurity", "Data Science", "Biology"]},
    {"name": "NJIT", "query": "New Jersey Institute of Technology", "unitid": 185262, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Architecture", "Cybersecurity"]},
    {"name": "Rutgers University–New Brunswick", "query": "Rutgers University-New Brunswick", "unitid": 186380, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Pharmacy / Pharmaceutical Science", "Data Science"]},
    {"name": "Northeastern University", "query": "Northeastern University", "unitid": 167358, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Health Science", "Robotics"]},
    {"name": "Boston University", "query": "Boston University", "unitid": 164988, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Public Health", "Data Science"]},
    {"name": "University of Connecticut", "query": "University of Connecticut", "unitid": 129020, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Pharmacy / Pharmaceutical Science"]},
    {"name": "Yale University", "query": "Yale University", "unitid": 130794, "region": "Northeast", "research": True, "fields": ["Computer Science", "Biology", "Physics", "Engineering", "Mathematics"]},
    {"name": "Brown University", "query": "Brown University", "unitid": 217156, "region": "Northeast", "research": True, "fields": ["Computer Science", "Biology", "Engineering", "Data Science", "Physics"]},
    # National public / private research
    {"name": "UCLA", "query": "University of California-Los Angeles", "unitid": 110662, "region": "West", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Data Science", "Public Health"]},
    {"name": "UC San Diego", "query": "University of California-San Diego", "unitid": 110680, "region": "West", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Data Science", "Marine Science"]},
    {"name": "University of Illinois Urbana-Champaign", "query": "University of Illinois Urbana-Champaign", "unitid": 145637, "region": "Midwest", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Physics", "Mathematics"]},
    {"name": "University of Wisconsin–Madison", "query": "University of Wisconsin-Madison", "unitid": 240444, "region": "Midwest", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Data Science"]},
    {"name": "UT Austin", "query": "The University of Texas at Austin", "unitid": 228778, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Biology"]},
    {"name": "Virginia Tech", "query": "Virginia Polytechnic Institute and State University", "unitid": 233921, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Architecture"]},
    {"name": "Penn State", "query": "Pennsylvania State University-Main Campus", "unitid": 214777, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Data Science", "Biology"]},
    {"name": "Ohio State University", "query": "Ohio State University-Main Campus", "unitid": 204796, "region": "Midwest", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Data Science"]},
    {"name": "University of Washington", "query": "University of Washington-Seattle Campus", "unitid": 236948, "region": "West", "research": True, "fields": ["Computer Science", "Engineering", "Biology", "Data Science", "Public Health"]},
    {"name": "University of Maryland", "query": "University of Maryland-College Park", "unitid": 163286, "region": "Northeast", "research": True, "fields": ["Computer Science", "Engineering", "Cybersecurity", "Data Science", "Biology"]},
    {"name": "University of Virginia", "query": "University of Virginia-Main Campus", "unitid": 234076, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Data Science"]},
    {"name": "University of Pennsylvania", "query": "University of Pennsylvania", "unitid": 215062, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Data Science", "Business Analytics"]},
    # HBCUs
    {"name": "Howard University", "query": "Howard University", "unitid": 131520, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Medicine / Health Science", "Public Health"]},
    {"name": "Spelman College", "query": "Spelman College", "unitid": 141060, "region": "South", "research": False, "fields": ["Biology", "Chemistry", "Computer Science", "Mathematics", "Physics"]},
    {"name": "Morehouse College", "query": "Morehouse College", "unitid": 140553, "region": "South", "research": False, "fields": ["Biology", "Chemistry", "Computer Science", "Mathematics", "Physics"]},
    {"name": "North Carolina A&T State University", "query": "North Carolina A&T State University", "unitid": 199102, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Agriculture / Plant Science", "Biology"]},
    {"name": "Florida A&M University", "query": "Florida Agricultural and Mechanical University", "unitid": 133650, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Pharmacy / Pharmaceutical Science", "Biology"]},
    {"name": "Hampton University", "query": "Hampton University", "unitid": 232265, "region": "South", "research": False, "fields": ["Engineering", "Computer Science", "Biology", "Nursing", "Marine Science"]},
    # HSIs / affordable publics
    {"name": "Florida International University", "query": "Florida International University", "unitid": 133951, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Public Health", "Data Science"]},
    {"name": "University of Texas at El Paso", "query": "The University of Texas at El Paso", "unitid": 228796, "region": "South", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Data Science"]},
    {"name": "New Jersey City University", "query": "New Jersey City University", "unitid": 185129, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Nursing", "Mathematics"]},
    {"name": "Montclair State University", "query": "Montclair State University", "unitid": 185590, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Data Science", "Public Health"]},
    {"name": "William Paterson University", "query": "William Paterson University of New Jersey", "unitid": 187444, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Chemistry", "Nursing"]},
    {"name": "College of New Jersey", "query": "The College of New Jersey", "unitid": 187134, "region": "Northeast", "research": False, "fields": ["Computer Science", "Biology", "Engineering", "Mathematics"]},
    {"name": "Rowan University", "query": "Rowan University", "unitid": 186371, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Data Science"]},
    {"name": "Temple University", "query": "Temple University", "unitid": 216339, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Public Health", "Data Science"]},
    {"name": "Drexel University", "query": "Drexel University", "unitid": 212054, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biomedical Engineering", "Data Science"]},
    {"name": "University of Delaware", "query": "University of Delaware", "unitid": 130943, "region": "Northeast", "research": True, "fields": ["Engineering", "Computer Science", "Biology", "Chemistry"]},
]


def haversine_miles(lat1, lon1, lat2, lon2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return round(2 * r * math.asin(math.sqrt(a)), 1)


def ownership_label(code):
    return {1: "Public", 2: "Private", 3: "Private for-profit"}.get(code, "Unknown")


def size_label(n):
    if n is None:
        return "Medium"
    if n < 3000:
        return "Small"
    if n < 15000:
        return "Medium"
    return "Large"


def setting_from_locale(locale):
    # IPEDS locale codes: 11-13 city, 21-23 suburb, 31-33 town, 41-43 rural
    if locale is None:
        return "Traditional college campus"
    if 11 <= locale <= 13:
        return "City / urban"
    if 21 <= locale <= 23:
        return "Traditional college campus"
    return "Traditional college campus"


def school_type(row, curated):
    if curated.get("school_type_override"):
        return curated["school_type_override"]
    pred = row.get("school.degrees_awarded.predominant")
    if pred == 2:
        return "Community College"
    if curated.get("research"):
        return "Research University"
    ownership = row.get("school.ownership")
    size = row.get("latest.student.size") or 0
    if ownership == 2 and size < 5000:
        return "Liberal Arts College"
    if ownership == 1:
        return "Public University"
    return "Private University"


def region_for_state(state, curated_region):
    if curated_region:
        return curated_region
    northeast = {"CT", "DC", "DE", "MA", "MD", "ME", "NH", "NJ", "NY", "PA", "RI", "VT"}
    midwest = {"IA", "IL", "IN", "KS", "MI", "MN", "MO", "ND", "NE", "OH", "SD", "WI"}
    west = {"AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NM", "NV", "OR", "UT", "WA", "WY"}
    south = {"AL", "AR", "FL", "GA", "KY", "LA", "MS", "NC", "OK", "SC", "TN", "TX", "VA", "WV"}
    if state in northeast:
        return "Northeast"
    if state in midwest:
        return "Midwest"
    if state in west:
        return "West"
    if state in south:
        return "South"
    return "Other"


def fetch_by_id(unitid):
    q = urllib.parse.urlencode(
        {"api_key": API_KEY, "id": unitid, "fields": FIELDS}
    )
    with urllib.request.urlopen(f"{API}?{q}", timeout=60) as resp:
        payload = json.load(resp)
    results = payload.get("results") or []
    return results[0] if results else None


def fetch_by_name(query):
    q = urllib.parse.urlencode(
        {
            "api_key": API_KEY,
            "school.name": query,
            "fields": FIELDS,
            "per_page": 5,
        }
    )
    with urllib.request.urlopen(f"{API}?{q}", timeout=60) as resp:
        payload = json.load(resp)
    return payload.get("results") or []


def pick_result(curated):
    unitid = curated.get("unitid")
    if unitid:
        row = fetch_by_id(unitid)
        if row:
            return row
    results = fetch_by_name(curated["query"])
    if not results:
        return None
    # Prefer exact-ish name contains
    query_l = curated["query"].lower()
    for row in results:
        name = (row.get("school.name") or "").lower()
        if query_l in name or name in query_l:
            return row
    return results[0]


def build_record(curated, row):
    city = row.get("school.city") or ""
    state = row.get("school.state") or ""
    location = f"{city}, {state}".strip(", ")
    lat = row.get("location.lat")
    lon = row.get("location.lon")
    distance = None
    if lat is not None and lon is not None:
        distance = haversine_miles(NYC[0], NYC[1], float(lat), float(lon))

    admit = row.get("latest.admissions.admission_rate.overall")
    admit_pct = round(float(admit) * 100, 1) if admit is not None else None
    tuition_in = row.get("latest.cost.tuition.in_state")
    tuition_out = row.get("latest.cost.tuition.out_of_state")
    net_public = row.get("latest.cost.avg_net_price.public")
    net_private = row.get("latest.cost.avg_net_price.private")
    net_price = net_public if net_public is not None else net_private

    ownership = ownership_label(row.get("school.ownership"))
    is_ny = state == "NY"
    # Scorecard publishes overall admission rate only — never invent OOS rates.
    rate_scope = "overall"
    rate_label = f"{SCORECARD_YEAR_LABEL} · overall acceptance"
    source_url = SCORECARD_SOURCE
    source_year = "Scorecard latest"
    cds = curated.get("cds") or {}
    if cds.get("admit_rate") is not None:
        admit_pct = cds["admit_rate"]
        rate_label = cds.get("rate_label") or rate_label
        source_url = cds.get("source_url") or source_url
        source_year = cds.get("source_year") or source_year
        rate_scope = "overall"

    cost_for_ny_student = tuition_in if is_ny else tuition_out
    cost_label = (
        "NY resident tuition & fees"
        if is_ny
        else "Out-of-state / published tuition & fees"
    )
    if not is_ny and tuition_out is None and tuition_in is not None:
        cost_for_ny_student = tuition_in
        cost_label = "Published tuition & fees (no separate out-of-state figure)"

    record = {
        "name": curated["name"],
        "official_name": row.get("school.name"),
        "unitid": row.get("id"),
        "location": location,
        "city": city,
        "state": state,
        "region": region_for_state(state, curated.get("region")),
        "setting": setting_from_locale(row.get("school.locale")),
        "size": size_label(row.get("latest.student.size")),
        "student_size": row.get("latest.student.size"),
        "control": ownership,
        "school_type": school_type(row, curated),
        "fields": curated.get("fields") or list(STEM_DEFAULT),
        "admit_rate": admit_pct,
        "admit_rate_scope": rate_scope,
        "rate_label": rate_label,
        "source_year": source_year,
        "source_url": source_url,
        "tuition_in_state": tuition_in,
        "tuition_out_of_state": tuition_out,
        "avg_net_price": net_price,
        "cost_for_ny_student": cost_for_ny_student,
        "cost_label": cost_label,
        "distance_from_nyc_miles": distance,
        "hbcu": bool(row.get("school.minority_serving.hbcu")),
        "hispanic_serving": bool(row.get("school.minority_serving.hispanic")),
        "research": bool(curated.get("research")),
        "school_url": row.get("school.school_url"),
        "notes": curated.get("notes"),
        "data_sources": [
            {
                "metric": "tuition_and_net_price",
                "source": "College Scorecard / IPEDS",
                "url": SCORECARD_SOURCE,
                "year_label": SCORECARD_YEAR_LABEL,
            }
        ],
    }
    if cds:
        record["data_sources"].append(
            {
                "metric": "acceptance_rate",
                "source": "Institution Common Data Set / admissions",
                "url": source_url,
                "year_label": source_year,
            }
        )
    else:
        record["data_sources"].append(
            {
                "metric": "acceptance_rate",
                "source": "College Scorecard / IPEDS",
                "url": SCORECARD_SOURCE,
                "year_label": SCORECARD_YEAR_LABEL,
            }
        )
    return record


def normalize_name(name: str) -> str:
    return "".join(ch.lower() for ch in name if ch.isalnum())


def main():
    built = []
    failures = []
    seen = set()
    for i, curated in enumerate(CURATED):
        time.sleep(0.35)
        try:
            row = pick_result(curated)
        except Exception as exc:  # noqa: BLE001
            failures.append((curated["name"], str(exc)))
            print("FAIL", curated["name"], exc)
            continue
        if not row:
            failures.append((curated["name"], "not found"))
            print("MISS", curated["name"])
            continue
        record = build_record(curated, row)
        key = normalize_name(record["name"])
        if key in seen:
            print("DUP skip", record["name"])
            continue
        seen.add(key)
        built.append(record)
        print(
            f"OK {len(built):02d}",
            record["name"],
            record["state"],
            record["admit_rate"],
            record["tuition_in_state"],
            record["tuition_out_of_state"],
        )

    required = [
        "name",
        "location",
        "region",
        "setting",
        "size",
        "fields",
        "admit_rate",
        "rate_label",
        "source_url",
        "source_year",
        "research",
        "state",
        "control",
        "school_type",
    ]
    incomplete = []
    for rec in built:
        missing = [k for k in required if rec.get(k) in (None, "", [])]
        # Community colleges sometimes lack admit_rate in Scorecard
        if "admit_rate" in missing and rec.get("school_type") == "Community College":
            missing.remove("admit_rate")
            rec["rate_label"] = rec.get("rate_label") or "Open / not separately published"
            rec["admit_rate_scope"] = "unavailable"
        if missing:
            incomplete.append((rec["name"], missing))

    payload = {
        "generated_from": "College Scorecard API + curated STEM metadata",
        "scorecard_docs": SCORECARD_SOURCE,
        "count": len(built),
        "colleges": built,
        "failures": failures,
        "incomplete": incomplete,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print("WROTE", OUT, "count", len(built), "failures", len(failures), "incomplete", len(incomplete))


if __name__ == "__main__":
    main()
