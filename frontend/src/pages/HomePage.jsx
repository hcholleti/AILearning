import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ResumeUpload from '../components/ResumeUpload'
import SearchForm from '../components/SearchForm'
import { useSession } from '../context/SessionContext'

const HomePage = () => {
  const [isLoading, setIsLoading] = useState(false)
  const { sessionId, setSessionId, resumeProfile, setResumeProfile } = useSession()
  const navigate = useNavigate()

  const handleUploadSuccess = (data) => {
    setSessionId(data.session_id)
    setResumeProfile(data.resume_profile)
  }

  const handleSearchSuccess = (data) => {
    navigate(`/results/${data.session_id}`)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Find Your Perfect Job Match
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Upload your resume and let our AI find the most relevant job opportunities, 
          ranked by compatibility with your skills and experience.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <ResumeUpload
          onUploadSuccess={handleUploadSuccess}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />
        
        <SearchForm
          sessionId={sessionId}
          onSearchSuccess={handleSearchSuccess}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />
      </div>

      {resumeProfile && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Resume Analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-primary-50 p-4 rounded-lg">
              <h4 className="font-medium text-primary-900">Experience</h4>
              <p className="text-2xl font-bold text-primary-600">
                {resumeProfile.experience_years} years
              </p>
            </div>
            <div className="bg-success-50 p-4 rounded-lg">
              <h4 className="font-medium text-success-900">Tech Skills</h4>
              <p className="text-2xl font-bold text-success-600">
                {resumeProfile.tech_skills?.length || 0}
              </p>
            </div>
            <div className="bg-warning-50 p-4 rounded-lg">
              <h4 className="font-medium text-warning-900">Total Skills</h4>
              <p className="text-2xl font-bold text-warning-600">
                {resumeProfile.skills?.length || 0}
              </p>
            </div>
          </div>
          
          {resumeProfile.tech_skills?.length > 0 && (
            <div className="mt-4">
              <h4 className="font-medium text-gray-900 mb-2">Key Technologies:</h4>
              <div className="flex flex-wrap gap-2">
                {resumeProfile.tech_skills.slice(0, 10).map((skill, index) => (
                  <span
                    key={index}
                    className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded"
                  >
                    {skill}
                  </span>
                ))}
                {resumeProfile.tech_skills.length > 10 && (
                  <span className="text-gray-500 text-xs">
                    +{resumeProfile.tech_skills.length - 10} more
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default HomePage
