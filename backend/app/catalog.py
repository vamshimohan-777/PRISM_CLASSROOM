"""The Class VIII Mathematics catalogue used by both the API and seed data."""

CHAPTERS = [
    {
        "id": "rational-numbers",
        "number": 1,
        "title": "Rational Numbers",
        "summary": "Compare, simplify, and represent rational numbers.",
        "concept": "equivalent-fractions",
        "minutes": 42,
        "color": "violet",
    },
    {
        "id": "linear-equations",
        "number": 2,
        "title": "Linear Equations in One Variable",
        "summary": "Model and solve everyday equations.",
        "concept": "linear-equations",
        "minutes": 46,
        "color": "blue",
    },
    {
        "id": "quadrilaterals",
        "number": 3,
        "title": "Understanding Quadrilaterals",
        "summary": "Classify shapes and reason with angle sums.",
        "concept": "quadrilaterals",
        "minutes": 38,
        "color": "teal",
    },
    {
        "id": "practical-geometry",
        "number": 4,
        "title": "Practical Geometry",
        "summary": "Construct quadrilaterals from precise information.",
        "concept": "practical-geometry",
        "minutes": 35,
        "color": "orange",
    },
    {
        "id": "data-handling",
        "number": 5,
        "title": "Data Handling",
        "summary": "Read graphs and use probability language.",
        "concept": "data-handling",
        "minutes": 40,
        "color": "pink",
    },
    {
        "id": "squares-roots",
        "number": 6,
        "title": "Squares and Square Roots",
        "summary": "Recognise square numbers and find roots.",
        "concept": "squares-roots",
        "minutes": 44,
        "color": "green",
    },
    {
        "id": "cubes-roots",
        "number": 7,
        "title": "Cubes and Cube Roots",
        "summary": "Explore cubes, patterns, and cube roots.",
        "concept": "cubes-roots",
        "minutes": 40,
        "color": "amber",
    },
    {
        "id": "comparing-quantities",
        "number": 8,
        "title": "Comparing Quantities",
        "summary": "Use percentages, profit, loss, and discount.",
        "concept": "comparing-quantities",
        "minutes": 48,
        "color": "rose",
    },
]

QUESTION_BANK = {
    "linear-equations": [
        (
            "diagnostic",
            "Solve: 3x + 5 = 20",
            ["3", "5", "8", "25"],
            "5",
            "Subtract 5 from both sides, then divide by 3.",
        ),
        (
            "practice",
            "A number increased by 7 is 19. What is the number?",
            ["10", "12", "19", "26"],
            "12",
            "Write x + 7 = 19 and subtract 7.",
        ),
        (
            "test",
            "Five identical notebooks cost ₹75. What is the cost of one?",
            ["₹10", "₹12", "₹15", "₹20"],
            "₹15",
            "If 5n = 75, then n = 15.",
        ),
    ],
    "quadrilaterals": [
        (
            "diagnostic",
            "What is the sum of interior angles of a quadrilateral?",
            ["180°", "270°", "360°", "540°"],
            "360°",
            "A quadrilateral can be split into two triangles: 180° + 180° = 360°.",
        ),
        (
            "practice",
            "A quadrilateral with both pairs of opposite sides parallel is a…",
            ["kite", "parallelogram", "trapezium", "triangle"],
            "parallelogram",
            "A parallelogram has two pairs of parallel opposite sides.",
        ),
        (
            "test",
            "Three angles of a quadrilateral are 90°, 85°, and 110°. The fourth is…",
            ["65°", "75°", "85°", "95°"],
            "75°",
            "Subtract the known angles from 360°.",
        ),
    ],
    "practical-geometry": [
        (
            "diagnostic",
            "Which tool is used to draw a circle with a fixed radius?",
            ["protractor", "compass", "ruler", "set square"],
            "compass",
            "A compass keeps a fixed distance from its centre.",
        ),
        (
            "practice",
            "To construct a quadrilateral uniquely, you need…",
            ["only one side", "enough side and angle measurements", "only one angle", "its colour"],
            "enough side and angle measurements",
            "Construction needs enough independent measurements to fix the shape.",
        ),
        (
            "test",
            "Which is most important in a geometry construction?",
            ["guessing lengths", "accurate measurement", "drawing quickly", "using colour"],
            "accurate measurement",
            "Precise measurement makes the construction reliable.",
        ),
    ],
    "data-handling": [
        (
            "diagnostic",
            "A fair coin is tossed once. Probability of heads is…",
            ["0", "1/4", "1/2", "1"],
            "1/2",
            "Heads is one of two equally likely outcomes.",
        ),
        (
            "practice",
            "The mean of 4, 6, and 8 is…",
            ["5", "6", "7", "18"],
            "6",
            "Add 4 + 6 + 8 = 18, then divide by 3.",
        ),
        (
            "test",
            "A bag has 3 red and 2 blue counters. Probability of blue is…",
            ["2/3", "2/5", "3/5", "1/5"],
            "2/5",
            "There are 2 blue counters out of 5 total counters.",
        ),
    ],
    "squares-roots": [
        ("diagnostic", "Which number is a perfect square?", ["18", "25", "30", "45"], "25", "25 = 5 × 5."),
        ("practice", "The square root of 144 is…", ["10", "11", "12", "14"], "12", "12 × 12 = 144."),
        (
            "test",
            "A square tile has area 81 cm². Its side length is…",
            ["8 cm", "9 cm", "10 cm", "81 cm"],
            "9 cm",
            "The side length is √81 = 9 cm.",
        ),
    ],
    "cubes-roots": [
        ("diagnostic", "Which number is a perfect cube?", ["16", "27", "36", "49"], "27", "27 = 3 × 3 × 3."),
        ("practice", "The cube root of 64 is…", ["2", "3", "4", "8"], "4", "4 × 4 × 4 = 64."),
        (
            "test",
            "A cube has volume 125 cm³. Its edge length is…",
            ["4 cm", "5 cm", "6 cm", "25 cm"],
            "5 cm",
            "The edge length is ∛125 = 5 cm.",
        ),
    ],
    "comparing-quantities": [
        (
            "diagnostic",
            "25% as a fraction in simplest form is…",
            ["1/2", "1/4", "1/5", "25/1"],
            "1/4",
            "25% = 25/100 = 1/4.",
        ),
        (
            "practice",
            "A ₹500 bag has a 10% discount. The discount is…",
            ["₹10", "₹50", "₹90", "₹450"],
            "₹50",
            "10% of ₹500 is ₹50.",
        ),
        (
            "test",
            "A price rises from ₹200 to ₹250. The percentage increase is…",
            ["20%", "25%", "40%", "50%"],
            "25%",
            "The increase is ₹50; 50/200 × 100 = 25%.",
        ),
    ],
}

QUESTION_BANK["rational-numbers"] = [
    (
        "diagnostic",
        "Which fraction is equivalent to 1/2?",
        ["2/3", "2/4", "3/4", "1/4"],
        "2/4",
        "Multiply the numerator and denominator of 1/2 by 2.",
    ),
    ("practice", "Complete: 3/5 = __/10", ["5", "6", "7", "8"], "6", "Multiply both numerator and denominator by 2."),
    (
        "test",
        "A recipe uses 2/3 cup of milk. In sixths this is…",
        ["3/6", "4/6", "5/6", "2/6"],
        "4/6",
        "Multiply 2/3 by 2/2 to write it in sixths.",
    ),
]


def chapter_for(chapter_id: str) -> dict | None:
    return next((chapter for chapter in CHAPTERS if chapter["id"] == chapter_id), None)
