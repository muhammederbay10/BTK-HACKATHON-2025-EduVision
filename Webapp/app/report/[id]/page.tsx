"use client"

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertCircleIcon, FileTextIcon } from 'lucide-react';

interface ReportPageProps {
  params: { id: string };
}

export default function ReportPage({ params }: ReportPageProps) {
  const [report, setReport] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const reportId = params.id;

  useEffect(() => {
    const fetchReport = async () => {
      // Don't try to fetch during static build/export
      if (reportId === 'placeholder') {
        setLoading(false);
        return;
      }
      
      try {
        setLoading(true);
        console.log("Fetching report for ID:", reportId);
        
        try {
          // First attempt: try to get the report directly
          const response = await fetch(`http://localhost:8000/report/${reportId}`);
          
          if (response.ok) {
            const data = await response.json();
            console.log("Report data received:", data);
            // Handle both cases: data.report or data directly containing the report
            setReport(data.report || data);
            setLoading(false);
            return;
          } else {
            console.log("Regular report endpoint failed, trying fallback...");
          }
        } catch (directErr) {
          console.log("Error fetching direct report:", directErr);
        }
        
        // Second attempt: check the status endpoint
        try {
          const statusResponse = await fetch(`http://localhost:8000/api/status/${reportId}`);
          if (statusResponse.ok) {
            const statusData = await statusResponse.json();
            console.log("Status data:", statusData);
            
            if (statusData.status === "completed") {
              // Status says completed but we couldn't fetch the report directly
              // Create a fallback report
              setReport({
                type: "text",
                content: `Your video has been processed successfully.\n\nThe classroom report has been generated on the server. The processing ID was: ${reportId}.\n\nPlease check the server's reports directory for the full analysis.`
              });
              setLoading(false);
              return;
            }
          }
        } catch (statusErr) {
          console.log("Error checking status:", statusErr);
        }
        
        throw new Error(`Could not fetch report data for ID: ${reportId}`);
      } catch (err: any) {
        console.error('Error fetching report:', err);
        setError(`Failed to load report: ${err?.message || 'Unknown error'}`);
        setLoading(false);
      }
    };

    fetchReport();
  }, [reportId]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-3xl font-bold mb-4">Loading Report...</h1>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <AlertCircleIcon className="h-16 w-16 text-red-500 mx-auto mb-4" />
        <h1 className="text-3xl font-bold mb-4">Error</h1>
        <p className="mb-8">{error}</p>
        <Button 
          onClick={() => router.push('/upload')}
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
        >
          Try Again
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-4xl mx-auto"
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Your Engagement Report
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-2">
            Report ID: {reportId}
          </p>
        </div>

        <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-xl mb-8">
          <CardContent className="p-6">
            {report ? (
              <div>
                <div className="flex items-center mb-4">
                  <FileTextIcon className="h-6 w-6 text-blue-500 mr-2" />
                  <h2 className="text-2xl font-bold">Report Summary</h2>
                </div>
                
                {/* Handle different report formats */}
                {report.type === "text" ? (
                  <div className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-auto whitespace-pre-wrap text-sm">
                    {report.content}
                  </div>
                ) : report.content ? (
                  <div className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-auto whitespace-pre-wrap text-sm">
                    {report.content}
                  </div>
                ) : (
                  <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-auto text-sm">
                    {JSON.stringify(report, null, 2)}
                  </pre>
                )}
              </div>
            ) : (
              <p>No report data available.</p>
            )}
          </CardContent>
        </Card>

        <div className="text-center">
          <Button 
            onClick={() => router.push('/upload')}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
          >
            Upload Another Video
          </Button>
        </div>
      </motion.div>
    </div>
  );
}

// Force this page to be dynamically rendered
export const dynamic = 'force-dynamic';
export const dynamicParams = true;

// For static export compatibility
export async function generateStaticParams() {
  return [{ id: 'placeholder' }];
}