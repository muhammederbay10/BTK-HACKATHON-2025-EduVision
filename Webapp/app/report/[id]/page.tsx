"use client"

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertCircleIcon, FileTextIcon, FileIcon, DownloadIcon, UsersIcon, PieChartIcon, LightbulbIcon, BarChartIcon } from 'lucide-react';
import dynamic from 'next/dynamic';
import { PDFExportButton } from '@/components/pdf-export-button';

// Utility function to process markdown-like text
const processMarkdown = (text: string) => {
  if (!text) return '';
  
  // Process bullet points
  return text.split('\n').map(line => {
    // Handle bullet points and indentation
    if (line.match(/^\s*\*\s/)) {
      return `<li class="mb-2 ml-2">${line.replace(/^\s*\*\s/, '')}</li>`;
    }
    // Handle sub-bullet points
    if (line.match(/^\s{4,}\*\s/)) {
      return `<li class="mb-2 ml-6">${line.replace(/^\s*\*\s/, '')}</li>`;
    }
    // Bold text between ** markers
    let processedLine = line;
    processedLine = processedLine.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Regular text
    return processedLine ? `<p class="mb-2">${processedLine}</p>` : '<br/>';
  }).join('');
};

// CSS styles for the report display
const reportStyles = {
  card: "bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-xl mb-8 hover:shadow-2xl transition-shadow duration-300",
  cardContent: "p-6",
  sectionHeading: "flex items-center mb-4",
  sectionIcon: "h-6 w-6 text-blue-500 mr-2",
  sectionTitle: "text-2xl font-bold",
  contentBox: "bg-gray-100 dark:bg-gray-900 p-5 rounded-lg",
  markdown: "list-none whitespace-pre-wrap",
  metaItem: "bg-gray-100 dark:bg-gray-900 p-3 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors duration-200",
  metaLabel: "text-sm text-gray-500 dark:text-gray-400",
  metaValue: "font-semibold",
  exportButton: "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 flex items-center gap-2 transition-all duration-200 transform hover:scale-105"
};

interface ReportPageProps {
  params: { id: string };
}

interface ReportMetadata {
  report_type: string;
  course_name: string;
  date: string;
  session_time: string;
  students_analyzed: number;
  generated_at: string;
  processing_time: string;
  video_id: string;
}

interface StudentSummary {
  total_students: number;
  student_list: string[];
}

interface AIAnalysis {
  executive_summary: string;
  individual_student_analysis: string;
  temporal_analysis: string;
  classroom_dynamics: string;
  actionable_recommendations: string;
  metrics_summary: string;
}

interface ReportData {
  report_metadata: ReportMetadata;
  student_summary: StudentSummary;
  ai_analysis: AIAnalysis;
  data_insights: {
    report_id: string;
  };
  type?: string;
  content?: string;
}

export default function ReportPage({ params }: ReportPageProps) {
  const [report, setReport] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const reportId = params.id;

  // PDF export functionality has been moved to the PDFExportButton component

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
              } as ReportData);
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

  // Render text-only report
  if (report?.type === "text" && report?.content) {
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

          <Card className={reportStyles.card}>
            <CardContent className={reportStyles.cardContent}>
              <div>
                <div className={reportStyles.sectionHeading}>
                  <FileTextIcon className={reportStyles.sectionIcon} />
                  <h2 className={reportStyles.sectionTitle}>Report Summary</h2>
                </div>
                <div className={reportStyles.contentBox}>
                  <div className={reportStyles.markdown} 
                      dangerouslySetInnerHTML={{ 
                        __html: processMarkdown(report.content) 
                      }} 
                  />
                </div>
              </div>
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

  // Render structured report
  return (
    <div className="container mx-auto px-4 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-5xl mx-auto"
        id="report-container"
      >
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Classroom Engagement Analysis
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            Report ID: {reportId}
          </p>
          <div className="flex justify-center mb-4">
            <PDFExportButton 
              reportId={reportId} 
              className={reportStyles.exportButton}
            />
          </div>
        </div>

        {report?.report_metadata && (
          <Card className={reportStyles.card}>
            <CardContent className={reportStyles.cardContent}>
              <div className={reportStyles.sectionHeading}>
                <FileIcon className={reportStyles.sectionIcon} />
                <h2 className={reportStyles.sectionTitle}>Report Metadata</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className={reportStyles.metaItem}>
                  <p className={reportStyles.metaLabel}>Report Type</p>
                  <p className={reportStyles.metaValue}>{report.report_metadata.report_type}</p>
                </div>
                <div className={reportStyles.metaItem}>
                  <p className={reportStyles.metaLabel}>Course Name</p>
                  <p className={reportStyles.metaValue}>{report.report_metadata.course_name}</p>
                </div>
                <div className={reportStyles.metaItem}>
                  <p className={reportStyles.metaLabel}>Date</p>
                  <p className={reportStyles.metaValue}>{report.report_metadata.date}</p>
                </div>
                <div className={reportStyles.metaItem}>
                  <p className={reportStyles.metaLabel}>Session Time</p>
                  <p className={reportStyles.metaValue}>{report.report_metadata.session_time}</p>
                </div>
                <div className={reportStyles.metaItem}>
                  <p className={reportStyles.metaLabel}>Students Analyzed</p>
                  <p className={reportStyles.metaValue}>{report.report_metadata.students_analyzed}</p>
                </div>
                <div className={reportStyles.metaItem}>
                  <p className={reportStyles.metaLabel}>Generated At</p>
                  <p className={reportStyles.metaValue}>{new Date(report.report_metadata.generated_at).toLocaleString()}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {report?.student_summary && (
          <Card className={reportStyles.card}>
            <CardContent className={reportStyles.cardContent}>
              <div className={reportStyles.sectionHeading}>
                <UsersIcon className={reportStyles.sectionIcon} />
                <h2 className={reportStyles.sectionTitle}>Student Summary</h2>
              </div>
              <div className={reportStyles.contentBox}>
                <p className="text-lg font-semibold mb-2">Total Students: {report.student_summary.total_students}</p>
                <h3 className="text-md font-medium text-gray-600 dark:text-gray-400 mb-2">Student List:</h3>
                <ul className="list-disc list-inside">
                  {report.student_summary.student_list.map((student, index) => (
                    <li key={index} className="ml-4">{student}</li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        )}

        {report?.ai_analysis && (
          <>
            <Card className={reportStyles.card}>
              <CardContent className={reportStyles.cardContent}>
                <div className={reportStyles.sectionHeading}>
                  <PieChartIcon className={reportStyles.sectionIcon} />
                  <h2 className={reportStyles.sectionTitle}>Executive Summary</h2>
                </div>
                <div className={reportStyles.contentBox}>
                  <ul className={reportStyles.markdown} 
                      dangerouslySetInnerHTML={{ 
                        __html: processMarkdown(report.ai_analysis.executive_summary) 
                      }} 
                  />
                </div>
              </CardContent>
            </Card>

            <Card className={reportStyles.card}>
              <CardContent className={reportStyles.cardContent}>
                <div className={reportStyles.sectionHeading}>
                  <UsersIcon className={reportStyles.sectionIcon} />
                  <h2 className={reportStyles.sectionTitle}>Individual Student Analysis</h2>
                </div>
                <div className={reportStyles.contentBox}>
                  <ul className={reportStyles.markdown} 
                      dangerouslySetInnerHTML={{ 
                        __html: processMarkdown(report.ai_analysis.individual_student_analysis) 
                      }} 
                  />
                </div>
              </CardContent>
            </Card>

            <Card className={reportStyles.card}>
              <CardContent className={reportStyles.cardContent}>
                <div className={reportStyles.sectionHeading}>
                  <BarChartIcon className={reportStyles.sectionIcon} />
                  <h2 className={reportStyles.sectionTitle}>Temporal Analysis</h2>
                </div>
                <div className={reportStyles.contentBox}>
                  <ul className={reportStyles.markdown} 
                      dangerouslySetInnerHTML={{ 
                        __html: processMarkdown(report.ai_analysis.temporal_analysis) 
                      }} 
                  />
                </div>
              </CardContent>
            </Card>

            <Card className={reportStyles.card}>
              <CardContent className={reportStyles.cardContent}>
                <div className={reportStyles.sectionHeading}>
                  <UsersIcon className={reportStyles.sectionIcon} />
                  <h2 className={reportStyles.sectionTitle}>Classroom Dynamics</h2>
                </div>
                <div className={reportStyles.contentBox}>
                  <ul className={reportStyles.markdown} 
                      dangerouslySetInnerHTML={{ 
                        __html: processMarkdown(report.ai_analysis.classroom_dynamics) 
                      }} 
                  />
                </div>
              </CardContent>
            </Card>

            <Card className={reportStyles.card}>
              <CardContent className={reportStyles.cardContent}>
                <div className={reportStyles.sectionHeading}>
                  <LightbulbIcon className={reportStyles.sectionIcon} />
                  <h2 className={reportStyles.sectionTitle}>Actionable Recommendations</h2>
                </div>
                <div className={reportStyles.contentBox}>
                  <div className="whitespace-pre-wrap markdown" 
                      dangerouslySetInnerHTML={{ 
                        __html: processMarkdown(report.ai_analysis.actionable_recommendations) 
                      }} 
                  />
                </div>
              </CardContent>
            </Card>

            <Card className={reportStyles.card}>
              <CardContent className={reportStyles.cardContent}>
                <div className={reportStyles.sectionHeading}>
                  <BarChartIcon className={reportStyles.sectionIcon} />
                  <h2 className={reportStyles.sectionTitle}>Metrics Summary</h2>
                </div>
                <div className={reportStyles.contentBox}>
                  <ul className={reportStyles.markdown} 
                      dangerouslySetInnerHTML={{ 
                        __html: processMarkdown(report.ai_analysis.metrics_summary) 
                      }} 
                  />
                </div>
              </CardContent>
            </Card>
          </>
        )}

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

// Client components should not export static params or dynamic config
// Using the separate file generateMetadata.ts for server-side exports