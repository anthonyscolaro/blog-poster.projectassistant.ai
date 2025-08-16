import React from 'react'

export default function Privacy() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-8">Privacy Policy</h1>
        <div className="prose prose-lg dark:prose-invert max-w-none">
          <p>Last updated: January 2024</p>
          <p>Your privacy is important to us. This Privacy Policy explains how Blog-Poster collects, uses, and protects your information.</p>
          
          <h2>Information We Collect</h2>
          <p>We collect minimal data necessary for service delivery including account information, usage data, and content you create.</p>
          
          <h2>How We Use Information</h2>
          <p>We use your information to provide and improve our service, process payments, and provide customer support.</p>
          
          <h2>Contact Us</h2>
          <p>For privacy questions, contact us at privacy@blog-poster.com</p>
        </div>
      </div>
    </div>
  )
}