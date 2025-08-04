"use client"

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useRouter } from 'next/navigation';
import { 
  UploadIcon, 
  FileVideoIcon, 
  CheckCircleIcon,
  AlertCircleIcon,
  BookOpenIcon,
  GlobeIcon
} from 'lucide-react';

export default function UploadPage() {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [reportId, setReportId] = useState<string>('');
  const [lessonName, setLessonName] = useState<string>('');
  const [language, setLanguage] = useState<string>('English');
  const router = useRouter();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      simulateUpload(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    },
    maxFiles: 1,
    maxSize: 500 * 1024 * 1024 // 500MB
  });

  const simulateUpload = async (file: File) => {
    setIsUploading(true);
    setUploadProgress(0);

    // Simulate upload progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 95) {
          clearInterval(progressInterval);
          return 95;
        }
        return prev + Math.random() * 15;
      });
    }, 200);

    // Simulate API call delay
    setTimeout(() => {
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      // Generate mock report ID
      const mockReportId = 'report_' + Math.random().toString(36).substr(2, 9);
      setReportId(mockReportId);
      setUploadComplete(true);
      setIsUploading(false);
    }, 3000);
  };

  const [isProcessing, setIsProcessing] = useState(false);
  const [processingError, setProcessingError] = useState<string | null>(null);
  
  const startProcessing = async () => {
    if (!uploadedFile) {
      console.error('No file uploaded');
      return;
    }
    
    if (!lessonName.trim()) {
      setProcessingError('Please enter a lesson name');
      return;
    }
    
    setIsProcessing(true);
    setProcessingError(null);
    
    try {
      // Create FormData to upload the file
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('lessonName', lessonName);
      formData.append('language', language);

      console.log("Starting upload and processing...");
      
      // Upload file and start processing
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed with status ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      console.log("Upload successful, received reportId:", result.reportId);
      
      const actualReportId = result.reportId;

      // Short delay to ensure backend has started processing
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Navigate to processing page with actual report ID
      console.log("Redirecting to processing page...");
      router.push(`/processing/${actualReportId}`);
    } catch (error: any) {
      console.error('Error uploading file:', error);
      setProcessingError(error?.message || 'Failed to upload file');
      setIsProcessing(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
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
            Upload Your Lesson Video
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Upload your virtual lesson recording to get detailed engagement analytics
          </p>
        </div>

        <AnimatePresence mode="wait">
          {!uploadComplete ? (
            <motion.div
              key="upload"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-xl">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <UploadIcon className="h-5 w-5" />
                    Video Upload
                  </CardTitle>
                  <CardDescription>
                    Supported formats: MP4, AVI, MOV, MKV, WebM (Max 500MB)
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {!isUploading ? (
                    <div {...getRootProps()}>
                      <motion.div
                        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
                          isDragActive
                            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                            : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
                        }`}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <input {...getInputProps()} />
                        <FileVideoIcon className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                        
                        {isDragActive ? (
                          <p className="text-blue-600 font-medium">Drop your video here!</p>
                        ) : (
                          <div>
                            <p className="text-lg font-medium mb-2">
                              Drag and drop your video here
                            </p>
                            <p className="text-gray-500 mb-4">or click to browse files</p>
                            <Button variant="outline">
                              Choose File
                            </Button>
                          </div>
                        )}
                      </motion.div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="flex items-center space-x-3">
                        <FileVideoIcon className="h-8 w-8 text-blue-500" />
                        <div className="flex-1">
                          <p className="font-medium">{uploadedFile?.name}</p>
                          <p className="text-sm text-gray-500">
                            {uploadedFile && formatFileSize(uploadedFile.size)}
                          </p>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Upload Progress</span>
                          <span>{Math.round(uploadProgress)}%</span>
                        </div>
                        <Progress value={uploadProgress} className="h-2" />
                      </div>
                      
                      <p className="text-sm text-gray-600 dark:text-gray-300">
                        {uploadProgress < 100 ? 'Uploading your video...' : 'Upload complete!'}
                      </p>
                    </div>
                  )}

                  {fileRejections.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md"
                    >
                      <div className="flex items-start space-x-2">
                        <AlertCircleIcon className="h-5 w-5 text-red-500 mt-0.5" />
                        <div>
                          <p className="text-sm font-medium text-red-800 dark:text-red-200">
                            Upload Error
                          </p>
                          {fileRejections.map(({ file, errors }) => (
                            <div key={file.name} className="mt-1">
                              <p className="text-sm text-red-600 dark:text-red-300">
                                {file.name}: {errors[0]?.message}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          ) : (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
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
                  
                  <h2 className="text-2xl font-bold mb-2">Upload Successful!</h2>
                  <p className="text-gray-600 dark:text-gray-300 mb-6">
                    Your video has been uploaded successfully.ll now analyze it to generate your engagement report.
                  </p>
                  
                  <div className="bg-white/60 dark:bg-gray-800/60 rounded-lg p-4 mb-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <FileVideoIcon className="h-6 w-6 text-blue-500" />
                        <div className="text-left">
                          <p className="font-medium">{uploadedFile?.name}</p>
                          <p className="text-sm text-gray-500">Report ID: {reportId}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-5 mb-6">
                    <div className="space-y-2">
                      <Label htmlFor="lessonName" className="flex items-center gap-2">
                        <BookOpenIcon className="h-4 w-4" />
                        Lesson Name
                      </Label>
                      <Input
                        id="lessonName"
                        placeholder="Enter lesson name"
                        value={lessonName}
                        onChange={(e) => setLessonName(e.target.value)}
                        className="bg-white/80 dark:bg-gray-800/80"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="language" className="flex items-center gap-2">
                        <GlobeIcon className="h-4 w-4" />
                        Content Language
                      </Label>
                      <Select value={language} onValueChange={setLanguage}>
                        <SelectTrigger id="language" className="bg-white/80 dark:bg-gray-800/80">
                          <SelectValue placeholder="Select language" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="English">English</SelectItem>
                          <SelectItem value="Turkish">Turkish</SelectItem>
                          <SelectItem value="Arabic">Arabic</SelectItem>
                          <SelectItem value="Spanish">Spanish</SelectItem>
                          <SelectItem value="French">French</SelectItem>
                          <SelectItem value="German">German</SelectItem>
                          <SelectItem value="Italian">Italian</SelectItem>
                          <SelectItem value="Portuguese">Portuguese</SelectItem>
                          <SelectItem value="Chinese">Chinese</SelectItem>
                          <SelectItem value="Japanese">Japanese</SelectItem>
                          <SelectItem value="Russian">Russian</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  
                  {processingError && (
                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-3 rounded-lg mb-4 text-left">
                      <p className="text-sm font-medium text-red-800 dark:text-red-200">
                        Error: {processingError}
                      </p>
                    </div>
                  )}
                  
                  <Button 
                    onClick={startProcessing}
                    disabled={isProcessing}
                    className={`relative ${
                      isProcessing 
                        ? "bg-gray-400" 
                        : "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    }`}
                  >
                    {isProcessing ? (
                      <>
                        <span className="animate-spin inline-block mr-2">◌</span>
                        Processing...
                      </>
                    ) : (
                      "Start Analysis"
                    )}
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}