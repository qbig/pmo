import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'

function MeetingIngest() {
  const navigate = useNavigate()
  const [notes, setNotes] = useState('')
  const [projectId, setProjectId] = useState('')
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [applying, setApplying] = useState(false)

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      const res = await api.listProjects()
      setProjects(res.data.projects || [])
    } catch (error) {
      console.error('Error loading projects:', error)
    }
  }

  const handleIngest = async () => {
    if (!notes.trim()) {
      alert('Please enter meeting notes')
      return
    }

    setLoading(true)
    setResult(null)
    try {
      const res = await api.ingestMeeting(notes, projectId || null)
      setResult(res.data)
    } catch (error) {
      console.error('Error ingesting meeting:', error)
      alert('Error processing meeting notes')
    } finally {
      setLoading(false)
    }
  }

  const applyResults = async () => {
    if (!result) return

    setApplying(true)
    try {
      // Create risk files
      for (const risk of result.risks || []) {
        // In a real implementation, we'd create the file via API
        // For now, we'll show what would be created
        console.log('Would create risk:', risk)
      }

      // Create decision files
      for (const decision of result.decisions || []) {
        console.log('Would create decision:', decision)
      }

      alert('Results processed. Files would be created in workspace.')
      setResult(null)
      setNotes('')
    } catch (error) {
      console.error('Error applying results:', error)
      alert('Error applying results')
    } finally {
      setApplying(false)
    }
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Meeting Notes Ingestion</h2>
        <p className="mt-1 text-sm text-gray-500">Extract structured information from meeting notes</p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Project Context (Optional)
            </label>
            <select
              value={projectId}
              onChange={(e) => setProjectId(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">None</option>
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.title}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Meeting Notes
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={15}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
              placeholder="Paste meeting notes here..."
            />
          </div>

          <button
            onClick={handleIngest}
            disabled={loading || !notes.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Extract Information'}
          </button>
        </div>
      </div>

      {result && (
        <div className="mt-6 space-y-4">
          {/* Risks */}
          {result.risks && result.risks.length > 0 && (
            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-3 border-b">
                <h3 className="text-lg font-medium text-gray-900">Risks Identified</h3>
              </div>
              <div className="px-4 py-4 space-y-3">
                {result.risks.map((risk, idx) => (
                  <div key={idx} className="p-3 border border-gray-200 rounded">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-900">{risk.title}</h4>
                      <div className="flex space-x-2">
                        <span className={`px-2 py-1 text-xs rounded ${
                          risk.severity === 'critical' ? 'bg-red-100 text-red-800' :
                          risk.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                          risk.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {risk.severity}
                        </span>
                        <span className={`px-2 py-1 text-xs rounded ${
                          risk.probability === 'high' ? 'bg-red-100 text-red-800' :
                          risk.probability === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {risk.probability}
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-700">{risk.description}</p>
                    <p className="text-xs text-gray-600 mt-1">Impact: {risk.impact}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Decisions */}
          {result.decisions && result.decisions.length > 0 && (
            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-3 border-b">
                <h3 className="text-lg font-medium text-gray-900">Decisions Made</h3>
              </div>
              <div className="px-4 py-4 space-y-3">
                {result.decisions.map((decision, idx) => (
                  <div key={idx} className="p-3 border border-gray-200 rounded">
                    <h4 className="font-medium text-gray-900 mb-2">{decision.title}</h4>
                    <p className="text-sm text-gray-700 mb-2"><strong>Context:</strong> {decision.context}</p>
                    <p className="text-sm text-gray-700 mb-2"><strong>Decision:</strong> {decision.decision}</p>
                    {decision.consequences && decision.consequences.length > 0 && (
                      <div className="mt-2">
                        <p className="text-xs font-medium text-gray-600 mb-1">Consequences:</p>
                        <ul className="list-disc list-inside text-xs text-gray-600 space-y-1">
                          {decision.consequences.map((cons, i) => (
                            <li key={i}>{cons}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Status Updates */}
          {result.status_updates && (
            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-3 border-b">
                <h3 className="text-lg font-medium text-gray-900">Status Updates</h3>
              </div>
              <div className="px-4 py-4">
                {result.status_updates.progress && (
                  <div className="mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-1">Progress:</p>
                    <p className="text-sm text-gray-600">{result.status_updates.progress}</p>
                  </div>
                )}
                {result.status_updates.milestones && result.status_updates.milestones.length > 0 && (
                  <div className="mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-1">Milestones:</p>
                    <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                      {result.status_updates.milestones.map((milestone, i) => (
                        <li key={i}>{milestone}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {result.status_updates.blockers && result.status_updates.blockers.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-1">Blockers:</p>
                    <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                      {result.status_updates.blockers.map((blocker, i) => (
                        <li key={i}>{blocker}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Action Items */}
          {result.action_items && result.action_items.length > 0 && (
            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-3 border-b">
                <h3 className="text-lg font-medium text-gray-900">Action Items</h3>
              </div>
              <div className="px-4 py-4">
                <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                  {result.action_items.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          <div className="flex justify-end">
            <button
              onClick={applyResults}
              disabled={applying}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
            >
              {applying ? 'Applying...' : 'Apply Results'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default MeetingIngest
