import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Mail, Clock, ArrowLeft } from 'lucide-react'
import { supabase } from '@/services/supabase'
import { toast } from 'react-hot-toast'

export function VerifyEmail() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [resending, setResending] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)

  useEffect(() => {
    // If user is already verified, redirect to dashboard
    if (user?.email_confirmed_at) {
      navigate('/dashboard')
    }
  }, [user, navigate])

  useEffect(() => {
    // Cooldown timer
    if (resendCooldown > 0) {
      const timer = setTimeout(() => setResendCooldown(resendCooldown - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [resendCooldown])

  const handleResendEmail = async () => {
    if (!user?.email || resendCooldown > 0) return

    setResending(true)
    try {
      const { error } = await supabase.auth.resend({
        type: 'signup',
        email: user.email,
        options: {
          emailRedirectTo: `${window.location.origin}/onboarding`
        }
      })

      if (error) throw error

      toast.success('Verification email sent!')
      setResendCooldown(60) // 60 second cooldown
    } catch (error: any) {
      toast.error(error.message || 'Failed to resend email')
    } finally {
      setResending(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-purple-gradient rounded-xl flex items-center justify-center">
              <Mail className="w-8 h-8 text-white" />
            </div>
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
            Check Your Email
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            We've sent a verification link to:
          </p>
          <p className="font-medium text-gray-900 dark:text-white mt-1">
            {user?.email}
          </p>
        </div>

        {/* Verification Card */}
        <Card>
          <CardHeader>
            <CardTitle>Email Verification</CardTitle>
            <CardDescription>
              Click the link in your email to verify your account
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <Alert>
              <Clock className="w-4 h-4" />
              <AlertDescription className="text-sm">
                The verification link will expire in 24 hours. Please check your spam folder if you don't see the email.
              </AlertDescription>
            </Alert>

            <div className="space-y-4">
              <Button
                onClick={handleResendEmail}
                disabled={resending || resendCooldown > 0}
                variant="outline"
                className="w-full"
              >
                {resending ? (
                  <div className="flex items-center space-x-2">
                    <div className="spinner"></div>
                    <span>Sending...</span>
                  </div>
                ) : resendCooldown > 0 ? (
                  `Resend in ${resendCooldown}s`
                ) : (
                  'Resend Verification Email'
                )}
              </Button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300 dark:border-gray-600"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-background text-muted-foreground">
                    Already verified?
                  </span>
                </div>
              </div>

              <Button
                onClick={() => navigate('/login')}
                variant="default"
                className="w-full bg-purple-gradient hover:opacity-90"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Login
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Support Link */}
        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Having trouble?{' '}
            <Link
              to="/contact"
              className="font-medium text-primary hover:text-primary/80"
            >
              Contact Support
            </Link>
          </p>
        </div>

        {/* Footer */}
        <div className="text-center text-xs text-gray-500">
          <p>© 2024 ServiceDogUS. All rights reserved.</p>
        </div>
      </div>
    </div>
  )
}