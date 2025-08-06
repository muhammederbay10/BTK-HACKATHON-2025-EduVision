## Deployment Guide

### Environment Configuration

The application uses environment variables to handle different deployment environments. We've centralized the backend API URL configuration.

1. Create environment files for different environments:

#### Development (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Production (.env.production)
```bash
NEXT_PUBLIC_API_URL=https://btk-hackathon-2025-eduvision-production.up.railway.app
```

2. Deploy to Vercel:
   - Ensure you've added the environment variables in your Vercel project settings:
     - Go to your project in the Vercel dashboard
     - Navigate to Settings > Environment Variables
     - Add `NEXT_PUBLIC_API_URL` with your production backend URL

3. To deploy locally with production settings:
```bash
npm run build
npm run start
```

### Notes
- All API requests in the codebase reference the environment variable through the config utility
- To change the backend URL, you only need to update the environment variable
