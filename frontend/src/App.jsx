import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Header from './components/Header'
import HomePage from './pages/HomePage'
import SearchResults from './pages/SearchResults'
import { SessionProvider } from './context/SessionContext'

function App() {
  return (
    <SessionProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header />
          
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/results/:sessionId" element={<SearchResults />} />
            </Routes>
          </main>
          
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              className: 'text-sm',
            }}
          />
        </div>
      </Router>
    </SessionProvider>
  )
}

export default App
