import React, { useState } from 'react'

const FloorPlanControls = ({ floorPlan, onSave }) => {
  const [isNaming, setIsNaming] = useState(false)
  const [name, setName] = useState(floorPlan.name || '')

  // Handle download of the floor plan image
  const handleDownload = () => {
    // Create a temporary anchor element
    const link = document.createElement('a')
    link.href = floorPlan.imageUrl
    link.download = `floorplan-${floorPlan.id}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  // Handle saving with a custom name
  const handleSave = (e) => {
    e.preventDefault()
    onSave(name.trim() || 'Untitled Floor Plan')
    setIsNaming(false)
  }

  // Cancel naming and reset to previous name
  const handleCancel = () => {
    setName(floorPlan.name || '')
    setIsNaming(false)
  }

  return (
    <div className="mt-4 bg-surface rounded-lg p-4 shadow-md">
      {isNaming ? (
        <form onSubmit={handleSave} className="flex gap-2">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter a name"
            className="flex-grow px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
            autoFocus
          />
          <button
            type="submit"
            className="px-4 py-2 bg-success text-white rounded-md hover:bg-success/90 transition-colors"
          >
            Save
          </button>
          <button
            type="button"
            onClick={handleCancel}
            className="px-4 py-2 bg-surface text-foreground border border-gray-300 rounded-md hover:bg-gray-100 transition-colors"
          >
            Cancel
          </button>
        </form>
      ) : (
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setIsNaming(true)}
            className="flex items-center gap-1 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              strokeWidth="1.5"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10"
              />
            </svg>
            Rename
          </button>

          <button
            onClick={handleDownload}
            className="flex items-center gap-1 px-4 py-2 bg-secondary text-white rounded-md hover:bg-secondary/90 transition-colors"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              strokeWidth="1.5"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"
              />
            </svg>
            Download
          </button>

          <button
            className="flex items-center gap-1 px-4 py-2 bg-surface text-foreground border border-gray-300 rounded-md hover:bg-gray-100 transition-colors"
            onClick={() => {
              // Copy image URL to clipboard
              navigator.clipboard.writeText(floorPlan.imageUrl);
              // A real app would show a toast notification here
              alert('Image URL copied to clipboard');
            }}
          >
            <svg
              className="w-5 h-5"
              fill="none"
              strokeWidth="1.5"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M8.25 7.5V6.108c0-1.135.845-2.098 1.976-2.192.373-.03.748-.057 1.123-.08M15.75 18H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08M15.75 18.75v-1.875a3.375 3.375 0 00-3.375-3.375h-1.5a1.125 1.125 0 01-1.125-1.125v-1.5A3.375 3.375 0 006.375 7.5H5.25m11.9-3.664A2.251 2.251 0 0015 2.25h-1.5a2.251 2.251 0 00-2.15 1.586m5.8 0c.065.21.1.433.1.664v.75h-6V4.5c0-.231.035-.454.1-.664M6.75 7.5H4.875c-.621 0-1.125.504-1.125 1.125v12c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V16.5a9 9 0 00-9-9z"
              />
            </svg>
            Copy Link
          </button>
        </div>
      )}

      {/* Display generation date */}
      <div className="mt-3 text-xs text-muted">
        Generated on: {new Date(floorPlan.createdAt).toLocaleString()}
      </div>
    </div>
  )
}

export default FloorPlanControls