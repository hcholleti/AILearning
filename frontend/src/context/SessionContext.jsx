import React, { createContext, useContext, useState } from 'react'

const SessionContext = createContext()

export const useSession = () => {
  const context = useContext(SessionContext)
  if (!context) {
    throw new Error('useSession must be used within a SessionProvider')
  }
  return context
}

export const SessionProvider = ({ children }) => {
  const [sessionId, setSessionId] = useState(null)
  const [resumeProfile, setResumeProfile] = useState(null)
  const [searchResults, setSearchResults] = useState(null)

  const clearSession = () => {
    setSessionId(null)
    setResumeProfile(null)
    setSearchResults(null)
  }

  const value = {
    sessionId,
    setSessionId,
    resumeProfile,
    setResumeProfile,
    searchResults,
    setSearchResults,
    clearSession
  }

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  )
}

export default SessionContext
