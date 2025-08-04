"use client";

import { useRouter } from 'next/navigation';
import { useEffect, useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Loader2Icon, AlertCircleIcon, CheckCircleIcon, WifiOffIcon } from 'lucide-react';
import { isReportComplete, pollUntilComplete } from '@/app/utils/reportStatus';

interface Props {
  reportId: string;
}

export default function ProcessingPage({ reportId }: Props) {
  const [status, setStatus] = useState<'pending' | 'processing' | 'completed' | 'error'>('pending');
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [pollAttempts, setPollAttempts] = useState(0);
  const [connectionIssue, setConnectionIssue] = useState(false);
  const [estimatedTimeRemaining, setEstimatedTimeRemaining] = useState<number | null>(null);
  const router = useRouter();

  // Function to check if report exists directly
  const checkReportExists = useCallback(async () => {
    try {
      setConnectionIssue(false);
      console.log("Checking if report exists directly for:", reportId);
      const isComplete = await isReportComplete(reportId);
      
      if (isComplete) {
        console.log("Report exists! Setting status to completed");
        setStatus('completed');
        setProgress(100);
        return true;
      }
    } catch (err) {
      console.log("Error checking report existence:", err);
      setConnectionIssue(true);
    }
    return false;
  }, [reportId]);

  // Handle navigation to report when complete
  const viewReport = useCallback(() => {
    router.push(`/report/${reportId}`);
  }, [router, reportId]);

  useEffect(() => {
    // Don't try to fetch during static build/export
    if (reportId === 'placeholder') {
      return;
    }
    
    console.log("Starting processing for reportId:", reportId);
    setStatus('processing');
    
    // Initialize the estimated time based on typical processing duration
    setEstimatedTimeRemaining(60); // Assume 60 seconds initially
    
    // Use our utility to poll until the report is ready - THIS HANDLES ALL POLLING
    const cancelPolling = pollUntilComplete(reportId, () => {
      console.log("Report is complete (from utility)");
      setStatus('completed');
      setProgress(100);
      setEstimatedTimeRemaining(0);
    }, 60, 6000); // Polling every 6 seconds
    
    // Update estimated time remaining
    const timeRemainingInterval = setInterval(() => {
      if (status !== 'completed' && estimatedTimeRemaining !== null && estimatedTimeRemaining > 0) {
        setEstimatedTimeRemaining(prev => {
          if (prev === null) return null;
          return Math.max(0, prev - 1);
        });
        
        // Keep track of polling attempts for UI feedback only
        setPollAttempts(prev => prev + 1);
      }
    }, 1000);
    
    // Simulate progress even when waiting for backend
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        // Don't go to 100% until we know processing is complete
        if (status === 'completed') return 100;
        if (prev >= 95) return 95;
        
        // After many polling attempts, speed up the progress
        if (pollAttempts > 10) {
          return prev + Math.random() * 5; // Move faster
          
          // Also reduce the estimated time more aggressively
          setEstimatedTimeRemaining(prevTime => {
            if (prevTime === null) return null;
            return Math.max(0, prevTime - 2);
          });
        }
        return prev + Math.random() * 2;
      });
    }, 1000);

    return () => {
      clearInterval(progressInterval);
      clearInterval(timeRemainingInterval);
      cancelPolling();
    };
  }, [reportId, status, pollAttempts, estimatedTimeRemaining]);

  const getStatusText = () => {
    switch (status) {
      case 'pending':
        return 'Preparing to process your video...';
      case 'processing':
        return connectionIssue 
          ? 'Connecting to processing server...' 
          : 'Analyzing your video for engagement metrics...';
      case 'completed':
        return 'Processing complete!';
      case 'error':
        return 'There was a problem processing your video.';
      default:
        return 'Processing your video...';
    }
  };

  const getStepProgress = () => {
    const steps = [
      { name: "Initializing", complete: progress > 10 },
      { name: "Reading video frames", complete: progress > 35 },
      { name: "Analyzing engagement metrics", complete: progress > 65 },
      { name: "Generating report", complete: progress > 85 },
      { name: "Finishing up", complete: progress >= 100 }
    ];
    
    return steps.map((step, index) => (
      <div key={index} className="flex items-center gap-2">
        {step.complete ? 
          <CheckCircleIcon className="h-4 w-4 text-green-500" /> : 
          <div className="h-4 w-4 rounded-full border border-gray-300"></div>
        }
        <span className={`text-sm ${step.complete ? 'text-green-600 dark:text-green-400' : 'text-gray-500'}`}>
          {step.name}
        </span>
      </div>
    ));
  };

  const getTimeRemainingText = () => {
    if (!estimatedTimeRemaining || estimatedTimeRemaining <= 0) {
      return "Finishing up...";
    }
    
    if (estimatedTimeRemaining > 60) {
      const mins = Math.floor(estimatedTimeRemaining / 60);
      return `Est. ${mins} minute${mins > 1 ? 's' : ''} remaining`;
    }
    
    return `Est. ${Math.ceil(estimatedTimeRemaining)} seconds remaining`;
  };

  return (
    <div className="container mx-auto px-4 py-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-2xl mx-auto"
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Processing Your Video
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Please wait while we analyze your video for engagement metrics
          </p>
        </div>

        <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-xl">
          <CardContent className="pt-6">
            {error ? (
              <div className="text-center py-8">
                <AlertCircleIcon className="h-16 w-16 text-red-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold mb-2">Processing Failed</h2>
                <p className="text-gray-600 dark:text-gray-300 mb-6">{error}</p>
                <div className="flex justify-center gap-4">
                  <Button 
                    onClick={() => {
                      setError(null);
                      setProgress(0);
                      setStatus('pending');
                      setPollAttempts(0);
                    }}
                    variant="outline"
                  >
                    Try Again
                  </Button>
                  <Button 
                    onClick={() => router.push('/upload')}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                  >
                    Upload New Video
                  </Button>
                </div>
              </div>
            ) : status === 'completed' ? (
              <div className="text-center py-8">
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
                </motion.div>
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.3, duration: 0.5 }}
                >
                  <h2 className="text-2xl font-bold mb-2">Processing Complete!</h2>
                  <p className="text-gray-600 dark:text-gray-300 mb-6">
                    Your engagement analysis report is ready to view
                  </p>
                  <Progress value={100} className="h-2 mb-4" />
                  <Button
                    onClick={viewReport}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    size="lg"
                  >
                    View Engagement Report
                  </Button>
                </motion.div>
              </div>
            ) : (
              <div className="py-8">
                <div className="flex justify-center mb-8">
                  <div className="relative">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-xl font-bold">{Math.round(progress)}%</span>
                    </div>
                    <Loader2Icon className="h-24 w-24 text-blue-500 animate-spin opacity-25" />
                  </div>
                </div>
                
                <h2 className="text-xl font-medium text-center mb-6">{getStatusText()}</h2>
                
                <div className="space-y-4">
                  <Progress value={progress} className="h-2" />
                  
                  {connectionIssue && (
                    <div className="flex items-center justify-center gap-2 text-amber-500 text-sm mt-2 mb-4">
                      <WifiOffIcon size={16} />
                      <span>Connection issues detected. Retrying...</span>
                    </div>
                  )}
                  
                  {/* Processing steps indicator */}
                  <div className="space-y-2 my-6 max-w-sm mx-auto">
                    {getStepProgress()}
                  </div>
                  
                  <div className="flex justify-between text-sm text-gray-500">
                    <span>Report ID: {reportId}</span>
                    <span>{getTimeRemainingText()}</span>
                  </div>
                  
                  {progress > 40 && (
                    <div className="text-center mt-6">
                      <p className="text-sm text-gray-500 mb-2">
                        Taking longer than expected?
                      </p>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          console.log("Manual check for report");
                          checkReportExists();
                        }}
                      >
                        Check If Report Is Ready
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
