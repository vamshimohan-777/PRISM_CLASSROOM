import { api, type CurriculumGraphRow } from './api';
import { getLocalizedChapterTitle } from './localization';
import { prerequisiteName, teacherText } from './teacherText';
import { useEffect, useState } from 'react';
import {
  CheckCircle2,
  ArrowRight,
  ExternalLink,
  Shield,
  Users,
  Clock3,
  Printer,
  ChevronDown,
  ChevronUp,
  FileText,
} from 'lucide-react';
import { Language, TRANSLATIONS } from './translations';
import { VisualFractionBarWorkbench } from './InteractiveTools';

interface LandingPageProps {
  lang: Language;
  onLaunchApp: () => void;
}

// ----------------------------------------------------
// 1. PUBLIC MARKETING & PRODUCT LANDING PAGE
// ----------------------------------------------------
export function LandingPage({ lang, onLaunchApp }: LandingPageProps) {
  const t = TRANSLATIONS[lang];

  return (
    <div className="landing-page-container">
      {/* Hero Section */}
      <section className="landing-hero">
        <div className="landing-badge-row">
          <span className="badge-pill teal">{t.landingBadge1}</span>
          <span className="badge-pill green">{t.landingBadge2}</span>
          <span className="badge-pill purple">{t.landingBadge3}</span>
        </div>

        <h1 className="landing-title">{t.landingTitle}</h1>
        <p className="landing-subtitle">{t.landingSubtitle}</p>

        <div className="landing-cta-row">
          <button type="button" className="btn-primary hero-cta-btn" onClick={onLaunchApp}>
            {t.landingGetStarted} <ArrowRight size={18} />
          </button>
          <button type="button" className="btn-secondary hero-flowchart-btn" onClick={onLaunchApp}>
            {t.landingSignInWorkspace}
          </button>
        </div>
      </section>

      {/* The Indian Classroom Reality Section */}
      <section className="landing-section bg-alt">
        <div className="section-head">
          <span className="eyebrow">{t.landingRealityEyebrow}</span>
          <h2>{t.landingRealityTitle}</h2>
          <p>{t.landingRealitySub}</p>
        </div>

        <div className="reality-grid">
          <div className="reality-card">
            <div className="card-badge red">{lang === 'hi' ? 'समस्या 1' : lang === 'te' ? 'సమస్య 1' : 'PROBLEM 1'}</div>
            <h3>{t.landingProblem1Title}</h3>
            <p>{t.landingProblem1Desc}</p>
          </div>
          <div className="reality-card">
            <div className="card-badge red">{lang === 'hi' ? 'समस्या 2' : lang === 'te' ? 'సమస్య 2' : 'PROBLEM 2'}</div>
            <h3>{t.landingProblem2Title}</h3>
            <p>{t.landingProblem2Desc}</p>
          </div>
          <div className="reality-card">
            <div className="card-badge green">{lang === 'hi' ? 'PRISM समाधान' : lang === 'te' ? 'PRISM పరిష్కారం' : 'THE PRISM SOLUTION'}</div>
            <h3>{t.landingSolutionTitle}</h3>
            <p>{t.landingSolutionDesc}</p>
          </div>
        </div>
      </section>

      {/* The 3 Pillars of Adaptation */}
      <section className="landing-section">
        <div className="section-head">
          <span className="eyebrow">{t.landingPillarsEyebrow}</span>
          <h2>{t.landingPillarsTitle}</h2>
          <p>{t.landingPillarsSub}</p>
        </div>

        <div className="pillars-grid">
          <div className="pillar-card">
            <div className="pillar-num">1</div>
            <h3>{t.landingPillar1Title}</h3>
            <p>{t.landingPillar1Desc}</p>
            <span className="tag-pill purple">{t.landingPillar1Tag}</span>
          </div>
          <div className="pillar-card">
            <div className="pillar-num">2</div>
            <h3>{t.landingPillar2Title}</h3>
            <p>{t.landingPillar2Desc}</p>
            <span className="tag-pill teal">{t.landingPillar2Tag}</span>
          </div>
          <div className="pillar-card">
            <div className="pillar-num">3</div>
            <h3>{t.landingPillar3Title}</h3>
            <p>{t.landingPillar3Desc}</p>
            <span className="tag-pill green">{t.landingPillar3Tag}</span>
          </div>
        </div>
      </section>

      {/* Interactive Tool Playground Showcase */}
      <section className="landing-section bg-alt">
        <div className="section-head">
          <span className="eyebrow">{t.landingShowcaseEyebrow}</span>
          <h2>{t.landingShowcaseTitle}</h2>
          <p>{t.landingShowcaseSub}</p>
        </div>
        <div style={{ maxWidth: '850px', margin: '0 auto' }}>
          <VisualFractionBarWorkbench lang={lang} />
        </div>
      </section>

      {/* Teacher Intervention Compiler Showcase */}
      <section className="landing-section">
        <div className="section-head">
          <span className="eyebrow">{t.landingCompilerEyebrow}</span>
          <h2>{t.landingCompilerTitle}</h2>
          <p>{t.landingCompilerSub}</p>
        </div>

        <div className="compiler-feature-grid">
          <div className="compiler-feature-box">
            <Clock3 size={24} className="purple-text" />
            <h4>{t.landingCompilerF1Title}</h4>
            <p>{t.landingCompilerF1Desc}</p>
          </div>
          <div className="compiler-feature-box">
            <Users size={24} className="teal-text" />
            <h4>{t.landingCompilerF2Title}</h4>
            <p>{t.landingCompilerF2Desc}</p>
          </div>
          <div className="compiler-feature-box">
            <FileText size={24} className="green-text" />
            <h4>{t.landingCompilerF3Title}</h4>
            <p>{t.landingCompilerF3Desc}</p>
          </div>
          <div className="compiler-feature-box">
            <Printer size={24} className="amber-text" />
            <h4>{t.landingCompilerF4Title}</h4>
            <p>{t.landingCompilerF4Desc}</p>
          </div>
        </div>
      </section>

      {/* Real Data & Safety Banner */}
      <section className="landing-banner-safety">
        <Shield size={36} />
        <div>
          <h3>{t.landingSafetyTitle}</h3>
          <p>{t.landingSafetyDesc}</p>
        </div>
        <button type="button" className="btn-primary" onClick={onLaunchApp}>
          {t.landingGetStarted} <ArrowRight size={16} />
        </button>
      </section>
    </div>
  );
}

// ----------------------------------------------------
// 2. CURRICULUM & CONCEPT DAG EXPLORER PAGE
// ----------------------------------------------------
export function CurriculumPage({ lang, onLaunchApp }: { lang: Language; onLaunchApp: () => void }) {
  const t = TRANSLATIONS[lang];
  const x = teacherText(lang);
  const [graph, setGraph] = useState<CurriculumGraphRow[]>([]);
  useEffect(() => {
    api.curriculumGraph().then((data) => setGraph(data.prerequisite_graph)).catch(() => setGraph([]));
  }, []);

  const chapters = [
    {
      num: 1,
      title: lang === 'hi' ? 'परिमेय संख्याएँ (Rational Numbers)' : lang === 'te' ? 'అకరణీయ సంఖ్యలు (Rational Numbers)' : 'Rational Numbers',
      summary: lang === 'hi' ? 'तुल्य भिन्न और मानक रूप के साथ परिमेय संख्याओं की तुलना, सरलीकरण और निरूपण।' : lang === 'te' ? 'సమతుల్య భిన్నాలు మరియు ప్రామాణిక రూపంతో అకరణీయ సంఖ్యలను పోల్చడం, సరళీకరించడం.' : 'Compare, simplify, and represent rational numbers with equivalent fractions and standard form.',
      status: 'Active Focus',
      minutes: 42,
    },
    {
      num: 2,
      title: lang === 'hi' ? 'एक चर वाले रैखिक समीकरण (Linear Equations)' : lang === 'te' ? 'ఏక చరరాశిలో రేఖీయ సమీకరణాలు (Linear Equations)' : 'Linear Equations in One Variable',
      summary: lang === 'hi' ? 'एक अज्ञात मात्रा वाले वास्तविक जीवन के रैखिक समीकरणों का मॉडल बनाएं और हल करें।' : lang === 'te' ? 'ఒక తెలియని పరిమాణంతో వాస్తవ ప్రపంచ రేఖీయ సమీకరణాలను రూపొందించి సాధించండి.' : 'Model and solve real-world linear equations with one unknown quantity.',
      status: 'Diagnostic Ready',
      minutes: 46,
    },
    {
      num: 3,
      title: lang === 'hi' ? 'चतुर्भुजों को समझना (Understanding Quadrilaterals)' : lang === 'te' ? 'చతుర్భుజాలను అర్థం చేసుకోవడం (Quadrilaterals)' : 'Understanding Quadrilaterals',
      summary: lang === 'hi' ? 'बहुभुजों, समानांतर चतुर्भुजों का वर्गीकरण करें और कोण-योग गुणों से तर्क करें।' : lang === 'te' ? 'బహుభుజులు, సమాంతర చతుర్భుజాలను వర్గీకరించి, కోణాల మొత్తం ధర్మాలను వర్తింపజేయండి.' : 'Classify polygons, parallelograms, and reason with angle-sum properties.',
      status: 'Diagnostic Ready',
      minutes: 38,
    },
    {
      num: 4,
      title: lang === 'hi' ? 'प्रायोगिक ज्यामिति (Practical Geometry)' : lang === 'te' ? 'ప్రాయోగిక జ్యామితి (Practical Geometry)' : 'Practical Geometry',
      summary: lang === 'hi' ? 'सटीक भुजा और कोण मापों से अद्वितीय चतुर्भुजों की रचना करें।' : lang === 'te' ? 'ఖచ్చితమైన భుజాలు మరియు కోణాల కొలతలతో ప్రత్యేక చతుర్భుజాలను నిర్మించండి.' : 'Construct unique quadrilaterals from precise side and angle measurements.',
      status: 'Diagnostic Ready',
      minutes: 35,
    },
    {
      num: 5,
      title: lang === 'hi' ? 'आँकड़ों का प्रबंधन (Data Handling)' : lang === 'te' ? 'దత్తాంశ నిర్వహణ (Data Handling)' : 'Data Handling',
      summary: lang === 'hi' ? 'बारंबारता बंटन, दोहरे दंड आलेख और प्रायिकता की मूल बातों से डेटा व्यवस्थित करें।' : lang === 'te' ? 'పౌనఃపున్య విభాజనాలు, డబుల్ బార్ గ్రాఫ్‌లు మరియు సంభావ్యతతో డేటాను నిర్వహించండి.' : 'Organize data with frequency distributions, double bar graphs, and probability basics.',
      status: 'Diagnostic Ready',
      minutes: 40,
    },
    {
      num: 6,
      title: lang === 'hi' ? 'वर्ग और वर्गमूल (Squares & Square Roots)' : lang === 'te' ? 'వర్గాలు మరియు వర్గమూలాలు (Squares & Roots)' : 'Squares and Square Roots',
      summary: lang === 'hi' ? 'पूर्ण वर्ग, पाइथागोरस त्रिक और भाग विधि से वर्गमूल की जांच करें।' : lang === 'te' ? 'ఖచ్చితమైన వర్గాలు, పైథాగరియన్ త్రికాలు మరియు భాగహార పద్ధతి వర్గమూలాలను కనుగొనండి.' : 'Investigate perfect squares, Pythagorean triplets, and division method roots.',
      status: 'Diagnostic Ready',
      minutes: 44,
    },
    {
      num: 7,
      title: lang === 'hi' ? 'घन और घनमूल (Cubes & Cube Roots)' : lang === 'te' ? 'ఘనాలు మరియు ఘనమూలాలు (Cubes & Roots)' : 'Cubes and Cube Roots',
      summary: lang === 'hi' ? 'घन संख्याएं, अभाज्य गुणनखंडन पैटर्न और घनमूल का अन्वेषण करें।' : lang === 'te' ? 'ఘన సంఖ్యలు, ప్రధాన కారణాంక పద్ధతులు మరియు ఘనమూలాలను అన్వేషించండి.' : 'Explore cubic numbers, prime factorisation patterns, and cube roots.',
      status: 'Diagnostic Ready',
      minutes: 40,
    },
    {
      num: 8,
      title: lang === 'hi' ? 'राशियों की तुलना (Comparing Quantities)' : lang === 'te' ? 'రాశులను పోల్చడం (Comparing Quantities)' : 'Comparing Quantities',
      summary: lang === 'hi' ? 'प्रतिशत, छूट, लाभ/हानि और चक्रवृद्धि ब्याज की गणना लागू करें।' : lang === 'te' ? 'శాతాలు, తగ్గింపులు, లాభ/నష్టాలు మరియు చక్రవడ్డీ గణనలను వర్తింపజేయండి.' : 'Apply percentages, discounts, profit/loss, and compound interest calculations.',
      status: 'Diagnostic Ready',
      minutes: 48,
    },
  ];

  return (
    <div className="curriculum-page-container">
      <div className="page-header">
        <span className="eyebrow">{t.curriculumEyebrow}</span>
        <h1>{t.curriculumTitle}</h1>
        <p>{t.curriculumSub}</p>
      </div>

      {/* Visual DAG Diagram */}
      <section className="dag-section">
        <h3>{t.dagTitle}</h3>
        <p className="dag-sub">{t.dagSub}</p>

        <div className="dag-visual-card">
          <div className="dag-step step-root">
            <span className="step-tag">{t.dagRootTag}</span>
            <h4>{t.dagRootTitle}</h4>
            <p>{t.dagRootDesc}</p>
          </div>

          <div className="dag-split-arrows">
            <div className="arrow-split">↘</div>
            <div className="arrow-split">↗</div>
          </div>

          <div className="dag-branches">
            <div className="dag-step step-branch">
              <span className="step-tag">{t.dagBranch1Tag}</span>
              <h4>{t.dagBranch1Title}</h4>
              <p>{t.dagBranch1Desc}</p>
            </div>
            <div className="dag-step step-branch">
              <span className="step-tag">{t.dagBranch2Tag}</span>
              <h4>{t.dagBranch2Title}</h4>
              <p>{t.dagBranch2Desc}</p>
            </div>
          </div>

          <div className="dag-converge-arrow">➔</div>

          <div className="dag-step step-target">
            <span className="step-tag">{t.dagTargetTag}</span>
            <h4>{t.dagTargetTitle}</h4>
            <p>{t.dagTargetDesc}</p>
          </div>
        </div>
      </section>

      {/* Prerequisites for every chapter, from the API so it cannot drift from the engine */}
      {graph.length > 0 && (
        <section className="chapters-catalog-section">
          <h3>{x.graphTitle}</h3>
          <p className="dag-sub">{x.graphSub}</p>
          <div className="curriculum-table-wrapper">
            <table className="curriculum-table">
              <thead>
                <tr>
                  <th>{t.colChapter}</th>
                  <th>{x.thSkills}</th>
                  <th>{x.thEarlier}</th>
                </tr>
              </thead>
              <tbody>
                {graph.map((row) => (
                  <tr key={row.unit_id}>
                    <td><b>{getLocalizedChapterTitle(row.unit_id, row.title, lang)}</b></td>
                    <td>{row.skills.map((skill) => prerequisiteName(skill.id, lang, skill.title)).join(', ')}</td>
                    <td>
                      {row.chapters.length
                        ? row.chapters
                            .map((chapter) => {
                              const unit = graph.find((item) => item.concept === chapter.id);
                              return unit ? getLocalizedChapterTitle(unit.unit_id, unit.title, lang) : chapter.title;
                            })
                            .join(', ')
                        : x.noneEarlier}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {/* 8 Chapters Table */}
      <section className="chapters-catalog-section">
        <h3>{t.syllabusTableTitle}</h3>
        <div className="curriculum-table-wrapper">
          <table className="curriculum-table">
            <thead>
              <tr>
                <th>{t.colChapter}</th>
                <th>{t.colModuleTitle}</th>
                <th>{t.colCompetencies}</th>
                <th>{t.colDuration}</th>
                <th>{t.colStatus}</th>
              </tr>
            </thead>
            <tbody>
              {chapters.map((ch) => (
                <tr key={ch.num}>
                  <td>
                    <b>{t.chapterPrefix} {ch.num.toString().padStart(2, '0')}</b>
                  </td>
                  <td><b>{ch.title}</b></td>
                  <td>{ch.summary}</td>
                  <td>
                    <Clock3 size={13} style={{ display: 'inline', marginRight: '4px' }} /> {ch.minutes} min
                  </td>
                  <td>
                    <span className={`status-badge ${ch.status === 'Active Focus' ? 'active' : 'ready'}`}>
                      {ch.status === 'Active Focus' ? t.statusActiveFocus : t.statusDiagnosticReady}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <div style={{ textAlign: 'center', marginTop: '24px' }}>
        <button type="button" className="btn-primary" onClick={onLaunchApp}>
          {t.testCurriculumBtn} <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 3. PROJECT FLOWCHART PAGE
// ----------------------------------------------------
export function FlowchartPage() {
  return (
    <div className="flowchart-page-container">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <span className="eyebrow">SYSTEM ARCHITECTURE</span>
          <h1>Adaptive Learning — Closed-Loop Workflow</h1>
          <p>End-to-end data lifecycle from student attempt ingestion to the Teacher Intervention Compiler.</p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <a href="/flowchart.html" target="_blank" rel="noreferrer" className="btn-primary">
            <ExternalLink size={15} /> Open Fullscreen Flowchart
          </a>
          <button type="button" className="btn-secondary" onClick={() => window.print()}>
            <Printer size={15} /> Print / Save PDF
          </button>
        </div>
      </div>

      <div className="flowchart-frame-box">
        <iframe
          src="/flowchart.html"
          title="PRISM Classroom Project Flowchart"
          className="flowchart-iframe"
        />
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 4. PRODUCT HELP & FAQ PAGE (FULLY MULTILINGUAL EN, HI, TE)
// ----------------------------------------------------
export function AeoGeoFaqPage({ lang }: { lang: Language }) {
  const [openIdx, setOpenIdx] = useState<number | null>(0);
  const t = TRANSLATIONS[lang];

  const faqs = [
    {
      category: 'For Students',
      q:
        lang === 'hi'
          ? 'मैं अपने शिक्षक की कक्षा में कैसे शामिल होऊं?'
          : lang === 'te'
          ? 'నేను నా ఉపాధ్యాయుని తరగతి గదిలో ఎలా చేరాలి?'
          : "How do I join my teacher's classroom?",
      a:
        lang === 'hi'
          ? 'साइन इन करने के बाद, अपने डैशबोर्ड पर "कोड द्वारा कक्षा से जुड़ें" बटन पर क्लिक करें। अपने शिक्षक द्वारा साझा किया गया कक्षा कोड दर्ज करें (उदा. MATH8A)। जुड़ने के बाद, आपके नैदानिक परिणाम स्वचालित रूप से शिक्षक के नियंत्रण कक्ष में प्रदर्शित होंगे।'
          : lang === 'te'
          ? 'లాగిన్ అయిన తర్వాత, మీ డాష్‌బోర్డ్‌లో "కోడ్ ద్వారా తరగతిలో చేరండి" బటన్‌పై క్లిక్ చేయండి. మీ ఉపాధ్యాయుడు పంచుకున్న తరగతి గది కోడ్‌ను నమోదు చేయండి (ఉదా: MATH8A). నమోదు చేసుకున్న తర్వాత, మీ ఫలితాలు స్వయంచాలకంగా ఉపాధ్యాయుని నియంత్రణ గదికి వెళ్తాయి.'
          : 'After signing in, click the "Join Classroom by Code" button on your learning dashboard. Enter the classroom code your teacher shared with you (for example: MATH8A). Once enrolled, your diagnostic results and progress will automatically stream to your teacher\'s control room in real time.',
    },
    {
      category: 'For Students',
      q:
        lang === 'hi'
          ? 'नैदानिक परीक्षण क्या है और मुझे इसे पहले क्यों करना पड़ता है?'
          : lang === 'te'
          ? 'నిర్ధారణ పరీక్ష అంటే ఏమిటి మరియు నేను దీన్ని మొదట ఎందుకు చేయాలి?'
          : 'What is a diagnostic and why do I need to do it first?',
      a:
        lang === 'hi'
          ? 'नैदानिक परीक्षण 3–5 लक्षित प्रश्नों का एक संक्षिप्त सेट है जो यह समझने में मदद करता है कि आप किसी संकल्पना में कहाँ हैं — केवल यह नहीं कि आपका उत्तर सही था या गलत, बल्कि यह कि आपने किस प्रकार के तर्क का उपयोग किया। इससे PRISM आपके लिए उपयुक्त सीखने का मार्ग निर्धारित करता है।'
          : lang === 'te'
          ? 'నిర్ధారణ పరీక్ష అనేది 3–5 లక్ష్యిత ప్రశ్నల సమాహారం, ఇది ఒక భావనలో మీ అవగాహనను ఖచ్చితంగా అర్థం చేసుకోవడానికి సహాయపడుతుంది. మీరు సరైన మార్గంలో నేర్చుకోవడానికి PRISM సరైన అభ్యాస మార్గాన్ని సూచించడానికి ఇది ఉపయోగపడుతుంది.'
          : 'A diagnostic is a short set of 3–5 targeted questions that helps PRISM understand exactly where you are with a concept — not just whether you got the answer right, but what kind of reasoning you used. This allows PRISM to prescribe the right learning path for you, so you aren\'t repeating things you already know or jumping ahead of concepts you haven\'t secured yet.',
    },
    {
      category: 'For Students',
      q:
        lang === 'hi'
          ? 'यदि मैं किसी प्रश्न का गलत उत्तर देता हूँ तो क्या होगा?'
          : lang === 'te'
          ? 'నేను ప్రశ్నకు తప్పు సమాధానం ఇస్తే ఏమి జరుగుతుంది?'
          : 'What happens if I answer a question incorrectly?',
      a:
        lang === 'hi'
          ? 'एक भी गलत उत्तर आपको कभी स्थायी लेबल नहीं देता। PRISM को आपकी समझ के बारे में निष्कर्ष निकालने से पहले कम से कम दो मेल खाने वाले त्रुटि पैटर्न की आवश्यकता होती है। आपका प्रत्येक प्रयास आपकी साक्ष्य प्रोफ़ाइल बनाता है।'
          : lang === 'te'
          ? 'ఒక్క తప్పు సమాధానం మిమ్మల్ని ఎప్పటికీ తక్కువగా అంచనా వేయదు. PRISM మీ అవగాహన గురించి నిర్ధారించడానికి కనీసం రెండు సరిపోలే తప్పుల సరళిని పరిశీలిస్తుంది. ప్రతి ప్రయత్నం మీ సమగ్ర ప్రొఫైల్‌ను నిర్మిస్తుంది.'
          : 'A single wrong answer never labels or categorises you. PRISM requires at least two matching error patterns before concluding anything about your understanding. Each attempt you make builds your evidence profile, and the system is always looking at the full picture — not just your last response.',
    },
    {
      category: 'For Students',
      q:
        lang === 'hi'
          ? 'क्या मैं इंटरनेट कनेक्शन के बिना PRISM का उपयोग कर सकता हूँ?'
          : lang === 'te'
          ? 'స్థిరమైన ఇంటర్నెట్ కనెక్షన్ లేకుండా నేను PRISMని ఉపయోగించవచ్చా?'
          : 'Can I use PRISM without a stable internet connection?',
      a:
        lang === 'hi'
          ? 'हाँ। जब आपका इंटरनेट अस्थिर या बंद होता है, तो PRISM आपके उत्तरों को सुरक्षित रूप से ऑफ़लाइन मोड में सहेजता है। स्क्रीन के शीर्ष पर "ऑफ़लाइन मोड" संकेतक दिखाई देगा। कनेक्शन वापस आने पर उत्तर स्वचालित रूप से सिंक हो जाते हैं।'
          : lang === 'te'
          ? 'అవును. ఇంటర్నెట్ సరిగ్గా లేనప్పుడు లేదా డిస్‌కనెక్ట్ అయినప్పుడు, PRISM మీ ప్రతిస్పందనలను ఆఫ్‌లైన్ మోడ్‌లో భద్రపరుస్తుంది. కనెక్షన్ పునరుద్ధరించబడినప్పుడు మీ సమాధానాలు స్వయంచాలకంగా సర్వర్‌కు సమకాలీకరించబడతాయి.'
          : 'Yes. When your internet is unreliable or disconnected, PRISM stores your responses securely in offline mode. You\'ll see an "Offline Mode" indicator at the top of the screen. When your connection returns, your queued responses sync automatically to the server with no duplicate submissions.',
    },
    {
      category: 'For Students',
      q:
        lang === 'hi'
          ? 'तीन चरण — निदान, अभ्यास और परीक्षण क्या हैं?'
          : lang === 'te'
          ? 'మూడు దశలు — నిర్ధారణ, అభ్యాసం మరియు పరీక్ష అంటే ఏమిటి?'
          : 'What are the three stages — Diagnostic, Practice, and Test?',
      a:
        lang === 'hi'
          ? 'प्रत्येक अध्याय तीन चरणों का पालन करता है: निदान आपकी वर्तमान समझ की पहचान करता है। अभ्यास चरण आपके निदान के अनुसार अनुकूलित होता है (दृश्य भिन्न पट्टियाँ, मार्गदर्शित गुणक गाइड, या चुनौती)। स्थानांतरण परीक्षण वास्तविक संदर्भ में स्वतंत्र दक्षता की पुष्टि करता है।'
          : lang === 'te'
          ? 'ప్రతి అధ్యాయం మూడు దశలను అనుసరిస్తుంది: నిర్ధారణ మీ ప్రస్తుత అవగాహనను గుర్తిస్తుంది. అభ్యాస దశ మీ నిర్ధారణ ఫలితానికి అనుగుణంగా మారుతుంది (దృశ్య భిన్నాల పట్టీలు, గుణకార గైడ్ లేదా సవాలు). బదిలీ పరీక్ష స్వతంత్ర నైపుణ్యాన్ని ధృవీకరిస్తుంది.'
          : 'Every chapter follows three stages. The Diagnostic identifies your current understanding. The Practice stage adapts to your diagnostic result — you might get interactive visual fraction bars, a scaffolded multiplier guide, or an extension challenge depending on what you need. The Transfer Test is a final unguided problem in a novel real-world context (such as a recipe scaling problem) that verifies independent mastery.',
    },
    {
      category: 'For Teachers',
      q:
        lang === 'hi'
          ? 'मैं अपनी कक्षा में विद्यार्थियों को कैसे नामांकित करूँ?'
          : lang === 'te'
          ? 'నా తరగతి గదిలో విద్యార్థులను ఎలా నమోదు చేయాలి?'
          : 'How do I enrol students into my classroom?',
      a:
        lang === 'hi'
          ? 'अपने नियंत्रण कक्ष से, अपना अनूठा कक्षा कोड देखने के लिए "विद्यार्थियों को नामांकित करें" पर क्लिक करें। यह कोड अपने विद्यार्थियों के साथ साझा करें। विद्यार्थी कोड दर्ज करके सीधे आपकी कक्षा सूची से जुड़ जाते हैं।'
          : lang === 'te'
          ? 'మీ కంట్రోల్ రూమ్ నుండి, ప్రత్యేక తరగతి గది కోడ్‌ను చూడటానికి "విద్యార్థులను నమోదు చేయండి"పై క్లిక్ చేయండి. ఈ కోడ్‌ను మీ విద్యార్థులతో పంచుకోండి. విద్యార్థులు కోడ్‌ను నమోదు చేయడం ద్వారా తక్షణమే మీ తరగతితో లింక్ అవుతారు.'
          : 'From your Control Room, click "Enroll Students" to view your unique classroom join code. Share this code with your students directly or copy the enrolment link. Students enter the code in their own dashboard to link their progress data to your class view instantly.',
    },
    {
      category: 'For Teachers',
      q:
        lang === 'hi'
          ? 'शिक्षक हस्तक्षेप संकलक (Intervention Compiler) क्या है?'
          : lang === 'te'
          ? 'ఉపాధ్యాయ జోక్య సంకలనం (Intervention Compiler) అంటే ఏమిటి?'
          : 'What is the Teacher Intervention Compiler?',
      a:
        lang === 'hi'
          ? 'हस्तक्षेप संकलक कक्षा के सभी विद्यार्थियों के वास्तविक नैदानिक साक्ष्यों को एकत्रित करता है और सुझाई गई गतिविधियों और समय आवंटन के साथ उन्हें 4 छोटे समूहों में समूहीकृत करता है। शिक्षकों के पास योजनाओं को स्वीकृत करने, संशोधित करने या खारिज करने का 100% अधिकार होता है।'
          : lang === 'te'
          ? 'ఇంటర్‌వెన్షన్ కంపైలర్ మీ తరగతిలోని విద్యార్థులందరి వాస్తవ నిర్ధారణ సాక్ష్యాలను సేకరించి, సూచించిన కార్యకలాపాలు మరియు సమయంతో 4 చిన్న బృందాలుగా విభజిస్తుంది. ప్రణాళికలను ఆమోదించడానికి, సవరించడానికి లేదా తిరస్కరించడానికి ఉపాధ్యాయులకు పూర్తి అధికారం ఉంటుంది.'
          : 'The Intervention Compiler aggregates real diagnostic evidence across all students in your class and groups them into small-group pods with suggested activities and time allocations. You retain complete professional authority — you can approve a suggested plan with one click, modify the duration or activity, reassign students between pods, or dismiss a suggestion entirely. Nothing happens in your classroom without your approval.',
    },
    {
      category: 'For Teachers',
      q:
        lang === 'hi'
          ? '"सजीव समूह पुनः संकलित करें" (Recompile Live Pods) क्या करता है?'
          : lang === 'te'
          ? '"ప్రత్యక్ష బృందాలను రీకంపైల్ చేయండి" (Recompile Live Pods) ఏమి చేస్తుంది?'
          : 'What does "Recompile Live Pods" do?',
      a:
        lang === 'hi'
          ? 'रीकंपाइल आपके विद्यार्थियों के सबसे हालिया प्रयासों पर नैदानिक नियमों को फिर से चलाता है। जब विद्यार्थी नए प्रश्न हल कर लें, तो अद्यतन समूह सुझाव प्राप्त करने के लिए इसका उपयोग करें।'
          : lang === 'te'
          ? 'రీకంపైల్ మీ తరగతిలోని విద్యార్థుల తాజా ప్రయత్నాల ఆధారంగా నిర్ధారణ ఇంజిన్‌ను మళ్లీ అమలు చేస్తుంది. విద్యార్థులు తాజా అభ్యాసాన్ని పూర్తి చేసిన తర్వాత నవీకరించబడిన బృంద సూచనలను పొందడానికి దీన్ని ఉపయోగించండి.'
          : 'Recompile runs the diagnostic engine again on the most recent student attempt data from your class. Use this after students have completed a new round of practice to get updated pod suggestions that reflect their latest evidence. The previous suggestions are replaced with the new ones.',
    },
    {
      category: 'For Teachers',
      q:
        lang === 'hi'
          ? 'स्कूल प्रशासन के लिए औपचारिक पाठ योजना कैसे प्रिंट करें?'
          : lang === 'te'
          ? 'పాఠశాల పరిపాలన కోసం అధికారిక పాఠ్య ప్రణాళికను ఎలా ప్రింట్ చేయాలి?'
          : 'How do I print a formal lesson plan for school administration?',
      a:
        lang === 'hi'
          ? 'स्वच्छ, मुद्रण योग्य विभेदित अनुदेशन योजना बनाने के लिए अपने नियंत्रण कक्ष में "योजना निर्यात करें" पर क्लिक करें। इसमें समूह कार्य, गतिविधि विवरण, समय आवंटन और आपकी व्यक्तिगत टिप्पणियाँ शामिल होती हैं।'
          : lang === 'te'
          ? 'ముద్రించదగిన విభజిత బోధనా ప్రణాళికను రూపొందించడానికి మీ కంట్రోల్ రూమ్‌లో "ప్రణాళికను ఎగుమతి చేయండి"పై క్లిక్ చేయండి. ఇందులో విద్యార్థుల బృందాలు, కార్యాచరణ వివరాలు మరియు మీ గమనికలు ఉంటాయి.'
          : 'Click "Print Intervention Briefing" in your Control Room to generate a clean, printable Differentiated Instruction Plan. It includes student pod assignments, activity descriptions, time allocations, and your personal teacher notes — formatted to meet CBSE inspection documentation standards.',
    },
    {
      category: 'For Teachers',
      q:
        lang === 'hi'
          ? 'क्या मैं किसी व्यक्तिगत विद्यार्थी का सीखने का इतिहास देख सकता हूँ?'
          : lang === 'te'
          ? 'నేను ఒక వ్యక్తిగత విద్యార్థి అభ్యాస చరిత్రను పరిశీలించవచ్చా?'
          : 'Can I inspect an individual student\'s learning history?',
      a:
        lang === 'hi'
          ? 'हाँ। कक्षा साक्ष्य स्पंदन पैनल में किसी भी विद्यार्थी के नाम या कोड पर क्लिक करें। एक विस्तृत शिक्षार्थी फ़ाइल (Dossier) खुलती है जिसमें उनके प्रत्येक प्रयास का इतिहास, दिए गए उत्तर और लागू नैदानिक नियम दिखाई देते हैं।'
          : lang === 'te'
          ? 'అవును. తరగతి సాక్ష్య పల్స్ ప్యానెల్‌లోని ఏదైనా విద్యార్థి పేరు లేదా కోడ్‌పై క్లిక్ చేయండి. వారి ప్రతి ప్రయత్నం, ఇచ్చిన సమాధానం మరియు నిర్ధారణ నియమాన్ని చూపే వివరణాత్మక లెర్నర్ డోసియర్ తెరుచుకుంటుంది.'
          : 'Yes. Click on any student name or code in the Classroom Evidence Pulse panel. A detailed Learner Dossier opens showing their question-by-question attempt history: the prompt presented, the response they gave, the diagnostic rule triggered, and their current mastery percentage. Everything is transparent and auditable.',
    },
    {
      category: 'Platform',
      q:
        lang === 'hi'
          ? 'PRISM किन विषयों और कक्षाओं का समर्थन करता है?'
          : lang === 'te'
          ? 'PRISM ఏ సబ్జెక్టులు మరియు తరగతులకు మద్దతు ఇస్తుంది?'
          : 'Which subjects and grades does PRISM support?',
      a:
        lang === 'hi'
          ? 'PRISM वर्तमान में सीबीएसई कक्षा 8 गणित के सभी 8 अध्यायों (परिमेय संख्याएँ, रैखिक समीकरण, चतुर्भुज, डेटा प्रबंधन, आदि) को कवर करता है। इसका अनुकूली इंजन कक्षा 6 से 10 तक गणित और विज्ञान में विस्तार योग्य है।'
          : lang === 'te'
          ? 'PRISM ప్రస్తుతం CBSE 8వ తరగతి గణితంలోని మొత్తం 8 అధ్యాయాలను కవర్ చేస్తుంది. ఈ అడాప్టివ్ ఇంజిన్ 6 నుండి 10వ తరగతుల వరకు గణితం మరియు సైన్స్‌కు విస్తరించడానికి రూపొందించబడింది.'
          : 'PRISM currently covers CBSE Class VIII Mathematics — all 8 chapters from the NCERT syllabus including Rational Numbers, Linear Equations, Quadrilaterals, Data Handling, Squares & Square Roots, Cubes & Cube Roots, and Comparing Quantities. The adaptive engine and prerequisite concept graph are designed to extend to Classes 6–10 across mathematics and science.',
    },
    {
      category: 'Platform',
      q:
        lang === 'hi'
          ? 'PRISM किन भाषाओं का समर्थन करता है?'
          : lang === 'te'
          ? 'PRISM ఏ భాషలకు మద్దతు ఇస్తుంది?'
          : 'Which languages does PRISM support?',
      a:
        lang === 'hi'
          ? 'PRISM अंग्रेजी, हिंदी (हिंदी) और तेलुगु (తెలుగు) का पूर्ण समर्थन करता है। शीर्ष नेविगेशन बार में भाषा चयनकर्ता का उपयोग करके किसी भी समय भाषा बदलें। नैदानिक प्रतिक्रिया, गतिविधि निर्देश और सभी बटन आपकी चुनी हुई भाषा में अनुकूलित होते हैं।'
          : lang === 'te'
          ? 'PRISM ఇంగ్లీష్, హిందీ (हिंदी) మరియు తెలుగు (తెలుగు) భాషలకు పూర్తి మద్దతు ఇస్తుంది. ఎగువ నావిగేషన్ బార్‌లోని భాషా ఎంపికను ఉపయోగించి ఎప్పుడైనా భాషలను మార్చుకోవచ్చు. సూచనలు, బటన్‌లు అన్నీ మీరు ఎంచుకున్న భాషకు అనుగుణంగా మారతాయి.'
          : 'PRISM supports English, Hindi (हिंदी), and Telugu (తెలుగు). Switch between languages at any time using the language selector in the top navigation bar. Diagnostic feedback, activity instructions, and button labels all adapt to your selected language.',
    },
  ];

  const categories = Array.from(new Set(faqs.map((f) => f.category)));

  return (
    <div className="aeo-faq-page-container">
      <div className="page-header">
        <span className="eyebrow">{t.faqEyebrow}</span>
        <h1>{t.faqTitle}</h1>
        <p>{t.faqSub}</p>
      </div>

      {categories.map((cat) => (
        <div key={cat} style={{ marginBottom: '32px' }}>
          <h3 style={{ color: '#6d28d9', fontSize: '14px', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '12px', paddingBottom: '8px', borderBottom: '2px solid #ede9fe' }}>
            {cat === 'For Students' ? t.catStudents : cat === 'For Teachers' ? t.catTeachers : t.catPlatform}
          </h3>
          <div className="faq-list">
            {faqs.filter((f) => f.category === cat).map((faq, i) => {
              const globalIdx = faqs.indexOf(faq);
              const isOpen = openIdx === globalIdx;
              return (
                <div key={i} className={`faq-accordion-item ${isOpen ? 'open' : ''}`}>
                  <button
                    type="button"
                    className="faq-question-btn"
                    onClick={() => setOpenIdx(isOpen ? null : globalIdx)}
                  >
                    <span>{faq.q}</span>
                    {isOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                  </button>

                  {isOpen && (
                    <div className="faq-answer-box">
                      <p>{faq.a}</p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      ))}

      <div className="geo-resource-box">
        <h4>{t.faqStillQuestions}</h4>
        <p>{t.faqStillQuestionsSub}</p>
      </div>
    </div>
  );
}
