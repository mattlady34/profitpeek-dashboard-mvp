'use client';

import React from 'react';

// Simple Progress Bar Component
export function ProgressBar({ value, max = 100, label, color = 'blue' }: { 
  value: number, 
  max?: number, 
  label?: string, 
  color?: 'blue' | 'green' | 'yellow' | 'red' 
}) {
  const percentage = (value / max) * 100;
  
  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    red: 'bg-red-500',
  };

  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between text-sm font-medium text-gray-700 mb-2">
          <span>{label}</span>
          <span>{value.toFixed(1)}%</span>
        </div>
      )}
      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <div 
          className={`h-full rounded-full transition-all duration-1000 ease-out ${colorClasses[color]}`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
    </div>
  );
}

// Trend Indicator Component
export function TrendIndicator({ value, previousValue, label }: { 
  value: number, 
  previousValue: number, 
  label: string 
}) {
  const change = value - previousValue;
  const changePercent = previousValue > 0 ? (change / previousValue) * 100 : 0;
  const isPositive = change >= 0;
  
  return (
    <div className="flex items-center space-x-2">
      <div className={`flex items-center space-x-1 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
        <span className="text-lg">
          {isPositive ? '↗' : '↘'}
        </span>
        <span className="text-sm font-semibold">
          {Math.abs(changePercent).toFixed(1)}%
        </span>
      </div>
      <span className="text-sm text-gray-600">{label}</span>
    </div>
  );
}

// Mini Sparkline Chart (CSS-based)
export function MiniSparkline({ data, color = 'rgb(14, 165, 233)' }: { data: number[], color?: string }) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min;
  
  return (
    <div className="h-12 w-full flex items-end space-x-1">
      {data.map((value, index) => {
        const height = range > 0 ? ((value - min) / range) * 100 : 50;
        return (
          <div
            key={index}
            className="flex-1 rounded-sm opacity-80 hover:opacity-100 transition-opacity"
            style={{
              height: `${height}%`,
              backgroundColor: color,
              minHeight: '2px'
            }}
          />
        );
      })}
    </div>
  );
}

// Simple Bar Chart Component
export function SimpleBarChart({ data, title }: { data: any[], title: string }) {
  const max = Math.max(...data.map(item => item.value));
  
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      <div className="space-y-3">
        {data.map((item, index) => (
          <div key={index} className="flex items-center space-x-4">
            <div className="w-20 text-sm font-medium text-gray-600 truncate">
              {item.label}
            </div>
            <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full transition-all duration-1000 ease-out"
                style={{ width: `${(item.value / max) * 100}%` }}
              />
            </div>
            <div className="w-16 text-sm font-semibold text-gray-800 text-right">
              {item.value}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Revenue Trend Chart (CSS-based)
export function RevenueTrendChart({ data }: { data: any[] }) {
  const max = Math.max(...data.map(item => item.revenue));
  const min = Math.min(...data.map(item => item.revenue));
  const range = max - min;
  
  return (
    <div className="h-64 p-4">
      <div className="h-full flex items-end space-x-2">
        {data.map((item, index) => {
          const height = range > 0 ? ((item.revenue - min) / range) * 100 : 50;
          return (
            <div key={index} className="flex-1 flex flex-col items-center">
              <div
                className="w-full bg-gradient-to-t from-blue-500 to-blue-300 rounded-t-lg transition-all duration-500 hover:from-blue-600 hover:to-blue-400"
                style={{ height: `${height}%` }}
              />
              <div className="text-xs text-gray-600 mt-2 font-medium">
                {new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                ${item.revenue.toLocaleString()}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// Orders Status Chart (CSS-based)
export function OrdersStatusChart({ data }: { data: Record<string, number> }) {
  const total = Object.values(data).reduce((sum, value) => sum + value, 0);
  const entries = Object.entries(data);
  
  return (
    <div className="h-64 p-4">
      <div className="space-y-4">
        {entries.map(([status, count], index) => {
          const percentage = (count / total) * 100;
          const colors = [
            'bg-green-500',
            'bg-yellow-500', 
            'bg-blue-500',
            'bg-purple-500',
            'bg-red-500'
          ];
          
          return (
            <div key={status} className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700 capitalize">
                  {status.replace('_', ' ')}
                </span>
                <span className="text-sm font-semibold text-gray-900">
                  {count} ({percentage.toFixed(1)}%)
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className={`h-full ${colors[index % colors.length]} rounded-full transition-all duration-1000 ease-out`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// Profit Margin Chart (CSS-based)
export function ProfitMarginChart({ data }: { data: any[] }) {
  const max = Math.max(...data.map(item => item.margin));
  
  return (
    <div className="h-64 p-4">
      <div className="space-y-3">
        {data.map((item, index) => {
          const percentage = (item.margin / max) * 100;
          const color = item.margin >= 50 ? 'bg-green-500' : 
                      item.margin >= 30 ? 'bg-yellow-500' : 'bg-red-500';
          
          return (
            <div key={index} className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">
                  {item.order_name}
                </span>
                <span className="text-sm font-semibold text-gray-900">
                  {item.margin.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                <div
                  className={`h-full ${color} rounded-full transition-all duration-1000 ease-out`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
