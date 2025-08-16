import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'

interface TeamChartsProps {
  productivityData?: Array<{
    date: string
    articles: number
    member: string
  }>
  collaborationData?: Array<{
    name: string
    articles: number
    quality: number
    role: string
  }>
  activityData?: Array<{
    date: string
    activities: number
  }>
}

export function TeamCharts({ productivityData, collaborationData, activityData }: TeamChartsProps) {
  // Mock data for demonstration
  const defaultProductivityData = [
    { date: '2024-01-01', articles: 12, member: 'Sarah Chen' },
    { date: '2024-01-02', articles: 8, member: 'Mike Rodriguez' },
    { date: '2024-01-03', articles: 15, member: 'Lisa Park' },
    { date: '2024-01-04', articles: 6, member: 'John Smith' },
    { date: '2024-01-05', articles: 10, member: 'Emma Wilson' },
    { date: '2024-01-06', articles: 9, member: 'David Kim' },
    { date: '2024-01-07', articles: 14, member: 'Anna Taylor' }
  ]

  const defaultCollaborationData = [
    { name: 'Sarah Chen', articles: 12, quality: 95, role: 'editor' },
    { name: 'Mike Rodriguez', articles: 8, quality: 92, role: 'member' },
    { name: 'Lisa Park', articles: 15, quality: 88, role: 'admin' },
    { name: 'John Smith', articles: 6, quality: 91, role: 'member' },
    { name: 'Emma Wilson', articles: 10, quality: 94, role: 'editor' },
  ]

  const defaultActivityData = [
    { date: '2024-01-01', activities: 45 },
    { date: '2024-01-02', activities: 38 },
    { date: '2024-01-03', activities: 52 },
    { date: '2024-01-04', activities: 31 },
    { date: '2024-01-05', activities: 42 },
    { date: '2024-01-06', activities: 39 },
    { date: '2024-01-07', activities: 47 }
  ]

  const roleColors = {
    owner: '#8b5cf6',
    admin: '#3b82f6', 
    editor: '#10b981',
    member: '#6b7280',
    viewer: '#9ca3af'
  }

  const productivity = productivityData || defaultProductivityData
  const collaboration = collaborationData || defaultCollaborationData
  const activity = activityData || defaultActivityData

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Team Productivity Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Team Productivity</CardTitle>
          <CardDescription>Articles created by team members this week</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={collaboration}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                formatter={(value, name) => [value, name === 'articles' ? 'Articles' : 'Quality Score']}
                labelFormatter={(name) => `Team Member: ${name}`}
              />
              <Bar dataKey="articles" fill="#8b5cf6" name="articles" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Quality vs Quantity */}
      <Card>
        <CardHeader>
          <CardTitle>Quality vs Quantity</CardTitle>
          <CardDescription>Balance between article output and SEO quality</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={collaboration}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                formatter={(value, name) => [
                  value, 
                  name === 'articles' ? 'Articles' : 'Quality Score'
                ]}
              />
              <Bar dataKey="quality" fill="#10b981" name="quality" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Daily Activity Trend */}
      <Card>
        <CardHeader>
          <CardTitle>Team Activity Trend</CardTitle>
          <CardDescription>Daily team activity over the past week</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={activity}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleDateString()}
                formatter={(value) => [value, 'Activities']}
              />
              <Line 
                type="monotone" 
                dataKey="activities" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Team Performance Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Summary</CardTitle>
          <CardDescription>Key metrics for team collaboration</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {collaboration.map((member, index) => (
            <div key={member.name} className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: roleColors[member.role as keyof typeof roleColors] || '#6b7280' }} />
                <span className="text-sm font-medium">{member.name}</span>
                <Badge variant="outline" className="text-xs">
                  {member.role}
                </Badge>
              </div>
              
              <div className="flex items-center gap-4 text-sm">
                <span className="text-muted-foreground">
                  {member.articles} articles
                </span>
                <span className={`font-medium ${
                  member.quality >= 90 ? 'text-green-600' : 
                  member.quality >= 80 ? 'text-yellow-600' : 
                  'text-red-600'
                }`}>
                  {member.quality}% quality
                </span>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}