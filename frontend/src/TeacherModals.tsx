import { useState } from 'react';
import { Plan, StudentDetail, LearnerSummary } from './api';
import { Language, TRANSLATIONS } from './translations';
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
            <span className="eyebrow">TEACHER INTERVENTION COMPILER</span>
            <h3>Edit Intervention: {plan.barrier}</h3>
          </div>
          <button className="icon-close" onClick={onClose}><X size={20} /></button>
        </div>

        <form onSubmit={handleSave} className="modal-form">
          <div className="form-group">
            <label>Plan Status Decision:
              <div className="status-selector">
                <button
                  type="button"
                  className={status === 'approved' ? 'active-status approved' : ''}
                  onClick={() => setStatus('approved')}
                >
                  <CheckCircle2 size={16} /> Approve Plan
                </button>
                <button
                  type="button"
                  className={status === 'modified' ? 'active-status modified' : ''}
                  onClick={() => setStatus('modified')}
                >
                  <Sparkles size={16} /> Modified by Teacher
                </button>
                <button
                  type="button"
                  className={status === 'rejected' ? 'active-status rejected' : ''}
                  onClick={() => setStatus('rejected')}
                >
                  <X size={16} /> Dismiss / Reject
                </button>
              </div>
            </label>
          </div>

          <div className="form-group">
            <label>Prescribed Instructional Activity:
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
              <label>Allocated Time:
                <select value={duration} onChange={(e) => setDuration(e.target.value)}>
                  <option value="5 min">5 min (Quick check)</option>
                  <option value="10 min">10 min (Focused support)</option>
                  <option value="12 min">12 min (Standard pod)</option>
                  <option value="15 min">15 min (Deep extension)</option>
                  <option value="20 min">20 min (Extended group)</option>
                </select>
              </label>
            </div>

            <div className="form-group">
              <label>Target Outcome:
                <input
                  required
                  value={outcome}
                  onChange={(e) => setOutcome(e.target.value)}
                />
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>Assigned Students (Click to toggle/reassign):
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
                placeholder="Add pedagogical observations, seating notes, or scaffolding instructions..."
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
              {busy ? 'Saving...' : t.saveChanges}
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

  return (
    <div className="modal-backdrop">
      <div className="modal-container dossier-modal">
        <div className="modal-header">
          <div className="dossier-id">
            <span className="eyebrow">LEARNER EVIDENCE DOSSIER</span>
            <h3>{detail.name} <small>({detail.code})</small></h3>
            <p className="student-meta-info">Class VIII CBSE · Email: {detail.email}</p>
          </div>
          <button className="icon-close" onClick={onClose}><X size={20} /></button>
        </div>

        <div className="dossier-metrics">
          <div className="dossier-card">
            <span>Estimated Mastery</span>
            <b>{Math.round(detail.mastery * 100)}%</b>
            <div className="mini-progress">
              <i style={{ width: `${detail.mastery * 100}%` }} />
            </div>
          </div>
          <div className="dossier-card">
            <span>Evidence Responses</span>
            <b>{detail.evidence_count}</b>
            <small>Total observable attempts</small>
          </div>
          <div className="dossier-card">
            <span>Diagnosed Barrier</span>
            <b className="purple-text">{detail.misconception || 'No persistent error'}</b>
            <small>
              {detail.misconception_confidence
                ? `${Math.round(detail.misconception_confidence * 100)}% rule confidence`
                : 'Secured or provisional'}
            </small>
          </div>
          <div className="dossier-card">
            <span>Recommended Route</span>
            <b className="badge-pill teal">{detail.recommendation.toUpperCase()}</b>
            <small>Prerequisite: {detail.prerequisite_status}</small>
          </div>
        </div>

        <div className="dossier-history-section">
          <h4>Observable Response History</h4>
          <p className="subtext">
            Transparent evidentiary basis for PRISM’s route hypothesis. Every diagnosis is explainable and grounded in these responses:
          </p>

          <div className="attempt-timeline">
            {detail.attempts.length === 0 ? (
              <p className="empty-msg">No attempts recorded yet for this student.</p>
            ) : (
              detail.attempts.map((att, idx) => (
                <div key={att.id || idx} className={`attempt-item ${att.correct ? 'correct' : 'incorrect'}`}>
                  <div className="attempt-status-col">
                    {att.correct ? (
                      <CheckCircle2 size={18} className="text-green" />
                    ) : (
                      <AlertCircle size={18} className="text-red" />
                    )}
                    <span className="stage-tag">{att.stage}</span>
                  </div>
                  <div className="attempt-detail-col">
                    <p className="attempt-prompt"><b>Q:</b> {att.prompt}</p>
                    <div className="attempt-answer-row">
                      <span>Student selected: <b>{att.response}</b></span>
                      {!att.correct && (
                        <span className="expected-ans">Expected: <b>{att.expected_answer}</b></span>
                      )}
                      {att.misconception && (
                        <span className="miscon-pill">Triggered Rule: {att.misconception}</span>
                      )}
                    </div>
                    {att.explanation && (
                      <small className="attempt-exp">💡 {att.explanation}</small>
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
            <span>
              Safeguard: Non-permanent hypothesis. A single error cannot establish a label; teacher retains full discretion.
            </span>
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
  onClose: () => void;
}

export function PrintPlanModal({ plans, classCode, teacherName, learners = [], onClose }: PrintPlanModalProps) {
  const learnerName = (code: string) => learners.find(l => l.code === code)?.name || code;
  return (
    <div className="modal-backdrop">
      <div className="modal-container print-modal">
        <div className="modal-header no-print">
          <div>
            <span className="eyebrow">CBSE OFFICIAL FORMAT</span>
            <h3>Classroom Intervention Briefing</h3>
          </div>
          <div className="print-actions">
            <button className="btn-primary" onClick={() => window.print()}>
              <Printer size={16} /> Print / Save as PDF
            </button>
            <button className="icon-close" onClick={onClose}><X size={20} /></button>
          </div>
        </div>

        <div className="printable-document">
          <div className="cbse-doc-header">
            <div className="school-title">
              <h2>CENTRAL BOARD OF SECONDARY EDUCATION</h2>
              <h3>DIFFERENTIATED CLASSROOM INSTRUCTION PLAN · 2026–27</h3>
              <p>NCERT Mathematics Class VIII · Rational Numbers: Equivalent Fractions</p>
            </div>
            <div className="doc-meta-grid">
              <div><b>Class / Section:</b> {classCode}</div>
              <div><b>Subject Teacher:</b> {teacherName}</div>
              <div><b>Date:</b> {new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}</div>
              <div><b>Lesson Period:</b> 45 Minutes</div>
            </div>
          </div>

          <table className="print-plan-table">
            <thead>
              <tr>
                <th style={{ width: '18%' }}>Intervention Pod</th>
                <th style={{ width: '20%' }}>Assigned Students</th>
                <th style={{ width: '34%' }}>Prescribed Activity & Scaffolding</th>
                <th style={{ width: '10%' }}>Duration</th>
                <th style={{ width: '18%' }}>Target Outcome & Status</th>
              </tr>
            </thead>
            <tbody>
              {plans.map((plan) => (
                <tr key={plan.id}>
                  <td>
                    <b>{plan.barrier}</b>
                    <br />
                    <small style={{ color: '#666' }}>Confidence: {plan.confidence}</small>
                  </td>
                  <td>
                    <b>{plan.student_codes.map(learnerName).join(', ')}</b>
                  </td>
                  <td>
                    {plan.activity}
                    {plan.teacher_notes && (
                      <p style={{ marginTop: '4px', fontStyle: 'italic', color: '#444' }}>
                        Note: {plan.teacher_notes}
                      </p>
                    )}
                  </td>
                  <td><b>{plan.duration}</b></td>
                  <td>
                    {plan.outcome}
                    <br />
                    <span className={`status-tag ${plan.status}`}>
                      [{plan.status.toUpperCase()}]
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="print-signoff">
            <div className="signoff-box">
              <hr />
              <span>Subject Teacher Signature</span>
            </div>
            <div className="signoff-box">
              <hr />
              <span>Head of Mathematics / Principal</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function LessonTimelineSchedule() {
  return (
    <div className="timeline-schedule-card">
      <div className="timeline-header">
        <Clock3 size={18} className="purple-text" />
        <div>
          <h4>45-Minute Lesson Pacing & Pod Workflow</h4>
          <p>How the Teacher Intervention Compiler divides classroom time dynamically:</p>
        </div>
      </div>

      <div className="timeline-blocks">
        <div className="t-block phase-1" style={{ flex: 2 }}>
          <span className="t-time">00 – 10 min</span>
          <b>1. Whole-Class Concept Launch & Quick Diagnostic</b>
          <small>Interactive check probes prerequisite readiness and equivalence.</small>
        </div>
        <div className="t-block phase-2" style={{ flex: 3 }}>
          <span className="t-time">10 – 25 min</span>
          <b>2. Differentiated Learning Pods (Interventions)</b>
          <small>
            Visual Support Pod (10m) · Foundation Pod (12m) · Guided Practice (12m) · Recipe Lab (15m)
          </small>
        </div>
        <div className="t-block phase-3" style={{ flex: 2 }}>
          <span className="t-time">25 – 35 min</span>
          <b>3. Independent Transfer Verification</b>
          <small>Students test transfer in a novel context; engine updates evidence live.</small>
        </div>
        <div className="t-block phase-4" style={{ flex: 2 }}>
          <span className="t-time">35 – 45 min</span>
          <b>4. Whole-Class Synthesis & Next Lesson Pacing</b>
          <small>Teacher reviews updated evidence pulse and confirms readiness to progress.</small>
        </div>
      </div>
    </div>
  );
}

export function InviteStudentsModal({ classCode, onClose }: { classCode: string; onClose: () => void }) {
  const [copied, setCopied] = useState(false);

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
            <span className="eyebrow">REAL DATA ENROLLMENT</span>
            <h3>Enroll Real Students</h3>
          </div>
          <button className="icon-close" onClick={onClose}><X size={20} /></button>
        </div>

        <div style={{ padding: '20px 24px' }}>
          <p style={{ color: '#4b5563', fontSize: '14px', marginBottom: '16px' }}>
            Share this official Classroom Join Code with your students. Real student submissions will automatically feed into your Teacher Intervention Compiler.
          </p>

          <div style={{ background: '#f5f3ff', border: '2px dashed #7c3aed', borderRadius: '12px', padding: '18px', textAlign: 'center', marginBottom: '20px' }}>
            <span style={{ fontSize: '11px', color: '#6d28d9', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '1px' }}>Your Classroom Code</span>
            <div style={{ fontSize: '32px', fontWeight: 900, color: '#5b21b6', letterSpacing: '2px', margin: '6px 0' }}>{classCode}</div>
            <button
              type="button"
              className="btn-primary"
              style={{ marginTop: '8px', padding: '8px 16px', fontSize: '13px' }}
              onClick={copyCode}
            >
              {copied ? <><Check size={16} /> Code Copied!</> : <><Copy size={16} /> Copy Join Code</>}
            </button>
          </div>

          <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '10px', padding: '14px' }}>
            <h5 style={{ fontSize: '13px', color: '#1e293b', marginBottom: '8px' }}>How real students join:</h5>
            <ol style={{ fontSize: '12px', color: '#64748b', paddingLeft: '18px', lineHeight: '1.7' }}>
              <li>Student registers with their email at <b>prism-classroom.onrender.com</b>.</li>
              <li>Enters code <b>{classCode}</b> during registration or clicks "Join Classroom".</li>
              <li>Completes diagnostic or practice tasks; their real data streams into your Control Room live!</li>
            </ol>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>Close</button>
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

