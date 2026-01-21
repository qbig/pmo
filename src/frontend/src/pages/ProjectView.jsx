import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api'

function ProjectView() {
  const { projectId } = useParams()
  const [project, setProject] = useState(null)
  const [summary, setSummary] = useState(null)
  const [drift, setDrift] = useState(null)
  const [forecast, setForecast] = useState(null)
  const [loading, setLoading] = useState(true)
  const [summaryLoading, setSummaryLoading] = useState(false)
  const [forecastLoading, setForecastLoading] = useState(false)

  useEffect(() => {
    loadProject()
  }, [projectId])

  const loadProject = async () => {
    try {
      const res = await api.getFile(projectId)
      setProject(res.data)
    } catch (error) {
      console.error('Error loading project:', error)
    } finally {
      setLoading(false)
    }
  }

  const generateSummary = async () => {
    setSummaryLoading(true)
    try {
      const res = await api.getProjectSummary(projectId)
      setSummary(res.data.summary)
    } catch (error) {
      console.error('Error generating summary:', error)
    } finally {
      setSummaryLoading(false)
    }
  }

  const checkDrift = async () => {
    try {
      const res = await api.detectDrift(projectId)
      setDrift(res.data)
    } catch (error) {
      console.error('Error checking drift:', error)
    }
  }

  const generateForecast = async () => {
    setForecastLoading(true)
    try {
      const res = await api.forecastBlockers(projectId)
      setForecast(res.data)
    } catch (error) {
      console.error('Error generating forecast:', error)
    } finally {
      setForecastLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  if (!project) {
    return <div className="text-center py-12">Project not found</div>
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-6">
        <Link to="/" className="text-sm text-gray-500 hover:text-gray-700">← Back to Dashboard</Link>
        <h2 className="text-2xl font-bold text-gray-900 mt-2">{project.title}</h2>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Project Content */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Project Details</h3>
              <Link
                to={`/file/${projectId}`}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                Edit
              </Link>
            </div>
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap text-sm">{project.content}</pre>
            </div>
          </div>
        </div>

        {/* AI Summary */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">AI Summary</h3>
              <button
                onClick={generateSummary}
                disabled={summaryLoading}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {summaryLoading ? 'Generating...' : 'Generate'}
              </button>
            </div>
            {summary ? (
              <div className="prose max-w-none text-sm">
                <div className="whitespace-pre-wrap">{summary}</div>
              </div>
            ) : (
              <p className="text-sm text-gray-500">Click "Generate" to create an executive summary</p>
            )}
          </div>
        </div>

        {/* Drift Detection */}
        <div className="bg-white shadow rounded-lg lg:col-span-2">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Drift Detection</h3>
              <button
                onClick={checkDrift}
                className="px-3 py-1 text-sm bg-yellow-600 text-white rounded hover:bg-yellow-700"
              >
                Check
              </button>
            </div>
            {drift && drift.issues && drift.issues.length > 0 ? (
              <div className="space-y-2">
                {drift.issues.map((issue, idx) => (
                  <div key={idx} className="p-3 border border-yellow-200 bg-yellow-50 rounded">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-yellow-800">{issue.type}</span>
                      <span className={`px-2 py-1 text-xs rounded ${
                        issue.severity === 'high' ? 'bg-red-100 text-red-800' :
                        issue.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {issue.severity}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 mt-1">{issue.description}</p>
                    <p className="text-xs text-gray-600 mt-1">Recommendation: {issue.recommendation}</p>
                  </div>
                ))}
              </div>
            ) : drift ? (
              <p className="text-sm text-green-600">No issues detected</p>
            ) : (
              <p className="text-sm text-gray-500">Click "Check" to analyze project health</p>
            )}
          </div>
        </div>

        {/* Forecasting */}
        <div className="bg-white shadow rounded-lg lg:col-span-2">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Forecast & Blockers</h3>
              <button
                onClick={generateForecast}
                disabled={forecastLoading}
                className="px-3 py-1 text-sm bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50"
              >
                {forecastLoading ? 'Analyzing...' : 'Forecast'}
              </button>
            </div>
            {forecast ? (
              <div className="space-y-4">
                {/* Forecast Probabilities */}
                {forecast.forecast && (
                  <div className="p-4 bg-gray-50 rounded">
                    <h4 className="text-sm font-medium text-gray-900 mb-3">Delivery Forecast</h4>
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <div className="text-xs text-gray-600 mb-1">On Time</div>
                        <div className="text-lg font-semibold text-green-600">
                          {(forecast.forecast.on_time_probability * 100).toFixed(0)}%
                        </div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">At Risk</div>
                        <div className="text-lg font-semibold text-yellow-600">
                          {(forecast.forecast.at_risk_probability * 100).toFixed(0)}%
                        </div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">Delayed</div>
                        <div className="text-lg font-semibold text-red-600">
                          {(forecast.forecast.delayed_probability * 100).toFixed(0)}%
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Blockers */}
                {forecast.blockers && forecast.blockers.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-3">Top Blockers</h4>
                    <div className="space-y-2">
                      {forecast.blockers.map((blocker, idx) => (
                        <div key={idx} className="p-3 border border-gray-200 rounded">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-900">{blocker.id}</span>
                            <div className="flex space-x-2">
                              <span className={`px-2 py-1 text-xs rounded ${
                                blocker.impact === 'high' ? 'bg-red-100 text-red-800' :
                                blocker.impact === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {blocker.impact}
                              </span>
                              <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded">
                                {(blocker.delay_probability * 100).toFixed(0)}% delay risk
                              </span>
                            </div>
                          </div>
                          <p className="text-sm text-gray-700">{blocker.description}</p>
                          {blocker.estimated_delay_days && (
                            <p className="text-xs text-gray-600 mt-1">
                              Estimated delay: {blocker.estimated_delay_days} days
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Critical Path */}
                {forecast.critical_path && forecast.critical_path.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Critical Path</h4>
                    <div className="flex flex-wrap gap-2">
                      {forecast.critical_path.map((item, idx) => (
                        <span key={idx} className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-sm text-gray-500">Click "Forecast" to analyze potential blockers and delays</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProjectView
