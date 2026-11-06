import { FormEvent, useCallback, useEffect, useRef, useState } from 'react';
import {
  ArrowRight,
  CheckCircle2,
  Clock3,
  GraduationCap,
  LockKeyhole,
  LogOut,
  Sparkles,
  Users,
  Wifi,
  WifiOff,
  FileText,
  UserPlus,
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
  type StudentDetail,
  type Persona,
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
  InviteStudentsModal,
  JoinClassroomModal,
} from './TeacherModals';
import { LandingPage, CurriculumPage, FlowchartPage, AeoGeoFaqPage } from './Pages';
import { ROUTES, applyPageMeta, tabFromPath, type ActiveTab } from './seo';
import { EnginesHub } from './EnginesHub';
import {
  getLocalizedChapterTitle,
  getLocalizedChapterSummary,
  getLocalizedQuestionPrompt,
  getLocalizedOptionLabel,
  getLocalizedExplanation,
} from './localization';
import {
  fill,
  localisedDuration,
  localisedPlanText,
  misconceptionLabel,
  prerequisiteName,
  prerequisiteRemedy,
  reasonForRoute,
  routeLabel,
  teacherText,
} from './teacherText';

export type { ActiveTab };

type Session = Auth;
const sessionKey = 'prism-session';
const offlineQueueKey = 'prism-offline-attempts';
const langKey = 'prism-language';
const cacheKey = (name: string) => `prism-cache:${name}`;

/** Read-through cache, so already-seen activities still open with no connection. */
function remember<T>(name: string, value: T): T {
  try {
    localStorage.setItem(cacheKey(name), JSON.stringify(value));
  } catch {
    /* A full or blocked store only costs the offline convenience. */
  }
  return value;
}

function recall<T>(name: string): T | null {
  try {
    return JSON.parse(localStorage.getItem(cacheKey(name)) || 'null');
  } catch {
    return null;
  }
}

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
// Topbar (Authenticated Navigation)
// ----------------------------------------------------
function Topbar({
  user,
  lang,
  onLangChange,
  activeTab,
  onTabChange,
  isOffline,
  onToggleOffline,
  queuedCount,
  onSyncQueue,
  onSignOut,
  personas,
  onSelectPersona,
}: {
  user: User;
  lang: Language;
  onLangChange: (lang: Language) => void;
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
  isOffline: boolean;
  onToggleOffline: () => void;
  queuedCount: number;
  onSyncQueue: () => void;
  onSignOut: () => void;
  personas: Persona[];
  onSelectPersona: (email: string) => void;
}) {
  const t = TRANSLATIONS[lang];
  const x = teacherText(lang);

  return (
    <header className="topbar">
      <div className="topbar-content">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ cursor: 'pointer' }} onClick={() => onTabChange('home')}>
            <Brand />
          </div>
          <nav className="site-nav-tabs">
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'home' ? 'active' : ''}`}
              onClick={() => onTabChange('home')}
            >
              {t.navHome}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'curriculum' ? 'active' : ''}`}
              onClick={() => onTabChange('curriculum')}
            >
              {t.navCurriculum}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'faq' ? 'active' : ''}`}
              onClick={() => onTabChange('faq')}
            >
              {t.navFaq}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'flowchart' ? 'active' : ''}`}
              onClick={() => onTabChange('flowchart')}
            >
              {t.navFlowchart}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'engines' ? 'active' : ''}`}
              onClick={() => onTabChange('engines')}
            >
              {t.navEngines}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'app' ? 'active' : ''}`}
              onClick={() => onTabChange('app')}
            >
              {user.role === 'teacher' ? t.navControlRoom : t.navMyLearning}
            </button>
          </nav>
        </div>

        <div className="showcase-actions">
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

          {personas.length > 0 && (
            <select
              className="persona-switcher"
              aria-label={x.demoPersona}
              value={user.email}
              onChange={(e) => onSelectPersona(e.target.value)}
              style={{ fontSize: '12px', padding: '5px 6px', borderRadius: '8px', border: '1px solid #cbd5e1', background: '#fff', maxWidth: '170px' }}
            >
              {!personas.some((persona) => persona.email === user.email) && <option value={user.email}>{user.name}</option>}
              {personas.map((persona) => (
                <option key={persona.id} value={persona.email}>
                  {persona.name} · {routeLabel(persona.route, lang)}
                </option>
              ))}
            </select>
          )}

          {/* Offline Queue Indicator */}
          <button
            type="button"
            className={`net-status-pill ${isOffline ? 'offline' : 'online'}`}
            onClick={onToggleOffline}
            title="Offline mode queues your responses and syncs when connection resumes"
          >
            {isOffline ? <WifiOff size={13} /> : <Wifi size={13} />}
            <span>{isOffline ? t.offlineModeActive : t.onlineSynced}</span>
            {queuedCount > 0 && <span className="badge-pill gold">({queuedCount} {t.pendingQueue})</span>}
          </button>

          {queuedCount > 0 && (
            <button
              type="button"
              className="btn-primary"
              style={{ padding: '5px 10px', fontSize: '11px' }}
              onClick={onSyncQueue}
            >
              {x.syncNow} ({queuedCount})
            </button>
          )}

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
// Authentication Screen
// ----------------------------------------------------
function AuthScreen({
  onAuthenticated,
  lang,
  onLangChange,
  activeTab,
  onTabChange,
  personas,
  onSelectPersona,
}: {
  onAuthenticated: (auth: Session) => void;
  lang: Language;
  onLangChange: (lang: Language) => void;
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
  personas: Persona[];
  onSelectPersona: (email: string) => void;
}) {
  const [mode, setMode] = useState<'sign-in' | 'register'>('sign-in');
  const [role, setRole] = useState<'student' | 'teacher'>('student');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [classroomCode, setClassroomCode] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const t = TRANSLATIONS[lang];
  const x = teacherText(lang);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError('');
    try {
      const result =
        mode === 'sign-in'
          ? await api.login(email, password)
          : await api.register(name, email, password, role, role === 'student' ? classroomCode.trim() : undefined);
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
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ cursor: 'pointer' }} onClick={() => onTabChange('home')}>
            <Brand />
          </div>
          <div className="site-nav-tabs">
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'home' ? 'active' : ''}`}
              onClick={() => onTabChange('home')}
            >
              {t.navHome}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'curriculum' ? 'active' : ''}`}
              onClick={() => onTabChange('curriculum')}
            >
              {t.navCurriculum}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'faq' ? 'active' : ''}`}
              onClick={() => onTabChange('faq')}
            >
              {t.navFaq}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'flowchart' ? 'active' : ''}`}
              onClick={() => onTabChange('flowchart')}
            >
              {t.navFlowchart}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'engines' ? 'active' : ''}`}
              onClick={() => onTabChange('engines')}
            >
              {t.navEngines}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'app' ? 'active' : ''}`}
              onClick={() => onTabChange('app')}
            >
              {t.navSignIn}
            </button>
          </div>
        </div>
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
          <span className="secure">
            <LockKeyhole size={14} /> {t.cbseLabel}
          </span>
        </div>
      </nav>

      <section className="auth-layout">
        <div className="auth-story">
          <span className="eyebrow">{t.boardTag}</span>
          <h1>{t.authHeroHeading}</h1>
          <p>{t.authHeroPara}</p>

          <div className="auth-points">
            <span>
              <CheckCircle2 /> <b>{t.authBullet1Bold}</b> {t.authBullet1}
            </span>
            <span>
              <CheckCircle2 /> <b>{t.authBullet2Bold}</b> {t.authBullet2}
            </span>
            <span>
              <CheckCircle2 /> <b>{t.authBullet3Bold}</b> {t.authBullet3}
            </span>
            <span>
              <CheckCircle2 /> <b>{t.authBullet4Bold}</b> {t.authBullet4}
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

          {mode === 'register' && (
            <>
              <label>
                {t.fullName}
                <input
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder={t.fullNamePlaceholder}
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
              {role === 'student' && (
                <label>
                  {x.classCodeLabel}
                  <input
                    value={classroomCode}
                    onChange={(e) => setClassroomCode(e.target.value.toUpperCase())}
                    placeholder={x.classCodePlaceholder}
                  />
                </label>
              )}
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
              autoComplete="email"
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
              placeholder={t.passwordPlaceholder}
              autoComplete="current-password"
            />
          </label>

          {error && <div className="errorbox">{error}</div>}

          <button type="submit" className="btn-primary" disabled={busy}>
            {busy ? '…' : mode === 'sign-in' ? t.signInBtn : t.createAccountBtn}{' '}
            <ArrowRight size={17} />
          </button>

          {personas.length > 0 && (
            <label>
              {x.demoPersona}
              <select
                value=""
                onChange={(e) => e.target.value && onSelectPersona(e.target.value)}
                aria-label={x.demoPersona}
              >
                <option value="">{x.switchPersona}</option>
                {personas.map((persona) => (
                  <option key={persona.id} value={persona.email}>
                    {persona.name} · {routeLabel(persona.route, lang)}
                  </option>
                ))}
              </select>
            </label>
          )}
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
  syncVersion,
}: {
  user: User;
  token: string;
  lang: Language;
  isOffline: boolean;
  onQueueAttempt: (item: QueuedAttempt) => void;
  onSignOut: () => void;
  syncVersion: number;
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
  const [lastRoute, setLastRoute] = useState('');
  const [lastEngineReason, setLastEngineReason] = useState('');
  const [showCelebration, setShowCelebration] = useState(false);
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [notice, setNotice] = useState('');
  const t = TRANSLATIONS[lang];
  const x = teacherText(lang);

  const load = () =>
    Promise.all([api.units(), api.progress(token)])
      .then(([catalogue, profile]) => {
        setUnits(remember('units', catalogue));
        setProgress(remember(`progress:${user.id}`, profile));
        setError('');
      })
      .catch((e) => {
        const cachedUnits = recall<Unit[]>('units');
        if (cachedUnits) {
          setUnits(cachedUnits);
          setProgress(recall<Progress[]>(`progress:${user.id}`) || []);
        } else {
          setError(e.message);
        }
      });

  useEffect(() => {
    load();
    // syncVersion: queued answers just reached the server, so scores have changed.
  }, [token, syncVersion]);

  const start = async (unit: Unit, nextStage: 'diagnostic' | 'practice' | 'test' = 'diagnostic') => {
    setError('');
    setFeedback('');
    setAnswer('');
    setIndex(0);
    setShowCelebration(false);
    setSelected(unit);
    setStage(nextStage);
    try {
      const qList = await api.questions(unit.id, nextStage, token);
      setQuestions(remember(`questions:${unit.id}:${nextStage}`, qList));
    } catch (e) {
      const cached = recall<Question[]>(`questions:${unit.id}:${nextStage}`);
      if (cached) {
        setQuestions(cached);
      } else {
        setQuestions([]);
        setError(e instanceof Error ? e.message : 'Unable to load activity');
      }
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
      setLastRoute('');
      setFeedback(`⚡ ${x.queuedOffline}`);
      return;
    }

    try {
      const result = await api.attempt(
        { question_id: question.id, response: answer, stage, submission_id },
        token
      );
      setFeedback(
        `${result.correct ? t.correct : t.keepGoing}${getLocalizedExplanation(question.id, result.explanation || result.feedback, lang)}`
      );
      setLastRoute(result.route || result.profile?.recommendation || '');
      setLastEngineReason(result.reason);

      if (stage === 'test' && result.correct) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 4200);
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
      setLastRoute('');
      setFeedback(`⚡ ${x.queuedNetwork}`);
    }
  };

  const currentProgress = selected && progress.find((item) => item.unit_id === selected.id);
  const route = currentProgress?.recommendation || 'diagnostic';
  const isFractionChapter = selected?.id === 'rational-numbers';
  const barrierLabel = misconceptionLabel(currentProgress?.misconception, lang, currentProgress?.misconception_title);
  const shownReason = lastRoute ? (lang === 'en' ? lastEngineReason : reasonForRoute(lastRoute, x)) : '';
  const genericRoute: Record<string, { banner: string; text: string; tone: string }> = {
    foundation: { banner: x.routeFoundationGeneric, text: x.routeFoundationText, tone: 'foundation' },
    'visual-support': { banner: x.routeVisualGeneric, text: x.routeVisualText, tone: 'visual' },
    'guided-practice': { banner: x.routeGuidedGeneric, text: x.routeGuidedText, tone: 'guided' },
    extension: { banner: x.routeExtensionGeneric, text: x.routeExtensionText, tone: 'extension' },
    test: { banner: x.routeTest, text: x.routeTestText, tone: 'extension' },
    'follow-up': { banner: x.routeFollowUp, text: x.routeFollowUpText, tone: 'guided' },
  };
  const panel = genericRoute[route];
  const gap = currentProgress?.prerequisite_gap;
  const gapName = gap ? prerequisiteName(gap.concept_id, lang, gap.title) : '';
  const gapRemedy = gap ? prerequisiteRemedy(gap.concept_id, lang, gap.remedy) : '';
  // Fraction tools only make sense in the fraction chapter; follow-up and transfer
  // routes have no tool in any chapter.
  const usesFractionTool = isFractionChapter && ['foundation', 'visual-support', 'guided-practice', 'extension'].includes(route);

  if (selected) {
    return (
      <main className="workspace">
        {showCelebration && (
          <div className="celebration-banner" role="status" aria-live="polite">
            <span>🎉</span>
            <div>
              <b>{t.transferVerifiedTitle}</b>
              <p>{t.transferVerifiedDesc}</p>
            </div>
            <CheckCircle2 size={28} style={{ color: '#10b981' }} />
          </div>
        )}
        <section className="learning-view">
          <button className="back" onClick={() => setSelected(null)}>
            ← {t.allChapters}
          </button>

          <div className="lesson-heading">
            <span className={`chapter-dot ${selected.color}`} />
            <div>
              <span className="eyebrow">
                {t.boardTag} · {t.chapterPrefix} {selected.number} · {stage.toUpperCase()}
              </span>
              <h1>{getLocalizedChapterTitle(selected.id, selected.title, lang)}</h1>
              <p>{getLocalizedChapterSummary(selected.id, selected.summary, lang)}</p>
            </div>
          </div>

          {error && <div className="errorbox">{error}</div>}

          <div>
            {/* ADAPT: Differentiated Learning Pod & Interactive Tools */}
            {stage === 'practice' && usesFractionTool && (
              <div className="adaptive-route-container">
                {route === 'visual-support' && (
                  <div className="adaptive-route-banner visual">
                    <div className="route-badge-row">
                      <Sparkles size={14} /> {t.visualSupportBanner}
                    </div>
                    <h3>{x.visualTitle}</h3>
                    <p>
                      {currentProgress?.misconception && currentProgress.misconception !== 'denominator-magnitude'
                        ? fill(x.patternExplanation, { label: barrierLabel })
                        : t.visualSupportExplanation}
                    </p>
                    <VisualFractionBarWorkbench lang={lang} />
                  </div>
                )}

                {route === 'foundation' && (
                  <div className="adaptive-route-banner foundation">
                    <div className="route-badge-row">
                      <Sparkles size={14} /> {t.foundationBanner}
                    </div>
                    <h3>{x.foundationTitle}</h3>
                    <p>{t.foundationExplanation}</p>
                    {gap && (
                      <p><b>{x.weakPrerequisite}</b> {gapName}. {gapRemedy}</p>
                    )}
                    <FoundationStripWorkbench lang={lang} />
                  </div>
                )}

                {route === 'guided-practice' && (
                  <div className="adaptive-route-banner guided">
                    <div className="route-badge-row">
                      <Sparkles size={14} /> {t.guidedPracticeBanner}
                    </div>
                    <h3>{x.guidedTitle}</h3>
                    <p>{t.guidedPracticeExplanation}</p>
                    <GuidedPracticeWorkbench lang={lang} />
                  </div>
                )}

                {route === 'extension' && (
                  <div className="adaptive-route-banner extension">
                    <div className="route-badge-row">
                      <Sparkles size={14} /> {t.extensionBanner}
                    </div>
                    <h3>{x.extensionTitle}</h3>
                    <p>{t.extensionExplanation}</p>
                    <ExtensionRecipeWorkbench lang={lang} />
                  </div>
                )}
              </div>
            )}

            {stage === 'practice' && !usesFractionTool && panel && (
              <div className="adaptive-route-container">
                <div className={`adaptive-route-banner ${panel.tone}`}>
                  <div className="route-badge-row">
                    <Sparkles size={14} /> {panel.banner}
                  </div>
                  {barrierLabel && (
                    <p><b>{x.patternSeen}</b> {barrierLabel}</p>
                  )}
                  {gap && (
                    <p><b>{x.weakPrerequisite}</b> {gapName}</p>
                  )}
                  <p>{panel.text}</p>
                  {(gapRemedy || currentProgress?.misconception_remedy) && (
                    <p><b>{x.whatToTry}</b> {gapRemedy || currentProgress?.misconception_remedy}</p>
                  )}
                </div>
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
                      {t.questionWord} {index + 1} {t.questionMetaOf} {questions.length}
                    </span>
                  </div>

                  <h2>{getLocalizedQuestionPrompt(questions[index].id, questions[index].prompt, lang)}</h2>

                  <div className="answers">
                    {questions[index].options.map((option) => (
                      <button
                        key={option}
                        disabled={!!feedback}
                        className={answer === option ? 'selected' : ''}
                        onClick={() => setAnswer(option)}
                      >
                        {getLocalizedOptionLabel(option, lang)}
                      </button>
                    ))}
                  </div>

                  {feedback ? (
                    <div className="feedback">
                      <p>{feedback}</p>
                      {shownReason && (
                        <p style={{ fontSize: '12px', color: '#047857' }}>
                          <b>{t.diagnosticEngineNote}</b> {shownReason}
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
                <p>{t.loadingActivity}</p>
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
                <b>{t.identifiedBarrier}</b> {barrierLabel}
              </div>
            )}

            <div className="stage-list">
              {(['diagnostic', 'practice', 'test'] as const).map((item, position) => (
                <span
                  key={item}
                  role="button"
                  tabIndex={0}
                  title={x.stageJump}
                  style={{ cursor: 'pointer' }}
                  className={stage === item ? 'current' : ''}
                  onClick={() => start(selected, item)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      start(selected, item);
                    }
                  }}
                >
                  {position + 1}. {item === 'diagnostic' ? t.diagnostic : item === 'practice' ? t.practice : t.test}
                </span>
              ))}
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
            {(() => {
              const h = new Date().getHours();
              return h < 12 ? t.greetingMorning : h < 17 ? t.greetingAfternoon : t.greetingEvening;
            })()}, {user.name.split(' ')[0]}.
          </h1>
          <p>{t.studentHeroSub}</p>
          <div style={{ marginTop: '14px', marginBottom: '14px', display: 'flex', gap: '10px' }}>
            <button
              type="button"
              className="btn-secondary"
              style={{ background: '#fff', fontSize: '13px', padding: '6px 14px' }}
              onClick={() => setShowJoinModal(true)}
            >
              <UserPlus size={15} /> {t.joinClassroomBtn}
            </button>
          </div>
          <div className="hero-stats">
            <span>
              <b>{completed}</b> {t.chaptersStarted}
            </span>
            <span>
              <b>8</b> {t.cbseModulesAvailable}
            </span>
            <span>
              <b>{t.class8NcertRef}</b>
            </span>
          </div>
        </div>
        <div className="hero-mark">
          <Sparkles />
          <span>
            {t.pillarDiagnose}
            <br />
            {t.pillarAdapt}
            <br />
            {t.pillarVerify}
          </span>
        </div>
      </section>

      {error && <div className="page-error">{error}</div>}
      {notice && <div className="feedback" role="status"><p>{notice}</p></div>}

      <section className="catalogue-head">
        <div>
          <span className="eyebrow">{t.courseCatalogueTitle}</span>
          <h2>{t.courseCatalogueSub}</h2>
        </div>
        <span className="catalogue-count">{units.length} {t.learningModulesCount}</span>
      </section>

      <section className="chapter-grid">
        {units.map((unit) => {
          const item = progress.find((p) => p.unit_id === unit.id);
          const hasEvidence = item && item.evidence_count > 0;
          return (
            <article className="chapter-card" key={unit.id}>
              <div className="chapter-card-top">
                <span className={`chapter-dot ${unit.color}`} />
                <span>{t.chapterPrefix} {unit.number.toString().padStart(2, '0')}</span>
              </div>
              <h3>{getLocalizedChapterTitle(unit.id, unit.title, lang)}</h3>
              <p>{getLocalizedChapterSummary(unit.id, unit.summary, lang)}</p>
              <div className="card-bottom">
                <span>
                  <Clock3 size={14} /> {unit.minutes} {lang === 'hi' ? 'मिनट' : lang === 'te' ? 'నిమి' : 'min'}
                </span>
                <span>
                  {hasEvidence ? `${Math.round(item.mastery * 100)}% ${t.masteryLabel}` : t.notStarted}
                </span>
              </div>
              <button
                type="button"
                onClick={() => start(unit, hasEvidence ? 'practice' : 'diagnostic')}
              >
                {hasEvidence ? t.continueChapter : t.startChapter} <ArrowRight size={16} />
              </button>
            </article>
          );
        })}
      </section>

      {showJoinModal && (
        <JoinClassroomModal
          lang={lang}
          onJoin={async (code) => {
            await api.joinClassroom(code, token);
            setNotice(fill(x.joined, { code }));
            load();
          }}
          onClose={() => setShowJoinModal(false)}
        />
      )}
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
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [recompiling, setRecompiling] = useState(false);
  const [notice, setNotice] = useState('');
  const [chapterFilter, setChapterFilter] = useState<string>('all');
  const t = TRANSLATIONS[lang];
  const x = teacherText(lang);

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

  const handleRecompile = async () => {
    setRecompiling(true);
    try {
      await api.recompileInterventions(token);
      await loadWorkspace();
      setNotice(x.recompileDone);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to recompile interventions');
    } finally {
      setRecompiling(false);
    }
  };

  const learnerName = (code: string) => data?.learners.find((l) => l.code === code)?.name || code;
  const allPlans = data?.interventions || [];
  const chapterTabs = Array.from(
    new Map(allPlans.filter((plan) => plan.unit_id).map((plan) => [plan.unit_id as string, plan])).values()
  );
  const visiblePlans = chapterFilter === 'all' ? allPlans : allPlans.filter((plan) => plan.unit_id === chapterFilter);
  const statusLabel = (status: Plan['status']) =>
    status === 'approved' ? x.statusApproved : status === 'modified' ? x.statusModified : status === 'rejected' ? x.statusRejected : x.statusProposed;
  const confidenceLabel = (level: string) =>
    level === 'high' ? x.confHigh : level === 'review' ? x.confReview : x.confModerate;
  const activeChapter = chapterTabs.find((plan) => plan.unit_id === chapterFilter);

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
            className="btn-secondary"
            style={{ background: '#f5f3ff', color: '#6d28d9', borderColor: '#c4b5fd' }}
            onClick={() => setShowInviteModal(true)}
            title="Invite real students to join this class"
          >
            <UserPlus size={16} /> {t.enrollStudentsBtn} ({data?.class_code || '8A-CBSE'})
          </button>
          <button
            type="button"
            className="btn-secondary"
            style={{ background: '#ecfdf5', color: '#047857', borderColor: '#a7f3d0' }}
            onClick={handleRecompile}
            disabled={recompiling}
            title="Re-run deterministic rules engine on latest student attempts"
          >
            <Sparkles size={16} /> {recompiling ? t.recompilingText : t.recompilePodsBtn}
          </button>
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
      {notice && <div className="feedback" role="status"><p>{notice}</p></div>}

      {/* Professional Metrics */}
      <section className="metric-grid professional">
        <article>
          <span>{t.activeLearners}</span>
          <b>{data?.learners.length || 0}</b>
          <small>{t.enrolledInClass}</small>
        </article>
        <article>
          <span>{t.averageMastery}</span>
          <b>{avgMastery}%</b>
          <small>{t.acrossActiveModules}</small>
        </article>
        <article>
          <span>{t.evidenceCollected}</span>
          <b>{totalEvidence}</b>
          <small>{t.observableResponses}</small>
        </article>
      </section>

      {/* 45-Minute Lesson Timeline */}
      <LessonTimelineSchedule lang={lang} />

      {/* Teacher Columns: Intervention Compiler & Learner Pulse */}
      <section className="teacher-columns">
        {/* Left Column: Teacher Intervention Compiler */}
        <article className="teacher-panel">
          <div className="panel-title">
            <div>
              <span className="eyebrow">{t.interventionReview}</span>
              <h2>{t.teacherApprovedGroups}</h2>
            </div>
            <span className="badge-pill purple">{t.decisionSupportActive}</span>
          </div>

          {chapterTabs.length > 1 && (
            <div className="student-pill-list" style={{ marginBottom: '12px' }}>
              <button
                type="button"
                className={`student-select-pill ${chapterFilter === 'all' ? 'assigned' : 'unassigned'}`}
                onClick={() => setChapterFilter('all')}
              >
                {x.allChapters}
              </button>
              {chapterTabs.map((plan) => (
                <button
                  type="button"
                  key={plan.unit_id}
                  className={`student-select-pill ${chapterFilter === plan.unit_id ? 'assigned' : 'unassigned'}`}
                  onClick={() => setChapterFilter(plan.unit_id as string)}
                >
                  {x.chapterShort} {plan.chapter_number}: {getLocalizedChapterTitle(plan.unit_id as string, plan.chapter_title || '', lang)}
                </button>
              ))}
            </div>
          )}

          {!data ? (
            <p>{t.loadingInterventions}</p>
          ) : visiblePlans.length > 0 ? (
            visiblePlans.map((plan) => (
              <section key={plan.id} className={`plan-card ${plan.status}`}>
                <div className="plan-card-header">
                  <span className={`badge-pill ${plan.confidence === 'high' ? 'green' : 'gold'}`}>
                    {x.confidence}: {confidenceLabel(plan.confidence)}
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
                    {statusLabel(plan.status)}
                  </span>
                </div>

                <span className="eyebrow">
                  {x.chapterShort} {plan.chapter_number} · {routeLabel(plan.group_key, lang)}
                </span>
                <h3>{localisedPlanText(plan.barrier, lang)}</h3>
                <p>{fill(x.podEvidence, { n: plan.student_codes.length })}</p>

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
                          title={c}
                        >
                          {learnerName(c)}
                        </button>
                      ))}
                    </div>
                  </span>
                  <span>
                    <b>{t.suggestedActivity}</b>
                    {localisedPlanText(plan.activity, lang)}
                  </span>
                  <span>
                    <b>{t.timeAllocation}</b>
                    {localisedDuration(plan.duration, lang)}
                  </span>
                </div>

                {((plan.suggested_add?.length || 0) > 0 || (plan.suggested_remove?.length || 0) > 0) && (
                  <div className="plan-notes-banner" role="note">
                    <b>{x.engineSuggests}</b>{' '}
                    {(plan.suggested_add?.length || 0) > 0 && (
                      <span>{x.suggestAdd}: {plan.suggested_add?.map(learnerName).join(', ')}. </span>
                    )}
                    {(plan.suggested_remove?.length || 0) > 0 && (
                      <span>{x.suggestRemove}: {plan.suggested_remove?.map(learnerName).join(', ')}. </span>
                    )}
                    <small style={{ display: 'block', marginTop: '4px' }}>{x.suggestHint}</small>
                  </div>
                )}

                {plan.teacher_notes && (
                  <div className="plan-notes-banner">
                    <b>{t.teacherNotes}</b> {plan.teacher_notes}
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
                    {t.dismiss}
                  </button>
                </div>
              </section>
            ))
          ) : (
            <p>{x.noPlans}</p>
          )}
        </article>

        {/* Right Column: Classroom Evidence Pulse */}
        <article className="teacher-panel learner-panel">
          <div className="panel-title">
            <div>
              <span className="eyebrow">{x.evidencePulse}</span>
              <h2>{t.currentClassView}</h2>
            </div>
            <span className="badge-pill teal">{t.clickToInspect}</span>
          </div>

          <div className="learner-list">
            {data?.learners.map((learner) => (
              <div
                key={learner.code}
                onClick={() => handleInspectStudent(learner.code)}
                title={x.dossierEyebrow}
              >
                <span className="learner-avatar">{learner.name.slice(0, 1)}</span>
                <div>
                  <b>{learner.name}</b>
                  <small>
                    {learner.focus_chapter_number ? `${x.chapterShort} ${learner.focus_chapter_number} · ` : ''}
                    {learner.evidence_count} {t.evidencePoints}
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
                      {misconceptionLabel(learner.misconception, lang, learner.misconception_title)}
                    </span>
                  )}
                  {!learner.misconception && learner.prerequisite_gap && (
                    <span
                      style={{
                        display: 'inline-block',
                        background: '#fff7ed',
                        color: '#9a3412',
                        fontSize: '10px',
                        fontWeight: 700,
                        padding: '1px 5px',
                        borderRadius: '4px',
                        marginTop: '2px',
                      }}
                    >
                      {x.weakPrerequisite} {prerequisiteName(learner.prerequisite_gap.concept_id, lang, learner.prerequisite_gap.title)}
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
          plans={visiblePlans}
          classCode={data.class_code}
          teacherName={data.teacher_name || user.name}
          learners={data.learners}
          lang={lang}
          chapterLabel={
            activeChapter
              ? `${x.chapterShort} ${activeChapter.chapter_number}: ${getLocalizedChapterTitle(activeChapter.unit_id as string, activeChapter.chapter_title || '', lang)}`
              : chapterTabs.length === 1
              ? `${x.chapterShort} ${chapterTabs[0].chapter_number}: ${getLocalizedChapterTitle(chapterTabs[0].unit_id as string, chapterTabs[0].chapter_title || '', lang)}`
              : undefined
          }
          onClose={() => setShowPrintModal(false)}
        />
      )}

      {/* Invite Students Real Data Modal */}
      {showInviteModal && data && (
        <InviteStudentsModal
          classCode={data.class_code}
          lang={lang}
          onClose={() => setShowInviteModal(false)}
        />
      )}
    </main>
  );
}

// ----------------------------------------------------
// Public Header for Unauthenticated Visitors
// ----------------------------------------------------
function PublicHeader({
  lang,
  onLangChange,
  activeTab,
  onTabChange,
}: {
  lang: Language;
  onLangChange: (lang: Language) => void;
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
}) {
  const t = TRANSLATIONS[lang];

  return (
    <header className="topbar">
      <div className="topbar-content">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ cursor: 'pointer' }} onClick={() => onTabChange('home')}>
            <Brand />
          </div>
          <nav className="site-nav-tabs">
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'home' ? 'active' : ''}`}
              onClick={() => onTabChange('home')}
            >
              {t.navHome}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'curriculum' ? 'active' : ''}`}
              onClick={() => onTabChange('curriculum')}
            >
              {t.navCurriculum}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'faq' ? 'active' : ''}`}
              onClick={() => onTabChange('faq')}
            >
              {t.navFaq}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'flowchart' ? 'active' : ''}`}
              onClick={() => onTabChange('flowchart')}
            >
              {t.navFlowchart}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'engines' ? 'active' : ''}`}
              onClick={() => onTabChange('engines')}
            >
              {t.navEngines}
            </button>
            <button
              type="button"
              className={`site-nav-btn ${activeTab === 'app' ? 'active' : ''}`}
              onClick={() => onTabChange('app')}
            >
              {t.navSignIn}
            </button>
          </nav>
        </div>

        <div className="showcase-actions">
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
          <button
            type="button"
            className="btn-primary"
            style={{ padding: '6px 14px', fontSize: '13px' }}
            onClick={() => onTabChange('app')}
          >
            {t.navGetStarted} <ArrowRight size={14} />
          </button>
        </div>
      </div>
    </header>
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

  // Tab state is mirrored into the URL so every page is a real, linkable,
  // crawlable address rather than transient component state.
  const [activeTab, setActiveTabState] = useState<ActiveTab>(() =>
    typeof window === 'undefined' ? 'home' : tabFromPath(window.location.pathname)
  );

  const setActiveTab = useCallback((tab: ActiveTab) => {
    setActiveTabState(tab);
    if (typeof window !== 'undefined' && window.location.pathname !== ROUTES[tab]) {
      window.history.pushState({ tab }, '', ROUTES[tab]);
    }
  }, []);

  // Keep the browser's back and forward buttons working.
  useEffect(() => {
    const onPopState = () => setActiveTabState(tabFromPath(window.location.pathname));
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  // Retarget title, description, canonical and social tags at the active route.
  useEffect(() => {
    applyPageMeta(activeTab);
  }, [activeTab]);
  const [lang, setLangState] = useState<Language>(() => {
    try {
      const saved = localStorage.getItem(langKey);
      return saved === 'hi' || saved === 'te' ? saved : 'en';
    } catch {
      return 'en';
    }
  });
  const setLang = useCallback((next: Language) => {
    setLangState(next);
    try {
      localStorage.setItem(langKey, next);
    } catch {
      /* Remembering the language is a convenience only. */
    }
  }, []);
  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  // Offline is either real (the browser lost the network) or chosen, so a teacher
  // can demonstrate the behaviour without unplugging anything.
  const [manualOffline, setManualOffline] = useState(false);
  const [networkDown, setNetworkDown] = useState(() => typeof navigator !== 'undefined' && navigator.onLine === false);
  useEffect(() => {
    const goOffline = () => setNetworkDown(true);
    const goOnline = () => setNetworkDown(false);
    window.addEventListener('offline', goOffline);
    window.addEventListener('online', goOnline);
    return () => {
      window.removeEventListener('offline', goOffline);
      window.removeEventListener('online', goOnline);
    };
  }, []);
  const isOffline = manualOffline || networkDown;

  // The queue belongs to one account. Classroom devices are shared, and one shared
  // queue would submit a previous learner's answers under the next learner's name.
  const userId = session?.user.id;
  const queueKey = userId ? `${offlineQueueKey}:${userId}` : '';
  const [offlineQueue, setOfflineQueue] = useState<QueuedAttempt[]>([]);
  useEffect(() => {
    if (!queueKey) {
      setOfflineQueue([]);
      return;
    }
    try {
      setOfflineQueue(JSON.parse(localStorage.getItem(queueKey) || '[]'));
    } catch {
      setOfflineQueue([]);
    }
  }, [queueKey]);
  const saveQueue = useCallback(
    (items: QueuedAttempt[]) => {
      if (!queueKey) return;
      if (items.length) localStorage.setItem(queueKey, JSON.stringify(items));
      else localStorage.removeItem(queueKey);
    },
    [queueKey]
  );

  const [syncNotice, setSyncNotice] = useState('');
  const [syncVersion, setSyncVersion] = useState(0);
  const syncing = useRef(false);

  const [personas, setPersonas] = useState<Persona[]>([]);
  useEffect(() => {
    // Returns 404 when PRISM_DEMO_MODE=0, in which case no switcher is offered.
    api.personas().then(setPersonas).catch(() => setPersonas([]));
  }, []);

  const signOut = () => {
    localStorage.removeItem(sessionKey);
    setSession(null);
    setActiveTab('app');
  };

  const selectPersona = async (email: string) => {
    try {
      const res = await api.login(email, 'PrismDemo!2026');
      localStorage.setItem(sessionKey, JSON.stringify(res));
      setSession(res);
      setActiveTab('app');
    } catch (e) {
      console.error('Persona login error:', e);
    }
  };

  const handleQueueAttempt = (item: QueuedAttempt) => {
    setOfflineQueue((current) => {
      const updated = [...current, item];
      saveQueue(updated);
      return updated;
    });
  };

  /**
   * Sends queued answers oldest first and forgets each one only once the server has
   * it. Stopping part-way is safe: every item keeps its submission_id, so replaying
   * one that actually arrived is answered as a duplicate rather than scored twice.
   */
  const syncOfflineQueue = useCallback(async () => {
    if (!session || syncing.current) return;
    syncing.current = true;
    const pending = [...offlineQueue];
    let sent = 0;
    try {
      for (const item of pending) {
        await api.attempt(
          {
            question_id: item.question_id,
            response: item.response,
            stage: item.stage,
            submission_id: item.submission_id,
          },
          session.access_token
        );
        sent += 1;
        const remaining = pending.slice(sent);
        saveQueue(remaining);
        setOfflineQueue(remaining);
      }
      if (sent > 0) {
        setSyncNotice(fill(teacherText(lang).syncDone, { n: sent }));
        setSyncVersion((version) => version + 1);
      }
    } catch {
      setSyncNotice(teacherText(lang).syncRetry);
    } finally {
      syncing.current = false;
    }
  }, [session, offlineQueue, saveQueue, lang]);

  // Reconnecting is all it takes; nobody should have to remember to press Sync.
  useEffect(() => {
    if (isOffline || !session || offlineQueue.length === 0) return;
    syncOfflineQueue();
    const retry = window.setInterval(syncOfflineQueue, 20000);
    return () => window.clearInterval(retry);
  }, [isOffline, session, offlineQueue.length, syncOfflineQueue]);

  useEffect(() => {
    if (!syncNotice) return;
    const timer = window.setTimeout(() => setSyncNotice(''), 6000);
    return () => window.clearTimeout(timer);
  }, [syncNotice]);

  if (!session) {
    return (
      <>
        {activeTab === 'app' ? (
          <AuthScreen
            onAuthenticated={(s) => {
              setSession(s);
              setActiveTab('app');
            }}
            lang={lang}
            onLangChange={setLang}
            activeTab={activeTab}
            onTabChange={setActiveTab}
            personas={personas}
            onSelectPersona={selectPersona}
          />
        ) : (
          <>
            <PublicHeader
              lang={lang}
              onLangChange={setLang}
              activeTab={activeTab}
              onTabChange={setActiveTab}
            />
            {activeTab === 'home' && (
              <LandingPage
                lang={lang}
                onLaunchApp={() => setActiveTab('app')}
              />
            )}
            {activeTab === 'curriculum' && (
              <CurriculumPage lang={lang} onLaunchApp={() => setActiveTab('app')} />
            )}
            {activeTab === 'flowchart' && <FlowchartPage />}
            {activeTab === 'faq' && <AeoGeoFaqPage lang={lang} />}
            {activeTab === 'engines' && (
              <EnginesHub lang={lang} onNavigateToCurriculum={() => setActiveTab('curriculum')} />
            )}
          </>
        )}
      </>
    );
  }

  return (
    <>
      <Topbar
        user={session.user}
        lang={lang}
        onLangChange={setLang}
        activeTab={activeTab}
        onTabChange={setActiveTab}
        isOffline={isOffline}
        onToggleOffline={() => setManualOffline(!manualOffline)}
        queuedCount={offlineQueue.length}
        onSyncQueue={syncOfflineQueue}
        onSignOut={signOut}
        personas={personas}
        onSelectPersona={selectPersona}
      />

      {syncNotice && (
        <div className="feedback" role="status" style={{ margin: '12px auto', maxWidth: '1180px' }}>
          <p>{syncNotice}</p>
        </div>
      )}

      {activeTab === 'home' && (
        <LandingPage
          lang={lang}
          onLaunchApp={() => setActiveTab('app')}
        />
      )}
      {activeTab === 'curriculum' && (
        <CurriculumPage lang={lang} onLaunchApp={() => setActiveTab('app')} />
      )}
      {activeTab === 'flowchart' && <FlowchartPage />}
      {activeTab === 'faq' && <AeoGeoFaqPage lang={lang} />}
      {activeTab === 'engines' && (
        <EnginesHub lang={lang} onNavigateToCurriculum={() => setActiveTab('curriculum')} />
      )}
      {activeTab === 'app' && (
        session.user.role === 'teacher' ? (
          <TeacherHome
            key={session.user.id}
            user={session.user}
            token={session.access_token}
            lang={lang}
            onSignOut={signOut}
          />
        ) : (
          <StudentHome
            key={session.user.id}
            user={session.user}
            token={session.access_token}
            lang={lang}
            isOffline={isOffline}
            onQueueAttempt={handleQueueAttempt}
            onSignOut={signOut}
            syncVersion={syncVersion}
          />
        )
      )}
    </>
  );
}
