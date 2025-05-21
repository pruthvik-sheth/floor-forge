import React from 'react'
import { formatDate } from '../../../utils/helpers'

const GeneratedFloorPlans = ({ floorPlans, onSelect }) => {
  // If no floor plans have been generated yet, show a message
  if (floorPlans.length === 0) {
    return (
      <div className="bg-surface rounded-md border border-gray-200 p-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
          <svg
            className="w-8 h-8 text-muted"
            fill="none"
            strokeWidth="1.5"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <p className="font-heading text-foreground font-medium">
          No Floor Plans Yet
        </p>
        <p className="text-sm text-muted mt-1">
          Your generated floor plans will appear here
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {floorPlans.map((plan) => (
        <div
          key={plan.id}
          className="group bg-white border border-gray-200 cursor-pointer transition-all hover:border-accent"
          onClick={() => onSelect(plan)}
        >
          <div className="relative aspect-square overflow-hidden bg-grid-pattern/50">
            {/* Blueprint corners - decorative elements */}
            <div className="absolute top-0 left-0 w-3 h-3 border-t border-l border-accent/30 z-10"></div>
            <div className="absolute top-0 right-0 w-3 h-3 border-t border-r border-accent/30 z-10"></div>
            <div className="absolute bottom-0 left-0 w-3 h-3 border-b border-l border-accent/30 z-10"></div>
            <div className="absolute bottom-0 right-0 w-3 h-3 border-b border-r border-accent/30 z-10"></div>
            
            {/* Floor plan image */}
            <img
              src={plan.imageUrl}
              alt={`Floor plan: ${plan.prompt}`}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
            />
            
            {/* Hover overlay */}
            <div className="absolute inset-0 bg-primary/10 opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="absolute bottom-2 right-2 bg-accent text-white text-xs px-2 py-1 rounded-sm">
                View
              </div>
            </div>
          </div>
          
          <div className="p-4">
            {/* Plan name with architectural styling */}
            <div className="flex items-center">
              <h3 className="font-heading font-medium text-foreground group-hover:text-accent transition-colors truncate">
                {plan.name || "Untitled Blueprint"}
              </h3>
              <div className="flex-grow ml-2 h-px bg-gray-200"></div>
            </div>
            
            {/* Plan description */}
            <p className="text-xs text-muted mt-2 line-clamp-2 h-8">
              {plan.prompt}
            </p>
            
            {/* Metadata row */}
            <div className="mt-3 pt-2 border-t border-gray-100 flex justify-between items-center">
              <div className="text-xs text-muted opacity-70 font-mono">
                {formatDate(plan.createdAt, { 
                  year: 'numeric', 
                  month: '2-digit', 
                  day: '2-digit' 
                })}
              </div>
              
              {/* Room count indicators */}
              <div className="flex space-x-2">
                {plan.roomCount && (
                  <div className="text-xs bg-surface px-1.5 py-0.5 rounded text-muted">
                    {plan.roomCount} {plan.roomCount === 1 ? 'room' : 'rooms'}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default GeneratedFloorPlans