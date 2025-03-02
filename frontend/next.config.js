/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*'
      }
    ]
  },
  webpack: (config, { isServer }) => {
    config.infrastructureLogging = {
      level: 'error',
    }
    return config
  },
}

module.exports = nextConfig 