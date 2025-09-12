import React from 'react';
import { clsx } from 'clsx';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'danger' | 'gray' | 'outline';
  className?: string;
}

export function Badge({ 
  children, 
  variant = 'gray', 
  className 
}: BadgeProps) {
  const baseClasses = 'badge';
  
  const variantClasses = {
    success: 'badge-success',
    warning: 'badge-warning',
    danger: 'badge-danger',
    gray: 'badge-gray',
    outline: 'border border-gray-300 bg-white text-gray-700',
  };
  
  return (
    <span className={clsx(baseClasses, variantClasses[variant], className)}>
      {children}
    </span>
  );
}
