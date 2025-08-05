/**
 * Environment configuration utility
 * This file provides centralized access to environment variables
 */

export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
};
