import React from 'react'
import { Brain, Briefcase } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">AI Job Tracker</h1>
              <p className="text-sm text-gray-600">Smart job matching with AI</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Briefcase className="h-4 w-4" />
            <span>Find your perfect match</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
