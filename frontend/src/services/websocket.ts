import { getAuthToken } from './auth'

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private listeners: Map<string, Set<Function>> = new Map()
  private pingInterval: number | null = null
  private currentPipelineId: string | null = null

  async connect(pipelineId?: string) {
    const token = await getAuthToken()
    if (!token) {
      console.error('No auth token available for WebSocket connection')
      return null
    }

    // Store pipeline ID for reconnections
    this.currentPipelineId = pipelineId || null

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8088'
    const wsHost = apiUrl.replace(/^https?:\/\//, '')
    
    // Use the correct WebSocket endpoint
    const endpoint = pipelineId 
      ? `/api/v1/ws/pipeline/${pipelineId}?token=${token}`
      : `/api/v1/ws/notifications?token=${token}`
    
    const wsUrl = `${wsProtocol}//${wsHost}${endpoint}`
    
    try {
      this.ws = new WebSocket(wsUrl)

      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0
        this.startPing()
        this.emit('connected', null)
      }

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          
          // Handle different message types from backend
          switch (data.type) {
            case 'pipeline_progress':
              this.emit('pipeline_progress', data.payload)
              break
            case 'agent_status':
              this.emit('agent_status', data.payload)
              break
            case 'article_complete':
              this.emit('article_complete', data.payload)
              break
            case 'error':
              this.emit('error', data.payload)
              break
            case 'pong':
              // Heartbeat response
              break
            default:
              console.warn('Unknown WebSocket message type:', data.type)
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.emit('error', error)
      }

      this.ws.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason)
        this.stopPing()
        this.emit('disconnected', event)
        
        // Attempt reconnection if not manually closed
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++
          setTimeout(() => {
            console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`)
            this.connect(this.currentPipelineId || undefined)
          }, this.reconnectDelay * this.reconnectAttempts)
        }
      }

      return this.ws
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
      this.emit('error', error)
      return null
    }
  }

  disconnect() {
    this.stopPing()
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect')
      this.ws = null
    }
    this.listeners.clear()
    this.currentPipelineId = null
  }

  // Send commands to backend
  send(type: string, payload: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload }))
    } else {
      console.error('WebSocket not connected')
    }
  }

  // Pipeline control commands
  pausePipeline(pipelineId: string) {
    this.send('pause_pipeline', { pipeline_id: pipelineId })
  }

  resumePipeline(pipelineId: string) {
    this.send('resume_pipeline', { pipeline_id: pipelineId })
  }

  cancelPipeline(pipelineId: string) {
    this.send('cancel_pipeline', { pipeline_id: pipelineId })
  }

  // Event handling
  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set())
    }
    this.listeners.get(event)!.add(callback)
  }

  off(event: string, callback: Function) {
    this.listeners.get(event)?.delete(callback)
  }

  private emit(event: string, data: any) {
    this.listeners.get(event)?.forEach(callback => callback(data))
  }

  // Heartbeat to keep connection alive
  private startPing() {
    this.pingInterval = window.setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000) // Ping every 30 seconds
  }

  private stopPing() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval)
      this.pingInterval = null
    }
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }
}

export const wsService = new WebSocketService()
export default wsService
