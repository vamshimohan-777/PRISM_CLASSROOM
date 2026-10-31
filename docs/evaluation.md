# How the prototype is checked

Section 07 of the Decode submission lists five measures for the Prove round.
Each one has a matching test class in
[`backend/tests/test_prototype_evaluation.py`](../backend/tests/test_prototype_evaluation.py),
which runs against the real API through FastAPI's test client.

These tests check **software behaviour on simulated learners**. They make no
claim about diagnostic accuracy with real students or about learning gains.

| Measure (from the submission) | What we check | Test class |
| --- | --- | --- |
| Diagnostic consistency | Each seeded learner's stored route equals what the engine derives from their answers. Conflicting errors go to `follow-up`. A single wrong answer produces no label. | `TestDiagnosticConsistency` |
| Route appropriateness | The four archetypes receive four distinct routes: visual, foundation, guided and extension. Procedural slips are not reported as a misconception. | `TestRouteAppropriateness` |
| Transfer check | A correct answer to a new transfer problem adds evidence and raises the estimate. | `TestTransferCheck` |
| Teacher control | The teacher can edit, reject and reassign a plan, and the change shows on reload. Students cannot change plans. | `TestTeacherControl` |
| Practicality (offline path) | Replaying a queued answer with the same `submission_id` is accepted once and not double-counted. | `TestPracticality` |

The engine's unit tests in `tests/test_engine.py` cover each rule in isolation,
and `tests/test_api.py` covers authentication, the curriculum catalogue and
demo reset.

## Running

```bash
cd backend
pytest -q                 # 27 tests
cd ../frontend
npm test && npm run build
```

CI (`.github/workflows/ci.yml`) runs the same commands, plus `ruff`, on every
push and pull request.

## Manual check of the offline path

The automated tests cover the server side of offline sync. To check the
browser side:

1. Run a production build (`npm run build && npm run preview`), so the
   service worker is registered.
2. Sign in as a student and open a chapter.
3. In DevTools → Network, choose **Offline**, or use the **Online** pill in
   the top bar.
4. Answer a question. It is saved on the device and the top bar shows the
   queue count.
5. Reload the page. The app shell still loads from the cache.
6. Go back online and press **Sync**. The answer is sent once, and the teacher
   view shows the new evidence.

## Known limits

- One topic (equivalent fractions) has misconception-tagged questions. The
  other seven chapters have plain question sets with no tags.
- Thresholds were set by hand to separate the four archetypes. They need
  review against real classroom data before any use with students.
- The intervention plan is compiled once per classroom and then edited by the
  teacher. It is not automatically recompiled after every new answer.
