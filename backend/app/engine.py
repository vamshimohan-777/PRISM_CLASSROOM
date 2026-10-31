"""Deterministic learning rules for the equivalent-fractions prototype.

Every value produced here is a rubric score derived from observable answers,
not a calibrated probability. The rules are ordered and the first match wins,
so any recommendation can be traced back to a single rule and the evidence
that triggered it. See docs/rules-engine.md for the full decision table.
"""

from __future__ import annotations

from dataclasses import dataclass

# Concept -> prerequisite concepts. Must stay a DAG (checked at start-up).
CONCEPT_GRAPH: dict[str, list[str]] = {
    "fraction-parts": [],
    "fraction-magnitude": ["fraction-parts"],
    "simplification": ["fraction-parts"],
    "equivalent-fractions": ["fraction-magnitude", "simplification"],
}

# Each tagged wrong answer points at the concept it gives evidence about and
# whether it looks like a conceptual misunderstanding or a procedural slip.
ERROR_TAGS: dict[str, tuple[str, str]] = {
    "fraction-parts-gap": ("fraction-parts", "conceptual"),
    "denominator-magnitude": ("fraction-magnitude", "conceptual"),
    "additive-equivalence": ("equivalent-fractions", "conceptual"),
    "sign-error": ("simplification", "procedural"),
    "incomplete-simplification": ("simplification", "procedural"),
    "unequal-operations": ("equivalent-fractions", "procedural"),
}

# Concepts with no prerequisites of their own; an error here means later
# work may be built on an insecure foundation.
FOUNDATIONAL_CONCEPTS = {node for node, parents in CONCEPT_GRAPH.items() if not parents}

TEST_STAGE_WEIGHT = 1.4  # transfer/test answers count more than practice
PRIOR_WEIGHT = 0.25  # how much the previous estimate carries over
MASTERY_FLOOR, MASTERY_CEILING = 0.05, 0.95
MIN_PATTERN_REPEATS = 2  # one wrong answer never establishes a pattern
PATTERN_SHARE = 0.5  # share of all responses the pattern must cover
PREREQUISITE_SECURE = 0.65
EXTENSION_MASTERY = 0.72
TEST_READY_MASTERY = 0.68
TEST_READY_EVIDENCE = 3


def validate_graph(graph: dict[str, list[str]] = CONCEPT_GRAPH) -> bool:
    """Raise ValueError if the prerequisite graph has unknown nodes or a cycle."""
    for node, parents in graph.items():
        for parent in parents:
            if parent not in graph:
                raise ValueError(f"Unknown prerequisite '{parent}' for '{node}'")

    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(node: str) -> None:
        if node in visiting:
            raise ValueError("Prerequisite graph has a cycle")
        if node in visited:
            return
        visiting.add(node)
        for parent in graph[node]:
            walk(parent)
        visiting.remove(node)
        visited.add(node)

    for key in graph:
        walk(key)
    return True


@dataclass
class RuleResult:
    mastery: float
    evidence_count: int
    misconception: str | None
    misconception_confidence: float
    prerequisite_status: str
    recommendation: str
    reason: str


def _weight(attempt: dict) -> float:
    return TEST_STAGE_WEIGHT if attempt.get("stage") == "test" else 1.0


def _prerequisite_status(error_tags: list[str], override: float | None) -> str:
    if override is not None:
        return "secure" if override >= PREREQUISITE_SECURE else "needs-check"
    foundational_errors = [t for t in error_tags if ERROR_TAGS.get(t, ("", ""))[0] in FOUNDATIONAL_CONCEPTS]
    return "needs-check" if foundational_errors else "secure"


def update_profile(previous: float, attempts: list[dict], prerequisite_mastery: float | None = None) -> RuleResult:
    """Recompute a learner's profile for one concept from their attempts.

    ``attempts`` are dicts with ``correct`` and optionally ``stage``,
    ``transfer`` and ``misconception`` (the tag mapped from the chosen wrong
    answer). ``prerequisite_mastery`` overrides the evidence-based
    prerequisite check when a separate estimate is available.
    """
    count = len(attempts)
    if not count:
        return RuleResult(previous, 0, None, 0, "unknown", "diagnostic", "No response evidence yet.")

    correct = sum(bool(a["correct"]) for a in attempts)
    weighted = sum(_weight(a) * bool(a["correct"]) for a in attempts)
    total_weight = sum(_weight(a) for a in attempts)
    raw = PRIOR_WEIGHT * previous + (1 - PRIOR_WEIGHT) * weighted / total_weight
    mastery = round(max(MASTERY_FLOOR, min(MASTERY_CEILING, raw)), 2)

    tags = [a["misconception"] for a in attempts if not a["correct"] and a.get("misconception")]
    conceptual = [t for t in tags if ERROR_TAGS.get(t, ("", "conceptual"))[1] == "conceptual"]
    procedural = [t for t in tags if t not in conceptual]

    leading = max(set(conceptual), key=conceptual.count) if conceptual else None
    leading_count = conceptual.count(leading) if leading else 0
    confidence = round(leading_count / count, 2) if leading_count >= MIN_PATTERN_REPEATS else 0.0

    prerequisite = _prerequisite_status(tags, prerequisite_mastery)
    transfer = [a for a in attempts if a.get("transfer")]

    # Rule 1: insecure foundation and little correct evidence.
    if prerequisite == "needs-check" and correct <= 1:
        return RuleResult(
            mastery,
            count,
            leading if confidence else None,
            confidence,
            prerequisite,
            "foundation",
            "Foundational fraction-part evidence should be checked before equivalence practice.",
        )

    # Rule 2: the same conceptual error appears repeatedly.
    if leading and confidence >= PATTERN_SHARE:
        return RuleResult(
            mastery,
            count,
            leading,
            confidence,
            prerequisite,
            "visual-support",
            f"{leading_count} responses match a possible pattern; use a visual check before concluding.",
        )

    # Rule 3: every error is procedural and there are at least two of them.
    if len(procedural) >= MIN_PATTERN_REPEATS and not conceptual:
        return RuleResult(
            mastery,
            count,
            None,
            0,
            prerequisite,
            "guided-practice",
            "Concept items are answered correctly; errors are procedural slips, so scaffold the calculation steps.",
        )

    # Rule 4: errors that do not agree with each other.
    if count >= 2 and correct != count and leading_count < MIN_PATTERN_REPEATS:
        return RuleResult(
            mastery,
            count,
            None,
            0,
            prerequisite,
            "follow-up",
            "Evidence is mixed; ask a discriminating follow-up or review with the teacher.",
        )

    # Rule 5: the most recent transfer item was answered independently and correctly.
    if transfer and transfer[-1]["correct"] and mastery >= EXTENSION_MASTERY:
        return RuleResult(
            mastery, count, None, 0, "secure", "extension", "Independent transfer evidence supports an extension task."
        )

    # Rule 6: enough correct practice to justify a transfer check.
    if mastery >= TEST_READY_MASTERY and count >= TEST_READY_EVIDENCE:
        return RuleResult(
            mastery,
            count,
            None,
            0,
            prerequisite,
            "test",
            "Practice evidence supports independent transfer verification.",
        )

    # Default: keep gathering evidence with guided practice.
    return RuleResult(
        mastery,
        count,
        None,
        0,
        prerequisite,
        "guided-practice",
        "More guided equivalence practice will provide useful evidence.",
    )


INTERVENTION_LIBRARY = {
    "foundation": (
        "Check fraction parts",
        "Use paper strips to name numerator and denominator, then simplify two shaded bars.",
        "12 min",
        "Student identifies equal-sized parts before comparing fractions.",
        "Two prerequisite check questions",
    ),
    "visual-support": (
        "Compare with fraction bars",
        "Place fraction bars with the same whole side by side; ask learners to justify which is larger.",
        "10 min",
        "Student connects denominator size to equal parts rather than magnitude.",
        "Discriminating magnitude question",
    ),
    "guided-practice": (
        "Build equivalent pairs",
        "Pairs multiply numerator and denominator by the same number using a multiplication grid.",
        "12 min",
        "Student generates and simplifies equivalent fractions accurately.",
        "Independent equivalence item",
    ),
    "extension": (
        "Recipe scaling challenge",
        "Scale a recipe for a different number of people and justify the equivalent fraction used.",
        "15 min",
        "Student applies equivalence in a novel context.",
        "Transfer application question",
    ),
    "follow-up": (
        "Teacher conference",
        "Ask one contrast question and listen to the explanation before selecting a route.",
        "5 min",
        "Teacher gathers enough evidence to choose an appropriate next step.",
        "Teacher-selected follow-up",
    ),
    "test": (
        "Independent transfer check",
        "Learners attempt one unfamiliar equivalence problem without hints.",
        "8 min",
        "Student shows equivalence without scaffolding.",
        "Transfer application question",
    ),
    "diagnostic": (
        "Start the diagnostic",
        "Learners complete the short diagnostic so PRISM has evidence to work from.",
        "8 min",
        "Each learner has at least three pieces of evidence.",
        "Diagnostic set",
    ),
}


def compile_groups(profiles) -> list[dict]:
    """Group learners by recommended route and attach a draft activity.

    Grouping uses only the route, never names or past labels. Every plan is
    created as a proposal for the teacher to approve, edit or reject.
    """
    groups: dict[str, list] = {}
    for profile in profiles:
        groups.setdefault(profile.recommendation, []).append(profile)

    plans = []
    for key, members in groups.items():
        title, activity, duration, outcome, follow_up = INTERVENTION_LIBRARY[key]
        confidence = "review" if key == "follow-up" else ("high" if len(members) >= 2 else "moderate")
        plans.append(
            {
                "group_key": key,
                "students": [m.code for m in members],
                "barrier": title,
                "evidence": f"{len(members)} synthetic learner profile(s) currently route to {key.replace('-', ' ')}.",
                "confidence": confidence,
                "activity": activity,
                "duration": duration,
                "outcome": outcome,
                "follow_up": follow_up,
            }
        )
    return plans
