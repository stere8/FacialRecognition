import React, { useEffect, useState } from 'react'
import { recognizeFace, saveFace } from '../api'

const UploadForm = ({ mode, onComplete }) => {
  // mode: 'add' → show name field + save; 'identify' → recognize
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [errorMessage, setErrorMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [fileName, setFileName] = useState('')

  const handleFileNameChange = (e) => {
    setFileName(e.target.value)
    setErrorMessage('')
  }

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0]
    if (!selectedFile) {
      setErrorMessage('Please select a file')
      setFile(null)
      return
    }
    if (!selectedFile.type.startsWith('image/') || selectedFile.size > 5 * 1024 * 1024) {
      setErrorMessage('Select an image under 5 MB')
      setFile(null)
      return
    }
    setErrorMessage('')
    setFile(selectedFile)
  }

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null)
      return
    }
    const url = URL.createObjectURL(file)
    setPreviewUrl(url)
    return () => URL.revokeObjectURL(url)
  }, [file])

  const handleSubmit = async () => {
    if (!file || isLoading) return
    setErrorMessage('')
    setIsLoading(true)

    try {
      if (mode === 'add') {
        if (!fileName.trim()) {
          setErrorMessage('Enter a name before saving')
          setIsLoading(false)
          return
        }
        const result = await saveFace(file, fileName)
        onComplete(result)
      } else {
        // mode === 'identify'
        const result = await recognizeFace(file)
        onComplete(result)
      }
    } catch (err) {
      console.error(err)
      setErrorMessage('Operation failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="upload-form max-w-sm mx-auto">
      {/* File Input */}
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        disabled={isLoading}
        className="block w-full text-sm text-gray-600"
      />

      {/* Preview */}
      {previewUrl && (
        <img
          src={previewUrl}
          alt="Preview"
          className="w-32 h-32 object-cover mt-2 mx-auto rounded"
        />
      )}

      {/* Name input only in “add” mode */}
      {mode === 'add' && (
        <div className="mt-2">
          <label className="block text-sm font-medium text-gray-700">
            Name:
          </label>
          <input
            type="text"
            placeholder="Enter name"
            value={fileName}
            onChange={handleFileNameChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-1 focus:ring-blue-500 focus:border-blue-500 text-sm"
            disabled={isLoading}
          />
        </div>
      )}

      {/* Error Message */}
      {errorMessage && (
        <p className="text-red-500 mt-1 text-sm">{errorMessage}</p>
      )}

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={!file || isLoading}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 w-full"
      >
        {isLoading
          ? 'Processing…'
          : mode === 'add'
          ? 'Save Person'
          : 'Identify Face'}
      </button>
    </div>
  )
}

export default UploadForm
