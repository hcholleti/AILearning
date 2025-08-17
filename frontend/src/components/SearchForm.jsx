import React, { useState } from 'react'
import { Search, MapPin, Calendar, Filter, Zap } from 'lucide-react'
import toast from 'react-hot-toast'

const SearchForm = ({ sessionId, onSearchSuccess, isLoading, setIsLoading }) => {
  const [searchParams, setSearchParams] = useState({
    keywords: 'Software Engineer',
    location: 'USA',
    posted_within_days: 7,
    user_prompt: 'filter for relevant jobs',
    match_score_threshold: 50,
    use_llm_filtering: false
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!sessionId) {
      toast.error('Please upload your resume first')
      return
    }

    setIsLoading(true)

    try {
      const response = await fetch(`/api/search-jobs?session_id=${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchParams),
      })

      if (!response.ok) {
        throw new Error('Search failed')
      }

      const data = await response.json()
      toast.success(`Found ${data.filtered_jobs} matching jobs!`)
      onSearchSuccess(data)
    } catch (error) {
      toast.error('Search failed. Please try again.')
      console.error('Search error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (field, value) => {
    setSearchParams(prev => ({
      ...prev,
      [field]: value
    }))
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        2. Search & Filter Jobs
      </h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label">
              <Search className="inline h-4 w-4 mr-1" />
              Job Keywords
            </label>
            <input
              type="text"
              className="input-field"
              value={searchParams.keywords}
              onChange={(e) => handleChange('keywords', e.target.value)}
              placeholder="e.g., Software Engineer, DevOps"
              required
            />
          </div>
          
          <div>
            <label className="label">
              <MapPin className="inline h-4 w-4 mr-1" />
              Location
            </label>
            <input
              type="text"
              className="input-field"
              value={searchParams.location}
              onChange={(e) => handleChange('location', e.target.value)}
              placeholder="e.g., USA, San Francisco"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label">
              <Calendar className="inline h-4 w-4 mr-1" />
              Posted Within (days)
            </label>
            <select
              className="input-field"
              value={searchParams.posted_within_days}
              onChange={(e) => handleChange('posted_within_days', parseInt(e.target.value))}
            >
              <option value={1}>1 day</option>
              <option value={3}>3 days</option>
              <option value={7}>1 week</option>
              <option value={14}>2 weeks</option>
              <option value={30}>1 month</option>
            </select>
          </div>
          
          <div>
            <label className="label">
              <Filter className="inline h-4 w-4 mr-1" />
              Minimum Match Score (%)
            </label>
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              className="w-full"
              value={searchParams.match_score_threshold}
              onChange={(e) => handleChange('match_score_threshold', parseInt(e.target.value))}
            />
            <div className="text-center text-sm text-gray-600 mt-1">
              {searchParams.match_score_threshold}%
            </div>
          </div>
        </div>

        <div>
          <label className="label">
            <Zap className="inline h-4 w-4 mr-1" />
            AI Filter Prompt
          </label>
          <input
            type="text"
            className="input-field"
            value={searchParams.user_prompt}
            onChange={(e) => handleChange('user_prompt', e.target.value)}
            placeholder="e.g., filter for DevOps jobs requiring Terraform"
          />
          <p className="text-xs text-gray-500 mt-1">
            Describe what types of jobs you want to find
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="use_llm"
            checked={searchParams.use_llm_filtering}
            onChange={(e) => handleChange('use_llm_filtering', e.target.checked)}
            className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <label htmlFor="use_llm" className="text-sm text-gray-700">
            Use advanced LLM filtering (slower but more accurate)
          </label>
        </div>

        <button
          type="submit"
          disabled={isLoading || !sessionId}
          className={`w-full btn-primary ${isLoading || !sessionId ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Searching Jobs...
            </span>
          ) : (
            'Search Jobs'
          )}
        </button>
      </form>
    </div>
  )
}

export default SearchForm
