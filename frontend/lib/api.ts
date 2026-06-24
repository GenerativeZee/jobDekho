import type { Job, JobFilters, JobListResponse } from "@/types/job";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8001";

async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, { next: { revalidate: 300 } });
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
  return res.json();
}

export async function getJobs(filters: JobFilters = {}): Promise<JobListResponse> {
  const params = new URLSearchParams();
  if (filters.q) params.set("q", filters.q);
  if (filters.category) params.set("category", filters.category);
  if (filters.location) params.set("location", filters.location);
  if (filters.qualification) params.set("qualification", filters.qualification);
  if (filters.page) params.set("page", String(filters.page));
  const qs = params.toString();
  return apiFetch<JobListResponse>(`/api/jobs${qs ? `?${qs}` : ""}`);
}

export async function getJob(id: string): Promise<Job> {
  return apiFetch<Job>(`/api/jobs/${id}`);
}

export async function getCategories(): Promise<{ category: string; count: number }[]> {
  return apiFetch<{ category: string; count: number }[]>("/api/jobs/categories");
}
