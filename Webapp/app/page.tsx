"use client"

import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useLanguage } from '@/lib/language-context';
import Link from 'next/link';
import { 
  UploadIcon, 
  BarChart3Icon, 
  BrainIcon, 
  VideoIcon,
  TrendingUpIcon,
  UsersIcon
} from 'lucide-react';

export default function Home() {
  const { t } = useLanguage();
  
  const features = [
    {
      icon: VideoIcon,
      title: t('home.features.videoAnalysis.title'),
      description: t('home.features.videoAnalysis.description')
    },
    {
      icon: BrainIcon,
      title: t('home.features.aiInsights.title'),
      description: t('home.features.aiInsights.description')
    },
    {
      icon: TrendingUpIcon,
      title: t('home.features.performanceMetrics.title'),
      description: t('home.features.performanceMetrics.description')
    },
    {
      icon: UsersIcon,
      title: t('home.features.studentAnalytics.title'),
      description: t('home.features.studentAnalytics.description')
    }
  ];

  return (
    <div className="container mx-auto px-4 py-16">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center mb-16"
      >
        <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
          {t('home.title')}
        </h1>
        <p className="text-xl text-gray-800 dark:text-gray-200 mb-8 max-w-3xl mx-auto">
          {t('home.subtitle')}
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/upload">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white">
                <UploadIcon className="mr-2 h-5 w-5" />
                {t('home.uploadButton')}
              </Button>
            </motion.div>
          </Link>
          
          <Link href="/history">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button variant="outline" size="lg" className="border-blue-600 text-blue-600 hover:bg-blue-50">
                <BarChart3Icon className="mr-2 h-5 w-5" />
                {t('home.sampleReportsButton')}
              </Button>
            </motion.div>
          </Link>
        </div>
      </motion.div>

      {/* Features Grid */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0.3 }}
        className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16"
      >
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 * index }}
              whileHover={{ y: -5, scale: 1.02 }}
            >
              <Card className="h-full bg-white/60 backdrop-blur-sm dark:bg-gray-900/60 border-blue-100 dark:border-blue-800 shadow-lg">
                <CardHeader className="text-center">
                  <div className="mx-auto w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mb-4">
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-center">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Demo Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
        className="text-center"
      >
        <Card className="max-w-4xl mx-auto bg-gradient-to-r from-blue-50 to-white dark:from-gray-800 dark:to-gray-900 border-0 shadow-xl">
          <CardHeader>
            <CardTitle className="text-2xl">{t('home.demo.title')}</CardTitle>
            <CardDescription className="text-lg">
              {t('home.demo.subtitle')}
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                  1
                </div>
                <div>
                  <h3 className="font-semibold mb-1">{t('home.demo.step1.title')}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {t('home.demo.step1.description')}
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                  2
                </div>
                <div>
                  <h3 className="font-semibold mb-1">{t('home.demo.step2.title')}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {t('home.demo.step2.description')}
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-700 rounded-full flex items-center justify-center text-white font-bold text-sm">
                  3
                </div>
                <div>
                  <h3 className="font-semibold mb-1">{t('home.demo.step3.title')}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {t('home.demo.step3.description')}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}