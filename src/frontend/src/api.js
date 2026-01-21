import axios from 'axios'

const API_BASE = '/api'

export const api = {
  // Files
  listFiles: (fileType) => axios.get(`${API_BASE}/files`, { params: { file_type: fileType } }),
  getFile: (fileId) => axios.get(`${API_BASE}/files/${fileId}`),
  listProjects: () => axios.get(`${API_BASE}/projects`),
  listRisks: () => axios.get(`${API_BASE}/risks`),
  listDecisions: () => axios.get(`${API_BASE}/decisions`),

  // AI
  getProjectSummary: (projectId) => axios.get(`${API_BASE}/ai/summary/${projectId}`),
  detectDrift: (projectId) => axios.get(`${API_BASE}/ai/drift/${projectId}`),
  forecastBlockers: (projectId) => axios.post(`${API_BASE}/ai/forecast/${projectId}`),
  ingestMeeting: (notes, projectId) => axios.post(`${API_BASE}/ai/ingest-meeting`, { notes, project_id: projectId }),
  editFile: (fileId, request) => axios.post(`${API_BASE}/ai/edit/${fileId}`, { request }),

  // Diff
  generateDiff: (original, updated, filename) => axios.post(`${API_BASE}/diff/generate`, { original, updated, filename }),
  previewDiff: (fileId, content) => axios.post(`${API_BASE}/diff/preview/${fileId}`, { content }),
  applyDiff: (fileId, content, backup = true) => axios.post(`${API_BASE}/diff/apply/${fileId}`, { content, backup }),

  // Search
  search: (query, topK = 5) => axios.post(`${API_BASE}/search`, { query, top_k: topK }),
}
