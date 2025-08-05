export const API_BASE = process.env.NEXT_PUBLIC_API_URL || (
  process.env.NODE_ENV === 'production' 
    ? 'https://your-backend-domain.com' 
    : 'http://localhost:8000'
);