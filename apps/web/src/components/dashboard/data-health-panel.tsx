'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  ExclamationTriangleIcon, 
  CheckCircleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';
import { useDataHealth } from '@/hooks/use-data-health';

export function DataHealthPanel() {
  const { data: healthData, isLoading } = useDataHealth();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Data Health</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  const getHealthStatus = (score: number) => {
    if (score >= 0.9) return { status: 'excellent', color: 'success', icon: CheckCircleIcon };
    if (score >= 0.7) return { status: 'good', color: 'warning', icon: InformationCircleIcon };
    return { status: 'needs attention', color: 'danger', icon: ExclamationTriangleIcon };
  };

  const healthStatus = getHealthStatus(healthData?.data_completeness_score || 0);

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Data Health</CardTitle>
          <Badge variant={healthStatus.color as any}>
            {healthStatus.status}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Completeness Score</span>
            <span className="text-sm font-medium">
              {Math.round((healthData?.data_completeness_score || 0) * 100)}%
            </span>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all duration-300 ${
                healthStatus.color === 'success' ? 'bg-success-500' :
                healthStatus.color === 'warning' ? 'bg-warning-500' : 'bg-danger-500'
              }`}
              style={{ width: `${(healthData?.data_completeness_score || 0) * 100}%` }}
            />
          </div>

          <div className="space-y-2 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Orders with estimated fees</span>
              <span className="font-medium">{healthData?.orders_with_estimated_fees || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Orders missing unit costs</span>
              <span className="font-medium">{healthData?.orders_missing_unit_costs || 0}</span>
            </div>
          </div>

          {healthData?.recommendations && healthData.recommendations.length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Recommendations</h4>
              <ul className="space-y-1">
                {healthData.recommendations.map((recommendation, index) => (
                  <li key={index} className="flex items-start text-sm text-gray-600">
                    <ExclamationTriangleIcon className="h-4 w-4 text-warning-500 mr-2 mt-0.5 flex-shrink-0" />
                    {recommendation}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
