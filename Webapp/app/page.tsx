/* eslint-disable @next/next/no-img-element */
"use client"

import { motion } from 'framer-motion';
import React, { useRef, useEffect, useState } from 'react';
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
  UsersIcon,
  CheckCircleIcon,
  PlayCircleIcon,
  StarIcon,
  ShieldCheckIcon,
  ClockIcon,
  ZapIcon,
  GraduationCapIcon,
  BookOpenIcon,
  MonitorIcon,
  HeadphonesIcon,
  ArrowRightIcon,
  EyeIcon,
  ActivityIcon,
  PieChartIcon,
  BarChart2Icon,
  TrendingDownIcon
} from 'lucide-react';

export default function Home() {
  const { t } = useLanguage();
  const [activeTestimonial, setActiveTestimonial] = useState(0);
  
  // Sample images for the attention model demo
  const demoImages = [
    {
      src: "/images/attentive.jpeg",
      alt: "Student attention heatmap showing focus patterns",
      caption: "Real-time attention tracking"
    },
    {
      src: "/images/distracted.jpeg",
      alt: "Classroom overview with multiple students",
      caption: "Multi-student analysis"
    },
    {
      src: "/images/moderate.jpeg",
      alt: "Engagement metrics and charts",
      caption: "Detailed engagement reports"
    },
    {
      src: "/images/processing.jpeg",
      alt: "Timeline showing attention patterns over class duration",
      caption: "Attention timeline analysis"
    }
  ];
  
  const features = [
    {
      icon: VideoIcon,
      title: t('home.features.videoAnalysis.title') || 'Video Analysis',
      description: t('home.features.videoAnalysis.description') || 'Advanced video processing and analysis'
    },
    {
      icon: BrainIcon,
      title: t('home.features.aiInsights.title') || 'AI Insights',
      description: t('home.features.aiInsights.description') || 'Intelligent insights powered by AI'
    },
    {
      icon: TrendingUpIcon,
      title: t('home.features.performanceMetrics.title') || 'Performance Metrics',
      description: t('home.features.performanceMetrics.description') || 'Comprehensive performance tracking'
    },
    {
      icon: UsersIcon,
      title: t('home.features.studentAnalytics.title') || 'Student Analytics',
      description: t('home.features.studentAnalytics.description') || 'Deep student behavior analysis'
    }
  ];

  // Enhanced features with more detail
  const enhancedFeatures = [
    {
      icon: EyeIcon,
      title: "Advanced Gaze Tracking",
      description: "AI-powered eye movement analysis to understand where students focus during lessons",
      color: "bg-blue-500"
    },
    {
      icon: ActivityIcon,
      title: "Engagement Patterns",
      description: "Identify peak attention periods and optimize content delivery timing",
      color: "bg-green-500"
    },
    {
      icon: PieChartIcon,
      title: "Distraction Analysis",
      description: "Detect and categorize different types of student distractions in real-time",
      color: "bg-purple-500"
    },
    {
      icon: BarChart2Icon,
      title: "Learning Effectiveness",
      description: "Measure comprehension levels through attention and engagement metrics",
      color: "bg-orange-500"
    },
    {
      icon: TrendingDownIcon,
      title: "Fatigue Detection",
      description: "Monitor student energy levels and suggest optimal break times",
      color: "bg-red-500"
    },
    {
      icon: ZapIcon,
      title: "Real-time Alerts (Comming Soon)",
      description: "Instant notifications when students need additional support or attention",
      color: "bg-yellow-500"
    }
  ];

  // Testimonials
  const testimonials = [
    {
      name: "Dr. Sarah Johnson",
      role: "Professor of Education, Stanford University",
      content: "This platform has revolutionized how I understand student engagement in my online courses. The insights are invaluable.",
      rating: 5
    },
    {
      name: "Michael Chen",
      role: "K-12 Teacher, Lincoln Elementary",
      content: "I can now identify which students need extra help before they fall behind. It's like having x-ray vision for attention.",
      rating: 5
    },
    {
      name: "Prof. Maria Rodriguez",
      role: "Online Course Creator",
      content: "The analytics help me optimize my content in real-time. Student completion rates have increased by 40%.",
      rating: 5
    }
  ];

  // Ref for the scrolling container
  const scrollRef = useRef<HTMLDivElement>(null);

  // Calculate total width for animation
  useEffect(() => {
    if (scrollRef.current) {
      const el = scrollRef.current;
      const firstChild = el.children[0] as HTMLElement;
      if (firstChild) {
        const totalWidth = firstChild.offsetWidth * demoImages.length;
        el.style.setProperty('--scroll-width', `${totalWidth}px`);
      }
    }
  }, []);

  // Auto-rotate testimonials
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [testimonials.length]);

  return (
    <div className="min-h-screen w-screen max-w-none bg-gradient-to-b from-blue-50/30 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section - Enhanced */}
      <section className="relative overflow-hidden w-screen max-w-none">
      {/* Background decorative elements */}
      <div className="absolute inset-0 overflow-hidden w-screen max-w-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-200/20 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-300/20 rounded-full blur-3xl"></div>
      </div>
        
        <div className="container mx-auto px-4 py-20 relative w-full max-w-none">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="text-center mb-0 max-w-5xl mx-auto"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="inline-block"
            >
            </motion.div>

            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.3 }}
              className="text-6xl md:text-7xl font-bold mb-8 leading-tight"
            >
              <span className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 bg-clip-text text-transparent">
                {t('home.title') || 'Transform Education with AI'}
              </span>
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.4 }}
              className="text-xl md:text-2xl text-gray-700 dark:text-gray-300 mb-10 leading-relaxed w-full"
            >
              {t('home.subtitle') || 'Advanced AI-powered attention tracking and engagement analytics for modern education'}
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-6 justify-center items-center -mb-12"
            >
              <Link href="/upload">
                <motion.div 
                  whileHover={{ scale: 1.05, y: -2 }} 
                  whileTap={{ scale: 0.98 }}
                  className="group"
                >
                  <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300 group-hover:shadow-blue-500/25">
                    <UploadIcon className="mr-3 h-6 w-6 group-hover:animate-bounce" />
                    {t('home.uploadButton') || 'Start Analysis'}
                    <ArrowRightIcon className="ml-3 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </motion.div>
              </Link>
              
              <Link href="/examples">
                <motion.div 
                  whileHover={{ scale: 1.05, y: -2 }} 
                  whileTap={{ scale: 0.98 }}
                >
                  <Button variant="outline" size="lg" className="border-2 border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-950 px-8 py-4 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300">
                    <PlayCircleIcon className="mr-3 h-6 w-6" />
                    Watch Demo
                  </Button>
                </motion.div>
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Demo Images Strip - Enhanced */}
      <section className="py-0 overflow-hidden">
        <div className="w-full px-0">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
          </motion.div>
          
          <div className="relative">
            {/* Enhanced gradient overlays - even higher opacity for stronger fade */}
            <div className="absolute left-0 top-0 w-32 h-full bg-gradient-to-r from-blue-50/95 dark:from-gray-900/95 via-blue-50/98 dark:via-gray-900/98 to-transparent z-20 pointer-events-none"></div>
            <div className="absolute right-0 top-0 w-32 h-full bg-gradient-to-l from-blue-50/95 dark:from-gray-900/95 via-blue-50/98 dark:via-gray-900/98 to-transparent z-20 pointer-events-none"></div>
            {/* Container with mask for better fade effect */}
            <div className="mask-image-horizontal w-full">
              {/* Scrolling images container */}
              <motion.div
                ref={scrollRef}
                className="flex gap-8 animate-carousel w-full"
                style={{ minWidth: '100vw' }}
                initial={{ x: 0 }}
              >
              {[...demoImages, ...demoImages].map((image, index) => (
                <motion.div
                  key={index}
                  className="flex-shrink-0 relative group cursor-pointer"
                  style={{ width: "22rem" }}
                  whileHover={{ y: -10, scale: 1.02 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="w-96 h-64 rounded-2xl overflow-hidden shadow-2xl bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 group-hover:shadow-3xl transition-all duration-500">
                    <img 
                      src={image.src} 
                      alt={image.alt}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    {/* Enhanced hover overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all duration-500 flex items-end">
                      <div className="w-full p-6 text-white transform translate-y-8 group-hover:translate-y-0 transition-transform duration-500">
                        <p className="text-lg font-semibold mb-2">{image.caption}</p>
                        <p className="text-sm opacity-90">Click to learn more about this analysis</p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </div>
          </div>
          
          
        </div>
      </section>


      {/* How It Works Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-800 dark:text-gray-200">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Get started with our platform in just three simple steps
            </p>
          </motion.div>

          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-3 gap-12">
              {[
                {
                  step: "1",
                  title: t('home.demo.step1.title') || "Upload Your Content",
                  description: t('home.demo.step1.description') || "Upload your video lectures or live stream your classes",
                  icon: UploadIcon,
                  color: "bg-blue-500"
                },
                {
                  step: "2", 
                  title: t('home.demo.step2.title') || "AI Analysis",
                  description: t('home.demo.step2.description') || "Our AI analyzes student attention and engagement in real-time",
                  icon: BrainIcon,
                  color: "bg-blue-600"
                },
                {
                  step: "3",
                  title: t('home.demo.step3.title') || "Get Insights",
                  description: t('home.demo.step3.description') || "Receive detailed reports and actionable insights to improve learning outcomes",
                  icon: BarChart3Icon,
                  color: "bg-blue-700"
                }
              ].map((step, index) => {
                const Icon = step.icon;
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.2 }}
                    viewport={{ once: true }}
                    className="text-center relative"
                  >
                    {/* Connection line */}
                    {index < 2 && (
                      <div className="hidden md:block absolute top-[40px] left-1 w-full h-[2px] bg-gradient-to-r from-blue-300 to-blue-400 transform translate-x-1/2 z-0"></div>
                    )}
                    
                    <div className="relative z-10">
                      <div className={`mx-auto w-20 h-20 ${step.color} rounded-full flex items-center justify-center mb-6 shadow-lg`}>
                        <Icon className="h-10 w-10 text-white" />
                      </div>
                    </div>
                    
                    <h3 className="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-200">
                      {step.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-lg leading-relaxed">
                      {step.description}
                    </p>
                  </motion.div>
                );
              })}
            </div>
          </div>
          {/* Enhanced call to action */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            viewport={{ once: true }}
            className="text-center mt-16 -mb-7"
          >
            <p className="text-xl text-gray-600 dark:text-gray-400 mb-6">
              Ready to transform your online classroom experience?
            </p>
            <Link href="/upload">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300">
                  Try It Free Today
                  <ArrowRightIcon className="ml-2 h-5 w-5" />
                </Button>
              </motion.div>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Dividing line between sections */}
      <div className="w-full flex justify-center">
        <div className="h-0.5 w-2/3 bg-gradient-to-r from-blue-200 via-blue-400 to-blue-200 dark:from-gray-700 dark:via-blue-800 dark:to-gray-700 rounded-full my-12"></div>
      </div>

      {/* Enhanced Features Grid */}
      <section className="py-19 bg-gray-50/50 dark:bg-gray-800/30">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-800 dark:text-gray-200">
              Powerful Features for Modern Education
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Our comprehensive suite of AI-powered tools helps educators understand and improve student engagement like never before
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            {enhancedFeatures.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  whileHover={{ y: -8, scale: 1.02 }}
                  className="group cursor-pointer"
                >
                  <Card className="h-full bg-white/80 backdrop-blur-sm dark:bg-gray-900/80 border-gray-200 dark:border-gray-700 shadow-lg group-hover:shadow-2xl transition-all duration-500 group-hover:border-blue-300 dark:group-hover:border-blue-600">
                    <CardHeader className="text-center pb-4">
                      <div className={`mx-auto w-16 h-16 ${feature.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 shadow-lg`}>
                        <Icon className="h-8 w-8 text-white" />
                      </div>
                      <CardTitle className="text-xl mb-3 group-hover:text-blue-600 transition-colors duration-300">{feature.title}</CardTitle>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <CardDescription className="text-center text-base leading-relaxed">
                        {feature.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </div>

          {/* Original features as secondary grid */}
        </div>
      </section>

      {/* About Us Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-800 dark:text-gray-200">
              About Us
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Meet the talented team behind EduVision
            </p>
          </motion.div>

          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-3 gap-10">
              {/* Team Member 1 */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -10 }}
                className="flex flex-col items-center"
              >
                <div className="w-48 h-48 rounded-full overflow-hidden mb-6 border-4 border-blue-100 dark:border-blue-900 shadow-xl">
                  <img
                    src="/images/Enes.jpeg"
                    alt="Enes Halit"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.src = `https://ui-avatars.com/api/?name=Enes+Halit&background=0062ff&color=fff&size=256`;
                    }}
                  />
                </div>
                <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">Enes Halit</h3>
                <p className="text-blue-600 dark:text-blue-400 font-medium mb-4">Full-Stack Developer</p>
                <div className="flex space-x-3">
                  <a href="https://github.com/Enes830" target="_blank" rel="noopener noreferrer" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-300 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                  </a>
                  <a href="https://www.linkedin.com/in/enes-halit-4361071a8/" target="_blank" rel="noopener noreferrer" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-300 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                      <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                    </svg>
                  </a>
                </div>
              </motion.div>

              {/* Team Member 2 */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                viewport={{ once: true }}
                whileHover={{ y: -10 }}
                className="flex flex-col items-center"
              >
                <div className="w-48 h-48 rounded-full overflow-hidden mb-6 border-4 border-blue-100 dark:border-blue-900 shadow-xl">
                  <img
                    src="/images/Mohammed.jpeg"
                    alt="Muhammed Erbay"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.src = `https://ui-avatars.com/api/?name=Muhammed+Erbay&background=0062ff&color=fff&size=256`;
                    }}
                  />
                </div>
                <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">Muhammed Erbay</h3>
                <p className="text-blue-600 dark:text-blue-400 font-medium mb-4">AI Engineer</p>
                <div className="flex space-x-3">
                  <a href="https://github.com/muhammederbay10" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-300 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                  </a>
                  <a href="https://www.linkedin.com/in/muhammed-erbay-00811422a/" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-300 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                      <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                    </svg>
                  </a>
                </div>
              </motion.div>

              {/* Team Member 3 */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
                viewport={{ once: true }}
                whileHover={{ y: -10 }}
                className="flex flex-col items-center"
              >
                <div className="w-48 h-48 rounded-full overflow-hidden mb-6 border-4 border-blue-100 dark:border-blue-900 shadow-xl">
                  <img
                    src="/images/Osama.jpg"
                    alt="Osama Elbagory"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.src = `https://ui-avatars.com/api/?name=Osama+Elbagory&background=0062ff&color=fff&size=256`;
                    }}
                  />
                </div>
                <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">Osama Elbagory</h3>
                <p className="text-blue-600 dark:text-blue-400 font-medium mb-4">Computer Vision Engineer</p>
                <div className="flex space-x-3">
                  <a href="https://github.com/O-sama2004" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-300 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                  </a>
                  <a href="https://www.linkedin.com/in/osama-elbagory/" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-300 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                      <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                    </svg>
                  </a>
                </div>
              </motion.div>
            </div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              viewport={{ once: true }}
              className="text-center mt-16 max-w-3xl mx-auto"
            >
              <p className="text-xl text-gray-700 dark:text-gray-300 leading-relaxed">
                Our passionate team of developers is dedicated to creating innovative AI solutions 
                that transform educational experiences and improve learning outcomes.
              </p>
            </motion.div>
          </div>
        </div>
      </section>


      {/* Integration Section (Coming Soon) */}
      <section className="py-20 bg-gray-50/50 dark:bg-gray-800/30 relative">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-800 dark:text-gray-200 flex items-center justify-center gap-4">
              Seamless Integration
              <span className="inline-block bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300 px-3 py-1 rounded-full text-base font-semibold border border-blue-200 dark:border-blue-800 animate-pulse">
                Coming Soon
              </span>
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Works with all your favorite educational platforms and tools
            </p>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8 max-w-4xl mx-auto">
            {[
              { name: "Zoom", icon: VideoIcon },
              { name: "Teams", icon: UsersIcon },
              { name: "Canvas", icon: BookOpenIcon },
              { name: "Moodle", icon: GraduationCapIcon },
              { name: "Blackboard", icon: MonitorIcon },
              { name: "Google Meet", icon: HeadphonesIcon }
            ].map((integration, index) => {
              const Icon = integration.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  whileHover={{ scale: 1.1, y: -5 }}
                  className="flex flex-col items-center group cursor-pointer"
                >
                  <div className="w-16 h-16 bg-white dark:bg-gray-800 rounded-2xl shadow-lg flex items-center justify-center mb-3 group-hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-gray-700">
                    <Icon className="h-8 w-8 text-blue-600" />
                  </div>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300 group-hover:text-blue-600 transition-colors">
                    {integration.name}
                  </span>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-blue-600 to-blue-800 text-white relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
        </div>
        
        <div className="container mx-auto px-4 relative">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center max-w-4xl mx-auto"
          >
            <h2 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              Ready to Transform Education?
            </h2>
            <p className="text-xl md:text-2xl mb-10 opacity-90 leading-relaxed">
              Join thousands of educators who are already using AI to create better learning experiences
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <Link href="/upload">
                <motion.div
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300">
                    <UploadIcon className="mr-3 h-6 w-6" />
                    Start for Free
                    <ArrowRightIcon className="ml-3 h-5 w-5" />
                  </Button>
                </motion.div>
              </Link>
              
            </div>

            {/* Trust indicators */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              viewport={{ once: true }}
              className="mt-12 flex flex-wrap justify-center items-center gap-8 text-sm opacity-80"
            >
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Slim Footer */}
      <footer className="py-10 bg-gray-900 text-white">
        <div className="container mx-auto px-6">
          <div className="border-t border-gray-800 pt-8 pb-2 flex flex-col md:flex-row justify-between items-center">
            <div className="text-left mb-6 md:mb-0 md:max-w-xl">
              <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                EduAI Analytics
              </h3>
              <p className="text-gray-400 leading-relaxed mt-3 mr-4">
                Transforming education through AI-powered attention analytics and engagement insights.
              </p>
            </div>
            <p className="text-gray-400 ml-0 md:ml-6">&copy; 2025 EduAI Analytics. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}