import { Language } from './translations';

// ----------------------------------------------------
// CBSE Class VIII 8 Chapters Localization
// ----------------------------------------------------
export interface ChapterTranslation {
  title: Record<Language, string>;
  summary: Record<Language, string>;
}

export const CHAPTER_TRANSLATIONS: Record<string, ChapterTranslation> = {
  'rational-numbers': {
    title: {
      en: 'Rational Numbers',
      hi: 'परिमेय संख्याएँ (Rational Numbers)',
      te: 'అకరణీయ సంఖ్యలు (Rational Numbers)',
    },
    summary: {
      en: 'Compare, simplify, and represent rational numbers.',
      hi: 'परिमेय संख्याओं की तुलना, सरलीकरण और निरूपण करें।',
      te: 'అకరణీయ సంఖ్యలను పోల్చడం, సరళీకరించడం మరియు సూచించడం.',
    },
  },
  'linear-equations': {
    title: {
      en: 'Linear Equations in One Variable',
      hi: 'एक चर वाले रैखिक समीकरण (Linear Equations)',
      te: 'ఏక చరరాశిలో రేఖీయ సమీకరణాలు (Linear Equations)',
    },
    summary: {
      en: 'Model and solve everyday equations.',
      hi: 'दैनिक जीवन के रैखिक समीकरणों का मॉडल बनाएं और हल करें।',
      te: 'రోజువారీ జీవితంలోని రేఖీయ సమీకరణాలను రూపొందించి సాధించండి.',
    },
  },
  'quadrilaterals': {
    title: {
      en: 'Understanding Quadrilaterals',
      hi: 'चतुर्भुजों को समझना (Quadrilaterals)',
      te: 'చతుర్భుజాలను అర్థం చేసుకోవడం (Quadrilaterals)',
    },
    summary: {
      en: 'Classify shapes and reason with angle sums.',
      hi: 'आकृतियों का वर्गीकरण करें और कोणों के योग के नियमों से तर्क करें।',
      te: 'ఆకారాలను వర్గీకరించి, కోణాల మొత్తం నియమాలతో సాధించండి.',
    },
  },
  'practical-geometry': {
    title: {
      en: 'Practical Geometry',
      hi: 'प्रायोगिक ज्यामिति (Practical Geometry)',
      te: 'ప్రాయోగిక జ్యామితి (Practical Geometry)',
    },
    summary: {
      en: 'Construct quadrilaterals from precise information.',
      hi: 'सटीक जानकारी से चतुर्भुजों की रचना करें।',
      te: 'ఖచ్చితమైన కొలతలతో చతుర్భుజాలను నిర్మించండి.',
    },
  },
  'data-handling': {
    title: {
      en: 'Data Handling',
      hi: 'आँकड़ों का प्रबंधन (Data Handling)',
      te: 'దత్తాంశ నిర్వహణ (Data Handling)',
    },
    summary: {
      en: 'Read graphs and use probability language.',
      hi: 'आलेख पढ़ें और प्रायिकता की भाषा का उपयोग करें।',
      te: 'గ్రాఫ్‌లను చదివి సంభావ్యత భావనలను ఉపయోగించండి.',
    },
  },
  'squares-roots': {
    title: {
      en: 'Squares and Square Roots',
      hi: 'वर्ग और वर्गमूल (Squares & Roots)',
      te: 'వర్గాలు మరియు వర్గమూలాలు (Squares & Roots)',
    },
    summary: {
      en: 'Recognise square numbers and find roots.',
      hi: 'पूर्ण वर्ग संख्याओं को पहचानें और वर्गमूल निकालें।',
      te: 'వర్గ సంఖ్యలను గుర్తించి వర్గమూలాలను కనుగొనండి.',
    },
  },
  'cubes-roots': {
    title: {
      en: 'Cubes and Cube Roots',
      hi: 'घन और घनमूल (Cubes & Roots)',
      te: 'ఘనాలు మరియు ఘనమూలాలు (Cubes & Roots)',
    },
    summary: {
      en: 'Explore cubes, patterns, and cube roots.',
      hi: 'घन, पैटर्न और घनमूल की जांच करें।',
      te: 'ఘనాలు, నమూనాలు మరియు ఘనమూలాలను అన్వేషించండి.',
    },
  },
  'comparing-quantities': {
    title: {
      en: 'Comparing Quantities',
      hi: 'राशियों की तुलना (Comparing Quantities)',
      te: 'రాశులను పోల్చడం (Comparing Quantities)',
    },
    summary: {
      en: 'Use percentages, profit, loss, and discount.',
      hi: 'प्रतिशत, लाभ, हानि और छूट का उपयोग करें।',
      te: 'శాతాలు, లాభం, నష్టం మరియు తగ్గింపులను ఉపయోగించండి.',
    },
  },
};

export function getLocalizedChapterTitle(id: string, defaultTitle: string, lang: Language): string {
  return CHAPTER_TRANSLATIONS[id]?.title[lang] || defaultTitle;
}

export function getLocalizedChapterSummary(id: string, defaultSummary: string, lang: Language): string {
  return CHAPTER_TRANSLATIONS[id]?.summary[lang] || defaultSummary;
}

// ----------------------------------------------------
// Question Prompts & Explanations Localization
// ----------------------------------------------------
interface QuestionText {
  prompt: Record<Language, string>;
  explanation?: Record<Language, string>;
}

export const QUESTION_TRANSLATIONS: Record<string, QuestionText> = {
  // Equivalent Fractions / Rational Numbers
  'diag-equivalent': {
    prompt: {
      en: 'Which fraction is equivalent to 1/2?',
      hi: '1/2 के समतुल्य कौन सा भिन्न है?',
      te: '1/2 కి సమానమైన భిన్నం ఏది?',
    },
    explanation: {
      en: 'Multiplying the numerator and denominator of 1/2 by 2 gives 2/4.',
      hi: '1/2 के अंश और हर दोनों को 2 से गुणा करने पर 2/4 प्राप्त होता है।',
      te: '1/2 యొక్క లవం మరియు హారాలను 2 తో గుణిస్తే 2/4 వస్తుంది.',
    },
  },
  'diag-magnitude': {
    prompt: {
      en: 'Which is greater?',
      hi: 'कौन सा भिन्न बड़ा है?',
      te: 'ఏది పెద్దది?',
    },
    explanation: {
      en: 'With the same numerator, the fraction with fewer equal parts is greater (1/3 > 1/8).',
      hi: 'समान अंश होने पर, कम भागों वाला भिन्न बड़ा होता है (1/3 > 1/8)।',
      te: 'లవం సమానంగా ఉన్నప్పుడు, తక్కువ భాగాలున్న భిన్నం పెద్దది (1/3 > 1/8).',
    },
  },
  'diag-simplify': {
    prompt: {
      en: 'Write -18/24 in standard form.',
      hi: '-18/24 को मानक रूप में लिखें।',
      te: '-18/24 ను ప్రామాణిక రూపంలో రాయండి.',
    },
    explanation: {
      en: 'Divide numerator and denominator by 6 and keep the negative sign: -18/24 = -3/4.',
      hi: 'अंश और हर को 6 से विभाजित करें और ऋण चिह्न रखें: -18/24 = -3/4।',
      te: 'లవం మరియు హారాలను 6 తో భాగించి మైనస్ గుర్తును ఉంచండి: -18/24 = -3/4.',
    },
  },
  'diag-representation': {
    prompt: {
      en: 'A strip is split into 6 equal parts and 3 are shaded. Which matching fraction names the same amount?',
      hi: 'एक पट्टी को 6 समान भागों में बांटा गया है और 3 रंगे हुए हैं। कौन सा भिन्न समान मान दर्शाता है?',
      te: 'ఒక పట్టీని 6 సమాన భాగాలుగా విభజించి, 3 భాగాలను షేడ్ చేశారు. అదే పరిమాణాన్ని సూచించే భిన్నం ఏది?',
    },
    explanation: {
      en: 'Three of six equal parts is one half (3/6 = 1/2).',
      hi: 'छह में से तीन समान भाग आधा (3/6 = 1/2) होता है।',
      te: 'ఆరింటిలో మూడు సమాన భాగాలు సగం (3/6 = 1/2) అవుతుంది.',
    },
  },
  'practice-guided': {
    prompt: {
      en: 'Complete: 3/5 = __/10',
      hi: 'पूर्ण करें: 3/5 = __/10',
      te: 'పూర్తి చేయండి: 3/5 = __/10',
    },
    explanation: {
      en: 'Multiply both numerator and denominator by 2: 3/5 = 6/10.',
      hi: 'अंश और हर दोनों को 2 से गुणा करें: 3/5 = 6/10।',
      te: 'లవం మరియు హారం రెండింటినీ 2 తో గుణించండి: 3/5 = 6/10.',
    },
  },
  'practice-standard': {
    prompt: {
      en: 'Which pair names the same rational number?',
      hi: 'कौन सा युग्म समान परिमेय संख्या को दर्शाता है?',
      te: 'ఏ జత ఒకే అకరణీయ సంఖ్యను సూచిస్తుంది?',
    },
    explanation: {
      en: 'A negative sign in either term makes the rational number negative: 6/-8 = -3/4.',
      hi: 'किसी भी पद में ऋण चिह्न होने पर परिमेय संख्या ऋणात्मक होती है: 6/-8 = -3/4।',
      te: 'లవం లేదా హారంలో మైనస్ ఉన్నా అకరణీయ సంఖ్య రుణాత్మకం: 6/-8 = -3/4.',
    },
  },
  'test-transfer': {
    prompt: {
      en: 'A recipe uses 2/3 cup of milk. Which amount is the same quantity in sixth-cup measures?',
      hi: 'एक रेसिपी में 2/3 कप दूध का उपयोग होता है। छठवें हिस्से में यह मात्रा कितनी होगी?',
      te: 'ఒక వంటకంలో 2/3 కప్పు పాలు వాడతారు. ఆరవ వంతులలో ఇది ఎంత అవుతుంది?',
    },
    explanation: {
      en: 'Multiply 2/3 by 2/2 to write it in sixths: 4/6.',
      hi: 'छठवें हिस्से में लिखने के लिए 2/3 को 2/2 से गुणा करें: 4/6।',
      te: 'ఆరవ వంతులలో రాయడానికి 2/3 ని 2/2 తో గుణించండి: 4/6.',
    },
  },
  // Linear Equations
  'linear-equations-diagnostic-1': {
    prompt: {
      en: 'Solve: 3x + 5 = 20',
      hi: 'हल करें: 3x + 5 = 20',
      te: 'సాధించండి: 3x + 5 = 20',
    },
  },
  'linear-equations-practice-2': {
    prompt: {
      en: 'A number increased by 7 is 19. What is the number?',
      hi: 'किसी संख्या में 7 जोड़ने पर 19 प्राप्त होता है। वह संख्या क्या है?',
      te: 'ఒక సంఖ్యకు 7 కలిపితే 19 వస్తుంది. ఆ సంఖ్య ఏది?',
    },
  },
  'linear-equations-test-3': {
    prompt: {
      en: 'Five identical notebooks cost ₹75. What is the cost of one?',
      hi: 'पाँच एक समान पुस्तिकाओं का मूल्य ₹75 है। एक का मूल्य क्या होगा?',
      te: 'ఐదు ఒకే రకమైన నోట్‌బుక్‌ల ధర ₹75. ఒకదాని ధర ఎంత?',
    },
  },
  // Quadrilaterals
  'quadrilaterals-diagnostic-1': {
    prompt: {
      en: 'What is the sum of interior angles of a quadrilateral?',
      hi: 'एक चतुर्भुज के आंतरिक कोणों का योग क्या होता है?',
      te: 'ఒక చతుర్భుజం యొక్క అంతర కోణాల మొత్తం ఎంత?',
    },
  },
  'quadrilaterals-practice-2': {
    prompt: {
      en: 'A quadrilateral with both pairs of opposite sides parallel is a…',
      hi: 'जिस चतुर्भुज की सम्मुख भुजाओं के दोनों युग्म समानांतर हों, वह कहलाता है…',
      te: 'ఎదురెదురు భుజాల జతలు రెండూ సమాంతరంగా ఉన్న చతుర్భుజం…',
    },
  },
  'quadrilaterals-test-3': {
    prompt: {
      en: 'Three angles of a quadrilateral are 90°, 85°, and 110°. The fourth is…',
      hi: 'एक चतुर्भुज के तीन कोण 90°, 85°, और 110° हैं। चौथा कोण क्या होगा?',
      te: 'చతుర్భుజంలోని మూడు కోణాలు 90°, 85° మరియు 110°. నాల్గవ కోణం…',
    },
  },
  // Practical Geometry
  'practical-geometry-diagnostic-1': {
    prompt: {
      en: 'Which tool is used to draw a circle with a fixed radius?',
      hi: 'निश्चित त्रिज्या का वृत्त खींचने के लिए किस उपकरण का उपयोग किया जाता है?',
      te: 'నిర్దిష్ట వ్యాసార్థంతో వృత్తాన్ని గీయడానికి ఏ సాధనాన్ని ఉపయోగిస్తారు?',
    },
  },
  'practical-geometry-practice-2': {
    prompt: {
      en: 'To construct a quadrilateral uniquely, you need…',
      hi: 'एक अद्वितीय चतुर्भुज बनाने के लिए आपको आवश्यकता है…',
      te: 'ప్రత్యేకమైన చతుర్భుజాన్ని నిర్మించడానికి మీకు ఏమి అవసరం…',
    },
  },
  'practical-geometry-test-3': {
    prompt: {
      en: 'Which is most important in a geometry construction?',
      hi: 'ज्यामितीय रचना में सबसे महत्वपूर्ण क्या है?',
      te: 'జ్యామితీయ నిర్మాణంలో అత్యంత ముఖ్యమైనది ఏది?',
    },
  },
  // Data Handling
  'data-handling-diagnostic-1': {
    prompt: {
      en: 'A fair coin is tossed once. Probability of heads is…',
      hi: 'एक निष्पक्ष सिक्का एक बार उछाला जाता है। चित (Heads) आने की प्रायिकता है…',
      te: 'ఒక నాణెం ఒకసారి ఎగురవేస్తే, బొమ్మ (Heads) పడే సంభావ్యత ఎంత…',
    },
  },
  'data-handling-practice-2': {
    prompt: {
      en: 'The mean of 4, 6, and 8 is…',
      hi: '4, 6, और 8 का माध्य (Mean) क्या है?',
      te: '4, 6, మరియు 8 ల సగటు (Mean) ఎంత…',
    },
  },
  'data-handling-test-3': {
    prompt: {
      en: 'A bag has 3 red and 2 blue counters. Probability of blue is…',
      hi: 'एक थैले में 3 लाल और 2 नीले टोकन हैं। नीले टोकन की प्रायिकता है…',
      te: 'ఒక సంచిలో 3 ఎరుపు మరియు 2 నీలం రంగు కౌంటర్లు ఉన్నాయి. నీలం రంగు వచ్చే సంభావ్యత…',
    },
  },
  // Squares and Roots
  'squares-roots-diagnostic-1': {
    prompt: {
      en: 'Which number is a perfect square?',
      hi: 'कौन सी संख्या एक पूर्ण वर्ग (Perfect Square) है?',
      te: 'ఏ సంఖ్య ఖచ్చితమైన వర్గం (Perfect Square) అవుతుంది?',
    },
  },
  'squares-roots-practice-2': {
    prompt: {
      en: 'The square root of 144 is…',
      hi: '144 का वर्गमूल क्या है?',
      te: '144 యొక్క వర్గమూలం ఎంత…',
    },
  },
  'squares-roots-test-3': {
    prompt: {
      en: 'A square tile has area 81 cm². Its side length is…',
      hi: 'एक वर्गाकार टाइल का क्षेत्रफल 81 सेमी² है। इसकी भुजा की लंबाई क्या होगी?',
      te: 'ఒక చతురస్రాకార టైల్ వైశాల్యం 81 సెం.మీ². దాని భుజం పొడవు…',
    },
  },
  // Cubes and Roots
  'cubes-roots-diagnostic-1': {
    prompt: {
      en: 'Which number is a perfect cube?',
      hi: 'कौन सी संख्या एक पूर्ण घन (Perfect Cube) है?',
      te: 'ఏ సంఖ్య ఖచ్చితమైన ఘనం (Perfect Cube) అవుతుంది?',
    },
  },
  'cubes-roots-practice-2': {
    prompt: {
      en: 'The cube root of 64 is…',
      hi: '64 का घनमूल क्या है?',
      te: '64 యొక్క ఘనమూలం ఎంత…',
    },
  },
  'cubes-roots-test-3': {
    prompt: {
      en: 'A cube has volume 125 cm³. Its edge length is…',
      hi: 'एक घन का आयतन 125 सेमी³ है। इसके किनारे की लंबाई क्या होगी?',
      te: 'ఒక ఘనం ఘనపరిమాణం 125 సెం.మీ³. దాని అంచు పొడవు…',
    },
  },
  // Comparing Quantities
  'comparing-quantities-diagnostic-1': {
    prompt: {
      en: '25% as a fraction in simplest form is…',
      hi: '25% का सरलतम भिन्न रूप क्या है?',
      te: '25% యొక్క సరళమైన భిన్న రూపం ఏది…',
    },
  },
  'comparing-quantities-practice-2': {
    prompt: {
      en: 'A ₹500 bag has a 10% discount. The discount is…',
      hi: '₹500 के बैग पर 10% की छूट है। छूट की राशि क्या है?',
      te: '₹500 బ్యాగ్‌పై 10% తగ్గింపు ఉంది. తగ్గింపు మొత్తం ఎంత…',
    },
  },
  'comparing-quantities-test-3': {
    prompt: {
      en: 'A price rises from ₹200 to ₹250. The percentage increase is…',
      hi: 'एक वस्तु का मूल्य ₹200 से बढ़कर ₹250 हो जाता है। प्रतिशत वृद्धि क्या है?',
      te: 'ధర ₹200 నుండి ₹250కి పెరిగింది. పెరిగిన శాతం ఎంత…',
    },
  },
};

export function getLocalizedQuestionPrompt(id: string, defaultPrompt: string, lang: Language): string {
  if (lang === 'en') return defaultPrompt;
  const match = QUESTION_TRANSLATIONS[id];
  if (match?.prompt[lang]) return match.prompt[lang];

  // Fallback pattern matching on prompt text
  for (const q of Object.values(QUESTION_TRANSLATIONS)) {
    if (q.prompt.en.trim() === defaultPrompt.trim() && q.prompt[lang]) {
      return q.prompt[lang];
    }
  }
  return defaultPrompt;
}

export function getLocalizedExplanation(id: string, defaultExp: string | undefined, lang: Language): string {
  if (!defaultExp) return '';
  if (lang === 'en') return defaultExp;
  const match = QUESTION_TRANSLATIONS[id];
  if (match?.explanation && match.explanation[lang]) return match.explanation[lang];
  return defaultExp;
}

// ----------------------------------------------------
// Option Text Localization
// ----------------------------------------------------
export const OPTION_TRANSLATIONS: Record<string, Record<Language, string>> = {
  'They are equal': {
    en: 'They are equal',
    hi: 'वे बराबर हैं',
    te: 'అవి సమానం',
  },
  'kite': {
    en: 'kite',
    hi: 'पतंग (Kite)',
    te: 'గాలిపటం (Kite)',
  },
  'parallelogram': {
    en: 'parallelogram',
    hi: 'समानांतर चतुर्भुज (Parallelogram)',
    te: 'సమాంతర చతుర్భుజం (Parallelogram)',
  },
  'trapezium': {
    en: 'trapezium',
    hi: 'समलंब (Trapezium)',
    te: 'ట్రెపీజియం (Trapezium)',
  },
  'triangle': {
    en: 'triangle',
    hi: 'त्रिभुज (Triangle)',
    te: 'త్రిభుజం (Triangle)',
  },
  'protractor': {
    en: 'protractor',
    hi: 'चांदा (Protractor)',
    te: 'కోణమానిని (Protractor)',
  },
  'compass': {
    en: 'compass',
    hi: 'परकार (Compass)',
    te: 'కంపాస్ (Compass)',
  },
  'ruler': {
    en: 'ruler',
    hi: 'पैमाना (Ruler)',
    te: 'స్కేలు (Ruler)',
  },
  'set square': {
    en: 'set square',
    hi: 'सेट स्क्वायर (Set square)',
    te: 'సెట్ స్క్వేర్ (Set square)',
  },
  'only one side': {
    en: 'only one side',
    hi: 'केवल एक भुजा',
    te: 'ఒకే ఒక భుజం',
  },
  'enough side and angle measurements': {
    en: 'enough side and angle measurements',
    hi: 'पर्याप्त भुजा और कोण माप',
    te: 'సరిపడా భుజాలు మరియు కోణాల కొలతలు',
  },
  'only one angle': {
    en: 'only one angle',
    hi: 'केवल एक कोण',
    te: 'ఒకే ఒక కోణం',
  },
  'its colour': {
    en: 'its colour',
    hi: 'इसका रंग',
    te: 'దాని రంగు',
  },
  'guessing lengths': {
    en: 'guessing lengths',
    hi: 'लंबाइयों का अनुमान लगाना',
    te: 'పొడవులను ఊహించడం',
  },
  'accurate measurement': {
    en: 'accurate measurement',
    hi: 'सटीक मापन',
    te: 'ఖచ్చితమైన కొలత',
  },
  'drawing quickly': {
    en: 'drawing quickly',
    hi: 'जल्दी बनाना',
    te: 'వేగంగా గీయడం',
  },
  'using colour': {
    en: 'using colour',
    hi: 'रंगों का उपयोग',
    te: 'రంగులు ఉపయోగించడం',
  },
};

export function getLocalizedOptionLabel(option: string, lang: Language): string {
  if (lang === 'en') return option;
  return OPTION_TRANSLATIONS[option]?.[lang] || option;
}

