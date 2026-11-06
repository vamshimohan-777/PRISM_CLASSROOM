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


# ---------------------------------------------------------------------------
# Misconception database.
#
# Lives here, below both engine.py and search_engine.py, because the rules engine
# reads each entry's prescribed route and the search index reads its text.
# ---------------------------------------------------------------------------

MISCONCEPTIONS_DATABASE = [
    {
        "id": "denominator-magnitude",
        "title": "Denominator Magnitude Misconception",
        "description": "Believing 1/8 > 1/3 because 8 > 3. Conflating the magnitude of the denominator with the total value of the unit fraction.",
        "concept": "equivalent-fractions",
        "symptoms": ["Learner selects larger denominator when comparing unit fractions", "Believes more parts means larger piece"],
        "recommended_route": "visual-support",
        "remedy": "Interactive SVG Fraction Bar exploration where learners visually compare equal-sized wholes split into 3 versus 8 equal parts."
    },
    {
        "id": "unequal-operations",
        "title": "Unequal Operations Slip",
        "description": "Operating on only the numerator or only the denominator, or multiplying/dividing top and bottom by different numbers.",
        "concept": "equivalent-fractions",
        "symptoms": ["e.g. changing 2/3 to 4/3 or 4/9 by applying multiplier to only one part", "Arithmetic slips in multiplier grids"],
        "recommended_route": "guided-practice",
        "remedy": "Scaffolded multiplier grid with linked numerator-denominator ratio locks."
    },
    {
        "id": "fraction-parts-gap",
        "title": "Foundational Fraction Parts Gap",
        "description": "Counting partitioned regions without verifying that all parts are strictly equal in area or length.",
        "concept": "fraction-parts",
        "symptoms": ["Treating unequal slices as identical fractional units", "Confusing numerator with total parts"],
        "recommended_route": "foundation",
        "remedy": "Hands-on physical paper-strip folding and shading to establish equal-partitioning before equivalence."
    },
    {
        "id": "additive-bias",
        "title": "Additive Equivalence Bias",
        "description": "Attempting to create equivalent fractions by adding or subtracting the same number from numerator and denominator (e.g. 1/2 = 2/3 by adding 1).",
        "concept": "equivalent-fractions",
        "symptoms": ["Adds constant k to both top and bottom instead of multiplying by k", "Believes (a+k)/(b+k) == a/b"],
        "recommended_route": "visual-support",
        "remedy": "Visual counter-example showing 1/2 bar alongside 2/3 bar to prove area is not preserved under addition."
    },
    {
        "id": "sign-inversion-slip",
        "title": "Sign Inversion & Balancing Error",
        "description": "Dropping or inverting negative signs when transposing terms across an equals sign in linear equations.",
        "concept": "linear-equations",
        "symptoms": ["Changing 3x + 5 = 20 into 3x = 25 (adding instead of subtracting 5)", "Errors when dividing by negative coefficients"],
        "recommended_route": "guided-practice",
        "remedy": "Two-pan balance scale visualization showing opposite operations applied simultaneously to both sides."
    },
    {
        "id": "perimeter-area-confusion",
        "title": "Perimeter vs Area Conflation",
        "description": "Confusing the boundary length of a quadrilateral with the two-dimensional surface area enclosed.",
        "concept": "quadrilaterals",
        "symptoms": ["Using perimeter formulas when asked for area", "Assuming shapes with equal perimeter have equal area"],
        "recommended_route": "foundation",
        "remedy": "Tile-grid area counting alongside string-boundary perimeter measurement."
    },
    {
        "id": "square-root-halving",
        "title": "Square Root Halving Fallacy",
        "description": "Dividing a number by 2 instead of finding the number which when multiplied by itself yields the original value (e.g. sqrt(16) = 8).",
        "concept": "squares-roots",
        "symptoms": ["sqrt(100) answered as 50", "sqrt(64) answered as 32"],
        "recommended_route": "visual-support",
        "remedy": "Square tile geometric array showing side length of a square with area N."
    },
    {
        "id": "sign-error",
        "title": "Negative Sign Dropped in Standard Form",
        "description": "Losing or misplacing the negative sign when writing a rational number in standard form.",
        "concept": "equivalent-fractions",
        "symptoms": ["Writes -18/24 as 3/4", "Treats -a/b and a/b as the same number"],
        "recommended_route": "guided-practice",
        "remedy": "Number-line placement of the pair -3/4 and 3/4 before simplifying, so the sign is fixed before the arithmetic."
    },
    {
        "id": "incomplete-simplification",
        "title": "Partial Simplification",
        "description": "Dividing by a common factor but stopping before the highest common factor is removed.",
        "concept": "simplification",
        "symptoms": ["Gives -9/12 instead of -3/4", "Stops after dividing by 2 when 6 was available"],
        "recommended_route": "guided-practice",
        "remedy": "Prime-factor both terms and strike out every shared factor, then check no common factor remains."
    },
    {
        "id": "property-confusion",
        "title": "Algebraic Property Misnaming",
        "description": "Confusing commutativity, associativity and distributivity when naming which property an identity shows.",
        "concept": "equivalent-fractions",
        "symptoms": ["Calls a + b = b + a associativity", "Cannot separate regrouping from reordering"],
        "recommended_route": "foundation",
        "remedy": "Side-by-side card sort: reorder (commutative) versus regroup (associative) versus share-out (distributive)."
    },
    {
        "id": "inverse-type-confusion",
        "title": "Additive vs Multiplicative Inverse",
        "description": "Returning the reciprocal when the additive inverse was asked for, or the reverse.",
        "concept": "equivalent-fractions",
        "symptoms": ["Gives -5/3 as the additive inverse of -3/5", "Flips the fraction instead of flipping the sign"],
        "recommended_route": "guided-practice",
        "remedy": "Anchor each inverse to its identity: additive inverses sum to 0, multiplicative inverses multiply to 1."
    },
    {
        "id": "coefficient-confusion",
        "title": "Coefficient Reported as the Solution",
        "description": "Reading the coefficient of the variable as the answer rather than solving for the variable.",
        "concept": "linear-equations",
        "symptoms": ["Answers 3 for 3x + 5 = 20", "Stops once the variable term is isolated"],
        "recommended_route": "guided-practice",
        "remedy": "Finish every solution by stating 'x = ...' and substituting the value back into the original equation."
    },
    {
        "id": "inverse-operation-slip",
        "title": "Wrong Inverse Operation",
        "description": "Undoing multiplication by subtracting (or division by adding) when isolating a variable.",
        "concept": "linear-equations",
        "symptoms": ["Solves 7x = 49 as x = 42", "Subtracts the coefficient instead of dividing by it"],
        "recommended_route": "guided-practice",
        "remedy": "Pair each operation with its inverse on a two-pan balance before transposing any term."
    },
    {
        "id": "equation-setup-slip",
        "title": "Word Problem Modelling Error",
        "description": "Forming an equation that does not represent the stated relationship, even though the algebra is then carried out correctly.",
        "concept": "linear-equations",
        "symptoms": ["Mis-assigns which quantity is the unknown", "Omits a stated condition such as 'after 3 years'"],
        "recommended_route": "follow-up",
        "remedy": "Underline each quantity in the sentence and label it before writing any symbol; read the equation back as English."
    },
    {
        "id": "angle-sum-slip",
        "title": "Polygon Angle Sum Error",
        "description": "Using the wrong angle sum for a polygon, usually the triangle's 180° or an un-adjusted (n-2) x 180 calculation.",
        "concept": "quadrilaterals",
        "symptoms": ["Uses 180° for a quadrilateral", "Forgets to subtract 2 from the side count"],
        "recommended_route": "visual-support",
        "remedy": "Physically split each polygon into triangles from one vertex and count them before applying (n-2) x 180."
    },
    {
        "id": "quadrilateral-classification-slip",
        "title": "Quadrilateral Property Mix-Up",
        "description": "Attributing the defining properties of one special quadrilateral to another.",
        "concept": "quadrilaterals",
        "symptoms": ["Calls a trapezium a parallelogram", "Assumes every quadrilateral has equal opposite angles"],
        "recommended_route": "visual-support",
        "remedy": "Build a property grid (parallel sides, equal sides, equal angles, perpendicular diagonals) and place each shape in it."
    },
    {
        "id": "construction-tool-slip",
        "title": "Construction Instrument Choice",
        "description": "Selecting an instrument that cannot produce the required constraint, such as a ruler for a fixed radius.",
        "concept": "practical-geometry",
        "symptoms": ["Reaches for a protractor to draw a circle", "Measures arcs by eye"],
        "recommended_route": "foundation",
        "remedy": "Match each instrument to the single constraint it fixes: compass for distance, protractor for angle, ruler for length."
    },
    {
        "id": "construction-data-slip",
        "title": "Insufficient Construction Data",
        "description": "Believing a quadrilateral can be constructed uniquely from fewer than five independent measurements.",
        "concept": "practical-geometry",
        "symptoms": ["Attempts a construction from three sides", "Guesses the missing measurement"],
        "recommended_route": "foundation",
        "remedy": "Count degrees of freedom aloud before drawing; demonstrate two different shapes fitting the same incomplete data."
    },
    {
        "id": "pythagoras-slip",
        "title": "Pythagorean Relationship Error",
        "description": "Adding side lengths instead of squaring them, or misidentifying the hypotenuse.",
        "concept": "squares-roots",
        "symptoms": ["Claims 3 + 4 is close enough to 5", "Applies a^2 + b^2 = c^2 with c as a leg"],
        "recommended_route": "visual-support",
        "remedy": "Draw squares on each side of the right triangle and compare their areas by counting unit tiles."
    },
    {
        "id": "probability-denominator-slip",
        "title": "Probability Denominator Error",
        "description": "Using the count of unfavourable outcomes, or the favourable count, as the denominator instead of the total.",
        "concept": "data-handling",
        "symptoms": ["Gives 2/3 instead of 2/5 for 2 blue among 5 counters", "Inverts favourable and total"],
        "recommended_route": "guided-practice",
        "remedy": "Write 'favourable / total' as a fixed template and fill the total first, listing every outcome."
    },
    {
        "id": "mean-median-confusion",
        "title": "Mean and Median Conflated",
        "description": "Reporting the middle value when the average is asked for, or the average when the middle value is asked for.",
        "concept": "data-handling",
        "symptoms": ["Gives the median for a mean question", "Forgets to divide by the number of observations"],
        "recommended_route": "guided-practice",
        "remedy": "Compute both statistics for the same small data set and name what each one answers."
    },
    {
        "id": "perfect-square-recognition",
        "title": "Perfect Square Not Recognised",
        "description": "Failing to identify which numbers are perfect squares, or guessing roots without checking by multiplication.",
        "concept": "squares-roots",
        "symptoms": ["Selects 18 or 30 as a perfect square", "Cannot recall squares beyond 10 x 10"],
        "recommended_route": "foundation",
        "remedy": "Build the 1-20 square table from tile arrays, then verify every candidate root by multiplying it by itself."
    },
    {
        "id": "cube-square-confusion",
        "title": "Cube and Square Conflated",
        "description": "Treating a perfect square as a perfect cube, or returning a square root where a cube root was required.",
        "concept": "cubes-roots",
        "symptoms": ["Answers 8 for the cube root of 64", "Selects 36 or 49 as perfect cubes"],
        "recommended_route": "visual-support",
        "remedy": "Contrast a flat square tile array with a stacked unit-cube model so the third dimension is visible."
    },
    {
        "id": "interest-simple-vs-compound",
        "title": "Simple Interest Used for Compound",
        "description": "Applying the simple interest formula where interest should accrue on the accumulated amount.",
        "concept": "comparing-quantities",
        "symptoms": ["Gives Rs 2,000 instead of Rs 2,100 for 2 years at 10%", "Never recalculates the principal"],
        "recommended_route": "guided-practice",
        "remedy": "Lay out a year-by-year table where each year's closing amount becomes the next year's principal."
    },
    {
        "id": "percentage-base-confusion",
        "title": "Percentage Base Quantity Slip",
        "description": "Calculating percentage increase or decrease relative to the final value instead of the original initial base.",
        "concept": "comparing-quantities",
        "symptoms": ["Using (New - Old)/New instead of (New - Old)/Old", "Inverting markup and discount percentages"],
        "recommended_route": "guided-practice",
        "remedy": "Step-by-step ratio tables anchoring the 100% reference bar to the original quantity."
    },
    {
        "id": "forgot-division-slip",
        "title": "Stopped Before Dividing",
        "description": "Isolating the variable term correctly and then reporting that value without dividing by the coefficient.",
        "concept": "linear-equations",
        "symptoms": ["Answers 15 for 3x + 5 = 20", "Treats 3x = 15 as the finished solution"],
        "recommended_route": "guided-practice",
        "remedy": "Finish every solution by writing 'x = ...' with coefficient 1, then substitute it back into the original equation."
    },
    {
        "id": "reciprocal-inversion",
        "title": "Scaling the Wrong Term",
        "description": "Multiplying the denominator when a quantity is scaled up, which makes the amount smaller rather than larger.",
        "concept": "equivalent-fractions",
        "symptoms": ["Doubles 3/4 cup to 3/8 cup", "Expects a larger denominator to mean a larger amount"],
        "recommended_route": "visual-support",
        "remedy": "Lay scaled copies of the fraction bar end to end and compare the total length with the original bar."
    },
    {
        "id": "division-instead-of-root",
        "title": "Dividing Instead of Taking a Root",
        "description": "Dividing a number by 3 (or 2) instead of finding the value that multiplies by itself to give the number.",
        "concept": "cubes-roots",
        "symptoms": ["Gives 9 for the cube root of 27", "Treats the root symbol as a division instruction"],
        "recommended_route": "visual-support",
        "remedy": "Build the number as a cube from unit blocks and read the root from the edge length."
    },
]


def misconception_entry(misconception_id: str | None) -> dict | None:
    return next((m for m in MISCONCEPTIONS_DATABASE if m["id"] == misconception_id), None)


def misconception_route(misconception_id: str | None, default: str = "visual-support") -> str:
    entry = misconception_entry(misconception_id)
    return entry["recommended_route"] if entry else default


# ---------------------------------------------------------------------------
# Prerequisite skills.
#
# Each chapter has at least one skill it depends on and one quick question that
# measures it, so a weak foundation can be detected in any chapter. These are not
# chapters: their questions appear inside the chapters that depend on them.
# ---------------------------------------------------------------------------

PREREQUISITE_SKILLS: dict[str, dict[str, str]] = {
    "fraction-parts": {"title": "Parts of a fraction", "chapter_id": "rational-numbers", "objective": "Learner identifies equal parts and names numerator and denominator.", "remedy": "Fold paper strips into equal parts, shade some, and name the fraction before comparing anything."},
    "fraction-magnitude": {"title": "Comparing fraction sizes", "chapter_id": "rational-numbers", "objective": "Learner connects a larger denominator with smaller equal parts.", "remedy": "Place two fraction bars of the same whole side by side and compare the size of one part from each."},
    "simplification": {"title": "Simplifying fractions", "chapter_id": "rational-numbers", "objective": "Learner divides both terms by a common factor until none remains.", "remedy": "List the factors of both terms, divide by the highest common factor, and check that no factor remains."},
    "inverse-operations": {"title": "Undoing an operation", "chapter_id": "linear-equations", "objective": "Learner undoes addition with subtraction and multiplication with division.", "remedy": "Use a two-pan balance: whatever is done to one pan must be done to the other, using the opposite operation."},
    "triangle-angle-sum": {"title": "Angle sum of a triangle", "chapter_id": "quadrilaterals", "objective": "Learner uses the fact that a triangle's angles total 180°.", "remedy": "Tear the three corners off a paper triangle and place them together to form a straight line."},
    "measuring-skills": {"title": "Measuring with a ruler", "chapter_id": "practical-geometry", "objective": "Learner reads a length correctly as the difference between two ruler marks.", "remedy": "Measure the same segment starting from 0 and from another mark, then compare the two readings."},
    "reading-data": {"title": "Reading a data list", "chapter_id": "data-handling", "objective": "Learner counts how often a value occurs in a data list.", "remedy": "Turn the list into a tally table, then read the frequency of each value from the table."},
    "number-factors": {"title": "Prime factorisation", "chapter_id": "squares-roots", "objective": "Learner writes a number as a product of prime numbers only.", "remedy": "Build a factor tree and keep splitting until every number at the end is prime."},
    "repeated-multiplication": {"title": "Repeated multiplication", "chapter_id": "cubes-roots", "objective": "Learner calculates a number multiplied by itself three times.", "remedy": "Stack unit cubes into layers: multiply for one layer, then multiply again by the number of layers."},
    "percent-meaning": {"title": "Meaning of percent", "chapter_id": "comparing-quantities", "objective": "Learner reads a percentage as parts out of 100 and finds it of a quantity.", "remedy": "Shade a 100-square grid to show the percentage, then scale the grid to the quantity in the question."},
}

# (id, concept_id, prompt, options, answer, explanation, misconception_map)
PREREQUISITE_QUESTIONS = [
    ("prereq-magnitude", "fraction-magnitude", "Which is larger: 1/2 or 1/5?", ["1/2", "1/5", "They are equal"], "1/2", "Halves are larger pieces than fifths of the same whole, so 1/2 is larger.", {"1/5": "denominator-magnitude"}),
    ("prereq-simplify", "simplification", "Write 6/8 in simplest form.", ["3/4", "2/3", "6/8", "1/2"], "3/4", "Divide both terms by their highest common factor, 2: 6/8 = 3/4.", {"6/8": "incomplete-simplification"}),
    ("prereq-inverse", "inverse-operations", "If n + 6 = 10, what is n?", ["4", "16", "6", "10"], "4", "Undo adding 6 by subtracting 6 from both sides: n = 10 - 6 = 4.", {"16": "sign-inversion-slip"}),
    ("prereq-triangle", "triangle-angle-sum", "Two angles of a triangle are 60° and 70°. The third angle is…", ["50°", "60°", "130°", "230°"], "50°", "A triangle's angles total 180°: 180° - (60° + 70°) = 50°.", {"230°": "angle-sum-slip"}),
    ("prereq-ruler", "measuring-skills", "A line segment runs from the 2 cm mark to the 9 cm mark on a ruler. How long is it?", ["7 cm", "9 cm", "11 cm", "2 cm"], "7 cm", "The length is the difference between the marks: 9 cm - 2 cm = 7 cm.", {"9 cm": "construction-tool-slip"}),
    ("prereq-data", "reading-data", "The marks of four students are 5, 7, 7 and 9. How many students scored 7?", ["1", "2", "3", "7"], "2", "The value 7 appears twice in the list, so 2 students scored 7.", {}),
    ("prereq-factors", "number-factors", "Which is the prime factorisation of 36?", ["2 × 2 × 3 × 3", "4 × 9", "6 × 6", "2 × 3 × 6"], "2 × 2 × 3 × 3", "Every factor must be prime: 36 = 2 × 2 × 3 × 3. The numbers 4, 6 and 9 are not prime.", {}),
    ("prereq-repeated", "repeated-multiplication", "What is 3 × 3 × 3?", ["9", "27", "6", "33"], "27", "3 × 3 = 9, and 9 × 3 = 27.", {"9": "cube-square-confusion"}),
    ("prereq-percent", "percent-meaning", "What is 50% of 80?", ["40", "50", "30", "160"], "40", "50% means 50 out of 100, which is one half. Half of 80 is 40.", {"50": "percentage-base-confusion"}),
]


def concept_title(concept_id: str) -> str:
    """A readable name for any node in the prerequisite graph."""
    if concept_id in PREREQUISITE_SKILLS:
        return PREREQUISITE_SKILLS[concept_id]["title"]
    chapter = next((c for c in CHAPTERS if c["concept"] == concept_id), None)
    return chapter["title"] if chapter else concept_id.replace("-", " ").title()


def concept_remedy(concept_id: str) -> str:
    """What to do about a weak prerequisite, whether it is a skill or a whole chapter."""
    if concept_id in PREREQUISITE_SKILLS:
        return PREREQUISITE_SKILLS[concept_id]["remedy"]
    chapter = next((c for c in CHAPTERS if c["concept"] == concept_id), None)
    if chapter:
        return f"Review Chapter {chapter['number']}: {chapter['title']} before continuing, starting with its diagnostic questions."
    return "Review this concept before continuing."
