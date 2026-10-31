import { X, Sparkles, CheckCircle2, Shield, Cpu, BookOpen, Globe2, WifiOff, Users } from 'lucide-react';

interface Props {
  onClose: () => void;
}

export function HackathonTourModal({ onClose }: Props) {
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
              Unlike unpredictable black-box generative models, PRISM uses a <b>deterministic rules engine + directed acyclic concept map</b>. Every diagnosis, confidence score, and route hypothesis is 100% reproducible and audit-proof.
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
              • <b>Languages:</b> Instant English, Hindi (हिंदी), and Telugu (తెలుగు) toggle.<br />
              • <b>Curriculum:</b> 100% CBSE Class VIII NCERT aligned reference.<br />
              • <b>Connectivity:</b> Offline queueing with idempotent sync for low-bandwidth schools.
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
          <h5>The 4 Proved Learner Archetypes (Quick Switch available in Top Bar):</h5>
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
            Explore Live PRISM Prototype <CheckCircle2 size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}

