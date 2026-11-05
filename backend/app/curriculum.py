"""CBSE/NCERT curriculum metadata used consistently across the platform.

This platform is not published by, affiliated with, or endorsed by CBSE or NCERT.
Schools must verify their prescribed text, annual plan, and assessment policy locally.

Official CBSE portal:    https://cbseacademic.nic.in/
NCERT textbook (PDF):    https://ncert.nic.in/textbook.php?hmhe1=0-8
NCERT Class VIII Maths:  HMHE101 — Mathematics (Class 8)
"""

CBSE_CURRICULUM = {
    "board_code": "CBSE",
    "board_name": "Central Board of Secondary Education",
    "framework": "NCERT Class VIII Mathematics",
    "textbook": "Mathematics — Textbook for Class VIII (NCERT, New Delhi)",
    "textbook_code": "HMHE101",
    "textbook_url": "https://ncert.nic.in/textbook.php?hmhe1=0-8",
    "academic_year": "2024–25",
    "grade": 8,
    "subject": "Mathematics",
    "total_chapters": 8,
    "official_reference": "https://cbseacademic.nic.in/",
    "chapters": [
        {"number": 1, "title": "Rational Numbers",                       "ncert_ref": "NCERT Class 8 Maths Ch 1"},
        {"number": 2, "title": "Linear Equations in One Variable",       "ncert_ref": "NCERT Class 8 Maths Ch 2"},
        {"number": 3, "title": "Understanding Quadrilaterals",            "ncert_ref": "NCERT Class 8 Maths Ch 3"},
        {"number": 4, "title": "Practical Geometry",                     "ncert_ref": "NCERT Class 8 Maths Ch 4"},
        {"number": 5, "title": "Data Handling",                          "ncert_ref": "NCERT Class 8 Maths Ch 5"},
        {"number": 6, "title": "Squares and Square Roots",               "ncert_ref": "NCERT Class 8 Maths Ch 6"},
        {"number": 7, "title": "Cubes and Cube Roots",                   "ncert_ref": "NCERT Class 8 Maths Ch 7"},
        {"number": 8, "title": "Comparing Quantities",                   "ncert_ref": "NCERT Class 8 Maths Ch 8"},
    ],
    "learning_outcomes": [
        "Apply properties of rational numbers: commutativity, associativity, distributivity.",
        "Represent rational numbers on a number line and find rational numbers between two rationals.",
        "Model and solve linear equations in one variable with real-life applications.",
        "Classify quadrilaterals and apply the angle-sum property (360°).",
        "Construct quadrilaterals with given measurements using compass, ruler, and protractor.",
        "Read and interpret pie charts, double bar graphs; compute simple probability.",
        "Identify perfect squares and Pythagorean triplets; find square roots by prime factorisation.",
        "Identify perfect cubes; find cube roots of perfect cubes by prime factorisation.",
        "Apply percentages, profit, loss, discount, and simple/compound interest in real contexts.",
    ],
    "pedagogy": [
        "conceptual understanding",
        "reasoning and proof",
        "real-life application",
        "constructivist exploration",
        "peer discussion",
    ],
    "disclaimer": (
        "CBSE/NCERT alignment reference only. PRISM is an independent EdTech prototype; "
        "it is NOT an official CBSE or NCERT product. Confirm local pacing, your school's "
        "prescribed textbook edition, and assessment schedule before classroom use."
    ),
}
