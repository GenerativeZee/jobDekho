export function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function formatSalary(job: {
  salary_min: number | null;
  salary_max: number | null;
  salary_text: string | null;
}): string {
  if (job.salary_text) return job.salary_text;
  if (job.salary_min && job.salary_max)
    return `Rs.${job.salary_min.toLocaleString("en-IN")} – Rs.${job.salary_max.toLocaleString("en-IN")}/month`;
  if (job.salary_min)
    return `Rs.${job.salary_min.toLocaleString("en-IN")}/month`;
  return "As per norms";
}

export function daysLeft(dateStr: string | null): number | null {
  if (!dateStr) return null;
  const diff = new Date(dateStr).getTime() - Date.now();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

export function categoryLabel(cat: string): string {
  const labels: Record<string, string> = {
    banking: "Banking",
    railway: "Railway",
    ssc: "SSC",
    defence: "Defence",
    psc: "State PSC",
    upsc: "UPSC",
    engineering: "Engineering",
    teaching: "Teaching",
    police: "Police",
    health: "Health",
  };
  return labels[cat] ?? cat;
}

export function categoryColor(cat: string): string {
  const colors: Record<string, string> = {
    banking: "bg-blue-100 text-blue-800",
    railway: "bg-orange-100 text-orange-800",
    ssc: "bg-purple-100 text-purple-800",
    defence: "bg-red-100 text-red-800",
    psc: "bg-green-100 text-green-800",
    upsc: "bg-yellow-100 text-yellow-800",
    engineering: "bg-cyan-100 text-cyan-800",
    teaching: "bg-pink-100 text-pink-800",
    police: "bg-gray-100 text-gray-800",
    health: "bg-teal-100 text-teal-800",
  };
  return colors[cat] ?? "bg-gray-100 text-gray-700";
}
