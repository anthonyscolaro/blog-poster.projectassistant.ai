import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Search } from 'lucide-react'

interface ArticleSearchProps {
  onSearch: (value: string) => void
}

export function ArticleSearch({ onSearch }: ArticleSearchProps) {
  const [value, setValue] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value
    setValue(newValue)
    onSearch(newValue)
  }

  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <Input
        placeholder="Search articles..."
        value={value}
        onChange={handleChange}
        className="pl-10"
      />
    </div>
  )
}