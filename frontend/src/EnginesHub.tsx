import { useState, useEffect, FormEvent } from 'react';
import {
  Search,
  Sparkles,
  HelpCircle,
  BookOpen,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ArrowRight,
  ExternalLink,
  Layers,
  Cpu,
  RefreshCw,
  Printer,
  ChevronRight,
  Lightbulb,
  Check,
  Compass,
  FileText,
  Clock3,
  Shield,
  Zap,
} from 'lucide-react';
import {
  api,
  SearchResultItem,
  AnswerResponse,
  GeneratedQuestion,
  RemediationGuide,
  GeneratedLessonPlan,
  GeneratedTransferTask,
} from './api';
import { Language, TRANSLATIONS } from './translations';

interface EnginesHubProps {
  lang: Language;
  initialTab?: 'search' | 'answer' | 'generative';
  initialQuery?: string;
  onNavigateToCurriculum?: () => void;
}

export function EnginesHub({
  lang,
  initialTab = 'search',
  initialQuery = '',
  onNavigateToCurriculum,
}: EnginesHubProps) {
  const [activeEngine, setActiveEngine] = useState<'search' | 'answer' | 'generative'>(initialTab);

  // ---------------------------------------------------------------------------
  // 1. Search Engine State
  // ---------------------------------------------------------------------------
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [entityType, setEntityType] = useState<string>('all');
  const [chapterFilter, setChapterFilter] = useState<string>('all');
  const [searchResults, setSearchResults] = useState<SearchResultItem[]>([]);
  const [searchBusy, setSearchBusy] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // ---------------------------------------------------------------------------
  // 2. Answer Engine State
  // ---------------------------------------------------------------------------
  const [answerQuery, setAnswerQuery] = useState('');
  const [answerResult, setAnswerResult] = useState<AnswerResponse | null>(null);
  const [answerBusy, setAnswerBusy] = useState(false);
  const [answerError, setAnswerError] = useState('');
  const [practiceSelected, setPracticeSelected] = useState<string | null>(null);

  // ---------------------------------------------------------------------------
  // 3. Generative Engine State
  // ---------------------------------------------------------------------------
  const [genMode, setGenMode] = useState<'question' | 'remediation' | 'lesson-plan' | 'transfer'>('question');

  // Question gen state
  const [genConcept, setGenConcept] = useState('equivalent-fractions');
  const [genStage, setGenStage] = useState<'diagnostic' | 'practice' | 'test'>('practice');
  const [genDifficulty, setGenDifficulty] = useState<'foundation' | 'standard' | 'challenge'>('standard');
  const [generatedQuestion, setGeneratedQuestion] = useState<GeneratedQuestion | null>(null);
  const [genQuestionBusy, setGenQuestionBusy] = useState(false);
  const [genSelectedOption, setGenSelectedOption] = useState<string | null>(null);

  // Remediation gen state
  const [genMisconception, setGenMisconception] = useState('denominator-magnitude');
  const [genStudentName, setGenStudentName] = useState('Aarav Sharma');
  const [remediationGuide, setRemediationGuide] = useState<RemediationGuide | null>(null);
  const [remediationBusy, setRemediationBusy] = useState(false);

  // Lesson plan state
  const [lessonPlan, setLessonPlan] = useState<GeneratedLessonPlan | null>(null);
  const [lessonPlanBusy, setLessonPlanBusy] = useState(false);

  // Transfer task state
  const [transferTheme, setTransferTheme] = useState<'recipes' | 'railways' | 'cricket'>('recipes');
  const [transferTask, setTransferTask] = useState<GeneratedTransferTask | null>(null);
  const [transferBusy, setTransferBusy] = useState(false);

  // Quick prompt chips for Answer Engine
  const answerPromptChips = [
    'Solve: 3x + 5 = 20',
    'Compare: 1/3 and 1/8',
    'Simplify: 18/24',
    'Square root of 144',
    '10% discount on ₹500',
    'Quadrilateral 4th angle: 90°, 85°, 110°',
    'Mean of 4, 6, and 8',
    'What is a rational number?',
  ];

  // Run initial search if query provided
  useEffect(() => {
    if (initialQuery) {
      handleSearch(initialQuery);
    } else {
      // Default initial query
      handleSearch('fraction');
    }
  }, []);

  const handleSearch = async (q: string) => {
    const term = q.trim();
    if (!term) return;
    setSearchBusy(true);
    setHasSearched(true);
    setShowSuggestions(false);
    try {
      const res = await api.search(term, entityType, chapterFilter, 20);
      setSearchResults(res.results);
    } catch (e) {
      console.error('Search error:', e);
    } finally {
      setSearchBusy(false);
    }
  };

  const handleSearchSubmit = (e: FormEvent) => {
    e.preventDefault();
    handleSearch(searchQuery);
  };

  const fetchSuggestions = async (prefix: string) => {
    if (!prefix.trim()) {
      setSuggestions([]);
      return;
    }
    try {
      const res = await api.searchSuggestions(prefix);
      setSuggestions(res.suggestions);
    } catch {
      setSuggestions([]);
    }
  };

  const handleAnswerSubmit = async (qText?: string) => {
    const q = (qText || answerQuery).trim();
    if (!q) return;
    setAnswerBusy(true);
    setAnswerError('');
    setPracticeSelected(null);
    try {
      const res = await api.answer(q);
      setAnswerResult(res);
      setAnswerQuery(q);
    } catch (e) {
      setAnswerError(e instanceof Error ? e.message : 'Unable to solve this problem.');
    } finally {
      setAnswerBusy(false);
    }
  };

  const handleGenerateQuestion = async () => {
    setGenQuestionBusy(true);
    setGenSelectedOption(null);
    try {
      const res = await api.generateQuestion(genConcept, genStage, genDifficulty);
      setGeneratedQuestion(res);
    } catch (e) {
      console.error('Gen question error:', e);
    } finally {
      setGenQuestionBusy(false);
    }
  };

  const handleGenerateRemediation = async () => {
    setRemediationBusy(true);
    try {
      const res = await api.generateRemediation(genMisconception, genStudentName, 8);
      setRemediationGuide(res);
    } catch (e) {
      console.error('Gen remediation error:', e);
    } finally {
      setRemediationBusy(false);
    }
  };

  const handleGenerateLessonPlan = async () => {
    setLessonPlanBusy(true);
    try {
      const res = await api.generateLessonPlan(genConcept, '8A-CBSE');
      setLessonPlan(res);
    } catch (e) {
      console.error('Gen lesson plan error:', e);
    } finally {
      setLessonPlanBusy(false);
    }
  };

  const handleGenerateTransfer = async () => {
    setTransferBusy(true);
    try {
      const res = await api.generateTransferTask(genConcept, transferTheme);
      setTransferTask(res);
    } catch (e) {
      console.error('Gen transfer error:', e);
    } finally {
      setTransferBusy(false);
    }
  };

  return (
    <div className="engines-hub-container">
      {/* Top Banner & Header */}
      <div className="engines-header">
        <div className="engine-badges">
          <span className="badge-pill purple">PRISM 3-ENGINE ARCHITECTURE</span>
          <span className="badge-pill teal">CBSE CLASS VIII NCERT MATHEMATICS</span>
          <span className="badge-pill green">100% REPRODUCIBLE & VERIFIED</span>
        </div>
        <h1>Curriculum Engines Hub</h1>
        <p>
          Integrated Search Engine for syllabus knowledge, Answer Engine for NCERT step-by-step problem solving,
          and Generative Engine for dynamic questions, remediation guides, and differentiated lesson plans.
        </p>

        {/* 3 Main Engine Switcher Tabs */}
        <div className="engine-tabs-nav">
          <button
            type="button"
            className={`engine-nav-pill ${activeEngine === 'search' ? 'active' : ''}`}
            onClick={() => setActiveEngine('search')}
          >
            <Search size={18} />
            <span>Search Engine</span>
            <small>Curriculum & Concepts</small>
          </button>
          <button
            type="button"
            className={`engine-nav-pill ${activeEngine === 'answer' ? 'active' : ''}`}
            onClick={() => setActiveEngine('answer')}
          >
            <Lightbulb size={18} />
            <span>Answer Engine</span>
            <small>Step-by-Step Solver</small>
          </button>
          <button
            type="button"
            className={`engine-nav-pill ${activeEngine === 'generative' ? 'active' : ''}`}
            onClick={() => setActiveEngine('generative')}
          >
            <Sparkles size={18} />
            <span>Generative Engine</span>
            <small>Questions, Guides & Plans</small>
          </button>
        </div>
      </div>

      {/* =================================================================== */}
      {/* 1. SEARCH ENGINE PANEL                                              */}
      {/* =================================================================== */}
      {activeEngine === 'search' && (
        <section className="engine-panel search-panel">
          <div className="search-controls-card">
            <form onSubmit={handleSearchSubmit} className="search-bar-form">
              <div className="search-input-wrapper">
                <Search size={20} className="search-icon-input" />
                <input
                  type="text"
                  value={searchQuery}
                  placeholder="Search chapters, concepts, questions, misconceptions, or intervention strategies..."
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    fetchSuggestions(e.target.value);
                    setShowSuggestions(true);
                  }}
                  onFocus={() => {
                    if (suggestions.length > 0) setShowSuggestions(true);
                  }}
                />
                {searchQuery && (
                  <button
                    type="button"
                    className="search-clear-btn"
                    onClick={() => {
                      setSearchQuery('');
                      setSuggestions([]);
                    }}
                  >
                    ×
                  </button>
                )}
                <button type="submit" className="btn-primary search-submit-btn" disabled={searchBusy}>
                  {searchBusy ? 'Searching…' : 'Search'}
                </button>
              </div>

              {/* Autocomplete Suggestions Dropdown */}
              {showSuggestions && suggestions.length > 0 && (
                <div className="search-suggestions-dropdown">
                  {suggestions.map((s, idx) => (
                    <div
                      key={idx}
                      className="suggestion-item"
                      onClick={() => {
                        setSearchQuery(s);
                        setShowSuggestions(false);
                        handleSearch(s);
                      }}
                    >
                      <Search size={14} />
                      <span>{s}</span>
                    </div>
                  ))}
                </div>
              )}
            </form>

            {/* Faceted Filter Pills */}
            <div className="search-facets-row">
              <span className="facet-label">Entity Type:</span>
              {[
                { id: 'all', label: 'All Entities' },
                { id: 'chapter', label: 'Chapters' },
                { id: 'concept', label: 'DAG Concepts' },
                { id: 'question', label: 'Questions' },
                { id: 'misconception', label: 'Misconceptions' },
                { id: 'intervention', label: 'Interventions' },
              ].map((f) => (
                <button
                  key={f.id}
                  type="button"
                  className={`facet-pill ${entityType === f.id ? 'active' : ''}`}
                  onClick={() => {
                    setEntityType(f.id);
                    if (searchQuery) handleSearch(searchQuery);
                  }}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          {/* Search Results List */}
          <div className="search-results-container">
            <div className="results-status-bar">
              <span>
                Found <b>{searchResults.length}</b> result{searchResults.length === 1 ? '' : 's'} for "{searchQuery}"
              </span>
              <span className="results-sort-note">Sorted by relevance score</span>
            </div>

            {searchBusy && (
              <div className="loading-state">
                <RefreshCw size={24} className="spin" />
                <p>Indexing and searching curriculum database...</p>
              </div>
            )}

            {!searchBusy && searchResults.length === 0 && hasSearched && (
              <div className="empty-results-box">
                <Compass size={40} className="empty-icon" />
                <h3>No exact matches found</h3>
                <p>Try searching for terms like "fraction", "linear equations", "denominator", or "square root".</p>
                <div className="quick-suggestions-pills">
                  {['Equivalent fractions', 'Linear equations', 'Denominator magnitude', 'Square root'].map((term) => (
                    <button
                      key={term}
                      type="button"
                      className="quick-term-btn"
                      onClick={() => {
                        setSearchQuery(term);
                        handleSearch(term);
                      }}
                    >
                      {term}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="results-grid">
              {searchResults.map((item) => (
                <div key={item.id} className={`search-result-card card-type-${item.type}`}>
                  <div className="result-card-header">
                    <span className={`result-type-badge ${item.type}`}>
                      {item.type.toUpperCase()}
                    </span>
                    <span className="relevance-score-badge">
                      {Math.min(100, Math.round(item.relevance_score * 5))}% Relevance
                    </span>
                  </div>

                  <h3 className="result-title">{item.title}</h3>
                  <p className="result-snippet">{item.snippet}</p>

                  <div className="result-tags-row">
                    {item.tags.slice(0, 4).map((tag, i) => (
                      <span key={i} className="mini-tag">
                        #{tag}
                      </span>
                    ))}
                  </div>

                  <div className="result-card-actions">
                    {item.type === 'misconception' && (
                      <button
                        type="button"
                        className="btn-link-action"
                        onClick={() => {
                          setGenMisconception(item.metadata?.id || 'denominator-magnitude');
                          setActiveEngine('generative');
                          setGenMode('remediation');
                          handleGenerateRemediation();
                        }}
                      >
                        <Sparkles size={14} /> Generate Remediation Guide
                      </button>
                    )}

                    {item.type === 'question' && (
                      <button
                        type="button"
                        className="btn-link-action"
                        onClick={() => {
                          setAnswerQuery(item.metadata?.prompt || item.title);
                          setActiveEngine('answer');
                          handleAnswerSubmit(item.metadata?.prompt || item.title);
                        }}
                      >
                        <Lightbulb size={14} /> Solve in Answer Engine
                      </button>
                    )}

                    {item.type === 'chapter' && onNavigateToCurriculum && (
                      <button
                        type="button"
                        className="btn-link-action"
                        onClick={onNavigateToCurriculum}
                      >
                        <BookOpen size={14} /> View Syllabus Chapter
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* =================================================================== */}
      {/* 2. ANSWER ENGINE PANEL                                              */}
      {/* =================================================================== */}
      {activeEngine === 'answer' && (
        <section className="engine-panel answer-panel">
          <div className="answer-query-box">
            <span className="eyebrow">NCERT PEDAGOGICAL SOLVER & REASONING ENGINE</span>
            <h2>Ask or Solve Any CBSE Class VIII Problem</h2>
            <p>
              Provides step-by-step NCERT reasoning, mathematical verification, common misconception traps,
              prerequisite DAG linkage, and instant practice challenges.
            </p>

            <div className="answer-input-row">
              <input
                type="text"
                value={answerQuery}
                placeholder="e.g. Solve: 3x + 5 = 20, Compare 1/3 and 1/8, Simplify 18/24, Square root of 144..."
                onChange={(e) => setAnswerQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleAnswerSubmit();
                }}
              />
              <button
                type="button"
                className="btn-primary"
                onClick={() => handleAnswerSubmit()}
                disabled={answerBusy || !answerQuery.trim()}
              >
                {answerBusy ? 'Solving…' : 'Solve Step-by-Step'} <ArrowRight size={16} />
              </button>
            </div>

            {/* Quick Prompt Chips */}
            <div className="prompt-chips-tray">
              <span className="chips-label">Quick Prompts:</span>
              {answerPromptChips.map((chip, idx) => (
                <button
                  key={idx}
                  type="button"
                  className="prompt-chip"
                  onClick={() => {
                    setAnswerQuery(chip);
                    handleAnswerSubmit(chip);
                  }}
                >
                  {chip}
                </button>
              ))}
            </div>
          </div>

          {answerError && <div className="errorbox" style={{ marginTop: '16px' }}>{answerError}</div>}

          {answerBusy && (
            <div className="loading-state" style={{ padding: '48px 0' }}>
              <RefreshCw size={28} className="spin purple-text" />
              <h3>Deriving step-by-step solution...</h3>
              <p>Analyzing equations, checking balance rules, and extracting NCERT explanations.</p>
            </div>
          )}

          {/* Answer Engine Results Showcase */}
          {answerResult && !answerBusy && (
            <div className="answer-result-display">
              {/* Category & Status Bar */}
              <div className="answer-meta-bar">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge-pill purple">{answerResult.category}</span>
                  <span className="badge-pill green">
                    <Shield size={12} style={{ display: 'inline', marginRight: '4px' }} />
                    {answerResult.source}
                  </span>
                </div>
                <span className="confidence-pill">
                  Confidence: {Math.round(answerResult.confidence * 100)}%
                </span>
              </div>

              {/* Direct Answer Banner */}
              <div className="direct-answer-banner">
                <div className="check-icon-large">
                  <CheckCircle2 size={32} />
                </div>
                <div>
                  <span className="answer-label">DIRECT VERIFIED RESULT</span>
                  <div className="answer-main-text">{answerResult.direct_answer}</div>
                </div>
              </div>

              {/* Step-by-Step Derivation */}
              <div className="derivation-steps-section">
                <h3>Step-by-Step NCERT Pedagogical Derivation</h3>
                <div className="steps-list">
                  {answerResult.steps.map((st, i) => (
                    <div key={i} className="step-card">
                      <div className="step-number-bubble">{st.step_number}</div>
                      <div className="step-body">
                        <h4>{st.title}</h4>
                        <p>{st.explanation}</p>
                        {st.math_expr && (
                          <div className="math-expression-box">
                            <code>{st.math_expr}</code>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Two Column Section: Verification & Misconception Warning */}
              <div className="answer-insights-grid">
                {/* Verification Box */}
                <div className="insight-card verification-card">
                  <div className="insight-header">
                    <Check size={20} className="green-text" />
                    <h4>Self-Check Verification</h4>
                  </div>
                  <p>{answerResult.verification}</p>
                </div>

                {/* Misconception Trap Alert */}
                <div className="insight-card trap-alert-card">
                  <div className="insight-header">
                    <AlertTriangle size={20} className="amber-text" />
                    <h4>Common Misconception Trap</h4>
                  </div>
                  <p>{answerResult.misconception_warning}</p>
                </div>
              </div>

              {/* Prerequisites DAG Tags */}
              {answerResult.prerequisites.length > 0 && (
                <div className="prerequisites-strip">
                  <span className="prereq-label">Prerequisites from Concept DAG:</span>
                  {answerResult.prerequisites.map((p, i) => (
                    <span key={i} className="prereq-badge">
                      🔗 {p.replace('-', ' ')}
                    </span>
                  ))}
                </div>
              )}

              {/* Interactive Follow-Up Practice Challenge */}
              {answerResult.practice_challenge && (
                <div className="practice-challenge-box">
                  <div className="challenge-header">
                    <Zap size={20} className="purple-text" />
                    <h4>Check Your Understanding: Quick Challenge</h4>
                  </div>
                  <p className="challenge-prompt">{answerResult.practice_challenge.question}</p>

                  <div className="challenge-options-grid">
                    {answerResult.practice_challenge.options.map((opt, i) => {
                      const isChosen = practiceSelected === opt;
                      const isCorrect = opt === answerResult.practice_challenge.correct_answer;
                      let btnClass = 'challenge-opt-btn';
                      if (practiceSelected) {
                        if (isCorrect) btnClass += ' correct';
                        else if (isChosen) btnClass += ' wrong';
                      }

                      return (
                        <button
                          key={i}
                          type="button"
                          className={btnClass}
                          disabled={practiceSelected !== null}
                          onClick={() => setPracticeSelected(opt)}
                        >
                          <span className="opt-letter">{String.fromCharCode(65 + i)}</span>
                          <span>{opt}</span>
                          {practiceSelected && isCorrect && <CheckCircle2 size={16} className="green-text" />}
                          {practiceSelected && isChosen && !isCorrect && <XCircle size={16} className="red-text" />}
                        </button>
                      );
                    })}
                  </div>

                  {practiceSelected && (
                    <div className={`challenge-feedback-box ${practiceSelected === answerResult.practice_challenge.correct_answer ? 'correct' : 'wrong'}`}>
                      <b>
                        {practiceSelected === answerResult.practice_challenge.correct_answer
                          ? '✓ Excellent! You got it right.'
                          : '✕ Not quite.'}
                      </b>
                      <p>{answerResult.practice_challenge.explanation}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </section>
      )}

      {/* =================================================================== */}
      {/* 3. GENERATIVE ENGINE PANEL                                          */}
      {/* =================================================================== */}
      {activeEngine === 'generative' && (
        <section className="engine-panel generative-panel">
          <div className="gen-subnav-row">
            <button
              type="button"
              className={`gen-sub-btn ${genMode === 'question' ? 'active' : ''}`}
              onClick={() => {
                setGenMode('question');
                if (!generatedQuestion) handleGenerateQuestion();
              }}
            >
              <Cpu size={16} /> Dynamic Question Generator
            </button>
            <button
              type="button"
              className={`gen-sub-btn ${genMode === 'remediation' ? 'active' : ''}`}
              onClick={() => {
                setGenMode('remediation');
                if (!remediationGuide) handleGenerateRemediation();
              }}
            >
              <Layers size={16} /> Personalized Remediation Guide
            </button>
            <button
              type="button"
              className={`gen-sub-btn ${genMode === 'lesson-plan' ? 'active' : ''}`}
              onClick={() => {
                setGenMode('lesson-plan');
                if (!lessonPlan) handleGenerateLessonPlan();
              }}
            >
              <FileText size={16} /> 45-Min Differentiated Lesson Plan
            </button>
            <button
              type="button"
              className={`gen-sub-btn ${genMode === 'transfer' ? 'active' : ''}`}
              onClick={() => {
                setGenMode('transfer');
                if (!transferTask) handleGenerateTransfer();
              }}
            >
              <Compass size={16} /> Indian Contextual Transfer Tasks
            </button>
          </div>

          {/* 3A. Dynamic Question Generator */}
          {genMode === 'question' && (
            <div className="gen-tool-card">
              <div className="gen-controls-bar">
                <div className="control-group">
                  <label>Chapter / Concept</label>
                  <select value={genConcept} onChange={(e) => setGenConcept(e.target.value)}>
                    <option value="equivalent-fractions">Rational Numbers & Fractions</option>
                    <option value="linear-equations">Linear Equations in One Variable</option>
                    <option value="squares-roots">Squares & Square Roots</option>
                    <option value="cubes-roots">Cubes & Cube Roots</option>
                    <option value="quadrilaterals">Understanding Quadrilaterals</option>
                    <option value="comparing-quantities">Comparing Quantities & Percentages</option>
                  </select>
                </div>

                <div className="control-group">
                  <label>Stage</label>
                  <select value={genStage} onChange={(e) => setGenStage(e.target.value as any)}>
                    <option value="diagnostic">Diagnostic (Initial Probe)</option>
                    <option value="practice">Practice (Scaffolded)</option>
                    <option value="test">Transfer Test (Novel Context)</option>
                  </select>
                </div>

                <div className="control-group">
                  <label>Difficulty</label>
                  <select value={genDifficulty} onChange={(e) => setGenDifficulty(e.target.value as any)}>
                    <option value="foundation">Foundation (Visual Scaffolds)</option>
                    <option value="standard">Standard (CBSE Regular)</option>
                    <option value="challenge">Challenge (Multi-step)</option>
                  </select>
                </div>

                <button
                  type="button"
                  className="btn-primary gen-action-btn"
                  onClick={handleGenerateQuestion}
                  disabled={genQuestionBusy}
                >
                  <RefreshCw size={16} className={genQuestionBusy ? 'spin' : ''} />
                  {genQuestionBusy ? 'Generating…' : 'Generate New Question'}
                </button>
              </div>

              {generatedQuestion && (
                <div className="generated-item-box">
                  <div className="item-meta-row">
                    <span className="badge-pill purple">ID: {generatedQuestion.id}</span>
                    <span className="badge-pill teal">Concept: {generatedQuestion.concept_id}</span>
                    <span className="badge-pill green">Difficulty: {generatedQuestion.difficulty}</span>
                    {generatedQuestion.is_transfer && <span className="badge-pill gold">Transfer Item</span>}
                  </div>

                  <h3 className="generated-prompt">{generatedQuestion.prompt}</h3>

                  <div className="options-interactive-grid">
                    {generatedQuestion.options.map((opt, i) => {
                      const isChosen = genSelectedOption === opt;
                      const isCorrect = opt === generatedQuestion.expected_answer;
                      let cls = 'gen-option-btn';
                      if (genSelectedOption) {
                        if (isCorrect) cls += ' correct';
                        else if (isChosen) cls += ' wrong';
                      }

                      return (
                        <button
                          key={i}
                          type="button"
                          className={cls}
                          onClick={() => setGenSelectedOption(opt)}
                        >
                          <span className="opt-letter">{String.fromCharCode(65 + i)}</span>
                          <span>{opt}</span>
                        </button>
                      );
                    })}
                  </div>

                  {genSelectedOption && (
                    <div className="gen-answer-revelation">
                      <div className="explanation-box">
                        <b>Step-by-Step NCERT Explanation:</b>
                        <p>{generatedQuestion.explanation}</p>
                      </div>

                      {/* The Misconception Map Table */}
                      <div className="distractor-misconception-table">
                        <h4>Cognitive Misconception Distractor Map</h4>
                        <p className="subtext">
                          Unlike naive random generators, PRISM maps each incorrect distractor to a specific latent cognitive error.
                        </p>
                        <table>
                          <thead>
                            <tr>
                              <th>Option</th>
                              <th>Nature</th>
                              <th>Associated Latent Misconception</th>
                            </tr>
                          </thead>
                          <tbody>
                            {generatedQuestion.options.map((opt, idx) => {
                              const isCorr = opt === generatedQuestion.expected_answer;
                              const tag = generatedQuestion.misconception_map[opt];
                              return (
                                <tr key={idx} className={isCorr ? 'row-correct' : 'row-distractor'}>
                                  <td><b>{opt}</b></td>
                                  <td>
                                    {isCorr ? (
                                      <span className="badge-pill green">Correct Answer</span>
                                    ) : (
                                      <span className="badge-pill red">Distractor</span>
                                    )}
                                  </td>
                                  <td>{isCorr ? 'Valid mathematical application' : tag ? `🚨 ${tag}` : 'Calculation slip'}</td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* 3B. Personalized Remediation Guide Generator */}
          {genMode === 'remediation' && (
            <div className="gen-tool-card">
              <div className="gen-controls-bar">
                <div className="control-group">
                  <label>Target Student Misconception</label>
                  <select value={genMisconception} onChange={(e) => setGenMisconception(e.target.value)}>
                    <option value="denominator-magnitude">Denominator-Magnitude (1/8 &gt; 1/3)</option>
                    <option value="additive-bias">Additive Equivalence Bias (+1/+1)</option>
                    <option value="unequal-operations">Unequal Multiplier Operations</option>
                    <option value="sign-inversion-slip">Sign Inversion & Balancing Error</option>
                  </select>
                </div>

                <div className="control-group">
                  <label>Learner Name</label>
                  <input
                    type="text"
                    value={genStudentName}
                    onChange={(e) => setGenStudentName(e.target.value)}
                    placeholder="Student name"
                  />
                </div>

                <button
                  type="button"
                  className="btn-primary gen-action-btn"
                  onClick={handleGenerateRemediation}
                  disabled={remediationBusy}
                >
                  <RefreshCw size={16} className={remediationBusy ? 'spin' : ''} />
                  {remediationBusy ? 'Generating Guide…' : 'Generate Remediation Guide'}
                </button>
              </div>

              {remediationGuide && (
                <div className="remediation-display-card">
                  <div className="remediation-header">
                    <span className="badge-pill purple">INDIVIDUAL REMEDIATION DOSSIER</span>
                    <h2>{remediationGuide.title}</h2>
                    <p className="student-target-tag">
                      Prepared for: <b>{remediationGuide.student_name}</b> · Class {remediationGuide.grade}
                    </p>
                  </div>

                  <div className="remediation-section barrier-box">
                    <h4>Cognitive Barrier Analysis</h4>
                    <p>{remediationGuide.cognitive_barrier}</p>
                  </div>

                  <div className="remediation-grid-2">
                    <div className="remediation-box analogy-box">
                      <h4>🥞 Concrete Real-World Mental Model</h4>
                      <p>{remediationGuide.concrete_analogy}</p>
                    </div>

                    <div className="remediation-box counter-box">
                      <h4>⚡ Proof by Contrast Counter-Example</h4>
                      <p>{remediationGuide.counter_example}</p>
                    </div>
                  </div>

                  <div className="remediation-box tool-box">
                    <h4>🛠 Recommended Visual Manipulative</h4>
                    <p>{remediationGuide.visual_manipulative}</p>
                  </div>

                  <div className="remediation-box steps-box">
                    <h4>3-Step Guided Scaffolding Sequence</h4>
                    <ol>
                      {remediationGuide.guided_steps.map((st, i) => (
                        <li key={i}>{st}</li>
                      ))}
                    </ol>
                  </div>

                  <div className="remediation-box probe-box">
                    <h4>🎯 Targeted Diagnostic Verification Probe</h4>
                    <p><b>{remediationGuide.diagnostic_probe.question}</b></p>
                    <div className="probe-options-row">
                      {remediationGuide.diagnostic_probe.options.map((opt, i) => (
                        <span
                          key={i}
                          className={`probe-chip ${opt === remediationGuide.diagnostic_probe.correct_answer ? 'correct' : ''}`}
                        >
                          {opt} {opt === remediationGuide.diagnostic_probe.correct_answer ? '✓ (Key)' : ''}
                        </span>
                      ))}
                    </div>
                    <small className="probe-explanation">{remediationGuide.diagnostic_probe.explanation}</small>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* 3C. 45-Min Differentiated Lesson Plan */}
          {genMode === 'lesson-plan' && (
            <div className="gen-tool-card">
              <div className="gen-controls-bar">
                <div className="control-group">
                  <label>Curriculum Concept</label>
                  <select value={genConcept} onChange={(e) => setGenConcept(e.target.value)}>
                    <option value="equivalent-fractions">Equivalent Fractions & Rational Numbers</option>
                    <option value="linear-equations">Linear Equations in One Variable</option>
                    <option value="quadrilaterals">Understanding Quadrilaterals</option>
                  </select>
                </div>

                <button
                  type="button"
                  className="btn-primary gen-action-btn"
                  onClick={handleGenerateLessonPlan}
                  disabled={lessonPlanBusy}
                >
                  <RefreshCw size={16} className={lessonPlanBusy ? 'spin' : ''} />
                  {lessonPlanBusy ? 'Compiling…' : 'Generate Differentiated Lesson Plan'}
                </button>

                {lessonPlan && (
                  <button type="button" className="btn-secondary" onClick={() => window.print()}>
                    <Printer size={15} /> Print / Save PDF
                  </button>
                )}
              </div>

              {lessonPlan && (
                <div className="lesson-plan-dossier">
                  <div className="plan-dossier-header">
                    <span className="badge-pill purple">{lessonPlan.curriculum_framework}</span>
                    <h2>{lessonPlan.title}</h2>
                    <div className="plan-stats-row">
                      <span><Clock3 size={15} /> {lessonPlan.duration_minutes} Minutes</span>
                      <span><Layers size={15} /> 4 Parallel Targeted Pods</span>
                      <span><Shield size={15} /> CBSE Inspection Compliant</span>
                    </div>
                  </div>

                  <div className="plan-objectives-box">
                    <h4>Core Learning Outcomes (CBSE / NEP 2020)</h4>
                    <ul>
                      {lessonPlan.learning_objectives.map((obj, i) => (
                        <li key={i}>{obj}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Timeline Phases */}
                  <div className="plan-timeline-container">
                    <h4>Structured 45-Minute Lesson Timeline</h4>
                    {lessonPlan.timeline.map((phase, idx) => (
                      <div key={idx} className="timeline-phase-card">
                        <div className="phase-header-row">
                          <span className="phase-duration-badge">{phase.duration}</span>
                          <h3>{phase.phase}</h3>
                          <span className="phase-pedagogy-tag">{phase.pedagogy}</span>
                        </div>

                        {phase.teacher_prompt && (
                          <div className="phase-prompt-box">
                            <b>Teacher Opening Script / Prompt:</b>
                            <p>"{phase.teacher_prompt}"</p>
                          </div>
                        )}

                        {phase.student_action && (
                          <p className="phase-action"><b>Student Activity:</b> {phase.student_action}</p>
                        )}

                        {/* Station Rotations Pods */}
                        {phase.pods && (
                          <div className="stations-pod-grid">
                            {phase.pods.map((pod, pIdx) => (
                              <div key={pIdx} className="station-pod-box">
                                <span className="pod-station-tag">{pod.pod_name}</span>
                                <h5>Target: {pod.target_barrier}</h5>
                                <p><b>Activity:</b> {pod.activity}</p>
                                <p><b>Teacher Checkpoint:</b> {pod.teacher_checkpoint}</p>
                                <small><b>Materials:</b> {pod.materials}</small>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* 3D. Indian Contextual Real-World Transfer Tasks */}
          {genMode === 'transfer' && (
            <div className="gen-tool-card">
              <div className="gen-controls-bar">
                <div className="control-group">
                  <label>Contextual Indian Theme</label>
                  <select value={transferTheme} onChange={(e) => setTransferTheme(e.target.value as any)}>
                    <option value="recipes">Festive Culinary: Diwali Sooji Halwa</option>
                    <option value="railways">Infrastructure: Vande Bharat Express Timetable</option>
                    <option value="cricket">Sports Analytics: IPL Match Run Rate</option>
                  </select>
                </div>

                <button
                  type="button"
                  className="btn-primary gen-action-btn"
                  onClick={handleGenerateTransfer}
                  disabled={transferBusy}
                >
                  <RefreshCw size={16} className={transferBusy ? 'spin' : ''} />
                  {transferBusy ? 'Generating Task…' : 'Generate Real-World Task'}
                </button>
              </div>

              {transferTask && (
                <div className="transfer-task-dossier">
                  <div className="task-header">
                    <span className="badge-pill gold">AUTHENTIC REAL-WORLD TRANSFER APPLICATION</span>
                    <h2>{transferTask.title}</h2>
                    <p className="task-context">{transferTask.context}</p>
                  </div>

                  {transferTask.ingredients && (
                    <div className="task-ingredients-box">
                      <h4>Recipe Ingredients (Design for 4 Servings):</h4>
                      <ul>
                        {transferTask.ingredients.map((ing, i) => (
                          <li key={i}>{ing}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="task-problem-box">
                    <h4>The Student Challenge:</h4>
                    <p>{transferTask.problem}</p>
                  </div>

                  <div className="task-solution-box">
                    <h4>Step-by-Step Proportional Solution & Key:</h4>
                    <ol>
                      {transferTask.solution_steps.map((st, i) => (
                        <li key={i}>{st}</li>
                      ))}
                    </ol>
                  </div>

                  {transferTask.pedagogical_outcome && (
                    <div className="task-outcome-strip">
                      <b>Pedagogical Outcome:</b> {transferTask.pedagogical_outcome}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </section>
      )}
    </div>
  );
}

