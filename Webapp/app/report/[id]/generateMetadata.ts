// filepath: /Users/enes/Documents/eduvision/BTK-HACKATHON-2025-EduVision/Webapp/app/report/[id]/generateMetadata.ts

// This is a server component file that handles static parameters and metadata

// Force this page to be dynamically rendered
export const dynamic = 'force-dynamic';
export const dynamicParams = true;

// For static export compatibility
export async function generateStaticParams() {
  return [{ id: 'placeholder' }];
}

// Optional: You can also define metadata for the page
export async function generateMetadata({ params }: { params: { id: string } }) {
  return {
    title: `Report ${params.id} | EduVision`,
    description: 'Classroom engagement analysis report',
  };
}