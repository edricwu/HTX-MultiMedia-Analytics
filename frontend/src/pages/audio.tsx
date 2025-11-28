import { useEffect, useState } from "react";
import Layout from "../components/Layout";

export default function AudioPage() {
  const [items, setItems] = useState<any[]>([]);
  const [selected, setSelected] = useState<number|null>(null);

  useEffect(() => {
    fetch("/api/transcriptions")
      .then(r => r.json())
      .then(setItems);
  }, []);

  const active = selected !== null ? items[selected] : null;

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Audio Transcriptions</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* LEFT – list of processed audio files */}
        <div className="bg-white shadow rounded p-4">
          <h2 className="font-semibold mb-3">Files</h2>
          <div className="flex flex-col gap-2">

            {items.map((a, i) => (
              <button
                key={a.id}
                onClick={() => setSelected(i)}
                className={`p-2 text-left rounded border 
                  ${selected===i ? "border-blue-500 bg-blue-50" : "border-gray-200 hover:bg-gray-100"}`}
              >
                <div className="font-mono text-sm">{a.filename}</div>
                <div className="text-xs text-gray-600">
                  Segments: {a.segments.length}
                </div>
              </button>
            ))}

          </div>
        </div>

        {/* RIGHT – transcription detail viewer */}
        <div className="lg:col-span-2 bg-white shadow rounded p-5">
          {!active && (
            <p className="text-gray-600 text-sm">Select a file to view transcription</p>
          )}

          {active && (
            <>
              <h2 className="text-lg font-semibold mb-4">{active.filename}</h2>

              <div className="space-y-3 max-h-[75vh] overflow-y-auto pr-2">
                {active.segments.map((seg: any, ix: number) => (
                  <div key={ix} className="border-b pb-2">
                    <div className="flex justify-between text-xs text-gray-600 mb-1">
                      <span>Timestamp: {seg.start.toFixed(1)}s → {seg.end.toFixed(1)}s</span>
                      <span className="text-gray-700 font-medium">
                        Confidence score: {(seg.confidence*100).toFixed(1)}%
                      </span>
                    </div>
                    <p className="text-gray-900">{seg.text}</p>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </Layout>
  );
}
