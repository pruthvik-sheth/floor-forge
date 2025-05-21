import React, { useState } from 'react'

const FloorPlanForm = ({ prompt, setPrompt, onGenerate, isGenerating, error }) => {
  // In FloorPlanForm.jsx, update the handleSubmit function
const handleSubmit = (e) => {
  e.preventDefault()
  
  // Add additional parameters if needed
  const options = {
    numInferenceSteps: 50,  // Default or let the user configure
    guidanceScale: 7.5,     // Default or let the user configure
    seed: Math.floor(Math.random() * 1000000)  // Random seed
  }
  
  onGenerate(options)
}

  // Sample prompts to help users get started
  const samplePrompts = [
    "A modern one-bedroom apartment with an open kitchen and living room",
    "A spacious three-bedroom house with two bathrooms and a large backyard",
    "A studio apartment with a kitchen island and built-in storage",
    "A two-story family home with four bedrooms and a home office"
  ]

  const handleUseSamplePrompt = (sample) => {
    setPrompt(sample)
  }

  return (
    <div className="bg-white rounded-lg overflow-hidden shadow-sm border border-gray-100">
      <div className="p-8">
        <h2 className="font-heading text-xl text-foreground mb-8 font-light tracking-wide">Blueprint Specifications</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-8">
            <label htmlFor="prompt" className="block text-xs uppercase tracking-wider text-muted mb-3 font-medium">
              Floor Plan Description
            </label>
            <textarea
              id="prompt"
              className="w-full border-0 border-b border-gray-200 px-0 py-2 bg-transparent focus:ring-0 focus:border-accent placeholder-gray-300 resize-none"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your ideal floor plan..."
              disabled={isGenerating}
              rows={4}
            />
          </div>
          
          {error && (
            <div className="mb-6 text-error text-sm font-light">
              {error}
            </div>
          )}
          
          <button
            type="submit"
            className={`w-full py-3.5 rounded-md font-medium text-sm transition-all ${
              isGenerating
                ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                : "bg-accent text-white hover:bg-accent/90"
            }`}
            disabled={isGenerating}
          >
            {isGenerating ? 
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating Blueprint
              </span> 
              : "GENERATE BLUEPRINT"
            }
          </button>
        </form>
      </div>
      
      <div className="bg-gray-50 p-6">
        <h3 className="text-xs uppercase tracking-wider text-muted/80 mb-4 font-medium">Sample Specifications</h3>
        <div className="space-y-3">
          {samplePrompts.map((sample, index) => (
            <button
              key={index}
              className="w-full text-left px-0 py-2 text-sm border-b border-gray-100 text-foreground/80 hover:text-accent transition-colors flex items-center"
              onClick={() => handleUseSamplePrompt(sample)}
              disabled={isGenerating}
            >
              <span className="w-1.5 h-1.5 bg-accent/30 rounded-full mr-2 flex-shrink-0"></span>
              {sample}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default FloorPlanForm