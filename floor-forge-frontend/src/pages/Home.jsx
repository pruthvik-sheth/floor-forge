import React, { useState } from 'react'
import FloorPlanForm from '../components/features/FloorPlanGenerator/FloorPlanForm'
import FloorPlanPreview from '../components/features/FloorPlanGenerator/FloorPlanPreview'
import FloorPlanControls from '../components/features/FloorPlanGenerator/FloorPlanControls'
import GeneratedFloorPlans from '../components/features/FloorPlanGenerator/GeneratedFloorPlans'
import useFloorPlan from '../hooks/useFloorPlan'

const Home = () => {
  // State for the current floor plan generation
  const [prompt, setPrompt] = useState('')
  const [error, setError] = useState(null)
  
  // Use the floor plan hook
  const {
    floorPlans,
    currentPlan: currentFloorPlan,
    isGenerating,
    generateFloorPlan,
    saveFloorPlan,
    setCurrentPlan: setCurrentFloorPlan
  } = useFloorPlan()

  // Handle floor plan generation with options
  const handleGenerateFloorPlan = async (options = {}) => {
    if (!prompt.trim()) {
      setError('Please enter a description for your floor plan')
      return
    }

    try {
      setError(null)
      
      // Generate the floor plan with options
      await generateFloorPlan(prompt, options)
      
    } catch (err) {
      console.error('Error generating floor plan:', err)
      setError('Failed to generate floor plan. Please try again.')
    }
  }

  // Handle saving the current floor plan with a custom name
  const handleSaveFloorPlan = (name) => {
    if (currentFloorPlan) {
      const updatedFloorPlan = { ...currentFloorPlan, name }
      saveFloorPlan(updatedFloorPlan)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header section with minimalist design */}
      <div className="w-full max-w-7xl mx-auto px-6 py-16 md:py-24">
        <h1 className="font-heading text-4xl md:text-6xl font-bold text-foreground leading-tight mb-4 max-w-4xl">
          Design your space <span className="text-accent">with precision</span>
        </h1>
        <p className="text-muted text-lg md:text-xl max-w-2xl">
          Generate architectural floor plans using AI. Simply describe what you need.
        </p>
      </div>
      
      {/* Main content area with glass morphism effect */}
      <div className="w-full max-w-7xl mx-auto px-6 pb-20">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left column - Input form */}
          <div className="lg:w-5/12">
            <div className="backdrop-blur-sm bg-white/80 rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="p-6 md:p-8">
                <h2 className="font-heading text-2xl font-semibold mb-6 text-foreground">
                  Blueprint Specifications
                </h2>
                
                <FloorPlanForm
                  prompt={prompt}
                  setPrompt={setPrompt}
                  onGenerate={handleGenerateFloorPlan}
                  isGenerating={isGenerating}
                  error={error}
                />
              </div>
              
              {/* Sample specifications with minimalist design */}
              <div className="bg-gray-50/80 p-6 md:p-8 border-t border-gray-100">
                <h3 className="text-xs uppercase tracking-wider font-medium mb-4 text-muted">
                  Sample Specifications
                </h3>
                <div className="space-y-3">
                  {[
                    "A modern one-bedroom apartment with an open kitchen and living room",
                    "A spacious three-bedroom house with two bathrooms and a large backyard",
                    "A studio apartment with a kitchen island and built-in storage",
                    "A two-story family home with four bedrooms and a home office"
                  ].map((sample, index) => (
                    <button
                      key={index}
                      onClick={() => setPrompt(sample)}
                      className="w-full text-left px-3 py-2 text-sm rounded-lg transition-colors hover:bg-white hover:shadow-sm text-foreground"
                      disabled={isGenerating}
                    >
                      {sample}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
          
          {/* Right column - Preview area */}
          <div className="lg:w-7/12 flex flex-col">
            <div className="backdrop-blur-sm bg-white/80 rounded-xl shadow-sm border border-gray-100 overflow-hidden flex-grow">
              <div className="p-6 md:p-8">
                <h2 className="font-heading text-2xl font-semibold mb-6 text-foreground flex items-center">
                  Blueprint Preview
                  {isGenerating && (
                    <span className="ml-3 text-xs bg-accent/10 text-accent px-2 py-1 rounded-full">
                      Generating...
                    </span>
                  )}
                </h2>
                
                <div className="aspect-square rounded-xl overflow-hidden bg-white shadow-inner border border-gray-100 relative">
                  <FloorPlanPreview
                    floorPlan={currentFloorPlan}
                    isGenerating={isGenerating}
                  />
                  
                  {/* Decorative corner elements */}
                  <div className="absolute top-0 left-0 w-6 h-6 border-t-2 border-l-2 border-accent/20 pointer-events-none"></div>
                  <div className="absolute top-0 right-0 w-6 h-6 border-t-2 border-r-2 border-accent/20 pointer-events-none"></div>
                  <div className="absolute bottom-0 left-0 w-6 h-6 border-b-2 border-l-2 border-accent/20 pointer-events-none"></div>
                  <div className="absolute bottom-0 right-0 w-6 h-6 border-b-2 border-r-2 border-accent/20 pointer-events-none"></div>
                </div>
              </div>
              
              {/* Controls appear when a floor plan is generated */}
              {currentFloorPlan && (
                <div className="p-6 md:p-8 border-t border-gray-100">
                  <FloorPlanControls
                    floorPlan={currentFloorPlan}
                    onSave={handleSaveFloorPlan}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Generated floor plans section */}
        {floorPlans.length > 0 && (
          <div className="mt-16">
            <div className="flex items-center mb-8">
              <h2 className="font-heading text-2xl font-semibold text-foreground">Your Floor Plans</h2>
              <div className="h-px bg-gray-200 flex-grow ml-4"></div>
            </div>
            <GeneratedFloorPlans 
              floorPlans={floorPlans}
              onSelect={setCurrentFloorPlan}
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default Home