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
      title: "Real-time Alerts",
      description: "Instant notifications when students need additional support or attention",
      color: "bg-yellow-500"
    }
  ];

  // Statistics
  const stats = [
    { number: "150K+", label: "Students Analyzed", icon: UsersIcon },
    { number: "2.5M+", label: "Hours of Content", icon: ClockIcon },
    { number: "98%", label: "Accuracy Rate", icon: CheckCircleIcon },
    { number: "45%", label: "Improvement in Engagement", icon: TrendingUpIcon }
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

  // Pricing tiers
  const pricingTiers = [
    {
      name: "Starter",
      price: "$29",
      period: "/month",
      description: "Perfect for individual educators",
      features: [
        "Up to 30 students",
        "Basic attention analytics",
        "Weekly reports",
        "Email support"
      ],
      popular: false
    },
    {
      name: "Professional",
      price: "$79",
      period: "/month",
      description: "Ideal for schools and institutions",
      features: [
        "Up to 200 students",
        "Advanced AI insights",
        "Real-time alerts",
        "Custom reports",
        "Priority support",
        "API access"
      ],
      popular: true
    },
    {
      name: "Enterprise",
      price: "Custom",
      period: "",
      description: "For large organizations",
      features: [
        "Unlimited students",
        "Custom AI models",
        "White-label solution",
        "Dedicated support",
        "Custom integrations",
        "SLA guarantee"
      ],
      popular: false
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
    <div className="min-h-screen bg-gradient-to-b from-blue-50/30 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section - Enhanced */}
      <section className="relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-200/20 rounded-full blur-3xl"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-300/20 rounded-full blur-3xl"></div>
        </div>
        
        <div className="container mx-auto px-4 py-24 relative">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="text-center mb-16 max-w-5xl mx-auto"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="inline-block"
            >
              <div className="bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-4 py-2 rounded-full text-sm font-medium mb-6 border border-blue-200 dark:border-blue-800">
                🚀 AI-Powered Education Analytics
              </div>
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
              className="text-xl md:text-2xl text-gray-700 dark:text-gray-300 mb-10 leading-relaxed max-w-4xl mx-auto"
            >
              {t('home.subtitle') || 'Advanced AI-powered attention tracking and engagement analytics for modern education'}
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-6 justify-center items-center"
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

            {/* Trust indicators */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="mt-12 flex flex-wrap justify-center items-center gap-8 text-sm text-gray-600 dark:text-gray-400"
            >
              <div className="flex items-center gap-2">
                <ShieldCheckIcon className="h-5 w-5 text-green-500" />
                <span>SOC 2 Compliant</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircleIcon className="h-5 w-5 text-blue-500" />
                <span>FERPA Certified</span>
              </div>
              <div className="flex items-center gap-2">
                <StarIcon className="h-5 w-5 text-yellow-500 fill-current" />
                <span>4.9/5 Rating</span>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-16 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="text-center group"
                >
                  <div className="mb-4 mx-auto w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <Icon className="h-8 w-8 text-blue-600" />
                  </div>
                  <motion.div
                    initial={{ scale: 1 }}
                    whileInView={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 0.6, delay: index * 0.1 + 0.5 }}
                    viewport={{ once: true }}
                    className="text-3xl md:text-4xl font-bold text-gray-800 dark:text-gray-200 mb-2"
                  >
                    {stat.number}
                  </motion.div>
                  <p className="text-gray-600 dark:text-gray-400 font-medium">{stat.label}</p>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* Demo Images Strip - Enhanced */}
      <section className="py-20 overflow-hidden">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-800 dark:text-gray-200">
              See Our AI in Action
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Real examples of attention tracking and classroom analysis powered by cutting-edge computer vision
            </p>
          </motion.div>
          
          <div className="relative">
            {/* Enhanced gradient overlays */}
            <div className="absolute left-0 top-0 w-32 h-full bg-gradient-to-r from-white dark:from-gray-900 via-white/80 dark:via-gray-900/80 to-transparent z-10 pointer-events-none"></div>
            <div className="absolute right-0 top-0 w-32 h-full bg-gradient-to-l from-white dark:from-gray-900 via-white/80 dark:via-gray-900/80 to-transparent z-10 pointer-events-none"></div>
            
            {/* Scrolling images container */}
            <motion.div
              ref={scrollRef}
              className="flex gap-8 animate-carousel"
              style={{ width: 'max-content' }}
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
          
          {/* Enhanced call to action */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            viewport={{ once: true }}
            className="text-center mt-16"
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

      {/* Enhanced Features Grid */}
      <section className="py-20 bg-gray-50/50 dark:bg-gray-800/30">
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
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 * index }}
                  viewport={{ once: true }}
                  whileHover={{ y: -5, scale: 1.02 }}
                >
                  <Card className="h-full bg-white/60 backdrop-blur-sm dark:bg-gray-900/60 border-blue-100 dark:border-blue-800 shadow-lg hover:shadow-xl transition-all duration-300">
                    <CardHeader className="text-center">
                      <div className="mx-auto w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mb-4 hover:rotate-6 transition-transform duration-300">
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
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
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
              Trusted by Educators Worldwide
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              See what teachers and professors are saying about our platform
            </p>
          </motion.div>

          <div className="max-w-6xl mx-auto">
            <motion.div
              key={activeTestimonial}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.5 }}
              className="text-center"
            >
              <Card className="max-w-4xl mx-auto bg-gradient-to-r from-blue-50 to-white dark:from-gray-800 dark:to-gray-900 border-0 shadow-2xl">
                <CardContent className="p-12">
                  <div className="flex justify-center mb-6">
                    {[...Array(testimonials[activeTestimonial].rating)].map((_, i) => (
                      <StarIcon key={i} className="h-6 w-6 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <blockquote className="text-2xl font-medium text-gray-800 dark:text-gray-200 mb-8 leading-relaxed">
                    "{testimonials[activeTestimonial].content}"
                  </blockquote>
                  <div className="flex items-center justify-center space-x-4">
                    <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-white font-bold text-xl">
                        {testimonials[activeTestimonial].name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div className="text-left">
                      <p className="font-semibold text-gray-800 dark:text-gray-200">
                        {testimonials[activeTestimonial].name}
                      </p>
                      <p className="text-gray-600 dark:text-gray-400">
                        {testimonials[activeTestimonial].role}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Testimonial indicators */}
            <div className="flex justify-center mt-8 space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setActiveTestimonial(index)}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === activeTestimonial 
                      ? 'bg-blue-600 w-8' 
                      : 'bg-gray-300 dark:bg-gray-600 hover:bg-gray-400'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-gray-50/50 dark:bg-gray-800/30">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-800 dark:text-gray-200">
              Choose Your Plan
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Flexible pricing options to fit your educational needs and budget
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {pricingTiers.map((tier, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -8, scale: 1.02 }}
                className={`relative ${tier.popular ? 'z-10' : ''}`}
              >
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium">
                      Most Popular
                    </span>
                  </div>
                )}
                <Card className={`h-full ${
                  tier.popular 
                    ? 'bg-white dark:bg-gray-900 border-2 border-blue-600 shadow-2xl' 
                    : 'bg-white/80 dark:bg-gray-900/80 border border-gray-200 dark:border-gray-700 shadow-lg'
                } hover:shadow-2xl transition-all duration-500`}>
                  <CardHeader className="text-center pb-8">
                    <CardTitle className="text-2xl font-bold mb-2">{tier.name}</CardTitle>
                    <div className="mb-4">
                      <span className="text-4xl font-bold text-blue-600">{tier.price}</span>
                      <span className="text-gray-600 dark:text-gray-400">{tier.period}</span>
                    </div>
                    <CardDescription className="text-base">{tier.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <ul className="space-y-3">
                      {tier.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-center">
                          <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                          <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <div className="pt-6">
                      <Button 
                        className={`w-full py-3 text-lg font-semibold transition-all duration-300 ${
                          tier.popular
                            ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl'
                            : 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-950'
                        }`}
                        variant={tier.popular ? 'default' : 'outline'}
                      >
                        {tier.name === 'Enterprise' ? 'Contact Sales' : 'Get Started'}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Money back guarantee */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: true }}
            className="text-center mt-12"
          >
            <div className="inline-flex items-center space-x-2 text-gray-600 dark:text-gray-400">
              <ShieldCheckIcon className="h-5 w-5 text-green-500" />
              <span>30-day money-back guarantee</span>
            </div>
          </motion.div>
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
                      <div className="hidden md:block absolute top-16 left-1/2 w-full h-0.5 bg-gradient-to-r from-blue-300 to-blue-400 transform translate-x-1/2 z-0"></div>
                    )}
                    
                    <div className="relative z-10">
                      <div className={`mx-auto w-20 h-20 ${step.color} rounded-full flex items-center justify-center mb-6 shadow-lg`}>
                        <Icon className="h-10 w-10 text-white" />
                      </div>
                      <div className="absolute -top-2 -right-2 w-8 h-8 bg-white dark:bg-gray-900 rounded-full flex items-center justify-center border-2 border-blue-500 shadow-lg">
                        <span className="text-blue-600 font-bold text-sm">{step.step}</span>
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
        </div>
      </section>

      {/* Integration Section */}
      <section className="py-20 bg-gray-50/50 dark:bg-gray-800/30">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-800 dark:text-gray-200">
              Seamless Integration
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
                    Start Free Trial
                    <ArrowRightIcon className="ml-3 h-5 w-5" />
                  </Button>
                </motion.div>
              </Link>
              
              <Link href="/contact">
                <motion.div
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Button variant="outline" size="lg" className="border-2 border-white text-white hover:bg-white hover:text-blue-600 px-8 py-4 text-lg font-semibold transition-all duration-300">
                    <HeadphonesIcon className="mr-3 h-6 w-6" />
                    Talk to Sales
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
              <div className="flex items-center gap-2">
                <CheckCircleIcon className="h-5 w-5" />
                <span>No setup fees</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircleIcon className="h-5 w-5" />
                <span>Cancel anytime</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircleIcon className="h-5 w-5" />
                <span>24/7 support</span>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 bg-gray-900 text-white">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                EduAI Analytics
              </h3>
              <p className="text-gray-400 leading-relaxed">
                Transforming education through AI-powered attention analytics and engagement insights.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4 text-lg">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Integrations</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4 text-lg">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4 text-lg">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2024 EduAI Analytics. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}