"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

const CATEGORIES = [
  { value: "", label: "All Categories" },
  { value: "banking", label: "Banking" },
  { value: "railway", label: "Railway" },
  { value: "ssc", label: "SSC" },
  { value: "upsc", label: "UPSC" },
  { value: "defence", label: "Defence" },
  { value: "psc", label: "State PSC" },
  { value: "police", label: "Police" },
  { value: "health", label: "Health" },
  { value: "teaching", label: "Teaching" },
];

const QUALIFICATIONS = [
  { value: "", label: "All Qualifications" },
  { value: "10th", label: "10th Pass" },
  { value: "12th", label: "12th Pass" },
  { value: "ITI", label: "ITI" },
  { value: "diploma", label: "Diploma" },
  { value: "graduate", label: "Graduate" },
  { value: "postgraduate", label: "Postgraduate" },
];

export default function JobFilters() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const updateFilter = useCallback(
    (key: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString());
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
      params.delete("page");
      router.push(`/jobs?${params.toString()}`);
    },
    [router, searchParams]
  );

  return (
    <div className="space-y-3">
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <Input
          className="pl-9"
          placeholder="Search jobs..."
          defaultValue={searchParams.get("q") ?? ""}
          onChange={(e) => {
            const v = e.target.value;
            const t = setTimeout(() => updateFilter("q", v), 400);
            return () => clearTimeout(t);
          }}
        />
      </div>

      {/* Category */}
      <div>
        <label className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1 block">
          Category
        </label>
        <div className="flex flex-wrap gap-2">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.value}
              onClick={() => updateFilter("category", cat.value)}
              className={`text-sm px-3 py-1 rounded-full border transition-colors ${
                (searchParams.get("category") ?? "") === cat.value
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-white text-gray-600 border-gray-200 hover:border-blue-400"
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Qualification */}
      <div>
        <label className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1 block">
          Qualification
        </label>
        <div className="flex flex-wrap gap-2">
          {QUALIFICATIONS.map((q) => (
            <button
              key={q.value}
              onClick={() => updateFilter("qualification", q.value)}
              className={`text-sm px-3 py-1 rounded-full border transition-colors ${
                (searchParams.get("qualification") ?? "") === q.value
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-white text-gray-600 border-gray-200 hover:border-blue-400"
              }`}
            >
              {q.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
