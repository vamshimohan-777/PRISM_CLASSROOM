import { FormEvent, useEffect, useState } from 'react';
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Clock3,
  GraduationCap,
  LayoutDashboard,
  LockKeyhole,
  LogOut,
  RotateCcw,
  Sparkles,
  Users,
  Wifi,
  WifiOff,
  Globe2,
  FileText,
  UserCheck,
  ChevronRight,
  Shield,
  Layers,
} from 'lucide-react';
import {
  api,
  type Auth,
  type Plan,
  type Progress,
  type Question,
  type Unit,
  type User,
  type WorkspaceData,
  type Persona,
  type StudentDetail,
  type LearnerSummary,
} from './api';
import { Language, TRANSLATIONS } from './translations';
import {
  VisualFractionBarWorkbench,
  FoundationStripWorkbench,
  GuidedPracticeWorkbench,
  ExtensionRecipeWorkbench,
} from './InteractiveTools';
import {
  EditPlanModal,
  StudentDossierModal,
  PrintPlanModal,
  LessonTimelineSchedule,
} from './TeacherModals';
import { ProjectOverviewModal } from './ProjectOverviewModal';

type Session = Auth;
const sessionKey = 'prism-session';
const offlineQueueKey = 'prism-offline-attempts';

interface QueuedAttempt {
  question_id: string;
  response: string;
  stage: 'diagnostic' | 'practice' | 'test';
  submission_id: string;
  unit_id: string;
  timestamp: string;
}

function Brand() {
  return (
    <div className="brand">
      <span className="logo">P</span>
      <span>PRISM</span>
      <small>CLASSROOM</small>
    </div>
  );
}

// ----------------------------------------------------
// Topbar
// ----------------------------------------------------
function Topbar({
  user,
  lang,
  onLangChange,
  isOffline,
  onToggleOffline,
  queuedCount,
  onSyncQueue,
  onResetDemo,
  onOpenTour,
  onSelectPersona,
  onSignOut,
}: {
  user: User;
  lang: Language;
  onLangChange: (lang: Language) => void;
  isOffline: boolean;
  onToggleOffline: () => void;
  queuedCount: number;
  onSyncQueue: () => void;
  onResetDemo: () => void;
  onOpenTour: () => void;
  onSelectPersona: (email: string) => void;
  onSignOut: () => void;
}) {
  const t = TRANSLATIONS[lang];

  return (
    <header className="topbar">
      <div className="topbar-content">
        <Brand />

        <div className="showcase-actions">
          {/* Switch between the seeded demo accounts without signing out */}
          <div className="persona-switcher" title="Switch demo account">
            <span className="persona-label">Persona:</span>
            <button
              type="button"
              className={`persona-btn ${user.student_code === 'STU-VISUAL' ? 'active' : ''}`}
              onClick={() => onSelectPersona('student@prism.demo')}
              title="Aarav: Denominator Misconception (Visual Route)"
            >
              Aarav (Visual)
            </button>
            <button
              type="button"
              className={`persona-btn ${user.student_code === 'STU-FOUNDATION' ? 'active' : ''}`}
              onClick={() => onSelectPersona('diya@prism.demo')}
              title="Diya: Prerequisite Gap (Foundation Route)"
            >
              Diya (Foundation)
            </button>
            <button
              type="button"
              className={`persona-btn ${user.student_code === 'STU-CALC' ? 'active' : ''}`}
              onClick={() => onSelectPersona('kabir@prism.demo')}
              title="Kabir: Calculation Slips (Guided Route)"
            >
              Kabir (Guided)
            </button>
            <button
              type="button"
              className={`persona-btn ${user.student_code === 'STU-EXTEND' ? 'active' : ''}`}
              onClick={() => onSelectPersona('meera@prism.demo')}
              title="Meera: High Mastery (Recipe Lab Route)"
            >
              Meera (Extension)
            </button>
            <button
              type="button"
              className={`persona-btn ${user.role === 'teacher' ? 'active' : ''}`}
              onClick={() => onSelectPersona('teacher@prism.demo')}
              title="Ms. Ananya: Teacher Control Room & Intervention Compiler"
            >
              Ms. Ananya (Teacher)
            </button>
          </div>

          {/* Multilingual Switcher */}
          <div className="lang-toggle">
            <button
              type="button"
              className={`lang-btn ${lang === 'en' ? 'active' : ''}`}
              onClick={() => onLangChange('en')}
            >
              EN
            </button>
            <button
              type="button"
              className={`lang-btn ${lang === 'hi' ? 'active' : ''}`}
              onClick={() => onLangChange('hi')}
            >
              हिंदी
            </button>
            <button
              type="button"
              className={`lang-btn ${lang === 'te' ? 'active' : ''}`}
              onClick={() => onLangChange('te')}
            >
              తెలుగు
            </button>
          </div>

          {/* Simulated Offline Toggle & Sync Queue */}
          <button
            type="button"
            className={`net-status-pill ${isOffline ? 'offline' : 'online'}`}
            onClick={onToggleOffline}
            title="Click to toggle Simulated Offline mode (tests local queueing & syncing)"
          >
            {isOffline ? <WifiOff size={13} /> : <Wifi size={13} />}
            <span>{isOffline ? 'Simulated Offline' : 'Online'}</span>
            {queuedCount > 0 && <span className="badge-pill gold">({queuedCount} queued)</span>}
          </button>

          {queuedCount > 0 && (
            <button
              type="button"
              className="btn-primary"
              style={{ padding: '5px 10px', fontSize: '11px' }}
              onClick={onSyncQueue}
            >
              Sync ({queuedCount})
            </button>
          )}

          {/* Architecture / Tour Modal */}
          <button type="button" className="tour-btn" onClick={onOpenTour}>
            <Sparkles size={14} /> About PRISM
          </button>

          {/* Reset Demo */}
          <button
            type="button"
            className="btn-reset-demo"
            onClick={onResetDemo}
            title="Reset demo data to initial pristine archetypes"
          >
            <RotateCcw size={14} /> Reset
          </button>

          {/* Sign Out */}
          <button type="button" className="btn-secondary" style={{ padding: '6px 12px', fontSize: '12px' }} onClick={onSignOut}>
            <LogOut size={14} /> {t.signOut}
          </button>
        </div>
      </div>
    </header>
  );
}

// ----------------------------------------------------
// Authentication and demo sign-in
// ----------------------------------------------------
function AuthScreen({
  onAuthenticated,
  lang,
  onLangChange,
  onOpenTour,
}: {
  onAuthenticated: (auth: Session) => void;
  lang: Language;
  onLangChange: (lang: Language) => void;
  onOpenTour: () => void;
}) {
  const [mode, setMode] = useState<'sign-in' | 'register'>('sign-in');
  const [role, setRole] = useState<'student' | 'teacher'>('student');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('student@prism.demo');
  const [password, setPassword] = useState('PrismDemo!2026');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const t = TRANSLATIONS[lang];

  const quickLogin = async (targetEmail: string) => {
    setBusy(true);
    setError('');
    try {
      const result = await api.login(targetEmail, 'PrismDemo!2026');
      localStorage.setItem(sessionKey, JSON.stringify(result));
      onAuthenticated(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to log in.');
    } finally {
      setBusy(false);
    }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError('');
    try {
      const result =
        mode === 'sign-in'
          ? await api.login(email, password)
          : await api.register(name, email, password, role);
      localStorage.setItem(sessionKey, JSON.stringify(result));
      onAuthenticated(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to continue.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="auth-page">
      <nav>
        <Brand />
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <div className="lang-toggle">
            <button
              type="button"
              className={`lang-btn ${lang === 'en' ? 'active' : ''}`}
              onClick={() => onLangChange('en')}
            >
              EN
            </button>
            <button
              type="button"
              className={`lang-btn ${lang === 'hi' ? 'active' : ''}`}
              onClick={() => onLangChange('hi')}
            >
              हिंदी
            </button>
            <button
              type="button"
              className={`lang-btn ${lang === 'te' ? 'active' : ''}`}
              onClick={() => onLangChange('te')}
            >
              తెలుగు
            </button>
          </div>
          <button type="button" className="tour-btn" onClick={onOpenTour}>
            <Sparkles size={14} /> About PRISM
          </button>
          <span className="secure">
            <LockKeyhole size={14} /> CBSE Mathematics 2026–27
          </span>
        </div>
      </nav>

      <section className="auth-layout">
        <div className="auth-story">
          <span className="eyebrow">{t.boardTag}</span>
          <h1>Misconception-aware learning that keeps teachers at the centre.</h1>
          <p>
            PRISM bridges the gap between student diagnostic evidence and teacher classroom action
            using transparent rules, interactive visual tools, and an editable Intervention Compiler.
          </p>

          <div className="auth-points">
            <span>
              <CheckCircle2 /> <b>Transparent Rules Engine:</b> every recommendation names the rule and evidence behind it.
            </span>
            <span>
              <CheckCircle2 /> <b>3-Part Adaptation:</b> Visual learn, scaffolded solve, independent transfer test.
            </span>
            <span>
              <CheckCircle2 /> <b>Teacher Intervention Compiler:</b> Turns learner evidence into editable pod plans.
            </span>
            <span>
              <CheckCircle2 /> <b>Built for Indian Classrooms:</b> English, Hindi & Telugu with offline queueing.
            </span>
          </div>
        </div>

        <form className="auth-card" onSubmit={submit}>
          <div className="auth-switch">
            <button
              type="button"
              className={mode === 'sign-in' ? 'active' : ''}
              onClick={() => setMode('sign-in')}
            >
              {t.signIn}
            </button>
            <button
              type="button"
              className={mode === 'register' ? 'active' : ''}
              onClick={() => setMode('register')}
            >
              {t.createAccount}
            </button>
          </div>

          <h2>{mode === 'sign-in' ? t.welcomeBack : t.createWorkspace}</h2>
          <p>{t.welcomeSub}</p>

          {/* Quick Demo Persona Launcher */}
          {mode === 'sign-in' && (
            <div className="persona-quick-grid">
              <span className="eyebrow">ONE-CLICK HACKATHON DEMO PERSONAS</span>
              <button
                type="button"
                className="quick-persona-card"
                onClick={() => quickLogin('student@prism.demo')}
              >
                <div>
                  <b>Aarav Sharma (Student)</b>
                  <small>Denominator Misconception → Visual Fraction Bar Route</small>
                </div>
                <ChevronRight size={16} />
              </button>
              <button
                type="button"
                className="quick-persona-card"
                onClick={() => quickLogin('diya@prism.demo')}
              >
                <div>
                  <b>Diya Patel (Student)</b>
                  <small>Prerequisite Gap → Equal-Parts Foundation Route</small>
                </div>
                <ChevronRight size={16} />
              </button>
              <button
                type="button"
                className="quick-persona-card"
                onClick={() => quickLogin('kabir@prism.demo')}
              >
                <div>
                  <b>Kabir Verma (Student)</b>
                  <small>Calculation Slips → Scaffolded Practice Route</small>
                </div>
                <ChevronRight size={16} />
              </button>
              <button
                type="button"
                className="quick-persona-card"
                onClick={() => quickLogin('meera@prism.demo')}
              >
                <div>
                  <b>Meera Iyer (Student)</b>
                  <small>Demonstrated Mastery → Recipe Scaling Extension Route</small>
                </div>
                <ChevronRight size={16} />
              </button>
              <button
                type="button"
                className="quick-persona-card"
                onClick={() => quickLogin('teacher@prism.demo')}
              >
                <div>
                  <b>Ms. Ananya (Teacher)</b>
                  <small>Control Room · Teacher Intervention Compiler & Grouping</small>
                </div>
                <ChevronRight size={16} />
              </button>
            </div>
          )}

          {mode === 'register' && (
            <>
              <label>
                {t.fullName}
                <input
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your full name"
                />
              </label>
              <div className="role-select">
                <button
                  type="button"
                  className={role === 'student' ? 'selected' : ''}
                  onClick={() => setRole('student')}
                >
                  <GraduationCap /> {t.roleStudent}
                </button>
                <button
                  type="button"
                  className={role === 'teacher' ? 'selected' : ''}
                  onClick={() => setRole('teacher')}
                >
                  <Users /> {t.roleTeacher}
                </button>
              </div>
            </>
          )}

          <label>
            {t.email}
            <input
              required
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@school.edu"
            />
          </label>
          <label>
            {t.password}
            <input
              required
              minLength={8}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>

          {error && <div className="errorbox">{error}</div>}

          <button type="submit" className="btn-primary" disabled={busy}>
            {busy ? 'Please wait…' : mode === 'sign-in' ? 'Sign in with credentials' : 'Create secure account'}{' '}
            <ArrowRight size={17} />
          </button>
        </form>
      </section>
    </main>
  );
}

// ----------------------------------------------------
// Student Adaptive Learning View
// ----------------------------------------------------
function StudentHome({
  user,
  token,
  lang,
  isOffline,
  onQueueAttempt,
  onSignOut,
}: {
  user: User;
  token: string;
  lang: Language;
  isOffline: boolean;
  onQueueAttempt: (item: QueuedAttempt) => void;
  onSignOut: () => void;
}) {
  const [units, setUnits] = useState<Unit[]>([]);
  const [progress, setProgress] = useState<Progress[]>([]);
  const [selected, setSelected] = useState<Unit | null>(null);
  const [stage, setStage] = useState<'diagnostic' | 'practice' | 'test'>('diagnostic');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState('');
  const [error, setError] = useState('');
  const [lastReason, setLastReason] = useState('');
  const [showCelebration, setShowCelebration] = useState(false);
  const t = TRANSLATIONS[lang];

  const load = () =>
    Promise.all([api.units(), api.progress(token)])
      .then(([catalogue, profile]) => {
        setUnits(catalogue);
        setProgress(profile);
      })
      .catch((e) => setError(e.message));

  useEffect(() => {
    load();
  }, [token]);

  const start = async (unit: Unit, nextStage: 'diagnostic' | 'practice' | 'test' = 'diagnostic') => {
    setError('');
    setFeedback('');
    setAnswer('');
    setIndex(0);
    setSelected(unit);
    setStage(nextStage);
    try {
      const qList = await api.questions(unit.id, nextStage, token);
      setQuestions(qList);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unable to load activity');
    }
  };

  const submit = async () => {
    const question = questions[index];
    if (!answer || !question || !selected) return;

    const submission_id = crypto.randomUUID();

    // If simulated offline or offline, queue locally!
    if (isOffline) {
      onQueueAttempt({
        question_id: question.id,
        response: answer,
        stage,
        submission_id,
        unit_id: selected.id,
        timestamp: new Date().toISOString(),
      });
      setFeedback('Saved on this device. It will sync when the connection is back.');
      return;
    }

    try {
      const result = await api.attempt(
        { question_id: question.id, response: answer, stage, submission_id },
        token
      );
      setFeedback(`${result.correct ? t.correct : t.keepGoing}${result.feedback}`);
      setLastReason(result.reason);

      if (stage === 'test' && result.correct) {
        setShowCelebration(true);
      }

      load();
    } catch (e) {
      // Network failed: fallback to queue!
      onQueueAttempt({
        question_id: question.id,
        response: answer,
        stage,
        submission_id,
        unit_id: selected.id,
        timestamp: new Date().toISOString(),
      });
      setFeedback('Connection lost. Your answer is saved on this device and will sync automatically.');
    }
  };

  const currentProgress = selected && progress.find((item) => item.unit_id === selected.id);
  const route = currentProgress?.recommendation || 'guided-practice';

  if (selected) {
    return (
      <main className="workspace">
        <section className="learning-view">
          <button className="back" onClick={() => setSelected(null)}>
            ← {t.allChapters}
          </button>

          <div className="lesson-heading">
            <span className={`chapter-dot ${selected.color}`} />
            <div>
              <span className="eyebrow">
                {t.boardTag} · CHAPTER {selected.number} · {stage.toUpperCase()}
              </span>
              <h1>{selected.title}</h1>
              <p>{selected.summary}</p>
            </div>
          </div>

          {error && <div className="errorbox">{error}</div>}

          <div>
            {/* ADAPT: Differentiated Learning Pod & Interactive Tools */}
            {stage === 'practice' && (
              <div className="adaptive-route-container">
                {route === 'visual-support' && (
                  <div className="adaptive-route-banner visual">
                    <div className="route-badge-row">
                      <Sparkles size={14} /> {t.visualSupportBanner}
                    </div>
                    <h3>Targeted Visual Workbench</h3>
                    <p>{t.visualSupportExplanation}</p>
                    <VisualFractionBarWorkbench lang={lang} />
                  </div>
                )}

                {route === 'foundation' && (
                  <div className="adaptive-route-banner foundation">
                    <div className="route-badge-row">
                      <Sparkles size={14} /> {t.foundationBanner}
                    </div>
                    <h3>Prerequisite Partitioning Tool</h3>
                    <p>{t.foundationExplanation}</p>
                    <FoundationStripWorkbench lang={lang} />
                  </div>
                )}

                {route === 'guided-practice' && (
                  <div className="adaptive-route-banner guided">
                    <div className="route-badge-row">
                      <Sparkles size={14} /> {t.guidedPracticeBanner}
                    </div>
                    <h3>Scaffolded Multiplier Guide</h3>
                    <p>{t.guidedPracticeExplanation}</p>
                    <GuidedPracticeWorkbench lang={lang} />
                  </div>
                )}

                {route === 'extension' && (
                  <div className="adaptive-route-banner extension">
                    <div className="route-badge-row">
                      <Sparkles size={14} /> {t.extensionBanner}
                    </div>
                    <h3>Kitchen Lab Proportion Challenge</h3>
                    <p>{t.extensionExplanation}</p>
                    <ExtensionRecipeWorkbench lang={lang} />
                  </div>
                )}
              </div>
            )}

            {/* Question Panel */}
            <article className="question-panel">
              {questions[index] ? (
                <>
                  <div className="activity-meta">
                    <span>
                      {stage === 'test'
                        ? t.test
                        : stage === 'practice'
                        ? t.practice
                        : t.diagnostic}
                    </span>
                    <span>
                      Question {index + 1} of {questions.length}
                    </span>
                  </div>

                  <h2>{questions[index].prompt}</h2>

                  <div className="answers">
                    {questions[index].options.map((option) => (
                      <button
                        key={option}
                        disabled={!!feedback}
                        className={answer === option ? 'selected' : ''}
                        onClick={() => setAnswer(option)}
                      >
                        {option}
                      </button>
                    ))}
                  </div>

                  {feedback ? (
                    <div className="feedback">
                      <p>{feedback}</p>
                      {lastReason && (
                        <p style={{ fontSize: '12px', color: '#047857' }}>
                          <b>Diagnostic Engine Note:</b> {lastReason}
                        </p>
                      )}
                      <button
                        type="button"
                        className="btn-primary"
                        onClick={() => {
                          if (index + 1 < questions.length) {
                            setIndex(index + 1);
                            setAnswer('');
                            setFeedback('');
                          } else if (stage === 'diagnostic') {
                            start(selected, 'practice');
                          } else if (stage === 'practice') {
                            start(selected, 'test');
                          } else {
                            setSelected(null);
                          }
                        }}
                      >
                        {index + 1 < questions.length
                          ? t.nextQuestion
                          : stage === 'test'
                          ? t.finishChapter
                          : t.continue}{' '}
                        <ArrowRight size={17} />
                      </button>
                    </div>
                  ) : (
                    <button
                      type="button"
                      className="btn-primary"
                      disabled={!answer}
                      onClick={submit}
                    >
                      {t.checkAnswer} <CheckCircle2 size={17} />
                    </button>
                  )}
                </>
              ) : (
                <p>Loading your learning activity…</p>
              )}
            </article>
          </div>

          {/* Learning Aside */}
          <aside className="learning-aside">
            <span className="eyebrow">{t.mastery}</span>
            <b>{Math.round((currentProgress?.mastery || 0) * 100)}%</b>
            <div className="progress-bar">
              <i style={{ width: `${(currentProgress?.mastery || 0) * 100}%` }} />
            </div>
            <p>
              {currentProgress?.evidence_count || 0} {t.evidencePoints}
            </p>

            {currentProgress?.misconception && (
              <div
                style={{
                  background: '#fdf2f8',
                  border: '1px solid #fbcfe8',
                  padding: '8px',
                  borderRadius: '6px',
                  fontSize: '11px',
                  color: '#9d174d',
                  marginTop: '10px',
                }}
              >
                <b>Identified Barrier:</b> {currentProgress.misconception}
              </div>
            )}

            <div className="stage-list">
              <span className={stage === 'diagnostic' ? 'current' : ''}>1. {t.diagnostic}</span>
              <span className={stage === 'practice' ? 'current' : ''}>2. {t.practice}</span>
              <span className={stage === 'test' ? 'current' : ''}>3. {t.test}</span>
            </div>
          </aside>
        </section>
      </main>
    );
  }

  const completed = progress.filter((item) => item.evidence_count > 0).length;

  return (
    <main className="workspace">
      <section className="student-hero">
        <div>
          <span className="eyebrow">{t.boardTag}</span>
          <h1>
            Good afternoon, {user.name.split(' ')[0]}.
          </h1>
          <p>
            Choose a chapter to begin a quick diagnostic, build understanding with adaptive visual
            tools, and verify independent transfer.
          </p>
          <div className="hero-stats">
            <span>
              <b>{completed}</b> chapters started
            </span>
            <span>
              <b>8</b> CBSE modules available
            </span>
            <span>
              <b>Class VIII</b> NCERT reference
            </span>
          </div>
        </div>
        <div className="hero-mark">
          <Sparkles />
          <span>
            Diagnose
            <br />
            Adapt
            <br />
            Verify
          </span>
        </div>
      </section>

      {error && <div className="page-error">{error}</div>}

      <section className="catalogue-head">
        <div>
          <span className="eyebrow">CBSE MATHEMATICS COURSE CATALOGUE</span>
          <h2>Mathematics, one concept at a time.</h2>
        </div>
        <span className="catalogue-count">{units.length} learning modules</span>
      </section>

      <section className="chapter-grid">
        {units.map((unit) => {
          const item = progress.find((p) => p.unit_id === unit.id);
          const hasEvidence = item && item.evidence_count > 0;
          return (
            <article className="chapter-card" key={unit.id}>
              <div className="chapter-card-top">
                <span className={`chapter-dot ${unit.color}`} />
                <span>CHAPTER {unit.number.toString().padStart(2, '0')}</span>
              </div>
              <h3>{unit.title}</h3>
              <p>{unit.summary}</p>
              <div className="card-bottom">
                <span>
                  <Clock3 size={14} /> {unit.minutes} min
                </span>
                <span>
                  {hasEvidence ? `${Math.round(item.mastery * 100)}% mastery` : 'Not started'}
                </span>
              </div>
              <button
                type="button"
                onClick={() => start(unit, hasEvidence ? 'practice' : 'diagnostic')}
              >
                {hasEvidence ? 'Continue chapter' : 'Start chapter'} <ArrowRight size={16} />
              </button>
            </article>
          );
        })}
      </section>
    </main>
  );
}

// ----------------------------------------------------
// Teacher Control Room & Intervention Compiler
// ----------------------------------------------------
function TeacherHome({
  user,
  token,
  lang,
  onSignOut,
}: {
  user: User;
  token: string;
  lang: Language;
  onSignOut: () => void;
}) {
  const [data, setData] = useState<WorkspaceData | null>(null);
  const [error, setError] = useState('');
  const [activeEditPlan, setActiveEditPlan] = useState<Plan | null>(null);
  const [activeDossierStudent, setActiveDossierStudent] = useState<StudentDetail | null>(null);
  const [showPrintModal, setShowPrintModal] = useState(false);
  const t = TRANSLATIONS[lang];

  const loadWorkspace = () =>
    api
      .workspace(token)
      .then(setData)
      .catch((e) => setError(e.message));

  useEffect(() => {
    loadWorkspace();
  }, [token]);

  const totalEvidence = data?.learners.reduce((sum, l) => sum + l.evidence_count, 0) || 0;
  const avgMastery =
    data && data.learners.length > 0
      ? Math.round((data.learners.reduce((s, l) => s + l.mastery, 0) / data.learners.length) * 100)
      : 0;

  const handleApprovePlan = async (planId: number) => {
    try {
      await api.updateIntervention(planId, { status: 'approved' }, token);
      loadWorkspace();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unable to approve plan');
    }
  };

  const handleRejectPlan = async (planId: number) => {
    try {
      await api.updateIntervention(planId, { status: 'rejected' }, token);
      loadWorkspace();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unable to reject plan');
    }
  };

  const handleSavePlanEdit = async (updated: Partial<Plan>) => {
    if (!activeEditPlan) return;
    try {
      await api.updateIntervention(
        activeEditPlan.id,
        {
          activity: updated.activity,
          duration: updated.duration,
          outcome: updated.outcome,
          teacher_notes: updated.teacher_notes,
          status: updated.status || 'modified',
          student_codes: updated.student_codes,
        },
        token
      );
      loadWorkspace();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unable to save modifications');
    }
  };

  const handleInspectStudent = async (code: string) => {
    try {
      const detail = await api.studentDetail(code, token);
      setActiveDossierStudent(detail);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unable to load student dossier');
    }
  };

  return (
    <main className="workspace">
      <section className="teacher-head">
        <div>
          <span className="eyebrow">
            {t.boardTag} · SECTION {data?.class_code || '8A-CBSE'}
          </span>
          <h1>{t.teacherWorkspace}</h1>
          <p>{t.interventionSub}</p>
        </div>

        <div className="teacher-head-actions">
          <button
            type="button"
            className="btn-primary"
            onClick={() => setShowPrintModal(true)}
          >
            <FileText size={16} /> {t.exportPlan}
          </button>
          <button type="button" className="btn-secondary" onClick={loadWorkspace}>
            {t.refreshData}
          </button>
        </div>
      </section>

      {error && <div className="page-error">{error}</div>}

      {/* Professional Metrics */}
      <section className="metric-grid professional">
        <article>
          <span>{t.activeLearners}</span>
          <b>{data?.learners.length || 0}</b>
          <small>Enrolled in Class 8-A</small>
        </article>
        <article>
          <span>Average Concept Mastery</span>
          <b>{avgMastery}%</b>
          <small>Across active learning modules</small>
        </article>
        <article>
          <span>{t.evidenceCollected}</span>
          <b>{totalEvidence}</b>
          <small>Observable student responses</small>
        </article>
      </section>

      {/* 45-Minute Lesson Timeline */}
      <LessonTimelineSchedule />

      {/* Teacher Columns: Intervention Compiler & Learner Pulse */}
      <section className="teacher-columns">
        {/* Left Column: Teacher Intervention Compiler */}
        <article className="teacher-panel">
          <div className="panel-title">
            <div>
              <span className="eyebrow">{t.interventionReview}</span>
              <h2>Suggested Small Groups</h2>
            </div>
            <span className="badge-pill purple">Decision Support Active</span>
          </div>

          {data?.interventions && data.interventions.length > 0 ? (
            data.interventions.map((plan) => (
              <section key={plan.id} className={`plan-card ${plan.status}`}>
                <div className="plan-card-header">
                  <span className={`badge-pill ${plan.confidence === 'high' ? 'green' : 'gold'}`}>
                    {plan.confidence.toUpperCase()} CONFIDENCE
                  </span>
                  <span
                    className={`badge-pill ${
                      plan.status === 'approved'
                        ? 'green'
                        : plan.status === 'modified'
                        ? 'teal'
                        : plan.status === 'rejected'
                        ? 'gray'
                        : 'gold'
                    }`}
                  >
                    {plan.status.toUpperCase()}
                  </span>
                </div>

                <h3>{plan.barrier}</h3>
                <p>{plan.evidence}</p>

                <div className="plan-info">
                  <span>
                    <b>{t.studentsInPod}</b>
                    <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                      {plan.student_codes.map((c) => (
                        <button
                          key={c}
                          type="button"
                          className="badge-pill purple"
                          style={{ cursor: 'pointer', border: 'none' }}
                          onClick={() => handleInspectStudent(c)}
                          title="Click to inspect this learner's dossier"
                        >
                          {c}
                        </button>
                      ))}
                    </div>
                  </span>
                  <span>
                    <b>{t.suggestedActivity}</b>
                    {plan.activity}
                  </span>
                  <span>
                    <b>{t.timeAllocation}</b>
                    {plan.duration}
                  </span>
                </div>

                {plan.teacher_notes && (
                  <div className="plan-notes-banner">
                    <b>Teacher Notes:</b> {plan.teacher_notes}
                  </div>
                )}

                {/* Direct Teacher Intervention Action Bar */}
                <div className="plan-action-bar">
                  <button
                    type="button"
                    className="btn-approve"
                    onClick={() => handleApprovePlan(plan.id)}
                  >
                    <CheckCircle2 size={14} /> {t.approve}
                  </button>
                  <button
                    type="button"
                    className="btn-modify"
                    onClick={() => setActiveEditPlan(plan)}
                  >
                    <Sparkles size={14} /> {t.modify}
                  </button>
                  <button
                    type="button"
                    className="btn-reject"
                    onClick={() => handleRejectPlan(plan.id)}
                  >
                    Dismiss
                  </button>
                </div>
              </section>
            ))
          ) : (
            <p>Loading compiled interventions…</p>
          )}
        </article>

        {/* Right Column: Classroom Evidence Pulse */}
        <article className="teacher-panel learner-panel">
          <div className="panel-title">
            <div>
              <span className="eyebrow">CLASSROOM EVIDENCE PULSE</span>
              <h2>{t.currentClassView}</h2>
            </div>
            <span className="badge-pill teal">Click to inspect</span>
          </div>

          <div className="learner-list">
            {data?.learners.map((learner) => (
              <div
                key={learner.code}
                onClick={() => handleInspectStudent(learner.code)}
                title="Click to view detailed Learner Evidence Dossier"
              >
                <span className="learner-avatar">{learner.name.slice(0, 1)}</span>
                <div>
                  <b>{learner.name}</b>
                  <small>
                    {learner.code} · {learner.evidence_count} evidence points
                  </small>
                  {learner.misconception && (
                    <span
                      style={{
                        display: 'inline-block',
                        background: '#fdf2f8',
                        color: '#9d174d',
                        fontSize: '10px',
                        fontWeight: 700,
                        padding: '1px 5px',
                        borderRadius: '4px',
                        marginTop: '2px',
                      }}
                    >
                      {learner.misconception}
                    </span>
                  )}
                </div>
                <div className="mini-progress">
                  <i style={{ width: `${learner.mastery * 100}%` }} />
                </div>
                <strong>{Math.round(learner.mastery * 100)}%</strong>
              </div>
            ))}
          </div>
        </article>
      </section>

      {/* Edit Plan Modal */}
      {activeEditPlan && (
        <EditPlanModal
          plan={activeEditPlan}
          allLearners={data?.learners || []}
          lang={lang}
          onSave={handleSavePlanEdit}
          onClose={() => setActiveEditPlan(null)}
        />
      )}

      {/* Student Dossier Modal */}
      {activeDossierStudent && (
        <StudentDossierModal
          detail={activeDossierStudent}
          lang={lang}
          onClose={() => setActiveDossierStudent(null)}
        />
      )}

      {/* Printable CBSE Lesson Plan Modal */}
      {showPrintModal && data && (
        <PrintPlanModal
          plans={data.interventions}
          classCode={data.class_code}
          teacherName={data.teacher_name || user.name}
          onClose={() => setShowPrintModal(false)}
        />
      )}
    </main>
  );
}

// ----------------------------------------------------
// Main App Root Component
// ----------------------------------------------------
export default function App() {
  const [session, setSession] = useState<Session | null>(() => {
    try {
      return JSON.parse(localStorage.getItem(sessionKey) || 'null');
    } catch {
      return null;
    }
  });

  const [lang, setLang] = useState<Language>('en');
  const [isOffline, setIsOffline] = useState(false);
  const [offlineQueue, setOfflineQueue] = useState<QueuedAttempt[]>(() => {
    try {
      return JSON.parse(localStorage.getItem(offlineQueueKey) || '[]');
    } catch {
      return [];
    }
  });
  const [showTour, setShowTour] = useState(false);

  const signOut = () => {
    localStorage.removeItem(sessionKey);
    setSession(null);
  };

  const selectPersona = async (email: string) => {
    try {
      const res = await api.login(email, 'PrismDemo!2026');
      localStorage.setItem(sessionKey, JSON.stringify(res));
      setSession(res);
    } catch (e) {
      console.error('Persona login error:', e);
    }
  };

  const handleQueueAttempt = (item: QueuedAttempt) => {
    const updated = [...offlineQueue, item];
    setOfflineQueue(updated);
    localStorage.setItem(offlineQueueKey, JSON.stringify(updated));
  };

  const syncOfflineQueue = async () => {
    if (!session || offlineQueue.length === 0) return;
    // Replay in order and drop each item only once the server has it. The
    // server de-duplicates on submission_id, so a retry after a partial
    // failure cannot double-count an answer.
    let remaining = [...offlineQueue];
    try {
      for (const item of offlineQueue) {
        await api.attempt(
          {
            question_id: item.question_id,
            response: item.response,
            stage: item.stage,
            submission_id: item.submission_id,
          },
          session.access_token
        );
        remaining = remaining.slice(1);
      }
      setIsOffline(false);
    } catch (e) {
      alert('Sync paused: ' + (e instanceof Error ? e.message : 'please check the connection') + '. Unsynced answers are kept.');
    } finally {
      setOfflineQueue(remaining);
      if (remaining.length) localStorage.setItem(offlineQueueKey, JSON.stringify(remaining));
      else localStorage.removeItem(offlineQueueKey);
    }
  };

  // Follow the browser's real connectivity as well as the manual toggle.
  useEffect(() => {
    const goOffline = () => setIsOffline(true);
    const goOnline = () => setIsOffline(false);
    window.addEventListener('offline', goOffline);
    window.addEventListener('online', goOnline);
    return () => {
      window.removeEventListener('offline', goOffline);
      window.removeEventListener('online', goOnline);
    };
  }, []);

  const handleResetDemo = async () => {
    try {
      await api.resetDemo();
      window.location.reload();
    } catch (e) {
      alert('Reset failed: ' + (e instanceof Error ? e.message : ''));
    }
  };

  if (!session) {
    return (
      <>
        <AuthScreen
          onAuthenticated={setSession}
          lang={lang}
          onLangChange={setLang}
          onOpenTour={() => setShowTour(true)}
        />
        {showTour && <ProjectOverviewModal onClose={() => setShowTour(false)} />}
      </>
    );
  }

  return (
    <>
      <Topbar
        user={session.user}
        lang={lang}
        onLangChange={setLang}
        isOffline={isOffline}
        onToggleOffline={() => setIsOffline(!isOffline)}
        queuedCount={offlineQueue.length}
        onSyncQueue={syncOfflineQueue}
        onResetDemo={handleResetDemo}
        onOpenTour={() => setShowTour(true)}
        onSelectPersona={selectPersona}
        onSignOut={signOut}
      />

      {session.user.role === 'teacher' ? (
        <TeacherHome
          user={session.user}
          token={session.access_token}
          lang={lang}
          onSignOut={signOut}
        />
      ) : (
        <StudentHome
          user={session.user}
          token={session.access_token}
          lang={lang}
          isOffline={isOffline}
          onQueueAttempt={handleQueueAttempt}
          onSignOut={signOut}
        />
      )}

      {showTour && <ProjectOverviewModal onClose={() => setShowTour(false)} />}
    </>
  );
}
