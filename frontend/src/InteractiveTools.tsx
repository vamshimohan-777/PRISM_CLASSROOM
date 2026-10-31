import { useState } from 'react';
import { CheckCircle2, Sparkles, Scale, Split, Calculator, Utensils } from 'lucide-react';
import { Language } from './translations';

interface Props {
  lang: Language;
}

export function VisualFractionBarWorkbench({ lang }: Props) {
  const [f1Num, setF1Num] = useState(1);
  const [f1Den, setF1Den] = useState(3);
  const [f2Num, setF2Num] = useState(1);
  const [f2Den, setF2Den] = useState(8);

  const val1 = f1Num / f1Den;
  const val2 = f2Num / f2Den;
  const isEquivalent = Math.abs(val1 - val2) < 0.0001;
  const isF1Larger = val1 > val2;

  return (
    <div className="interactive-tool-card visual-workbench">
      <div className="tool-header">
        <div className="tool-title-row">
          <Scale className="tool-icon" size={20} />
          <div>
            <h4>
              {lang === 'hi'
                ? 'तुलना कार्यक्षेत्र: भिन्न पट्टियाँ (Fraction Bar Comparator)'
                : lang === 'te'
                ? 'పోలిక వర్క్‌బెంచ్: భిన్నాల పట్టీలు (Fraction Bar Comparator)'
                : 'Interactive Visual Fraction Bar Comparator'}
            </h4>
            <p>
              {lang === 'hi'
                ? 'एक ही इकाई को अलग-अलग भागों में बांटकर देखें कि हर (Denominator) बड़ा होने पर प्रत्येक भाग छोटा क्यों हो जाता है।'
                : lang === 'te'
                ? 'ఒకే యూనిట్‌ను వేర్వేరు భాగాలుగా విభజించి, హారం (Denominator) పెద్దదైనప్పుడు ప్రతి భాగం ఎందుకు చిన్నదవుతుందో చూడండి.'
                : 'See how the whole is partitioned. Notice that dividing into more pieces makes each individual piece narrower!'}
            </p>
          </div>
        </div>
        <span className="badge-pill purple">
          <Sparkles size={13} /> {lang === 'hi' ? 'दृश्य प्रमाण' : lang === 'te' ? 'దృశ్య నిరూపణ' : 'Visual Proof'}
        </span>
      </div>

      <div className="comparison-container">
        {/* Fraction 1 Strip */}
        <div className="fraction-strip-block">
          <div className="strip-controls">
            <span className="fraction-label">
              Fraction A: <b>{f1Num}/{f1Den}</b> ({(val1 * 100).toFixed(1)}%)
            </span>
            <div className="button-group">
              <label>Numerator:
                <select value={f1Num} onChange={(e) => setF1Num(Number(e.target.value))}>
                  {[1, 2, 3, 4, 5, 6].map((n) => (
                    <option key={n} value={n} disabled={n > f1Den}>
                      {n}
                    </option>
                  ))}
                </select>
              </label>
              <label>Denominator:
                <select value={f1Den} onChange={(e) => {
                  const d = Number(e.target.value);
                  setF1Den(d);
                  if (f1Num > d) setF1Num(d);
                }}>
                  {[2, 3, 4, 5, 6, 8, 10, 12].map((d) => (
                    <option key={d} value={d}>{d} parts</option>
                  ))}
                </select>
              </label>
            </div>
          </div>

          <div className="visual-strip" title={`${f1Num} of ${f1Den} equal parts`}>
            {Array.from({ length: f1Den }).map((_, i) => (
              <div
                key={i}
                className={`strip-slice ${i < f1Num ? 'shaded purple' : 'unshaded'}`}
                style={{ width: `${100 / f1Den}%` }}
              >
                1/{f1Den}
              </div>
            ))}
          </div>
        </div>

        {/* Fraction 2 Strip */}
        <div className="fraction-strip-block">
          <div className="strip-controls">
            <span className="fraction-label">
              Fraction B: <b>{f2Num}/{f2Den}</b> ({(val2 * 100).toFixed(1)}%)
            </span>
            <div className="button-group">
              <label>Numerator:
                <select value={f2Num} onChange={(e) => setF2Num(Number(e.target.value))}>
                  {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
                    <option key={n} value={n} disabled={n > f2Den}>
                      {n}
                    </option>
                  ))}
                </select>
              </label>
              <label>Denominator:
                <select value={f2Den} onChange={(e) => {
                  const d = Number(e.target.value);
                  setF2Den(d);
                  if (f2Num > d) setF2Num(d);
                }}>
                  {[2, 3, 4, 5, 6, 8, 10, 12].map((d) => (
                    <option key={d} value={d}>{d} parts</option>
                  ))}
                </select>
              </label>
            </div>
          </div>

          <div className="visual-strip" title={`${f2Num} of ${f2Den} equal parts`}>
            {Array.from({ length: f2Den }).map((_, i) => (
              <div
                key={i}
                className={`strip-slice ${i < f2Num ? 'shaded teal' : 'unshaded'}`}
                style={{ width: `${100 / f2Den}%` }}
              >
                1/{f2Den}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Conceptual Insight */}
      <div className={`conceptual-verdict ${isEquivalent ? 'equivalent-glow' : ''}`}>
        {isEquivalent ? (
          <div className="verdict-content match">
            <CheckCircle2 size={24} className="success-icon" />
            <div>
              <strong>
                {lang === 'hi'
                  ? `तुल्य भिन्न! (Equivalent Fractions): ${f1Num}/${f1Den} = ${f2Num}/${f2Den}`
                  : lang === 'te'
                  ? `సమతుల్య భిన్నాలు! (Equivalent Fractions): ${f1Num}/${f1Den} = ${f2Num}/${f2Den}`
                  : `Equivalent Rational Numbers! ${f1Num}/${f1Den} = ${f2Num}/${f2Den}`}
              </strong>
              <p>
                {lang === 'hi'
                  ? 'यद्यपि भाग अलग-अलग हैं, दोनों पट्टियों में रंगा हुआ कुल क्षेत्रफल बिल्कुल बराबर है!'
                  : lang === 'te'
                  ? 'భాగాలు వేర్వేరుగా ఉన్నప్పటికీ, రెండు పట్టీలలో షేడ్ చేయబడిన మొత్తం వైశాల్యం ఖచ్చితంగా సమానం!'
                  : 'Even though the number of cuts is different, both shaded regions cover the exact same amount of the whole!'}
              </p>
            </div>
          </div>
        ) : (
          <div className="verdict-content comparison">
            <span className="verdict-math">
              {f1Num}/{f1Den} {isF1Larger ? '>' : '<'} {f2Num}/{f2Den}
            </span>
            <p>
              {lang === 'hi' ? (
                <>
                  <b>मुख्य संकल्पना:</b> 1/{Math.max(f1Den, f2Den)} का भाग 1/{Math.min(f1Den, f2Den)} के भाग से{' '}
                  <b>छोटा</b> है क्योंकि पूरी पट्टी को अधिक टुकड़ों में काटा गया है।
                </>
              ) : lang === 'te' ? (
                <>
                  <b>ముఖ్య భావన:</b> 1/{Math.max(f1Den, f2Den)} భాగం 1/{Math.min(f1Den, f2Den)} భాగం కంటే{' '}
                  <b>చిన్నది</b>, ఎందుకంటే మొత్తం పట్టీని ఎక్కువ భాగాలుగా విభజించారు.
                </>
              ) : (
                <>
                  <b>Key Concept:</b> Each 1/{Math.max(f1Den, f2Den)} slice is <b>narrower</b> than each 1/{Math.min(f1Den, f2Den)} slice because the whole was divided into more pieces. A bigger denominator means <i>smaller</i> pieces!
                </>
              )}
            </p>
          </div>
        )}
      </div>

      <div className="preset-buttons">
        <span>{lang === 'hi' ? 'त्वरित तुलना:' : lang === 'te' ? 'త్వరిత పోలిక:' : 'Quick Presets:'}</span>
        <button
          type="button"
          onClick={() => {
            setF1Num(1); setF1Den(3); setF2Num(1); setF2Den(8);
          }}
        >
          Compare 1/3 vs 1/8
        </button>
        <button
          type="button"
          onClick={() => {
            setF1Num(1); setF1Den(2); setF2Num(2); setF2Den(4);
          }}
        >
          Equivalence 1/2 = 2/4
        </button>
        <button
          type="button"
          onClick={() => {
            setF1Num(2); setF1Den(3); setF2Num(4); setF2Den(6);
          }}
        >
          Equivalence 2/3 = 4/6
        </button>
      </div>
    </div>
  );
}

export function FoundationStripWorkbench({ lang }: Props) {
  const [parts, setParts] = useState(6);
  const [shaded, setShaded] = useState(3);

  return (
    <div className="interactive-tool-card foundation-workbench">
      <div className="tool-header">
        <div className="tool-title-row">
          <Split className="tool-icon" size={20} />
          <div>
            <h4>
              {lang === 'hi'
                ? 'बुनियादी संकल्पना: भिन्न की संरचना (Fraction Anatomy & Equal Parts)'
                : lang === 'te'
                ? 'పునాది భావన: భిన్నం నిర్మాణం (Fraction Anatomy & Equal Parts)'
                : 'Fraction Anatomy & Equal-Part Partitioning'}
            </h4>
            <p>
              {lang === 'hi'
                ? 'भिन्न तभी मान्य होती है जब सभी भाग आकार में बिल्कुल समान हों।'
                : lang === 'te'
                ? 'అన్ని భాగాలు పరిమాణంలో ఖచ్చితంగా సమానంగా ఉన్నప్పుడు మాత్రమే భిన్నం చెల్లుబాటు అవుతుంది.'
                : 'A fraction represents equal shares of a unit. Click parts below to shade or unshade.'}
            </p>
          </div>
        </div>
      </div>

      <div className="anatomy-interactive">
        <div className="anatomy-strip-container">
          <div className="interactive-strip">
            {Array.from({ length: parts }).map((_, i) => (
              <button
                type="button"
                key={i}
                className={`slice-toggle ${i < shaded ? 'active' : ''}`}
                style={{ width: `${100 / parts}%` }}
                onClick={() => setShaded(i + 1 === shaded ? i : i + 1)}
                title={`Part ${i + 1} of ${parts}`}
              >
                Part {i + 1}
              </button>
            ))}
          </div>
          <div className="partition-controls">
            <label>
              Divide strip into equal parts (Denominator):
              <div className="pill-selector">
                {[2, 3, 4, 6, 8, 10].map((p) => (
                  <button
                    type="button"
                    key={p}
                    className={parts === p ? 'selected' : ''}
                    onClick={() => {
                      setParts(p);
                      if (shaded > p) setShaded(p);
                    }}
                  >
                    {p} parts
                  </button>
                ))}
              </div>
            </label>
          </div>
        </div>

        <div className="fraction-anatomy-display">
          <div className="fraction-vertical">
            <span className="numerator-highlight" title="Numerator: Shaded equal parts selected">
              {shaded}
            </span>
            <hr className="fraction-bar-line" />
            <span className="denominator-highlight" title="Denominator: Total equal parts in whole">
              {parts}
            </span>
          </div>
          <div className="anatomy-legend">
            <div>
              <b className="purple-text">
                {lang === 'hi' ? 'अंश (Numerator): ' : lang === 'te' ? 'లవం (Numerator): ' : 'Numerator: '}
              </b>
              <span>{shaded} {lang === 'hi' ? 'चुने गए समान भाग' : lang === 'te' ? 'ఎంచుకున్న సమాన భాగాలు' : 'equal parts selected'}</span>
            </div>
            <div>
              <b className="teal-text">
                {lang === 'hi' ? 'हर (Denominator): ' : lang === 'te' ? 'హారం (Denominator): ' : 'Denominator: '}
              </b>
              <span>{parts} {lang === 'hi' ? 'कुल समान भागों की संख्या' : lang === 'te' ? 'మొత్తం సమాన భాగాల సంఖ్య' : 'total equal parts making the whole'}</span>
            </div>
            <div className="simplification-note">
              {shaded === parts / 2 && parts % 2 === 0 && (
                <span className="badge-pill green">
                  💡 {shaded}/{parts} simplifies to <b>1/2</b> (One half of the whole strip)
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function GuidedPracticeWorkbench({ lang }: Props) {
  const [multiplier, setMultiplier] = useState(2);
  const baseNum = 3;
  const baseDen = 5;

  return (
    <div className="interactive-tool-card guided-workbench">
      <div className="tool-header">
        <div className="tool-title-row">
          <Calculator className="tool-icon" size={20} />
          <div>
            <h4>
              {lang === 'hi'
                ? 'मार्गदर्शित अभ्यास: समतुल्य गुणन ग्रिड (Equivalent Multiplier Grid)'
                : lang === 'te'
                ? 'మార్గదర్శక సాధన: సమతుల్య గుణకార గ్రిడ్ (Equivalent Multiplier Grid)'
                : 'Scaffolded Multiplication & Simplification Grid'}
            </h4>
            <p>
              {lang === 'hi'
                ? 'अंश और हर दोनों को एक ही गैर-शून्य संख्या से गुणा करने पर तुल्य भिन्न प्राप्त होती है।'
                : lang === 'te'
                ? 'లవం మరియు హారం రెండింటినీ ఒకే శూన్యేతర సంఖ్యతో గుణించినప్పుడు సమతుల్య భిన్నం వస్తుంది.'
                : 'Multiply numerator and denominator by the SAME non-zero integer (multiplying by 1 in disguise).'}
            </p>
          </div>
        </div>
      </div>

      <div className="multiplier-grid">
        <div className="grid-formula">
          <div className="fraction-box">
            <span className="num">{baseNum}</span>
            <hr />
            <span className="den">{baseDen}</span>
          </div>

          <span className="op">×</span>

          <div className="fraction-box multiplier-box">
            <span className="num highlight">{multiplier}</span>
            <hr />
            <span className="den highlight">{multiplier}</span>
          </div>

          <span className="op">=</span>

          <div className="fraction-box result-box">
            <span className="num result">{baseNum * multiplier}</span>
            <hr />
            <span className="den result">{baseDen * multiplier}</span>
          </div>
        </div>

        <div className="multiplier-stepper">
          <span>Choose common factor (k):</span>
          <div className="pill-selector">
            {[2, 3, 4, 5].map((k) => (
              <button
                type="button"
                key={k}
                className={multiplier === k ? 'selected' : ''}
                onClick={() => setMultiplier(k)}
              >
                k = {k}
              </button>
            ))}
          </div>
        </div>

        <div className="rule-explanation">
          <CheckCircle2 size={18} className="success-icon" />
          <span>
            {lang === 'hi'
              ? `चूंकि ${multiplier}/${multiplier} = 1 है, इसलिए ${baseNum}/${baseDen} का मूल्य नहीं बदलता। अत: ${baseNum}/${baseDen} और ${baseNum * multiplier}/${baseDen * multiplier} तुल्य हैं!`
              : lang === 'te'
              ? `${multiplier}/${multiplier} = 1 కాబట్టి, ${baseNum}/${baseDen} యొక్క విలువ మారదు. కాబట్టి ${baseNum}/${baseDen} మరియు ${baseNum * multiplier}/${baseDen * multiplier} సమతుల్య భిన్నాలు!`
              : `Because ${multiplier}/${multiplier} equals 1, multiplying by it does not change the actual value. Therefore, ${baseNum}/${baseDen} and ${baseNum * multiplier}/${baseDen * multiplier} are equivalent!`}
          </span>
        </div>
      </div>
    </div>
  );
}

export function ExtensionRecipeWorkbench({ lang }: Props) {
  const [servings, setServings] = useState(8);
  const baseServings = 4;
  const baseMilkSixths = 4; // 2/3 cup = 4/6 cup

  // Scaling factor
  const factor = servings / baseServings;
  const scaledSixths = Math.round(baseMilkSixths * factor);

  return (
    <div className="interactive-tool-card extension-workbench">
      <div className="tool-header">
        <div className="tool-title-row">
          <Utensils className="tool-icon" size={20} />
          <div>
            <h4>
              {lang === 'hi'
                ? 'विस्तार चुनौती: कक्षा 8 रसोई प्रयोगशाला (Recipe Scaling Lab)'
                : lang === 'te'
                ? 'విస్తరణ సవాలు: తరగతి 8 వంటశాల ల్యాబ్ (Recipe Scaling Lab)'
                : 'Class VIII Kitchen Lab: Recipe Proportion Scaling'}
            </h4>
            <p>
              {lang === 'hi'
                ? 'वास्तविक जीवन में तुल्य परिमेय संख्याओं का उपयोग: विभिन्न अतिथियों के लिए रेसिपी का पैमाना बदलना।'
                : lang === 'te'
                ? 'నిజ జీవితంలో సమతుల్య అకరణీయ సంఖ్యల ఉపయోగం: వేర్వేరు వ్యక్తుల కోసం వంటకాల పరిమాణాన్ని మార్చడం.'
                : 'Real-life NCERT application: Scale Grandma’s Payasam recipe using equivalent rational proportions.'}
            </p>
          </div>
        </div>
        <span className="badge-pill gold">
          <Sparkles size={13} /> {lang === 'hi' ? 'उच्च दक्षता' : lang === 'te' ? 'ఉన్నత నైపుణ్యం' : 'Mastery Route'}
        </span>
      </div>

      <div className="recipe-simulator">
        <div className="recipe-card">
          <h5>Grandmother's Special Payasam (Base: 4 Servings)</h5>
          <ul>
            <li>Milk: <b>2/3 cup</b> (which is equivalent to <b>4/6 cup</b>)</li>
            <li>Rice: <b>1/4 cup</b> (which is equivalent to <b>2/8 cup</b>)</li>
            <li>Jaggery: <b>1/2 cup</b> (which is equivalent to <b>3/6 cup</b>)</li>
          </ul>
        </div>

        <div className="servings-slider-block">
          <label>
            Scale for guests: <b>{servings} people</b> (Scale multiplier: <b>{factor}×</b>)
            <input
              type="range"
              min="2"
              max="16"
              step="2"
              value={servings}
              onChange={(e) => setServings(Number(e.target.value))}
            />
          </label>
        </div>

        <div className="scaled-output">
          <h6>Scaled Recipe for {servings} Servings:</h6>
          <div className="scaled-grid">
            <div className="scaled-item">
              <span>Milk Required:</span>
              <b>
                {scaledSixths}/6 cups = {(scaledSixths / 6).toFixed(2)} cups
              </b>
              <small>Proportion: (2/3) × {factor} = {scaledSixths}/6</small>
            </div>
            <div className="scaled-item">
              <span>Jaggery Required:</span>
              <b>
                {(0.5 * factor).toFixed(2)} cups
              </b>
              <small>Proportion: (1/2) × {factor}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

