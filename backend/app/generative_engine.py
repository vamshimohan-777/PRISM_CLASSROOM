"""PRISM Generative Engine: Pedagogical Generative System for CBSE Class VIII.

Generates:
1. Dynamic curriculum questions with mathematically grounded misconception distractors.
2. Personalized student remediation guides targeting specific cognitive barriers.
3. 45-minute differentiated multi-pod classroom lesson plans for teachers.
4. Culturally authentic Indian real-world transfer tasks.
"""
from dataclasses import dataclass, field
import os
import random
import re
from typing import Any
import httpx
from .catalog import MISCONCEPTIONS_DATABASE, QUESTION_BANK, misconception_entry, CHAPTERS

@dataclass
class GeneratedQuestion:
    id: str
    concept_id: str
    stage: str
    difficulty: str
    prompt: str
    options: list[str]
    expected_answer: str
    explanation: str
    misconception_map: dict[str, str]
    is_transfer: bool


class GenerativeEngine:
    def __init__(self):
        pass

    # -------------------------------------------------------------------------
    # 1. Dynamic Question Generator
    # -------------------------------------------------------------------------
    def generate_question(
        self,
        concept_id: str = "equivalent-fractions",
        stage: str = "practice",
        difficulty: str = "standard"
    ) -> dict[str, Any]:
        """Generates a mathematically balanced CBSE question with tagged misconception distractors."""
        cid = concept_id.lower()

        if "linear" in cid or cid == "linear-equations":
            question = self._gen_linear_equation_question(stage, difficulty)
        elif "square" in cid or cid == "squares-roots":
            question = self._gen_square_root_question(stage, difficulty)
        elif "cube" in cid or cid == "cubes-roots":
            question = self._gen_cube_root_question(stage, difficulty)
        elif "quadrilateral" in cid:
            question = self._gen_quadrilateral_question(stage, difficulty)
        elif "comparing" in cid or "quantity" in cid or cid == "comparing-quantities":
            question = self._gen_comparing_quantities_question(stage, difficulty)
        elif "data" in cid:
            question = self._gen_data_handling_question(stage, difficulty)
        elif "geometry" in cid:
            question = self._gen_practical_geometry_question(stage, difficulty)
        else:
            question = self._gen_fraction_question(stage, difficulty)
        return self._finalize(question)

    @staticmethod
    def _finalize(question: dict[str, Any]) -> dict[str, Any]:
        """Enforce the invariants every generated question must satisfy.

        Random parameters can make a distractor collide with the correct answer
        (2/3 = __/6 with k = 2 gives both 4 by multiplying and 4 by adding). A tag
        on the right answer would then label a correct learner as confused, so
        duplicates are removed, tags are kept only on real wrong options, and the
        list is padded back to four distinct choices.
        """
        answer = question["expected_answer"]
        options = list(dict.fromkeys(question["options"]))
        numeric = answer.lstrip("₹").split(" ")[0].rstrip("°")
        step = 1
        while len(options) < 4:
            if numeric.isdigit():
                candidate = answer.replace(numeric, str(int(numeric) + step), 1)
            else:
                candidate = f"None of these ({step})"
            if candidate not in options:
                options.append(candidate)
            step += 1
        random.shuffle(options)
        question["options"] = options
        question["misconception_map"] = {
            option: tag
            for option, tag in question["misconception_map"].items()
            if option != answer and option in options
        }
        return question

    def _gen_fraction_question(self, stage: str, difficulty: str) -> dict[str, Any]:
        """Generates dynamic fraction questions with explicit misconception distractors."""
        if difficulty == "foundation":
            # Comparing unit fractions: 1/a vs 1/b
            a = random.choice([2, 3, 4])
            b = random.choice([5, 6, 8, 10])
            prompt = f"Which fraction is greater: 1/{a} or 1/{b}?"
            correct = f"1/{a}"
            distractor_mag = f"1/{b}"
            d_equal = "Both are equal"
            d_zero = "Cannot be compared"
            options = [correct, distractor_mag, d_equal, d_zero]
            random.shuffle(options)
            return {
                "id": f"gen-frac-{random.randint(1000, 9999)}",
                "concept_id": "equivalent-fractions",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": prompt,
                "options": options,
                "expected_answer": correct,
                "explanation": f"1/{a} is greater because dividing the same whole into {a} equal parts yields larger individual pieces than dividing into {b} parts.",
                "misconception_map": {
                    distractor_mag: "denominator-magnitude",
                    d_equal: "fraction-parts-gap"
                },
                "is_transfer": stage == "test"
            }
        elif difficulty == "challenge" or stage == "test":
            # Transfer: Recipe scaling
            orig_servings = random.choice([2, 4])
            target_servings = orig_servings * random.choice([2, 3])
            multiplier = target_servings // orig_servings
            numerator = random.choice([1, 3])
            denominator = random.choice([2, 4])
            prompt = f"A recipe for {orig_servings} people requires {numerator}/{denominator} cup of milk. How much milk is required to serve {target_servings} people?"
            correct_num = numerator * multiplier
            correct = f"{correct_num}/{denominator} cups"
            d_add = f"{numerator + multiplier}/{denominator + multiplier} cups"
            d_top_only = f"{numerator + multiplier}/{denominator} cups"
            d_wrong = f"{numerator}/{denominator * multiplier} cups"
            options = [correct, d_add, d_top_only, d_wrong]
            random.shuffle(options)
            return {
                "id": f"gen-frac-{random.randint(1000, 9999)}",
                "concept_id": "equivalent-fractions",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": prompt,
                "options": options,
                "expected_answer": correct,
                "explanation": f"To scale from {orig_servings} to {target_servings} people, multiply the quantity by {multiplier}. {numerator}/{denominator} × {multiplier} = {correct_num}/{denominator} cups.",
                "misconception_map": {
                    d_add: "additive-bias",
                    d_top_only: "unequal-operations",
                    d_wrong: "reciprocal-inversion"
                },
                "is_transfer": True
            }
        else:
            # Standard equivalent fractions: a/b = ?/d
            a = random.choice([2, 3, 4, 5])
            b = random.choice([3, 5, 7, 8])
            while math_gcd(a, b) > 1:
                b += 1
            k = random.choice([2, 3, 4])
            target_den = b * k
            target_num = a * k
            prompt = f"Complete the equivalent fraction: {a}/{b} = __/{target_den}"
            correct = str(target_num)
            d_add = str(a + k)
            d_wrong_mul = str(a * (k + 1))
            d_raw = str(target_den - b)
            options = [correct, d_add, d_wrong_mul, d_raw]
            options = list(dict.fromkeys(options))  # Deduplicate
            while len(options) < 4:
                options.append(str(random.randint(10, 30)))
            random.shuffle(options)
            return {
                "id": f"gen-frac-{random.randint(1000, 9999)}",
                "concept_id": "equivalent-fractions",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": prompt,
                "options": options,
                "expected_answer": correct,
                "explanation": f"The denominator is multiplied by {k} ({b} × {k} = {target_den}). Multiply the numerator by the same factor: {a} × {k} = {correct}.",
                "misconception_map": {
                    d_add: "additive-bias",
                    d_raw: "unequal-operations"
                },
                "is_transfer": False
            }

    def _gen_linear_equation_question(self, stage: str, difficulty: str) -> dict[str, Any]:
        """Generates dynamic linear equation questions."""
        a = random.choice([2, 3, 4, 5])
        x = random.choice([3, 4, 5, 6, 7])
        b = random.choice([2, 4, 6, 8, 10])
        c = a * x + b
        var = "x"

        if difficulty == "challenge" or stage == "test":
            count = random.choice([4, 5, 6, 8])
            price = random.choice([12, 15, 18, 20, 25])
            shipping = random.choice([10, 15, 20, 30])
            total = count * price + shipping
            prompt = f"{count} identical notebooks plus a fixed delivery charge of ₹{shipping} cost ₹{total} in total. If {count}x + {shipping} = {total}, what is the cost of one notebook (x)?"
            correct = f"₹{price}"
            d_add = f"₹{(total + shipping) / count:g}"  # added the charge instead of subtracting
            d_no_div = f"₹{total - shipping}"  # subtracted but never divided
            d_mul = f"₹{(total - shipping) * count}"  # multiplied instead of dividing
            options = [correct, d_add, d_no_div, d_mul]
            random.shuffle(options)
            return {
                "id": f"gen-lin-{random.randint(1000, 9999)}",
                "concept_id": "linear-equations",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": prompt,
                "options": options,
                "expected_answer": correct,
                "explanation": f"Subtract {shipping} from {total} to get {total - shipping}, then divide by {count}: {total - shipping} ÷ {count} = ₹{price}.",
                "misconception_map": {
                    d_add: "sign-inversion-slip",
                    d_no_div: "forgot-division-slip"
                },
                "is_transfer": True
            }
        else:
            prompt = f"Solve for {var}: {a}{var} + {b} = {c}"
            correct = str(x)
            d_add = str(round((c + b) / a, 1)).replace(".0", "")
            d_no_div = str(c - b)
            d_div_err = str(x + 2)
            options = [correct, d_add, d_no_div, d_div_err]
            options = list(dict.fromkeys(options))
            while len(options) < 4:
                options.append(str(random.randint(8, 25)))
            random.shuffle(options)
            return {
                "id": f"gen-lin-{random.randint(1000, 9999)}",
                "concept_id": "linear-equations",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": prompt,
                "options": options,
                "expected_answer": correct,
                "explanation": f"Subtract {b} from both sides: {a}{var} = {c - b}. Then divide by {a}: {var} = {x}.",
                "misconception_map": {
                    d_add: "sign-inversion-slip",
                    d_no_div: "forgot-division-slip"
                },
                "is_transfer": False
            }

    def _gen_square_root_question(self, stage: str, difficulty: str) -> dict[str, Any]:
        squares = [(4, 16), (5, 25), (7, 49), (8, 64), (9, 81), (11, 121), (12, 144), (13, 169), (14, 196), (15, 225)]
        root, n = random.choice(squares)
        if difficulty == "challenge" or stage == "test":
            prompt = f"A square courtyard has an area of {n} m². What is the length of one side of the courtyard?"
            correct = f"{root} m"
            d_half = f"{n // 2} m"
            d_double = f"{root * 2} m"
            d_peri = f"{root * 4} m"
            options = [correct, d_half, d_double, d_peri]
            random.shuffle(options)
            return {
                "id": f"gen-sq-{random.randint(1000, 9999)}",
                "concept_id": "squares-roots",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": prompt,
                "options": options,
                "expected_answer": correct,
                "explanation": f"Side length of square = √Area = √{n} = {root} m.",
                "misconception_map": {
                    d_half: "square-root-halving",
                    d_peri: "perimeter-area-confusion"
                },
                "is_transfer": True
            }
        else:
            prompt = f"Find the square root of {n} (√{n}):"
            correct = str(root)
            d_half = str(n // 2)
            d_adj = str(root + 1)
            d_adj2 = str(root - 1)
            options = [correct, d_half, d_adj, d_adj2]
            random.shuffle(options)
            return {
                "id": f"gen-sq-{random.randint(1000, 9999)}",
                "concept_id": "squares-roots",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": prompt,
                "options": options,
                "expected_answer": correct,
                "explanation": f"Since {root} × {root} = {n}, √{n} = {root}.",
                "misconception_map": {
                    d_half: "square-root-halving"
                },
                "is_transfer": False
            }

    def _gen_cube_root_question(self, stage: str, difficulty: str) -> dict[str, Any]:
        cubes = [(2, 8), (3, 27), (4, 64), (5, 125), (6, 216)]
        root, n = random.choice(cubes)
        prompt = f"What is the cube root of {n} (∛{n})?"
        correct = str(root)
        d_div3 = str(n // 3)
        d_sq = str(root * root)
        d_adj = str(root + 2)
        options = [correct, d_div3, d_sq, d_adj]
        random.shuffle(options)
        return {
            "id": f"gen-cube-{random.randint(1000, 9999)}",
            "concept_id": "cubes-roots",
            "stage": stage,
            "difficulty": difficulty,
            "prompt": prompt,
            "options": options,
            "expected_answer": correct,
            "explanation": f"Since {root} × {root} × {root} = {n}, ∛{n} = {root}.",
            "misconception_map": {
                d_div3: "division-instead-of-root"
            },
            "is_transfer": stage == "test"
        }

    def _gen_quadrilateral_question(self, stage: str, difficulty: str) -> dict[str, Any]:
        a1 = random.choice([70, 80, 85, 90, 95])
        a2 = random.choice([75, 85, 100, 105])
        a3 = random.choice([60, 65, 95, 110])
        fourth = 360 - (a1 + a2 + a3)
        prompt = f"Three angles of a quadrilateral measure {a1}°, {a2}°, and {a3}°. What is the measure of the fourth angle?"
        correct = f"{fourth}°"
        d_tri = f"{abs(180 - (a1 + a2))}°"  # used the triangle's 180° as the total
        d_adj = f"{fourth + 10}°"
        d_sub = f"{360 - a1}°"
        options = [correct, d_tri, d_adj, d_sub]
        random.shuffle(options)
        return {
            "id": f"gen-quad-{random.randint(1000, 9999)}",
            "concept_id": "quadrilaterals",
            "stage": stage,
            "difficulty": difficulty,
            "prompt": prompt,
            "options": options,
            "expected_answer": correct,
            "explanation": f"Sum of interior angles of a quadrilateral is 360°. Fourth angle = 360° - ({a1}° + {a2}° + {a3}°) = {fourth}°.",
            "misconception_map": {
                d_tri: "angle-sum-slip"
            },
            "is_transfer": stage == "test"
        }

    def _gen_comparing_quantities_question(self, stage: str, difficulty: str) -> dict[str, Any]:
        price = random.choice([400, 500, 600, 800])
        disc_pct = random.choice([10, 15, 20, 25])
        disc_val = int((disc_pct / 100) * price)
        final_price = price - disc_val
        prompt = f"A school bag with Marked Price ₹{price} is offered at a {disc_pct}% discount. What is the discount amount?"
        correct = f"₹{disc_val}"
        d_final = f"₹{final_price}"
        d_raw = f"₹{disc_pct}"
        d_add = f"₹{price + disc_val}"
        options = [correct, d_final, d_raw, d_add]
        random.shuffle(options)
        return {
            "id": f"gen-cq-{random.randint(1000, 9999)}",
            "concept_id": "comparing-quantities",
            "stage": stage,
            "difficulty": difficulty,
            "prompt": prompt,
            "options": options,
            "expected_answer": correct,
            "explanation": f"Discount = ({disc_pct}/100) × ₹{price} = ₹{disc_val}.",
            "misconception_map": {
                d_final: "percentage-base-confusion",
                d_raw: "percentage-base-confusion"
            },
            "is_transfer": stage == "test"
        }

    def _gen_data_handling_question(self, stage: str, difficulty: str) -> dict[str, Any]:
        """Mean for routine items; probability for transfer items."""
        if difficulty == "challenge" or stage == "test":
            red = random.choice([2, 3, 4, 5, 7])
            blue = random.choice([3, 5, 6, 8])
            total = red + blue
            prompt = f"A bag holds {red} red and {blue} blue marbles. One marble is drawn at random. What is the probability that it is red?"
            correct = f"{red}/{total}"
            d_ratio = f"{red}/{blue}"  # favourable over unfavourable
            d_other = f"{blue}/{total}"
            d_inverted = f"{total}/{red}"
            options = [correct, d_ratio, d_other, d_inverted]
            random.shuffle(options)
            return {
                "id": f"gen-data-{random.randint(1000, 9999)}",
                "concept_id": "data-handling",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": prompt,
                "options": options,
                "expected_answer": correct,
                "explanation": f"P(red) = favourable ÷ total = {red} ÷ ({red} + {blue}) = {red}/{total}.",
                "misconception_map": {d_ratio: "probability-denominator-slip", d_inverted: "probability-denominator-slip"},
                "is_transfer": True,
            }
        mean = random.choice([5, 6, 7, 8, 9, 12])
        spread = random.choice([1, 2, 3])
        values = [mean - spread, mean, mean + spread + 3, mean - 3]
        total = sum(values)
        if total % len(values):
            values[-1] += len(values) - total % len(values)
            total = sum(values)
        correct = str(total // len(values))
        ordered = sorted(values)
        median = (ordered[1] + ordered[2]) / 2
        d_sum = str(total)  # forgot to divide
        d_median = f"{median:g}"
        d_range = str(ordered[-1] - ordered[0])
        options = [correct, d_sum, d_median, d_range]
        random.shuffle(options)
        return {
            "id": f"gen-data-{random.randint(1000, 9999)}",
            "concept_id": "data-handling",
            "stage": stage,
            "difficulty": difficulty,
            "prompt": f"Find the mean of {', '.join(str(v) for v in values)}.",
            "options": options,
            "expected_answer": correct,
            "explanation": f"Add the observations to get {total}, then divide by {len(values)}: {total} ÷ {len(values)} = {correct}.",
            "misconception_map": {d_sum: "mean-median-confusion", d_median: "mean-median-confusion"},
            "is_transfer": stage == "test",
        }

    def _gen_practical_geometry_question(self, stage: str, difficulty: str) -> dict[str, Any]:
        """Square diagonals (a measured transfer) and the five-measurement rule."""
        if difficulty == "challenge" or stage == "test":
            side, area_side = random.choice([(3, "3√2"), (5, "5√2"), (6, "6√2"), (7, "7√2"), (10, "10√2")])
            correct = f"{area_side} cm"
            d_side = f"{side} cm"
            d_double = f"{side * 2} cm"
            d_area = f"{side * side} cm"
            options = [correct, d_side, d_double, d_area]
            random.shuffle(options)
            return {
                "id": f"gen-geo-{random.randint(1000, 9999)}",
                "concept_id": "practical-geometry",
                "stage": stage,
                "difficulty": difficulty,
                "prompt": f"While constructing a square of side {side} cm, you draw its diagonal. How long is the diagonal?",
                "options": options,
                "expected_answer": correct,
                "explanation": f"By Pythagoras, diagonal = √({side}² + {side}²) = √{2 * side * side} = {area_side} cm.",
                "misconception_map": {d_double: "pythagoras-slip", d_area: "perimeter-area-confusion"},
                "is_transfer": True,
            }
        tool, purpose = random.choice([
            ("compass", "mark off a fixed distance from a point"),
            ("protractor", "measure a given angle at a vertex"),
            ("ruler", "draw a line segment of a given length"),
        ])
        others = [t for t in ["compass", "protractor", "ruler", "set square"] if t != tool]
        options = [tool, *others]
        random.shuffle(options)
        return {
            "id": f"gen-geo-{random.randint(1000, 9999)}",
            "concept_id": "practical-geometry",
            "stage": stage,
            "difficulty": difficulty,
            "prompt": f"In a quadrilateral construction, which instrument do you use to {purpose}?",
            "options": options,
            "expected_answer": tool,
            "explanation": f"The {tool} is the instrument that fixes this constraint in a construction.",
            "misconception_map": {other: "construction-tool-slip" for other in others},
            "is_transfer": stage == "test",
        }

    # -------------------------------------------------------------------------
    # 2. Personalized Remediation Generator
    # -------------------------------------------------------------------------
    def generate_remediation(
        self,
        misconception_id: str,
        student_name: str = "Learner",
        grade: int = 8
    ) -> dict[str, Any]:
        """Generates a targeted, scaffolded remediation guide for a specific cognitive barrier."""
        remediation_templates = {
            "denominator-magnitude": {
                "title": "Unpacking the Denominator: Why More Parts Make Smaller Slices",
                "cognitive_barrier": f"{student_name} perceives the denominator as an independent whole number magnitude (e.g. 8 > 3), erroneously concluding that 1/8 must exceed 1/3.",
                "concrete_analogy": "The Roti / Birthday Cake Sharing Model: If 1 whole roti is shared equally among 3 friends, each person gets a large slice (1/3). If the exact same roti is shared among 8 people, each slice must be cut much smaller (1/8) so everyone gets a portion.",
                "visual_manipulative": "Interactive SVG Fraction Bar Workbench: Place the 1/3 bar directly above the 1/8 bar. Observe that 1/3 spans more than double the length of 1/8.",
                "counter_example": "Look at 1/2 vs 1/100. 100 is a very large number, but 1/100 of a rupee is just 1 paisa, whereas 1/2 of a rupee is 50 paise. Therefore, a larger denominator means a smaller fraction value.",
                "guided_steps": [
                    "Step 1: Always sketch or view the whole unit first.",
                    "Step 2: Read the denominator as 'number of equal slices to make'.",
                    "Step 3: Remember: More cuts = thinner slices."
                ],
                "diagnostic_probe": {
                    "question": "Which fraction would give you the largest slice of cake?",
                    "options": ["1/2", "1/4", "1/8", "1/16"],
                    "correct_answer": "1/2",
                    "explanation": "Halves are the largest parts because the whole is only split into 2 pieces."
                }
            },
            "additive-bias": {
                "title": "Multiplication vs Addition: The Equivalence Ratio Lock",
                "cognitive_barrier": f"{student_name} assumes that adding the same number to top and bottom (e.g. (1+2)/(2+2) = 3/4) preserves fraction value.",
                "concrete_analogy": "The Orange Squash / Lemonade Recipe: If you have a mixture of 1 cup lemon to 2 cups water (strength 1/2), adding 2 spoons of lemon and 2 spoons of water changes the taste. To keep the exact same taste (equivalence), you must DOUBLE both ingredients (2 cups lemon, 4 cups water).",
                "visual_manipulative": "Visual 1/2 bar vs 3/4 bar comparison. 3/4 fills 75% of the bar, while 1/2 fills 50%. They are clearly not equal.",
                "counter_example": "1/2 = 0.50. Adding 1 to top and bottom gives (1+1)/(2+1) = 2/3 ≈ 0.67. Since 0.50 ≠ 0.67, addition destroys equivalence.",
                "guided_steps": [
                    "Step 1: Equivalence requires multiplying (or dividing) numerator and denominator by the SAME non-zero multiplier k.",
                    "Step 2: Never add or subtract constants from top and bottom.",
                    "Step 3: Verify using cross-multiplication: a × d must equal b × c."
                ],
                "diagnostic_probe": {
                    "question": "Which operation creates a fraction equivalent to 2/3?",
                    "options": ["Multiply top and bottom by 4", "Add 4 to top and bottom", "Subtract 1 from top and bottom", "Multiply only the top by 4"],
                    "correct_answer": "Multiply top and bottom by 4",
                    "explanation": "(2 × 4) / (3 × 4) = 8/12, which is equivalent."
                }
            },
            "unequal-operations": {
                "title": "Keeping Both Numbers in Step: The Golden Ratio Rule",
                "cognitive_barrier": f"{student_name} multiplies or divides the numerator without applying the identical operation to the denominator.",
                "concrete_analogy": "The Seesaw Balance: If you double the weight on the left side, you must double the weight on the right side to keep the balance level.",
                "visual_manipulative": "Multiplier Grid Workbench with Linked Ratio Locks.",
                "counter_example": "If you change 3/5 to 6/5 by doubling only the numerator, the fraction is now greater than 1, whereas 3/5 was less than 1.",
                "guided_steps": [
                    "Step 1: Identify the multiplier used on the given number.",
                    "Step 2: Apply the EXACT same multiplier to the remaining number.",
                    "Step 3: Simplify back to confirm you return to original fraction."
                ],
                "diagnostic_probe": {
                    "question": "To write 3/5 with denominator 20, what must you multiply the numerator by?",
                    "options": ["4", "2", "5", "15"],
                    "correct_answer": "4",
                    "explanation": "Since 5 × 4 = 20, multiply the numerator by 4: 3 × 4 = 12."
                }
            },
            "sign-inversion-slip": {
                "title": "Two-Pan Balance: Mastering Inverse Operations in Equations",
                "cognitive_barrier": f"{student_name} transposes terms without switching the algebraic sign (e.g. turning +5 into +5 across the equals sign).",
                "concrete_analogy": "The Two-Pan Physical Balance: If there are 5 extra grams on the left pan, you must REMOVE 5 grams from BOTH pans to keep it balanced.",
                "visual_manipulative": "Algebraic Balancing Scale simulation.",
                "counter_example": "In 3x + 5 = 20, if you add 5 to 20 you get 3x = 25 (x = 8.33). Checking: 3(8.33) + 5 = 30 ≠ 20! Subtraction is mandatory.",
                "guided_steps": [
                    "Step 1: Circle the operation attached to the constant term.",
                    "Step 2: Apply the inverse operation to BOTH sides of the equals sign.",
                    "Step 3: Always substitute your answer back to check LHS = RHS."
                ],
                "diagnostic_probe": {
                    "question": "In the equation 4x - 8 = 16, what is the first step to balance?",
                    "options": ["Add 8 to both sides", "Subtract 8 from both sides", "Divide by 16", "Multiply by 4"],
                    "correct_answer": "Add 8 to both sides",
                    "explanation": "The inverse of -8 is +8."
                }
            }
        }

        template = remediation_templates.get(misconception_id) or self._remediation_from_database(misconception_id, student_name)
        if template is None:
            raise ValueError(f"Unknown misconception '{misconception_id}'")

        return {
            "student_name": student_name,
            "grade": grade,
            "misconception_id": misconception_id,
            "generated_at": "Live PRISM Generative Engine",
            **template
        }

    @staticmethod
    def _remediation_from_database(misconception_id: str, student_name: str) -> dict[str, Any] | None:
        """Build a guide for any registered misconception from its database entry."""
        entry = misconception_entry(misconception_id)
        if entry is None:
            return None
        chapter = next((c for c in CHAPTERS if c["concept"] == entry["concept"]), CHAPTERS[0])
        bank = QUESTION_BANK[chapter["id"]]
        stage, prompt, options, answer, explanation = bank[0]
        return {
            "title": entry["title"],
            "cognitive_barrier": f"{student_name}: {entry['description']}",
            "concrete_analogy": entry["remedy"],
            "visual_manipulative": entry["remedy"],
            "counter_example": entry["symptoms"][0],
            "guided_steps": [
                f"Step 1: Name the error pattern: {entry['symptoms'][0]}.",
                f"Step 2: {entry['remedy']}",
                "Step 3: Answer a new question and explain the reasoning aloud.",
            ],
            "diagnostic_probe": {"question": prompt, "options": options, "correct_answer": answer, "explanation": explanation},
        }

    # -------------------------------------------------------------------------
    # 3. Differentiated Lesson Plan Generator
    # -------------------------------------------------------------------------
    def generate_lesson_plan(
        self,
        concept_id: str = "equivalent-fractions",
        classroom_code: str = "8A-CBSE",
        pod_profiles: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:
        """Generates a structured 45-minute CBSE differentiated classroom lesson plan."""
        if concept_id != "equivalent-fractions":
            return self._lesson_plan_for_chapter(concept_id, classroom_code)
        pods = pod_profiles or [
            {"group_key": "visual-support", "students": ["STU-VISUAL"], "count": 1},
            {"group_key": "foundation", "students": ["STU-FOUNDATION"], "count": 1},
            {"group_key": "guided-practice", "students": ["STU-CALC"], "count": 1},
            {"group_key": "extension", "students": ["STU-EXTEND"], "count": 1}
        ]

        return {
            "title": f"Differentiated Lesson Plan: {concept_id.replace('-', ' ').title()}",
            "classroom_code": classroom_code,
            "duration_minutes": 45,
            "curriculum_framework": "CBSE Class VIII Mathematics · NCERT Middle Stage",
            "learning_objectives": [
                "Diagnose and remediate latent misconceptions in equivalent fractions and rational numbers.",
                "Differentiate classroom instruction into 4 parallel targeted learning pods.",
                "Enable learners to justify equivalence using visual manipulatives, multiplier ratios, and real-world transfer."
            ],
            "timeline": [
                {
                    "phase": "Opening Launch & Anchor Problem",
                    "duration": "7 min",
                    "pedagogy": "Whole-Class Interactive Inquiry",
                    "teacher_prompt": "Display 1/3 and 1/8 on the board. Ask: 'If you had to share a pizza with 3 friends or 8 friends, in which case would you get more pizza? Why?' Listen for students who claim 8 is larger.",
                    "student_action": "Think-Pair-Share with elbow partner, sketch whole on mini-whiteboards."
                },
                {
                    "phase": "Parallel Pod Station Rotations",
                    "duration": "23 min",
                    "pedagogy": "Differentiated Flexible Pods (Teacher roving with targeted micro-conferences)",
                    "pods": [
                        {
                            "pod_name": "Visual Support Pod",
                            "target_barrier": "Denominator-Magnitude Misconception (1/8 > 1/3)",
                            "activity": "SVG Fraction Bar Comparator Workbench: Students manipulate fraction bars side by side with the same whole to prove that larger denominators partition into smaller parts.",
                            "teacher_checkpoint": "Check that student connects denominator size to equal parts rather than magnitude.",
                            "materials": "Tablets / PRISM Visual Fraction Bar Tool"
                        },
                        {
                            "pod_name": "Foundation Track Pod",
                            "target_barrier": "Foundational Equal-Part Partitioning Gap",
                            "activity": "Physical Paper Strip Folding: Fold strips of paper into 2, 4, and 8 equal parts. Label numerator and denominator, then shade 1/2 and 2/4 to establish equal-partitioning.",
                            "teacher_checkpoint": "Ensure learner rejects unequal slices before practicing equivalence.",
                            "materials": "Paper strips, colored highlighters, scissors"
                        },
                        {
                            "pod_name": "Guided Practice Pod",
                            "target_barrier": "Calculation & Unequal Multiplier Slips",
                            "activity": "Multiplier Grid Scaffolding: Work through structured tables multiplying top and bottom by identical integers (k = 2, 3, 5).",
                            "teacher_checkpoint": "Verify student applies multiplier to both numerator and denominator simultaneously.",
                            "materials": "Multiplication grid worksheets"
                        },
                        {
                            "pod_name": "Extension Challenge Pod",
                            "target_barrier": "High Mastery / Independent Application",
                            "activity": "Recipe Scaling & Ratio Transfer: Scale a traditional Indian Halwa recipe for 4, 8, and 12 people. Formulate and justify equivalent fractions used.",
                            "teacher_checkpoint": "Challenge learner to generalize rule for dividing fractions.",
                            "materials": "Recipe scaling challenge cards"
                        }
                    ]
                },
                {
                    "phase": "Plenary Consolidation & Synthesis",
                    "duration": "10 min",
                    "pedagogy": "Cross-Pod Synthesis",
                    "teacher_prompt": "Bring class together. Have one learner from the Visual Pod explain why 1/3 > 1/8 using their fraction bar insight, and one learner from the Extension Pod share how recipe scaling works.",
                    "student_action": "Class reflection and summarization in math journals."
                },
                {
                    "phase": "Formative Exit Ticket",
                    "duration": "5 min",
                    "pedagogy": "Independent Transfer Probe",
                    "teacher_prompt": "Distribute 2-item exit ticket: 1 standard equivalent fraction item and 1 discriminating transfer item.",
                    "student_action": "Individual submission recorded into PRISM diagnostic database."
                }
            ],
            "inspection_rubric": {
                "evidence_informed": "Pods formed dynamically from student diagnostic attempt patterns, not static achievement streaming.",
                "nep_2020_alignment": "Encourages experiential learning, visual manipulatives, and multilingual articulation."
            }
        }

    @staticmethod
    def _lesson_plan_for_chapter(concept_id: str, classroom_code: str) -> dict[str, Any]:
        """A 45-minute plan whose pods come from this chapter's own misconceptions."""
        chapter = next((c for c in CHAPTERS if c["concept"] == concept_id), None)
        title = chapter["title"] if chapter else concept_id.replace("-", " ").title()
        pods = [
            {
                "pod_name": f"{entry['recommended_route'].replace('-', ' ').title()} Pod",
                "target_barrier": entry["title"],
                "activity": entry["remedy"],
                "teacher_checkpoint": f"Listen for: {entry['symptoms'][0]}",
                "materials": "Notebook, board, and the activity described",
            }
            for entry in MISCONCEPTIONS_DATABASE
            if entry["concept"] == concept_id
        ]
        anchor = QUESTION_BANK[chapter["id"]][0][1] if chapter else f"Introduce {title} with one worked example."
        return {
            "title": f"Differentiated Lesson Plan: {title}",
            "classroom_code": classroom_code,
            "duration_minutes": 45,
            "curriculum_framework": "CBSE Class VIII Mathematics · NCERT Middle Stage",
            "learning_objectives": [
                f"Diagnose the specific errors learners make in {title}.",
                f"Differentiate instruction into {len(pods)} targeted pods for this chapter's common errors.",
                "Check understanding on a new problem before moving on.",
            ],
            "timeline": [
                {
                    "phase": "Opening Launch & Anchor Problem",
                    "duration": "7 min",
                    "pedagogy": "Whole-Class Interactive Inquiry",
                    "teacher_prompt": f"Put this on the board and ask for reasoning, not just the answer: {anchor}",
                    "student_action": "Think-Pair-Share with a partner, then write the working in a notebook.",
                },
                {
                    "phase": "Parallel Pod Station Rotations",
                    "duration": "23 min",
                    "pedagogy": "Differentiated Flexible Pods (Teacher roving with targeted micro-conferences)",
                    "pods": pods,
                },
                {
                    "phase": "Plenary Consolidation & Synthesis",
                    "duration": "10 min",
                    "pedagogy": "Cross-Pod Synthesis",
                    "teacher_prompt": "Ask one learner from each pod to explain the error their pod worked on and how to avoid it.",
                    "student_action": "Class reflection and summary in math journals.",
                },
                {
                    "phase": "Formative Exit Ticket",
                    "duration": "5 min",
                    "pedagogy": "Independent Transfer Probe",
                    "teacher_prompt": "Give a 2-item exit ticket: 1 standard item and 1 transfer item.",
                    "student_action": "Individual submission recorded in PRISM.",
                },
            ],
            "inspection_rubric": {
                "evidence_informed": "Pods target the error patterns registered for this chapter, not static achievement streaming.",
                "nep_2020_alignment": "Encourages experiential learning and multilingual articulation.",
            },
        }

    # -------------------------------------------------------------------------
    # 4. Contextual Indian Real-World Transfer Scenario Generator
    # -------------------------------------------------------------------------
    def generate_transfer_task(
        self,
        concept_id: str = "equivalent-fractions",
        theme: str = "recipes"
    ) -> dict[str, Any]:
        """Generates localized Indian real-world transfer problem scenarios."""
        themes = {
            "recipes": {
                "title": "Diwali Sooji Halwa Scaling Challenge",
                "context": "Chef Sunita is preparing Sooji Halwa for a festive family gathering in Jaipur. Her heirloom recipe is designed for 4 people and requires:",
                "ingredients": [
                    "1/2 cup coarse sooji (semolina)",
                    "3/4 cup pure ghee",
                    "2/3 cup sugar",
                    "1 1/2 cups hot water"
                ],
                "problem": "For the grand Diwali dinner, Sunita expects 12 guests (3 times the original recipe). Help Sunita calculate the exact equivalent quantities of each ingredient needed.",
                "solution_steps": [
                    "Scaling factor = 12 guests ÷ 4 guests = 3.",
                    "Sooji: 1/2 cup × 3 = 3/2 cups (1 1/2 cups).",
                    "Ghee: 3/4 cup × 3 = 9/4 cups (2 1/4 cups).",
                    "Sugar: 2/3 cup × 3 = 6/3 cups = 2 full cups.",
                    "Hot water: 3/2 cups × 3 = 9/2 cups (4 1/2 cups)."
                ],
                "pedagogical_outcome": "Applies equivalent fraction multiplication in a practical culinary proportion context."
            },
            "railways": {
                "title": "Indian Railways Vande Bharat Timetable Problem",
                "context": "The Vande Bharat Express travels between New Delhi and Varanasi. The train covers 2/5 of the total 760 km journey in the first 2 hours.",
                "problem": "What fraction of the total distance remains to be covered? How many kilometers does that represent?",
                "solution_steps": [
                    "Total journey represents 1 whole = 5/5.",
                    "Remaining fraction = 5/5 - 2/5 = 3/5 of the journey.",
                    "Remaining distance = 3/5 × 760 km = 3 × 152 = 456 km."
                ],
                "pedagogical_outcome": "Connects fraction complements (1 - a/b) to spatial distance models."
            },
            "cricket": {
                "title": "IPL Run Rate & Fraction Analysis",
                "context": "In an IPL T20 match, the chasing team needs to score at an average of 8 1/2 runs per over for the remaining 6 overs.",
                "problem": "Write 8 1/2 as an improper fraction. How many total runs must the team score in the final 6 overs?",
                "solution_steps": [
                    "8 1/2 = (8 × 2 + 1) / 2 = 17/2 runs per over.",
                    "Total runs needed = 17/2 × 6 = 17 × 3 = 51 runs."
                ],
                "pedagogical_outcome": "Multiplies rational numbers in sports analytics context."
            }
        }
        return themes.get(theme, themes["recipes"])


def math_gcd(a: int, b: int) -> int:
    import math
    return math.gcd(a, b)


# Global engine singleton
generative_engine = GenerativeEngine()

