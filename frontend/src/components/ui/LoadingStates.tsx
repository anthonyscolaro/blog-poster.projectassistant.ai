import React from 'react'
import { cn } from '@/lib/utils'

// Generic Skeleton Component
interface SkeletonProps {
  className?: string
  width?: string | number
  height?: string | number
  rounded?: boolean
  animate?: boolean
}

export function Skeleton({ 
  className, 
  width, 
  height, 
  rounded = true, 
  animate = true 
}: SkeletonProps) {
  return (
    <div
      className={cn(
        'bg-muted',
        rounded && 'rounded',
        animate && 'animate-pulse',
        className
      )}
      style={{ width, height }}
    />
  )
}

// Content Skeleton for text-heavy content
export function ContentSkeleton({ lines = 3 }: { lines?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="animate-pulse">
          <div 
            className={cn(
              "h-4 bg-muted rounded",
              i === 0 && "w-3/4",
              i === 1 && "w-1/2", 
              i === lines - 1 && "w-5/6",
              i > 1 && i < lines - 1 && "w-4/5"
            )}
          />
        </div>
      ))}
    </div>
  )
}

// Table Skeleton for data tables
export function TableSkeleton({ rows = 5, columns = 4 }: { rows?: number; columns?: number }) {
  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex gap-4">
        {Array.from({ length: columns }).map((_, i) => (
          <div key={i} className="flex-1">
            <Skeleton className="h-4 w-3/4" />
          </div>
        ))}
      </div>
      
      {/* Rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          {Array.from({ length: columns }).map((_, j) => (
            <div key={j} className="flex-1">
              <Skeleton className={cn(
                "h-10",
                j === 0 && "w-full",
                j === columns - 1 && "w-24",
                j > 0 && j < columns - 1 && "w-32"
              )} />
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

// Card Grid Skeleton for dashboard cards
export function CardGridSkeleton({ cards = 4, columns = 4 }: { cards?: number; columns?: number }) {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
  }[columns] || 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'

  return (
    <div className={cn("grid gap-6", gridCols)}>
      {Array.from({ length: cards }).map((_, i) => (
        <div key={i} className="bg-card border border-border rounded-lg p-6">
          <div className="animate-pulse space-y-4">
            <div className="flex items-center gap-3">
              <Skeleton className="h-8 w-8 rounded-lg" />
              <div className="space-y-2 flex-1">
                <Skeleton className="h-4 w-1/2" />
                <Skeleton className="h-3 w-1/3" />
              </div>
            </div>
            <Skeleton className="h-8 w-3/4" />
          </div>
        </div>
      ))}
    </div>
  )
}

// List Skeleton for article lists, team members, etc.
export function ListSkeleton({ items = 5 }: { items?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: items }).map((_, i) => (
        <div key={i} className="flex items-center gap-4 p-4 border border-border rounded-lg">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="flex-1 space-y-2">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-3 w-1/2" />
          </div>
          <Skeleton className="h-8 w-20" />
        </div>
      ))}
    </div>
  )
}

// Chart Skeleton for analytics
export function ChartSkeleton({ height = "h-64" }: { height?: string }) {
  return (
    <div className={cn("bg-card border border-border rounded-lg p-6", height)}>
      <div className="animate-pulse space-y-4">
        <div className="flex justify-between items-center">
          <Skeleton className="h-6 w-1/3" />
          <Skeleton className="h-4 w-16" />
        </div>
        <div className="flex items-end justify-between h-32 gap-2">
          {Array.from({ length: 7 }).map((_, i) => (
            <Skeleton 
              key={i} 
              className={cn(
                "w-8 rounded-t",
                i % 3 === 0 && "h-24",
                i % 3 === 1 && "h-16", 
                i % 3 === 2 && "h-20"
              )}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

// Form Skeleton for settings pages
export function FormSkeleton({ fields = 5 }: { fields?: number }) {
  return (
    <div className="space-y-6">
      {Array.from({ length: fields }).map((_, i) => (
        <div key={i} className="space-y-2">
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-10 w-full" />
        </div>
      ))}
      <div className="flex gap-3 pt-4">
        <Skeleton className="h-10 w-24" />
        <Skeleton className="h-10 w-20" />
      </div>
    </div>
  )
}

// Page Skeleton for full page loading
export function PageSkeleton() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <Skeleton className="h-8 w-1/3" />
        <Skeleton className="h-4 w-1/2" />
      </div>
      
      {/* Stats Cards */}
      <CardGridSkeleton cards={4} />
      
      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <ChartSkeleton />
          <TableSkeleton rows={6} />
        </div>
        <div className="space-y-6">
          <ListSkeleton items={4} />
        </div>
      </div>
    </div>
  )
}