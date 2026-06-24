"use client";

import Link from "next/link";
import { Bookmark, MapPin, GraduationCap, Users, Calendar } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { Job } from "@/types/job";
import { formatDate, formatSalary, daysLeft, categoryLabel, categoryColor } from "@/lib/format";

export default function JobCard({ job }: { job: Job }) {
  const days = daysLeft(job.application_end);
  const isUrgent = days !== null && days <= 7;

  return (
    <Card className="hover:shadow-md transition-shadow border border-gray-200">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            {/* Category + Urgency badges */}
            <div className="flex flex-wrap gap-2 mb-2">
              {job.category && (
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${categoryColor(job.category)}`}>
                  {categoryLabel(job.category)}
                </span>
              )}
              {isUrgent && (
                <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-red-100 text-red-700">
                  {days === 0 ? "Last day!" : `${days}d left`}
                </span>
              )}
            </div>

            {/* Title */}
            <Link href={`/jobs/${job.job_id}`}>
              <h3 className="font-semibold text-gray-900 text-base leading-snug hover:text-blue-600 transition-colors">
                {job.title}
              </h3>
            </Link>

            {/* Department */}
            {job.department && (
              <p className="text-sm text-gray-500 mt-0.5">{job.department}</p>
            )}

            {/* Meta row */}
            <div className="flex flex-wrap gap-x-4 gap-y-1 mt-3 text-sm text-gray-600">
              {job.location && job.location.length > 0 && (
                <span className="flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-gray-400" />
                  {job.location.slice(0, 2).join(", ")}
                </span>
              )}
              {job.qualification && job.qualification.length > 0 && (
                <span className="flex items-center gap-1">
                  <GraduationCap className="w-3.5 h-3.5 text-gray-400" />
                  {job.qualification.slice(0, 2).join(" / ")}
                </span>
              )}
              {job.vacancies && (
                <span className="flex items-center gap-1">
                  <Users className="w-3.5 h-3.5 text-gray-400" />
                  {job.vacancies.toLocaleString("en-IN")} posts
                </span>
              )}
            </div>

            {/* Salary + Deadline */}
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-2">
              <span className="text-sm font-medium text-green-700">
                {formatSalary(job)}
              </span>
              {job.application_end && (
                <span className={`flex items-center gap-1 text-sm ${isUrgent ? "text-red-600 font-medium" : "text-gray-500"}`}>
                  <Calendar className="w-3.5 h-3.5" />
                  Last date: {formatDate(job.application_end)}
                </span>
              )}
            </div>
          </div>

          {/* Save button */}
          <Button variant="ghost" size="icon" className="shrink-0 text-gray-400 hover:text-blue-600">
            <Bookmark className="w-4 h-4" />
          </Button>
        </div>

        {/* Apply button */}
        <div className="mt-4 flex gap-2">
          <Link href={`/jobs/${job.job_id}`} className="flex-1">
            <Button variant="outline" size="sm" className="w-full">
              View Details
            </Button>
          </Link>
          <a href={job.official_url} target="_blank" rel="noopener noreferrer" className="flex-1">
            <Button size="sm" className="w-full bg-blue-600 hover:bg-blue-700 text-white">
              Apply Now
            </Button>
          </a>
        </div>
      </CardContent>
    </Card>
  );
}
