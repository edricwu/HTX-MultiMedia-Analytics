import Layout from "../components/Layout";

export default function Home() {
  return (
    <Layout>
      <h1 className="text-3xl font-bold mb-6">Media Analytics Dashboard</h1>

      <p className="text-gray-600 mb-8">
        Monitor processing jobs, upload media for analysis, view extracted video summaries, 
        and run semantic search across audio + video embeddings.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">

        <a href="/upload"
           className="bg-white p-6 shadow rounded hover:border-blue-500 border transition">
          <h2 className="text-lg font-semibold mb-1">Upload</h2>
          <p className="text-gray-600 text-sm">Process new media files</p>
        </a>

        <a href="/videos"
           className="bg-white p-6 shadow rounded hover:border-blue-500 border transition">
          <h2 className="text-lg font-semibold mb-1">Videos</h2>
          <p className="text-gray-600 text-sm">View object detection summaries</p>
        </a>

        <a href="/audio"
           className="bg-white p-6 shadow rounded hover:border-blue-500 border transition">
          <h2 className="text-lg font-semibold mb-1">Transcriptions</h2>
          <p className="text-gray-600 text-sm">Speech analysis + transcripts</p>
        </a>

        <a href="/search"
           className="bg-white p-6 shadow rounded hover:border-blue-500 border transition">
          <h2 className="text-lg font-semibold mb-1">Search</h2>
          <p className="text-gray-600 text-sm">Semantic cross-media search</p>
        </a>

        <a href="/jobs"
           className="bg-white p-6 shadow rounded hover:border-blue-500 border transition">
          <h2 className="text-lg font-semibold mb-1">Jobs Monitor</h2>
          <p className="text-gray-600 text-sm">Track all running & completed tasks</p>
        </a>

      </div>
    </Layout>
  );
}
