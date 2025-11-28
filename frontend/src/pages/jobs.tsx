import { useEffect, useState } from "react";
import Layout from "../components/Layout";

export default function Jobs() {
  const [jobs, setJobs] = useState<{[key: string]: any}>({});
  const [filter, setFilter] = useState<"all"|"queued"|"running"|"complete"|"failed">("all");

  useEffect(() => {
    const interval = setInterval(async () => {
      const data = await fetch("/api/status/all").then(r => r.json());
      setJobs(data);
    }, 800);
    return () => clearInterval(interval);
  }, []);

  // newest first
  const sorted = Object.entries(jobs).reverse();

  // filtering including queued
  const filtered = sorted.filter(([_, job]) => {
    if (filter === "all") return true;
    return job.status === filter;
  });

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Job Monitor</h1>

      {/* Filters (now includes queued) */}
      <div className="flex gap-3 mb-6">
        {["all","queued","running","complete","failed"].map(f => (
          <button
            key={f}
            onClick={() => setFilter(f as any)}
            className={`px-4 py-1 border rounded text-sm capitalize
              ${filter === f 
                ? "bg-blue-600 text-white border-blue-600"
                : "bg-white hover:bg-gray-100"
              }`}
          >
            {f}
          </button>
        ))}
      </div>

      {filtered.length === 0 && (
        <p className="text-gray-600 text-sm">No jobs in this category.</p>
      )}

      <div className="space-y-4">
        {filtered.map(([id, job]) => (
          <div key={id} className="bg-white shadow p-5 rounded border-l-4 border-blue-500">
            <div className="flex justify-between text-sm text-gray-700 mb-2">
              <span className="font-mono">{id}</span>

              <span className={
                job.status === "queued"   ? "text-yellow-600 font-medium" :
                job.status === "running"  ? "text-purple-600 font-medium" :
                job.status === "complete" ? "text-green-600 font-medium" :
                job.status === "failed"   ? "text-red-600 font-medium" : ""
              }>
                {job.status}
              </span>
            </div>

            <div className="w-full bg-gray-200 h-3 rounded">
              <div className="bg-blue-600 h-3 rounded" style={{ width:`${job.progress}%` }} />
            </div>

            <div className="flex justify-between text-xs text-gray-600 mt-1">
              <span>{job.progress}%</span>
              {job.error && <span className="text-red-600">{job.error}</span>}
            </div>

            <a href={`/job/${id}`} className="text-blue-600 underline text-sm block mt-3">
              View details
            </a>
          </div>
        ))}
      </div>
    </Layout>
  );
}
