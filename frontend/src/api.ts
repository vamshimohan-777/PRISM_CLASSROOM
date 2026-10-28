export const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
export type Question = {id:string; prompt:string; options:string[]; stage:string; explanation:string; is_transfer:boolean};
export type Profile = {student_code:string; mastery:number; evidence_count:number; misconception:string|null; misconception_confidence:number; prerequisite_status:string; recommendation:string; provisional:boolean};
export type Plan = {id:number; group_key:string; student_codes:string[]; barrier:string; evidence:string; confidence:string; activity:string; duration:string; outcome:string; follow_up:string; status:string; teacher_notes:string};
export type Curriculum = {board_code:string;board_name:string;framework:string;academic_year:string;grade:number;subject:string;module_title:string;chapter_reference:string;learning_outcomes:string[];pedagogy:string[];official_reference:string;disclaimer:string};
async function get<T>(path:string, init:RequestInit={}) { const r=await fetch(`${API}${path}`,init); if(!r.ok) throw new Error(await r.text()); return r.json() as Promise<T> }
export const api={
  demo:()=>get<{students:string[];teacher:string}>('/demo'),
  curriculum:()=>get<Curriculum>('/curriculum'),
  questions:(code:string,stage:string)=>get<Question[]>(`/students/${code}/questions?stage=${stage}`),
  profile:(code:string)=>get<Profile>(`/students/${code}/progress`),
  attempt:(code:string,body:{question_id:string;response:string;stage:string;submission_id:string})=>get<{correct:boolean;feedback:string;profile:Profile;reason:string}>(`/students/${code}/attempts`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)}),
  overview:()=>get<{class_code:string;synthetic:boolean;curriculum:Curriculum;students:Profile[]}>('/teacher/overview',{headers:{'X-Demo-Teacher':'TEACHER-PRISM'}}),
  plans:()=>get<Plan[]>('/teacher/interventions',{headers:{'X-Demo-Teacher':'TEACHER-PRISM'}}),
  decide:(id:number,body:{status:'approved'|'rejected';teacher_notes:string;activity?:string})=>get<Plan>(`/teacher/interventions/${id}`,{method:'PUT',headers:{'content-type':'application/json','X-Demo-Teacher':'TEACHER-PRISM'},body:JSON.stringify(body)})
};
