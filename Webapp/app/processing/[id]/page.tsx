import ProcessingPage from './ProcessingPage';

// Force dynamic rendering
export const dynamic = 'force-dynamic';

// Use any type to bypass TypeScript checks for page props
export default function Page({ params }: any) {
  // Extract the ID from params
  const reportId = params?.id;
  
  // Return the client component
  return <ProcessingPage reportId={reportId} />;
}