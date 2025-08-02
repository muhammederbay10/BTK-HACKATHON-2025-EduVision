import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// This middleware runs before any request is completed
export function middleware(request: NextRequest) {
  // Get the pathname of the request
  const pathname = request.nextUrl.pathname;

  // Check if the request is for a processing or report page with a UUID
  if (pathname.match(/^\/(processing|report)\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/)) {
    console.log(`Middleware: Detected dynamic route: ${pathname}`);
    // Allow the request to proceed normally
    return NextResponse.next();
  }

  // For all other requests, proceed normally
  return NextResponse.next();
}

// Configure the paths that trigger this middleware
export const config = {
  matcher: [
    // Match all routes that start with /processing/ or /report/
    '/processing/:path*',
    '/report/:path*',
  ],
};