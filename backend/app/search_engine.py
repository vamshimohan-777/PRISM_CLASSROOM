"""PRISM Search Engine: High-performance, curriculum-aware indexed search.

Indexes CBSE Class VIII Mathematics concepts, prerequisite DAG nodes,
question banks, student misconceptions, and pedagogical intervention strategies.
Supports faceted filtering, relevance ranking, and highlight snippet extraction.
"""
from dataclasses import dataclass, field
import re
from typing import Any
from .catalog import CHAPTERS, MISCONCEPTIONS_DATABASE, PREREQUISITE_SKILLS, QUESTION_BANK
from .curriculum import CBSE_CURRICULUM
from .engine import CONCEPT_GRAPH, INTERVENTION_LIBRARY


SUGGESTIONS_BY_LANGUAGE: dict[str, list[str]] = {
    "en": [
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
        "Data handling probability",
    ],
    "hi": [
        "तुल्य भिन्न (Equivalent fractions)",
        "हर-परिमाण भ्रांति (Denominator magnitude)",
        "एक चर वाले रैखिक समीकरण (Linear equations)",
        "3x + 5 = 20 हल करें",
        "वर्ग और वर्गमूल (Squares and square roots)",
        "चतुर्भुजों की समझ (Quadrilaterals)",
        "योगात्मक तुल्यता भ्रांति (Additive bias)",
        "राशियों की तुलना और छूट (Discount)",
        "पूर्वापेक्षा संकल्पना DAG",
        "दृश्य भिन्न पट्टी समूह (Fraction bar pod)",
        "विधि मापन अनुप्रयोग (Recipe scaling)",
        "आँकड़ा प्रबंधन प्रायिकता (Probability)",
    ],
    "te": [
        "సమాన భిన్నాలు (Equivalent fractions)",
        "హారం-పరిమాణ అపోహ (Denominator magnitude)",
        "ఏక చరరాశి రేఖీయ సమీకరణాలు (Linear equations)",
        "3x + 5 = 20 పరిష్కరించండి",
        "వర్గాలు మరియు వర్గమూలాలు (Squares and square roots)",
        "చతుర్భుజాల అవగాహన (Quadrilaterals)",
        "సంకలన సమానత్వ అపోహ (Additive bias)",
        "రాశుల పోలిక మరియు తగ్గింపు (Discount)",
        "ముందస్తు భావన DAG",
        "దృశ్య భిన్న పట్టీ బృందం (Fraction bar pod)",
        "వంటకం నిష్పత్తి అనువర్తనం (Recipe scaling)",
        "దత్తాంశ నిర్వహణ సంభావ్యత (Probability)",
    ],
}


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
            skill = PREREQUISITE_SKILLS.get(concept_id)
            desc = skill["objective"] if skill else concept_descriptions.get(concept_id, f"Core learning concept for {concept_id}")
            owning_chapter = next((c["id"] for c in CHAPTERS if c["concept"] == concept_id), None)
            self.index.append({
                "id": f"concept-{concept_id}",
                "type": "concept",
                "title": f"Concept: {concept_id.replace('-', ' ').title()}",
                "text": f"{concept_id} {desc} prerequisites: {' '.join(parents)}",
                "chapter_id": skill["chapter_id"] if skill else owning_chapter,
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
        raw_query = self._english_terms((query or "").strip().lower())
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

    @staticmethod
    def _english_terms(query: str) -> str:
        """Map a Hindi or Telugu topic name to the English term the index is written in.

        The localised suggestion list doubles as a small glossary: 'तुल्य भिन्न
        (Equivalent fractions)' pairs a native name with its index term. Topics
        outside this list still need an English query.
        """
        if query.isascii():
            return query
        for lang in ("hi", "te"):
            for entry in SUGGESTIONS_BY_LANGUAGE[lang]:
                native, _, rest = entry.partition(" (")
                if rest and query.split(" (")[0] in native.lower():
                    return rest.rstrip(")").lower()
        return query

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

    def get_suggestions(self, prefix: str = "", limit: int = 6, lang: str = "en") -> list[str]:
        """Provides instant query autocompletion suggestions in the caller's language.

        These are rendered as clickable chips in the UI, so they are shown to the
        learner and have to follow the language switcher like any other visible
        string. The index itself is English, so a localised chip carries its
        English term in parentheses, matching how these topics are named in
        Hindi- and Telugu-medium CBSE classrooms, and keeping the chip usable as
        a query against the index.
        """
        curated = SUGGESTIONS_BY_LANGUAGE.get(lang, SUGGESTIONS_BY_LANGUAGE["en"])
        p = prefix.strip().lower()
        if not p:
            return curated[:limit]
        matches = [s for s in curated if p in s.lower()]
        if matches:
            return matches[:limit]
        # Fall back to matching the English index, so a learner typing an English
        # term still gets suggestions while the interface is in another language.
        english = [s for s in SUGGESTIONS_BY_LANGUAGE["en"] if p in s.lower()]
        return english[:limit] or [f"{prefix} concept", f"{prefix} questions", f"{prefix} misconception"]


# Global engine singleton
search_engine = SearchEngine()

