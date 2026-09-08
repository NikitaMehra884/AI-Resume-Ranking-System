export type UserRole = "CANDIDATE" | "RECRUITER" | "ADMIN";

export interface User {
  id: number;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface SkillItem {
  name: string;
  proficiency?: string;
  endorsements?: number;
  duration_months?: number;
}

export interface ExperienceItem {
  company: string;
  title: string;
  start_date?: string;
  end_date?: string | null;
  duration_months?: number;
  is_current?: boolean;
  industry?: string;
  description?: string;
}

export interface EducationItem {
  institution: string;
  degree?: string;
  field_of_study?: string;
  start_year?: number;
  end_year?: number;
  grade?: string;
  tier?: string;
}

export interface CandidateProfile {
  id: number;
  candidate_id: string;
  full_name: string;
  headline?: string;
  summary?: string;
  years_of_experience: number;
  current_title?: string;
  current_company?: string;
  location?: string;
  country?: string;
  work_mode_preference?: string;
  willing_to_relocate?: boolean;
  notice_period_days?: number;
  completeness_score: number;
  skills: SkillItem[];
  career_history: ExperienceItem[];
  education: EducationItem[];
  created_at?: string;
}

export interface JobSkill {
  name: string;
  is_required: boolean;
}

export interface Job {
  id: number;
  recruiter_id?: number;
  company_name?: string;
  title: string;
  description: string;
  department: string;
  location: string;
  work_mode: "remote" | "hybrid" | "onsite";
  employment_type: string;
  minimum_experience: number;
  maximum_experience: number;
  education_requirement: string;
  target_shortlist_count: number;
  status: "DRAFT" | "PUBLISHED" | "CLOSED";
  skills: JobSkill[];
  applicant_count?: number;
  shortlisted_count?: number;
  created_at: string;
}

export interface RankedCandidate {
  rank: number;
  candidate_id: string;
  name: string;
  current_title: string;
  current_company: string;
  years_of_experience: number;
  location: string;
  country: string;
  final_score: number;
  semantic_score: number;
  keyword_score: number;
  skill_score: number;
  experience_score: number;
  education_score: number;
  career_score: number;
  availability_score: number;
  matched_skills: string[];
  missing_skills: string[];
  reasons: string[];
  status: "APPLIED" | "SCREENING" | "SHORTLISTED" | "INTERVIEW" | "SELECTED" | "REJECTED";
  application_id?: number;
  email?: string;
  phone?: string;
  raw_resume_text?: string;
  notes?: string;
  explanation?: {
    why_ranked?: string;
    strengths?: string[];
    skill_gaps?: string[];
  };
}

export interface Application {
  id: number;
  job_id: number;
  candidate_id?: string;
  status: string;
  match_score?: number;
  created_at: string;
  job?: Job;
  candidate?: CandidateProfile;
}

export interface ScreeningResponse {
  job_id: number;
  job_title: string;
  total_candidates_evaluated: number;
  returned_count: number;
  candidates: RankedCandidate[];
  execution_time_seconds: number;
}

export interface MatchReport {
  candidate_id: string;
  job_id: number;
  match_score: number;
  strong_matches: string[];
  partial_matches: string[];
  missing_skills: string[];
  experience_assessment: string;
  education_assessment: string;
  project_relevance: string;
  why_good_match: string;
  what_to_improve: string;
  evidence_breakdown: {
    semantic_score: number;
    keyword_score: number;
    skill_score: number;
    experience_score: number;
    education_score: number;
    availability_score: number;
  };
}

export interface ComparisonCandidate {
  candidate_id: string;
  name: string;
  current_title: string;
  current_company: string;
  years_of_experience: number;
  final_score: number;
  skill_match: number;
  experience_match: number;
  education: string;
  matched_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
}

export interface ComparisonResponse {
  job_id: number;
  candidates: ComparisonCandidate[];
  comparison_summary: string;
}

export interface InterviewQuestion {
  question: string;
  rationale: string;
}

export interface InterviewQuestionsResponse {
  candidate_id: string;
  job_id: number;
  candidate_name: string;
  job_title: string;
  technical_questions: InterviewQuestion[];
  behavioral_questions: InterviewQuestion[];
  project_questions: InterviewQuestion[];
  role_specific_questions: InterviewQuestion[];
}

export interface ApplicationItem {
  id: number;
  job_id: number;
  job_title: string;
  company_name: string;
  status: string;
  match_score: number;
  applied_at: string;
}

export interface AnalyticsData {
  total_jobs: number;
  active_jobs: number;
  total_applicants: number;
  pipeline: {
    applied: number;
    screening: number;
    shortlisted: number;
    interview: number;
    selected: number;
    rejected: number;
    total: number;
  };
  average_match_score: number;
  top_skills: { skill: string; count: number }[];
  score_distribution: { bucket: string; count: number }[];
}
