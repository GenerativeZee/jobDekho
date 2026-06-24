export interface Job {
  job_id: string;
  title: string;
  department: string | null;
  company: string | null;
  category: string | null;
  sub_category: string | null;
  location: string[] | null;
  salary_min: number | null;
  salary_max: number | null;
  salary_text: string | null;
  qualification: string[] | null;
  min_age: number | null;
  max_age: number | null;
  vacancies: number | null;
  notification_date: string | null;
  application_start: string | null;
  application_end: string | null;
  exam_date: string | null;
  official_url: string;
  source: string | null;
  is_active: boolean;
  created_at: string;
}

export interface JobListResponse {
  jobs: Job[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface JobFilters {
  q?: string;
  category?: string;
  location?: string;
  qualification?: string;
  page?: number;
}
