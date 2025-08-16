import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card } from '@/components/ui/card'
import { PipelineConfiguration } from '@/components/pipeline/PipelineConfiguration'
import { ExecutionMonitor } from '@/components/pipeline/ExecutionMonitor'
import { PipelineHistory } from '@/components/pipeline/PipelineHistory'
import { AgentStatus } from '@/components/pipeline/AgentStatus'
import { Settings, Activity, History, Zap } from 'lucide-react'

export function Pipeline() {
  const [activeTab, setActiveTab] = useState('monitor')

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Pipeline Management
          </h1>
          <p className="mt-2 text-gray-600">
            Orchestrate and monitor your 5-agent content generation workflow
          </p>
        </div>

        {/* Agent Status Overview */}
        <div className="mb-8">
          <AgentStatus />
        </div>

        {/* Main Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <TabsList className="grid grid-cols-4 w-full max-w-2xl mx-auto bg-white/50 backdrop-blur-sm border border-purple-100">
            <TabsTrigger value="monitor" className="flex items-center gap-2">
              <Activity className="w-4 h-4" />
              Monitor
            </TabsTrigger>
            <TabsTrigger value="configure" className="flex items-center gap-2">
              <Settings className="w-4 h-4" />
              Configure
            </TabsTrigger>
            <TabsTrigger value="history" className="flex items-center gap-2">
              <History className="w-4 h-4" />
              History
            </TabsTrigger>
            <TabsTrigger value="quick" className="flex items-center gap-2">
              <Zap className="w-4 h-4" />
              Quick Run
            </TabsTrigger>
          </TabsList>

          <TabsContent value="monitor" className="space-y-4">
            <Card className="p-6 bg-white/80 backdrop-blur-sm">
              <ExecutionMonitor />
            </Card>
          </TabsContent>

          <TabsContent value="configure" className="space-y-4">
            <Card className="p-6 bg-white/80 backdrop-blur-sm">
              <PipelineConfiguration />
            </Card>
          </TabsContent>

          <TabsContent value="history" className="space-y-4">
            <Card className="p-6 bg-white/80 backdrop-blur-sm">
              <PipelineHistory />
            </Card>
          </TabsContent>

          <TabsContent value="quick" className="space-y-4">
            <Card className="p-6 bg-white/80 backdrop-blur-sm">
              <div className="text-center py-12">
                <Zap className="w-16 h-16 mx-auto text-purple-600 mb-4" />
                <h3 className="text-xl font-semibold mb-2">Quick Pipeline Run</h3>
                <p className="text-gray-600 mb-6">
                  Start a new pipeline execution with default settings
                </p>
                <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all">
                  Start Pipeline
                </button>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}