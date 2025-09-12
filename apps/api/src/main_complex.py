from flask import Flask, jsonify, request
import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Environment variables
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')
SHOPIFY_WEBHOOK_SECRET = os.getenv('SHOPIFY_WEBHOOK_SECRET')

# In-memory storage for access tokens (in production, use a database)
store_tokens = {}

def get_access_token(shop):
    """Get access token for a shop"""
    return store_tokens.get(shop)

def get_shopify_data(shop, endpoint, access_token=None):
    """Make authenticated request to Shopify API"""
    if not access_token:
        access_token = get_access_token(shop)
    
    if not access_token:
        return None
    
    url = f"https://{shop}/admin/api/2023-10/{endpoint}"
    headers = {
        'X-Shopify-Access-Token': access_token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Shopify API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error calling Shopify API: {e}")
        return None

def calculate_profit(order):
    """Calculate profit for a single order"""
    subtotal = float(order.get('subtotal_price', 0))
    
    # COGS estimation (40% of subtotal)
    cogs = subtotal * 0.40
    
    # Processing fees (2.9% + $0.30)
    processing_fee = (subtotal * 0.029) + 0.30
    
    # Shipping cost (from order data or estimate)
    shipping_cost = float(order.get('shipping_lines', [{}])[0].get('price', 0)) if order.get('shipping_lines') else 0
    
    # Ad spend (placeholder - would come from external data)
    ad_spend = 0
    
    # Net profit calculation
    net_profit = subtotal - cogs - processing_fee - shipping_cost - ad_spend
    margin = (net_profit / subtotal * 100) if subtotal > 0 else 0
    
    return {
        'order_id': order.get('id'),
        'order_name': order.get('name'),
        'subtotal': subtotal,
        'cogs': round(cogs, 2),
        'processing_fee': round(processing_fee, 2),
        'shipping_cost': shipping_cost,
        'ad_spend': ad_spend,
        'net_profit': round(net_profit, 2),
        'margin': round(margin, 2),
        'created_at': order.get('created_at')
    }

@app.route('/')
def home():
    return jsonify({
        "message": "ProfitPeek API - Production Ready",
        "status": "healthy",
        "version": "4.0.0",
        "api_key_loaded": bool(SHOPIFY_API_KEY),
        "webhook_secret_loaded": bool(SHOPIFY_WEBHOOK_SECRET),
        "endpoints": {
            "auth": "/auth/start?shop=your-shop.myshopify.com",
            "dashboard": "/api/dashboard?shop=your-shop.myshopify.com",
            "orders": "/api/orders?shop=your-shop.myshopify.com",
            "products": "/api/products?shop=your-shop.myshopify.com",
            "profit_analysis": "/api/profit-analysis?shop=your-shop.myshopify.com",
            "daily_digest": "/api/daily-digest?shop=your-shop.myshopify.com",
            "webhooks": "/webhooks/orders/*"
        }
    })

@app.route('/auth/start')
def auth_start():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    # Generate OAuth URL
    oauth_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope=read_orders,read_products,read_customers&redirect_uri={os.getenv('SHOPIFY_REDIRECT_URI')}"
    
    return jsonify({
        "message": "OAuth URL generated",
        "shop": shop,
        "oauth_url": oauth_url
    })

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    shop = request.args.get('shop')
    
    if not code or not shop:
        return jsonify({"error": "Missing code or shop parameter"}), 400
    
    # Exchange code for access token
    token_url = f"https://{shop}/admin/oauth/access_token"
    data = {
        'client_id': SHOPIFY_API_KEY,
        'client_secret': SHOPIFY_API_SECRET,
        'code': code
    }
    
    try:
        response = requests.post(token_url, json=data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            store_tokens[shop] = access_token
            
            return jsonify({
                "message": "Authentication successful",
                "shop": shop,
                "access_token": access_token[:10] + "..."  # Don't expose full token
            })
        else:
            return jsonify({"error": "Failed to get access token"}), 400
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 500

@app.route('/api/orders')
def get_orders():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = get_access_token(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get orders from Shopify
    orders_data = get_shopify_data(shop, "orders.json?limit=50", access_token)
    if not orders_data:
        return jsonify({"error": "Failed to fetch orders from Shopify"}), 500
    
    orders = orders_data.get('orders', [])
    
    return jsonify({
        "message": "Orders fetched successfully",
        "shop": shop,
        "total_orders": len(orders),
        "orders": orders[:10]  # Return first 10 orders
    })

@app.route('/api/products')
def get_products():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = get_access_token(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get products from Shopify
    products_data = get_shopify_data(shop, "products.json?limit=50", access_token)
    if not products_data:
        return jsonify({"error": "Failed to fetch products from Shopify"}), 500
    
    products = products_data.get('products', [])
    
    return jsonify({
        "message": "Products fetched successfully",
        "shop": shop,
        "total_products": len(products),
        "products": products[:10]  # Return first 10 products
    })

@app.route('/api/dashboard')
def get_dashboard():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = get_access_token(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get orders data
    orders_data = get_shopify_data(shop, "orders.json?limit=100", access_token)
    if not orders_data:
        return jsonify({"error": "Failed to fetch orders from Shopify"}), 500
    
    orders = orders_data.get('orders', [])
    
    # Calculate metrics
    total_revenue = sum(float(order.get('total_price', 0)) for order in orders)
    total_orders = len(orders)
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Orders by status
    status_counts = {}
    for order in orders:
        status = order.get('financial_status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Recent orders
    recent_orders = sorted(orders, key=lambda x: x.get('created_at', ''), reverse=True)[:5]
    
    return jsonify({
        "message": "Dashboard data fetched successfully",
        "shop": shop,
        "metrics": {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "average_order_value": round(average_order_value, 2),
            "orders_by_status": status_counts
        },
        "recent_orders": recent_orders,
        "last_updated": datetime.now().isoformat()
    })

@app.route('/api/profit-analysis')
def get_profit_analysis():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = get_access_token(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get orders data
    orders_data = get_shopify_data(shop, "orders.json?limit=100", access_token)
    if not orders_data:
        return jsonify({"error": "Failed to fetch orders from Shopify"}), 500
    
    orders = orders_data.get('orders', [])
    
    # Calculate profit for each order
    profit_data = []
    total_revenue = 0
    total_cogs = 0
    total_fees = 0
    total_net_profit = 0
    
    for order in orders:
        profit = calculate_profit(order)
        profit_data.append(profit)
        
        total_revenue += profit['subtotal']
        total_cogs += profit['cogs']
        total_fees += profit['processing_fee']
        total_net_profit += profit['net_profit']
    
    overall_margin = (total_net_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    return jsonify({
        "message": "Profit analysis completed",
        "shop": shop,
        "overall_metrics": {
            "total_revenue": round(total_revenue, 2),
            "total_cogs": round(total_cogs, 2),
            "total_fees": round(total_fees, 2),
            "total_net_profit": round(total_net_profit, 2),
            "overall_margin": round(overall_margin, 2)
        },
        "order_breakdown": profit_data[:20],  # Return first 20 orders
        "last_updated": datetime.now().isoformat()
    })

@app.route('/api/daily-digest')
def get_daily_digest():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = get_access_token(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get yesterday's orders
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')
    
    orders_data = get_shopify_data(shop, f"orders.json?created_at_min={date_str}&limit=100", access_token)
    if not orders_data:
        return jsonify({"error": "Failed to fetch orders from Shopify"}), 500
    
    orders = orders_data.get('orders', [])
    
    # Calculate daily metrics
    daily_revenue = sum(float(order.get('total_price', 0)) for order in orders)
    daily_orders = len(orders)
    daily_profit = sum(calculate_profit(order)['net_profit'] for order in orders)
    
    digest_data = {
        "date": date_str,
        "revenue": round(daily_revenue, 2),
        "orders": daily_orders,
        "profit": round(daily_profit, 2),
        "margin": round((daily_profit / daily_revenue * 100) if daily_revenue > 0 else 0, 2)
    }
    
    return jsonify({
        "message": "Daily digest generated successfully",
        "shop": shop,
        "digest": digest_data,
        "note": "Email/Slack integration needed for actual sending"
    })

# Webhook endpoints
@app.route('/webhooks/orders/create', methods=['POST'])
def webhook_order_create():
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    data = request.get_data()
    
    # Verify webhook (simplified for now)
    if not hmac_header:
        return jsonify({"error": "Missing HMAC header"}), 401
    
    order_data = json.loads(data)
    print(f"Webhook: New Order Created - {order_data.get('name')}")
    
    # In production, save to database and trigger profit calculation
    return jsonify({"status": "success", "message": "Order create webhook received"}), 200

@app.route('/webhooks/orders/updated', methods=['POST'])
def webhook_order_updated():
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    data = request.get_data()
    
    if not hmac_header:
        return jsonify({"error": "Missing HMAC header"}), 401
    
    order_data = json.loads(data)
    print(f"Webhook: Order Updated - {order_data.get('name')}")
    
    return jsonify({"status": "success", "message": "Order update webhook received"}), 200

@app.route('/webhooks/orders/paid', methods=['POST'])
def webhook_order_paid():
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    data = request.get_data()
    
    if not hmac_header:
        return jsonify({"error": "Missing HMAC header"}), 401
    
    order_data = json.loads(data)
    print(f"Webhook: Order Paid - {order_data.get('name')}")
    
    return jsonify({"status": "success", "message": "Order paid webhook received"}), 200

@app.route('/webhooks/app/uninstalled', methods=['POST'])
def webhook_app_uninstalled():
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    data = request.get_data()
    
    if not hmac_header:
        return jsonify({"error": "Missing HMAC header"}), 401
    
    shop_domain = request.headers.get('X-Shopify-Shop-Domain')
    if shop_domain in store_tokens:
        del store_tokens[shop_domain]
    
    print(f"Webhook: App Uninstalled for {shop_domain}")
    return jsonify({"status": "success", "message": "App uninstall webhook received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Force redeploy Fri Sep 12 12:54:50 PDT 2025
