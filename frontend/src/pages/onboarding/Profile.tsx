import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { OnboardingLayout } from '@/components/onboarding/OnboardingLayout'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
import { User, Building, Target, Lightbulb } from 'lucide-react'

export default function Profile() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    fullName: '',
    jobTitle: '',
    company: '',
    companySize: '',
    industry: '',
    contentFrequency: '',
    contentGoals: [] as string[],
    currentProcess: ''
  })

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleGoalToggle = (goal: string) => {
    setFormData(prev => ({
      ...prev,
      contentGoals: prev.contentGoals.includes(goal)
        ? prev.contentGoals.filter(g => g !== goal)
        : [...prev.contentGoals, goal]
    }))
  }

  const handleContinue = () => {
    navigate('/onboarding/api-keys')
  }

  const handleBack = () => {
    navigate('/onboarding')
  }

  const handleSkip = () => {
    navigate('/onboarding/api-keys')
  }

  const canContinue = Boolean(formData.fullName && formData.jobTitle)

  const jobTitles = [
    'Content Manager',
    'SEO Specialist', 
    'Marketing Director',
    'Agency Owner',
    'Blogger',
    'Content Writer',
    'Digital Marketer',
    'Other'
  ]

  const companySizes = [
    'Just me',
    '2-10 people',
    '11-50 people', 
    '51-200 people',
    '200+ people'
  ]

  const industries = [
    'Technology',
    'Healthcare',
    'Finance',
    'Legal',
    'E-commerce',
    'Education',
    'Real Estate',
    'Marketing & Advertising',
    'Manufacturing',
    'Other'
  ]

  const contentGoals = [
    'Increase organic traffic',
    'Save time on content creation',
    'Improve SEO rankings',
    'Scale content production',
    'Ensure legal compliance',
    'Reduce content costs'
  ]

  const currentProcesses = [
    'Manual writing',
    'Freelance writers',
    'Content agencies',
    'Basic AI tools',
    'No consistent process'
  ]

  const frequencies = [
    'Daily',
    'Weekly',
    'Bi-weekly',
    'Monthly',
    'As needed'
  ]

  return (
    <OnboardingLayout
      currentStep={2}
      totalSteps={5}
      stepName="Tell us about yourself"
      onBack={handleBack}
      onSkip={handleSkip}
      onContinue={handleContinue}
      canContinue={canContinue}
    >
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <User className="w-12 h-12 text-primary mx-auto" />
          <h1 className="text-2xl font-bold text-foreground">
            Tell Us About Yourself
          </h1>
          <p className="text-muted-foreground">
            This helps us personalize your experience and optimize our AI agents for your needs
          </p>
        </div>

        <div className="grid gap-6">
          {/* Personal Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <User className="w-5 h-5" />
                <span>Personal Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name *</Label>
                <Input
                  id="fullName"
                  value={formData.fullName}
                  onChange={(e) => handleInputChange('fullName', e.target.value)}
                  placeholder="Enter your full name"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="jobTitle">Job Title *</Label>
                <Select value={formData.jobTitle} onValueChange={(value) => handleInputChange('jobTitle', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select your role" />
                  </SelectTrigger>
                  <SelectContent>
                    {jobTitles.map(title => (
                      <SelectItem key={title} value={title}>{title}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="company">Company/Organization</Label>
                <Input
                  id="company"
                  value={formData.company}
                  onChange={(e) => handleInputChange('company', e.target.value)}
                  placeholder="Your company name"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="companySize">Company Size</Label>
                <Select value={formData.companySize} onValueChange={(value) => handleInputChange('companySize', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select company size" />
                  </SelectTrigger>
                  <SelectContent>
                    {companySizes.map(size => (
                      <SelectItem key={size} value={size}>{size}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Content Goals */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="w-5 h-5" />
                <span>Content Goals</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>What&apos;s your primary content goal? (Select all that apply)</Label>
                <div className="grid md:grid-cols-2 gap-3">
                  {contentGoals.map(goal => (
                    <div key={goal} className="flex items-center space-x-2">
                      <Checkbox
                        id={goal}
                        checked={formData.contentGoals.includes(goal)}
                        onCheckedChange={() => handleGoalToggle(goal)}
                      />
                      <Label htmlFor={goal} className="text-sm">{goal}</Label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>How do you currently create content?</Label>
                  <Select value={formData.currentProcess} onValueChange={(value) => handleInputChange('currentProcess', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select current process" />
                    </SelectTrigger>
                    <SelectContent>
                      {currentProcesses.map(process => (
                        <SelectItem key={process} value={process}>{process}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>How often do you publish content?</Label>
                  <Select value={formData.contentFrequency} onValueChange={(value) => handleInputChange('contentFrequency', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select frequency" />
                    </SelectTrigger>
                    <SelectContent>
                      {frequencies.map(freq => (
                        <SelectItem key={freq} value={freq}>{freq}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Blog Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Building className="w-5 h-5" />
                <span>Blog Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Industry/Niche</Label>
                <Select value={formData.industry} onValueChange={(value) => handleInputChange('industry', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select your industry" />
                  </SelectTrigger>
                  <SelectContent>
                    {industries.map(industry => (
                      <SelectItem key={industry} value={industry}>{industry}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Why We Ask This */}
          <Card className="bg-muted/50">
            <CardContent className="p-6">
              <div className="flex items-start space-x-3">
                <Lightbulb className="w-5 h-5 text-primary mt-0.5" />
                <div>
                  <h3 className="font-semibold text-foreground mb-2">Why We Ask This</h3>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Customize agent prompts for your industry</li>
                    <li>• Suggest relevant keywords and topics</li>
                    <li>• Optimize writing style and tone</li>
                    <li>• Provide industry-specific templates</li>
                    <li>• Recommend content strategies that work</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </OnboardingLayout>
  )
}