import Link from "next/link";
import { notFound } from "next/navigation";
import { ExternalLink, MapPin, GraduationCap, Users, Calendar, ArrowLeft, Building } from "lucide-react";
import { Button } from "@/components/ui/button";
import { getJob } from "@/lib/api";
import { formatDate, formatSalary, daysLeft, categoryLabel, categoryColor } from "@/lib/format";

interface Props {
  params: Promise<{ id: string }>;
}

export default async function JobDetailPage({ params }: Props) {
  const { id } = await params;

  let job;
  try {
    job = await getJob(id);
  } catch {
    notFound();
  }

  const days = daysLeft(job.application_end);
  const isUrgent = days !== null && days <= 7;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <Link href="/" className="text-xl font-bold text-blue-600">JobDekho</Link>
          <Link href="/auth/login" className="text-sm text-blue-600 hover:underline">Sign In</Link>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-6">
        <Link href="/jobs" className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 mb-5">
          <ArrowLeft className="w-4 h-4" /> Back to jobs
        </Link>

        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-4">
          {/* Header */}
          <div className="flex items-start justify-between gap-4 mb-4">
            <div>
              {job.category && (
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${categoryColor(job.category)}`}>
                  {categoryLabel(job.category)}
                </span>
              )}
              <h1 className="text-2xl font-bold text-gray-900 mt-2">{job.title}</h1>
              {job.department && (
                <p className="text-gray-500 mt-1 flex items-center gap-1">
                  <Building className="w-4 h-4" /> {job.department}
                </p>
              )}
            </div>
            {isUrgent && days !== null && (
              <div className="shrink-0 bg-red-50 border border-red-200 text-red-700 text-sm font-medium px-4 py-2 rounded-lg text-center">
                {days === 0 ? "Last day!" : `${days} days left`}
              </div>
            )}
          </div>

          {/* Key facts grid */}
          <div className="grid sm:grid-cols-2 gap-4 py-4 border-t border-gray-100">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-green-50 rounded-lg flex items-center justify-center shrink-0">
                <span className="text-green-700 text-xs font-bold">₹</span>
              </div>
              <div>
                <p className="text-xs text-gray-400 uppercase tracking-wide">Salary</p>
                <p className="text-sm font-medium text-gray-900">{formatSalary(job)}</p>
              </div>
            </div>

            {job.location && (
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center shrink-0">
                  <MapPin className="w-4 h-4 text-blue-600" />
                </div>
                <div>
                  <p className="text-xs text-gray-400 uppercase tracking-wide">Location</p>
                  <p className="text-sm font-medium text-gray-900">{job.location.join(", ")}</p>
                </div>
              </div>
            )}

            {job.qualification && (
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-purple-50 rounded-lg flex items-center justify-center shrink-0">
                  <GraduationCap className="w-4 h-4 text-purple-600" />
                </div>
                <div>
                  <p className="text-xs text-gray-400 uppercase tracking-wide">Education</p>
                  <p className="text-sm font-medium text-gray-900">{job.qualification.join(" / ")}</p>
                </div>
              </div>
            )}

            {job.vacancies && (
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-orange-50 rounded-lg flex items-center justify-center shrink-0">
                  <Users className="w-4 h-4 text-orange-600" />
                </div>
                <div>
                  <p className="text-xs text-gray-400 uppercase tracking-wide">Vacancies</p>
                  <p className="text-sm font-medium text-gray-900">
                    {job.vacancies.toLocaleString("en-IN")} posts
                  </p>
                </div>
              </div>
            )}

            {(job.min_age || job.max_age) && (
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-gray-50 rounded-lg flex items-center justify-center shrink-0">
                  <span className="text-gray-500 text-xs font-bold">Age</span>
                </div>
                <div>
                  <p className="text-xs text-gray-400 uppercase tracking-wide">Age Limit</p>
                  <p className="text-sm font-medium text-gray-900">
                    {job.min_age && job.max_age
                      ? `${job.min_age} – ${job.max_age} years`
                      : job.max_age
                      ? `Up to ${job.max_age} years`
                      : `Min ${job.min_age} years`}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Important dates */}
          <div className="border-t border-gray-100 pt-4 mt-2">
            <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">
              Important Dates
            </h2>
            <div className="space-y-2">
              {job.notification_date && (
                <div className="flex items-center gap-2 text-sm">
                  <Calendar className="w-4 h-4 text-gray-400 shrink-0" />
                  <span className="text-gray-500 w-40">Notification Date</span>
                  <span className="text-gray-900">{formatDate(job.notification_date)}</span>
                </div>
              )}
              {job.application_start && (
                <div className="flex items-center gap-2 text-sm">
                  <Calendar className="w-4 h-4 text-gray-400 shrink-0" />
                  <span className="text-gray-500 w-40">Application Opens</span>
                  <span className="text-gray-900">{formatDate(job.application_start)}</span>
                </div>
              )}
              {job.application_end && (
                <div className="flex items-center gap-2 text-sm">
                  <Calendar className="w-4 h-4 text-gray-400 shrink-0" />
                  <span className="text-gray-500 w-40">Application Closes</span>
                  <span className={`font-medium ${isUrgent ? "text-red-600" : "text-gray-900"}`}>
                    {formatDate(job.application_end)}
                    {isUrgent && days !== null && ` (${days === 0 ? "today!" : `${days} days`})`}
                  </span>
                </div>
              )}
              {job.exam_date && (
                <div className="flex items-center gap-2 text-sm">
                  <Calendar className="w-4 h-4 text-gray-400 shrink-0" />
                  <span className="text-gray-500 w-40">Exam Date</span>
                  <span className="text-gray-900">{formatDate(job.exam_date)}</span>
                </div>
              )}
            </div>
          </div>

          {/* Source */}
          <div className="border-t border-gray-100 pt-4 mt-4 flex items-center gap-2">
            <span className="text-xs text-gray-400">Source:</span>
            <span className="text-xs font-medium text-gray-600 uppercase">{job.source}</span>
            <span className="text-xs text-green-600 ml-auto">Verified — official link</span>
          </div>
        </div>

        {/* Disclaimer + CTA */}
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-4 text-sm text-amber-800">
          Always verify details on the official website before applying. Deadlines and eligibility may change.
        </div>

        <div className="flex gap-3">
          <a href={job.official_url} target="_blank" rel="noopener noreferrer" className="flex-1">
            <Button size="lg" className="w-full bg-blue-600 hover:bg-blue-700 text-white gap-2">
              Apply on Official Website <ExternalLink className="w-4 h-4" />
            </Button>
          </a>
        </div>
      </div>
    </div>
  );
}
