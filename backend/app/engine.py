"""Deterministic learning rules. Values are rubric scores, never probabilities.

All routing decisions in this module are rule-based and fully reproducible; no model is
consulted here. (The Answer Engine has a separate, optional LLM fallback that is off by
default and plays no part in routing.)
"""
from collections import Counter
from dataclasses import dataclass

from .catalog import CHAPTERS, misconception_route

# Every chapter depends on at least one prerequisite skill, and some chapters also
# depend on an earlier chapter. Each key lists what must be understood before it.
CONCEPT_GRAPH = {
    # Chapter 1: Rational Numbers
    "fraction-parts": [],
    "fraction-magnitude": ["fraction-parts"],
    "simplification": ["fraction-parts"],
    "equivalent-fractions": ["fraction-magnitude", "simplification"],
    # Chapter 2: Linear Equations
    "inverse-operations": [],
    "linear-equations": ["inverse-operations"],
    # Chapter 3: Understanding Quadrilaterals
    "triangle-angle-sum": [],
    "quadrilaterals": ["triangle-angle-sum"],
    # Chapter 4: Practical Geometry (constructing a shape needs its properties)
    "measuring-skills": [],
    "practical-geometry": ["measuring-skills", "quadrilaterals"],
    # Chapter 5: Data Handling (probability is written as a fraction)
    "reading-data": [],
    "data-handling": ["reading-data", "equivalent-fractions"],
    # Chapter 6: Squares and Square Roots
    "number-factors": [],
    "squares-roots": ["number-factors"],
    # Chapter 7: Cubes and Cube Roots (extends the factor-pair idea from squares)
    "repeated-multiplication": [],
    "cubes-roots": ["repeated-multiplication", "squares-roots"],
    # Chapter 8: Comparing Quantities (a percentage is a fraction out of 100)
    "percent-meaning": [],
    "comparing-quantities": ["percent-meaning", "equivalent-fractions"],
}

CHAPTER_CONCEPTS = {chapter["concept"] for chapter in CHAPTERS}
PREREQUISITE_SECURE_AT = 0.65

def validate_graph(graph=CONCEPT_GRAPH):
    for node, parents in graph.items():
        for parent in parents:
            if parent not in graph:
                raise ValueError(f"Unknown prerequisite '{parent}' for '{node}'")
    visiting, visited = set(), set()
    def walk(node):
        if node in visiting: raise ValueError("Prerequisite graph has a cycle")
        if node not in visited:
            visiting.add(node)
            for parent in graph[node]: walk(parent)
            visiting.remove(node); visited.add(node)
    for key in graph: walk(key)
    return True

def ancestors(concept_id, graph=CONCEPT_GRAPH):
    """All transitive prerequisites of a concept, nearest first.

    Concepts outside the graph (e.g. chapters with no modelled prerequisites)
    return an empty list, so prerequisite routing simply does not apply to them.
    """
    if concept_id not in graph:
        return []
    ordered, seen, frontier = [], {concept_id}, list(graph[concept_id])
    while frontier:
        node = frontier.pop(0)
        if node in seen:
            continue
        seen.add(node)
        ordered.append(node)
        frontier.extend(graph.get(node, []))
    return ordered

def dependants(concept_id, graph=CONCEPT_GRAPH):
    """Concepts that have `concept_id` as a transitive prerequisite, nearest first."""
    return sorted(
        (node for node in graph if concept_id in ancestors(node, graph)),
        key=lambda node: len(ancestors(node, graph)),
    )

def prerequisite_checks(concept_id, graph=CONCEPT_GRAPH):
    """Prerequisite skills a chapter should test itself, nearest first.

    The walk stops at other chapters. A chapter that depends on Chapter 1 uses the
    evidence Chapter 1 already holds, rather than asking all its questions again.
    """
    ordered, seen, frontier = [], {concept_id}, list(graph.get(concept_id, []))
    while frontier:
        node = frontier.pop(0)
        if node in seen or node in CHAPTER_CONCEPTS:
            continue
        seen.add(node)
        ordered.append(node)
        frontier.extend(graph.get(node, []))
    return ordered

def weakest_prerequisite(progress_by_concept, concept_id, graph=CONCEPT_GRAPH):
    """(concept, mastery) for the weakest attempted prerequisite, or None without evidence.

    `progress_by_concept` maps concept_id -> (mastery, evidence_count). Only
    prerequisites that the learner has actually attempted count as evidence;
    an unattempted prerequisite is unknown, not weak.
    """
    observed = [
        (progress_by_concept[parent][0], parent)
        for parent in ancestors(concept_id, graph)
        if progress_by_concept.get(parent, (0.0, 0))[1] > 0
    ]
    if not observed:
        return None
    mastery, concept = min(observed)
    return concept, mastery

def prerequisite_mastery_from(progress_by_concept, concept_id, graph=CONCEPT_GRAPH):
    """Weakest observed prerequisite mastery, or None when no prerequisite has evidence."""
    weakest = weakest_prerequisite(progress_by_concept, concept_id, graph)
    return weakest[1] if weakest else None

@dataclass
class RuleResult:
    mastery: float
    evidence_count: int
    misconception: str | None
    misconception_confidence: float
    prerequisite_status: str
    recommendation: str
    reason: str

def update_profile(previous, attempts, prerequisite_mastery=None, prerequisite_name=None):
    """Recompute profile from observable attempts; one error cannot establish a label."""
    count = len(attempts)
    if not count:
        return RuleResult(previous, 0, None, 0, "unknown", "diagnostic", "No response evidence yet.")
    correct = sum(a["correct"] for a in attempts)
    transfer = [a for a in attempts if a.get("transfer")]
    weighted = sum((1.4 if a.get("stage") == "test" else 1.0) * a["correct"] for a in attempts)
    total_weight = sum(1.4 if a.get("stage") == "test" else 1.0 for a in attempts)
    mastery = round(max(0.05, min(0.95, 0.25 * previous + 0.75 * weighted / total_weight)), 2)
    tags = [a.get("misconception") for a in attempts if not a["correct"] and a.get("misconception")]
    # A tie between error patterns is ambiguous evidence, so no tag leads and the
    # learner routes to a teacher conversation. Breaking the tie by iterating a set
    # would make the label depend on the process's string hash seed.
    counts = Counter(tags)
    top = max(counts.values(), default=0)
    leaders = [tag for tag, seen in counts.items() if seen == top]
    leading = leaders[0] if len(leaders) == 1 else None
    leading_count = top if leading else 0
    confidence = round(leading_count / count, 2) if leading_count >= 2 else 0.0
    if prerequisite_mastery is None:
        prerequisite = "unknown"
    elif prerequisite_mastery >= PREREQUISITE_SECURE_AT:
        prerequisite = "secure"
    else:
        prerequisite = "needs-check"
    if prerequisite == "needs-check" and correct <= 1:
        return RuleResult(mastery, count, leading if confidence else None, confidence, prerequisite, "foundation", f"Rule: weakest attempted prerequisite{f' ({prerequisite_name})' if prerequisite_name else ''} scores {prerequisite_mastery:.2f} (< 0.65 threshold) and only {correct}/{count} responses here are correct. Foundation scaffolding is prescribed before continuing this concept.")
    if leading and confidence >= .5:
        route = misconception_route(leading)
        return RuleResult(mastery, count, leading, confidence, prerequisite, route, f"Rule: {leading_count}/{count} responses carry the '{leading}' error tag (≥50% threshold). This misconception's prescribed route is {route.replace('-', ' ')}.")
    if count >= 2 and correct != count and leading_count < 2:
        return RuleResult(mastery, count, None, 0, prerequisite, "follow-up", "Evidence is mixed and no single error pattern dominates. Teacher should ask one discriminating follow-up question before choosing a route.")
    if transfer and transfer[-1]["correct"] and mastery >= .72:
        # An unassisted transfer item passed at high mastery is itself sufficient
        # evidence that the prerequisites hold, whatever the DAG has observed.
        return RuleResult(mastery, count, None, 0, "secure", "extension", "Most-recent transfer item answered correctly and rubric mastery ≥ 72%. Independent extension challenge is prescribed.")
    if mastery >= .68 and count >= 3:
        return RuleResult(mastery, count, None, 0, prerequisite, "test", "Mastery ≥ 68% across ≥3 items. Progressing to independent transfer verification stage.")
    return RuleResult(mastery, count, None, 0, prerequisite, "guided-practice", "Insufficient pattern evidence for labelling; scaffolded guided practice will yield clearer diagnostic signal.")

INTERVENTION_LIBRARY = {
    "foundation": ("Check fraction parts", "Use paper strips to name numerator and denominator, then simplify two shaded bars.", "12 min", "Student identifies equal-sized parts before comparing fractions.", "Two prerequisite check questions"),
    "visual-support": ("Compare with fraction bars", "Place fraction bars with the same whole side by side; ask learners to justify which is larger.", "10 min", "Student connects denominator size to equal parts rather than magnitude.", "Discriminating magnitude question"),
    "guided-practice": ("Build equivalent pairs", "Pairs multiply numerator and denominator by the same number using a multiplication grid.", "12 min", "Student generates and simplifies equivalent fractions accurately.", "Independent equivalence item"),
    "extension": ("Recipe scaling challenge", "Scale a recipe for a different number of people and justify the equivalent fraction used.", "15 min", "Student applies equivalence in a novel context.", "Transfer application question"),
    "test": ("Ready for a transfer check", "Give one unscaffolded problem in a new context and ask the learner to explain the method.", "5 min", "Learner applies the concept independently in an unfamiliar setting.", "Transfer application question"),
    "follow-up": ("Teacher conference", "Ask one contrast question and listen to the explanation before selecting a route.", "5 min", "Teacher gathers enough evidence to choose an appropriate next step.", "Teacher-selected follow-up"),
}

def compile_groups(profiles):
    groups = {}
    for p in profiles:
        key = p.recommendation
        # Skip profiles that haven't gathered enough evidence for grouping yet
        if key not in INTERVENTION_LIBRARY:
            continue
        groups.setdefault(key, []).append(p)
    plans = []
    for key, members in groups.items():
        title, activity, duration, outcome, follow_up = INTERVENTION_LIBRARY[key]
        labels = [m.code for m in members]
        # Evidence depth, not a probability: how many responses the thinnest profile
        # in this pod rests on. Pod size says nothing about how sure the rule is.
        thinnest = min(getattr(m, "evidence_count", 0) for m in members)
        confidence = "review" if key == "follow-up" else ("high" if thinnest >= 4 else "moderate")
        plans.append({"group_key": key, "students": labels, "barrier": title, "evidence": f"{len(members)} learner profile(s) currently route to {key.replace('-', ' ')}; the thinnest profile rests on {thinnest} response(s).", "confidence": confidence, "activity": activity, "duration": duration, "outcome": outcome, "follow_up": follow_up})
    return plans

