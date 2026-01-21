import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import Editor from '@monaco-editor/react'
import { api } from '../api'

function FileEditor() {
  const { fileId } = useParams()
  const [file, setFile] = useState(null)
  const [content, setContent] = useState('')
  const [originalContent, setOriginalContent] = useState('')
  const [diff, setDiff] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    loadFile()
  }, [fileId])

  const loadFile = async () => {
    try {
      const res = await api.getFile(fileId)
      setFile(res.data)
      setContent(res.data.content || '')
      setOriginalContent(res.data.content || '')
    } catch (error) {
      console.error('Error loading file:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleContentChange = (value) => {
    setContent(value || '')
  }

  const previewDiff = async () => {
    if (content === originalContent) {
      setDiff(null)
      return
    }
    try {
      const res = await api.previewDiff(fileId, content)
      setDiff(res.data)
    } catch (error) {
      console.error('Error generating diff:', error)
    }
  }

  const applyChanges = async () => {
    setSaving(true)
    try {
      await api.applyDiff(fileId, content)
      setOriginalContent(content)
      setDiff(null)
      alert('Changes applied successfully')
    } catch (error) {
      console.error('Error applying changes:', error)
      alert('Error applying changes')
    } finally {
      setSaving(false)
    }
  }

  const hasChanges = content !== originalContent

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  if (!file) {
    return <div className="text-center py-12">File not found</div>
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">{file.title}</h2>
        <p className="text-sm text-gray-500 mt-1">{file.path}</p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-3 border-b flex justify-between items-center">
          <span className="text-sm font-medium text-gray-700">Editor</span>
          <div className="space-x-2">
            {hasChanges && (
              <>
                <button
                  onClick={previewDiff}
                  className="px-3 py-1 text-sm bg-gray-600 text-white rounded hover:bg-gray-700"
                >
                  Preview Diff
                </button>
                <button
                  onClick={applyChanges}
                  disabled={saving}
                  className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </>
            )}
          </div>
        </div>
        <div className="h-96">
          <Editor
            height="100%"
            defaultLanguage="markdown"
            value={content}
            onChange={handleContentChange}
            theme="vs-light"
            options={{
              minimap: { enabled: false },
              wordWrap: 'on',
            }}
          />
        </div>
      </div>

      {diff && (
        <div className="mt-6 bg-white shadow rounded-lg">
          <div className="px-4 py-3 border-b">
            <h3 className="text-lg font-medium text-gray-900">Diff Preview</h3>
            {diff.summary && (
              <div className="mt-2 text-sm text-gray-600">
                <span className="mr-4">+{diff.summary.added_lines} lines</span>
                <span className="mr-4">-{diff.summary.deleted_lines} lines</span>
                <span>{diff.summary.modified_lines} modified</span>
              </div>
            )}
          </div>
          <div className="px-4 py-4">
            <pre className="text-xs bg-gray-50 p-4 rounded overflow-x-auto">
              {diff.unified_diff}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default FileEditor
