// Core business types for ProfitPeek

export interface Shop {
  id: string;
  shop_domain: string;
  access_token: string;
  timezone: string;
  currency: string;
  email: string;
  plan: string;
  scopes: string[];
  created_at: Date;
  updated_at: Date;
}

export interface Order {
  id: string;
  shop_id: string;
  shop_order_id: string;
  created_at: Date;
  processed_at: Date;
  currency: string;
  presentment_currency: string;
  current_total_price: number;
  current_total_discounts: number;
  current_total_tax: number;
  current_total_duties: number;
  current_total_shipping_price_set: ShippingPriceSet;
  financial_status: FinancialStatus;
  fulfillment_status: FulfillmentStatus;
  customer_id?: string;
  flags: OrderFlags;
}

export interface OrderLine {
  id: string;
  shop_id: string;
  order_id: string;
  line_id: string;
  product_id: string;
  variant_id: string;
  inventory_item_id: string;
  quantity: number;
  price_set: PriceSet;
  discount_allocations: DiscountAllocation[];
  presentment_currency: string;
  shop_currency: string;
  effective_unit_cost?: number;
  cost_source: CostSource;
  created_at: Date;
}

export interface RefundLine {
  id: string;
  shop_id: string;
  order_id: string;
  line_id: string;
  refunded_quantity: number;
  refunded_amount_set: PriceSet;
  created_at: Date;
}

export interface Transaction {
  id: string;
  shop_id: string;
  order_id: string;
  gateway: string;
  status: TransactionStatus;
  amount_set: PriceSet;
  processed_at: Date;
}

export interface TransactionFee {
  id: string;
  shop_id: string;
  transaction_id: string;
  fee_amount_set: PriceSet;
  currency: string;
  presentment_currency: string;
  estimated: boolean;
  created_at: Date;
}

export interface InventoryItemCostSnapshot {
  id: string;
  shop_id: string;
  inventory_item_id: string;
  effective_date: Date;
  unit_cost: number;
  currency: string;
  source: CostSource;
  created_at: Date;
}

export interface DailyRollup {
  id: string;
  shop_id: string;
  date: Date;
  net_revenue: number;
  cogs: number;
  fees: number;
  shipping_cost: number;
  ad_spend: Record<string, number>;
  net_profit: number;
  margin_pct: number;
  created_at: Date;
  updated_at: Date;
}

export interface AdSpendDaily {
  id: string;
  shop_id: string;
  date: Date;
  channel: string;
  amount: number;
  currency: string;
  created_at: Date;
}

export interface WebhookEvent {
  id: string;
  shop_id: string;
  topic: string;
  shop_resource_id: string;
  received_at: Date;
  processed_at?: Date;
  dedup_key: string;
  status: WebhookStatus;
  error?: string;
}

export interface Settings {
  id: string;
  shop_id: string;
  fee_default_pct: number;
  fee_overrides: Record<string, number>;
  shipping_cost_rule: ShippingCostRule;
  digest_local_time: string;
  ad_spend_channels: string[];
  updated_at: Date;
}

// Supporting types
export interface PriceSet {
  shop_money: Money;
  presentment_money: Money;
}

export interface Money {
  amount: string;
  currency_code: string;
}

export interface ShippingPriceSet {
  shop_money: Money;
  presentment_money: Money;
}

export interface DiscountAllocation {
  amount: PriceSet;
  discount_application_index: number;
}

export interface ShippingCostRule {
  type: 'flat' | 'percentage';
  value: number;
  currency?: string;
}

export interface OrderFlags {
  fees_estimated?: boolean;
  no_unit_cost?: boolean;
  multi_currency?: boolean;
  has_refunds?: boolean;
}

// Enums
export type FinancialStatus = 
  | 'pending'
  | 'authorized'
  | 'partially_paid'
  | 'paid'
  | 'partially_refunded'
  | 'refunded'
  | 'voided';

export type FulfillmentStatus = 
  | 'fulfilled'
  | 'null'
  | 'partial'
  | 'restocked';

export type TransactionStatus = 
  | 'pending'
  | 'failure'
  | 'success'
  | 'error';

export type CostSource = 
  | 'snapshot'
  | 'csv'
  | 'api'
  | 'null';

export type WebhookStatus = 
  | 'pending'
  | 'processing'
  | 'completed'
  | 'failed';

// API Response types
export interface DashboardSummary {
  period: string;
  net_revenue: number;
  cogs: number;
  fees: number;
  shipping_cost: number;
  ad_spend: number;
  net_profit: number;
  margin_pct: number;
  orders_count: number;
  aov: number;
  computed_at: Date;
  currency: string;
  flags: {
    fees_estimated: boolean;
    missing_costs: boolean;
    data_health_score: number;
  };
}

export interface OrderDetail {
  order: Order;
  lines: OrderLine[];
  refunds: RefundLine[];
  transactions: Transaction[];
  fees: TransactionFee[];
  profit_breakdown: {
    net_revenue: number;
    cogs: number;
    fees: number;
    shipping_cost: number;
    ad_spend: number;
    net_profit: number;
    margin_pct: number;
  };
  flags: OrderFlags;
}

export interface DataHealthMetrics {
  total_orders: number;
  orders_with_estimated_fees: number;
  orders_missing_unit_costs: number;
  webhook_lag_p95: number;
  data_completeness_score: number;
  last_updated: Date;
}
