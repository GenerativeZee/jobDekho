import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Search, Bell, Zap } from "lucide-react";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Link href="/" className="text-xl font-bold text-blue-600">
            JobDekho
          </Link>
          <div className="flex gap-3">
            <Link href="/jobs">
              <Button variant="ghost" size="sm">Browse Jobs</Button>
            </Link>
            <Link href="/auth/login">
              <Button size="sm" className="bg-blue-600 hover:bg-blue-700 text-white">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-3xl mx-auto text-center px-4 py-20">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight">
          Every Government Job.<br />
          <span className="text-blue-600">One Platform.</span>
        </h1>
        <p className="mt-4 text-lg text-gray-600 max-w-xl mx-auto">
          Stop missing opportunities. Get instant alerts for SSC, Railway, Banking, UPSC and all
          state government jobs — personalized for you.
        </p>

        <div className="mt-8 flex gap-2 max-w-xl mx-auto">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search jobs, e.g. SSC, Railway, Banking..."
              className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>
          <Link href="/jobs">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 h-auto">
              Search
            </Button>
          </Link>
        </div>

        <div className="mt-6 flex flex-wrap justify-center gap-2">
          {["SSC CGL", "IBPS PO", "Railway Group D", "UPSC CSE", "SBI Clerk"].map((term) => (
            <Link
              key={term}
              href={`/jobs?q=${encodeURIComponent(term)}`}
              className="text-sm text-blue-600 bg-blue-50 hover:bg-blue-100 px-3 py-1 rounded-full transition-colors"
            >
              {term}
            </Link>
          ))}
        </div>
      </section>

      {/* Stats */}
      <section className="max-w-4xl mx-auto px-4 pb-16">
        <div className="grid grid-cols-3 gap-6 text-center">
          {[
            { value: "10,000+", label: "Active Job Listings" },
            { value: "25+", label: "Government Sources" },
            { value: "Real-time", label: "Telegram Alerts" },
          ].map((stat) => (
            <div key={stat.label} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div className="text-2xl font-bold text-blue-600">{stat.value}</div>
              <div className="text-sm text-gray-500 mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="bg-white border-t border-gray-100 py-16">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-10">Why JobDekho?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Search className="w-6 h-6 text-blue-600" />,
                title: "All Jobs in One Place",
                desc: "UPSC, SSC, Railways, Banking, State PSC — aggregated and updated every 6 hours.",
              },
              {
                icon: <Bell className="w-6 h-6 text-blue-600" />,
                title: "Instant Alerts",
                desc: "Get Telegram and email alerts the moment a job matching your profile is posted.",
              },
              {
                icon: <Zap className="w-6 h-6 text-blue-600" />,
                title: "AI Match Score",
                desc: "See how well you match each job based on your education, location, and preferences.",
              },
            ].map((f) => (
              <div key={f.title} className="text-center">
                <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mx-auto mb-3">
                  {f.icon}
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">{f.title}</h3>
                <p className="text-sm text-gray-500">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 px-4 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-3">Start finding jobs today</h2>
        <p className="text-gray-500 mb-6">No account needed to browse. Sign up for personalized alerts.</p>
        <div className="flex justify-center gap-3">
          <Link href="/jobs">
            <Button variant="outline" size="lg">Browse All Jobs</Button>
          </Link>
          <Link href="/auth/login">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white">
              Create Free Account
            </Button>
          </Link>
        </div>
      </section>
    </main>
  );
}
