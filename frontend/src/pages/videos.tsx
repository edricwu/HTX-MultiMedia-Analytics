import { useEffect, useState } from "react";
import Layout from "../components/Layout";

export default function VideosPage() {
  const [videos, setVideos] = useState<any[]>([]);
  const [active, setActive] = useState<any|null>(null);
  const [selectedFrame, setSelectedFrame] = useState(0);
  const [fullscreen, setFullscreen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    fetch("/api/videos")
      .then(r => r.json())
      .then(d => {
        setVideos(d);
        if (d.length > 0) setActive(d[0]);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Processed Videos</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

      {/* LEFT PANEL — List View (now matches Audio style) */}
      <div className="bg-white shadow rounded p-4">
        <h2 className="font-semibold mb-3">Files</h2>

        {loading && <p className="text-sm text-gray-500">Loading...</p>}

        {!loading && videos.length === 0 && (
          <p className="text-gray-500 text-sm">No videos processed yet.</p>
        )}

        <div className="flex flex-col gap-2 max-h-[75vh] overflow-y-auto">
          {videos.map((v) => (
            <button
              key={v.id}
              onClick={() => { setActive(v); setSelectedFrame(0); }}
              className={`p-2 text-left rounded border 
                ${active?.id === v.id ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 hover:bg-gray-100"}`}
            >
              <div className="font-mono text-sm">{v.filename}</div>
              <div className="text-xs text-gray-600">
                {new Date(v.created_at).toLocaleString()}
              </div>
            </button>
          ))}
        </div>
      </div>


      {/* RIGHT PANEL — Viewer */}
      <div className="lg:col-span-2 bg-white shadow rounded p-5">

        {/* When no active video (empty state matches audio.tsx) */}
        {!active && (
          <p className="text-gray-600 text-sm">
            Select a video to view frames/detections
          </p>
        )}

        {active && (
          <>
            <h2 className="text-lg font-semibold mb-2">{active.filename}</h2>

            <p className="text-gray-600 mb-2">
              {expanded
                ? active.summary
                : active.summary.length > 200
                ? active.summary.slice(0,200) + "..."
                : active.summary}
            </p>

            {active.summary.length > 200 && (
              <button
                className="text-blue-600 underline text-sm mb-3"
                onClick={() => setExpanded(e => !e)}
              >
                {expanded ? "Show Less" : "Show More"}
              </button>
            )}

            {/* Frame selector */}
            <div className="flex gap-2 mb-3 flex-wrap">
              {active.detections?.map((f:any, i:number) => (
                <button
                  key={i}
                  onClick={() => setSelectedFrame(i)}
                  className={`px-3 py-1 text-sm rounded
                    ${i===selectedFrame ? "bg-blue-500 text-white" : "bg-gray-200 hover:bg-gray-300"}`}
                >
                  Frame {f.frame_index}
                </button>
              ))}
            </div>

            {/* Fullscreen button */}
            <button
              className="px-3 py-1 mb-2 bg-gray-800 text-white rounded text-sm hover:bg-black"
              onClick={() => setFullscreen(true)}
            >
              Fullscreen View
            </button>

            <img
              src={`data:image/jpeg;base64,${active.detections[selectedFrame].frame_base64}`}
              className="rounded shadow max-w-full"
            />


            {/* FULLSCREEN OVERLAY */}
            {fullscreen && (
              <div
                className="fixed inset-0 bg-black/90 flex items-center justify-center z-50"
                onClick={() => setFullscreen(false)}
              >
                <div className="relative" onClick={(e) => e.stopPropagation()}>
                  <img
                    src={`data:image/jpeg;base64,${active.detections[selectedFrame].frame_base64}`}
                    className="max-h-[95vh] max-w-[95vw] rounded shadow-2xl"
                  />
                  <button
                    className="absolute top-3 right-3 bg-white/90 px-3 py-1 rounded shadow hover:bg-white"
                    onClick={() => setFullscreen(false)}
                  >
                    ✕ Close
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  </Layout>
  );
}
