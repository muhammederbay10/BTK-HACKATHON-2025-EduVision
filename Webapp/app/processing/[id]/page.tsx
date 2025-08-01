"use client"

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter, useParams } from 'next/navigation';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { 
  BrainIcon, 
  EyeIcon, 
  MessageSquareIcon,
  CheckCircleIcon,
  LoaderIcon
} from 'lucide-react';

interface ProcessingStage {
  id: string;
  title: string;
  description: string;
  icon: React.ComponentType<any>;
  progress: number;
}

export default function ProcessingPage() {
  const [currentStage, setCurrentStage] = useState(0);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const router = useRouter();
  const params = useParams();
  const reportId = params.id as string;

  const stages: ProcessingStage[] = [
    {
      id: 'analyzing_faces',
      title: 'Analyzing Faces',
      description: 'Detecting and tracking student faces in the video...',
      icon: EyeIcon,
      progress: 25
    },
    {
      id: 'extracting_attention',
      title: 'Extracting Attention',
      description: 'Measuring engagement levels and attention patterns...',
      icon: BrainIcon,
      progress: 65
    },
    {
      id: 'generating_feedback',
      title: 'Generating Insights',
      description: 'Creating personalized feedback and recommendations...',
      icon: MessageSquareIcon,
      progress: 90
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress(prev => {
        const nextProgress = prev + 1;
        
        // Update current stage based on progress
        if (nextProgress <= 30) {
          setCurrentStage(0);
        } else if (nextProgress <= 70) {
          setCurrentStage(1);
        } else if (nextProgress <= 95) {
          setCurrentStage(2);
        } else {
          setIsComplete(true);
          clearInterval(timer);
        }
        
        return nextProgress;
      });
    }, 150);

    return () => clearInterval(timer);
  }, []);

  const viewReport = () => {
    router.push(`/report/${reportId}`);
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
            Analyzing Your Video
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Please wait while we process your lesson and generate insights
          </p>
        </div>

        <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-xl">
          <CardContent className="p-8">
            {!isComplete ? (
              <div className="space-y-8">
                {/* Overall Progress */}
                <div className="space-y-3">
                  <div className="flex justify-between text-sm font-medium">
                    <span>Overall Progress</span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-3" />
                </div>

                {/* Processing Stages */}
                <div className="space-y-6">
                  {stages.map((stage, index) => {
                    const Icon = stage.icon;
                    const isActive = index === currentStage;
                    const isCompleted = index < currentStage;
                    
                    return (
                      <motion.div
                        key={stage.id}
                        initial={{ opacity: 0.5, scale: 0.95 }}
                        animate={{ 
                          opacity: isActive ? 1 : isCompleted ? 0.8 : 0.5,
                          scale: isActive ? 1 : 0.95
                        }}
                        transition={{ duration: 0.3 }}
                        className={`flex items-center space-x-4 p-4 rounded-lg ${
                          isActive 
                            ? 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800' 
                            : isCompleted
                            ? 'bg-green-50 dark:bg-green-900/20'
                            : 'bg-gray-50 dark:bg-gray-800'
                        }`}
                      >
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                          isActive 
                            ? 'bg-blue-500 text-white' 
                            : isCompleted
                            ? 'bg-green-500 text-white'
                            : 'bg-gray-300 dark:bg-gray-600 text-gray-600 dark:text-gray-300'
                        }`}>
                          {isCompleted ? (
                            <CheckCircleIcon className="h-6 w-6" />
                          ) : isActive ? (
                            <motion.div
                              animate={{ rotate: 360 }}
                              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                            >
                              <LoaderIcon className="h-6 w-6" />
                            </motion.div>
                          ) : (
                            <Icon className="h-6 w-6" />
                          )}
                        </div>
                        
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg">{stage.title}</h3>
                          <p className={`text-sm ${
                            isActive ? 'text-blue-600 dark:text-blue-400' : 'text-gray-600 dark:text-gray-300'
                          }`}>
                            {stage.description}
                          </p>
                        </div>
                        
                        {isActive && (
                          <motion.div
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{ duration: 2, repeat: Infinity }}
                            className="w-3 h-3 bg-blue-500 rounded-full"
                          />
                        )}
                      </motion.div>
                    );
                  })}
                </div>

                <div className="text-center">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    This process typically takes 20-30 seconds
                  </p>
                </div>
              </div>
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="text-center space-y-6"
              >
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", duration: 0.6 }}
                >
                  <CheckCircleIcon className="h-20 w-20 text-green-500 mx-auto" />
                </motion.div>
                
                <div>
                  <h2 className="text-2xl font-bold mb-2">Analysis Complete!</h2>
                  <p className="text-gray-600 dark:text-gray-300 mb-6">
                    Your engagement report is ready. Click below to view detailed insights about your lesson.
                  </p>
                </div>
                
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Button 
                    onClick={viewReport}
                    size="lg"
                    className="bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700"
                  >
                    View Report
                  </Button>
                </motion.div>
              </motion.div>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}