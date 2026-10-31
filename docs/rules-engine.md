# Rules engine

Source: [`backend/app/engine.py`](../backend/app/engine.py)

PRISM does not train a model. The prototype has no validated student-response
data, so a learned model could not be trusted or checked. Instead, a short,
ordered list of rules turns observable answers into a route. Every route
includes the rule that produced it and a plain-language reason. The teacher
can see both and override either one.

## Inputs

Each answer becomes one piece of evidence:

| Field | Meaning |
| --- | --- |
| `correct` | Whether the answer matched the expected answer |
| `stage` | `diagnostic`, `practice` or `test` |
| `transfer` | `true` for the independent transfer question |
| `misconception` | Tag attached to the chosen wrong option, if any (from the question's `misconception_map`) |

## Concept map

```
fraction-parts ──► fraction-magnitude ──┐
      │                                 ├──► equivalent-fractions
      └──────────► simplification ──────┘
```

`validate_graph()` runs at start-up and refuses to start if the map has an
unknown node or a cycle.

## Error tags

Each tag points at the concept it gives evidence about, and is classed as
either a conceptual misunderstanding or a procedural slip.

| Tag | Concept | Kind | Example wrong answer |
| --- | --- | --- | --- |
| `fraction-parts-gap` | fraction-parts | conceptual | 3 of 6 equal parts named as 1/3 |
| `denominator-magnitude` | fraction-magnitude | conceptual | 1/8 chosen as greater than 1/3 |
| `additive-equivalence` | equivalent-fractions | conceptual | 3/5 = 8/10 ("add 5 to both") |
| `sign-error` | simplification | procedural | −18/24 written as 3/4 |
| `incomplete-simplification` | simplification | procedural | −18/24 written as −9/12 |
| `unequal-operations` | equivalent-fractions | procedural | 3/5 = 5/10 |

## Mastery estimate

```
mastery = clamp(0.25 × previous + 0.75 × weighted_correct_share, 0.05, 0.95)
```

Test-stage answers carry weight 1.4, all others 1.0. The result is a rubric
score for display and thresholds. It is not a probability.

## Decision table

Rules are checked in order, and the first match wins.

| # | Rule | Condition | Route |
| --- | --- | --- | --- |
| 0 | No evidence | no answers yet | `diagnostic` |
| 1 | Insecure foundation | an error tagged on a foundational concept **and** at most one correct answer | `foundation` |
| 2 | Repeated conceptual pattern | the same conceptual tag appears at least twice **and** covers at least half of all answers | `visual-support` |
| 3 | Procedural slips only | at least two tagged errors, all procedural | `guided-practice` |
| 4 | Conflicting evidence | some answers wrong, but no tag repeats | `follow-up` (teacher review) |
| 5 | Transfer success | latest transfer answer correct **and** mastery ≥ 0.72 | `extension` |
| 6 | Ready for transfer | mastery ≥ 0.68 with at least three answers | `test` |
| 7 | Default | anything else | `guided-practice` |

All thresholds are named constants at the top of `engine.py`.

## Safeguards built into the rules

- **One wrong answer never creates a label.** A tag must repeat
  (`MIN_PATTERN_REPEATS = 2`) before it is reported as a possible
  misconception.
- **Conflicting evidence goes to the teacher.** Rule 4 sends the learner to a
  teacher conference instead of guessing.
- **Slips are not misconceptions.** Rule 3 sends procedural errors to guided
  practice and reports no misconception.
- **Estimates are per concept and change with new evidence.** Nothing is
  stored as a permanent label, and every new answer recomputes the profile.

## Worked traces for the four simulated learners

These are the seeded answers in `backend/app/seed.py`. The stored profiles are
produced by running these answers through the engine, not typed in by hand.
`tests/test_prototype_evaluation.py` checks the result.

| Learner | Answers (✓ correct / ✗ tag) | Matching rule | Route |
| --- | --- | --- | --- |
| Aarav | ✓, ✗ `denominator-magnitude`, ✓, ✗ `denominator-magnitude` (transfer) | 2 | visual-support |
| Diya | ✗ `fraction-parts-gap`, ✗ (untagged), ✓ | 1 | foundation |
| Kabir | ✓, ✓, ✗ `incomplete-simplification`, ✗ `unequal-operations` | 3 | guided-practice |
| Meera | ✓, ✓, ✓, ✓, ✓ (transfer) | 5 | extension |
