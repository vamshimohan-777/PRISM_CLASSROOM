"""PRISM Search Engine: High-performance, curriculum-aware indexed search.

Indexes CBSE Class VIII Mathematics concepts, prerequisite DAG nodes,
question banks, student misconceptions, and pedagogical intervention strategies.
Supports faceted filtering, relevance ranking, and highlight snippet extraction.
"""
from dataclasses import dataclass, field
import re
from typing import Any
from .catalog import CHAPTERS, QUESTION_BANK
from .curriculum import CBSE_CURRICULUM
from .engine import CONCEPT_GRAPH, INTERVENTION_LIBRARY

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
    }
]

@dataclass
class SearchResult:
    id: str
    type: str  # "chapter" | "concept" | "question" | "misconception" | "intervention"
    title: str
    snippet: str
    relevance_score: float
    chapter_id: str | None = None
    concept_id: str | None = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class SearchEngine:
    def __init__(self):
        self.index: list[dict[str, Any]] = []
        self._build_index()

    def _build_index(self):
        """Constructs the unified search index across all pedagogical entities."""
        # 1. Chapters
        for ch in CHAPTERS:
            self.index.append({
                "id": ch["id"],
                "type": "chapter",
                "title": f"Chapter {ch['number']}: {ch['title']}",
                "text": f"Chapter {ch['number']} {ch['title']} {ch['summary']} concept {ch['concept']} CBSE Mathematics Class 8 NCERT",
                "chapter_id": ch["id"],
                "concept_id": ch["concept"],
                "tags": ["chapter", "cbse", "ncert", f"chapter-{ch['number']}", ch["concept"]],
                "metadata": {
                    "number": ch["number"],
                    "minutes": ch["minutes"],
                    "summary": ch["summary"],
                    "color": ch.get("color", "violet"),
                }
            })

        # 2. Prerequisite DAG Concepts
        concept_descriptions = {
            "fraction-parts": "Identify equal-sized unit parts and name numerator/denominator before comparing.",
            "fraction-magnitude": "Reason about size of unit fractions and connect denominator to piece size.",
            "simplification": "Reduce fractions to standard form using common factors and greatest common divisor.",
            "equivalent-fractions": "Multiply or divide numerator and denominator by identical non-zero factors.",
            "linear-equations": "Model and balance equations with one variable using inverse operations.",
            "quadrilaterals": "Properties of 4-sided figures, angle sum theorem (360 degrees), and parallelograms.",
            "practical-geometry": "Accurate geometric construction using compass, ruler, and protractor.",
            "data-handling": "Organize data, read double bar graphs, frequency tables, and calculate basic probability.",
            "squares-roots": "Identify square numbers, Pythagorean triplets, and square root extraction by prime factorisation.",
            "cubes-roots": "Explore cubic numbers, prime factorisation patterns, and cube roots of perfect cubes.",
            "comparing-quantities": "Ratios, percentages, profit and loss, discount, and compound interest calculations."
        }
        for concept_id, parents in CONCEPT_GRAPH.items():
            desc = concept_descriptions.get(concept_id, f"Core learning concept for {concept_id}")
            self.index.append({
                "id": f"concept-{concept_id}",
                "type": "concept",
                "title": f"Concept: {concept_id.replace('-', ' ').title()}",
                "text": f"{concept_id} {desc} prerequisites: {' '.join(parents)}",
                "chapter_id": "rational-numbers" if "fraction" in concept_id or concept_id == "simplification" else concept_id,
                "concept_id": concept_id,
                "tags": ["concept", "prerequisite-dag", concept_id] + parents,
                "metadata": {
                    "prerequisites": parents,
                    "description": desc,
                }
            })

        # 3. Question Bank
        for chapter_id, q_list in QUESTION_BANK.items():
            for idx, q_tuple in enumerate(q_list):
                stage, prompt, options, answer, explanation = q_tuple
                q_id = f"{chapter_id}-{stage}-{idx+1}"
                self.index.append({
                    "id": q_id,
                    "type": "question",
                    "title": f"[{stage.upper()}] {prompt}",
                    "text": f"{prompt} options: {' '.join(options)} answer: {answer} explanation: {explanation} stage: {stage} chapter: {chapter_id}",
                    "chapter_id": chapter_id,
                    "concept_id": chapter_id,
                    "tags": ["question", stage, chapter_id],
                    "metadata": {
                        "stage": stage,
                        "prompt": prompt,
                        "options": options,
                        "expected_answer": answer,
                        "explanation": explanation
                    }
                })

        # 4. Misconceptions
        for misc in MISCONCEPTIONS_DATABASE:
            self.index.append({
                "id": f"misc-{misc['id']}",
                "type": "misconception",
                "title": f"Misconception: {misc['title']}",
                "text": f"{misc['title']} {misc['description']} {' '.join(misc['symptoms'])} remedy: {misc['remedy']} route: {misc['recommended_route']} concept: {misc['concept']}",
                "chapter_id": "rational-numbers" if "fraction" in misc["concept"] else misc["concept"],
                "concept_id": misc["concept"],
                "tags": ["misconception", "diagnostic-trap", misc["id"], misc["recommended_route"], misc["concept"]],
                "metadata": misc
            })

        # 5. Interventions & Pedagogical Strategies
        for key, details in INTERVENTION_LIBRARY.items():
            title, activity, duration, outcome, follow_up = details
            self.index.append({
                "id": f"intervention-{key}",
                "type": "intervention",
                "title": f"Intervention Pod: {title} ({duration})",
                "text": f"{title} {activity} duration: {duration} outcome: {outcome} follow_up: {follow_up} key: {key}",
                "chapter_id": "rational-numbers",
                "concept_id": "equivalent-fractions",
                "tags": ["intervention", "pedagogy", key, "teacher-compiler"],
                "metadata": {
                    "key": key,
                    "activity": activity,
                    "duration": duration,
                    "outcome": outcome,
                    "follow_up": follow_up
                }
            })

    def search(
        self,
        query: str,
        entity_type: str | None = None,
        chapter_id: str | None = None,
        limit: int = 15
    ) -> list[SearchResult]:
        """Performs lexical and semantic keyword matching with score ranking."""
        raw_query = (query or "").strip().lower()
        if not raw_query:
            return []

        # Tokenize and extract query terms
        query_terms = [t for t in re.split(r"[^\w\d\-]+", raw_query) if len(t) > 1]
        if not query_terms:
            query_terms = [raw_query]

        results: list[SearchResult] = []

        for doc in self.index:
            # Apply filters
            if entity_type and entity_type != "all" and doc["type"] != entity_type:
                continue
            if chapter_id and chapter_id != "all" and doc["chapter_id"] != chapter_id:
                continue

            doc_text = doc["text"].lower()
            doc_title = doc["title"].lower()
            doc_tags = [t.lower() for t in doc["tags"]]

            score = 0.0

            # 1. Exact phrase match boost
            if raw_query in doc_title:
                score += 15.0
            elif raw_query in doc_text:
                score += 8.0

            # 2. Individual term matching
            matched_terms = 0
            for term in query_terms:
                term_matched = False
                if term in doc_title:
                    score += 5.0
                    term_matched = True
                if any(term in tag for tag in doc_tags):
                    score += 3.5
                    term_matched = True
                if term in doc_text:
                    score += 1.5
                    term_matched = True
                if term_matched:
                    matched_terms += 1

            if matched_terms == 0 and score == 0.0:
                continue

            # Term coverage bonus
            coverage_ratio = matched_terms / len(query_terms)
            score *= (0.5 + 0.5 * coverage_ratio)

            # Generate highlight snippet
            snippet = self._generate_snippet(doc["text"], query_terms)

            results.append(
                SearchResult(
                    id=doc["id"],
                    type=doc["type"],
                    title=doc["title"],
                    snippet=snippet,
                    relevance_score=round(score, 2),
                    chapter_id=doc.get("chapter_id"),
                    concept_id=doc.get("concept_id"),
                    tags=doc.get("tags", []),
                    metadata=doc.get("metadata", {})
                )
            )

        # Sort descending by score
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results[:limit]

    def _generate_snippet(self, text: str, query_terms: list[str], max_len: int = 160) -> str:
        """Extracts contextual text snippet around first matching term."""
        lowered = text.lower()
        earliest_idx = -1
        for term in query_terms:
            pos = lowered.find(term)
            if pos != -1 and (earliest_idx == -1 or pos < earliest_idx):
                earliest_idx = pos

        if earliest_idx == -1:
            return text[:max_len] + ("..." if len(text) > max_len else "")

        start = max(0, earliest_idx - 40)
        end = min(len(text), earliest_idx + max_len - 40)
        prefix = "..." if start > 0 else ""
        suffix = "..." if end < len(text) else ""
        return prefix + text[start:end].strip() + suffix

    def get_suggestions(self, prefix: str = "", limit: int = 6) -> list[str]:
        """Provides instant query autocompletion suggestions."""
        curated_suggestions = [
            "Equivalent fractions",
            "Denominator magnitude misconception",
            "Linear equations in one variable",
            "Solve 3x + 5 = 20",
            "Squares and square roots",
            "Understanding quadrilaterals",
            "Additive equivalence bias",
            "Comparing quantities discount",
            "Prerequisite concept DAG",
            "Visual fraction bar pod",
            "Recipe scaling transfer",
            "Data handling probability"
        ]
        p = prefix.strip().lower()
        if not p:
            return curated_suggestions[:limit]
        matches = [s for s in curated_suggestions if p in s.lower()]
        return matches[:limit] or [f"{prefix} concept", f"{prefix} questions", f"{prefix} misconception"]


# Global engine singleton
search_engine = SearchEngine()

