"""The Class VIII Mathematics catalogue used by both the API and seed data."""

CHAPTERS = [
    {"id": "rational-numbers", "number": 1, "title": "Rational Numbers", "summary": "Compare, simplify, and represent rational numbers.", "concept": "equivalent-fractions", "minutes": 42, "color": "violet"},
    {"id": "linear-equations", "number": 2, "title": "Linear Equations in One Variable", "summary": "Model and solve everyday equations.", "concept": "linear-equations", "minutes": 46, "color": "blue"},
    {"id": "quadrilaterals", "number": 3, "title": "Understanding Quadrilaterals", "summary": "Classify shapes and reason with angle sums.", "concept": "quadrilaterals", "minutes": 38, "color": "teal"},
    {"id": "practical-geometry", "number": 4, "title": "Practical Geometry", "summary": "Construct quadrilaterals from precise information.", "concept": "practical-geometry", "minutes": 35, "color": "orange"},
    {"id": "data-handling", "number": 5, "title": "Data Handling", "summary": "Read graphs and use probability language.", "concept": "data-handling", "minutes": 40, "color": "pink"},
    {"id": "squares-roots", "number": 6, "title": "Squares and Square Roots", "summary": "Recognise square numbers and find roots.", "concept": "squares-roots", "minutes": 44, "color": "green"},
    {"id": "cubes-roots", "number": 7, "title": "Cubes and Cube Roots", "summary": "Explore cubes, patterns, and cube roots.", "concept": "cubes-roots", "minutes": 40, "color": "amber"},
    {"id": "comparing-quantities", "number": 8, "title": "Comparing Quantities", "summary": "Use percentages, profit, loss, and discount.", "concept": "comparing-quantities", "minutes": 48, "color": "rose"},
]

QUESTION_BANK = {
    "linear-equations": [("diagnostic", "Solve: 3x + 5 = 20", ["3", "5", "8", "25"], "5", "Subtract 5 from both sides, then divide by 3."), ("practice", "A number increased by 7 is 19. What is the number?", ["10", "12", "19", "26"], "12", "Write x + 7 = 19 and subtract 7."), ("test", "Five identical notebooks cost ₹75. What is the cost of one?", ["₹10", "₹12", "₹15", "₹20"], "₹15", "If 5n = 75, then n = 15.")],
    "quadrilaterals": [("diagnostic", "What is the sum of interior angles of a quadrilateral?", ["180°", "270°", "360°", "540°"], "360°", "A quadrilateral can be split into two triangles: 180° + 180° = 360°."), ("practice", "A quadrilateral with both pairs of opposite sides parallel is a…", ["kite", "parallelogram", "trapezium", "triangle"], "parallelogram", "A parallelogram has two pairs of parallel opposite sides."), ("test", "Three angles of a quadrilateral are 90°, 85°, and 110°. The fourth is…", ["65°", "75°", "85°", "95°"], "75°", "Subtract the known angles from 360°.")],
    "practical-geometry": [("diagnostic", "Which tool is used to draw a circle with a fixed radius?", ["protractor", "compass", "ruler", "set square"], "compass", "A compass keeps a fixed distance from its centre."), ("practice", "To construct a quadrilateral uniquely, you need…", ["only one side", "enough side and angle measurements", "only one angle", "its colour"], "enough side and angle measurements", "Construction needs enough independent measurements to fix the shape."), ("test", "Which is most important in a geometry construction?", ["guessing lengths", "accurate measurement", "drawing quickly", "using colour"], "accurate measurement", "Precise measurement makes the construction reliable.")],
    "data-handling": [("diagnostic", "A fair coin is tossed once. Probability of heads is…", ["0", "1/4", "1/2", "1"], "1/2", "Heads is one of two equally likely outcomes."), ("practice", "The mean of 4, 6, and 8 is…", ["5", "6", "7", "18"], "6", "Add 4 + 6 + 8 = 18, then divide by 3."), ("test", "A bag has 3 red and 2 blue counters. Probability of blue is…", ["2/3", "2/5", "3/5", "1/5"], "2/5", "There are 2 blue counters out of 5 total counters.")],
    "squares-roots": [("diagnostic", "Which number is a perfect square?", ["18", "25", "30", "45"], "25", "25 = 5 × 5."), ("practice", "The square root of 144 is…", ["10", "11", "12", "14"], "12", "12 × 12 = 144."), ("test", "A square tile has area 81 cm². Its side length is…", ["8 cm", "9 cm", "10 cm", "81 cm"], "9 cm", "The side length is √81 = 9 cm.")],
    "cubes-roots": [("diagnostic", "Which number is a perfect cube?", ["16", "27", "36", "49"], "27", "27 = 3 × 3 × 3."), ("practice", "The cube root of 64 is…", ["2", "3", "4", "8"], "4", "4 × 4 × 4 = 64."), ("test", "A cube has volume 125 cm³. Its edge length is…", ["4 cm", "5 cm", "6 cm", "25 cm"], "5 cm", "The edge length is ∛125 = 5 cm.")],
    "comparing-quantities": [("diagnostic", "25% as a fraction in simplest form is…", ["1/2", "1/4", "1/5", "25/1"], "1/4", "25% = 25/100 = 1/4."), ("practice", "A ₹500 bag has a 10% discount. The discount is…", ["₹10", "₹50", "₹90", "₹450"], "₹50", "10% of ₹500 is ₹50."), ("test", "A price rises from ₹200 to ₹250. The percentage increase is…", ["20%", "25%", "40%", "50%"], "25%", "The increase is ₹50; 50/200 × 100 = 25%.")],
}

QUESTION_BANK["rational-numbers"] = [("diagnostic", "Which fraction is equivalent to 1/2?", ["2/3", "2/4", "3/4", "1/4"], "2/4", "Multiply the numerator and denominator of 1/2 by 2."), ("practice", "Complete: 3/5 = __/10", ["5", "6", "7", "8"], "6", "Multiply both numerator and denominator by 2."), ("test", "A recipe uses 2/3 cup of milk. In sixths this is…", ["3/6", "4/6", "5/6", "2/6"], "4/6", "Multiply 2/3 by 2/2 to write it in sixths.")]


# ---------------------------------------------------------------------------
# Additional authentic NCERT Class VIII questions (3 per chapter → 6 total each)
# ---------------------------------------------------------------------------

QUESTION_BANK["rational-numbers"] += [
    ("diagnostic", "Which property does 1/2 + 1/3 = 1/3 + 1/2 demonstrate?", ["Associativity", "Commutativity", "Distributivity", "Closure"], "Commutativity", "Changing the order of addition does not change the sum — this is commutativity. (NCERT Class 8, Ch 1)"),
    ("practice", "What is the additive inverse of -3/5?", ["-5/3", "3/5", "5/3", "-3/5"], "3/5", "The additive inverse of a rational number p/q is -p/q. Additive inverse of -3/5 is 3/5. (NCERT Class 8, Ch 1)"),
    ("test", "Find a rational number between 1/4 and 1/2.", ["1/3", "2/3", "3/4", "1/8"], "1/3", "Mean of 1/4 and 1/2 = (1/4 + 1/2)/2 = (3/4)/2 = 3/8. 1/3 ≈ 0.333 lies between 0.25 and 0.5. (NCERT Class 8, Ch 1)"),
]

QUESTION_BANK["linear-equations"] += [
    ("diagnostic", "If 7x = 49, what is x?", ["6", "7", "8", "42"], "7", "Divide both sides by 7: x = 49 ÷ 7 = 7. (NCERT Class 8, Ch 2)"),
    ("practice", "The sum of two consecutive integers is 37. The integers are:", ["18 and 19", "17 and 20", "15 and 22", "16 and 21"], "18 and 19", "If n and n+1 are consecutive integers: 2n + 1 = 37, so n = 18. (NCERT Class 8, Ch 2)"),
    ("test", "Raju's father is 26 years older than Raju. After 3 years the sum of their ages will be 66. What is Raju's current age?", ["16", "17", "19", "20"], "17", "Let Raju's age = x. Then: (x+3) + (x+26+3) = 66 → 2x + 32 = 66 → x = 17. (NCERT Class 8, Ch 2, Example)"),
]

QUESTION_BANK["quadrilaterals"] += [
    ("diagnostic", "How many sides does a polygon need to have for interior angle sum to be 540°?", ["4", "5", "6", "7"], "5", "(n-2) × 180 = 540 → n-2 = 3 → n = 5. A pentagon has angle sum 540°. (NCERT Class 8, Ch 3)"),
    ("practice", "In a rhombus, the diagonals bisect each other at:", ["60°", "90°", "120°", "180°"], "90°", "The diagonals of a rhombus bisect each other at right angles (90°). (NCERT Class 8, Ch 3)"),
    ("test", "One angle of a parallelogram is 75°. What are the other three angles?", ["75°, 105°, 105°", "105°, 75°, 75°", "105°, 75°, 105°", "75°, 75°, 75°"], "105°, 75°, 105°", "Adjacent angles in a parallelogram are supplementary (sum = 180°). So 180°−75° = 105°. Opposite angles are equal. (NCERT Class 8, Ch 3)"),
]

QUESTION_BANK["practical-geometry"] += [
    ("diagnostic", "To construct a unique quadrilateral ABCD you need at least:", ["3 sides only", "5 measurements (sides and angles)", "2 sides only", "4 sides and no angles"], "5 measurements (sides and angles)", "A quadrilateral has 5 independent elements needed for a unique construction. (NCERT Class 8, Ch 4)"),
    ("practice", "In construction ABCD with AB = 4cm, angle A = 75°, AD = 5cm, angle B = 110°, BC = 3cm, which element is NOT directly needed first?", ["AB", "CD", "angle A", "angle B"], "CD", "With 2 adjacent sides and 2 included angles, CD is determined by construction, not given directly. (NCERT Class 8, Ch 4)"),
    ("test", "A square has side 5cm. What length is its diagonal?", ["5 cm", "5√2 cm ≈ 7.07 cm", "10 cm", "25 cm"], "5√2 cm ≈ 7.07 cm", "By Pythagorean theorem: diagonal = √(5² + 5²) = √50 = 5√2 cm. (NCERT Class 8, Ch 4)"),
]

QUESTION_BANK["data-handling"] += [
    ("diagnostic", "In a pie chart for a data set, the angle for a category with 25% of data is:", ["45°", "90°", "180°", "360°"], "90°", "25% of 360° = (25/100) × 360° = 90°. (NCERT Class 8, Ch 5)"),
    ("practice", "The numbers 2, 4, 5, 3, 6 are arranged in ascending order. The median is:", ["3", "4", "5", "6"], "4", "Ascending order: 2, 3, 4, 5, 6. Middle value (3rd of 5) = 4. (NCERT Class 8, Ch 5)"),
    ("test", "A bag contains 5 red and 3 blue marbles. What is the probability of picking red?", ["3/8", "5/8", "5/3", "1/2"], "5/8", "P(red) = 5 favorable / 8 total = 5/8. (NCERT Class 8, Ch 5)"),
]

QUESTION_BANK["squares-roots"] += [
    ("diagnostic", "The number 169 is a perfect square of:", ["11", "12", "13", "14"], "13", "13 × 13 = 169. (NCERT Class 8, Ch 6)"),
    ("practice", "Find √(324) using prime factorisation. 324 = 4 × 81 = 2² × 3⁴. So √324 =", ["16", "18", "20", "9"], "18", "√(2² × 3⁴) = 2 × 3² = 2 × 9 = 18. (NCERT Class 8, Ch 6)"),
    ("test", "(3, 4, 5) is a Pythagorean triplet because:", ["3+4 = 7, close to 5", "3² + 4² = 5²", "3×4 = 12, 12-5 = 7", "All are odd"], "3² + 4² = 5²", "9 + 16 = 25 = 5². This satisfies a² + b² = c². (NCERT Class 8, Ch 6)"),
]

QUESTION_BANK["cubes-roots"] += [
    ("diagnostic", "Which is a perfect cube?", ["8", "12", "18", "20"], "8", "2 × 2 × 2 = 8. (NCERT Class 8, Ch 7)"),
    ("practice", "Find the cube root of 1000.", ["10", "100", "30", "50"], "10", "10 × 10 × 10 = 1000. ∛1000 = 10. (NCERT Class 8, Ch 7)"),
    ("test", "Is 392 a perfect cube? Its prime factorisation is 2³ × 7².", ["Yes, ∛392 = 14", "No, 7 appears only twice — needs one more 7", "Yes, because 392 = 8 × 49", "No, because 2 appears three times"], "No, 7 appears only twice — needs one more 7", "For a perfect cube every prime factor must appear in multiples of 3. 7² means 7 needs one more. (NCERT Class 8, Ch 7)"),
]

QUESTION_BANK["comparing-quantities"] += [
    ("diagnostic", "A shopkeeper buys a pen for ₹10 and sells it for ₹13. Profit percentage is:", ["13%", "30%", "3%", "10%"], "30%", "Profit = ₹3. Profit% = (3/10) × 100 = 30%. (NCERT Class 8, Ch 8)"),
    ("practice", "Find the compound interest on ₹10,000 at 10% per annum for 2 years.", ["₹1,000", "₹2,000", "₹2,100", "₹2,500"], "₹2,100", "CI = P[(1+r)^n - 1] = 10000[(1.1)² - 1] = 10000 × 0.21 = ₹2,100. (NCERT Class 8, Ch 8)"),
    ("test", "The price of a refrigerator was ₹14,000. It was sold at a loss of 5%. Find the selling price.", ["₹13,300", "₹13,000", "₹12,500", "₹13,500"], "₹13,300", "Loss = 5% of 14000 = ₹700. SP = 14000 - 700 = ₹13,300. (NCERT Class 8, Ch 8)"),
]


def chapter_for(chapter_id: str) -> dict | None:
    return next((chapter for chapter in CHAPTERS if chapter["id"] == chapter_id), None)


# ---------------------------------------------------------------------------
# Misconception tags for the chapter question bank.
#
# Keyed by the question id that `seed.py` derives as
# f"{chapter_id}-{stage}-{position}", where position counts every entry in that
# chapter's QUESTION_BANK list from 1. Each value maps a *distractor option* to
# the cognitive error a learner who picks it is most likely making, which is
# what lets the rules engine classify an error instead of merely marking it
# wrong. Distractors with no single clear diagnosis are deliberately left
# untagged rather than given a speculative label.
# ---------------------------------------------------------------------------

MISCONCEPTION_TAGS: dict[str, dict[str, str]] = {
    # --- Ch 1: Rational Numbers -------------------------------------------
    "rational-numbers-diagnostic-1": {"2/3": "additive-bias", "1/4": "unequal-operations"},
    "rational-numbers-practice-2": {"5": "unequal-operations", "8": "additive-bias"},
    "rational-numbers-test-3": {"3/6": "denominator-magnitude", "5/6": "additive-bias", "2/6": "unequal-operations"},
    "rational-numbers-diagnostic-4": {"Associativity": "property-confusion", "Distributivity": "property-confusion", "Closure": "property-confusion"},
    "rational-numbers-practice-5": {"-5/3": "inverse-type-confusion", "5/3": "inverse-type-confusion", "-3/5": "sign-error"},
    "rational-numbers-test-6": {"1/8": "denominator-magnitude"},

    # --- Ch 2: Linear Equations in One Variable ---------------------------
    "linear-equations-diagnostic-1": {"25": "sign-inversion-slip", "3": "coefficient-confusion"},
    "linear-equations-practice-2": {"26": "sign-inversion-slip"},
    "linear-equations-test-3": {},
    "linear-equations-diagnostic-4": {"42": "inverse-operation-slip"},
    "linear-equations-practice-5": {"17 and 20": "equation-setup-slip", "15 and 22": "equation-setup-slip", "16 and 21": "equation-setup-slip"},
    "linear-equations-test-6": {"16": "equation-setup-slip", "20": "equation-setup-slip", "19": "equation-setup-slip"},

    # --- Ch 3: Understanding Quadrilaterals -------------------------------
    "quadrilaterals-diagnostic-1": {"180°": "angle-sum-slip", "540°": "angle-sum-slip", "270°": "angle-sum-slip"},
    "quadrilaterals-practice-2": {"trapezium": "quadrilateral-classification-slip", "kite": "quadrilateral-classification-slip"},
    "quadrilaterals-test-3": {"65°": "angle-sum-slip", "95°": "angle-sum-slip", "85°": "angle-sum-slip"},
    "quadrilaterals-diagnostic-4": {"4": "angle-sum-slip", "6": "angle-sum-slip", "7": "angle-sum-slip"},
    "quadrilaterals-practice-5": {"180°": "quadrilateral-classification-slip", "60°": "quadrilateral-classification-slip"},
    "quadrilaterals-test-6": {"75°, 105°, 105°": "quadrilateral-classification-slip", "75°, 75°, 75°": "quadrilateral-classification-slip"},

    # --- Ch 4: Practical Geometry -----------------------------------------
    "practical-geometry-diagnostic-1": {"protractor": "construction-tool-slip", "ruler": "construction-tool-slip", "set square": "construction-tool-slip"},
    "practical-geometry-practice-2": {"only one side": "construction-data-slip", "only one angle": "construction-data-slip"},
    "practical-geometry-test-3": {"guessing lengths": "construction-data-slip", "drawing quickly": "construction-data-slip"},
    "practical-geometry-diagnostic-4": {"3 sides only": "construction-data-slip", "2 sides only": "construction-data-slip", "4 sides and no angles": "construction-data-slip"},
    "practical-geometry-practice-5": {"AB": "construction-data-slip", "angle A": "construction-data-slip", "angle B": "construction-data-slip"},
    "practical-geometry-test-6": {"10 cm": "pythagoras-slip", "25 cm": "perimeter-area-confusion", "5 cm": "pythagoras-slip"},

    # --- Ch 5: Data Handling ----------------------------------------------
    "data-handling-diagnostic-1": {"1/4": "probability-denominator-slip", "1": "probability-denominator-slip", "0": "probability-denominator-slip"},
    "data-handling-practice-2": {"18": "mean-median-confusion", "5": "mean-median-confusion", "7": "mean-median-confusion"},
    "data-handling-test-3": {"2/3": "probability-denominator-slip", "3/5": "probability-denominator-slip", "1/5": "probability-denominator-slip"},
    "data-handling-diagnostic-4": {"45°": "percentage-base-confusion", "180°": "percentage-base-confusion"},
    "data-handling-practice-5": {"5": "mean-median-confusion", "3": "mean-median-confusion"},
    "data-handling-test-6": {"5/3": "probability-denominator-slip", "3/8": "probability-denominator-slip"},

    # --- Ch 6: Squares and Square Roots -----------------------------------
    "squares-roots-diagnostic-1": {"18": "perfect-square-recognition", "30": "perfect-square-recognition", "45": "perfect-square-recognition"},
    "squares-roots-practice-2": {"14": "perfect-square-recognition", "11": "perfect-square-recognition"},
    "squares-roots-test-3": {"81 cm": "perimeter-area-confusion", "8 cm": "perfect-square-recognition"},
    "squares-roots-diagnostic-4": {"12": "perfect-square-recognition", "14": "perfect-square-recognition"},
    "squares-roots-practice-5": {"9": "square-root-halving", "16": "perfect-square-recognition"},
    "squares-roots-test-6": {"3+4 = 7, close to 5": "pythagoras-slip", "All are odd": "pythagoras-slip", "3×4 = 12, 12-5 = 7": "pythagoras-slip"},

    # --- Ch 7: Cubes and Cube Roots ---------------------------------------
    "cubes-roots-diagnostic-1": {"16": "cube-square-confusion", "36": "cube-square-confusion", "49": "cube-square-confusion"},
    "cubes-roots-practice-2": {"8": "cube-square-confusion", "2": "cube-square-confusion"},
    "cubes-roots-test-3": {"25 cm": "perimeter-area-confusion"},
    "cubes-roots-diagnostic-4": {},
    "cubes-roots-practice-5": {"100": "cube-square-confusion", "30": "cube-square-confusion"},
    "cubes-roots-test-6": {"Yes, ∛392 = 14": "cube-square-confusion", "Yes, because 392 = 8 × 49": "cube-square-confusion"},

    # --- Ch 8: Comparing Quantities ---------------------------------------
    "comparing-quantities-diagnostic-1": {"1/5": "percentage-base-confusion", "25/1": "percentage-base-confusion", "1/2": "percentage-base-confusion"},
    "comparing-quantities-practice-2": {"₹450": "percentage-base-confusion", "₹10": "percentage-base-confusion", "₹90": "percentage-base-confusion"},
    "comparing-quantities-test-3": {"20%": "percentage-base-confusion", "50%": "percentage-base-confusion", "40%": "percentage-base-confusion"},
    "comparing-quantities-diagnostic-4": {"3%": "percentage-base-confusion", "13%": "percentage-base-confusion"},
    "comparing-quantities-practice-5": {"₹2,000": "interest-simple-vs-compound", "₹1,000": "interest-simple-vs-compound"},
    "comparing-quantities-test-6": {"₹13,500": "percentage-base-confusion", "₹13,000": "percentage-base-confusion"},
}


def misconception_tags_for(question_id: str) -> dict[str, str]:
    return MISCONCEPTION_TAGS.get(question_id, {})
