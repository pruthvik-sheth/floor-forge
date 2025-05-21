import React from 'react'

const FloorPlanPreview = ({ floorPlan, isGenerating }) => {
  // If we're generating a floor plan, show a loading state
  if (isGenerating) {
    return (
      <div className="bg-surface rounded-lg shadow-md overflow-hidden">
        <div className="p-6 flex flex-col items-center justify-center h-80 bg-gray-50">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
          <p className="text-center text-muted">Generating your floor plan...</p>
          <p className="text-sm text-center text-muted mt-2">This may take a few moments</p>
        </div>
      </div>
    )
  }

  // If no floor plan is available yet, show a placeholder
  if (!floorPlan) {
    return (
      <div className="bg-surface rounded-lg shadow-md overflow-hidden">
        <div className="p-6 flex flex-col items-center justify-center h-80 bg-gray-50">
          <svg
            className="w-16 h-16 text-muted mb-4"
            fill="none"
            strokeWidth="1.5"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z"
            />
          </svg>
          <p className="text-center text-muted">Your floor plan will appear here</p>
          <p className="text-sm text-center text-muted mt-2">
            Enter a description and click Generate
          </p>
        </div>
      </div>
    )
  }

  // If we have a floor plan, display it with its prompt
  return (
    <div className="bg-white rounded-md border border-gray-200 overflow-hidden">
        <div className="relative aspect-square bg-grid-pattern">
            {isGenerating ? (
            <div className="flex flex-col items-center justify-center h-full">
                <div className="h-16 w-16 border-t-2 border-accent rounded-full animate-spin mb-4"></div>
                <p className="text-muted font-medium">Generating blueprint...</p>
            </div>
            ) : !floorPlan ? (
            <div className="flex flex-col items-center justify-center h-full">
                <svg
                className="w-16 h-16 text-muted/50 mb-4"
                fill="none"
                strokeWidth="1"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                >
                <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
                </svg>
                <p className="text-muted">Your blueprint will appear here</p>
            </div>
            ) : (
            <img
                src={floorPlan.imageUrl}
                alt={`Floor plan: ${floorPlan.prompt}`}
                className="w-full h-full object-contain"
            />
            )}
            
            {/* Blueprint decorative corner marks */}
            <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-accent/70"></div>
            <div className="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-accent/70"></div>
            <div className="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-accent/70"></div>
            <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-accent/70"></div>
        </div>
        
        {floorPlan && (
            <div className="p-4 border-t border-gray-200">
            <h3 className="font-heading font-medium text-foreground">
                {floorPlan.name || "Blueprint Draft"}
            </h3>
            <p className="text-sm text-muted mt-1">
                {floorPlan.prompt}
            </p>
            </div>
        )}
    </div>
  )
}

export default FloorPlanPreview