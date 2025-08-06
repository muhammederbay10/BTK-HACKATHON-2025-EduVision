"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Loader2, User, Mail, LogOut, Edit } from "lucide-react";

export default function ProfilePage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  
  // Redirect to login if not authenticated
  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [user, loading, router]);

  const handleLogout = async () => {
    try {
      await logout();
      router.push("/");
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50/30 to-white dark:from-gray-900 dark:to-gray-800 flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto text-blue-600" />
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900 dark:text-white">
            Loading...
          </h2>
        </div>
      </div>
    );
  }
  
  // If no user and not loading, the useEffect will redirect to login
  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50/30 to-white dark:from-gray-900 dark:to-gray-800 flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
      <motion.div 
        initial={{ opacity: 0, y: 20 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.5 }}
        className="w-full max-w-4xl"
      >
        <div className="text-center mb-12">
          <motion.h2 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="text-4xl font-extrabold text-gray-900 dark:text-white"
          >
            Your Profile
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="mt-2 text-xl text-gray-600 dark:text-gray-400"
          >
            Manage your account information and view your analytics
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Profile Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="md:col-span-1"
          >
            <Card className="border-gray-200 dark:border-gray-700 shadow-lg">
              <CardHeader className="text-center">
                <div className="mx-auto mb-4">
                  <Avatar className="h-24 w-24">
                    <AvatarImage
                      src={`https://ui-avatars.com/api/?name=${encodeURIComponent(
                        user.name
                      )}&background=0062ff&color=fff&size=256`}
                      alt={user.name}
                    />
                    <AvatarFallback className="text-2xl">
                      {user.name.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                </div>
                <CardTitle className="text-2xl">{user.name}</CardTitle>
                <CardDescription className="flex items-center justify-center mt-1">
                  <Mail className="h-4 w-4 mr-1" />
                  {user.email}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center">
                    <User className="h-4 w-4 mr-2" />
                    Account ID: {user.id}
                  </p>
                </div>
              </CardContent>
              <CardFooter className="flex flex-col gap-3">
                <Button 
                  variant="outline" 
                  className="w-full flex items-center"
                >
                  <Edit className="mr-2 h-4 w-4" />
                  Edit Profile
                </Button>
                <Button 
                  variant="destructive" 
                  className="w-full flex items-center"
                  onClick={handleLogout}
                >
                  <LogOut className="mr-2 h-4 w-4" />
                  Logout
                </Button>
              </CardFooter>
            </Card>
          </motion.div>

          {/* Stats and Activities */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="md:col-span-2"
          >
            <div className="space-y-6">
              <Card className="border-gray-200 dark:border-gray-700 shadow-lg">
                <CardHeader>
                  <CardTitle>Account Dashboard</CardTitle>
                  <CardDescription>
                    Your account statistics and activities
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div className="border rounded-lg p-4 bg-blue-50/50 dark:bg-blue-900/20">
                      <p className="text-sm text-gray-500 dark:text-gray-400">Uploads</p>
                      <p className="text-2xl font-semibold text-blue-600 dark:text-blue-400">0</p>
                    </div>
                    <div className="border rounded-lg p-4 bg-green-50/50 dark:bg-green-900/20">
                      <p className="text-sm text-gray-500 dark:text-gray-400">Reports Generated</p>
                      <p className="text-2xl font-semibold text-green-600 dark:text-green-400">0</p>
                    </div>
                  </div>

                  <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
                      Recent Activities
                    </h3>
                    <div className="space-y-2">
                      <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
                        <p className="text-sm text-gray-800 dark:text-gray-200">
                          Welcome to EduVision! Your account was created successfully.
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          Just now
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-gray-200 dark:border-gray-700 shadow-lg">
                <CardHeader>
                  <CardTitle>Get Started</CardTitle>
                  <CardDescription>
                    Begin using EduVision&apos;s powerful features
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white" onClick={() => router.push("/upload")}>
                      Upload your first video for analysis
                    </Button>
                    <Button variant="outline" className="w-full" onClick={() => router.push("/examples")}>
                      View example reports
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}