import { useState } from 'react';
import { Plan, StudentDetail, LearnerSummary } from './api';
import { Language, TRANSLATIONS } from './translations';
import {
  fill,
  localisedDuration,
  localisedPlanText,
  misconceptionLabel,
  PREREQUISITE_LABELS,
  prerequisiteName,
  routeLabel,
  teacherText,
} from './teacherText';
import {
  getLocalizedChapterTitle,
  getLocalizedExplanation,
  getLocalizedOptionLabel,
  getLocalizedQuestionPrompt,
} from './localization';
import { CheckCircle2, Clock3, AlertCircle, FileText, Printer, X, Sparkles, UserCheck, Shield, Copy, Check, UserPlus } from 'lucide-react';

interface EditPlanModalProps {
  plan: Plan;
  allLearners: LearnerSummary[];
  lang: Language;
  onSave: (updated: Partial<Plan>) => Promise<void>;
  onClose: () => void;
}

export function EditPlanModal({ plan, allLearners, lang, onSave, onClose }: EditPlanModalProps) {
  const [activity, setActivity] = useState(plan.activity);
  const [duration, setDuration] = useState(plan.duration);
  const [outcome, setOutcome] = useState(plan.outcome);
  const [teacherNotes, setTeacherNotes] = useState(plan.teacher_notes || '');
  const [status, setStatus] = useState(plan.status);
  const [selectedStudents, setSelectedStudents] = useState<string[]>(plan.student_codes);
  const [busy, setBusy] = useState(false);
  const t = TRANSLATIONS[lang];
  const x = teacherText(lang);

  const toggleStudent = (code: string) => {
    if (selectedStudents.includes(code)) {
      if (selectedStudents.length > 1) {
        setSelectedStudents(selectedStudents.filter((c) => c !== code));
      }
    } else {
      setSelectedStudents([...selectedStudents, code]);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      await onSave({
        activity,
        duration,
        outcome,
        teacher_notes: teacherNotes,
        status: status === 'proposed' ? 'modified' : status,
        student_codes: selectedStudents,
      });
      onClose();
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-container edit-plan-modal">
        <div className="modal-header">
          <div>
            <span className="eyebrow">{x.editEyebrow}</span>
            <h3>{x.editTitle} {localisedPlanText(plan.barrier, lang)}</h3>
          </div>
          <button className="icon-close" onClick={onClose}><X size={20} /></button>
        </div>

        <form onSubmit={handleSave} className="modal-form">
          <div className="form-group">
            <label>{x.statusDecision}
              <div className="status-selector">
                <button
                  type="button"
                  className={status === 'approved' ? 'active-status approved' : ''}
                  onClick={() => setStatus('approved')}
                >
                  <CheckCircle2 size={16} /> {x.approvePlan}
                </button>
                <button
                  type="button"
                  className={status === 'modified' ? 'active-status modified' : ''}
                  onClick={() => setStatus('modified')}
                >
                  <Sparkles size={16} /> {x.modifiedByTeacher}
                </button>
                <button
                  type="button"
                  className={status === 'rejected' ? 'active-status rejected' : ''}
                  onClick={() => setStatus('rejected')}
                >
                  <X size={16} /> {x.dismissReject}
                </button>
              </div>
            </label>
          </div>

          <div className="form-group">
            <label>{x.activityLabel}
              <textarea
                required
                rows={3}
                value={activity}
                onChange={(e) => setActivity(e.target.value)}
              />
            </label>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{x.timeLabel}
                <select value={duration} onChange={(e) => setDuration(e.target.value)}>
                  <option value="5 min">{x.time5}</option>
                  <option value="10 min">{x.time10}</option>
                  <option value="12 min">{x.time12}</option>
                  <option value="15 min">{x.time15}</option>
                  <option value="20 min">{x.time20}</option>
                </select>
              </label>
            </div>

            <div className="form-group">
              <label>{x.outcomeLabel}
                <input
                  required
                  value={outcome}
                  onChange={(e) => setOutcome(e.target.value)}
                />
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>{x.studentsLabel}
              <div className="student-pill-list">
                {allLearners.map((learner) => {
                  const isAssigned = selectedStudents.includes(learner.code);
                  return (
                    <button
                      type="button"
                      key={learner.code}
                      className={`student-select-pill ${isAssigned ? 'assigned' : 'unassigned'}`}
                      onClick={() => toggleStudent(learner.code)}
                    >
                      <UserCheck size={14} />
                      <span>{learner.name} ({learner.code})</span>
                    </button>
                  );
                })}
              </div>
            </label>
          </div>

          <div className="form-group">
            <label>{t.teacherNotes}:
              <textarea
                rows={2}
                placeholder={x.notesPlaceholder}
                value={teacherNotes}
                onChange={(e) => setTeacherNotes(e.target.value)}
              />
            </label>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              {t.cancel}
            </button>
            <button type="submit" className="btn-primary" disabled={busy}>
              {busy ? x.saving : t.saveChanges}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

interface StudentDossierModalProps {
  detail: StudentDetail | null;
  lang: Language;
  onClose: () => void;
}

export function StudentDossierModal({ detail, lang, onClose }: StudentDossierModalProps) {
  if (!detail) return null;
  const t = TRANSLATIONS[lang];
  const x = teacherText(lang);
  const gapText = (gap?: { concept_id: string; title: string } | null) =>
    gap ? `${x.weakPrerequisite} ${prerequisiteName(gap.concept_id, lang, gap.title)}` : '';
  const barrier = misconceptionLabel(detail.misconception, lang, detail.misconception_title) || gapText(detail.prerequisite_gap);

  return (
    <div className="modal-backdrop">
      <div className="modal-container dossier-modal">
        <div className="modal-header">
          <div className="dossier-id">
            <span className="eyebrow">{x.dossierEyebrow}</span>
            <h3>{detail.name} <small>({detail.code})</small></h3>
            <p className="student-meta-info">{x.classMeta} · {x.emailLabel}: {detail.email}</p>
          </div>
          <button className="icon-close" onClick={onClose}><X size={20} /></button>
        </div>

        <div className="dossier-metrics">
          <div className="dossier-card">
            <span>{x.estMastery}</span>
            <b>{Math.round(detail.mastery * 100)}%</b>
            <div className="mini-progress">
              <i style={{ width: `${detail.mastery * 100}%` }} />
            </div>
          </div>
          <div className="dossier-card">
            <span>{x.evidenceResponses}</span>
            <b>{detail.evidence_count}</b>
            <small>{x.totalAttempts}</small>
          </div>
          <div className="dossier-card">
            <span>{x.diagnosedBarrier}</span>
            <b className="purple-text">{barrier || x.noPersistentError}</b>
            <small>
              {detail.misconception_confidence
                ? `${Math.round(detail.misconception_confidence * 100)}% ${x.ruleConfidence}`
                : x.noLabelYet}
            </small>
          </div>
          <div className="dossier-card">
            <span>{x.recommendedRoute}</span>
            <b className="badge-pill teal">{routeLabel(detail.recommendation, lang)}</b>
            <small>{x.prerequisiteLabel}: {PREREQUISITE_LABELS[detail.prerequisite_status]?.[lang] ?? detail.prerequisite_status}</small>
          </div>
        </div>

        {detail.chapters && detail.chapters.length > 0 && (
          <div className="dossier-history-section">
            <h4>{x.byChapter}</h4>
            <table className="print-plan-table dossier-chapter-table">
              <thead>
                <tr>
                  <th>{x.thChapter}</th>
                  <th>{x.thMastery}</th>
                  <th>{x.thResponses}</th>
                  <th>{x.thBarrier}</th>
                  <th>{x.thRoute}</th>
                </tr>
              </thead>
              <tbody>
                {detail.chapters.map((chapter) => (
                  <tr key={chapter.unit_id}>
                    <td>{x.chapterShort} {chapter.number}: {getLocalizedChapterTitle(chapter.unit_id, chapter.title, lang)}</td>
                    <td>{Math.round(chapter.mastery * 100)}%</td>
                    <td>{chapter.evidence_count}</td>
                    <td>{misconceptionLabel(chapter.misconception, lang, chapter.misconception_title) || gapText(chapter.prerequisite_gap) || '–'}</td>
                    <td>{routeLabel(chapter.recommendation, lang)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="dossier-history-section">
          <h4>{x.historyTitle}</h4>
          <p className="subtext">{x.historySub}</p>

          <div className="attempt-timeline">
            {detail.attempts.length === 0 ? (
              <p className="empty-msg">{x.noAttempts}</p>
            ) : (
              detail.attempts.map((att, idx) => (
                <div key={att.id || idx} className={`attempt-item ${att.correct ? 'correct' : 'incorrect'}`}>
                  <div className="attempt-status-col">
                    {att.correct ? (
                      <CheckCircle2 size={18} className="text-green" />
                    ) : (
                      <AlertCircle size={18} className="text-red" />
                    )}
                    <span className="stage-tag">
                      {att.stage === 'test' ? t.test : att.stage === 'practice' ? t.practice : t.diagnostic}
                    </span>
                  </div>
                  <div className="attempt-detail-col">
                    <p className="attempt-prompt"><b>Q:</b> {getLocalizedQuestionPrompt(att.question_id, att.prompt, lang)}</p>
                    <div className="attempt-answer-row">
                      <span>{x.studentSelected} <b>{getLocalizedOptionLabel(att.response, lang)}</b></span>
                      {!att.correct && (
                        <span className="expected-ans">{x.expected} <b>{getLocalizedOptionLabel(att.expected_answer, lang)}</b></span>
                      )}
                      {att.misconception && (
                        <span className="miscon-pill">{x.triggeredRule} {misconceptionLabel(att.misconception, lang)}</span>
                      )}
                    </div>
                    {att.explanation && (
                      <small className="attempt-exp">💡 {getLocalizedExplanation(att.question_id, att.explanation, lang)}</small>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="modal-footer">
          <div className="safeguard-badge">
            <Shield size={16} />
            <span>{x.safeguard}</span>
          </div>
          <button className="btn-secondary" onClick={onClose}>{t.close}</button>
        </div>
      </div>
    </div>
  );
}

interface PrintPlanModalProps {
  plans: Plan[];
  classCode: string;
  teacherName: string;
  learners?: LearnerSummary[];
  /** The chapter being printed, or undefined when printing all of them. */
  chapterLabel?: string;
  lang: Language;
  onClose: () => void;
}

export function PrintPlanModal({ plans, classCode, teacherName, learners = [], chapterLabel, lang, onClose }: PrintPlanModalProps) {
  const x = teacherText(lang);
  const learnerName = (code: string) => learners.find(l => l.code === code)?.name || code;
  // Dismissed plans are the teacher's "no", so they do not belong on the record of what will happen.
  const printable = plans.filter((plan) => plan.status !== 'rejected');
  return (
    <div className="modal-backdrop">
      <div className="modal-container print-modal">
        <div className="modal-header no-print">
          <div>
            <span className="eyebrow">{x.printEyebrow}</span>
            <h3>{x.printTitle}</h3>
          </div>
          <div className="print-actions">
            <button className="btn-primary" onClick={() => window.print()}>
              <Printer size={16} /> {x.printBtn}
            </button>
            <button className="icon-close" onClick={onClose}><X size={20} /></button>
          </div>
        </div>

        <div className="printable-document">
          <div className="cbse-doc-header">
            <div className="school-title">
              <h2>{x.docOrg}</h2>
              <h3>{x.docSub}</h3>
              <p>{chapterLabel || x.allChaptersDoc}</p>
            </div>
            <div className="doc-meta-grid">
              <div><b>{x.classSection}</b> {classCode}</div>
              <div><b>{x.subjectTeacher}</b> {teacherName}</div>
              <div><b>{x.dateLabel}</b> {new Date().toLocaleDateString(lang === 'hi' ? 'hi-IN' : lang === 'te' ? 'te-IN' : 'en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}</div>
              <div><b>{x.lessonPeriod}</b> {x.minutes45}</div>
            </div>
          </div>

          <table className="print-plan-table">
            <thead>
              <tr>
                <th style={{ width: '18%' }}>{x.thPod}</th>
                <th style={{ width: '20%' }}>{x.thStudents}</th>
                <th style={{ width: '34%' }}>{x.thActivity}</th>
                <th style={{ width: '10%' }}>{x.thDuration}</th>
                <th style={{ width: '18%' }}>{x.thOutcome}</th>
              </tr>
            </thead>
            <tbody>
              {printable.map((plan) => (
                <tr key={plan.id}>
                  <td>
                    <b>{localisedPlanText(plan.barrier, lang)}</b>
                    <br />
                    <small style={{ color: '#666' }}>{routeLabel(plan.group_key, lang)}</small>
                  </td>
                  <td>
                    <b>{plan.student_codes.map(learnerName).join(', ')}</b>
                  </td>
                  <td>
                    {localisedPlanText(plan.activity, lang)}
                    {plan.teacher_notes && (
                      <p style={{ marginTop: '4px', fontStyle: 'italic', color: '#444' }}>
                        {x.noteLabel} {plan.teacher_notes}
                      </p>
                    )}
                  </td>
                  <td><b>{localisedDuration(plan.duration, lang)}</b></td>
                  <td>
                    {localisedPlanText(plan.outcome, lang)}
                    <br />
                    <span className={`status-tag ${plan.status}`}>
                      [{plan.status === 'approved' ? x.statusApproved : plan.status === 'modified' ? x.statusModified : x.statusProposed}]
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="print-signoff">
            <div className="signoff-box">
              <hr />
              <span>{x.sigTeacher}</span>
            </div>
            <div className="signoff-box">
              <hr />
              <span>{x.sigHead}</span>
            </div>
          </div>
          <p style={{ marginTop: '14px', fontSize: '11px', color: '#666' }}>{x.disclaimer}</p>
        </div>
      </div>
    </div>
  );
}

export function LessonTimelineSchedule({ lang }: { lang: Language }) {
  const x = teacherText(lang);
  return (
    <div className="timeline-schedule-card">
      <div className="timeline-header">
        <Clock3 size={18} className="purple-text" />
        <div>
          <h4>{x.tlTitle}</h4>
          <p>{x.tlSub}</p>
        </div>
      </div>

      <div className="timeline-blocks">
        <div className="t-block phase-1" style={{ flex: 2 }}>
          <span className="t-time">00 – 10</span>
          <b>{x.tl1Title}</b>
          <small>{x.tl1Desc}</small>
        </div>
        <div className="t-block phase-2" style={{ flex: 3 }}>
          <span className="t-time">10 – 25</span>
          <b>{x.tl2Title}</b>
          <small>{x.tl2Desc}</small>
        </div>
        <div className="t-block phase-3" style={{ flex: 2 }}>
          <span className="t-time">25 – 35</span>
          <b>{x.tl3Title}</b>
          <small>{x.tl3Desc}</small>
        </div>
        <div className="t-block phase-4" style={{ flex: 2 }}>
          <span className="t-time">35 – 45</span>
          <b>{x.tl4Title}</b>
          <small>{x.tl4Desc}</small>
        </div>
      </div>
    </div>
  );
}

export function InviteStudentsModal({ classCode, lang, onClose }: { classCode: string; lang: Language; onClose: () => void }) {
  const [copied, setCopied] = useState(false);
  const x = teacherText(lang);
  const t = TRANSLATIONS[lang];

  const copyCode = () => {
    navigator.clipboard.writeText(classCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-container invite-modal" style={{ maxWidth: '480px' }}>
        <div className="modal-header">
          <div>
            <span className="eyebrow">{x.inviteEyebrow}</span>
            <h3>{x.inviteTitle}</h3>
          </div>
          <button className="icon-close" onClick={onClose}><X size={20} /></button>
        </div>

        <div style={{ padding: '20px 24px' }}>
          <p style={{ color: '#4b5563', fontSize: '14px', marginBottom: '16px' }}>
            {x.inviteBody}
          </p>

          <div style={{ background: '#f5f3ff', border: '2px dashed #7c3aed', borderRadius: '12px', padding: '18px', textAlign: 'center', marginBottom: '20px' }}>
            <span style={{ fontSize: '11px', color: '#6d28d9', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '1px' }}>{x.yourCode}</span>
            <div style={{ fontSize: '32px', fontWeight: 900, color: '#5b21b6', letterSpacing: '2px', margin: '6px 0' }}>{classCode}</div>
            <button
              type="button"
              className="btn-primary"
              style={{ marginTop: '8px', padding: '8px 16px', fontSize: '13px' }}
              onClick={copyCode}
            >
              {copied ? <><Check size={16} /> {x.copied}</> : <><Copy size={16} /> {x.copyCode}</>}
            </button>
          </div>

          <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '10px', padding: '14px' }}>
            <h5 style={{ fontSize: '13px', color: '#1e293b', marginBottom: '8px' }}>{x.howJoin}</h5>
            <ol style={{ fontSize: '12px', color: '#64748b', paddingLeft: '18px', lineHeight: '1.7' }}>
              <li>{x.joinStep1}</li>
              <li>{fill(x.joinStep2, { code: classCode })}</li>
              <li>{x.joinStep3}</li>
            </ol>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>{t.close}</button>
        </div>
      </div>
    </div>
  );
}

export function JoinClassroomModal({
  lang = 'en',
  onJoin,
  onClose,
}: {
  lang?: Language;
  onJoin: (code: string) => Promise<void>;
  onClose: () => void;
}) {
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const t = TRANSLATIONS[lang];

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!code.trim()) return;
    setBusy(true);
    setError('');
    try {
      await onJoin(code.trim().toUpperCase());
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to join classroom. Check code.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-container" style={{ maxWidth: '440px' }}>
        <div className="modal-header">
          <div>
            <span className="eyebrow">{lang === 'hi' ? 'कक्षा नामांकन' : lang === 'te' ? 'తరగతి నమోదు' : 'ENROLL IN CLASSROOM'}</span>
            <h3>{lang === 'hi' ? 'शिक्षक की कक्षा से जुड़ें' : lang === 'te' ? 'ఉపాధ్యాయుని తరగతిలో చేరండి' : "Join Teacher's Classroom"}</h3>
          </div>
          <button className="icon-close" onClick={onClose}><X size={20} /></button>
        </div>

        <form onSubmit={submit} style={{ padding: '20px 24px' }}>
          <p style={{ color: '#4b5563', fontSize: '13px', marginBottom: '16px' }}>
            {lang === 'hi'
              ? 'अपने शिक्षक द्वारा प्रदान किया गया कक्षा कोड दर्ज करें (उदा. 8A-CBSE) ताकि आपके परिणाम उनके नियंत्रण कक्ष से जुड़ सकें।'
              : lang === 'te'
              ? 'మీ ఫలితాలను ఉపాధ్యాయుని కంట్రోల్ రూమ్‌కు అనుసంధానించడానికి మీ ఉపాధ్యాయుడు అందించిన తరగతి గది కోడ్‌ను నమోదు చేయండి (ఉదా: 8A-CBSE).'
              : 'Enter the unique Classroom Code provided by your teacher (e.g. 8A-CBSE) to link your responses to their dashboard.'}
          </p>

          <label style={{ display: 'block', marginBottom: '16px' }}>
            <span style={{ fontSize: '12px', fontWeight: 700, color: '#374151' }}>
              {lang === 'hi' ? 'कक्षा कोड (Classroom Code)' : lang === 'te' ? 'తరగతి గది కోడ్ (Classroom Code)' : 'Classroom Code'}
            </span>
            <input
              required
              type="text"
              placeholder="e.g. 8A-CBSE"
              value={code}
              onChange={(e) => setCode(e.target.value.toUpperCase())}
              style={{ width: '100%', padding: '10px 14px', fontSize: '16px', fontWeight: 700, letterSpacing: '1px', textTransform: 'uppercase', borderRadius: '8px', border: '1px solid #cbd5e1', marginTop: '4px' }}
            />
          </label>

          {error && <div className="errorbox" style={{ marginBottom: '14px' }}>{error}</div>}

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
            <button type="button" className="btn-secondary" onClick={onClose}>{t.cancel}</button>
            <button type="submit" className="btn-primary" disabled={busy || !code.trim()}>
              {busy ? '…' : lang === 'hi' ? 'कक्षा से जुड़ें' : lang === 'te' ? 'తరగతిలో చేరండి' : 'Join Classroom'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

