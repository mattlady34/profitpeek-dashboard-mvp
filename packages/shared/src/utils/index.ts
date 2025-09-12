// Utility functions for ProfitPeek

import { Money, PriceSet, ShippingPriceSet } from '../types';

/**
 * Convert a string amount to a number with proper decimal handling
 */
export function parseAmount(amount: string): number {
  return parseFloat(amount) || 0;
}

/**
 * Format a number as currency with proper decimal places
 */
export function formatCurrency(amount: number, currency: string = 'USD', precision: number = 2): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: precision,
    maximumFractionDigits: precision,
  }).format(amount);
}

/**
 * Convert money object to number
 */
export function moneyToNumber(money: Money): number {
  return parseAmount(money.amount);
}

/**
 * Convert price set to number (shop currency)
 */
export function priceSetToNumber(priceSet: PriceSet): number {
  return moneyToNumber(priceSet.shop_money);
}

/**
 * Convert shipping price set to number (shop currency)
 */
export function shippingPriceSetToNumber(priceSet: ShippingPriceSet): number {
  return moneyToNumber(priceSet.shop_money);
}

/**
 * Calculate percentage with proper rounding
 */
export function calculatePercentage(part: number, total: number): number {
  if (total === 0) return 0;
  return Math.round((part / total) * 10000) / 100; // Round to 2 decimal places
}

/**
 * Calculate margin percentage
 */
export function calculateMargin(netProfit: number, netRevenue: number): number {
  if (netRevenue === 0) return 0;
  return calculatePercentage(netProfit, netRevenue);
}

/**
 * Generate a unique deduplication key for webhooks
 */
export function generateDedupKey(topic: string, shopId: string, resourceId: string, timestamp: string): string {
  return `${topic}:${shopId}:${resourceId}:${timestamp}`;
}

/**
 * Generate a unique deduplication key for webhooks
 */
export function generateWebhookDedupKey(topic: string, shopDomain: string, resourceId: string, timestamp: string): string {
  return `${topic}:${shopDomain}:${resourceId}:${timestamp}`;
}

/**
 * Validate Shopify webhook HMAC signature
 */
export function validateWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const crypto = require('crypto');
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(payload, 'utf8');
  const calculatedSignature = hmac.digest('base64');
  return crypto.timingSafeEqual(
    Buffer.from(signature, 'base64'),
    Buffer.from(calculatedSignature, 'base64')
  );
}

/**
 * Convert Shopify timestamp to Date
 */
export function parseShopifyTimestamp(timestamp: string): Date {
  return new Date(timestamp);
}

/**
 * Get start and end dates for a time period
 */
export function getTimePeriodDates(period: string, timezone: string = 'UTC'): { start: Date; end: Date } {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  
  switch (period) {
    case 'today':
      return {
        start: new Date(today),
        end: new Date(today.getTime() + 24 * 60 * 60 * 1000 - 1),
      };
    
    case 'yesterday':
      const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000);
      return {
        start: yesterday,
        end: new Date(yesterday.getTime() + 24 * 60 * 60 * 1000 - 1),
      };
    
    case '7d':
      return {
        start: new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000),
        end: new Date(today.getTime() + 24 * 60 * 60 * 1000 - 1),
      };
    
    case '30d':
      return {
        start: new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000),
        end: new Date(today.getTime() + 24 * 60 * 60 * 1000 - 1),
      };
    
    case 'mtd':
      const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
      return {
        start: monthStart,
        end: new Date(today.getTime() + 24 * 60 * 60 * 1000 - 1),
      };
    
    case 'qtd':
      const quarter = Math.floor(now.getMonth() / 3);
      const quarterStart = new Date(now.getFullYear(), quarter * 3, 1);
      return {
        start: quarterStart,
        end: new Date(today.getTime() + 24 * 60 * 60 * 1000 - 1),
      };
    
    case 'ytd':
      const yearStart = new Date(now.getFullYear(), 0, 1);
      return {
        start: yearStart,
        end: new Date(today.getTime() + 24 * 60 * 60 * 1000 - 1),
      };
    
    default:
      throw new Error(`Invalid time period: ${period}`);
  }
}

/**
 * Format date for display
 */
export function formatDate(date: Date, format: 'short' | 'long' | 'time' = 'short'): string {
  switch (format) {
    case 'short':
      return date.toLocaleDateString();
    case 'long':
      return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    case 'time':
      return date.toLocaleTimeString();
    default:
      return date.toISOString();
  }
}

/**
 * Calculate time difference in human-readable format
 */
export function timeAgo(date: Date): string {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSeconds = Math.floor(diffMs / 1000);
  const diffMinutes = Math.floor(diffSeconds / 60);
  const diffHours = Math.floor(diffMinutes / 60);
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffSeconds < 60) {
    return `${diffSeconds} seconds ago`;
  } else if (diffMinutes < 60) {
    return `${diffMinutes} minutes ago`;
  } else if (diffHours < 24) {
    return `${diffHours} hours ago`;
  } else if (diffDays < 7) {
    return `${diffDays} days ago`;
  } else {
    return formatDate(date, 'short');
  }
}

/**
 * Generate a random string for IDs
 */
export function generateId(length: number = 8): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * Retry a function with exponential backoff
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error;
  
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      
      if (i === maxRetries) {
        throw lastError;
      }
      
      const delay = baseDelay * Math.pow(2, i);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError!;
}

/**
 * Sanitize string for database storage
 */
export function sanitizeString(str: string): string {
  return str.replace(/[<>]/g, '').trim();
}

/**
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate Shopify domain format
 */
export function isValidShopifyDomain(domain: string): boolean {
  const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com$/;
  return domainRegex.test(domain);
}

/**
 * Extract shop domain from Shopify URL
 */
export function extractShopDomain(url: string): string | null {
  const match = url.match(/([a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com)/);
  return match ? match[1] : null;
}

/**
 * Convert bytes to human readable format
 */
export function formatBytes(bytes: number, decimals: number = 2): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Deep clone an object
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime()) as unknown as T;
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as unknown as T;
  if (typeof obj === 'object') {
    const clonedObj = {} as T;
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key]);
      }
    }
    return clonedObj;
  }
  return obj;
}

/**
 * Sleep for a specified number of milliseconds
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
