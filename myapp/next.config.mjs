/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
  reactCompiler: true,
  output: 'standalone', // For Docker deployment
  images: {
    unoptimized: true, // For static export if needed
  },
};

export default nextConfig;
