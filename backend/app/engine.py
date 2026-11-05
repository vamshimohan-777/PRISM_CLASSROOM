"""Deterministic learning rules. Values are rubric scores, never probabilities.

All routing decisions are rule-based and fully reproducible. No generative AI is used.
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

@dataclass
class RuleResult:
    mastery: float
    evidence_count: int
    misconception: str | None
    misconception_confidence: float
    prerequisite_status: str
    recommendation: str
    reason: str

def update_profile(previous, attempts, prerequisite_mastery=0.75):
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
    prerequisite = "secure" if prerequisite_mastery >= .65 else "needs-check"
    if prerequisite == "needs-check" and correct <= 1:
        return RuleResult(mastery, count, leading if confidence else None, confidence, prerequisite, "foundation", "Prerequisite fraction-part knowledge appears incomplete; foundation scaffolding is prescribed before equivalence practice.")
    if leading and confidence >= .5:
        return RuleResult(mastery, count, leading, confidence, prerequisite, "visual-support", f"Rule: {leading_count}/{count} incorrect responses carry the '{leading}' error tag (≥50% threshold). Visual representation change is prescribed.")
    if count >= 2 and correct != count and leading_count < 2:
        return RuleResult(mastery, count, None, 0, prerequisite, "follow-up", "Evidence is mixed and no single error pattern dominates. Teacher should ask one discriminating follow-up question before choosing a route.")
    if transfer and transfer[-1]["correct"] and mastery >= .72:
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

