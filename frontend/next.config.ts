import type { NextConfig } from "next";

const isDocker = process.env.DOCKER === "true";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    middlewareClientMaxBodySize: 1024 * 1024 * 1024, // 1GB upload limit
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: isDocker
          ? "http://backend:8000/:path*"     // Docker compose
          : "http://localhost:8000/:path*"   // Local dev
      }
    ];
  },
  reactStrictMode: true,
};

export default nextConfig;
