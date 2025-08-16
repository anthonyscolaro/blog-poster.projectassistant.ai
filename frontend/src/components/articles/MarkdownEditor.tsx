import { useState } from 'react'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { 
  Bold, 
  Italic, 
  Link, 
  List, 
  ListOrdered, 
  Quote,
  Heading2,
  Heading3,
  Eye,
  Code
} from 'lucide-react'

interface MarkdownEditorProps {
  content: string
  onChange: (content: string) => void
}

export function MarkdownEditor({ content, onChange }: MarkdownEditorProps) {
  const [showPreview, setShowPreview] = useState(false)

  const insertMarkdown = (before: string, after: string = '') => {
    const textarea = document.querySelector('textarea') as HTMLTextAreaElement
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const selectedText = content.substring(start, end)
    
    const newContent = 
      content.substring(0, start) + 
      before + selectedText + after + 
      content.substring(end)
    
    onChange(newContent)
    
    // Set cursor position after insertion
    setTimeout(() => {
      textarea.focus()
      textarea.setSelectionRange(start + before.length, start + before.length + selectedText.length)
    }, 0)
  }

  const formatContent = (text: string) => {
    // Simple markdown to HTML conversion for preview
    return text
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*(.*)\*/gim, '<em>$1</em>')
      .replace(/\[([^\]]*)\]\(([^\)]*)\)/gim, '<a href="$2">$1</a>')
      .replace(/\n/gim, '<br>')
  }

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex items-center gap-2 p-2 border border-border rounded-lg bg-background">
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('**', '**')}
          title="Bold"
        >
          <Bold className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('*', '*')}
          title="Italic"
        >
          <Italic className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('## ')}
          title="Heading 2"
        >
          <Heading2 className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('### ')}
          title="Heading 3"
        >
          <Heading3 className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('[', '](url)')}
          title="Link"
        >
          <Link className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('- ')}
          title="Bullet List"
        >
          <List className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('1. ')}
          title="Numbered List"
        >
          <ListOrdered className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('> ')}
          title="Quote"
        >
          <Quote className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => insertMarkdown('`', '`')}
          title="Inline Code"
        >
          <Code className="h-4 w-4" />
        </Button>
        
        <div className="ml-auto">
          <Button
            size="sm"
            variant={showPreview ? "default" : "ghost"}
            onClick={() => setShowPreview(!showPreview)}
          >
            <Eye className="h-4 w-4 mr-2" />
            Preview
          </Button>
        </div>
      </div>

      {/* Editor */}
      <div className="grid grid-cols-1 gap-4" style={{ gridTemplateColumns: showPreview ? '1fr 1fr' : '1fr' }}>
        <div>
          <Textarea
            value={content}
            onChange={(e) => onChange(e.target.value)}
            placeholder="Write your article content in Markdown..."
            className="min-h-[500px] font-mono text-sm"
          />
        </div>
        
        {showPreview && (
          <div className="border border-border rounded-lg p-4 bg-background">
            <h4 className="text-sm font-medium text-muted-foreground mb-3">Preview</h4>
            <div 
              className="prose prose-sm max-w-none dark:prose-invert"
              dangerouslySetInnerHTML={{ __html: formatContent(content) }}
            />
          </div>
        )}
      </div>
    </div>
  )
}