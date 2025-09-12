import { z } from 'zod';

// Shopify webhook schemas
export const ShopifyOrderSchema = z.object({
  id: z.number(),
  order_number: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
  processed_at: z.string().optional(),
  currency: z.string(),
  presentment_currency: z.string(),
  total_price: z.string(),
  total_discounts: z.string(),
  total_tax: z.string(),
  total_duties: z.string().optional(),
  total_shipping_price_set: z.object({
    shop_money: z.object({
      amount: z.string(),
      currency_code: z.string(),
    }),
    presentment_money: z.object({
      amount: z.string(),
      currency_code: z.string(),
    }),
  }),
  financial_status: z.string(),
  fulfillment_status: z.string().nullable(),
  customer: z.object({
    id: z.number(),
  }).optional(),
  line_items: z.array(z.object({
    id: z.number(),
    product_id: z.number(),
    variant_id: z.number(),
    inventory_item_id: z.number(),
    quantity: z.number(),
    price: z.string(),
    price_set: z.object({
      shop_money: z.object({
        amount: z.string(),
        currency_code: z.string(),
      }),
      presentment_money: z.object({
        amount: z.string(),
        currency_code: z.string(),
      }),
    }),
    discount_allocations: z.array(z.object({
      amount: z.string(),
      amount_set: z.object({
        shop_money: z.object({
          amount: z.string(),
          currency_code: z.string(),
        }),
        presentment_money: z.object({
          amount: z.string(),
          currency_code: z.string(),
        }),
      }),
      discount_application_index: z.number(),
    })),
  })),
  refunds: z.array(z.object({
    id: z.number(),
    created_at: z.string(),
    refund_line_items: z.array(z.object({
      id: z.number(),
      line_item_id: z.number(),
      quantity: z.number(),
      restock_type: z.string(),
      subtotal: z.string(),
      total_tax: z.string(),
      subtotal_set: z.object({
        shop_money: z.object({
          amount: z.string(),
          currency_code: z.string(),
        }),
        presentment_money: z.object({
          amount: z.string(),
          currency_code: z.string(),
        }),
      }),
      total_tax_set: z.object({
        shop_money: z.object({
          amount: z.string(),
          currency_code: z.string(),
        }),
        presentment_money: z.object({
          amount: z.string(),
          currency_code: z.string(),
        }),
      }),
    })),
  })),
  transactions: z.array(z.object({
    id: z.number(),
    gateway: z.string(),
    status: z.string(),
    amount: z.string(),
    processed_at: z.string().optional(),
    currency: z.string(),
    parent_id: z.number().optional(),
    kind: z.string(),
    authorization: z.string().optional(),
    authorization_expires_at: z.string().optional(),
    created_at: z.string(),
    updated_at: z.string(),
  })),
});

export const ShopifyRefundSchema = z.object({
  id: z.number(),
  order_id: z.number(),
  created_at: z.string(),
  note: z.string().optional(),
  user_id: z.number().optional(),
  processed_at: z.string().optional(),
  restock: z.boolean(),
  admin_graphql_api_id: z.string(),
  refund_line_items: z.array(z.object({
    id: z.number(),
    line_item_id: z.number(),
    quantity: z.number(),
    restock_type: z.string(),
    subtotal: z.string(),
    total_tax: z.string(),
    subtotal_set: z.object({
      shop_money: z.object({
        amount: z.string(),
        currency_code: z.string(),
      }),
      presentment_money: z.object({
        amount: z.string(),
        currency_code: z.string(),
      }),
    }),
    total_tax_set: z.object({
      shop_money: z.object({
        amount: z.string(),
        currency_code: z.string(),
      }),
      presentment_money: z.object({
        amount: z.string(),
        currency_code: z.string(),
      }),
    }),
  })),
});

export const ShopifyTransactionSchema = z.object({
  id: z.number(),
  order_id: z.number(),
  kind: z.string(),
  gateway: z.string(),
  status: z.string(),
  message: z.string().optional(),
  created_at: z.string(),
  test: z.boolean(),
  authorization: z.string().optional(),
  location_id: z.number().optional(),
  user_id: z.number().optional(),
  parent_id: z.number().optional(),
  device_id: z.number().optional(),
  receipt: z.object({
    testcase: z.boolean(),
    authorization: z.string(),
  }).optional(),
  amount: z.string(),
  currency: z.string(),
  currency_exchange_adjustment: z.object({
    adjustment: z.string(),
    original_amount: z.string(),
    final_amount: z.string(),
    currency: z.string(),
  }).optional(),
  fee: z.string().optional(),
  processed_at: z.string().optional(),
  source_name: z.string().optional(),
  source_url: z.string().optional(),
  authorization_expires_at: z.string().optional(),
  admin_graphql_api_id: z.string(),
});

// API request/response schemas
export const DashboardSummaryRequestSchema = z.object({
  period: z.enum(['today', 'yesterday', '7d', 'mtd']),
  shop_id: z.string().optional(),
});

export const SettingsUpdateSchema = z.object({
  fee_default_pct: z.number().min(0).max(100).optional(),
  fee_overrides: z.record(z.string(), z.number().min(0).max(100)).optional(),
  shipping_cost_rule: z.object({
    type: z.enum(['flat', 'percentage']),
    value: z.number().min(0),
    currency: z.string().optional(),
  }).optional(),
  digest_local_time: z.string().optional(),
  ad_spend_channels: z.array(z.string()).optional(),
});

export const CostImportSchema = z.object({
  variant_id: z.string(),
  unit_cost: z.number().min(0),
  effective_date: z.string().datetime().optional(),
  currency: z.string().optional(),
});

export const AdSpendInputSchema = z.object({
  date: z.string().date(),
  channel: z.string(),
  amount: z.number().min(0),
  currency: z.string().optional(),
});

// Webhook validation schemas
export const WebhookHeadersSchema = z.object({
  'x-shopify-hmac-sha256': z.string(),
  'x-shopify-shop-domain': z.string(),
  'x-shopify-topic': z.string(),
  'x-shopify-api-version': z.string(),
});

export const WebhookPayloadSchema = z.object({
  id: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
  number: z.number().optional(),
  order_number: z.number().optional(),
  email: z.string().optional(),
  phone: z.string().optional(),
  test: z.boolean().optional(),
  closed_at: z.string().optional(),
  processed_at: z.string().optional(),
  cancelled_at: z.string().optional(),
  cancel_reason: z.string().optional(),
  tags: z.string().optional(),
  note: z.string().optional(),
  token: z.string(),
  gateway: z.string().optional(),
  total_price: z.string(),
  subtotal_price: z.string(),
  total_weight: z.number().optional(),
  total_tax: z.string(),
  taxes_included: z.boolean().optional(),
  currency: z.string(),
  financial_status: z.string(),
  confirmed: z.boolean().optional(),
  total_discounts: z.string(),
  buyer_accepts_marketing: z.boolean().optional(),
  name: z.string(),
  referring_site: z.string().optional(),
  landing_site: z.string().optional(),
  reference: z.string().optional(),
  user_id: z.number().optional(),
  location_id: z.number().optional(),
  source_identifier: z.string().optional(),
  source_url: z.string().optional(),
  processed_at: z.string().optional(),
  device_id: z.number().optional(),
  phone: z.string().optional(),
  customer_locale: z.string().optional(),
  app_id: z.number().optional(),
  browser_ip: z.string().optional(),
  landing_site_ref: z.string().optional(),
  order_number: z.number().optional(),
  checkout_token: z.string().optional(),
  reference: z.string().optional(),
  source_name: z.string().optional(),
  source_url: z.string().optional(),
  total_duties: z.string().optional(),
  presentment_currency: z.string().optional(),
  total_shipping_price_set: z.object({
    shop_money: z.object({
      amount: z.string(),
      currency_code: z.string(),
    }),
    presentment_money: z.object({
      amount: z.string(),
      currency_code: z.string(),
    }),
  }).optional(),
  admin_graphql_api_id: z.string(),
  line_items: z.array(z.any()).optional(),
  shipping_lines: z.array(z.any()).optional(),
  billing_address: z.any().optional(),
  shipping_address: z.any().optional(),
  fulfillments: z.array(z.any()).optional(),
  refunds: z.array(z.any()).optional(),
  payment_gateway_names: z.array(z.string()).optional(),
  discount_applications: z.array(z.any()).optional(),
  discount_codes: z.array(z.any()).optional(),
  note_attributes: z.array(z.any()).optional(),
  customer: z.any().optional(),
});

// Type exports
export type ShopifyOrder = z.infer<typeof ShopifyOrderSchema>;
export type ShopifyRefund = z.infer<typeof ShopifyRefundSchema>;
export type ShopifyTransaction = z.infer<typeof ShopifyTransactionSchema>;
export type DashboardSummaryRequest = z.infer<typeof DashboardSummaryRequestSchema>;
export type SettingsUpdate = z.infer<typeof SettingsUpdateSchema>;
export type CostImport = z.infer<typeof CostImportSchema>;
export type AdSpendInput = z.infer<typeof AdSpendInputSchema>;
export type WebhookHeaders = z.infer<typeof WebhookHeadersSchema>;
export type WebhookPayload = z.infer<typeof WebhookPayloadSchema>;
