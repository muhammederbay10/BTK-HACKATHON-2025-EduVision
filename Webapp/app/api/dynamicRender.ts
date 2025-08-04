// This ensures your page doesn't use static exports for dynamic routes
export const generateStaticParams = async () => {
  // Return a set of placeholder IDs for static generation
  // These will be used during build time, but dynamic routes will still work at runtime
  return [
    { id: 'placeholder' },
    // You can add more IDs here for testing if needed
    { id: 'demo' }
  ];
};

// Helper function to generate fallback routes that should always work
export const getFallbackRoutes = () => {
  // This would be for testing purposes
  return ['placeholder', 'demo'];
};