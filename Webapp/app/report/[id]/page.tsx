"use client"

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useParams } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { 
  TrendingUpIcon, 
  TrendingDownIcon, 
  UsersIcon, 
  ClockIcon,
  BrainIcon,
  PlayIcon,
  PauseIcon,
  AlertTriangleIcon,
  CheckCircleIcon,
  LightbulbIcon
} from 'lucide-react';

interface ReportData {
  id: string;
  filename: string;
  upload_time: string;
  duration: string;
  total_students: number;
  average_attention: number;
  engagement_trends: Array<{
    timestamp: string;
    score: number;
    students_engaged: number;
  }>;
  high_engagement: {
    timestamp: string;
    summary: string;
    score: number;
    duration: string;
  };
  low_engagement: {
    timestamp: string;
    summary: string;
    score: number;
    duration: string;
  };
  insights: {
    most_engaging_topics: string[];
    least_engaging_topics: string[];
    recommendations: string[];
  };
  llm_feedback: string;
}

export default function ReportPage() {
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const params = useParams();
  const reportId = params.id as string;

  useEffect(() => {
    // Load mock report data
    const mockData: ReportData = {
      id: reportId,
      filename: `lesson_video_${reportId.slice(0, 8)}.mp4`,
      upload_time: new Date().toISOString(),
      duration: "15:30",
      total_students: 24,
      average_attention: 0.73,
      engagement_trends: [
        { timestamp: "00:01:00", score: 0.78, students_engaged: 19 },
        { timestamp: "00:02:00", score: 0.63, students_engaged: 15 },
        { timestamp: "00:03:00", score: 0.82, students_engaged: 20 },
        { timestamp: "00:04:00", score: 0.71, students_engaged: 17 },
        { timestamp: "00:05:00", score: 0.89, students_engaged: 21 },
        { timestamp: "00:06:00", score: 0.67, students_engaged: 16 },
        { timestamp: "00:07:00", score: 0.45, students_engaged: 11 },
        { timestamp: "00:08:00", score: 0.39, students_engaged: 9 },
        { timestamp: "00:09:00", score: 0.56, students_engaged: 13 },
        { timestamp: "00:10:00", score: 0.74, students_engaged: 18 },
        { timestamp: "00:11:00", score: 0.81, students_engaged: 19 },
        { timestamp: "00:12:00", score: 0.69, students_engaged: 17 },
        { timestamp: "00:13:00", score: 0.42, students_engaged: 10 },
        { timestamp: "00:14:00", score: 0.21, students_engaged: 5 },
        { timestamp: "00:15:00", score: 0.65, students_engaged: 16 }
      ],
      high_engagement: {
        timestamp: "00:05:00",
        summary: "Teacher demonstrated interactive problem-solving with student participation",
        score: 0.89,
        duration: "2:15"
      },
      low_engagement: {
        timestamp: "00:14:00",
        summary: "Teacher was reading definitions from slides with minimal interaction",
        score: 0.21,
        duration: "1:45"
      },
      insights: {
        most_engaging_topics: [
          "Interactive problem solving",
          "Q&A sessions", 
          "Visual demonstrations"
        ],
        least_engaging_topics: [
          "Theory reading",
          "Definition explanations",
          "Administrative announcements"
        ],
        recommendations: [
          "Incorporate more interactive elements during theory sections",
          "Use visual aids and examples when introducing new concepts",
          "Break up long explanations with student questions",
          "Consider shorter segments for complex topics"
        ]
      },
      llm_feedback: "Your lesson shows strong peaks during interactive moments. Consider breaking up theory-heavy sections with more frequent student engagement opportunities. The problem-solving segment at 5:00 was particularly effective - similar interactive approaches could boost attention during lower-engagement periods."
    };

    setReportData(mockData);
  }, [reportId]);

  const chartData = reportData?.engagement_trends.map((item, index) => ({
    time: index + 1,
    attention: Math.round(item.score * 100),
    students: item.students_engaged,
    timestamp: item.timestamp
  })) || [];

  const formatScore = (score: number) => Math.round(score * 100);

  if (!reportData) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="flex items-center justify-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          >
            <BrainIcon className="h-8 w-8 text-blue-500" />
          </motion.div>
          <span className="ml-2">Loading report...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Engagement Report
          </h1>
          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 dark:text-gray-300">
            <span className="flex items-center gap-1">
              <ClockIcon className="h-4 w-4" />
              {reportData.filename}
            </span>
            <span>Duration: {reportData.duration}</span>
            <span className="flex items-center gap-1">
              <UsersIcon className="h-4 w-4" />
              {reportData.total_students} students
            </span>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Average Attention</p>
                  <p className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                    {formatScore(reportData.average_attention)}%
                  </p>
                </div>
                <BrainIcon className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-green-600 dark:text-green-400">Peak Engagement</p>
                  <p className="text-2xl font-bold text-green-700 dark:text-green-300">
                    {formatScore(reportData.high_engagement.score)}%
                  </p>
                </div>
                <TrendingUpIcon className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-red-600 dark:text-red-400">Lowest Point</p>
                  <p className="text-2xl font-bold text-red-700 dark:text-red-300">
                    {formatScore(reportData.low_engagement.score)}%
                  </p>
                </div>
                <TrendingDownIcon className="h-8 w-8 text-red-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-purple-600 dark:text-purple-400">Total Students</p>
                  <p className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                    {reportData.total_students}
                  </p>
                </div>
                <UsersIcon className="h-8 w-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="timeline">Timeline</TabsTrigger>
            <TabsTrigger value="insights">Insights</TabsTrigger>
            <TabsTrigger value="feedback">Feedback</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Attention Chart */}
            <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-lg">
              <CardHeader>
                <CardTitle>Attention Over Time</CardTitle>
                <CardDescription>Student engagement levels throughout the lesson</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                      <defs>
                        <linearGradient id="attentionGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="time" 
                        label={{ value: 'Time (minutes)', position: 'insideBottom', offset: -5 }}
                      />
                      <YAxis 
                        label={{ value: 'Attention %', angle: -90, position: 'insideLeft' }}
                      />
                      <Tooltip 
                        formatter={(value: number, name: string) => [
                          `${value}${name === 'attention' ? '%' : ' students'}`,
                          name === 'attention' ? 'Attention' : 'Engaged Students'
                        ]}
                        labelFormatter={(label) => `Minute ${label}`}
                      />
                      <Area
                        type="monotone"
                        dataKey="attention"
                        stroke="#3B82F6"
                        strokeWidth={2}
                        fill="url(#attentionGradient)"
                      />
                      <Line
                        type="monotone"
                        dataKey="students"
                        stroke="#10B981"
                        strokeWidth={2}
                        dot={{ fill: '#10B981', strokeWidth: 2, r: 4 }}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Key Moments */}
            <div className="grid md:grid-cols-2 gap-6">
              <Card className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-green-700 dark:text-green-300">
                    <CheckCircleIcon className="h-5 w-5" />
                    Most Engaging Moment
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100">
                        {reportData.high_engagement.timestamp}
                      </Badge>
                      <span className="text-2xl font-bold text-green-600">
                        {formatScore(reportData.high_engagement.score)}%
                      </span>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300">
                      {reportData.high_engagement.summary}
                    </p>
                    <p className="text-sm text-gray-500">
                      Duration: {reportData.high_engagement.duration}
                    </p>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-red-700 dark:text-red-300">
                    <AlertTriangleIcon className="h-5 w-5" />
                    Needs Attention
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Badge variant="secondary" className="bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100">
                        {reportData.low_engagement.timestamp}
                      </Badge>
                      <span className="text-2xl font-bold text-red-600">
                        {formatScore(reportData.low_engagement.score)}%
                      </span>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300">
                      {reportData.low_engagement.summary}
                    </p>
                    <p className="text-sm text-gray-500">
                      Duration: {reportData.low_engagement.duration}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="timeline" className="space-y-6">
            <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-lg">
              <CardHeader>
                <CardTitle>Video Timeline</CardTitle>
                <CardDescription>Interactive timeline showing engagement levels</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {/* Mock Video Player */}
                  <div className="aspect-video bg-gray-900 rounded-lg flex items-center justify-center">
                    <div className="text-center">
                      <PlayIcon className="h-16 w-16 text-white mb-4 mx-auto" />
                      <p className="text-white">Video Preview</p>
                      <p className="text-gray-400 text-sm">
                        {reportData.filename}
                      </p>
                    </div>
                  </div>

                  {/* Timeline Controls */}
                  <div className="space-y-2">
                    <Progress value={65} className="h-2" />
                    <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-300">
                      <span>8:30</span>
                      <div className="flex items-center gap-2">
                        <Button variant="ghost" size="sm">
                          {isPlaying ? <PauseIcon className="h-4 w-4" /> : <PlayIcon className="h-4 w-4" />}
                        </Button>
                      </div>
                      <span>{reportData.duration}</span>
                    </div>
                  </div>

                  {/* Engagement Markers */}
                  <div className="space-y-3">
                    <h4 className="font-semibold">Key Moments</h4>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                          <span className="font-medium">{reportData.high_engagement.timestamp}</span>
                          <Badge className="bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100">
                            High Engagement
                          </Badge>
                        </div>
                        <span className="text-green-600 font-bold">
                          {formatScore(reportData.high_engagement.score)}%
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                          <span className="font-medium">{reportData.low_engagement.timestamp}</span>
                          <Badge className="bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100">
                            Low Engagement
                          </Badge>
                        </div>
                        <span className="text-red-600 font-bold">
                          {formatScore(reportData.low_engagement.score)}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="insights" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <Card className="bg-gradient-to-br from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-green-700 dark:text-green-300">
                    <TrendingUpIcon className="h-5 w-5" />
                    Most Engaging Topics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {reportData.insights.most_engaging_topics.map((topic, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <CheckCircleIcon className="h-4 w-4 text-green-500" />
                        <span>{topic}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-red-700 dark:text-red-300">
                    <TrendingDownIcon className="h-5 w-5" />
                    Areas for Improvement
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {reportData.insights.least_engaging_topics.map((topic, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <AlertTriangleIcon className="h-4 w-4 text-red-500" />
                        <span>{topic}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>

            <Card className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <LightbulbIcon className="h-5 w-5 text-yellow-500" />
                  Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {reportData.insights.recommendations.map((rec, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center text-sm font-bold text-blue-600 dark:text-blue-300 mt-0.5">
                        {index + 1}
                      </div>
                      <span className="text-gray-700 dark:text-gray-300">{rec}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="feedback" className="space-y-6">
            <Card className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BrainIcon className="h-5 w-5 text-purple-500" />
                  AI-Generated Feedback
                </CardTitle>
                <CardDescription>
                  Personalized insights and suggestions for your teaching approach
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="prose dark:prose-invert max-w-none">
                  <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                    {reportData.llm_feedback}
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/60 backdrop-blur-sm dark:bg-gray-800/60 border-0 shadow-lg">
              <CardHeader>
                <CardTitle>Next Steps</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-3 gap-4">
                  <Button className="h-auto p-4 flex flex-col items-center space-y-2">
                    <UploadIcon className="h-6 w-6" />
                    <span>Upload Another Video</span>
                  </Button>
                  
                  <Button variant="outline" className="h-auto p-4 flex flex-col items-center space-y-2">
                    <TrendingUpIcon className="h-6 w-6" />
                    <span>Compare Reports</span>
                  </Button>
                  
                  <Button variant="outline" className="h-auto p-4 flex flex-col items-center space-y-2">
                    <BrainIcon className="h-6 w-6" />
                    <span>Get More Insights</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </motion.div>
    </div>
  );
}