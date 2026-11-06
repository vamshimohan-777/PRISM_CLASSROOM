"""Deterministic learning rules. Values are rubric scores, never probabilities.

All routing decisions in this module are rule-based and fully reproducible; no model is
consulted here. (The Answer Engine has a separate, optional LLM fallback that is off by
default and plays no part in routing.)
"""
from dataclasses import dataclass

CONCEPT_GRAPH = {
    "fraction-parts": [],
    "fraction-magnitude": ["fraction-parts"],
    "simplification": ["fraction-parts"],
    "equivalent-fractions": ["fraction-magnitude", "simplification"],
}

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

def prerequisite_mastery_from(progress_by_concept, concept_id, graph=CONCEPT_GRAPH):
    """Weakest observed prerequisite mastery, or None when no prerequisite has evidence.

    `progress_by_concept` maps concept_id -> (mastery, evidence_count). Only
    prerequisites that the learner has actually attempted count as evidence;
    an unattempted prerequisite is unknown, not weak.
    """
    observed = [
        mastery
        for parent in ancestors(concept_id, graph)
        for mastery, evidence_count in [progress_by_concept.get(parent, (0.0, 0))]
        if evidence_count > 0
    ]
    return min(observed) if observed else None

@dataclass
class RuleResult:
    mastery: float
    evidence_count: int
    misconception: str | None
    misconception_confidence: float
    prerequisite_status: str
    recommendation: str
    reason: str

def update_profile(previous, attempts, prerequisite_mastery=None):
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
    leading = max(set(tags), key=tags.count) if tags else None
    leading_count = tags.count(leading) if leading else 0
    confidence = round(leading_count / count, 2) if leading_count >= 2 else 0.0
    if prerequisite_mastery is None:
        prerequisite = "unknown"
    elif prerequisite_mastery >= .65:
        prerequisite = "secure"
    else:
        prerequisite = "needs-check"
    if prerequisite == "needs-check" and correct <= 1:
        return RuleResult(mastery, count, leading if confidence else None, confidence, prerequisite, "foundation", f"Rule: weakest attempted prerequisite scores {prerequisite_mastery:.2f} (< 0.65 threshold) and only {correct}/{count} responses here are correct. Foundation scaffolding is prescribed before continuing this concept.")
    if leading and confidence >= .5:
        return RuleResult(mastery, count, leading, confidence, prerequisite, "visual-support", f"Rule: {leading_count}/{count} incorrect responses carry the '{leading}' error tag (≥50% threshold). Visual representation change is prescribed.")
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
        confidence = "review" if key == "follow-up" else ("high" if len(members) >= 2 else "moderate")
        plans.append({"group_key": key, "students": labels, "barrier": title, "evidence": f"{len(members)} learner profile(s) currently route to {key.replace('-', ' ')}.", "confidence": confidence, "activity": activity, "duration": duration, "outcome": outcome, "follow_up": follow_up})
    return plans

