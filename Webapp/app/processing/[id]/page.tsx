import ProcessingPage from './ProcessingPage';
// Import just what we need without causing naming conflicts
import { generateStaticParams as getParams } from '../../api/dynamicRender';

// Force this page to be dynamically rendered
// These settings tell Next.js to render this page at request time, not build time
export const dynamicParams = true;
export const dynamic = 'force-dynamic';

// This function is used for static generation of placeholder routes only
// All other routes will be rendered at runtime
export const generateStaticParams = getParams;

export default function Page({ params }: { params: { id: string } }) {
  return <ProcessingPage reportId={params.id} />;
}