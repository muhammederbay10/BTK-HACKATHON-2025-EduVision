"use client"

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { 
  HistoryIcon, 
  SearchIcon, 
  EyeIcon, 
  CalendarIcon,
  ClockIcon,
  TrendingUpIcon,
  BarChart3Icon,
  VideoIcon
} from 'lucide-react';

interface Report {
  id: string;
  filename: string;
  upload_time: string;
  average_attention: number;
  duration: string;
  status: string;
}

export default function HistoryPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load mock reports
    const mockReports: Report[] = [
      {
        id: 'demo-1',
        filename: 'math_lesson_intro.mp4',
        upload_time: '2024-01-15T10:30:00',
        average_attention: 0.76,
        duration: '12:45',
        status: 'completed'
      },
      {
        id: 'demo-2', 
        filename: 'physics_experiment.mp4',
        upload_time: '2024-01-14T14:20:00',
        average_attention: 0.82,
        duration: '18:20',
        status: 'completed'
      },
      {
        id: 'demo-3',
        filename: 'history_discussion.mp4',
        upload_time: '2024-01-12T09:15:00',
        average_attention: 0.68,
        duration: '25:10',
        status: 'completed'
      },
      {
        id: 'demo-4',
        filename: 'chemistry_lab_demo.mp4',
        upload_time: '2024-01-10T11:45:00',
        average_attention: 0.79,
        duration: '22:30',
        status: 'completed'
      },
      {
        id: 'demo-5',
        filename: 'english_literature.mp4',
        upload_time: '2024-01-08T16:10:00',
        average_attention: 0.63,
        duration: '28:15',
        status: 'completed'
      }
    ];

    setTimeout(() => {
      setReports(mockReports);
      setLoading(false);
    }, 500);
  }, []);

  const filteredReports = reports.filter(report =>
    report.filename.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatScore = (score: number) => Math.round(score * 100);

  const getScoreColor = (score: number) => {
    const percentage = score * 100;
    if (percentage >= 80) return 'text-green-600 dark:text-green-400';
    if (percentage >= 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreBadgeColor = (score: number) => {
    const percentage = score * 100;
    if (percentage >= 80) return 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100';
    if (percentage >= 60) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100';
    return 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100';
  };

  return (
    <div className="container mx-auto px-4 py-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent flex items-center gap-3">
            <HistoryIcon className="h-8 w-8 text-blue-600" />
            Report History
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            View and analyze your past lesson engagement reports
          </p>

          {/* Search */}
          <div className="relative max-w-md">
            <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search reports..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Total Reports</p>
                  <p className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                    {reports.length}
                  </p>
                </div>
                <BarChart3Icon className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-green-600 dark:text-green-400">Avg Engagement</p>
                  <p className="text-2xl font-bold text-green-700 dark:text-green-300">
                    {reports.length > 0 ? Math.round((reports.reduce((sum, r) => sum + r.average_attention, 0) / reports.length) * 100) : 0}%
                  </p>
                </div>
                <TrendingUpIcon className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-purple-600 dark:text-purple-400">Best Score</p>
                  <p className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                    {reports.length > 0 ? formatScore(Math.max(...reports.map(r => r.average_attention))) : 0}%
                  </p>
                </div>
                <TrendingUpIcon className="h-8 w-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-orange-600 dark:text-orange-400">Total Duration</p>
                  <p className="text-2xl font-bold text-orange-700 dark:text-orange-300">
                    {reports.reduce((total, report) => {
                      const [minutes, seconds] = report.duration.split(':').map(Number);
                      return total + minutes + (seconds / 60);
                    }, 0).toFixed(0)}m
                  </p>
                </div>
                <ClockIcon className="h-8 w-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Reports List */}
        {loading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <Card key={i} className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-lg">
                <CardContent className="p-6">
                  <div className="animate-pulse">
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-2"></div>
                    <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4"></div>
                    <div className="flex space-x-4">
                      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
                      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
                      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="space-y-4">
            {filteredReports.length > 0 ? (
              filteredReports.map((report, index) => (
                <motion.div
                  key={report.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  whileHover={{ y: -2, scale: 1.01 }}
                >
                  <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-lg hover:shadow-xl transition-all">
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                            <VideoIcon className="h-6 w-6 text-white" />
                          </div>
                          
                          <div>
                            <h3 className="font-semibold text-lg mb-1">{report.filename}</h3>
                            <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-300">
                              <span className="flex items-center gap-1">
                                <CalendarIcon className="h-4 w-4" />
                                {formatDate(report.upload_time)}
                              </span>
                              <span className="flex items-center gap-1">
                                <ClockIcon className="h-4 w-4" />
                                {report.duration}
                              </span>
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center space-x-4">
                          <div className="text-right">
                            <p className="text-sm text-gray-600 dark:text-gray-300 mb-1">
                              Engagement Score
                            </p>
                            <Badge className={getScoreBadgeColor(report.average_attention)}>
                              {formatScore(report.average_attention)}%
                            </Badge>
                          </div>

                          <Link href={`/report/${report.id}`}>
                            <motion.div
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                            >
                              <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                                <EyeIcon className="h-4 w-4 mr-2" />
                                View Report
                              </Button>
                            </motion.div>
                          </Link>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))
            ) : (
              <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-lg">
                <CardContent className="p-12 text-center">
                  <HistoryIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold mb-2">No Reports Found</h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-6">
                    {searchTerm ? 'No reports match your search.' : 'You haven\'t uploaded any videos yet.'}
                  </p>
                  <Link href="/upload">
                    <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                      Upload Your First Video
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Call to Action */}
        {filteredReports.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="mt-12 text-center"
          >
            <Card className="max-w-2xl mx-auto bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-800 dark:to-purple-900 border-0 shadow-xl">
              <CardContent className="p-8">
                <h3 className="text-2xl font-bold mb-4">Ready for More Insights?</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Upload another lesson video to continue improving your teaching effectiveness.
                </p>
                <Link href="/upload">
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Button size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                      Upload New Video
                    </Button>
                  </motion.div>
                </Link>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}