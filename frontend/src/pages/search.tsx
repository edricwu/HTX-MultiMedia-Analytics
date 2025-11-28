import { useEffect, useState } from "react";
import Layout from "../components/Layout";

interface SearchResult {
  id: number;
  type: "video" | "audio";
  filename: string;
  score: number;
}

export default function SearchPage() {
  const [mode, setMode] = useState<"text" | "video" | "audio">("text");
  const [query, setQuery] = useState("");
  const [mediaList, setMediaList] = useState<any[]>([]);
  const [selectedMedia, setSelectedMedia] = useState<number | null>(null);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  // load available audio + video for reference-search
  useEffect(() => {
    async function load() {
      const [videos, audio] = await Promise.all([
        fetch("/api/videos").then(r => r.json()).catch(() => []),
        fetch("/api/transcriptions").then(r => r.json()).catch(() => []),
      ]);
      setMediaList([
        ...videos.map((v: any) => ({ id: v.id, filename: v.filename, type: "video" })),
        ...audio.map((a: any) => ({ id: a.id, filename: a.filename, type: "audio" })),
      ]);
    }
    load();
  }, []);

  async function runSearch() {
    setLoading(true);

    let url = "/api/search?top_k=5";
    if (mode === "text" && query.trim()) url += `&q=${encodeURIComponent(query)}`;
    if (mode === "video" && selectedMedia) url += `&video_id=${selectedMedia}`;
    if (mode === "audio" && selectedMedia) url += `&audio_id=${selectedMedia}`;

    const res = await fetch(url).then(r => r.json()).catch(() => []);
    setResults(res);
    setLoading(false);
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Unified Search</h1>

      <div className="max-w-xl space-y-5">

        {/* Search Mode Selector */}
        <div className="flex gap-3">
          <select
            className="border rounded p-2"
            value={mode}
            onChange={e => {
              setMode(e.target.value as any);
              setSelectedMedia(null);
              setQuery("");
            }}
          >
            <option value="text">Text Search</option>
            <option value="video">Video Similarity</option>
            <option value="audio">Audio Similarity</option>
          </select>
        </div>

        {/* Input changes depending on search mode */}

        {mode === "text" && (
          <input
            className="w-full border p-2 rounded"
            placeholder="search objects/transcript/media name"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === "Enter" && runSearch()}
          />
        )}

        {mode !== "text" && (
          <select
            className="w-full border p-2 rounded"
            value={selectedMedia ?? ""}
            onChange={e => setSelectedMedia(Number(e.target.value))}
          >
            <option disabled value="">Select a media reference</option>
            {mediaList
              .filter(m => m.type === mode)
              .map(m => (
                <option key={m.id} value={m.id}>
                  {m.type.toUpperCase()} — {m.filename}
                </option>
              ))}
          </select>
        )}

        <button
          onClick={runSearch}
          className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Search
        </button>

        {loading && <p className="text-gray-500">Searching...</p>}
        {!loading && results.length === 0 && (query || selectedMedia) && (
          <p className="text-gray-500">No results found.</p>
        )}

        {/* Results */}
        <div className="space-y-3 mt-4">
          {results.map(r => (
            <div
              key={`${r.type}-${r.id}`}
              className="bg-white shadow p-4 rounded border-l-4 border-blue-400 hover:shadow-md"
            >
              <div className="flex justify-between text-sm mb-1">
                <span className={`font-medium ${r.type === "video" ? "text-blue-600" : "text-green-600"}`}>
                  {r.type.toUpperCase()}
                </span>
                <span className="text-xs bg-gray-200 py-1 px-2 rounded">
                  score {r.score.toFixed(3)}
                </span>
              </div>
              <p className="font-semibold">{r.filename}</p>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
