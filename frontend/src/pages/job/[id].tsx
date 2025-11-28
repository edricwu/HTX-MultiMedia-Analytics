import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Layout from "../../components/Layout";

export default function JobStatus() {
  const { query } = useRouter();
  const id = query.id as string;
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (!id) return;

    const interval = setInterval(async () => {
      const res = await fetch(`/api/status/${id}`).then(r => r.json());
      setData(res);
    }, 1000);

    return () => clearInterval(interval);
  }, [id]);

  const status = data?.status;
  const progress = data?.progress ?? 0;

  return (
    <Layout>
      <div className="max-w-lg mx-auto">
        <h1 className="text-2xl font-bold mb-6">Job Status</h1>

        <div className="bg-white rounded shadow p-6 space-y-4">

          <div className="flex justify-between text-sm text-gray-600">
            <span>Job ID</span>
            <span className="font-mono text-gray-800">{id}</span>
          </div>

          <div className="flex justify-between text-sm">
            <span>Status</span>
            <span
              className={`font-medium ${
                status === "complete" ? "text-green-600" :
                status === "failed"   ? "text-red-600"   :
                "text-blue-600"
              }`}
            >
              {status ?? "loading"}
            </span>
          </div>

          {/* Progress bar */}
          <div>
            <div className="w-full bg-gray-200 h-3 rounded">
              <div
                className="bg-blue-600 h-3 rounded transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-xs text-center mt-1 text-gray-600">{progress}%</p>
          </div>

          {/* Error state */}
          {data?.error && (
            <p className="text-red-600 text-sm border border-red-300 bg-red-50 p-2 rounded">
              {data.error}
            </p>
          )}

          {/* Navigation on completion */}
          {status === "complete" && (
            <a
              href="/videos"
              className="block text-center bg-green-600 text-white py-2 rounded hover:bg-green-700 transition"
            >
              View Results
            </a>
          )}
        </div>
      </div>
    </Layout>
  );
}
