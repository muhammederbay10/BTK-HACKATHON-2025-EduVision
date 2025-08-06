/** @type {import('next').NextConfig} */
const nextConfig = {
  // Output in standalone mode for optimal Vercel deployment
  output: 'standalone',
  
  // Configure allowed image domains if you need to display external images
  images: {
    domains: ['btk-hackathon-2025-eduvision-production.up.railway.app'],
  },
};

module.exports = nextConfig;

