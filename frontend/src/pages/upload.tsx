import { useState, DragEvent } from "react";
import Layout from "../components/Layout";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [type, setType] = useState("video");
  const [jobId, setJobId] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);

  const [error, setError] = useState<string | null>(null);


  function handleDrag(e: DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragover") setDragActive(true);
    if (e.type === "dragleave") setDragActive(false);
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  }

  async function submit() {
    if (!file) {
      alert("No file selected");
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const form = new FormData();
      form.append("file", file);

      const res = await fetch(`/api/process/${type}`, { method: "POST", body: form });

      if (!res.ok) {
        // surfacing backend HTTP errors (e.g. 422, 500)
        const text = await res.text();
        throw new Error(`Request failed (${res.status}): ${text}`);
      }

      const data = await res.json();
      setJobId(data.job_id);
    } catch (e: any) {
      console.error("Upload error:", e);
      setError(e.message ?? "Upload failed");
    } finally {
      setUploading(false);
    }
  }


  return (
    <Layout>
      <div className="max-w-lg mx-auto">

        <h1 className="text-2xl font-bold mb-6">Upload Media</h1>

        <div
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={() => document.getElementById("file-input")?.click()}  // ← makes whole box clickable
          className={`border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition
    ${dragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-white hover:border-blue-300"}`}
        >
          <p className="text-gray-600">
            {file ? `Selected: ${file.name}` : "Drag & drop or click to select a file"}
          </p>

          <input
            id="file-input"
            data-testid="upload-input"
            type="file"
            className="hidden"
            onChange={e => setFile(e.target.files?.[0] ?? null)}
          />
        </div>

        <div className="mt-6 space-y-4 p-6 bg-white rounded shadow">

          <label className="flex flex-col gap-1">
            <span className="font-medium">Media Type</span>
            <select
              className="border rounded px-3 py-2"
              value={type}
              onChange={e => setType(e.target.value)}
            >
              <option value="video">Video</option>
              <option value="audio">Audio</option>
            </select>
          </label>

          <button
            disabled={uploading}
            onClick={submit}
            className={`w-full py-2 rounded text-white font-medium transition
              ${uploading ? "bg-blue-300" : "bg-blue-600 hover:bg-blue-700"}`}
          >
            {uploading ? "Uploading..." : "Start Processing"}
          </button>
        </div>

        {jobId && (
          <div className="mt-6 p-4 rounded bg-green-100 text-green-800">
            Job submitted. View progress:
            <a className="underline ml-1" href={`/job/${jobId}`}>{jobId}</a>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 rounded bg-red-100 text-red-800 text-sm">
            {error}
          </div>
        )}

      </div>
    </Layout>
  );
}
