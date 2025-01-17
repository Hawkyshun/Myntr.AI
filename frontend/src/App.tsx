import { useState } from 'react'
import { QuestionMarkCircleIcon, ChartBarIcon, CurrencyDollarIcon } from '@heroicons/react/24/outline'
import axios from 'axios'

interface FinancialAdvice {
  answer: string;
  recommendations: string[];
  additional_info?: {
    risk_level?: string;
    suggested_allocation?: {
      [key: string]: string;
    };
  };
}

function App() {
  const [question, setQuestion] = useState('')
  const [riskTolerance, setRiskTolerance] = useState('medium')
  const [advice, setAdvice] = useState<FinancialAdvice | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        question,
        risk_tolerance: riskTolerance
      })
      setAdvice(response.data)
    } catch (error) {
      console.error('Error:', error)
      alert('Bir hata oluştu. Lütfen tekrar deneyin.')
    }

    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">Finansal Danışman</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="question" className="block text-sm font-medium text-gray-700">
                  Finansal Sorunuz
                </label>
                <div className="mt-1">
                  <textarea
                    id="question"
                    name="question"
                    rows={3}
                    className="input"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Örnek: Risk toleransı düşük biri için hangi yatırım araçları uygundur?"
                    required
                  />
                </div>
              </div>

              <div>
                <label htmlFor="risk" className="block text-sm font-medium text-gray-700">
                  Risk Toleransı
                </label>
                <select
                  id="risk"
                  name="risk"
                  className="mt-1 input"
                  value={riskTolerance}
                  onChange={(e) => setRiskTolerance(e.target.value)}
                >
                  <option value="low">Düşük</option>
                  <option value="medium">Orta</option>
                  <option value="high">Yüksek</option>
                </select>
              </div>

              <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={loading}
              >
                {loading ? 'Analiz ediliyor...' : 'Analiz Et'}
              </button>
            </form>

            {advice && (
              <div className="mt-8 space-y-6">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex items-start">
                    <QuestionMarkCircleIcon className="h-6 w-6 text-primary-600 mt-1" />
                    <div className="ml-3">
                      <h3 className="text-lg font-medium text-gray-900">Cevap</h3>
                      <p className="mt-2 text-gray-600">{advice.answer}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex items-start">
                    <ChartBarIcon className="h-6 w-6 text-primary-600 mt-1" />
                    <div className="ml-3">
                      <h3 className="text-lg font-medium text-gray-900">Öneriler</h3>
                      <ul className="mt-2 space-y-2">
                        {advice.recommendations.map((rec, index) => (
                          <li key={index} className="text-gray-600">• {rec}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>

                {advice.additional_info?.suggested_allocation && (
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-start">
                      <CurrencyDollarIcon className="h-6 w-6 text-primary-600 mt-1" />
                      <div className="ml-3">
                        <h3 className="text-lg font-medium text-gray-900">Önerilen Dağılım</h3>
                        <div className="mt-2 grid grid-cols-2 gap-4">
                          {Object.entries(advice.additional_info.suggested_allocation).map(([key, value]) => (
                            <div key={key} className="flex justify-between">
                              <span className="text-gray-600 capitalize">{key}</span>
                              <span className="font-medium text-gray-900">{value}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App 