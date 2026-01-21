import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

function AIInbox() {
  const [projects, setProjects] = useState([])
  const [selectedProject, setSelectedProject] = useState(null)
  const [driftIssues, setDriftIssues] = useState([])
  const [loading, setLoading] = useState(false)

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

  const checkAllProjects = async () => {
    setLoading(true)
    setDriftIssues([])
    try {
      const issues = []
      for (const project of projects) {
        try {
          const res = await api.detectDrift(project.id)
          if (res.data.issues && res.data.issues.length > 0) {
            issues.push({
              project: project,
              issues: res.data.issues
            })
          }
        } catch (error) {
          console.error(`Error checking ${project.id}:`, error)
        }
      }
      setDriftIssues(issues)
    } catch (error) {
      console.error('Error checking projects:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">AI Inbox</h2>
        <p className="mt-1 text-sm text-gray-500">Things you should look at</p>
      </div>

      <div className="mb-4">
        <button
          onClick={checkAllProjects}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Checking...' : 'Check All Projects'}
        </button>
      </div>

      {driftIssues.length > 0 ? (
        <div className="space-y-4">
          {driftIssues.map((item, idx) => (
            <div key={idx} className="bg-white shadow rounded-lg">
              <div className="px-4 py-3 border-b">
                <Link
                  to={`/project/${item.project.id}`}
                  className="text-lg font-medium text-blue-600 hover:text-blue-800"
                >
                  {item.project.title}
                </Link>
              </div>
              <div className="px-4 py-4 space-y-2">
                {item.issues.map((issue, issueIdx) => (
                  <div key={issueIdx} className="p-3 border border-yellow-200 bg-yellow-50 rounded">
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
            </div>
          ))}
        </div>
      ) : !loading && (
        <div className="bg-white shadow rounded-lg p-8 text-center">
          <p className="text-gray-500">No issues detected. Click "Check All Projects" to scan for drift and issues.</p>
        </div>
      )}
    </div>
  )
}

export default AIInbox
