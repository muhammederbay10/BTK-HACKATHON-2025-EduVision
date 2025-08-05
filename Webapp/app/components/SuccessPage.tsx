"use client"

import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircleIcon } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { config } from '@/app/lib/config';

interface SuccessPageProps {
  reportId: string;
  message: string;
}

export default function SuccessPage({ reportId, message = "Your analysis is complete!" }: SuccessPageProps) {
  const router = useRouter();
  
  return (
    <div className="container mx-auto px-4 py-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-2xl mx-auto"
      >
        <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 border-0 shadow-xl">
          <CardContent className="p-8 text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", duration: 0.6 }}
            >
              <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
            </motion.div>
            
            <h2 className="text-2xl font-bold mb-2">Success!</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">{message}</p>
            
            <div className="flex justify-center space-x-4">
              <Button 
                onClick={() => {
                  console.log("Navigating to report page:", reportId);
                  // First verify the report exists
                  fetch(`${config.apiUrl}/report/${reportId}`)
                    .then(res => {
                      if (res.ok) {
                        router.push(`/report/${reportId}`);
                      } else {
                        alert("Report is still being processed. Please wait a moment and try again.");
                      }
                    })
                    .catch(err => {
                      console.error("Error checking report:", err);
                      alert("Could not verify if report is ready. Please try again.");
                    });
                }}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                View Report
              </Button>
              
              <Button 
                onClick={() => router.push('/upload')}
                variant="outline"
              >
                Upload Another Video
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}