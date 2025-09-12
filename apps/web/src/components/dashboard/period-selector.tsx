import React from 'react';
import { clsx } from 'clsx';

interface PeriodSelectorProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const periods = [
  { value: 'today', label: 'Today' },
  { value: 'yesterday', label: 'Yesterday' },
  { value: '7d', label: 'Last 7 days' },
  { value: 'mtd', label: 'Month to date' },
];

export function PeriodSelector({ value, onChange, disabled = false }: PeriodSelectorProps) {
  return (
    <div className="flex rounded-lg border border-gray-300 bg-white p-1">
      {periods.map((period) => (
        <button
          key={period.value}
          onClick={() => onChange(period.value)}
          disabled={disabled}
          className={clsx(
            'px-3 py-1.5 text-sm font-medium rounded-md transition-colors',
            value === period.value
              ? 'bg-primary-600 text-white'
              : 'text-gray-700 hover:bg-gray-100',
            disabled && 'opacity-50 cursor-not-allowed'
          )}
        >
          {period.label}
        </button>
      ))}
    </div>
  );
}
