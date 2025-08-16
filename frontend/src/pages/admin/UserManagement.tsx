import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/integrations/supabase/client'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { 
  Users, 
  Search, 
  Filter, 
  Download,
  MoreHorizontal,
  UserCheck,
  UserX,
  Shield,
  Activity,
  Clock,
  TrendingUp,
  Building
} from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

interface User {
  id: string
  email: string
  full_name: string | null
  avatar_url: string | null
  organization_name: string
  plan: string
  role: string
  status: 'active' | 'inactive' | 'suspended' | 'trial'
  last_active: string
  articles_generated: number
  health_score: number
  joined_date: string
}

interface UserStats {
  total_users: number
  active_users: number
  new_users_week: number
  inactive_users: number
  suspended_users: number
}

export default function UserManagement() {
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [planFilter, setPlanFilter] = useState<string>('all')
  const [roleFilter, setRoleFilter] = useState<string>('all')

  // Mock data for demonstration
  const mockStats: UserStats = {
    total_users: 12456,
    active_users: 8123,
    new_users_week: 234,
    inactive_users: 2156,
    suspended_users: 12
  }

  const mockUsers: User[] = [
    {
      id: '1',
      email: 'john.doe@techcorp.com',
      full_name: 'John Doe',
      avatar_url: null,
      organization_name: 'TechCorp',
      plan: 'Professional',
      role: 'Owner',
      status: 'active',
      last_active: '2 hours ago',
      articles_generated: 247,
      health_score: 95,
      joined_date: '2024-01-15'
    },
    {
      id: '2',
      email: 'sarah.smith@startup.io',
      full_name: 'Sarah Smith',
      avatar_url: null,
      organization_name: 'StartupXYZ',
      plan: 'Starter',
      role: 'Admin',
      status: 'active',
      last_active: '1 day ago',
      articles_generated: 89,
      health_score: 82,
      joined_date: '2024-02-20'
    },
    {
      id: '3',
      email: 'mike.wilson@enterprise.com',
      full_name: 'Mike Wilson',
      avatar_url: null,
      organization_name: 'Enterprise Inc',
      plan: 'Enterprise',
      role: 'Editor',
      status: 'trial',
      last_active: '5 minutes ago',
      articles_generated: 12,
      health_score: 67,
      joined_date: '2024-03-10'
    },
    {
      id: '4',
      email: 'inactive@oldcompany.com',
      full_name: 'Bob Johnson',
      avatar_url: null,
      organization_name: 'Old Company',
      plan: 'Free',
      role: 'Member',
      status: 'inactive',
      last_active: '45 days ago',
      articles_generated: 3,
      health_score: 23,
      joined_date: '2023-11-05'
    }
  ]

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'active':
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Active</Badge>
      case 'trial':
        return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-100">Trial</Badge>
      case 'inactive':
        return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-100">Inactive</Badge>
      case 'suspended':
        return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Suspended</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }

  const getPlanBadge = (plan: string) => {
    switch (plan) {
      case 'Enterprise':
        return <Badge className="bg-purple-100 text-purple-800 hover:bg-purple-100">Enterprise</Badge>
      case 'Professional':
        return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-100">Professional</Badge>
      case 'Starter':
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Starter</Badge>
      case 'Free':
        return <Badge variant="outline">Free</Badge>
      default:
        return <Badge variant="outline">{plan}</Badge>
    }
  }

  const getHealthColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const filteredUsers = mockUsers.filter(user => {
    const matchesSearch = user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         user.full_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         user.organization_name.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesStatus = statusFilter === 'all' || user.status === statusFilter
    const matchesPlan = planFilter === 'all' || user.plan.toLowerCase() === planFilter
    const matchesRole = roleFilter === 'all' || user.role.toLowerCase() === roleFilter
    
    return matchesSearch && matchesStatus && matchesPlan && matchesRole
  })

  return (
    <div className="container mx-auto py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">User Management</h1>
          <p className="text-muted-foreground">
            Manage platform users and their access
          </p>
        </div>
        
        <div className="flex gap-2">
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export Users
          </Button>
          <Button>
            <Users className="h-4 w-4 mr-2" />
            Bulk Actions
          </Button>
        </div>
      </div>

      {/* User Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Users</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.total_users.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">registered users</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Users</CardTitle>
            <UserCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.active_users.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">active (30 days)</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">New Users</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">+{mockStats.new_users_week}</div>
            <p className="text-xs text-muted-foreground">this week</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Inactive Users</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.inactive_users.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">inactive (90+ days)</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Suspended</CardTitle>
            <UserX className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.suspended_users}</div>
            <p className="text-xs text-muted-foreground">suspended accounts</p>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            User Filters & Search
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-[200px]">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search by name, email, or organization..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="trial">Trial</SelectItem>
                <SelectItem value="inactive">Inactive</SelectItem>
                <SelectItem value="suspended">Suspended</SelectItem>
              </SelectContent>
            </Select>

            <Select value={planFilter} onValueChange={setPlanFilter}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="Plan" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Plans</SelectItem>
                <SelectItem value="free">Free</SelectItem>
                <SelectItem value="starter">Starter</SelectItem>
                <SelectItem value="professional">Professional</SelectItem>
                <SelectItem value="enterprise">Enterprise</SelectItem>
              </SelectContent>
            </Select>

            <Select value={roleFilter} onValueChange={setRoleFilter}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="Role" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Roles</SelectItem>
                <SelectItem value="owner">Owner</SelectItem>
                <SelectItem value="admin">Admin</SelectItem>
                <SelectItem value="editor">Editor</SelectItem>
                <SelectItem value="member">Member</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Users Table */}
      <Card>
        <CardHeader>
          <CardTitle>Users ({filteredUsers.length})</CardTitle>
          <CardDescription>
            Complete list of platform users with their details and status
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>User</TableHead>
                <TableHead>Organization</TableHead>
                <TableHead>Plan/Status</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Last Active</TableHead>
                <TableHead>Articles</TableHead>
                <TableHead>Health</TableHead>
                <TableHead className="w-[50px]"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredUsers.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <Avatar className="h-8 w-8">
                        <AvatarImage src={user.avatar_url || ''} />
                        <AvatarFallback>
                          {user.full_name?.split(' ').map(n => n[0]).join('') || user.email[0].toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <div className="font-medium">{user.full_name || 'No name'}</div>
                        <div className="text-sm text-muted-foreground">{user.email}</div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Building className="h-4 w-4 text-muted-foreground" />
                      {user.organization_name}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex flex-col gap-1">
                      {getPlanBadge(user.plan)}
                      {getStatusBadge(user.status)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="flex items-center gap-1 w-fit">
                      <Shield className="h-3 w-3" />
                      {user.role}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Activity className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm">{user.last_active}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="font-mono text-sm">{user.articles_generated}</span>
                  </TableCell>
                  <TableCell>
                    <span className={`font-medium ${getHealthColor(user.health_score)}`}>
                      {user.health_score}/100
                    </span>
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem>View Details</DropdownMenuItem>
                        <DropdownMenuItem>Impersonate User</DropdownMenuItem>
                        <DropdownMenuItem>Reset Password</DropdownMenuItem>
                        <DropdownMenuItem>Update Profile</DropdownMenuItem>
                        <DropdownMenuItem className="text-yellow-600">
                          Suspend Account
                        </DropdownMenuItem>
                        <DropdownMenuItem className="text-red-600">
                          Delete Account
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}