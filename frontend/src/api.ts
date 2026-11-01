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
};
