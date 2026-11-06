# PRISM Classroom: Technical Interview Guide

**Round:** 10-minute Google Meet, questions on architecture, implementation, technologies, data handling and decisions.

**How to answer:** decision, then why, then the trade-off, then where to see it in the code. Keep each answer under 40 seconds and offer to show the code. Name a limit before you are asked about it.

## Contents
1. [Opening](#1-opening-40-seconds)
2. [Live demo](#2-live-demo-90-seconds)
3. [Every feature](#3-every-feature)
4. [Architecture and where each pattern is used](#4-architecture-and-where-each-pattern-is-used)
5. [Algorithms](#5-algorithms)
6. [Data storage](#6-data-storage)
7. [Translation](#7-translation)
8. [Security](#8-security)
9. [Performance](#9-performance)
10. [Comparison with other platforms](#10-comparison-with-other-platforms)
11. [Decisions and challenges](#11-decisions-and-challenges)
12. [Known limits](#12-known-limits)
13. [Words to avoid](#13-words-to-avoid)
14. [Rapid-fire niche answers](#14-rapid-fire-niche-answers)
15. [Day-of checklist](#15-day-of-checklist)

---

## 1. Opening (40 seconds)

> "PRISM is a teacher-in-the-loop diagnostic tool for CBSE Class 8 maths. Wrong answers are tagged with the specific error they reveal. A deterministic rules engine turns the attempt log into a mastery score, a misconception label and a route, then proposes small groups, chapter by chapter, that the teacher can approve, edit or reject. It is FastAPI, React and SQLite in one container, with no model in the routing path. Shall I show it live, or start with the architecture?"

## 2. Live demo (90 seconds)

Rehearse this once. The sequence was checked in a browser against a fresh database.

1. **Create a student** with class code `8A-CBSE`, then open Chapter 1.
2. **Q1, answer `2/4` (correct).** The note says there is not enough pattern evidence yet.
3. **Q2 "Which is greater?", answer `1/8`.** One error creates no label. The route becomes teacher follow-up.
4. **Click stage 3 in the sidebar and answer `3/6`.** This is the second error with the same tag, so the label appears and the route becomes visual support.
5. **Click stage 2.** The fraction-bar workbench opens because of the route.
6. **Press the Online pill to go offline and answer a question.** The answer is queued. Press the pill again and it syncs by itself.
7. **Switch to Ms. Ananya with the demo account menu and press Recompile.** The student appears by name in a pod. Click the name to open the evidence record.
8. **Approve a pod, answer as another student, then press Recompile.** The approved pod stays as it was and shows "consider adding".
9. **Press हिंदी.** The whole workspace changes, and the choice survives a reload.

If asked for retry safety, resend one `submission_id` in `/docs`. It returns `duplicate: true` and scores nothing.

## 3. Every feature

### Novel features: lead with these

| Feature | What it does | Where |
|---|---|---|
| Misconception tagging | Each wrong option can name the error it reveals. Options with no clear diagnosis stay untagged. | `backend/app/catalog.py`, `seed.py` |
| Single-error safeguard | One error can never create a label. A label needs at least 2 matching tags and at least 50% of the learner's responses. | `engine.update_profile` |
| Tie goes to the teacher | Two equally common error patterns count as ambiguous, so the route is teacher follow-up rather than a guess. | `engine.update_profile` |
| Route per misconception | Each of the 28 misconceptions names its own route, such as visual support or guided practice. | `catalog.MISCONCEPTIONS_DATABASE` |
| Prerequisite routing in all 8 chapters | Each chapter checks its own prerequisite skills, and some build on earlier chapters. The weakest attempted prerequisite can trigger the foundation route and is named to the teacher. An unattempted one counts as unknown, not weak. | `engine.CONCEPT_GRAPH`, `weakest_prerequisite`, `scoring.prerequisite_gap` |
| Teacher Intervention Compiler | Groups learners by route, per chapter, with an activity, duration and target outcome. | `backend/app/compiler.py` |
| Teacher authority | Approve, edit or dismiss a pod. Recompile refreshes only undecided pods and shows new evidence as a suggestion. | `compiler.recompile_classroom` |
| Evidence record | Every label traces to question, chosen option, expected answer and error pattern, across chapters. | `main.teacher_student_detail` |
| Derived profiles | No score is stored by hand. Profiles, including demo ones, are recomputed from attempts. | `backend/app/scoring.py` |
| Offline-safe answers | Answers queue per account and sync on reconnect. Retries cannot score twice. | `App.tsx`, `main.record_attempt`, `models.py` |
| Three-language workspace | English, Hindi and Telugu through written string tables, with tests that fail on missing translations. | `translations.ts`, `localization.ts`, `enginesText.ts`, `teacherText.ts` |

### Student side
- 8 chapters and 58 questions, 9 of them prerequisite checks, in three stages: Quick Diagnostic, Targeted Practice, Transfer Verification.
- Four interactive tools for fractions: fraction-bar comparator, equal-parts strips, multiplier grid and recipe-scaling lab. They appear only in Chapter 1.
- Other chapters show the route, the named error and a suggested remedy in place of fraction tools.
- Mastery display, a plain-language reason after each answer, and a join-class flow.

### Teacher side
- Class metrics, evidence list, chapter filter on pods, and a 45-minute pacing view.
- Edit dialog for activity, 5 to 20 minute duration, outcome, members and notes.
- Printable briefing, labelled as a school planning document and not a CBSE form.
- Class code enrolment.

### Engines Studio: public, no login
- **Search:** weighted keyword search over 108 documents: chapters, concepts, questions, misconceptions and interventions.
- **Answer:** rule-based solvers for linear equations, fractions, roots, percentages, quadrilaterals and the mean, each with steps and a check.
- **Generative:** randomised templates for questions in all 8 chapters, remediation guides for all 28 misconceptions, 45-minute lesson plans and Indian-context transfer tasks.

### Discoverability
Real URLs for each page, per-route metadata, JSON-LD, `sitemap.xml`, `robots.txt`, `llms.txt`, and `<noscript>` content for crawlers that do not run JavaScript.

## 4. Architecture and where each pattern is used

**Overall:** a modular monolith in one container, with a React single-page app talking to a REST API over a layered backend.

```
React SPA (Vite build)
   |  REST / JSON, same origin
FastAPI routes ............ main.py        validation, auth, HTTP
   |
Application services ...... scoring.py     re-derive profiles from attempts
                            compiler.py    build and reconcile pods
   |
Pure domain rules ......... engine.py      DAG, mastery, routing (no database)
Reference data ............ catalog.py     chapters, questions, misconceptions
   |
SQLAlchemy ORM ............ models.py      SQLite by default, Postgres by config
```

| Pattern | Where | Why |
|---|---|---|
| Modular monolith, single container | `Dockerfile`, `main.py` static serving | One deploy, no CORS, and enough for one school. |
| Layered architecture | `main` to `scoring` and `compiler` to `engine` | Each layer has one reason to change. |
| Functional core, imperative shell | `engine.py` has no database or HTTP imports | Rules can be tested without a server. |
| Rule-based expert system | `engine.update_profile` | First matching rule wins, so each decision has a stated reason. |
| Directed acyclic graph | `engine.CONCEPT_GRAPH`, `validate_graph`, `ancestors`, `dependants` | Models prerequisites. The app refuses to boot on a cycle. |
| Attempt log as source of truth, with a derived read model | `attempts` table, `scoring.recompute_concept`, `learner_progress` | A rule change is a replay, not a data migration. |
| Idempotency key | `submission_id`, `UniqueConstraint`, `IntegrityError` handling | Retries are safe at the database level. |
| Outbox-style client queue | `App.tsx` `syncOfflineQueue` | At-least-once delivery plus idempotency gives one scored result. |
| Read-through cache | `App.tsx` `remember` and `recall` | Activities already seen still open with no connection. |
| Tenant scoping by classroom | `classroom_id` checks in `main.py` and `compiler.py` | Teachers see only their own class. |
| Single-source reference data | `catalog.py` used by the engine, search and generator | Prevents the tables drifting apart. |
| In-memory singleton index | `search_engine = SearchEngine()` | Reference data does not change at runtime. |
| Adapter-style fallback chain | `AnswerEngine.solve` tries each solver in order | Rule solvers answer first. The LLM is last and optional. |
| Feature flag | `config.demo_mode` | One switch closes demo-only paths. |

**Attempt flow:** the client creates a UUID and posts it. The server checks for a duplicate, grades on the server, inserts the attempt, re-derives that concept and its dependants, commits, and returns the profile and reason.

**Teacher flow:** the workspace loads learners in bulk, picks each learner's most recent chapter as their focus, and returns stored plans with the engine's latest suggested changes.

## 5. Algorithms

### Mastery
```
mastery = clamp(0.05, 0.95, 0.25 x 0.35 + 0.75 x weighted accuracy), rounded to 2 places
weighted accuracy = sum(weight x correct) / sum(weight), where test items weigh 1.4 and others 1.0
```
- It is a weighted average with a starting prior. **It is not an EMA.**
- The practical range is 0.09 to 0.84, so the clamps never fire with the 0.35 prior.
- It ignores order: five wrong then five right scores 0.46, the same as the reverse. This is its main weakness. The next step is recency weighting or Bayesian Knowledge Tracing once real data exists.

### Routing: first match wins
| # | Condition | Route |
|---|---|---|
| 1 | Weakest attempted prerequisite below 0.65, and at most 1 correct here | Foundation |
| 2 | One leading tag, at least 2 occurrences, at least 50% of responses | That misconception's own route |
| 3 | At least 2 responses, some wrong, no repeated leading tag | Teacher follow-up |
| 4 | Latest transfer item correct and mastery at least 0.72 | Extension |
| 5 | Mastery at least 0.68 with at least 3 responses | Transfer check |
| 6 | Otherwise | Guided practice |

The thresholds are hand-set judgement calls, not fitted values. A classroom pilot would calibrate them.

### Prerequisite graph
18 nodes: 8 chapters and 10 prerequisite skills, all with at least one question. It lives in `engine.CONCEPT_GRAPH`, and a depth-first walk validates it at startup.

| Chapter | Skills it checks | Earlier chapter it builds on |
|---|---|---|
| 1 Rational Numbers | Parts of a fraction, comparing sizes, simplifying | None |
| 2 Linear Equations | Undoing an operation | None |
| 3 Quadrilaterals | Angle sum of a triangle | None |
| 4 Practical Geometry | Measuring with a ruler | Chapter 3 |
| 5 Data Handling | Reading a data list | Chapter 1 |
| 6 Squares and Roots | Prime factorisation | None |
| 7 Cubes and Roots | Repeated multiplication | Chapter 6 |
| 8 Comparing Quantities | Meaning of percent | Chapter 1 |

- **Serving:** a chapter asks about its own skills, after its chapter questions. It does not re-ask another chapter's questions; it reuses that evidence.
- **Propagation:** a new answer on a prerequisite re-derives everything that depends on it. A weak Chapter 1 can move a Chapter 8 student to foundation without a new Chapter 8 answer.
- **Order:** sorting by ancestor count is a valid topological order, because a concept's ancestors are a strict subset of its dependant's.
- **Basis:** the links are our judgement of how the topics build on each other. They are not validated by data or a subject expert.

### Pod evidence level
"Strong" means the thinnest profile in the pod rests on at least 4 responses. Otherwise it shows "Building". Follow-up pods show "Needs teacher review". It measures evidence depth and is not a probability.

### Search scoring
Exact phrase in title +15, or in text +8. Each term: title +5, tag +3.5, text +1.5. The total is multiplied by `0.5 + 0.5 x term coverage`. It uses substring matching with a linear scan of 94 documents, which is simple and fast at this size. A real corpus would need an inverted index and BM25.

### Linear solver
A recursive-descent parser reduces each side to `coefficient x variable + constant` using exact `Fraction` arithmetic. It handles brackets, fractions, negatives and a variable on both sides. It reports "No solution" or "Every value" when the coefficient cancels. It substitutes the answer back before returning it, so the check is really computed.

## 6. Data storage

### Server database: 9 tables
| Table | Holds | Niche detail |
|---|---|---|
| `classrooms` | Code, grade, curriculum | Unique code |
| `teachers` | Name, classroom | One classroom per teacher |
| `users` | Email, name, role, salt, hash | Unique email |
| `students` | Code, grade, language, classroom | Uses a code, not the email, as the working identity |
| `concepts` | Objective, prerequisites | The live graph is in `engine.py`; this column records it |
| `questions` | Prompt, options, answer, explanation, tag map, transfer flag | Options and tag map are JSON |
| `attempts` | Student, question, response, correct, stage, UUID, time | **Source of truth.** Unique on student and UUID |
| `learner_progress` | Mastery, evidence count, label, route per concept | **Derived and rebuildable.** Unique on student and concept |
| `interventions` | Pod members, text, status, notes | `student_ids` is JSON, a deliberate shortcut that I would normalise |

Current seed: 1 classroom, 1 teacher, 5 users, 4 students, 18 concepts, 58 questions, 16 attempts, 5 profiles, 4 pods.

### Where the database lives
- **Local:** `sqlite:///./prism.db`.
- **Container:** `sqlite:////data/prism.db`, seeded on first start by `entrypoint.sh` and not baked into the image.
- **Render free plan:** the filesystem is ephemeral, so a restart re-creates and re-seeds the database. That is fine for judging and not for real data.
- **Durable options:** a config change to Postgres (URL normalised, `psycopg` pinned) or a paid disk.
- **Schema changes:** `create_all` only. There are no migrations yet, and Alembic would be next.

### Browser storage
| Key | Holds | Why |
|---|---|---|
| `prism-session` | Token and user | Stay signed in. XSS exposure is a known trade-off. |
| `prism-language` | en, hi or te | Remember the choice |
| `prism-offline-attempts:<userId>` | Queued answers | Per account, because classroom devices are shared |
| `prism-cache:*` | Chapters, progress, questions | Open seen activities offline |

### In memory
The search index and reference tables are built at import. There is no Redis and no queue.

### What is collected
Name, email, password hash, classroom link and answers. There is no behavioural tracking in the schema. Demo data is synthetic.

### Privacy, if asked
India's DPDP rules were notified in November 2025 and require verifiable parental consent for under-18s, with a narrow exemption for educational institutions. PRISM has no consent or deletion flow yet, so it is demo-only. Do not claim compliance.

## 7. Translation

- **Method:** team-written string tables, not a translation API at runtime. A generic machine translation can distort terms like अंश and हर, and it would add a network dependency that offline use cannot afford.
- **Convention:** Hindi and Telugu keep the English term in parentheses where classrooms use it, for example `तुल्य भिन्न (Equivalent fractions)`.
- **Tables:**
  - `translations.ts`: app chrome and landing page
  - `localization.ts`: chapters, question prompts, explanations and options, keyed by question ID with a fallback match on English text
  - `enginesText.ts`: Engines Studio
  - `teacherText.ts`: teacher workspace, modals, route panels, 28 misconception names, pod text
- **Measured share of native-script letters, Hindi / Telugu, before the final fixes:** teacher page 80% / 82%, evidence record 81% / 81%, edit dialog 73% / 75%, print view 75% / 76%. The rest was mostly student names and codes.
- **Teacher edits are safe:** pod text is translated only if it exactly matches the library text, so a teacher's own words are never replaced.
- **Language behaviour:** saved in `localStorage` and set on `<html lang>`. The `students.language` column exists but nothing updates it yet.
- **Search:** the index is English. A small glossary maps listed Hindi and Telugu topic names to index terms. Other native-language queries return nothing.
- **Guards:** `i18n.test.ts` fails the build if a key is missing, empty, left in English, or loses a placeholder.
- **Still English in Hindi and Telugu:** the worked explanations for Chapters 2 to 8, Answer and Generative Engine output, and the 28 remedy sentences. All 58 question prompts and the prerequisite explanations are translated, and a test fails if a prompt is missing.
- **Not done:** review by a native-speaking maths teacher. I wrote or extended these translations, so say this if asked.

## 8. Security

- **Passwords:** PBKDF2-HMAC-SHA256 with 600,000 rounds, a per-user salt and constant-time comparison. Older 210,000-round hashes still work and upgrade at next sign-in.
- **Tokens:** 8-hour, HMAC-SHA256 signed, built from the standard library. They are **JWT-style, not real JWTs**: there is no header, so no algorithm-confusion surface, but also no standard tooling.
- **Roles:** `require_student`, `require_teacher`, `resolve_teacher`. A forged token gets 401, a student on a teacher route gets 403, and an anonymous caller gets 401.
- **Tenant isolation:** another class's student returns 404, so codes cannot be probed.
- **Demo mode:** `PRISM_DEMO_MODE=0` closes the persona list, demo header, reset and legacy routes, and makes `PRISM_AUTH_SECRET` mandatory at boot.
- **Static files:** the SPA handler checks the real path stays inside the build directory.
- **CORS:** exact origins only, no credentials, and not needed for same-origin serving.
- **Answers:** graded on the server, and explanations are sent only after an attempt.
- **LLM key:** sent in a header, not the URL.

## 9. Performance

Measured in-process with FastAPI's `TestClient` on a laptop with SQLite and 60 learners. There was no network and no concurrency, so **this is not a load test**.

| Operation | p50 | SQL statements |
|---|---|---|
| Teacher workspace, 60 learners | 8.8 ms | 11 |
| Recompile, 60 learners | 9.3 ms | 15 |
| Submit attempt | 10.7 ms | 14 |
| Answer Engine | 3.2 ms | 0 |
| Search | 5.1 ms | 0 |
| Login | 406 ms | 1 (slow on purpose: password hashing) |

- The workspace statement count stays flat as learners grow, because it uses bulk queries.
- JS bundle: 557 kB, 153 kB gzipped. Code splitting is not set up yet.
- The Render free plan took 33 seconds to wake from cold when measured.
- Handlers are synchronous `def`, run in FastAPI's thread pool, which suits short database work with a synchronous session.
- One Uvicorn worker, because SQLite allows one writer at a time. For production: Postgres and more workers.

## 10. Comparison with other platforms

**Do not say "nobody else does this".** Mindspark diagnoses misconceptions and has years of evidence behind it. The defensible claim is narrower: PRISM combines transparent rules with an evidence-to-small-group loop that the teacher controls.

| | **PRISM** | **Mindspark (Ei)** | **Khanmigo** | **DIKSHA** | **Embibe** |
|---|---|---|---|---|---|
| Main idea | Teacher-controlled pods from error patterns | Adaptive practice with misconception diagnosis | LLM tutor and teacher assistant | National content platform | Knowledge-graph personalised learning |
| Diagnosis | Rules on tagged wrong answers | Misconception-based, built on two decades of research | Conversational | No adaptive diagnosis found in public sources | Knowledge tracing at concept level |
| Teacher role | Approves, edits or rejects each pod | Receives reports on misconceptions and gaps | Generates plans, rubrics and differentiation | Courses and content | Teacher app reported, not confirmed on official pages |
| Explainability | Each decision shows its rule and responses | Reports | Model-generated | Not applicable | Model-based mastery |
| AI cost per answer | None | Not publicly stated | LLM usage | Not applicable | Not publicly stated |
| Languages | English, Hindi, Telugu | Vernacular versions reported | English and Hindi for India | 135 languages | Not checked |
| Offline | Answer queue with safe retries | Not checked | None found | Stated, details not found | Not checked |
| Evidence | **No pilot yet** | **J-PAL randomised trials** | Not checked | Very large national use | Vendor-reported |
| Scale and content | 8 chapters, 58 questions, 1 subject | Maths classes 1 to 10, plus English and science | Full Khan Academy library | 3.67 lakh pieces of e-content | 74,000+ concepts by its own count |

Competitor rows come from public descriptions, not from testing those products, so say "from what is publicly described".

**Where PRISM is genuinely stronger**
- **Teacher control:** the decision point is an editable group plan, and recompiling never overwrites it.
- **Traceability:** a teacher can see why, down to the response, in plain language.
- **Conservative labelling:** one mistake cannot label a child, and ambiguity goes to the teacher.
- **Cost and predictability:** no per-answer AI cost, and the same input always gives the same result.
- **Honest failure:** the solver says "could not solve" and does not guess.

**Where others are stronger:** Mindspark on evidence and content depth, Khan Academy on content and reach, DIKSHA on scale and languages, Embibe on graph size and statistical modelling. Say this first. It builds trust.

**Positioning line:**
> "We are not competing on content volume. We are testing one idea: can a teacher of 50 students get from raw answers to a defensible small-group plan in minutes, and stay in charge of it?"

## 11. Decisions and challenges

These all come from the real commit history and code.

| Problem found | Fix | Lesson |
|---|---|---|
| Demo profiles were hand-written, so the demo was partly fake | Derive every profile from attempts, with a test that replays them | The demo uses the same path as live traffic |
| An anonymous fallback exposed the class roster | Removed it, added tests | Convenience paths need the same scrutiny |
| Seeding in the Docker build wiped learner data on redeploy | Seed on first start only | Keep data out of image layers |
| Recompile deleted teacher approvals | Keep decisions, show suggestions | The code must match the product promise |
| One-click Approve erased notes | `None` now means "leave unchanged" | Defaults matter in partial updates |
| Tied error tags gave different labels per process | A tie now routes to the teacher | Iterating a set is not deterministic across runs |
| Foundation route was reachable only from seed data | Chapters now serve their prerequisite questions | Test the learner journey, not just the function |
| Teacher view read only Chapter 1 | Multi-chapter summaries and pods | A feature is not done until its reader sees it |
| A solver said "∛100 = 5 ✓" | Rebuilt checks on exact arithmetic, added tests | A check that is only a string is not a check |
| Shared devices could mix learners' queued answers | Queue per account | Design for how classrooms actually work |

**Why not an LLM for diagnosis?**
> "We need the same result every time and a reason a teacher can read. Our tags come from known error patterns, so we do not need inference. An LLM could help draft content later, with a person reviewing it, but it should not decide a child's route."

**Why FastAPI?** Boundary validation with Pydantic, automatic API docs at `/docs`, and rules testable without a server. Choose this over any claim about graph libraries: the engine uses plain dictionaries.

**Why SQLite?** No setup, real constraints, and the idempotency key relies on one. Postgres is a config change away.

**Why React with so few libraries?** Three runtime dependencies. Six routes did not justify a router library, so `seo.ts` handles routing with `pushState`.

**Why a monolith?** One team, one school-scale workload, and rules that belong in one transaction with the attempt.

## 12. Known limits

Say these before you are asked.

- **No classroom pilot.** Tests show the logic works as designed. Nothing yet shows students learn better.
- **Thresholds are hand-set,** and mastery ignores recency.
- **Curriculum version:** content follows the older 8-chapter NCERT book. NCERT's new Class 8 book, Ganita Prakash, has 14 chapters and replaced it, with some schools still in transition. Moving over is mostly a content change.
- **Prerequisite links are judgement calls,** with one question per skill, so a single slip can make a skill look weak.
- **Question bank is small and team-written,** without validation by a subject expert.
- **Offline covers queued answers and activities already seen.** With no service worker, a first page load needs a network.
- **Not built:** login rate limiting, parental consent and deletion flows, schema migrations, code splitting.
- **Anyone can register as a teacher.** Tenancy isolates them, but there is no school verification.
- **Not verified:** Docker image build, real concurrent load, and the Gemini fallback (no key available, and the default model name is an assumption).

## 13. Words to avoid

| Avoid | Say instead |
|---|---|
| EMA | Weighted average with a prior |
| JWT | Signed JWT-style token |
| Async, high-throughput | Synchronous handlers in a thread pool |
| Semantic or indexed search | Weighted keyword search |
| Generative AI | Randomised templates with tagged wrong answers |
| Real-time | Updated when the teacher refreshes or recompiles |
| Drag-and-drop | Click to reassign in the edit dialog |
| 9 normalized tables | 9 tables, with one JSON field I would normalise |
| Zero hallucinations | No model in routing |
| Official CBSE report | Printable school planning document |
| Current NCERT syllabus | Modelled on the earlier 8-chapter NCERT book |
| Proven to improve learning | Not yet tested in a classroom |

## 14. Rapid-fire niche answers

- **Why is mastery 0.09 and not 0 for all wrong?** The 0.35 prior contributes 0.0875.
- **Why can't mastery reach 95%?** With the prior fixed at 0.35, the most it can reach is 0.84. Keep that in mind when reading the dashboard.
- **What does the "50%" mean?** Share of all the learner's responses on that concept, not just the wrong ones.
- **What happens on two simultaneous retries?** Both can pass the read check. The unique constraint rejects one, and it returns as a duplicate.
- **Can a queue sync stop halfway?** Yes. Each item is removed only after success, and replaying is safe.
- **How often does sync retry?** On reconnect, and every 20 seconds while answers are waiting.
- **Is grading on the client?** No, on the server. An offline answer gets feedback only after syncing.
- **What is a `prerequisite_status` of unknown?** No attempted prerequisite yet. It never forces the foundation route.
- **How are answers compared?** Lowercased with spaces removed, against the stored answer.
- **Why do search and the database differ on questions?** The database serves 58, including 9 prerequisite checks. Search indexes the 48-item chapter bank, and 3 of its Chapter 1 items appear only in search.
- **Are Test and Diagnostic questions the same?** No exact duplicates. Every `test` item is flagged as transfer and weighted 1.4, but a few are routine rather than new contexts, such as the Pythagorean triplet question. Say so if asked.
- **What does Recompile do to a dismissed pod?** It keeps it dismissed and can still show a suggestion.
- **Do pods overlap across chapters?** Yes. One learner can be in a pod for each chapter they have worked on.
- **Which chapter does the teacher see for a learner?** Their most recently attempted chapter, with all chapters in the evidence record.
- **What does "Solver confidence: 100%" mean?** A rule solver matched and computed it. "Not solved" means nothing matched. The Gemini fallback, when enabled, shows 50% because nothing checked it.
- **What is `llms.txt`?** A plain-text summary for AI crawlers. It is a convention, not a guarantee of indexing.
- **Why `pool_pre_ping`?** It catches connections recycled by a managed database before a request fails.
- **Why normalise `postgres://`?** SQLAlchemy 2 rejects that alias, which would break at boot.
- **How do you test?** 320 pytest and 15 Vitest tests. A test session starts from empty databases, so old rows cannot hide a seed change. Run `npm run build` first, because two serving tests read the build output.

## 15. Day-of checklist

- [ ] Deploy `minor-fixes` and confirm the live site changed (`/api/search/suggestions?lang=hi` should return Hindi).
- [ ] Open the live site 5 minutes early, because the free plan sleeps.
- [ ] Keep a local copy running as backup, since restarts re-seed the database.
- [ ] Run the demo once on the deployed site, and reset through `/docs` (`POST /api/demo/reset`).
- [ ] Have open: `engine.py`, `scoring.py`, `compiler.py`, `models.py`, `/docs` and the app.
- [ ] One person answers while another shares the screen.
- [ ] When you do not know something, say "we have not built that; here is how I would".

---

## Sources for platform and policy facts

- [Mindspark: MIT Solve](https://solve.mit.edu/solutions/88679), [Ei brochure](https://ei.study/wp-content/uploads/2023/08/Ei-Mindspark-Brochure-2022-Web.pdf), [IT for Change panel](https://itforchange.net/sites/default/files/2025-10/Panel%201%20I%20Mindspark%20I%20EdTech%20for%20Equitable%20Education.pdf)
- [Khanmigo for teachers: Khan Academy blog](https://blog.khanacademy.org/teachers-in-44-countries-now-get-free-access-to-khanmigo-in-english-thanks-to-microsoft-support), [India launch coverage](https://scoonews.com/news/khan-academy-launches-khanmigo-ai-tool-for-teachers-in-india/?amp=1)
- [DIKSHA: PIB factsheet](https://pib.gov.in/FactsheetDetails.aspx?Id=150639), [Free Press Journal](https://www.freepressjournal.in/education/diksha-emerges-as-indias-one-nation-one-digital-platform-for-school-education)
- [Embibe: Achieve product page](https://embibe.com/in-en/best-education-content/dynamic-and-adaptive-practice-to-increase-competency-levels), [Embibe outcomes](https://embibe.com/outcomes)
- [Ganita Prakash: NCERT CIET](https://ciet.ncert.gov.in/audio-book/130), [Vedantu](https://www.vedantu.com/ncert-solutions/ncert-solutions-class-8-maths)
- [DPDP Rules: Biometric Update](https://www.biometricupdate.com/202511/india-notifies-its-sweeping-digital-personal-data-protection-rules), [AZB Partners](https://www.azbpartners.com/bank/one-step-closer-to-implementation-meity-releases-draft-dpdp-rules/), [Medianama](https://www.medianama.com/2025/11/223-dpdp-rules-real-time-child-tracking-without-consent/)
- [PBKDF2 iterations: PentesterLab](https://pentesterlab.com/glossary/pbkdf2) (a secondary source; OWASP's own cheat sheet was not directly retrieved)
