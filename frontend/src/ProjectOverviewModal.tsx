import { X, Sparkles, CheckCircle2, Shield, Cpu, BookOpen, Globe2, WifiOff, Users } from 'lucide-react';

interface Props {
  onClose: () => void;
}

export function ProjectOverviewModal({ onClose }: Props) {
  return (
    <div className="modal-backdrop">
      <div className="modal-container tour-modal">
        <div className="modal-header">
          <div className="tour-badge-row">
            <span className="badge-pill purple">CODE KERNEL '26 · DECODE SUBMISSION</span>
            <span className="badge-pill teal">CBSE CLASS VIII MATHEMATICS</span>
          </div>
          <button className="icon-close" onClick={onClose}><X size={20} /></button>
        </div>

        <div className="tour-hero">
          <h1>PRISM CLASSROOM</h1>
          <h2>Misconception-aware adaptive learning that keeps teachers at the centre.</h2>
          <p className="tour-tagline">
            <i>"One concept. Many learning paths. One teacher-led classroom."</i>
          </p>
        </div>

        <div className="tour-grid">
          <div className="tour-card">
            <div className="card-icon"><Users className="purple-text" size={24} /></div>
            <h4>1. The Indian Classroom Challenge</h4>
            <p>
              In Classes 6–10 with 45–60 students, every learner brings different prior knowledge. End-of-chapter tests diagnose gaps too late, and teachers cannot easily personalize instruction without surrendering classroom control.
            </p>
          </div>

          <div className="tour-card">
            <div className="card-icon"><Cpu className="teal-text" size={24} /></div>
            <h4>2. Deterministic, Explainable Engine</h4>
            <p>
              PRISM uses a <b>deterministic rules engine and a prerequisite concept map</b> instead of a trained model. The same answers always produce the same route, and each route shows the rule and evidence behind it.
            </p>
          </div>

          <div className="tour-card">
            <div className="card-icon"><Sparkles className="gold-text" size={24} /></div>
            <h4>3. Three-Pillar Adaptation (LEARN · SOLVE · TEST)</h4>
            <p>
              • <b>LEARN:</b> Changes visual representation (e.g. interactive fraction bar comparator for denominator confusion).<br />
              • <b>SOLVE:</b> Adjusts scaffolding and worked-step hints.<br />
              • <b>TEST:</b> Verifies independent transfer before updating mastery.
            </p>
          </div>

          <div className="tour-card">
            <div className="card-icon"><BookOpen className="blue-text" size={24} /></div>
            <h4>4. Signature: Teacher Intervention Compiler</h4>
            <p>
              Aggregates individual evidence into an actionable, editable classroom plan with suggested flexible pods (Visual, Foundation, Guided, Extension), timings, outcomes, and one-click teacher approval.
            </p>
          </div>

          <div className="tour-card">
            <div className="card-icon"><Globe2 className="green-text" size={24} /></div>
            <h4>5. Built for Indian Realities</h4>
            <p>
              • <b>Languages:</b> English, Hindi (हिंदी), and Telugu (తెలుగు) toggle.<br />
              • <b>Curriculum:</b> one CBSE Class VIII unit, using NCERT as the reference text.<br />
              • <b>Connectivity:</b> answers are queued on the device and synced without duplicates when the connection returns.
            </p>
          </div>

          <div className="tour-card">
            <div className="card-icon"><Shield className="purple-text" size={24} /></div>
            <h4>6. Teacher-in-the-Loop Safeguards</h4>
            <p>
              No permanent student labels like "slow" or "weak". A single error never establishes a misconception. Teacher retains full authority to accept, modify, or reject every plan.
            </p>
          </div>
        </div>

        <div className="archetype-showcase-bar">
          <h5>Four simulated learner profiles (switch between them from the top bar):</h5>
          <div className="archetype-pills">
            <span className="arc-pill visual">
              <b>Aarav:</b> Denominator Magnitude Misconception (1/8 &gt; 1/3 error) → Visual Fraction Bar Route
            </span>
            <span className="arc-pill foundation">
              <b>Diya:</b> Prerequisite Gap (Fraction parts) → Equal-Parts Foundation Route
            </span>
            <span className="arc-pill calc">
              <b>Kabir:</b> Calculation Slips → Scaffolded Multiplier Grid Route
            </span>
            <span className="arc-pill extend">
              <b>Meera:</b> Demonstrated Mastery → Recipe Scaling Extension Route
            </span>
          </div>
        </div>

        <div className="tour-footer">
          <button className="btn-primary" onClick={onClose}>
            Open the prototype <CheckCircle2 size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}

