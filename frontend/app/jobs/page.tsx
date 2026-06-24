import { Suspense } from "react";
import Link from "next/link";
import { getJobs } from "@/lib/api";
import JobCard from "@/components/jobs/JobCard";
import JobFilters from "@/components/jobs/JobFilters";
import { Skeleton } from "@/components/ui/skeleton";

interface Props {
  searchParams: Promise<{ q?: string; category?: string; qualification?: string; location?: string; page?: string }>;
}

function JobCardSkeleton() {
  return (
    <div className="border border-gray-200 rounded-lg p-5 space-y-3">
      <Skeleton className="h-4 w-24 rounded-full" />
      <Skeleton className="h-5 w-3/4" />
      <Skeleton className="h-4 w-1/2" />
      <div className="flex gap-4">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-4 w-24" />
      </div>
      <div className="flex gap-2 pt-1">
        <Skeleton className="h-8 flex-1" />
        <Skeleton className="h-8 flex-1" />
      </div>
    </div>
  );
}

async function JobList({ filters }: { filters: Record<string, string> }) {
  const page = Number(filters.page ?? 1);
  const data = await getJobs({ ...filters, page });

  if (data.jobs.length === 0) {
    return (
      <div className="text-center py-16 text-gray-500">
        <p className="text-lg font-medium">No jobs found</p>
        <p className="text-sm mt-1">Try adjusting your filters</p>
      </div>
    );
  }

  return (
    <div>
      <p className="text-sm text-gray-500 mb-4">
        Showing {data.jobs.length} of {data.total.toLocaleString("en-IN")} jobs
      </p>
      <div className="space-y-4">
        {data.jobs.map((job) => (
          <JobCard key={job.job_id} job={job} />
        ))}
      </div>

      {/* Pagination */}
      {data.total_pages > 1 && (
        <div className="flex justify-center gap-2 mt-8">
          {page > 1 && (
            <Link
              href={`/jobs?${new URLSearchParams({ ...filters, page: String(page - 1) })}`}
              className="px-4 py-2 border rounded-lg text-sm hover:bg-gray-50"
            >
              Previous
            </Link>
          )}
          <span className="px-4 py-2 text-sm text-gray-600">
            Page {page} of {data.total_pages}
          </span>
          {page < data.total_pages && (
            <Link
              href={`/jobs?${new URLSearchParams({ ...filters, page: String(page + 1) })}`}
              className="px-4 py-2 border rounded-lg text-sm hover:bg-gray-50"
            >
              Next
            </Link>
          )}
        </div>
      )}
    </div>
  );
}

export default async function JobsPage({ searchParams }: Props) {
  const params = await searchParams;
  const filters = Object.fromEntries(
    Object.entries(params).filter(([, v]) => Boolean(v))
  ) as Record<string, string>;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Link href="/" className="text-xl font-bold text-blue-600">JobDekho</Link>
          <Link href="/auth/login" className="text-sm text-blue-600 hover:underline">Sign In</Link>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Government Jobs 2026</h1>
          <p className="text-sm text-gray-500 mt-1">Updated every 6 hours from official sources</p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6">
          <Suspense>
            <JobFilters />
          </Suspense>
        </div>

        {/* Job list */}
        <Suspense fallback={
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => <JobCardSkeleton key={i} />)}
          </div>
        }>
          <JobList filters={filters} />
        </Suspense>
      </div>
    </div>
  );
}
