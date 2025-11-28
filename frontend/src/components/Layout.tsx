export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-6xl mx-auto p-4 flex gap-6 font-medium">
          <a href="/" className="hover:text-blue-600">Dashboard</a>
          <a href="/upload" className="hover:text-blue-600">Upload</a>
          <a href="/videos" className="hover:text-blue-600">Videos</a>
          <a href="/audio" className="hover:text-blue-600">Transcriptions</a>
          <a href="/search" className="hover:text-blue-600">Search</a>
          <a href="/jobs" className="hover:text-blue-600">Jobs</a>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto p-10">{children}</main>
    </div>
  );
}
