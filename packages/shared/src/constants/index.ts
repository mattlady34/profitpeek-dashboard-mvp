// Application constants

export const APP_NAME = 'ProfitPeek';
export const APP_VERSION = '1.0.0';

// Shopify API constants
export const SHOPIFY_API_VERSION = '2024-01';
export const SHOPIFY_SCOPES = [
  'read_orders',
  'read_products',
  'read_inventory',
  'read_customers',
  'read_analytics',
];

export const SHOPIFY_WEBHOOK_TOPICS = [
  'orders/create',
  'orders/updated',
  'orders/paid',
  'orders/cancelled',
  'orders/fulfilled',
  'orders/partially_fulfilled',
  'refunds/create',
  'transactions/create',
] as const;

// Database constants
export const DB_CONSTRAINTS = {
  MAX_RETRIES: 3,
  RETRY_DELAY_MS: 1000,
  BATCH_SIZE: 1000,
  CONNECTION_TIMEOUT_MS: 30000,
} as const;

// Redis constants
export const REDIS_KEYS = {
  WEBHOOK_QUEUE: 'webhook:queue',
  BACKFILL_QUEUE: 'backfill:queue',
  RECONCILE_QUEUE: 'reconcile:queue',
  EMAIL_QUEUE: 'email:queue',
  CACHE_PREFIX: 'profitpeek:cache',
  SESSION_PREFIX: 'profitpeek:session',
} as const;

export const REDIS_TTL = {
  SESSION: 24 * 60 * 60, // 24 hours
  CACHE: 60, // 1 minute
  RATE_LIMIT: 60, // 1 minute
} as const;

// Business logic constants
export const PROFIT_CALCULATION = {
  DEFAULT_FEE_PERCENTAGE: 2.9, // Default processing fee
  DEFAULT_FEE_FIXED: 0.30, // Default fixed fee
  MIN_MARGIN_THRESHOLD: 0.1, // 10% minimum margin warning
  CURRENCY_PRECISION: 2,
} as const;

export const DATA_HEALTH_THRESHOLDS = {
  MISSING_COSTS_WARNING: 0.1, // 10% of items missing costs
  MISSING_COSTS_CRITICAL: 0.2, // 20% of items missing costs
  ESTIMATED_FEES_WARNING: 0.05, // 5% of orders with estimated fees
  ESTIMATED_FEES_CRITICAL: 0.25, // 25% of orders with estimated fees
  WEBHOOK_LAG_WARNING_MS: 60000, // 1 minute
  WEBHOOK_LAG_CRITICAL_MS: 300000, // 5 minutes
} as const;

// Time periods
export const TIME_PERIODS = {
  TODAY: 'today',
  YESTERDAY: 'yesterday',
  LAST_7_DAYS: '7d',
  LAST_30_DAYS: '30d',
  MONTH_TO_DATE: 'mtd',
  QUARTER_TO_DATE: 'qtd',
  YEAR_TO_DATE: 'ytd',
} as const;

// Currency codes
export const SUPPORTED_CURRENCIES = [
  'USD', 'CAD', 'EUR', 'GBP', 'AUD', 'JPY', 'CHF', 'SEK', 'NOK', 'DKK',
  'PLN', 'CZK', 'HUF', 'BGN', 'RON', 'HRK', 'RUB', 'TRY', 'BRL', 'MXN',
  'ARS', 'CLP', 'COP', 'PEN', 'UYU', 'VEF', 'ZAR', 'EGP', 'MAD', 'TND',
  'DZD', 'NGN', 'KES', 'UGX', 'TZS', 'GHS', 'XOF', 'XAF', 'CDF', 'AOA',
  'INR', 'PKR', 'BDT', 'LKR', 'NPR', 'AFN', 'KZT', 'UZS', 'KGS', 'TJS',
  'MNT', 'CNY', 'HKD', 'SGD', 'KRW', 'TWD', 'THB', 'VND', 'IDR', 'MYR',
  'PHP', 'MMK', 'LAK', 'KHR', 'BND', 'FJD', 'PGK', 'SBD', 'VUV', 'WST',
  'TOP', 'NZD', 'XPF', 'NOK', 'DKK', 'SEK', 'ISK', 'CHF', 'EUR', 'GBP',
] as const;

// Error codes
export const ERROR_CODES = {
  // Authentication
  INVALID_TOKEN: 'INVALID_TOKEN',
  TOKEN_EXPIRED: 'TOKEN_EXPIRED',
  INSUFFICIENT_SCOPES: 'INSUFFICIENT_SCOPES',
  
  // Shopify API
  SHOPIFY_RATE_LIMIT: 'SHOPIFY_RATE_LIMIT',
  SHOPIFY_UNAUTHORIZED: 'SHOPIFY_UNAUTHORIZED',
  SHOPIFY_NOT_FOUND: 'SHOPIFY_NOT_FOUND',
  SHOPIFY_INTERNAL_ERROR: 'SHOPIFY_INTERNAL_ERROR',
  
  // Webhooks
  INVALID_WEBHOOK_SIGNATURE: 'INVALID_WEBHOOK_SIGNATURE',
  WEBHOOK_PROCESSING_FAILED: 'WEBHOOK_PROCESSING_FAILED',
  DUPLICATE_WEBHOOK: 'DUPLICATE_WEBHOOK',
  
  // Data processing
  INVALID_ORDER_DATA: 'INVALID_ORDER_DATA',
  MISSING_REQUIRED_FIELD: 'MISSING_REQUIRED_FIELD',
  CALCULATION_ERROR: 'CALCULATION_ERROR',
  
  // Database
  DATABASE_CONNECTION_ERROR: 'DATABASE_CONNECTION_ERROR',
  DATABASE_QUERY_ERROR: 'DATABASE_QUERY_ERROR',
  CONSTRAINT_VIOLATION: 'CONSTRAINT_VIOLATION',
  
  // External services
  EMAIL_SEND_FAILED: 'EMAIL_SEND_FAILED',
  SLACK_SEND_FAILED: 'SLACK_SEND_FAILED',
  S3_UPLOAD_FAILED: 'S3_UPLOAD_FAILED',
} as const;

// Feature flags
export const FEATURE_FLAGS = {
  ENABLE_SLACK_DIGEST: 'ENABLE_SLACK_DIGEST',
  ENABLE_CSV_EXPORT: 'ENABLE_CSV_EXPORT',
  ENABLE_ADVANCED_ANALYTICS: 'ENABLE_ADVANCED_ANALYTICS',
  ENABLE_MULTI_CURRENCY: 'ENABLE_MULTI_CURRENCY',
  ENABLE_LLM_DIGEST: 'ENABLE_LLM_DIGEST',
} as const;

// Rate limiting
export const RATE_LIMITS = {
  WEBHOOKS_PER_MINUTE: 100,
  API_REQUESTS_PER_MINUTE: 1000,
  BULK_OPERATIONS_PER_HOUR: 10,
  EMAIL_SENDS_PER_HOUR: 100,
} as const;

// File upload limits
export const UPLOAD_LIMITS = {
  MAX_FILE_SIZE_MB: 10,
  MAX_ROWS_PER_CSV: 10000,
  ALLOWED_FILE_TYPES: ['.csv', '.xlsx', '.xls'],
} as const;

// Email templates
export const EMAIL_TEMPLATES = {
  DAILY_DIGEST: 'daily_digest',
  WELCOME: 'welcome',
  DATA_HEALTH_ALERT: 'data_health_alert',
  BACKFILL_COMPLETE: 'backfill_complete',
} as const;

// Slack message templates
export const SLACK_TEMPLATES = {
  DAILY_DIGEST: 'daily_digest',
  ALERT: 'alert',
  BACKFILL_STATUS: 'backfill_status',
} as const;
