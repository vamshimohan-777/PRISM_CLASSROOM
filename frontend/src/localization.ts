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
  'linear-equations-diagnostic-4': {
    prompt: {
      en: "If 7x = 49, what is x?",
      hi: "यदि 7x = 49 है, तो x का मान क्या है?",
      te: "7x = 49 అయితే x విలువ ఎంత?",
    },
  },
  'linear-equations-practice-5': {
    prompt: {
      en: "The sum of two consecutive integers is 37. The integers are:",
      hi: "दो क्रमागत पूर्णांकों का योग 37 है। वे पूर्णांक हैं:",
      te: "రెండు వరుస పూర్ణాంకాల మొత్తం 37. ఆ పూర్ణాంకాలు:",
    },
  },
  'linear-equations-test-6': {
    prompt: {
      en: "Raju's father is 26 years older than Raju. After 3 years the sum of their ages will be 66. What is Raju's current age?",
      hi: "राजू के पिता राजू से 26 वर्ष बड़े हैं। 3 वर्ष बाद उनकी आयु का योग 66 होगा। राजू की वर्तमान आयु क्या है?",
      te: "రాజు తండ్రి రాజు కంటే 26 సంవత్సరాలు పెద్దవారు. 3 సంవత్సరాల తర్వాత వారి వయసుల మొత్తం 66 అవుతుంది. రాజు ప్రస్తుత వయసు ఎంత?",
    },
  },
  'quadrilaterals-diagnostic-4': {
    prompt: {
      en: "How many sides does a polygon need to have for interior angle sum to be 540°?",
      hi: "अंतः कोणों का योग 540° होने के लिए बहुभुज में कितनी भुजाएँ होनी चाहिए?",
      te: "అంతర కోణాల మొత్తం 540° కావాలంటే బహుభుజికి ఎన్ని భుజాలు ఉండాలి?",
    },
  },
  'quadrilaterals-practice-5': {
    prompt: {
      en: "In a rhombus, the diagonals bisect each other at:",
      hi: "समचतुर्भुज में विकर्ण एक-दूसरे को किस कोण पर समद्विभाजित करते हैं?",
      te: "రాంబస్‌లో కర్ణాలు ఒకదానినొకటి ఏ కోణంలో సమద్విఖండన చేసుకుంటాయి?",
    },
  },
  'quadrilaterals-test-6': {
    prompt: {
      en: "One angle of a parallelogram is 75°. What are the other three angles?",
      hi: "एक समांतर चतुर्भुज का एक कोण 75° है। शेष तीन कोण क्या हैं?",
      te: "సమాంతర చతుర్భుజంలో ఒక కోణం 75°. మిగిలిన మూడు కోణాలు ఏవి?",
    },
  },
  'practical-geometry-diagnostic-4': {
    prompt: {
      en: "To construct a unique quadrilateral ABCD you need at least:",
      hi: "एक अद्वितीय चतुर्भुज ABCD की रचना के लिए कम से कम क्या चाहिए?",
      te: "ఒకే ఒక చతుర్భుజం ABCD నిర్మించడానికి కనీసం ఏమి కావాలి?",
    },
  },
  'practical-geometry-practice-5': {
    prompt: {
      en: "In construction ABCD with AB = 4cm, angle A = 75°, AD = 5cm, angle B = 110°, BC = 3cm, which element is NOT directly needed first?",
      hi: "रचना ABCD में AB = 4 सेमी, कोण A = 75°, AD = 5 सेमी, कोण B = 110°, BC = 3 सेमी है। पहले किस अवयव की सीधे आवश्यकता नहीं है?",
      te: "నిర్మాణం ABCDలో AB = 4 సెం.మీ., కోణం A = 75°, AD = 5 సెం.మీ., కోణం B = 110°, BC = 3 సెం.మీ. మొదట నేరుగా అవసరం లేని అంశం ఏది?",
    },
  },
  'practical-geometry-test-6': {
    prompt: {
      en: "A square has side 5cm. What length is its diagonal?",
      hi: "एक वर्ग की भुजा 5 सेमी है। उसके विकर्ण की लंबाई कितनी है?",
      te: "ఒక చతురస్రం భుజం 5 సెం.మీ. దాని కర్ణం పొడవు ఎంత?",
    },
  },
  'data-handling-diagnostic-4': {
    prompt: {
      en: "In a pie chart for a data set, the angle for a category with 25% of data is:",
      hi: "पाई चार्ट में 25% आँकड़ों वाली श्रेणी का कोण कितना होगा?",
      te: "పై చార్ట్‌లో 25% దత్తాంశం ఉన్న వర్గం కోణం ఎంత?",
    },
  },
  'data-handling-practice-5': {
    prompt: {
      en: "The numbers 2, 4, 5, 3, 6 are arranged in ascending order. The median is:",
      hi: "संख्याओं 2, 4, 5, 3, 6 को आरोही क्रम में रखा गया है। माध्यिका है:",
      te: "2, 4, 5, 3, 6 సంఖ్యలను ఆరోహణ క్రమంలో అమర్చారు. మధ్యగతం:",
    },
  },
  'data-handling-test-6': {
    prompt: {
      en: "A bag contains 5 red and 3 blue marbles. What is the probability of picking red?",
      hi: "एक थैले में 5 लाल और 3 नीले कंचे हैं। लाल कंचा निकलने की प्रायिकता क्या है?",
      te: "ఒక సంచిలో 5 ఎరుపు, 3 నీలం గోళీలు ఉన్నాయి. ఎరుపు గోళీ వచ్చే సంభావ్యత ఎంత?",
    },
  },
  'squares-roots-diagnostic-4': {
    prompt: {
      en: "The number 169 is a perfect square of:",
      hi: "संख्या 169 किस संख्या का पूर्ण वर्ग है?",
      te: "169 ఏ సంఖ్య యొక్క పూర్ణ వర్గం?",
    },
  },
  'squares-roots-practice-5': {
    prompt: {
      en: "Find √(324) using prime factorisation. 324 = 4 × 81 = 2² × 3⁴. So √324 =",
      hi: "अभाज्य गुणनखंडन से √(324) ज्ञात कीजिए। 324 = 4 × 81 = 2² × 3⁴। अतः √324 =",
      te: "ప్రధాన కారణాంకాలతో √(324) కనుగొనండి. 324 = 4 × 81 = 2² × 3⁴. కాబట్టి √324 =",
    },
  },
  'squares-roots-test-6': {
    prompt: {
      en: "(3, 4, 5) is a Pythagorean triplet because:",
      hi: "(3, 4, 5) एक पाइथागोरस त्रिक है क्योंकि:",
      te: "(3, 4, 5) పైథాగరియన్ త్రికం ఎందుకంటే:",
    },
  },
  'cubes-roots-diagnostic-4': {
    prompt: {
      en: "Which is a perfect cube?",
      hi: "इनमें से पूर्ण घन कौन सा है?",
      te: "వీటిలో పూర్ణ ఘనం ఏది?",
    },
  },
  'cubes-roots-practice-5': {
    prompt: {
      en: "Find the cube root of 1000.",
      hi: "1000 का घनमूल ज्ञात कीजिए।",
      te: "1000 యొక్క ఘనమూలం కనుగొనండి.",
    },
  },
  'cubes-roots-test-6': {
    prompt: {
      en: "Is 392 a perfect cube? Its prime factorisation is 2³ × 7².",
      hi: "क्या 392 एक पूर्ण घन है? इसका अभाज्य गुणनखंडन 2³ × 7² है।",
      te: "392 పూర్ణ ఘనమా? దాని ప్రధాన కారణాంకాలు 2³ × 7².",
    },
  },
  'comparing-quantities-diagnostic-4': {
    prompt: {
      en: "A shopkeeper buys a pen for ₹10 and sells it for ₹13. Profit percentage is:",
      hi: "एक दुकानदार ₹10 में पेन खरीदकर ₹13 में बेचता है। लाभ प्रतिशत है:",
      te: "ఒక దుకాణదారు పెన్నును ₹10కి కొని ₹13కి అమ్మారు. లాభ శాతం:",
    },
  },
  'comparing-quantities-practice-5': {
    prompt: {
      en: "Find the compound interest on ₹10,000 at 10% per annum for 2 years.",
      hi: "₹10,000 पर 10% वार्षिक दर से 2 वर्ष का चक्रवृद्धि ब्याज ज्ञात कीजिए।",
      te: "₹10,000 పై సంవత్సరానికి 10% చొప్పున 2 సంవత్సరాల చక్రవడ్డీ కనుగొనండి.",
    },
  },
  'comparing-quantities-test-6': {
    prompt: {
      en: "The price of a refrigerator was ₹14,000. It was sold at a loss of 5%. Find the selling price.",
      hi: "एक रेफ्रिजरेटर का मूल्य ₹14,000 था। उसे 5% हानि पर बेचा गया। विक्रय मूल्य ज्ञात कीजिए।",
      te: "ఒక రిఫ్రిజిరేటర్ ధర ₹14,000. దాన్ని 5% నష్టానికి అమ్మారు. అమ్మిన ధర కనుగొనండి.",
    },
  },
  // Prerequisite checks: one for each skill the chapters depend on
  'prereq-magnitude': {
    prompt: {
      en: "Which is larger: 1/2 or 1/5?",
      hi: "कौन बड़ा है: 1/2 या 1/5?",
      te: "ఏది పెద్దది: 1/2 లేదా 1/5?",
    },
    explanation: {
      en: "Halves are larger pieces than fifths of the same whole, so 1/2 is larger.",
      hi: "एक ही पूर्ण के आधे भाग पाँचवें भागों से बड़े होते हैं, इसलिए 1/2 बड़ा है।",
      te: "ఒకే మొత్తంలో సగం భాగాలు ఐదో భాగాల కంటే పెద్దవి, కాబట్టి 1/2 పెద్దది.",
    },
  },
  'prereq-simplify': {
    prompt: {
      en: "Write 6/8 in simplest form.",
      hi: "6/8 को सरलतम रूप में लिखिए।",
      te: "6/8ని సరళ రూపంలో రాయండి.",
    },
    explanation: {
      en: "Divide both terms by their highest common factor, 2: 6/8 = 3/4.",
      hi: "दोनों पदों को उनके महत्तम समापवर्तक 2 से भाग दें: 6/8 = 3/4।",
      te: "రెండు పదాలను వాటి గరిష్ఠ సామాన్య భాజకం 2తో భాగించండి: 6/8 = 3/4.",
    },
  },
  'prereq-inverse': {
    prompt: {
      en: "If n + 6 = 10, what is n?",
      hi: "यदि n + 6 = 10 है, तो n क्या है?",
      te: "n + 6 = 10 అయితే n ఎంత?",
    },
    explanation: {
      en: "Undo adding 6 by subtracting 6 from both sides: n = 10 - 6 = 4.",
      hi: "6 जोड़ने को उलटने के लिए दोनों ओर से 6 घटाएँ: n = 10 - 6 = 4।",
      te: "6 కలపడాన్ని రద్దు చేయడానికి రెండు వైపులా 6 తీసివేయండి: n = 10 - 6 = 4.",
    },
  },
  'prereq-triangle': {
    prompt: {
      en: "Two angles of a triangle are 60° and 70°. The third angle is…",
      hi: "एक त्रिभुज के दो कोण 60° और 70° हैं। तीसरा कोण है…",
      te: "త్రిభుజంలో రెండు కోణాలు 60°, 70°. మూడో కోణం…",
    },
    explanation: {
      en: "A triangle's angles total 180°: 180° - (60° + 70°) = 50°.",
      hi: "त्रिभुज के कोणों का योग 180° होता है: 180° - (60° + 70°) = 50°।",
      te: "త్రిభుజ కోణాల మొత్తం 180°: 180° - (60° + 70°) = 50°.",
    },
  },
  'prereq-ruler': {
    prompt: {
      en: "A line segment runs from the 2 cm mark to the 9 cm mark on a ruler. How long is it?",
      hi: "एक रेखाखंड पैमाने पर 2 सेमी के निशान से 9 सेमी के निशान तक है। उसकी लंबाई कितनी है?",
      te: "ఒక రేఖాఖండం స్కేలుపై 2 సెం.మీ. గుర్తు నుండి 9 సెం.మీ. గుర్తు వరకు ఉంది. దాని పొడవు ఎంత?",
    },
    explanation: {
      en: "The length is the difference between the marks: 9 cm - 2 cm = 7 cm.",
      hi: "लंबाई दोनों निशानों का अंतर है: 9 सेमी - 2 सेमी = 7 सेमी।",
      te: "పొడవు రెండు గుర్తుల మధ్య తేడా: 9 సెం.మీ. - 2 సెం.మీ. = 7 సెం.మీ.",
    },
  },
  'prereq-data': {
    prompt: {
      en: "The marks of four students are 5, 7, 7 and 9. How many students scored 7?",
      hi: "चार विद्यार्थियों के अंक 5, 7, 7 और 9 हैं। कितने विद्यार्थियों ने 7 अंक पाए?",
      te: "నలుగురు విద్యార్థుల మార్కులు 5, 7, 7, 9. ఎంత మందికి 7 మార్కులు వచ్చాయి?",
    },
    explanation: {
      en: "The value 7 appears twice in the list, so 2 students scored 7.",
      hi: "सूची में 7 दो बार आया है, इसलिए 2 विद्यार्थियों ने 7 अंक पाए।",
      te: "జాబితాలో 7 రెండుసార్లు ఉంది, కాబట్టి 2 మందికి 7 మార్కులు వచ్చాయి.",
    },
  },
  'prereq-factors': {
    prompt: {
      en: "Which is the prime factorisation of 36?",
      hi: "36 का अभाज्य गुणनखंडन कौन सा है?",
      te: "36 యొక్క ప్రధాన కారణాంకాల లబ్ధం ఏది?",
    },
    explanation: {
      en: "Every factor must be prime: 36 = 2 × 2 × 3 × 3. The numbers 4, 6 and 9 are not prime.",
      hi: "हर गुणनखंड अभाज्य होना चाहिए: 36 = 2 × 2 × 3 × 3। संख्याएँ 4, 6 और 9 अभाज्य नहीं हैं।",
      te: "ప్రతి కారణాంకం ప్రధాన సంఖ్య కావాలి: 36 = 2 × 2 × 3 × 3. 4, 6, 9 ప్రధాన సంఖ్యలు కావు.",
    },
  },
  'prereq-repeated': {
    prompt: {
      en: "What is 3 × 3 × 3?",
      hi: "3 × 3 × 3 का मान क्या है?",
      te: "3 × 3 × 3 విలువ ఎంత?",
    },
    explanation: {
      en: "3 × 3 = 9, and 9 × 3 = 27.",
      hi: "3 × 3 = 9, और 9 × 3 = 27।",
      te: "3 × 3 = 9, మరియు 9 × 3 = 27.",
    },
  },
  'prereq-percent': {
    prompt: {
      en: "What is 50% of 80?",
      hi: "80 का 50% कितना है?",
      te: "80లో 50% ఎంత?",
    },
    explanation: {
      en: "50% means 50 out of 100, which is one half. Half of 80 is 40.",
      hi: "50% का अर्थ है 100 में से 50, यानी आधा। 80 का आधा 40 है।",
      te: "50% అంటే 100లో 50, అంటే సగం. 80లో సగం 40.",
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
  "18 and 19": { en: "18 and 19", hi: "18 और 19", te: "18 మరియు 19" },
  "17 and 20": { en: "17 and 20", hi: "17 और 20", te: "17 మరియు 20" },
  "15 and 22": { en: "15 and 22", hi: "15 और 22", te: "15 మరియు 22" },
  "16 and 21": { en: "16 and 21", hi: "16 और 21", te: "16 మరియు 21" },
  "3 sides only": { en: "3 sides only", hi: "केवल 3 भुजाएँ", te: "3 భుజాలు మాత్రమే" },
  "5 measurements (sides and angles)": { en: "5 measurements (sides and angles)", hi: "5 माप (भुजाएँ और कोण)", te: "5 కొలతలు (భుజాలు, కోణాలు)" },
  "2 sides only": { en: "2 sides only", hi: "केवल 2 भुजाएँ", te: "2 భుజాలు మాత్రమే" },
  "4 sides and no angles": { en: "4 sides and no angles", hi: "4 भुजाएँ और कोई कोण नहीं", te: "4 భుజాలు, కోణాలు లేవు" },
  "angle A": { en: "angle A", hi: "कोण A", te: "కోణం A" },
  "angle B": { en: "angle B", hi: "कोण B", te: "కోణం B" },
  "3+4 = 7, close to 5": { en: "3+4 = 7, close to 5", hi: "3+4 = 7, जो 5 के निकट है", te: "3+4 = 7, ఇది 5కి దగ్గర" },
  "All are odd": { en: "All are odd", hi: "सभी विषम हैं", te: "అన్నీ బేసి సంఖ్యలు" },
  "Yes, ∛392 = 14": { en: "Yes, ∛392 = 14", hi: "हाँ, ∛392 = 14", te: "అవును, ∛392 = 14" },
  "No, 7 appears only twice — needs one more 7": { en: "No, 7 appears only twice — needs one more 7", hi: "नहीं, 7 केवल दो बार आया है, एक और 7 चाहिए", te: "కాదు, 7 రెండుసార్లే ఉంది, ఇంకో 7 కావాలి" },
  "Yes, because 392 = 8 × 49": { en: "Yes, because 392 = 8 × 49", hi: "हाँ, क्योंकि 392 = 8 × 49", te: "అవును, ఎందుకంటే 392 = 8 × 49" },
  "No, because 2 appears three times": { en: "No, because 2 appears three times", hi: "नहीं, क्योंकि 2 तीन बार आया है", te: "కాదు, ఎందుకంటే 2 మూడుసార్లు ఉంది" },
};

export function getLocalizedOptionLabel(option: string, lang: Language): string {
  if (lang === 'en') return option;
  return OPTION_TRANSLATIONS[option]?.[lang] || option;
}

