import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return

    setLoading(true)
    try {
      const res = await api.search(query, 10)
      setResults(res.data.results || [])
    } catch (error) {
      console.error('Error searching:', error)
      if (error.response?.status === 503) {
        alert('Semantic search not available. Install sentence-transformers in backend.')
      } else {
        alert('Error performing search')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Semantic Search</h2>
        <p className="mt-1 text-sm text-gray-500">Search across all files using semantic similarity</p>
      </div>

      <div className="bg-white shadow rounded-lg mb-6">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex space-x-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter search query..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
            <button
              onClick={handleSearch}
              disabled={loading || !query.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </div>
      </div>

      {results.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-3 border-b">
            <h3 className="text-lg font-medium text-gray-900">
              Results ({results.length})
            </h3>
          </div>
          <div className="px-4 py-4 space-y-3">
            {results.map((result, idx) => (
              <Link
                key={idx}
                to={`/file/${result.file_id}`}
                className="block p-3 border border-gray-200 rounded hover:bg-gray-50"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">{result.title}</h4>
                    <p className="text-xs text-gray-500 mt-1">{result.path}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded">
                      {result.file_type}
                    </span>
                    <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                      {(result.similarity * 100).toFixed(0)}% match
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {results.length === 0 && !loading && query && (
        <div className="bg-white shadow rounded-lg p-8 text-center">
          <p className="text-gray-500">No results found</p>
        </div>
      )}
    </div>
  )
}

export default Search
