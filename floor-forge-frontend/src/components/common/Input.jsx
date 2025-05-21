import React, { forwardRef } from 'react'

// Input sizes
const sizes = {
  sm: 'px-2 py-1 text-sm',
  md: 'px-4 py-2',
  lg: 'px-4 py-3 text-lg',
}

const Input = forwardRef(({
  id,
  name,
  type = 'text',
  label,
  placeholder,
  helper,
  error,
  size = 'md',
  fullWidth = false,
  disabled = false,
  required = false,
  className = '',
  leftIcon = null,
  rightIcon = null,
  onChange,
  onBlur,
  value,
  ...props
}, ref) => {
  // Generate a unique ID if one is not provided
  const inputId = id || `input-${name || Math.random().toString(36).substr(2, 9)}`
  
  // Basic input classes
  const inputClasses = `
    rounded-md border border-gray-300 bg-white
    focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
    disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed
    ${error ? 'border-error focus:ring-error focus:border-error' : ''}
    ${sizes[size] || sizes.md}
    ${fullWidth ? 'w-full' : ''}
    ${leftIcon ? 'pl-10' : ''}
    ${rightIcon ? 'pr-10' : ''}
    ${className}
  `

  return (
    <div className={`${fullWidth ? 'w-full' : ''}`}>
      {/* Input label */}
      {label && (
        <label 
          htmlFor={inputId} 
          className="block text-sm font-medium text-foreground mb-1"
        >
          {label}
          {required && <span className="text-error ml-1">*</span>}
        </label>
      )}
      
      {/* Input wrapper for positioning icons */}
      <div className="relative">
        {/* Left icon */}
        {leftIcon && (
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-muted">
            {leftIcon}
          </div>
        )}
        
        {/* Input element */}
        <input
          ref={ref}
          id={inputId}
          name={name}
          type={type}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          className={inputClasses}
          onChange={onChange}
          onBlur={onBlur}
          value={value}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${inputId}-error` : helper ? `${inputId}-helper` : undefined}
          {...props}
        />
        
        {/* Right icon */}
        {rightIcon && (
          <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-muted">
            {rightIcon}
          </div>
        )}
      </div>
      
      {/* Helper text */}
      {helper && !error && (
        <p id={`${inputId}-helper`} className="mt-1 text-sm text-muted">
          {helper}
        </p>
      )}
      
      {/* Error message */}
      {error && (
        <p id={`${inputId}-error`} className="mt-1 text-sm text-error">
          {error}
        </p>
      )}
    </div>
  )
})

// Display name for debugging
Input.displayName = 'Input'

export default Input