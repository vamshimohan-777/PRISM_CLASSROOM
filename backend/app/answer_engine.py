"""PRISM Answer Engine: Pedagogical NCERT Step-by-Step Solver & Reasoning Engine.

Derives verified mathematical solutions with step-by-step NCERT reasoning,
self-verification checks, latent misconception trap warnings, prerequisite mapping,
and interactive follow-up practice challenges.
"""
from dataclasses import dataclass, field
from fractions import Fraction
import math
import os
import re
from typing import Any
import httpx

@dataclass
class SolutionStep:
    step_number: int
    title: str
    explanation: str
    math_expr: str

@dataclass
class PracticeChallenge:
    question: str
    options: list[str]
    correct_answer: str
    explanation: str

@dataclass
class AnswerResult:
    query: str
    category: str
    direct_answer: str
    confidence: float
    steps: list[dict[str, Any]]
    verification: str
    misconception_warning: str
    prerequisites: list[str]
    practice_challenge: dict[str, Any]
    source: str = "PRISM NCERT Engine"


def _fmt(value: Fraction) -> str:
    """Render an exact rational without ever losing precision to a float."""
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _term(coefficient: Fraction, var: str) -> str:
    """'3x', 'x' or '-x', never '1x'."""
    if coefficient == 1:
        return var
    if coefficient == -1:
        return f"-{var}"
    text = _fmt(coefficient)
    return f"({text}){var}" if coefficient.denominator != 1 else f"{text}{var}"


class _NotLinear(Exception):
    """The text is not a linear expression in one variable."""


class _LinearParser:
    """Recursive-descent parser reducing an expression to `coef * var + const`.

    Grammar: expr := term (('+'|'-') term)* ; term := factor (('*'|'/'|implicit) factor)* ;
    factor := number | letter | '(' expr ')' | '-' factor. All arithmetic is on
    exact Fractions, so the verification step cannot be defeated by rounding.
    """

    def __init__(self, text: str):
        self.tokens = re.findall(r"\d+(?:\.\d+)?|[a-zA-Z]|[-+*/()]", text.replace("×", "*").replace("÷", "/").replace("−", "-"))
        self.pos = 0
        self.variables: set[str] = set()

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _next(self):
        token = self._peek()
        self.pos += 1
        return token

    def parse(self) -> tuple[Fraction, Fraction]:
        result = self._expr()
        if self._peek() is not None:
            raise _NotLinear()
        return result

    def _expr(self):
        coef, const = self._term()
        while self._peek() in ("+", "-"):
            sign = 1 if self._next() == "+" else -1
            c, k = self._term()
            coef, const = coef + sign * c, const + sign * k
        return coef, const

    def _term(self):
        coef, const = self._factor()
        while self._peek() is not None and self._peek() not in ("+", "-", ")"):
            op = "*"
            if self._peek() in ("*", "/"):
                op = self._next()
            c, k = self._factor()
            if op == "*":
                if coef != 0 and c != 0:
                    raise _NotLinear()  # x * x
                coef, const = coef * k + c * const, const * k
            else:
                if c != 0 or k == 0:
                    raise _NotLinear()  # dividing by a variable, or by zero
                coef, const = coef / k, const / k
        return coef, const

    def _factor(self):
        token = self._next()
        if token is None:
            raise _NotLinear()
        if token == "-":
            c, k = self._factor()
            return -c, -k
        if token == "+":
            return self._factor()
        if token == "(":
            inner = self._expr()
            if self._next() != ")":
                raise _NotLinear()
            return inner
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            return Fraction(0), Fraction(token)
        if re.fullmatch(r"[a-zA-Z]", token):
            self.variables.add(token)
            return Fraction(1), Fraction(0)
        raise _NotLinear()


def _extract_equation(query: str) -> tuple[str, str] | None:
    """Pull `lhs = rhs` out of a sentence such as 'Find x if 2x + 3 = 7?'."""
    allowed = r"[0-9a-zA-Z+\-−*×÷/().\s]+"
    match = re.search(f"({allowed})=({allowed})", query)
    if not match:
        return None
    # Words of two or more letters are prose; the equation is what follows the last one.
    left = re.split(r"\b[a-zA-Z]{2,}\b", match.group(1))[-1].strip()
    right = re.split(r"\b[a-zA-Z]{2,}\b", match.group(2))[0].strip().rstrip(".")
    return (left, right) if left and right else None


class AnswerEngine:
    def __init__(self):
        pass

    def solve(self, query: str, concept_id: str | None = None) -> AnswerResult:
        """Solves a mathematical problem or answers a curriculum question."""
        q = (query or "").strip()
        lowered = q.lower()

        # 1. Try Linear Equation Solver
        linear_res = self._solve_linear_equation(q)
        if linear_res:
            return linear_res

        # 2. Try Rational Numbers / Fraction Comparison & Simplification Solver
        fraction_res = self._solve_fractions(q)
        if fraction_res:
            return fraction_res

        # 3. Try Square and Square Root Solver
        square_res = self._solve_square_roots(q)
        if square_res:
            return square_res

        # 4. Try Cube and Cube Root Solver
        cube_res = self._solve_cubes(q)
        if cube_res:
            return cube_res

        # 5. Try Percentages & Comparing Quantities Solver
        percent_res = self._solve_percentages(q)
        if percent_res:
            return percent_res

        # 6. Try Quadrilateral & Geometry Angle Solver
        geom_res = self._solve_quadrilaterals(q)
        if geom_res:
            return geom_res

        # 7. Try Data Handling & Mean / Probability Solver
        stats_res = self._solve_data_handling(q)
        if stats_res:
            return stats_res

        # 8. Try Conceptual NCERT Curriculum Knowledge Base
        concept_res = self._solve_conceptual(q)
        if concept_res:
            return concept_res

        # 9. Fallback: Optional LLM (Gemini) if GEMINI_API_KEY is configured
        llm_res = self._solve_with_llm_if_available(q)
        if llm_res:
            return llm_res

        # 10. Default Pedagogical Guidance Fallback
        return self._default_guidance(q)

    # -------------------------------------------------------------------------
    # Solvers
    # -------------------------------------------------------------------------

    def _solve_linear_equation(self, q: str) -> AnswerResult | None:
        """Solves any linear equation in one variable, with exact arithmetic.

        Handles a variable on both sides, brackets, fractions and negative numbers,
        and states plainly when an equation has no solution or infinitely many.
        """
        sides = _extract_equation(q)
        if not sides:
            return None
        left_parser, right_parser = _LinearParser(sides[0]), _LinearParser(sides[1])
        try:
            a, b = left_parser.parse()
            c, d = right_parser.parse()
        except (_NotLinear, ZeroDivisionError):
            return None
        variables = left_parser.variables | right_parser.variables
        if len(variables) != 1:
            return None
        var = variables.pop()
        equation = f"{sides[0]} = {sides[1]}"
        coefficient, constant = a - c, d - b
        category = "Linear Equations in One Variable (NCERT Ch 2)"
        practice = {
            "question": f"Solve: 4{var} + 3 = 19",
            "options": ["3", "4", "5.5", "16"],
            "correct_answer": "4",
            "explanation": f"Subtract 3: 4{var} = 16, then divide by 4: {var} = 4.",
        }

        if coefficient == 0:
            identity = constant == 0
            return AnswerResult(
                query=q,
                category=category,
                direct_answer="Every value of " + var + " is a solution" if identity else "No solution",
                confidence=1.0,
                steps=[{
                    "step_number": 1,
                    "title": f"Collect the {var} terms on one side",
                    "explanation": f"After moving the {var} terms, the coefficient of {var} is 0, so {var} disappears from the equation.",
                    "math_expr": f"0 × {var} = {_fmt(constant)}",
                }],
                verification=(
                    f"0 = 0 holds for every {var}, so this is an identity."
                    if identity else f"0 = {_fmt(constant)} is false for every {var}, so no value can satisfy it."
                ),
                misconception_warning="Trap Alert: Do not divide by a zero coefficient. Division by zero is undefined; read the remaining statement instead.",
                prerequisites=["linear-equations"],
                practice_challenge=practice,
            )

        value = constant / coefficient
        if a * value + b != c * value + d:  # defensive: substitute before claiming anything
            return None

        steps = [{
            "step_number": 1,
            "title": "State the linear equation",
            "explanation": f"We want to isolate {var} using inverse operations, keeping both sides equal.",
            "math_expr": equation,
        }]
        if c != 0:
            steps.append({
                "step_number": len(steps) + 1,
                "title": f"Subtract {_term(c, var)} from both sides",
                "explanation": f"Collect every {var} term on the Left Hand Side (LHS).",
                "math_expr": f"{_term(coefficient, var)} + {_fmt(b)} = {_fmt(d)}",
            })
        if b != 0:
            verb = "Subtract" if b > 0 else "Add"
            steps.append({
                "step_number": len(steps) + 1,
                "title": f"{verb} {_fmt(abs(b))} {'from' if b > 0 else 'to'} both sides",
                "explanation": f"Apply the inverse operation so the {var} term stands alone on the LHS (balancing rule).",
                "math_expr": f"{_term(coefficient, var)} = {_fmt(d)} {'-' if b > 0 else '+'} {_fmt(abs(b))} = {_fmt(constant)}",
            })
        steps.append({
            "step_number": len(steps) + 1,
            "title": f"Divide both sides by {_fmt(coefficient)}",
            "explanation": f"Divide by the coefficient of {var} to find its value.",
            "math_expr": f"{var} = {_fmt(constant)} ÷ {_fmt(coefficient)} = {_fmt(value)}",
        })

        if b != 0:
            wrong = "subtract" if b < 0 else "add"
            warning = (
                f"Trap Alert: Do not {wrong} {_fmt(abs(b))} on the right. "
                f"Undoing {'+' if b > 0 else '-'}{_fmt(abs(b))} on the left needs the opposite operation on both sides."
            )
        else:
            warning = "Trap Alert: Do not subtract the coefficient. Multiplication must be undone by division."
        return AnswerResult(
            query=q,
            category=category,
            direct_answer=f"{var} = {_fmt(value)}",
            confidence=1.0,
            steps=steps,
            verification=(
                f"Substitute {var} = {_fmt(value)}: LHS = {_fmt(a * value + b)}, RHS = {_fmt(c * value + d)}. "
                "Checked with exact arithmetic ✓."
            ),
            misconception_warning=warning,
            prerequisites=["integer-operations", "balance-method", "linear-equations"],
            practice_challenge=practice,
        )

    def _solve_fractions(self, q: str) -> AnswerResult | None:
        """Handles fraction simplification, comparison (1/8 vs 1/3), equivalence."""
        lowered = q.lower()

        def undefined(text: str) -> AnswerResult:
            return AnswerResult(
                query=q,
                category="Rational Numbers (NCERT Ch 1)",
                direct_answer="Undefined: a denominator cannot be 0",
                confidence=1.0,
                steps=[{
                    "step_number": 1,
                    "title": "Check every denominator",
                    "explanation": f"{text} has a denominator of 0. A rational number p/q requires q ≠ 0, because division by zero has no meaning.",
                    "math_expr": "p/q is defined only when q ≠ 0",
                }],
                verification="No number multiplied by 0 can give a non-zero result, so p/0 cannot have a value.",
                misconception_warning="Trap Alert: 0/5 = 0 is fine, but 5/0 is undefined. The zero matters only in the denominator.",
                prerequisites=["fraction-parts"],
                practice_challenge={
                    "question": "Which of these is NOT a rational number?",
                    "options": ["-3/4", "0", "5/0", "22/7"],
                    "correct_answer": "5/0",
                    "explanation": "The denominator cannot be 0.",
                },
            )

        # Fraction comparison: e.g. "compare 1/3 and 1/8", "which is larger 1/3 or 1/8", "is 1/8 > 1/3"
        comp_match = re.search(r"(-?\d+)/(\d+)\s*(?:and|or|vs\.?|than|>|<|compared to|with)\s*(-?\d+)/(\d+)", lowered)
        if comp_match:
            n1, d1, n2, d2 = [int(x) for x in comp_match.groups()]
            if d1 == 0 or d2 == 0:
                return undefined(f"{n1}/{d1} or {n2}/{d2}")
            f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
            sym = ">" if f1 > f2 else "<" if f1 < f2 else "="
            first, second = f"{n1}/{d1}", f"{n2}/{d2}"
            lcm_d = (d1 * d2) // math.gcd(d1, d2)
            eq_n1, eq_n2 = n1 * (lcm_d // d1), n2 * (lcm_d // d2)
            if sym == "=":
                direct = f"{first} = {second} (they are equivalent fractions)"
            else:
                larger, smaller = (first, second) if f1 > f2 else (second, first)
                direct = f"{first} {sym} {second} (i.e. {larger} is greater than {smaller})"
            return AnswerResult(
                query=q,
                category="Rational Numbers: Comparison & Magnitude (NCERT Ch 1)",
                direct_answer=direct,
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Read what the denominators mean",
                        "explanation": f"The denominator tells us how many equal parts the whole is split into: {d1} parts for {first} and {d2} parts for {second}. Parts of different sizes cannot be compared directly.",
                        "math_expr": "Piece size ∝ 1 / Denominator"
                    },
                    {
                        "step_number": 2,
                        "title": f"Convert to common denominator (LCM = {lcm_d})",
                        "explanation": "Multiply each fraction so both use equal-sized parts.",
                        "math_expr": f"{first} = ({n1} × {lcm_d // d1})/({d1} × {lcm_d // d1}) = {eq_n1}/{lcm_d}\n{second} = ({n2} × {lcm_d // d2})/({d2} × {lcm_d // d2}) = {eq_n2}/{lcm_d}"
                    },
                    {
                        "step_number": 3,
                        "title": "Compare the numerators",
                        "explanation": f"Since {eq_n1} {sym} {eq_n2}, we conclude that {first} {sym} {second}.",
                        "math_expr": f"{eq_n1}/{lcm_d} {sym} {eq_n2}/{lcm_d}  ⟹  {first} {sym} {second}"
                    }
                ],
                verification=f"Exact check: {eq_n1}/{lcm_d} {sym} {eq_n2}/{lcm_d} ✓. As decimals, {first} ≈ {float(f1):.3f} and {second} ≈ {float(f2):.3f}.",
                misconception_warning="Trap Alert (Denominator-Magnitude Misconception): A common mistake is believing 1/8 > 1/3 because 8 > 3. With fractions, more parts make each individual piece SMALLER, not larger!",
                prerequisites=["fraction-parts", "fraction-magnitude", "equivalent-fractions"],
                practice_challenge={
                    "question": "Which statement is true?",
                    "options": ["1/4 > 1/2", "1/5 > 1/3", "1/2 > 1/4", "1/6 > 1/3"],
                    "correct_answer": "1/2 > 1/4",
                    "explanation": "Halves are larger pieces than fourths (0.5 > 0.25)."
                }
            )

        # Fraction simplification: e.g. "simplify 18/24", "reduce 12/18", "standard form of 15/25"
        simp_match = re.search(r"(?:simplify|reduce|standard form(?: of)?)\s*(-?\d+)/(\d+)", lowered)
        if simp_match:
            num = int(simp_match.group(1))
            den = int(simp_match.group(2))
            if den == 0:
                return undefined(f"{num}/{den}")
            g = math.gcd(abs(num), den)
            s_num = num // g
            s_den = den // g
            return AnswerResult(
                query=q,
                category="Rational Numbers: Standard Form & Simplification",
                direct_answer=f"{s_num}/{s_den}",
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Find the Highest Common Factor (HCF / GCD)",
                        "explanation": f"Find the greatest integer that divides both numerator ({abs(num)}) and denominator ({den}).",
                        "math_expr": f"HCF({abs(num)}, {den}) = {g}"
                    },
                    {
                        "step_number": 2,
                        "title": f"Divide numerator and denominator by HCF = {g}",
                        "explanation": "Dividing both terms by the same factor yields an equivalent fraction in standard form.",
                        "math_expr": f"({num} ÷ {g}) / ({den} ÷ {g}) = {s_num}/{s_den}"
                    }
                ],
                verification=f"Check: Cross-multiply {num} × {s_den} = {num * s_den}, and {den} × {s_num} = {den * s_num}. Products are equal, confirming equivalence ✓.",
                misconception_warning="Trap Alert: Both numerator and denominator must be divided by the exact same number. Dividing only one produces an unequal fraction.",
                prerequisites=["simplification", "fraction-parts"],
                practice_challenge={
                    "question": "Reduce 14/21 to standard form:",
                    "options": ["2/3", "7/10", "1/2", "4/7"],
                    "correct_answer": "2/3",
                    "explanation": "Divide both by HCF(14, 21) = 7: 14÷7 = 2, 21÷7 = 3."
                }
            )

        # Missing equivalent fraction: e.g. "3/5 = ?/10" or "3/5 = __/10"
        eq_match = re.search(r"(\d+)/(\d+)\s*=\s*(?:\?|_+)\s*/\s*(\d+)", q)
        if eq_match:
            n1, d1, d2 = int(eq_match.group(1)), int(eq_match.group(2)), int(eq_match.group(3))
            if d1 == 0 or d2 == 0:
                return undefined(f"{n1}/{d1} = ?/{d2}")
            multiplier = Fraction(d2, d1)
            target = n1 * multiplier
            target_n = _fmt(target)
            return AnswerResult(
                query=q,
                category="Rational Numbers: Equivalent Fractions",
                direct_answer=(
                    f"{target_n} (i.e. {n1}/{d1} = {target_n}/{d2})"
                    if target.denominator == 1
                    else f"{target_n} (not a whole number, so {n1}/{d1} has no equivalent with denominator {d2} and a whole-number numerator)"
                ),
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": f"Find multiplier between denominators",
                        "explanation": f"Divide target denominator {d2} by initial denominator {d1}.",
                        "math_expr": f"{d2} ÷ {d1} = {_fmt(multiplier)}"
                    },
                    {
                        "step_number": 2,
                        "title": f"Multiply numerator by same factor",
                        "explanation": f"To maintain mathematical equivalence, multiply the numerator {n1} by the same factor.",
                        "math_expr": f"{n1} × {_fmt(multiplier)} = {target_n}"
                    }
                ],
                verification=f"Check by cross-multiplying: {n1} × {d2} = {n1 * d2} and {d1} × {target_n} = {_fmt(d1 * target)} ✓.",
                misconception_warning="Trap Alert: Never add numbers to both sides (e.g. adding 5). Equivalence is strictly multiplicative.",
                prerequisites=["equivalent-fractions"],
                practice_challenge={
                    "question": "Complete: 2/7 = __/28",
                    "options": ["4", "8", "14", "16"],
                    "correct_answer": "8",
                    "explanation": "Denominator 7 is multiplied by 4 (7 × 4 = 28). Numerator 2 × 4 = 8."
                }
            )

        return None

    def _solve_square_roots(self, q: str) -> AnswerResult | None:
        """Handles square roots: e.g. sqrt(144), square root of 81."""
        lowered = q.lower()
        m = re.search(r"(?:sqrt|square root of|square root)\s*\(?(\d+)\)?", lowered)
        if m:
            n = int(m.group(1))
            root = math.isqrt(n)
            is_perfect = (root * root == n)

            # Prime factorisation
            temp = n
            factors = []
            d = 2
            while d * d <= temp:
                while temp % d == 0:
                    factors.append(d)
                    temp //= d
                d += 1
            if temp > 1:
                factors.append(temp)

            factor_str = " × ".join(str(f) for f in factors) or str(n)

            if is_perfect:
                return AnswerResult(
                    query=q,
                    category="Squares and Square Roots (NCERT Ch 6)",
                    direct_answer=f"√{n} = {root}",
                    confidence=1.0,
                    steps=[
                        {
                            "step_number": 1,
                            "title": "Prime factorisation of the number",
                            "explanation": f"Express {n} as a product of prime numbers.",
                            "math_expr": f"{n} = {factor_str}"
                        },
                        {
                            "step_number": 2,
                            "title": "Group prime factors into pairs",
                            "explanation": "Since every square number has factors in pairs of identical primes, group them in twos.",
                            "math_expr": "Pairs: " + " ".join(f"({f}×{f})" for f in factors[::2])
                        },
                        {
                            "step_number": 3,
                            "title": "Take one factor from each pair",
                            "explanation": f"Multiply one prime factor from each pair to obtain the principal square root.",
                            "math_expr": f"√{n} = {root}"
                        }
                    ],
                    verification=f"Check by squaring: {root}² = {root} × {root} = {root * root} = {n} ✓.",
                    misconception_warning=(
                        f"Trap Alert (Halving Fallacy): √{n} is NOT {n // 2}! Square root means finding what number multiplied by itself gives {n}, not dividing by 2."
                        if n // 2 != root
                        else "Trap Alert (Halving Fallacy): Square root means finding what number multiplied by itself gives the value, not dividing by 2. They only agree here by coincidence."
                    ),
                    prerequisites=["prime-factorisation", "multiplication", "squares-roots"],
                    practice_challenge={
                        "question": "What is the square root of 196?",
                        "options": ["12", "14", "16", "98"],
                        "correct_answer": "14",
                        "explanation": "14 × 14 = 196 (98 is half, which is the halving fallacy trap)."
                    }
                )
            else:
                return AnswerResult(
                    query=q,
                    category="Squares and Square Roots",
                    direct_answer=f"√{n} ≈ {math.sqrt(n):.3f} (Not a perfect square)",
                    confidence=1.0,
                    steps=[
                        {
                            "step_number": 1,
                            "title": "Check prime factor pairs",
                            "explanation": f"Factors: {factor_str}. The prime factors cannot all be grouped into complete pairs.",
                            "math_expr": f"{n} is not a perfect square."
                        }
                    ],
                    verification=f"The nearest perfect squares are {root**2} (root {root}) and {(root+1)**2} (root {root+1}).",
                    misconception_warning="Notice: Only numbers with all prime factors in complete pairs are perfect squares.",
                    prerequisites=["squares-roots"],
                    practice_challenge={
                        "question": "Which of these is a perfect square?",
                        "options": ["18", "25", "30", "45"],
                        "correct_answer": "25",
                        "explanation": "5 × 5 = 25."
                    }
                )
        return None

    def _solve_cubes(self, q: str) -> AnswerResult | None:
        """Handles cube roots: e.g. cbrt(64), cube root of 125."""
        lowered = q.lower()
        m = re.search(r"(?:cbrt|cube root of|cube root)\s*\(?(\d+)\)?", lowered)
        if m:
            n = int(m.group(1))
            root = round(n ** (1 / 3))
            if root ** 3 != n:
                below = next(r for r in range(root + 1, -1, -1) if r ** 3 < n) if n > 0 else 0
                return AnswerResult(
                    query=q,
                    category="Cubes and Cube Roots (NCERT Ch 7)",
                    direct_answer=f"∛{n} ≈ {n ** (1 / 3):.3f} (Not a perfect cube)",
                    confidence=1.0,
                    steps=[{
                        "step_number": 1,
                        "title": "Check for prime factor triplets",
                        "explanation": f"{n} lies between the perfect cubes {below ** 3} and {(below + 1) ** 3}, so its prime factors cannot all be grouped into triplets.",
                        "math_expr": f"{below}³ = {below ** 3} < {n} < {(below + 1) ** 3} = {below + 1}³",
                    }],
                    verification=f"{n ** (1 / 3):.3f}³ ≈ {(n ** (1 / 3)) ** 3:.3f}. The cube root is irrational, so the decimal is an approximation.",
                    misconception_warning="Notice: Only numbers whose prime factors all occur in groups of three are perfect cubes.",
                    prerequisites=["cubes-roots", "prime-factorisation"],
                    practice_challenge={
                        "question": "Which of these is a perfect cube?",
                        "options": ["100", "125", "150", "200"],
                        "correct_answer": "125",
                        "explanation": "5 × 5 × 5 = 125.",
                    },
                )
            return AnswerResult(
                query=q,
                category="Cubes and Cube Roots (NCERT Ch 7)",
                direct_answer=f"∛{n} = {root}",
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Prime factorisation triplets",
                        "explanation": f"For a cube root, we group identical prime factors into triplets (groups of 3).",
                        "math_expr": f"{root} × {root} × {root} = {root ** 3} = {n}"
                    },
                    {
                        "step_number": 2,
                        "title": "Extract one factor per triplet",
                        "explanation": f"Take one factor from each triplet of 3 identical primes.",
                        "math_expr": f"∛{n} = {root}"
                    }
                ],
                verification=f"Check: {root}³ = {root} × {root} × {root} = {n} ✓.",
                misconception_warning=f"Trap Alert: Cube root is NOT dividing by 3! ∛{n} is {root} because {root}×{root}×{root} = {n}.",
                prerequisites=["cubes-roots", "prime-factorisation"],
                practice_challenge={
                    "question": "What is the cube root of 216?",
                    "options": ["4", "6", "8", "72"],
                    "correct_answer": "6",
                    "explanation": "6 × 6 × 6 = 216."
                }
            )
        return None

    def _solve_percentages(self, q: str) -> AnswerResult | None:
        """Handles percentages and discounts: e.g. 25% of 500, 10% discount on 500."""
        lowered = q.lower()

        # Discount: e.g. "10% discount on 500"
        m_disc = re.search(r"(\d+)%\s*discount\s*(?:on|of)?\s*(?:₹|rs\.?)?\s*(\d+)", lowered)
        if m_disc:
            pct = int(m_disc.group(1))
            orig = int(m_disc.group(2))
            disc = (pct / 100) * orig
            final_p = orig - disc
            disc_int = int(disc) if disc.is_integer() else disc
            final_int = int(final_p) if final_p.is_integer() else final_p
            return AnswerResult(
                query=q,
                category="Comparing Quantities: Discount (NCERT Ch 8)",
                direct_answer=f"Discount = ₹{disc_int} (Final Sale Price = ₹{final_int})",
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Convert percentage to fraction",
                        "explanation": f"{pct}% means {pct} parts per 100.",
                        "math_expr": f"{pct}% = {pct} / 100"
                    },
                    {
                        "step_number": 2,
                        "title": f"Calculate discount amount on Marked Price ₹{orig}",
                        "explanation": f"Multiply Marked Price by the discount rate.",
                        "math_expr": f"Discount = ({pct} / 100) × ₹{orig} = ₹{disc_int}"
                    },
                    {
                        "step_number": 3,
                        "title": "Calculate final discounted price",
                        "explanation": f"Subtract the discount from marked price.",
                        "math_expr": f"Sale Price = ₹{orig} - ₹{disc_int} = ₹{final_int}"
                    }
                ],
                verification=f"Check: (Discount ₹{disc_int} / Marked Price ₹{orig}) × 100% = {pct}% ✓.",
                misconception_warning="Trap Alert: Always calculate discount on Marked Price (original price), never on the final sale price.",
                prerequisites=["fractions", "percentages", "comparing-quantities"],
                practice_challenge={
                    "question": "A ₹800 jacket is on 20% discount. What is the discount?",
                    "options": ["₹80", "₹160", "₹200", "₹640"],
                    "correct_answer": "₹160",
                    "explanation": "20/100 × 800 = ₹160 (₹640 is the remaining price)."
                }
            )

        # General percent: e.g. "25% of 500"
        m_pct = re.search(r"(\d+)%\s*of\s*(\d+)", lowered)
        if m_pct:
            pct = int(m_pct.group(1))
            val = int(m_pct.group(2))
            ans = (pct / 100) * val
            ans_int = int(ans) if ans.is_integer() else round(ans, 2)
            return AnswerResult(
                query=q,
                category="Comparing Quantities: Percentages",
                direct_answer=f"{ans_int}",
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Write percentage as fraction out of 100",
                        "explanation": f"Percent comes from 'per centum' (out of 100).",
                        "math_expr": f"{pct}% = {pct} / 100"
                    },
                    {
                        "step_number": 2,
                        "title": f"Multiply fraction by {val}",
                        "explanation": f"Multiply: ({pct} × {val}) ÷ 100.",
                        "math_expr": f"({pct} × {val}) / 100 = {pct * val} / 100 = {ans_int}"
                    }
                ],
                verification=f"Check: ({ans_int} / {val}) × 100% = {pct}% ✓.",
                misconception_warning="Trap Alert: Don't forget to divide by 100 when computing percentages.",
                prerequisites=["percentages", "fractions"],
                practice_challenge={
                    "question": "What is 15% of 200?",
                    "options": ["15", "30", "45", "60"],
                    "correct_answer": "30",
                    "explanation": "15/100 × 200 = 30."
                }
            )

        return None

    def _solve_quadrilaterals(self, q: str) -> AnswerResult | None:
        """Handles quadrilaterals: interior angle sum (360°), finding 4th angle."""
        lowered = q.lower()
        if "quadrilateral" in lowered and ("angle" in lowered or "interior" in lowered or "sum" in lowered):
            # Check if 3 angles are given: e.g. 90, 85, 110
            angles = [int(x) for x in re.findall(r"\b(\d{2,3})°?\b", q) if int(x) < 360]
            if len(angles) >= 3:
                a1, a2, a3 = angles[0], angles[1], angles[2]
                fourth = 360 - (a1 + a2 + a3)
                if fourth <= 0:
                    return AnswerResult(
                        query=q,
                        category="Understanding Quadrilaterals: Angle Sum (NCERT Ch 3)",
                        direct_answer=f"Impossible: {a1}° + {a2}° + {a3}° already reaches {a1 + a2 + a3}°",
                        confidence=1.0,
                        steps=[{
                            "step_number": 1,
                            "title": "Apply the angle sum theorem",
                            "explanation": "The four interior angles must total exactly 360°, so three of them must total less than 360°.",
                            "math_expr": f"{a1}° + {a2}° + {a3}° = {a1 + a2 + a3}° ≥ 360°",
                        }],
                        verification="No positive fourth angle exists, so no such quadrilateral can be drawn.",
                        misconception_warning="Trap Alert: Check that the given measurements are possible before calculating.",
                        prerequisites=["angle-sum-property", "quadrilaterals"],
                        practice_challenge={
                            "question": "Three angles of a quadrilateral are 100°, 80°, and 110°. What is the fourth?",
                            "options": ["70°", "80°", "90°", "110°"],
                            "correct_answer": "70°",
                            "explanation": "360° - (100° + 80° + 110°) = 70°.",
                        },
                    )
                return AnswerResult(
                    query=q,
                    category="Understanding Quadrilaterals: Angle Sum (NCERT Ch 3)",
                    direct_answer=f"{fourth}°",
                    confidence=1.0,
                    steps=[
                        {
                            "step_number": 1,
                            "title": "State Quadrilateral Angle Sum Theorem",
                            "explanation": "Any 4-sided polygon can be partitioned into two triangles by drawing one diagonal. Since each triangle has angle sum 180°, the total interior angle sum of a quadrilateral is 2 × 180° = 360°.",
                            "math_expr": "∠A + ∠B + ∠C + ∠D = 360°"
                        },
                        {
                            "step_number": 2,
                            "title": f"Sum known angles: {a1}° + {a2}° + {a3}°",
                            "explanation": "Add the three known angles.",
                            "math_expr": f"{a1}° + {a2}° + {a3}° = {a1 + a2 + a3}°"
                        },
                        {
                            "step_number": 3,
                            "title": "Subtract from 360° to find the fourth angle",
                            "explanation": f"Subtract the combined sum from 360°.",
                            "math_expr": f"∠D = 360° - {a1 + a2 + a3}° = {fourth}°"
                        }
                    ],
                    verification=f"Check: {a1}° + {a2}° + {a3}° + {fourth}° = {a1 + a2 + a3 + fourth}° = 360° ✓.",
                    misconception_warning="Trap Alert: Do not use 180° for quadrilaterals! 180° is the angle sum of a triangle, while quadrilaterals have 360°.",
                    prerequisites=["angle-sum-property", "triangles", "quadrilaterals"],
                    practice_challenge={
                        "question": "Three angles of a quadrilateral are 100°, 80°, and 110°. What is the fourth?",
                        "options": ["70°", "80°", "90°", "110°"],
                        "correct_answer": "70°",
                        "explanation": "360° - (100° + 80° + 110°) = 360° - 290° = 70°."
                    }
                )

            return AnswerResult(
                query=q,
                category="Understanding Quadrilaterals (NCERT Ch 3)",
                direct_answer="The sum of the interior angles of any quadrilateral is always 360°.",
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Divide quadrilateral into 2 triangles",
                        "explanation": "Join any two opposite vertices with a diagonal. This splits the quadrilateral into 2 disjoint triangles.",
                        "math_expr": "(n - 2) × 180° = (4 - 2) × 180° = 360°"
                    },
                    {
                        "step_number": 2,
                        "title": "Add angle sums of both triangles",
                        "explanation": "Each triangle contributes 180°. 180° + 180° = 360°.",
                        "math_expr": "180° + 180° = 360°"
                    }
                ],
                verification="Check for a rectangle/square: 90° + 90° + 90° + 90° = 360° ✓.",
                misconception_warning="Trap Alert: Polygons with n sides have angle sum (n - 2) × 180°. For 4 sides: 2 × 180° = 360°.",
                prerequisites=["quadrilaterals"],
                practice_challenge={
                    "question": "In a parallelogram, opposite angles are always:",
                    "options": ["Equal", "Complementary (add to 90°)", "Unequal", "Zero"],
                    "correct_answer": "Equal",
                    "explanation": "Opposite angles of a parallelogram are equal in measure."
                }
            )

        return None

    def _solve_data_handling(self, q: str) -> AnswerResult | None:
        """Handles mean and probability."""
        lowered = q.lower()
        if "mean" in lowered:
            nums = [float(x) for x in re.findall(r"\b\d+\.?\d*\b", q)]
            if nums:
                s = sum(nums)
                count = len(nums)
                mean_val = s / count
                mean_str = f"{int(mean_val) if mean_val.is_integer() else round(mean_val, 2)}"
                return AnswerResult(
                    query=q,
                    category="Data Handling: Arithmetic Mean (NCERT Ch 5)",
                    direct_answer=f"Mean = {mean_str}",
                    confidence=1.0,
                    steps=[
                        {
                            "step_number": 1,
                            "title": "Sum all observations",
                            "explanation": f"Add all {count} data values together.",
                            "math_expr": f"Sum = {' + '.join(str(int(x) if x.is_integer() else x) for x in nums)} = {int(s) if s.is_integer() else s}"
                        },
                        {
                            "step_number": 2,
                            "title": f"Divide sum by total number of observations ({count})",
                            "explanation": "Mean is defined as the arithmetic average: Sum / Count.",
                            "math_expr": f"Mean = {int(s) if s.is_integer() else s} ÷ {count} = {mean_str}"
                        }
                    ],
                    verification=f"Check: Mean × Count = {mean_str} × {count} = {int(s) if s.is_integer() else s} ✓.",
                    misconception_warning="Trap Alert: The mean is NOT the middle number (that is the median). The mean accounts for all values equally.",
                    prerequisites=["data-handling", "division"],
                    practice_challenge={
                        "question": "What is the mean of 10, 20, and 30?",
                        "options": ["15", "20", "25", "60"],
                        "correct_answer": "20",
                        "explanation": "(10 + 20 + 30) / 3 = 60 / 3 = 20."
                    }
                )

        if "coin" in lowered and "probability" in lowered:
            return AnswerResult(
                query=q,
                category="Data Handling: Probability",
                direct_answer="P(Heads) = 1/2 (or 50%)",
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Count total possible outcomes",
                        "explanation": "A fair coin has 2 equally likely outcomes: Heads (H) or Tails (T).",
                        "math_expr": "Total outcomes = 2"
                    },
                    {
                        "step_number": 2,
                        "title": "Count favorable outcomes",
                        "explanation": "Getting Heads is 1 favorable outcome.",
                        "math_expr": "P(E) = Favorable / Total = 1 / 2"
                    }
                ],
                verification="P(Heads) + P(Tails) = 1/2 + 1/2 = 1 (Certain event) ✓.",
                misconception_warning="Trap Alert: Probability is always bounded between 0 (impossible) and 1 (certain).",
                prerequisites=["data-handling"],
                practice_challenge={
                    "question": "When rolling a standard 6-sided die, probability of getting a 5 is:",
                    "options": ["1/6", "5/6", "1/2", "1/5"],
                    "correct_answer": "1/6",
                    "explanation": "5 is one outcome out of 6 equally likely outcomes."
                }
            )

        return None

    def _solve_conceptual(self, q: str) -> AnswerResult | None:
        """Answers standard NCERT definition and conceptual questions."""
        lowered = q.lower()

        if "rational number" in lowered:
            return AnswerResult(
                query=q,
                category="Rational Numbers (NCERT Class VIII Ch 1)",
                direct_answer="A rational number is any number that can be expressed in the form p/q, where p and q are integers and q ≠ 0.",
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Definition & Conditions",
                        "explanation": "p is the numerator (any integer positive, negative, or zero), and q is the denominator (any non-zero integer).",
                        "math_expr": "x = p / q  (p, q ∈ ℤ, q ≠ 0)"
                    },
                    {
                        "step_number": 2,
                        "title": "Examples of Rational Numbers",
                        "explanation": "All integers, fractions, and terminating or repeating decimals are rational numbers.",
                        "math_expr": "Examples: 2/3, -5/8, 7 (= 7/1), 0 (= 0/1), 0.75 (= 3/4)"
                    }
                ],
                verification="Check: Can zero be written as p/q? Yes: 0 = 0/1. Can denominator be 0? No, division by zero is undefined.",
                misconception_warning="Trap Alert: Zero IS a rational number (0 = 0/1). But 1/0 is NOT a rational number because division by zero is mathematically undefined.",
                prerequisites=["integers", "fractions"],
                practice_challenge={
                    "question": "Which of these is NOT a rational number?",
                    "options": ["-3/4", "0", "5/0", "22/7"],
                    "correct_answer": "5/0",
                    "explanation": "Denominator cannot be 0."
                }
            )

        if "equivalent fraction" in lowered:
            return AnswerResult(
                query=q,
                category="Rational Numbers: Equivalent Fractions",
                direct_answer="Fractions that name the exact same quantity or region of a whole, obtained by multiplying or dividing numerator and denominator by the same non-zero number.",
                confidence=1.0,
                steps=[
                    {
                        "step_number": 1,
                        "title": "Fundamental Multiplicative Property",
                        "explanation": "For any fraction a/b and non-zero integer m, multiplying both terms by m preserves the ratio.",
                        "math_expr": "a / b = (a × m) / (b × m)  (m ≠ 0)"
                    },
                    {
                        "step_number": 2,
                        "title": "Visual Representation",
                        "explanation": "1/2 represents the exact same shaded area as 2/4 and 3/6 when the whole is identical in size.",
                        "math_expr": "1/2 = 2/4 = 3/6 = 4/8"
                    }
                ],
                verification="Cross multiplication rule: a/b = c/d if and only if a × d = b × c.",
                misconception_warning="Trap Alert (Additive Bias): Adding numbers to numerator and denominator does NOT make an equivalent fraction! (e.g. 1/2 ≠ (1+1)/(2+1) = 2/3).",
                prerequisites=["fraction-parts", "simplification"],
                practice_challenge={
                    "question": "Which fraction is equivalent to 3/4?",
                    "options": ["4/5", "6/8", "9/10", "3/8"],
                    "correct_answer": "6/8",
                    "explanation": "(3 × 2) / (4 × 2) = 6/8."
                }
            )

        return None

    def _solve_with_llm_if_available(self, q: str) -> AnswerResult | None:
        """Calls Gemini API if GEMINI_API_KEY is configured in the environment."""
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            return None

        try:
            model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            prompt = (
                "You are the PRISM NCERT Class VIII Mathematics Answer Engine. "
                "Solve this question pedagogically: '" + q + "'. "
                "Output JSON with keys: direct_answer, category, steps (array of {step_number, title, explanation, math_expr}), "
                "verification, misconception_warning, prerequisites (array of strings), "
                "practice_challenge ({question, options, correct_answer, explanation}). Output ONLY raw JSON."
            )
            with httpx.Client(timeout=8.0) as client:
                res = client.post(url, headers={"x-goog-api-key": api_key}, json={"contents": [{"parts": [{"text": prompt}]}]})
                if res.status_code == 200:
                    data = res.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    clean_json = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
                    clean_json = re.sub(r"\s*```$", "", clean_json, flags=re.MULTILINE).strip()
                    import json
                    parsed = json.loads(clean_json)
                    return AnswerResult(
                        query=q,
                        category=parsed.get("category", "CBSE Mathematics"),
                        direct_answer=parsed.get("direct_answer", ""),
                        # Nothing here has been checked by the symbolic solvers.
                        confidence=0.5,
                        steps=parsed.get("steps", []),
                        verification=parsed.get("verification", ""),
                        misconception_warning=parsed.get("misconception_warning", ""),
                        prerequisites=parsed.get("prerequisites", []),
                        practice_challenge=parsed.get("practice_challenge", {}),
                        source="Gemini fallback (not verified by PRISM's solvers)"
                    )
        except Exception:
            pass
        return None

    def _default_guidance(self, q: str) -> AnswerResult:
        """An honest 'not solved' result for anything no solver recognises."""
        return AnswerResult(
            query=q,
            category="Outside the solver's scope",
            direct_answer="PRISM could not solve this question. Try a form such as 3x + 5 = 20, compare 1/3 and 1/8, or cube root of 64.",
            confidence=0.0,
            steps=[
                {
                    "step_number": 1,
                    "title": "Identify the mathematical operation",
                    "explanation": "Separate the given values, the unknown, and the operation the question asks for.",
                    "math_expr": "Given ⟶ Formula or property ⟶ Step-by-step working"
                },
                {
                    "step_number": 2,
                    "title": "Find the matching chapter",
                    "explanation": "Open the Curriculum page to find the concept and its prerequisites.",
                    "math_expr": "Check the answer by substituting it back into the question"
                }
            ],
            verification="No answer was produced, so there is nothing to verify.",
            misconception_warning="PRISM does not guess. Without a matching solver it reports that it has no answer.",
            prerequisites=[],
            practice_challenge={
                "question": "Which fraction is equivalent to 1/2?",
                "options": ["2/3", "2/4", "3/4", "1/4"],
                "correct_answer": "2/4",
                "explanation": "Multiply numerator and denominator of 1/2 by 2."
            }
        )


# Global engine singleton
answer_engine = AnswerEngine()
