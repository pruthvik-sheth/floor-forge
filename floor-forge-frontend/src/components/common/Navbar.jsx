import React, { useState } from 'react'
import { Link } from 'react-router-dom'

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  return (
    // In Navbar.jsx
    <nav className="bg-white border-b border-gray-100">
    <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
        {/* Logo with blueprint icon */}
        <Link to="/" className="flex items-center space-x-3">
            <svg 
            className="w-8 h-8 text-accent" 
            viewBox="0 0 24 24" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
            >
            <path 
                d="M2 9h20M9 16V9m3 7V9m3-6H5a1 1 0 00-1 1v16a1 1 0 001 1h14a1 1 0 001-1V4a1 1 0 00-1-1z" 
                stroke="currentColor" 
                strokeWidth="1.5" 
                strokeLinecap="round" 
                strokeLinejoin="round"
            />
            </svg>
            <span className="font-heading font-semibold tracking-wide text-foreground">FLOORFORGE</span>
        </Link>
        
        {/* Minimal navigation - just essential links */}
        <div className="hidden md:flex items-center space-x-8">
            <Link 
            to="/" 
            className="text-sm uppercase tracking-wider text-foreground hover:text-accent transition-colors"
            >
            Create
            </Link>
            <Link 
            to="/gallery" 
            className="text-sm uppercase tracking-wider text-foreground hover:text-accent transition-colors"
            >
            Gallery
            </Link>
        </div>
        </div>
    </div>
    </nav>
  )
}

export default Navbar