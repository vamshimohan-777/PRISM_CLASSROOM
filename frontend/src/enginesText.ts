/**
 * Localised copy for the Engines Studio.
 *
 * EnginesHub imported TRANSLATIONS but never read it, so every visible string
 * on the page was hardcoded English and the language switcher changed only the
 * surrounding navigation. Following the convention already used in
 * localization.ts, Hindi and Telugu keep the established English technical term
 * in parentheses where that is how the topic is taught in Indian classrooms.
 */
import type { Language } from './translations';

export interface EnginesStrings {
  hubTitle: string;
  hubSubtitle: string;
  badgeArchitecture: string;
  badgeCurriculum: string;
  badgeReproducible: string;

  searchEngine: string;
  searchEngineSub: string;
  answerEngine: string;
  answerEngineSub: string;
  generativeEngine: string;
  generativeEngineSub: string;

  searchPlaceholder: string;
  searchButton: string;
  searching: string;
  entityType: string;
  entityAll: string;
  entityChapters: string;
  entityConcepts: string;
  entityQuestions: string;
  entityMisconceptions: string;
  entityInterventions: string;
  foundLabel: string;
  resultsFor: string;
  resultSingular: string;
  resultPlural: string;
  chipEquivalent: string;
  chipLinear: string;
  chipDenominator: string;
  chipSquareRoot: string;
  sortedByRelevance: string;
  indexing: string;
  noMatches: string;
  noMatchesHint: string;
  generateRemediation: string;
  solveInAnswerEngine: string;
  viewSyllabusChapter: string;

  askAnything: string;
  answerPlaceholder: string;
  quickPrompts: string;
  deriving: string;
  derivingSub: string;
  derivation: string;
  selfCheck: string;
  misconceptionTrap: string;
  prerequisitesFromDag: string;
  checkUnderstanding: string;
  confidence: string;

  questionGenerator: string;
  remediationGuide: string;
  transferTasks: string;
  chapterConcept: string;
  stage: string;
  stageDiagnostic: string;
  stagePractice: string;
  stageTest: string;
  difficulty: string;
  difficultyFoundation: string;
  difficultyStandard: string;
  difficultyChallenge: string;
  transferItem: string;
  ncertExplanation: string;
  distractorMap: string;
  colOption: string;
  colNature: string;
  colMisconception: string;
  correctAnswer: string;
  distractor: string;

  learnerName: string;
  studentNamePlaceholder: string;
  preparedFor: string;
  targetMisconception: string;
  cognitiveBarrier: string;
  curriculumConcept: string;
  printSavePdf: string;
  inspectionCompliant: string;
  learningOutcomes: string;
  lessonTimeline: string;
  teacherScript: string;
  studentActivity: string;
  activity: string;
  teacherCheckpoint: string;
  materials: string;

  contextualTheme: string;
  recipeIngredients: string;
  studentChallenge: string;
  proportionalSolution: string;
  pedagogicalOutcome: string;

  optRational: string;
  optLinear: string;
  optSquares: string;
  optCubes: string;
  optQuadrilaterals: string;
  optComparing: string;
  conceptEquivalent: string;
  miscDenominator: string;
  miscAdditive: string;
  miscUnequal: string;
  miscSign: string;
  themeHalwa: string;
  themeRailways: string;
  themeCricket: string;
}

export const ENGINES_TEXT: Record<Language, EnginesStrings> = {
  en: {
    hubTitle: 'Curriculum Engines Hub',
    hubSubtitle:
      'Integrated Search Engine for syllabus knowledge, Answer Engine for NCERT step-by-step problem solving, and Generative Engine for dynamic questions, remediation guides, and differentiated lesson plans.',
    badgeArchitecture: 'PRISM 3-ENGINE ARCHITECTURE',
    badgeCurriculum: 'CBSE CLASS VIII NCERT MATHEMATICS',
    badgeReproducible: '100% REPRODUCIBLE & VERIFIED',

    searchEngine: 'Search Engine',
    searchEngineSub: 'Curriculum & Concepts',
    answerEngine: 'Answer Engine',
    answerEngineSub: 'Step-by-Step Solver',
    generativeEngine: 'Generative Engine',
    generativeEngineSub: 'Questions, Guides & Plans',

    searchPlaceholder: 'Search chapters, concepts, questions, misconceptions, or intervention strategies...',
    searchButton: 'Search',
    searching: 'Searching…',
    entityType: 'Entity Type:',
    entityAll: 'All Entities',
    entityChapters: 'Chapters',
    entityConcepts: 'DAG Concepts',
    entityQuestions: 'Questions',
    entityMisconceptions: 'Misconceptions',
    entityInterventions: 'Interventions',
    foundLabel: 'Found',
    resultsFor: 'results for',
    resultSingular: 'result',
    resultPlural: 'results',
    chipEquivalent: 'Equivalent fractions',
    chipLinear: 'Linear equations',
    chipDenominator: 'Denominator magnitude',
    chipSquareRoot: 'Square root',
    sortedByRelevance: 'Sorted by relevance score',
    indexing: 'Indexing and searching curriculum database...',
    noMatches: 'No exact matches found',
    noMatchesHint: 'Try searching for terms like "fraction", "linear equations", "denominator", or "square root".',
    generateRemediation: 'Generate Remediation Guide',
    solveInAnswerEngine: 'Solve in Answer Engine',
    viewSyllabusChapter: 'View Syllabus Chapter',

    askAnything: 'Ask or Solve Any CBSE Class VIII Problem',
    answerPlaceholder: 'e.g. Solve: 3x + 5 = 20, Compare 1/3 and 1/8, Simplify 18/24, Square root of 144...',
    quickPrompts: 'Quick Prompts:',
    deriving: 'Deriving step-by-step solution...',
    derivingSub: 'Analyzing equations, checking balance rules, and extracting NCERT explanations.',
    derivation: 'Step-by-Step NCERT Pedagogical Derivation',
    selfCheck: 'Self-Check Verification',
    misconceptionTrap: 'Common Misconception Trap',
    prerequisitesFromDag: 'Prerequisites from Concept DAG:',
    checkUnderstanding: 'Check Your Understanding: Quick Challenge',
    confidence: 'Confidence',

    questionGenerator: 'Dynamic Question Generator',
    remediationGuide: 'Personalized Remediation Guide',
    transferTasks: 'Indian Contextual Transfer Tasks',
    chapterConcept: 'Chapter / Concept',
    stage: 'Stage',
    stageDiagnostic: 'Diagnostic (Initial Probe)',
    stagePractice: 'Practice (Scaffolded)',
    stageTest: 'Transfer Test (Novel Context)',
    difficulty: 'Difficulty',
    difficultyFoundation: 'Foundation (Visual Scaffolds)',
    difficultyStandard: 'Standard (CBSE Regular)',
    difficultyChallenge: 'Challenge (Multi-step)',
    transferItem: 'Transfer Item',
    ncertExplanation: 'Step-by-Step NCERT Explanation:',
    distractorMap: 'Cognitive Misconception Distractor Map',
    colOption: 'Option',
    colNature: 'Nature',
    colMisconception: 'Associated Latent Misconception',
    correctAnswer: 'Correct Answer',
    distractor: 'Distractor',

    learnerName: 'Learner Name',
    studentNamePlaceholder: 'Student name',
    preparedFor: 'Prepared for:',
    targetMisconception: 'Target Student Misconception',
    cognitiveBarrier: 'Cognitive Barrier Analysis',
    curriculumConcept: 'Curriculum Concept',
    printSavePdf: 'Print / Save PDF',
    inspectionCompliant: 'CBSE Inspection Compliant',
    learningOutcomes: 'Core Learning Outcomes (CBSE / NEP 2020)',
    lessonTimeline: 'Structured 45-Minute Lesson Timeline',
    teacherScript: 'Teacher Opening Script / Prompt:',
    studentActivity: 'Student Activity:',
    activity: 'Activity:',
    teacherCheckpoint: 'Teacher Checkpoint:',
    materials: 'Materials:',

    contextualTheme: 'Contextual Indian Theme',
    recipeIngredients: 'Recipe Ingredients (Design for 4 Servings):',
    studentChallenge: 'The Student Challenge:',
    proportionalSolution: 'Step-by-Step Proportional Solution & Key:',
    pedagogicalOutcome: 'Pedagogical Outcome:',
    optRational: 'Rational Numbers & Fractions',
    optLinear: 'Linear Equations in One Variable',
    optSquares: 'Squares & Square Roots',
    optCubes: 'Cubes & Cube Roots',
    optQuadrilaterals: 'Understanding Quadrilaterals',
    optComparing: 'Comparing Quantities & Percentages',
    conceptEquivalent: 'Equivalent Fractions & Rational Numbers',
    miscDenominator: 'Denominator-Magnitude (1/8 > 1/3)',
    miscAdditive: 'Additive Equivalence Bias (+1/+1)',
    miscUnequal: 'Unequal Multiplier Operations',
    miscSign: 'Sign Inversion & Balancing Error',
    themeHalwa: 'Festive Culinary: Diwali Sooji Halwa',
    themeRailways: 'Infrastructure: Vande Bharat Express Timetable',
    themeCricket: 'Sports Analytics: IPL Match Run Rate',
  },

  hi: {
    hubTitle: 'पाठ्यक्रम इंजन हब (Curriculum Engines Hub)',
    hubSubtitle:
      'पाठ्यक्रम ज्ञान के लिए एकीकृत सर्च इंजन, NCERT चरण-दर-चरण समाधान के लिए आंसर इंजन, और गतिशील प्रश्नों, उपचारात्मक मार्गदर्शिकाओं तथा विभेदित पाठ योजनाओं के लिए जेनरेटिव इंजन।',
    badgeArchitecture: 'PRISM त्रि-इंजन संरचना',
    badgeCurriculum: 'CBSE कक्षा VIII · NCERT गणित',
    badgeReproducible: '100% पुनरुत्पादनीय और सत्यापित',

    searchEngine: 'सर्च इंजन',
    searchEngineSub: 'पाठ्यक्रम और संकल्पनाएँ',
    answerEngine: 'आंसर इंजन',
    answerEngineSub: 'चरण-दर-चरण हल',
    generativeEngine: 'जेनरेटिव इंजन',
    generativeEngineSub: 'प्रश्न, मार्गदर्शिकाएँ और योजनाएँ',

    searchPlaceholder: 'अध्याय, संकल्पना, प्रश्न, भ्रांति या हस्तक्षेप रणनीति खोजें...',
    searchButton: 'खोजें',
    searching: 'खोजा जा रहा है…',
    entityType: 'प्रकार:',
    entityAll: 'सभी',
    entityChapters: 'अध्याय',
    entityConcepts: 'DAG संकल्पनाएँ',
    entityQuestions: 'प्रश्न',
    entityMisconceptions: 'भ्रांतियाँ',
    entityInterventions: 'हस्तक्षेप',
    foundLabel: 'मिले',
    resultsFor: '—',
    resultSingular: 'परिणाम',
    resultPlural: 'परिणाम',
    chipEquivalent: 'तुल्य भिन्न',
    chipLinear: 'रैखिक समीकरण',
    chipDenominator: 'हर का परिमाण',
    chipSquareRoot: 'वर्गमूल',
    sortedByRelevance: 'प्रासंगिकता स्कोर के अनुसार क्रमबद्ध',
    indexing: 'पाठ्यक्रम डेटाबेस अनुक्रमित और खोजा जा रहा है...',
    noMatches: 'कोई सटीक मिलान नहीं मिला',
    noMatchesHint: '"भिन्न", "रैखिक समीकरण", "हर" या "वर्गमूल" जैसे शब्द खोजकर देखें।',
    generateRemediation: 'उपचारात्मक मार्गदर्शिका बनाएँ',
    solveInAnswerEngine: 'आंसर इंजन में हल करें',
    viewSyllabusChapter: 'पाठ्यक्रम अध्याय देखें',

    askAnything: 'CBSE कक्षा VIII का कोई भी प्रश्न पूछें या हल करें',
    answerPlaceholder: 'जैसे: 3x + 5 = 20 हल करें, 1/3 और 1/8 की तुलना करें, 18/24 सरल करें, 144 का वर्गमूल...',
    quickPrompts: 'त्वरित प्रश्न:',
    deriving: 'चरण-दर-चरण हल निकाला जा रहा है...',
    derivingSub: 'समीकरणों का विश्लेषण, संतुलन नियमों की जाँच और NCERT व्याख्याएँ निकाली जा रही हैं।',
    derivation: 'चरण-दर-चरण NCERT शैक्षणिक व्युत्पत्ति',
    selfCheck: 'स्व-जाँच सत्यापन',
    misconceptionTrap: 'सामान्य भ्रांति का जाल',
    prerequisitesFromDag: 'संकल्पना DAG से पूर्वापेक्षाएँ:',
    checkUnderstanding: 'अपनी समझ जाँचें: त्वरित चुनौती',
    confidence: 'विश्वास स्तर',

    questionGenerator: 'गतिशील प्रश्न जनरेटर',
    remediationGuide: 'व्यक्तिगत उपचारात्मक मार्गदर्शिका',
    transferTasks: 'भारतीय संदर्भ आधारित अनुप्रयोग कार्य',
    chapterConcept: 'अध्याय / संकल्पना',
    stage: 'चरण',
    stageDiagnostic: 'निदानात्मक (प्रारंभिक जाँच)',
    stagePractice: 'अभ्यास (सहायता सहित)',
    stageTest: 'अनुप्रयोग परीक्षण (नया संदर्भ)',
    difficulty: 'कठिनाई',
    difficultyFoundation: 'आधारभूत (दृश्य सहायता)',
    difficultyStandard: 'मानक (CBSE सामान्य)',
    difficultyChallenge: 'चुनौतीपूर्ण (बहु-चरणीय)',
    transferItem: 'अनुप्रयोग प्रश्न',
    ncertExplanation: 'चरण-दर-चरण NCERT व्याख्या:',
    distractorMap: 'संज्ञानात्मक भ्रांति विकल्प मानचित्र',
    colOption: 'विकल्प',
    colNature: 'प्रकृति',
    colMisconception: 'संबंधित अंतर्निहित भ्रांति',
    correctAnswer: 'सही उत्तर',
    distractor: 'भ्रामक विकल्प',

    learnerName: 'शिक्षार्थी का नाम',
    studentNamePlaceholder: 'छात्र का नाम',
    preparedFor: 'के लिए तैयार:',
    targetMisconception: 'लक्षित छात्र भ्रांति',
    cognitiveBarrier: 'संज्ञानात्मक बाधा विश्लेषण',
    curriculumConcept: 'पाठ्यक्रम संकल्पना',
    printSavePdf: 'प्रिंट / PDF सहेजें',
    inspectionCompliant: 'CBSE निरीक्षण अनुरूप',
    learningOutcomes: 'मुख्य अधिगम परिणाम (CBSE / NEP 2020)',
    lessonTimeline: 'संरचित 45-मिनट पाठ समयरेखा',
    teacherScript: 'शिक्षक प्रारंभिक कथन / संकेत:',
    studentActivity: 'छात्र गतिविधि:',
    activity: 'गतिविधि:',
    teacherCheckpoint: 'शिक्षक जाँच बिंदु:',
    materials: 'सामग्री:',

    contextualTheme: 'भारतीय संदर्भ विषय',
    recipeIngredients: 'विधि की सामग्री (4 लोगों के लिए):',
    studentChallenge: 'छात्र चुनौती:',
    proportionalSolution: 'चरण-दर-चरण अनुपातिक हल और कुंजी:',
    pedagogicalOutcome: 'शैक्षणिक परिणाम:',
    optRational: 'परिमेय संख्याएँ और भिन्न',
    optLinear: 'एक चर वाले रैखिक समीकरण',
    optSquares: 'वर्ग और वर्गमूल',
    optCubes: 'घन और घनमूल',
    optQuadrilaterals: 'चतुर्भुजों की समझ',
    optComparing: 'राशियों की तुलना और प्रतिशत',
    conceptEquivalent: 'तुल्य भिन्न और परिमेय संख्याएँ',
    miscDenominator: 'हर-परिमाण भ्रांति (1/8 > 1/3)',
    miscAdditive: 'योगात्मक तुल्यता भ्रांति (+1/+1)',
    miscUnequal: 'असमान गुणक संक्रियाएँ',
    miscSign: 'चिह्न व्युत्क्रम और संतुलन त्रुटि',
    themeHalwa: 'त्योहार पाक-कला: दिवाली सूजी हलवा',
    themeRailways: 'अवसंरचना: वंदे भारत एक्सप्रेस समय-सारणी',
    themeCricket: 'खेल विश्लेषण: IPL मैच रन रेट',
  },

  te: {
    hubTitle: 'పాఠ్యప్రణాళిక ఇంజిన్ హబ్ (Curriculum Engines Hub)',
    hubSubtitle:
      'పాఠ్యప్రణాళిక జ్ఞానం కోసం సమీకృత సెర్చ్ ఇంజిన్, NCERT దశల వారీ సమస్య పరిష్కారానికి ఆన్సర్ ఇంజిన్, మరియు డైనமిక్ ప్రశ్నలు, నివారణ మార్గదర్శకాలు, విభిన్న పాఠ ప్రణాళికల కోసం జెనరేటివ్ ఇంజిన్.',
    badgeArchitecture: 'PRISM మూడు-ఇంజిన్ నిర్మాణం',
    badgeCurriculum: 'CBSE తరగతి VIII · NCERT గణితం',
    badgeReproducible: '100% పునరుత్పాదక మరియు ధృవీకరించబడిన',

    searchEngine: 'సెర్చ్ ఇంజిన్',
    searchEngineSub: 'పాఠ్యప్రణాళిక & భావనలు',
    answerEngine: 'ఆన్సర్ ఇంజిన్',
    answerEngineSub: 'దశల వారీ పరిష్కర్త',
    generativeEngine: 'జెనరేటివ్ ఇంజిన్',
    generativeEngineSub: 'ప్రశ్నలు, మార్గదర్శకాలు & ప్రణాళికలు',

    searchPlaceholder: 'అధ్యాయాలు, భావనలు, ప్రశ్నలు, అపోహలు లేదా జోక్య వ్యూహాలను వెతకండి...',
    searchButton: 'వెతకండి',
    searching: 'వెతుకుతోంది…',
    entityType: 'రకం:',
    entityAll: 'అన్నీ',
    entityChapters: 'అధ్యాయాలు',
    entityConcepts: 'DAG భావనలు',
    entityQuestions: 'ప్రశ్నలు',
    entityMisconceptions: 'అపోహలు',
    entityInterventions: 'జోక్యాలు',
    foundLabel: 'దొరికాయి',
    resultsFor: '—',
    resultSingular: 'ఫలితం',
    resultPlural: 'ఫలితాలు',
    chipEquivalent: 'సమాన భిన్నాలు',
    chipLinear: 'రేఖీయ సమీకరణాలు',
    chipDenominator: 'హారం పరిమాణం',
    chipSquareRoot: 'వర్గమూలం',
    sortedByRelevance: 'ప్రాసంగికత స్కోరు ప్రకారం క్రమబద్ధీకరించబడింది',
    indexing: 'పాఠ్యప్రణాళిక డేటాబేస్ సూచీకరించి వెతుకుతోంది...',
    noMatches: 'ఖచ్చితమైన ఫలితాలు దొరకలేదు',
    noMatchesHint: '"భిన్నం", "రేఖీయ సమీకరణాలు", "హారం" లేదా "వర్గమూలం" వంటి పదాలతో వెతకండి.',
    generateRemediation: 'నివారణ మార్గదర్శిని రూపొందించండి',
    solveInAnswerEngine: 'ఆన్సర్ ఇంజిన్‌లో పరిష్కరించండి',
    viewSyllabusChapter: 'సిలబస్ అధ్యాయం చూడండి',

    askAnything: 'CBSE తరగతి VIII ఏ సమస్యనైనా అడగండి లేదా పరిష్కరించండి',
    answerPlaceholder: 'ఉదా: 3x + 5 = 20 పరిష్కరించండి, 1/3 మరియు 1/8 పోల్చండి, 18/24 సరళీకరించండి, 144 వర్గమూలం...',
    quickPrompts: 'త్వరిత ప్రశ్నలు:',
    deriving: 'దశల వారీ పరిష్కారం రాబడుతోంది...',
    derivingSub: 'సమీకరణాల విశ్లేషణ, సమతుల్య నియమాల తనిఖీ మరియు NCERT వివరణల సేకరణ జరుగుతోంది.',
    derivation: 'దశల వారీ NCERT బోధనా ఉత్పాదన',
    selfCheck: 'స్వీయ-తనిఖీ ధృవీకరణ',
    misconceptionTrap: 'సాధారణ అపోహ ఉచ్చు',
    prerequisitesFromDag: 'భావన DAG నుండి ముందస్తు అవసరాలు:',
    checkUnderstanding: 'మీ అవగాహన తనిఖీ చేసుకోండి: త్వరిత సవాలు',
    confidence: 'విశ్వాస స్థాయి',

    questionGenerator: 'డైనమిక్ ప్రశ్న జనరేటర్',
    remediationGuide: 'వ్యక్తిగత నివారణ మార్గదర్శిని',
    transferTasks: 'భారతీయ సందర్భ అనువర్తన పనులు',
    chapterConcept: 'అధ్యాయం / భావన',
    stage: 'దశ',
    stageDiagnostic: 'నిర్ధారణ (ప్రారంభ పరిశీలన)',
    stagePractice: 'అభ్యాసం (సహాయంతో)',
    stageTest: 'అనువర్తన పరీక్ష (కొత్త సందర్భం)',
    difficulty: 'కఠినత',
    difficultyFoundation: 'పునాది (దృశ్య సహాయాలు)',
    difficultyStandard: 'ప్రామాణిక (CBSE సాధారణ)',
    difficultyChallenge: 'సవాలు (బహు-దశల)',
    transferItem: 'అనువర్తన ప్రశ్న',
    ncertExplanation: 'దశల వారీ NCERT వివరణ:',
    distractorMap: 'జ్ఞానాత్మక అపోహ ఎంపికల పటం',
    colOption: 'ఎంపిక',
    colNature: 'స్వభావం',
    colMisconception: 'సంబంధిత అంతర్గత అపోహ',
    correctAnswer: 'సరైన సమాధానం',
    distractor: 'తప్పుదారి ఎంపిక',

    learnerName: 'విద్యార్థి పేరు',
    studentNamePlaceholder: 'విద్యార్థి పేరు',
    preparedFor: 'వీరి కోసం తయారుచేయబడింది:',
    targetMisconception: 'లక్ష్య విద్యార్థి అపోహ',
    cognitiveBarrier: 'జ్ఞానాత్మక అవరోధ విశ్లేషణ',
    curriculumConcept: 'పాఠ్యప్రణాళిక భావన',
    printSavePdf: 'ప్రింట్ / PDF సేవ్ చేయండి',
    inspectionCompliant: 'CBSE తనిఖీకి అనుగుణం',
    learningOutcomes: 'ముఖ్య అభ్యసన ఫలితాలు (CBSE / NEP 2020)',
    lessonTimeline: 'నిర్మాణాత్మక 45-నిమిషాల పాఠ కాలరేఖ',
    teacherScript: 'ఉపాధ్యాయ ప్రారంభ వ్యాఖ్య / సూచన:',
    studentActivity: 'విద్యార్థి కార్యకలాపం:',
    activity: 'కార్యకలాపం:',
    teacherCheckpoint: 'ఉపాధ్యాయ తనిఖీ బిందువు:',
    materials: 'సామగ్రి:',

    contextualTheme: 'భారతీయ సందర్భ ఇతివృత్తం',
    recipeIngredients: 'వంటకం పదార్థాలు (4 మందికి):',
    studentChallenge: 'విద్యార్థి సవాలు:',
    proportionalSolution: 'దశల వారీ అనుపాత పరిష్కారం & కీ:',
    pedagogicalOutcome: 'బోధనా ఫలితం:',
    optRational: 'అకరణీయ సంఖ్యలు & భిన్నాలు',
    optLinear: 'ఏక చరరాశిలో రేఖీయ సమీకరణాలు',
    optSquares: 'వర్గాలు & వర్గమూలాలు',
    optCubes: 'ఘనాలు & ఘనమూలాలు',
    optQuadrilaterals: 'చతుర్భుజాల అవగాహన',
    optComparing: 'రాశుల పోలిక & శాతాలు',
    conceptEquivalent: 'సమాన భిన్నాలు & అకరణీయ సంఖ్యలు',
    miscDenominator: 'హారం-పరిమాణ అపోహ (1/8 > 1/3)',
    miscAdditive: 'సంకలన సమానత్వ అపోహ (+1/+1)',
    miscUnequal: 'అసమాన గుణక ప్రక్రియలు',
    miscSign: 'సంకేత విలోమం & సమతుల్య దోషం',
    themeHalwa: 'పండుగ వంటకం: దీపావళి సూజీ హల్వా',
    themeRailways: 'మౌలిక సదుపాయాలు: వందే భారత్ ఎక్స్‌ప్రెస్ సమయ పట్టిక',
    themeCricket: 'క్రీడా విశ్లేషణ: IPL మ్యాచ్ రన్ రేట్',
  },
};

export const enginesText = (lang: Language): EnginesStrings => ENGINES_TEXT[lang] ?? ENGINES_TEXT.en;
