import React from 'react'
import { Link } from 'react-router-dom'

const NotFound = () => {
  return (
    <div className="container mx-auto px-4 py-16 text-center">
      <div className="max-w-md mx-auto">
        <svg
          className="w-24 h-24 mx-auto text-muted mb-6"
          fill="none"
          strokeWidth="1.5"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
          />
        </svg>
        
        <h1 className="text-5xl font-bold mb-4 text-foreground">404</h1>
        <h2 className="text-2xl font-semibold mb-6 text-foreground">Page Not Found</h2>
        
        <p className="text-muted mb-8">
          Sorry, we couldn't find the page you're looking for. It might have been moved or doesn't exist.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/"
            className="inline-block px-6 py-3 bg-primary text-white rounded-md font-medium hover:bg-primary/90 transition-colors"
          >
            Return Home
          </Link>
          
          <button
            onClick={() => window.history.back()}
            className="inline-block px-6 py-3 bg-surface text-foreground border border-gray-300 rounded-md font-medium hover:bg-gray-100 transition-colors"
          >
            Go Back
          </button>
        </div>
        
        {/* Blueprint-style decoration */}
        <div className="mt-12 border-2 border-primary/20 p-4 rounded-lg relative hidden md:block">
          <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-background px-4 text-primary text-sm">
            BLUEPRINT ERROR
          </div>
          <div className="grid grid-cols-6 gap-2">
            {Array(24).fill().map((_, i) => (
              <div 
                key={i} 
                className={`h-4 rounded-sm ${i % 3 === 0 ? 'bg-primary/20' : 'bg-primary/10'}`}
              ></div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default NotFound