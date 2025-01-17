import React, { useState, useRef, useEffect } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/solid'
import { SparklesIcon, ChatBubbleLeftIcon, CurrencyDollarIcon } from '@heroicons/react/24/outline'
import axios from 'axios'

function App() {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: 'Merhaba! Ben sizin finansal danışmanınızım. Size nasıl yardımcı olabilirim?'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const analyzeRiskTolerance = (message) => {
    const lowRiskKeywords = ['düşük', 'güvenli', 'risk sevmem', 'temkinli']
    const highRiskKeywords = ['yüksek', 'agresif', 'risk alabilirim', 'cesur']
    
    const messageLower = message.toLowerCase()
    
    for (const keyword of lowRiskKeywords) {
      if (messageLower.includes(keyword)) return 'low'
    }
    
    for (const keyword of highRiskKeywords) {
      if (messageLower.includes(keyword)) return 'high'
    }
    
    return 'medium'
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = input
    setInput('')
    setLoading(true)

    setMessages(prev => [...prev, { type: 'user', content: userMessage }])

    try {
      const riskTolerance = analyzeRiskTolerance(userMessage)
      
      const response = await axios.post('http://localhost:8000/analyze', {
        question: userMessage,
        risk_tolerance: riskTolerance
      })

      setMessages(prev => [
        ...prev,
        { type: 'bot', content: response.data.answer },
        { 
          type: 'bot', 
          content: 'Önerilerim:',
          recommendations: response.data.recommendations 
        }
      ])

      if (response.data.additional_info?.suggested_allocation) {
        setMessages(prev => [
          ...prev,
          {
            type: 'bot',
            content: 'Önerilen Portföy Dağılımı:',
            allocation: response.data.additional_info.suggested_allocation
          }
        ])
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, {
        type: 'bot',
        content: 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.'
      }])
    }

    setLoading(false)
  }

  const quickPrompts = [
    {
      icon: <SparklesIcon className="h-5 w-5" />,
      text: "Yatırım tavsiyeleri"
    },
    {
      icon: <ChatBubbleLeftIcon className="h-5 w-5" />,
      text: "Borç yönetimi"
    },
    {
      icon: <CurrencyDollarIcon className="h-5 w-5" />,
      text: "Emeklilik planlaması"
    }
  ]

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="max-w-2xl mx-auto h-screen flex flex-col">
        {/* Header */}
        <header className="p-4 border-b border-gray-800">
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <SparklesIcon className="h-8 w-8 text-primary-500" />
            Finansal Danışman
          </h1>
          <p className="text-gray-400 mt-1">Akıllı finansal rehberiniz</p>
        </header>

        {/* Main Chat Area */}
        <main className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Quick Prompts */}
          {messages.length === 1 && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              {quickPrompts.map((prompt, index) => (
                <button
                  key={index}
                  onClick={() => setInput(prompt.text)}
                  className="flex items-center gap-3 p-4 rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors"
                >
                  <div className="p-2 rounded-lg bg-gray-700">
                    {prompt.icon}
                  </div>
                  <span className="text-sm font-medium">{prompt.text}</span>
                </button>
              ))}
            </div>
          )}

          {/* Messages */}
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`rounded-2xl px-4 py-3 max-w-[80%] ${
                  message.type === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-800'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                {message.recommendations && (
                  <ul className="mt-3 space-y-2">
                    {message.recommendations.map((rec, idx) => (
                      <li key={idx} className="text-sm flex items-start gap-2">
                        <span className="text-primary-400">•</span>
                        <span className="text-gray-300">{rec}</span>
                      </li>
                    ))}
                  </ul>
                )}
                {message.allocation && (
                  <div className="mt-3 space-y-2 bg-gray-700/50 rounded-lg p-3">
                    {Object.entries(message.allocation).map(([key, value], idx) => (
                      <div key={idx} className="flex justify-between text-sm">
                        <span className="text-gray-400 capitalize">{key}:</span>
                        <span className="text-primary-400 font-medium">{value}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </main>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-800">
          <form onSubmit={handleSubmit} className="flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Finansal sorunuzu yazın..."
              className="flex-1 bg-gray-800 text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="p-3 rounded-xl bg-primary-600 hover:bg-primary-700 transition-colors disabled:opacity-50"
            >
              <PaperAirplaneIcon className="h-5 w-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default App
