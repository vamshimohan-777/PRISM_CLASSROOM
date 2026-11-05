export const API = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '/api' : 'http://127.0.0.1:8000/api');

export type User = { id: number; name: string; email: string; role: 'student' | 'teacher'; student_code?: string | null };
export type Auth = { access_token: string; token_type: 'bearer'; user: User };
export type Unit = { id: string; number: number; title: string; summary: string; concept: string; minutes: number; color: string };
export type Question = { id: string; prompt: string; options: string[]; stage: string; explanation: string; is_transfer: boolean };
export type Progress = {
  unit_id?: string;
  student_code: string;
  mastery: number;
  evidence_count: number;
  recommendation: string;
  misconception: string | null;
  misconception_confidence?: number;
  prerequisite_status?: string;
  provisional?: boolean;
};

export type Plan = {
  id: number;
  group_key: string;
  barrier: string;
  evidence: string;
  confidence: string;
  activity: string;
  duration: string;
  outcome: string;
  follow_up: string;
  status: 'proposed' | 'approved' | 'modified' | 'rejected';
  student_codes: string[];
  teacher_notes: string;
};

export type Persona = {
  id: string;
  name: string;
  role: 'student' | 'teacher';
  email: string;
  student_code: string | null;
  archetype: string;
  route: string;
  tag: string;
  description: string;
};

export type AttemptRecord = {
  id: number;
  question_id: string;
  prompt: string;
  stage: string;
  response: string;
  expected_answer: string;
  correct: boolean;
  misconception: string | null;
  explanation: string;
  created_at: string | null;
};

export type StudentDetail = {
  code: string;
  name: string;
  email: string;
  grade: number;
  mastery: number;
  evidence_count: number;
  misconception: string | null;
  misconception_confidence: number;
  prerequisite_status: string;
  recommendation: string;
  attempts: AttemptRecord[];
};

export type LearnerSummary = {
  code: string;
  name: string;
  mastery: number;
  evidence_count: number;
  active_units: number;
  recommendation: string;
  misconception: string | null;
  misconception_confidence: number;
  prerequisite_status: string;
};

export type WorkspaceData = {
  class_code: string;
  teacher_name?: string;
  learners: LearnerSummary[];
  interventions: Plan[];
};

export type InterventionUpdate = {
  status: 'proposed' | 'approved' | 'modified' | 'rejected';
  teacher_notes?: string;
  activity?: string;
  duration?: string;
  outcome?: string;
  student_codes?: string[];
};

// ----------------------------------------------------
// Search Engine Types
// ----------------------------------------------------
export type SearchResultItem = {
  id: string;
  type: 'chapter' | 'concept' | 'question' | 'misconception' | 'intervention';
  title: string;
  snippet: string;
  relevance_score: number;
  chapter_id?: string | null;
  concept_id?: string | null;
  tags: string[];
  metadata: Record<string, any>;
};

export type SearchResponse = {
  query: string;
  total_results: number;
  results: SearchResultItem[];
};

// ----------------------------------------------------
// Answer Engine Types
// ----------------------------------------------------
export type SolutionStep = {
  step_number: number;
  title: string;
  explanation: string;
  math_expr: string;
};

export type PracticeChallenge = {
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
};

export type AnswerResponse = {
  query: string;
  category: string;
  direct_answer: string;
  confidence: number;
  steps: SolutionStep[];
  verification: string;
  misconception_warning: string;
  prerequisites: string[];
  practice_challenge: PracticeChallenge;
  source: string;
};

// ----------------------------------------------------
// Generative Engine Types
// ----------------------------------------------------
export type GeneratedQuestion = {
  id: string;
  concept_id: string;
  stage: 'diagnostic' | 'practice' | 'test';
  difficulty: 'foundation' | 'standard' | 'challenge';
  prompt: string;
  options: string[];
  expected_answer: string;
  explanation: string;
  misconception_map: Record<string, string>;
  is_transfer: boolean;
};

export type RemediationGuide = {
  student_name: string;
  grade: number;
  misconception_id: string;
  title: string;
  cognitive_barrier: string;
  concrete_analogy: string;
  visual_manipulative: string;
  counter_example: string;
  guided_steps: string[];
  diagnostic_probe: {
    question: string;
    options: string[];
    correct_answer: string;
    explanation: string;
  };
  generated_at?: string;
};

export type LessonPlanTimelinePhase = {
  phase: string;
  duration: string;
  pedagogy: string;
  teacher_prompt?: string;
  student_action?: string;
  pods?: Array<{
    pod_name: string;
    target_barrier: string;
    activity: string;
    teacher_checkpoint: string;
    materials: string;
  }>;
};

export type GeneratedLessonPlan = {
  title: string;
  classroom_code: string;
  duration_minutes: number;
  curriculum_framework: string;
  learning_objectives: string[];
  timeline: LessonPlanTimelinePhase[];
  inspection_rubric: Record<string, string>;
};

export type GeneratedTransferTask = {
  title: string;
  context: string;
  ingredients?: string[];
  problem: string;
  solution_steps: string[];
  pedagogy?: string;
  pedagogical_outcome?: string;
};

async function request<T>(path: string, init: RequestInit = {}, token?: string): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set('content-type', 'application/json');
  if (token) headers.set('authorization', `Bearer ${token}`);
  const response = await fetch(`${API}${path}`, { ...init, headers });
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new Error(data?.detail || 'Something went wrong. Please try again.');
  }
  return response.json() as Promise<T>;
}

export const api = {
  login: (email: string, password: string) => request<Auth>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  register: (name: string, email: string, password: string, role: 'student' | 'teacher') =>
    request<Auth>('/auth/register', { method: 'POST', body: JSON.stringify({ name, email, password, role }) }),
  me: (token: string) => request<User>('/auth/me', {}, token),
  units: () => request<Unit[]>('/learning/units'),
  progress: (token: string) => request<Progress[]>('/learning/my-progress', {}, token),
  questions: (unitId: string, stage: string, token: string) => request<Question[]>(`/learning/units/${unitId}/questions?stage=${stage}`, {}, token),
  attempt: (body: { question_id: string; response: string; stage: 'diagnostic' | 'practice' | 'test'; submission_id: string }, token: string) =>
    request<{ correct: boolean; feedback: string; profile: Progress; reason: string }>('/learning/attempts', { method: 'POST', body: JSON.stringify(body) }, token),
  workspace: (token: string) => request<WorkspaceData>('/teacher/workspace', {}, token),
  personas: () => request<Persona[]>('/demo/personas'),
  resetDemo: () => request<{ status: string; message: string }>('/demo/reset', { method: 'POST' }),
  studentDetail: (code: string, token: string) => request<StudentDetail>(`/teacher/students/${code}/detail`, {}, token),
  updateIntervention: (id: number, body: InterventionUpdate, token: string) =>
    request<Plan>(`/teacher/interventions/${id}`, { method: 'PUT', body: JSON.stringify(body) }, token),
  joinClassroom: (classroom_code: string, token: string) =>
    request<{ status: string; classroom_code: string; curriculum: string; teacher_name: string }>('/students/join-classroom', { method: 'POST', body: JSON.stringify({ classroom_code }) }, token),
  recompileInterventions: (token: string) =>
    request<Plan[]>('/teacher/interventions/recompile', { method: 'POST' }, token),
  search: (query: string, entity_type: string = 'all', chapter_id: string = 'all', limit: number = 15) =>
    request<SearchResponse>('/search', { method: 'POST', body: JSON.stringify({ query, entity_type, chapter_id, limit }) }),
  searchSuggestions: (prefix: string = '') =>
    request<{ suggestions: string[] }>(`/search/suggestions?q=${encodeURIComponent(prefix)}`),
  answer: (query: string, concept_id?: string) =>
    request<AnswerResponse>('/answer', { method: 'POST', body: JSON.stringify({ query, concept_id }) }),
  generateQuestion: (concept_id: string = 'equivalent-fractions', stage: 'diagnostic' | 'practice' | 'test' = 'practice', difficulty: 'foundation' | 'standard' | 'challenge' = 'standard') =>
    request<GeneratedQuestion>('/generate/question', { method: 'POST', body: JSON.stringify({ concept_id, stage, difficulty }) }),
  generateRemediation: (misconception_id: string, student_name: string = 'Learner', grade: number = 8) =>
    request<RemediationGuide>('/generate/remediation', { method: 'POST', body: JSON.stringify({ misconception_id, student_name, grade }) }),
  generateLessonPlan: (concept_id: string = 'equivalent-fractions', classroom_code: string = '8A-CBSE') =>
    request<GeneratedLessonPlan>('/generate/lesson-plan', { method: 'POST', body: JSON.stringify({ concept_id, classroom_code }) }),
  generateTransferTask: (concept_id: string = 'equivalent-fractions', theme: string = 'recipes') =>
    request<GeneratedTransferTask>('/generate/transfer-task', { method: 'POST', body: JSON.stringify({ concept_id, theme }) }),
};
