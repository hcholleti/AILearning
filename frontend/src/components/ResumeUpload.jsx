import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

const ResumeUpload = ({ onUploadSuccess, isLoading, setIsLoading }) => {
  const [uploadStatus, setUploadStatus] = useState(null) // null, 'success', 'error'

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return

    setIsLoading(true)
    setUploadStatus(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/upload-resume', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const data = await response.json()
      setUploadStatus('success')
      toast.success('Resume uploaded and parsed successfully!')
      onUploadSuccess(data)
    } catch (error) {
      setUploadStatus('error')
      toast.error('Failed to upload resume. Please try again.')
      console.error('Upload error:', error)
    } finally {
      setIsLoading(false)
    }
  }, [onUploadSuccess, setIsLoading])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1,
    disabled: isLoading
  })

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        1. Upload Your Resume
      </h3>
      
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer
          ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-400'}
          ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
          ${uploadStatus === 'success' ? 'border-success-500 bg-success-50' : ''}
          ${uploadStatus === 'error' ? 'border-danger-500 bg-danger-50' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-3">
          {uploadStatus === 'success' ? (
            <CheckCircle className="h-12 w-12 text-success-500" />
          ) : uploadStatus === 'error' ? (
            <AlertCircle className="h-12 w-12 text-danger-500" />
          ) : (
            <Upload className={`h-12 w-12 ${isDragActive ? 'text-primary-500' : 'text-gray-400'}`} />
          )}
          
          <div>
            {isLoading ? (
              <p className="text-gray-600">Processing your resume...</p>
            ) : uploadStatus === 'success' ? (
              <p className="text-success-600 font-medium">Resume uploaded successfully!</p>
            ) : uploadStatus === 'error' ? (
              <p className="text-danger-600">Upload failed. Please try again.</p>
            ) : (
              <>
                <p className="text-gray-700 font-medium">
                  {isDragActive
                    ? 'Drop your resume here'
                    : 'Drag & drop your resume, or click to browse'
                  }
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Supports PDF and DOCX files
                </p>
              </>
            )}
          </div>
          
          {uploadStatus === 'success' && (
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <FileText className="h-4 w-4" />
              <span>Resume parsed and ready for matching</span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ResumeUpload
