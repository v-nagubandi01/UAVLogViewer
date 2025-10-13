<template>
  <div class="chat-wrapper">
    <!-- Collapsed AI Chatbot Button -->
    <div
      v-if="!showChat && showCollapsedButton"
      class="collapsed-chat-button"
      @click="expandChat"
      title="Open AI Chatbot"
    >
      <div class="chatbot-icon">🤖</div>
      <span class="chatbot-label">AI Chatbot</span>
    </div>

    <!-- Expanded Chat Interface -->
    <div
      class="chat-interface"
      v-if="showChat"
      :class="{ 'resized': isResized }"
    >
    <div class="chat-container">
      <!-- Chat Header -->
      <div class="chat-header">
        <h4>Chat Assistant</h4>
        <div class="header-buttons">
          <button class="resize-btn" @click="toggleResize" :title="isResized ? 'Make smaller' : 'Make larger'">
            <i :class="isResized ? 'fas fa-compress' : 'fas fa-expand'"></i>
          </button>
          <button class="close-btn" @click="collapseChat" title="Close Chat">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>

      <!-- Chat Messages Area -->
      <div class="chat-messages" ref="chatMessages">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['message', message.type]"
        >
          <div class="message-content" v-html="formatMessage(message.text)"></div>
          <div class="message-time">
            {{ formatTime(message.timestamp) }}
          </div>
        </div>

        <!-- Backend processing message -->
        <div v-if="showChat && !isBackendProcessingComplete" class="message bot processing-message">
          <div class="message-content">
            <div class="processing-container">
              <div class="processing-indicator">
                <i class="fas fa-spinner fa-spin"></i>
              </div>
              <div class="processing-text">
                <strong>Backend Processing</strong><br>
                The chatbot is currently unavailable while your file is being processed. Please wait...
              </div>
            </div>
          </div>
        </div>

        <!-- Loading indicator -->
        <div v-if="isTyping" class="message bot loading-message">
          <div class="message-content">
            <div class="loading-container">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span class="loading-text">Assistant is thinking...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Input Area -->
      <div class="chat-input-area" :class="{ 'disabled': !isChatAvailable }">
        <div class="input-group">
          <input
            v-model="newMessage"
            @keyup.enter="sendMessage"
            type="text"
            :placeholder="isChatAvailable ? 'Type your message...' : 'Chat unavailable - processing file...'"
            class="chat-input"
            :disabled="isTyping || !isChatAvailable"
          />
          <button
            @click="sendMessage"
            :disabled="!newMessage.trim() || isTyping || !isChatAvailable"
            class="send-btn"
            :class="{ 'loading': isTyping, 'disabled': !isChatAvailable }"
          >
            <i v-if="!isTyping" class="fas fa-paper-plane"></i>
            <i v-else class="fas fa-spinner fa-spin"></i>
          </button>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'

export default {
    name: 'ChatInterface',
    data () {
        return {
            messages: [],
            newMessage: '',
            isTyping: false,
            messageId: 0,
            isResized: false,
            eventSource: null,
            currentBotMessage: null
        }
    },
    computed: {
        showChat () {
            return this.$parent.state &&
                   this.$parent.state.processDone &&
                   this.$parent.state.showChat &&
                   this.$parent.state.logType === 'bin'
        },
        showCollapsedButton () {
            return this.$parent.state &&
                   this.$parent.state.processDone &&
                   this.$parent.state.logType === 'bin'
        },
        isBackendProcessingComplete () {
            return this.$parent.state && this.$parent.state.backendProcessingComplete
        },
        isChatAvailable () {
            return this.showChat && this.isBackendProcessingComplete
        }
    },
    methods: {
        async sendMessage () {
            if (!this.newMessage.trim() || this.isTyping || !this.isChatAvailable) {
                return
            }

            const userMessage = {
                id: this.messageId++,
                text: this.newMessage.trim(),
                type: 'user',
                timestamp: new Date()
            }

            this.messages.push(userMessage)
            const messageText = this.newMessage.trim()
            this.newMessage = ''
            this.scrollToBottom()

            // Show loading indicator
            this.isTyping = true

            // Initialize bot message that we'll update as chunks arrive
            this.currentBotMessage = {
                id: this.messageId++,
                text: '',
                type: 'bot',
                timestamp: new Date()
            }
            this.messages.push(this.currentBotMessage)

            try {
                // Make POST request to get SSE stream
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: messageText,
                        conversationId: this.$parent.state.conversationId
                    })
                })

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                }

                // Read the stream
                const reader = response.body.getReader()
                const decoder = new TextDecoder()

                while (true) {
                    const { done, value } = await reader.read()
                    
                    if (done) {
                        break
                    }

                    // Decode the chunk
                    const chunk = decoder.decode(value, { stream: true })
                    
                    // Process SSE messages
                    const lines = chunk.split('\n')
                    let eventType = null
                    
                    for (const line of lines) {
                        if (line.startsWith('event:')) {
                            eventType = line.substring(6).trim()
                        } else if (line.startsWith('data:')) {
                            const dataStr = line.substring(5).trim()
                            
                            try {
                                const data = JSON.parse(dataStr)
                                
                                if (eventType === 'message') {
                                    // Update the current bot message with the content
                                    this.currentBotMessage.text = data.content
                                    this.scrollToBottom()
                                } else if (eventType === 'processing') {
                                    // Optional: show processing status
                                    console.log('Processing:', data.content)
                                } else if (eventType === 'complete') {
                                    // Stream completed successfully
                                    console.log('Stream completed')
                                } else if (eventType === 'error') {
                                    // Handle error
                                    this.currentBotMessage.text = `**Error:** ${data.content}`
                                    this.scrollToBottom()
                                } else if (eventType === 'cancelled') {
                                    // Handle cancellation
                                    this.currentBotMessage.text = `**Cancelled:** ${data.content}`
                                    this.scrollToBottom()
                                }
                            } catch (e) {
                                console.error('Error parsing SSE data:', e)
                            }
                            
                            eventType = null
                        }
                    }
                }

            } catch (error) {
                console.error('Error sending message:', error)
                let errorText = ''

                if (error.name === 'AbortError') {
                    errorText = '**Timeout Error:** The request took too long to respond.'
                } else if (error.message.includes('Failed to fetch')) {
                    errorText = 'Cannot connect to the backend server. Check what port the backend is on.'
                } else {
                    errorText = `I got an error while processing your message.\n\n**Details:** ${error.message}\n\n`
                }

                // Update current bot message with error
                if (this.currentBotMessage) {
                    this.currentBotMessage.text = errorText
                } else {
                    const errorMessage = {
                        id: this.messageId++,
                        text: errorText,
                        type: 'bot',
                        timestamp: new Date()
                    }
                    this.messages.push(errorMessage)
                }
            } finally {
                this.isTyping = false
                this.currentBotMessage = null
                this.scrollToBottom()
            }
        },

        scrollToBottom () {
            this.$nextTick(() => {
                const chatMessages = this.$refs.chatMessages
                if (chatMessages) {
                    chatMessages.scrollTop = chatMessages.scrollHeight
                }
            })
        },

        formatTime (timestamp) {
            return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },

        formatMessage (text) {
            // Configure marked options for security and styling
            marked.setOptions({
                breaks: true,
                gfm: true,
                sanitize: false, // We'll handle sanitization if needed
                smartLists: true,
                smartypants: true
            })

            // Convert markdown to HTML
            return marked.parse(text)
        },

        toggleChat () {
            // This will be handled by the parent component
            this.$emit('toggle-chat')
        },

        toggleResize () {
            this.isResized = !this.isResized
        },

        collapseChat () {
            // Emit event to parent to hide the chat
            this.$emit('toggle-chat')
        },

        expandChat () {
            // Emit event to parent to show the chat
            this.$emit('toggle-chat')
        }
    },
    mounted () {
        // Add welcome message when chat becomes available
        this.$watch('isChatAvailable', (newValue) => {
            if (newValue && this.messages.length === 0) {
                const welcomeMessage = {
                    id: this.messageId++,
                    text: 'Hello! I\'m your UAV log analysis assistant. How can I help you today?',
                    type: 'bot',
                    timestamp: new Date()
                }
                this.messages.push(welcomeMessage)
            }
        }, { immediate: true })
    },
    beforeUnmount () {
        // Cleanup any active connections when component is destroyed
        if (this.eventSource) {
            this.eventSource.close()
            this.eventSource = null
        }
    }
}
</script>

<style scoped>
/* Chat Wrapper */
.chat-wrapper {
  position: relative;
}

/* Collapsed AI Chatbot Button */
.collapsed-chat-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 20px;
  border-radius: 25px;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 1000;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 14px;
}

.collapsed-chat-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.chatbot-icon {
  font-size: 18px;
}

.chatbot-label {
  white-space: nowrap;
}

/* Expanded Chat Interface */
.chat-interface {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 350px;
  height: 650px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s ease;
}

.chat-interface.resized {
  width: 500px;
  height: 750px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.header-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.resize-btn, .close-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.2s;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resize-btn:hover, .close-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.resize-btn i, .close-btn i {
  font-size: 14px;
}

.chat-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
}

.message.bot {
  align-self: flex-start;
}

.message-content {
  padding: 10px 15px;
  border-radius: 18px;
  word-wrap: break-word;
  font-size: 14px;
  line-height: 1.4;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.bot .message-content {
  background: white;
  color: #333;
  border: 1px solid #e1e5e9;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-time {
  font-size: 11px;
  color: #999;
  margin-top: 4px;
  padding: 0 5px;
}

.message.user .message-time {
  text-align: right;
}

.message.bot .message-time {
  text-align: left;
}

/* Loading indicator styles */
.loading-message .message-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.loading-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #667eea;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.loading-text {
  font-style: italic;
  color: #666;
  font-size: 13px;
}

/* Processing message styles */
.processing-message .message-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.processing-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.processing-indicator {
  color: #667eea;
  font-size: 16px;
}

.processing-text {
  color: #666;
  font-size: 13px;
  line-height: 1.4;
}

/* Markdown content styles */
.message-content h1,
.message-content h2,
.message-content h3,
.message-content h4,
.message-content h5,
.message-content h6 {
  margin: 8px 0 4px 0;
  font-weight: 600;
  color: inherit;
}

.message-content h1 { font-size: 1.2em; }
.message-content h2 { font-size: 1.1em; }
.message-content h3 { font-size: 1.05em; }

.message-content p {
  margin: 4px 0;
  line-height: 1.4;
}

.message-content ul,
.message-content ol {
  margin: 4px 0;
  padding-left: 20px;
}

.message-content li {
  margin: 2px 0;
}

.message-content code {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.message-content pre {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 8px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 4px 0;
}

.message-content pre code {
  background: none;
  padding: 0;
}

.message-content blockquote {
  border-left: 3px solid #667eea;
  margin: 4px 0;
  padding-left: 12px;
  color: #666;
  font-style: italic;
}

.message-content a {
  color: #667eea;
  text-decoration: none;
}

.message-content a:hover {
  text-decoration: underline;
}

.message-content strong {
  font-weight: 600;
}

.message-content em {
  font-style: italic;
}

.chat-input-area {
  padding: 15px;
  background: white;
  border-top: 1px solid #e1e5e9;
}

.chat-input-area.disabled {
  background: #f8f9fa;
  opacity: 0.7;
}

.input-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.chat-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #e1e5e9;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.chat-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.chat-input:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.send-btn {
  width: 45px;
  height: 45px;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.send-btn:disabled {
  background: #e1e5e9;
  color: #6c757d;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.send-btn.loading {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  cursor: not-allowed;
}

.send-btn.loading:hover {
  transform: none;
  box-shadow: none;
}

.send-btn.disabled {
  background: #e1e5e9;
  color: #6c757d;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.send-btn.disabled:hover {
  transform: none;
  box-shadow: none;
}

/* Responsive design */
@media (max-width: 768px) {
  .collapsed-chat-button {
    bottom: 10px;
    right: 10px;
    padding: 10px 16px;
    font-size: 13px;
  }

  .chat-interface {
    width: calc(100vw - 40px);
    height: 500px;
    bottom: 10px;
    right: 10px;
    left: 10px;
  }

  .chat-interface.resized {
    width: calc(100vw - 20px);
    height: 600px;
    left: 10px;
  }
}
</style>
