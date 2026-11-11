import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  cacheComponents: true,
  allowedDevOrigins: ['127.0.0.1'],
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "www.poewiki.net",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
