import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

function Dashboard() {
  const [projects, setProjects] = useState([])
  const [risks, setRisks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [projectsRes, risksRes] = await Promise.all([
        api.listProjects(),
        api.listRisks()
      ])
      setProjects(projectsRes.data.projects || [])
      setRisks(risksRes.data.risks || [])
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'on-hold':
        return 'bg-yellow-100 text-yellow-800'
      case 'completed':
        return 'bg-blue-100 text-blue-800'
      case 'cancelled':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800'
      case 'high':
        return 'bg-orange-100 text-orange-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">PMO Dashboard</h2>
        <p className="mt-1 text-sm text-gray-500">Portfolio health overview</p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Projects */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Projects</h3>
            <div className="space-y-3">
              {projects.length === 0 ? (
                <p className="text-sm text-gray-500">No projects found</p>
              ) : (
                projects.map((project) => (
                  <Link
                    key={project.id}
                    to={`/project/${project.id}`}
                    className="block p-3 border border-gray-200 rounded hover:bg-gray-50"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">{project.title}</h4>
                        <p className="text-xs text-gray-500 mt-1">Owner: {project.owner || 'Unassigned'}</p>
                      </div>
                      {project.status && (
                        <span className={`px-2 py-1 text-xs font-medium rounded ${getStatusColor(project.status)}`}>
                          {project.status}
                        </span>
                      )}
                    </div>
                  </Link>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Top Risks */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Top Risks</h3>
            <div className="space-y-3">
              {risks.length === 0 ? (
                <p className="text-sm text-gray-500">No risks found</p>
              ) : (
                risks.slice(0, 5).map((risk) => (
                  <Link
                    key={risk.id}
                    to={`/file/${risk.id}`}
                    className="block p-3 border border-gray-200 rounded hover:bg-gray-50"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">{risk.title}</h4>
                        <p className="text-xs text-gray-500 mt-1">Owner: {risk.owner || 'Unassigned'}</p>
                      </div>
                      {risk.frontmatter?.severity && (
                        <span className={`px-2 py-1 text-xs font-medium rounded ${getSeverityColor(risk.frontmatter.severity)}`}>
                          {risk.frontmatter.severity}
                        </span>
                      )}
                    </div>
                  </Link>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
