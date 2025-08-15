# Critical Missing Features for Blog-Poster MicroSaaS

## 🚨 MUST-HAVE Features for Production

This prompt addresses critical security, compliance, and business features that are ESSENTIAL for launching a production MicroSaaS platform.

## Priority 1: Security & Authentication Enhancements

### Email Verification System
```typescript
// src/components/auth/EmailVerification.tsx
import { useState, useEffect } from 'react'
import { supabase } from '@/services/supabase'

export function EmailVerification() {
  const [verifying, setVerifying] = useState(true)
  const [verified, setVerified] = useState(false)
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-indigo-100">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
        {verifying ? (
          <div className="text-center">
            <div className="spinner mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-2">Verifying your email...</h2>
            <p className="text-gray-600">Please wait while we confirm your email address.</p>
          </div>
        ) : verified ? (
          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold mb-2">Email Verified!</h2>
            <p className="text-gray-600 mb-6">Your email has been successfully verified.</p>
            <button 
              onClick={() => window.location.href = '/onboarding'}
              className="w-full py-3 bg-purple-gradient text-white rounded-lg hover:opacity-90"
            >
              Continue to Setup
            </button>
          </div>
        ) : (
          <div className="text-center">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold mb-2">Verification Failed</h2>
            <p className="text-gray-600 mb-6">The verification link is invalid or expired.</p>
            <button 
              onClick={() => window.location.href = '/register'}
              className="w-full py-3 bg-purple-gradient text-white rounded-lg hover:opacity-90"
            >
              Back to Registration
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
```

### Password Requirements Component
```typescript
// src/components/auth/PasswordStrength.tsx
export function PasswordStrength({ password }: { password: string }) {
  const requirements = [
    { regex: /.{8,}/, text: 'At least 8 characters' },
    { regex: /[A-Z]/, text: 'One uppercase letter' },
    { regex: /[a-z]/, text: 'One lowercase letter' },
    { regex: /[0-9]/, text: 'One number' },
    { regex: /[^A-Za-z0-9]/, text: 'One special character' }
  ]
  
  const strength = requirements.filter(req => req.regex.test(password)).length
  const strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'][strength]
  const strengthColor = ['red', 'orange', 'yellow', 'blue', 'green'][strength]
  
  return (
    <div className="mt-2">
      <div className="flex gap-1 mb-2">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className={`h-1 flex-1 rounded-full ${
              i < strength ? `bg-${strengthColor}-500` : 'bg-gray-200'
            }`}
          />
        ))}
      </div>
      <p className={`text-sm text-${strengthColor}-600`}>{strengthText}</p>
      <ul className="mt-2 space-y-1">
        {requirements.map((req, i) => (
          <li key={i} className="flex items-center text-sm">
            {req.regex.test(password) ? (
              <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" />
              </svg>
            ) : (
              <svg className="w-4 h-4 text-gray-300 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
              </svg>
            )}
            <span className={req.regex.test(password) ? 'text-green-600' : 'text-gray-400'}>
              {req.text}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
```

### Two-Factor Authentication (2FA)
```typescript
// src/pages/auth/TwoFactorSetup.tsx
import { useState } from 'react'
import QRCode from 'qrcode.react'

export function TwoFactorSetup() {
  const [secret] = useState('JBSWY3DPEHPK3PXP') // Generated secret
  const [verificationCode, setVerificationCode] = useState('')
  const [isEnabled, setIsEnabled] = useState(false)
  
  const otpAuthUrl = `otpauth://totp/BlogPoster:user@example.com?secret=${secret}&issuer=BlogPoster`
  
  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-6">Enable Two-Factor Authentication</h2>
      
      {!isEnabled ? (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border">
            <h3 className="font-semibold mb-4">1. Scan QR Code</h3>
            <p className="text-sm text-gray-600 mb-4">
              Use your authenticator app to scan this QR code:
            </p>
            <div className="bg-white p-4 rounded-lg flex justify-center">
              <QRCode value={otpAuthUrl} size={200} />
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg border">
            <h3 className="font-semibold mb-4">2. Enter Verification Code</h3>
            <p className="text-sm text-gray-600 mb-4">
              Enter the 6-digit code from your authenticator app:
            </p>
            <input
              type="text"
              value={verificationCode}
              onChange={(e) => setVerificationCode(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg text-center text-2xl tracking-widest"
              placeholder="000000"
              maxLength={6}
            />
          </div>
          
          <button
            onClick={() => setIsEnabled(true)}
            className="w-full py-3 bg-purple-gradient text-white rounded-lg hover:opacity-90"
          >
            Enable 2FA
          </button>
        </div>
      ) : (
        <div className="bg-green-50 p-6 rounded-lg">
          <div className="flex items-center mb-4">
            <svg className="w-8 h-8 text-green-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
            </svg>
            <h3 className="text-lg font-semibold text-green-800">2FA Enabled</h3>
          </div>
          <p className="text-green-700">
            Your account is now protected with two-factor authentication.
          </p>
        </div>
      )}
    </div>
  )
}
```

## Priority 2: GDPR Compliance

### Cookie Consent Banner
```typescript
// src/components/CookieConsent.tsx
import { useState, useEffect } from 'react'

export function CookieConsent() {
  const [show, setShow] = useState(false)
  
  useEffect(() => {
    const consent = localStorage.getItem('cookie-consent')
    if (!consent) setShow(true)
  }, [])
  
  const handleAccept = () => {
    localStorage.setItem('cookie-consent', 'accepted')
    setShow(false)
  }
  
  const handleDecline = () => {
    localStorage.setItem('cookie-consent', 'declined')
    setShow(false)
  }
  
  if (!show) return null
  
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg z-50 p-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex-1 mr-4">
          <p className="text-sm text-gray-600">
            We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies.
            <a href="/privacy" className="text-purple-600 hover:underline ml-1">Learn more</a>
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleDecline}
            className="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Decline
          </button>
          <button
            onClick={handleAccept}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Accept
          </button>
        </div>
      </div>
    </div>
  )
}
```

### Data Export & Account Deletion
```typescript
// src/pages/settings/DataPrivacy.tsx
export function DataPrivacy() {
  const [isDeleting, setIsDeleting] = useState(false)
  const [confirmText, setConfirmText] = useState('')
  
  const handleExportData = async () => {
    // Generate and download user data
    const userData = await apiClient.get('/api/user/export')
    const blob = new Blob([JSON.stringify(userData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'my-blog-poster-data.json'
    a.click()
  }
  
  const handleDeleteAccount = async () => {
    if (confirmText === 'DELETE MY ACCOUNT') {
      setIsDeleting(true)
      await apiClient.delete('/api/user/delete')
      // Redirect to goodbye page
      window.location.href = '/goodbye'
    }
  }
  
  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">Data & Privacy</h2>
      
      {/* Data Export */}
      <div className="bg-white p-6 rounded-lg border mb-6">
        <h3 className="text-lg font-semibold mb-2">Export Your Data</h3>
        <p className="text-gray-600 mb-4">
          Download all your data including articles, settings, and account information.
        </p>
        <button
          onClick={handleExportData}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Download My Data
        </button>
      </div>
      
      {/* Account Deletion */}
      <div className="bg-red-50 p-6 rounded-lg border border-red-200">
        <h3 className="text-lg font-semibold text-red-800 mb-2">Delete Account</h3>
        <p className="text-red-600 mb-4">
          This action is permanent and cannot be undone. All your data will be deleted.
        </p>
        <input
          type="text"
          value={confirmText}
          onChange={(e) => setConfirmText(e.target.value)}
          className="w-full px-4 py-2 border border-red-300 rounded-lg mb-4"
          placeholder="Type DELETE MY ACCOUNT to confirm"
        />
        <button
          onClick={handleDeleteAccount}
          disabled={confirmText !== 'DELETE MY ACCOUNT' || isDeleting}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
        >
          {isDeleting ? 'Deleting...' : 'Delete My Account'}
        </button>
      </div>
    </div>
  )
}
```

## Priority 3: Business-Critical Features

### Trial Management
```typescript
// src/components/TrialBanner.tsx
export function TrialBanner({ daysLeft }: { daysLeft: number }) {
  if (daysLeft > 7) return null
  
  const urgency = daysLeft <= 3 ? 'bg-red-600' : 'bg-orange-600'
  
  return (
    <div className={`${urgency} text-white px-4 py-3`}>
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" />
          </svg>
          <span className="font-medium">
            {daysLeft === 0 
              ? 'Your trial ends today!' 
              : `Your trial ends in ${daysLeft} day${daysLeft === 1 ? '' : 's'}`
            }
          </span>
        </div>
        <a
          href="/billing/upgrade"
          className="bg-white text-gray-900 px-4 py-2 rounded-lg font-medium hover:bg-gray-100"
        >
          Upgrade Now
        </a>
      </div>
    </div>
  )
}
```

### Coupon System
```typescript
// src/components/billing/CouponInput.tsx
export function CouponInput({ onApply }: { onApply: (discount: number) => void }) {
  const [code, setCode] = useState('')
  const [checking, setChecking] = useState(false)
  const [applied, setApplied] = useState(false)
  const [error, setError] = useState('')
  
  const handleApply = async () => {
    setChecking(true)
    setError('')
    
    try {
      const response = await apiClient.post('/api/coupons/validate', { code })
      if (response.valid) {
        setApplied(true)
        onApply(response.discount)
      } else {
        setError('Invalid coupon code')
      }
    } catch {
      setError('Failed to validate coupon')
    } finally {
      setChecking(false)
    }
  }
  
  return (
    <div className="bg-gray-50 p-4 rounded-lg">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Have a coupon code?
      </label>
      <div className="flex gap-2">
        <input
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value.toUpperCase())}
          disabled={applied}
          className="flex-1 px-4 py-2 border rounded-lg disabled:bg-gray-100"
          placeholder="ENTER CODE"
        />
        <button
          onClick={handleApply}
          disabled={!code || checking || applied}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
        >
          {checking ? 'Checking...' : applied ? 'Applied!' : 'Apply'}
        </button>
      </div>
      {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
      {applied && <p className="text-green-600 text-sm mt-2">Coupon applied successfully!</p>}
    </div>
  )
}
```

## Priority 4: Error Handling

### 404 Page
```typescript
// src/pages/NotFound.tsx
export function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-indigo-100">
      <div className="text-center">
        <h1 className="text-9xl font-bold text-purple-600 mb-4">404</h1>
        <h2 className="text-3xl font-semibold text-gray-800 mb-4">Page Not Found</h2>
        <p className="text-gray-600 mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={() => window.history.back()}
            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300"
          >
            Go Back
          </button>
          <a
            href="/"
            className="px-6 py-3 bg-purple-gradient text-white rounded-lg hover:opacity-90"
          >
            Go Home
          </a>
        </div>
      </div>
    </div>
  )
}
```

### Error Boundary
```typescript
// src/components/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
    // Send to error tracking service (e.g., Sentry)
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center p-8">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Something went wrong</h2>
            <p className="text-gray-600 mb-6">
              We're sorry, but something unexpected happened. Please try refreshing the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-3 bg-purple-gradient text-white rounded-lg hover:opacity-90"
            >
              Refresh Page
            </button>
          </div>
        </div>
      )
    }
    
    return this.props.children
  }
}
```

## Priority 5: Search & Filtering

### Global Search Component
```typescript
// src/components/GlobalSearch.tsx
import { useState, useEffect, useRef } from 'react'
import { Search } from 'lucide-react'

export function GlobalSearch() {
  const [isOpen, setIsOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any[]>([])
  const inputRef = useRef<HTMLInputElement>(null)
  
  // Keyboard shortcut (Cmd+K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setIsOpen(true)
      }
      if (e.key === 'Escape') {
        setIsOpen(false)
      }
    }
    
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])
  
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])
  
  const handleSearch = async (searchQuery: string) => {
    setQuery(searchQuery)
    if (searchQuery.length > 2) {
      // Simulate search
      setResults([
        { type: 'article', title: 'Service Dog Training Guide', url: '/articles/1' },
        { type: 'pipeline', title: 'Recent Pipeline Run', url: '/pipeline/1' },
        { type: 'setting', title: 'API Keys Configuration', url: '/settings/api-keys' },
      ])
    } else {
      setResults([])
    }
  }
  
  if (!isOpen) return null
  
  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-start justify-center min-h-screen pt-20 px-4">
        <div
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          onClick={() => setIsOpen(false)}
        />
        
        <div className="relative bg-white rounded-lg max-w-2xl w-full shadow-xl">
          <div className="flex items-center border-b px-4 py-3">
            <Search className="h-5 w-5 text-gray-400 mr-3" />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => handleSearch(e.target.value)}
              className="flex-1 outline-none text-lg"
              placeholder="Search articles, pipelines, settings..."
            />
            <kbd className="px-2 py-1 text-xs bg-gray-100 rounded">ESC</kbd>
          </div>
          
          {results.length > 0 && (
            <div className="max-h-96 overflow-y-auto">
              {results.map((result, index) => (
                <a
                  key={index}
                  href={result.url}
                  className="block px-4 py-3 hover:bg-gray-50 flex items-center"
                >
                  <span className="text-xs uppercase text-gray-500 mr-3">
                    {result.type}
                  </span>
                  <span className="flex-1">{result.title}</span>
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </a>
              ))}
            </div>
          )}
          
          {query.length > 2 && results.length === 0 && (
            <div className="px-4 py-8 text-center text-gray-500">
              No results found for "{query}"
            </div>
          )}
          
          <div className="px-4 py-3 border-t bg-gray-50 flex items-center justify-between">
            <div className="flex gap-4 text-xs text-gray-500">
              <span><kbd>↑↓</kbd> Navigate</span>
              <span><kbd>Enter</kbd> Select</span>
              <span><kbd>Esc</kbd> Close</span>
            </div>
            <div className="text-xs text-gray-500">
              Press <kbd className="px-1 py-0.5 bg-gray-200 rounded">⌘K</kbd> to search
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

## Implementation Priority

### Must-Have for Launch (Week 1)
1. ✅ Email verification
2. ✅ Password requirements
3. ✅ 404 page
4. ✅ Error boundary
5. ✅ Cookie consent

### High Priority (Week 2)
1. ✅ Two-factor authentication
2. ✅ Trial management
3. ✅ Data export
4. ✅ Account deletion
5. ✅ Global search

### Important (Week 3)
1. ✅ Coupon system
2. ✅ Session management
3. ✅ Rate limiting
4. ✅ Audit logging

This prompt provides the CRITICAL missing features that are essential for a production MicroSaaS platform. Implement these before launching to ensure security, compliance, and professional functionality.