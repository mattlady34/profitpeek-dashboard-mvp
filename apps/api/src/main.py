from flask import Flask, jsonify, request, redirect
import os
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Shopify OAuth - Read from environment variables
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')
SHOPIFY_REDIRECT_URI = os.getenv('SHOPIFY_REDIRECT_URI')

# Store access tokens (in production, use a database)
store_tokens = {}

def get_access_token(shop, code):
    """Exchange authorization code for access token"""
    url = f"https://{shop}/admin/oauth/access_token"
    data = {
        'client_id': SHOPIFY_API_KEY,
        'client_secret': SHOPIFY_API_SECRET,
        'code': code
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def make_shopify_request(shop, access_token, endpoint, method='GET', data=None):
    """Make authenticated request to Shopify API"""
    url = f"https://{shop}/admin/api/2023-10/{endpoint}"
    headers = {
        'X-Shopify-Access-Token': access_token,
        'Content-Type': 'application/json'
    }
    
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/')
def home():
    return jsonify({
        "message": "ProfitPeek API",
        "version": "1.0.0",
        "status": "healthy",
        "api_key_loaded": bool(SHOPIFY_API_KEY),
        "endpoints": {
            "webhooks": "/webhooks/orders/*",
            "profit_analysis": "/api/profit-analysis?shop=your-shop.myshopify.com",
            "daily_digest": "/api/daily-digest?shop=your-shop.myshopify.com",
            "auth": "/auth/start?shop=your-shop.myshopify.com",
            "orders": "/api/orders?shop=your-shop.myshopify.com",
            "products": "/api/products?shop=your-shop.myshopify.com",
            "dashboard": "/api/dashboard?shop=your-shop.myshopify.com"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/auth/start')
def auth_start():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    if not SHOPIFY_API_KEY:
        return jsonify({"error": "SHOPIFY_API_KEY not configured"}), 500
    
    # Generate Shopify OAuth URL with real API key
    auth_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope=read_orders,read_products&redirect_uri={SHOPIFY_REDIRECT_URI}"
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    shop = request.args.get('shop')
    
    if not code or not shop:
        return jsonify({"error": "Missing code or shop parameter"}), 400
    
    # Exchange code for access token
    access_token = get_access_token(shop, code)
    if access_token:
        store_tokens[shop] = access_token
        return jsonify({
            "message": "OAuth successful",
            "shop": shop,
            "access_token": access_token[:10] + "...",  # Don't expose full token
            "dashboard_url": f"https://profitpeek-dashboard.onrender.com/dashboard?shop={shop}"
        })
    else:
        return jsonify({"error": "Failed to get access token"}), 500

@app.route('/api/orders')
def get_orders():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = store_tokens.get(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get orders from last 30 days
    orders_data = make_shopify_request(shop, access_token, 'orders.json?status=any&limit=50')
    if not orders_data:
        return jsonify({"error": "Failed to fetch orders"}), 500
    
    # Process orders for profit calculation
    orders = []
    total_revenue = 0
    total_orders = 0
    
    for order in orders_data.get('orders', []):
        order_data = {
            'id': order['id'],
            'name': order['name'],
            'created_at': order['created_at'],
            'total_price': float(order['total_price']),
            'subtotal_price': float(order['subtotal_price']),
            'total_tax': float(order['total_tax']),
            'shipping_cost': float(order.get('shipping_lines', [{}])[0].get('price', 0)),
            'currency': order['currency'],
            'financial_status': order['financial_status'],
            'line_items': []
        }
        
        # Process line items
        for item in order.get('line_items', []):
            line_item = {
                'id': item['id'],
                'title': item['title'],
                'quantity': item['quantity'],
                'price': float(item['price']),
                'total_discount': float(item.get('total_discount', 0)),
                'sku': item.get('sku', ''),
                'vendor': item.get('vendor', '')
            }
            order_data['line_items'].append(line_item)
        
        orders.append(order_data)
        total_revenue += order_data['total_price']
        total_orders += 1
    
    return jsonify({
        'orders': orders,
        'summary': {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'currency': orders[0]['currency'] if orders else 'USD'
        }
    })

@app.route('/api/products')
def get_products():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = store_tokens.get(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    products_data = make_shopify_request(shop, access_token, 'products.json?limit=50')
    if not products_data:
        return jsonify({"error": "Failed to fetch products"}), 500
    
    products = []
    for product in products_data.get('products', []):
        product_data = {
            'id': product['id'],
            'title': product['title'],
            'handle': product['handle'],
            'vendor': product['vendor'],
            'product_type': product['product_type'],
            'status': product['status'],
            'variants': []
        }
        
        for variant in product.get('variants', []):
            variant_data = {
                'id': variant['id'],
                'title': variant['title'],
                'price': float(variant['price']),
                'compare_at_price': float(variant.get('compare_at_price', 0)),
                'sku': variant.get('sku', ''),
                'inventory_quantity': variant.get('inventory_quantity', 0),
                'weight': float(variant.get('weight', 0))
            }
            product_data['variants'].append(variant_data)
        
        products.append(product_data)
    
    return jsonify({
        'products': products,
        'total_products': len(products)
    })

@app.route('/api/dashboard')
def get_dashboard_data():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = store_tokens.get(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get orders data
    orders_data = make_shopify_request(shop, access_token, 'orders.json?status=any&limit=50')
    if not orders_data:
        return jsonify({"error": "Failed to fetch dashboard data"}), 500
    
    # Calculate metrics
    orders = orders_data.get('orders', [])
    total_revenue = sum(float(order['total_price']) for order in orders)
    total_orders = len(orders)
    
    # Calculate by status
    status_counts = {}
    for order in orders:
        status = order['financial_status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Calculate recent activity (last 7 days)
    recent_orders = []
    week_ago = datetime.now() - timedelta(days=7)
    
    for order in orders:
        order_date = datetime.fromisoformat(order['created_at'].replace('Z', '+00:00'))
        if order_date >= week_ago:
            recent_orders.append({
                'id': order['id'],
                'name': order['name'],
                'total_price': float(order['total_price']),
                'created_at': order['created_at'],
                'financial_status': order['financial_status']
            })
    
    return jsonify({
        'shop': shop,
        'metrics': {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'average_order_value': total_revenue / total_orders if total_orders > 0 else 0,
            'orders_by_status': status_counts
        },
        'recent_orders': recent_orders,
        'last_updated': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Force redeploy Fri Sep 12 06:19:32 PDT 2025

@app.route('/webhooks/orders/create', methods=['POST'])
def webhook_orders_create():
    """Handle order creation webhooks"""
    try:
        # Get webhook data
        webhook_data = request.get_json()
        
        if not webhook_data:
            return jsonify({"error": "No webhook data"}), 400
        
        # Extract order information
        order = webhook_data.get('order', {})
        shop_domain = webhook_data.get('shop_domain', '')
        
        # Log the webhook (in production, store in database)
        print(f"New order webhook received for {shop_domain}: Order #{order.get('name', 'Unknown')}")
        
        # Process the order for real-time updates
        order_data = {
            'id': order.get('id'),
            'name': order.get('name'),
            'total_price': float(order.get('total_price', 0)),
            'created_at': order.get('created_at'),
            'financial_status': order.get('financial_status'),
            'shop': shop_domain
        }
        
        # In production, you would:
        # 1. Store in database
        # 2. Update real-time metrics
        # 3. Send notifications
        # 4. Trigger profit calculations
        
        return jsonify({
            "message": "Webhook processed successfully",
            "order_id": order.get('id'),
            "shop": shop_domain
        }), 200
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"error": "Webhook processing failed"}), 500

@app.route('/webhooks/orders/updated', methods=['POST'])
def webhook_orders_updated():
    """Handle order update webhooks"""
    try:
        webhook_data = request.get_json()
        order = webhook_data.get('order', {})
        shop_domain = webhook_data.get('shop_domain', '')
        
        print(f"Order updated webhook for {shop_domain}: Order #{order.get('name', 'Unknown')}")
        
        # Process order updates
        return jsonify({
            "message": "Order update processed",
            "order_id": order.get('id'),
            "shop": shop_domain
        }), 200
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"error": "Webhook processing failed"}), 500

@app.route('/webhooks/orders/paid', methods=['POST'])
def webhook_orders_paid():
    """Handle order payment webhooks"""
    try:
        webhook_data = request.get_json()
        order = webhook_data.get('order', {})
        shop_domain = webhook_data.get('shop_domain', '')
        
        print(f"Order paid webhook for {shop_domain}: Order #{order.get('name', 'Unknown')}")
        
        # Process payment - this is where you'd trigger profit calculations
        return jsonify({
            "message": "Payment processed",
            "order_id": order.get('id'),
            "shop": shop_domain
        }), 200
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"error": "Webhook processing failed"}), 500


@app.route('/api/profit-analysis')
def get_profit_analysis():
    """Get detailed profit analysis with COGS, fees, and margins"""
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = store_tokens.get(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get orders data
    orders_data = make_shopify_request(shop, access_token, 'orders.json?status=any&limit=50')
    if not orders_data:
        return jsonify({"error": "Failed to fetch orders data"}), 500
    
    orders = orders_data.get('orders', [])
    
    # Calculate profit metrics
    total_revenue = 0
    total_cogs = 0
    total_fees = 0
    total_shipping = 0
    total_tax = 0
    
    profit_breakdown = []
    
    for order in orders:
        order_revenue = float(order['total_price'])
        order_subtotal = float(order['subtotal_price'])
        order_tax = float(order['total_tax'])
        order_shipping = float(order.get('shipping_lines', [{}])[0].get('price', 0))
        
        # Estimate COGS (Cost of Goods Sold) - 40% of subtotal (adjustable)
        estimated_cogs = order_subtotal * 0.4
        
        # Estimate processing fees (2.9% + $0.30 per transaction)
        processing_fee = (order_revenue * 0.029) + 0.30
        
        # Calculate net profit
        net_profit = order_revenue - estimated_cogs - processing_fee - order_shipping - order_tax
        
        # Calculate profit margin
        profit_margin = (net_profit / order_revenue * 100) if order_revenue > 0 else 0
        
        total_revenue += order_revenue
        total_cogs += estimated_cogs
        total_fees += processing_fee
        total_shipping += order_shipping
        total_tax += order_tax
        
        profit_breakdown.append({
            'order_id': order['id'],
            'order_name': order['name'],
            'revenue': order_revenue,
            'cogs': estimated_cogs,
            'processing_fee': processing_fee,
            'shipping': order_shipping,
            'tax': order_tax,
            'net_profit': net_profit,
            'profit_margin': round(profit_margin, 2),
            'created_at': order['created_at']
        })
    
    # Calculate totals
    total_net_profit = total_revenue - total_cogs - total_fees - total_shipping - total_tax
    overall_profit_margin = (total_net_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    return jsonify({
        'shop': shop,
        'summary': {
            'total_revenue': round(total_revenue, 2),
            'total_cogs': round(total_cogs, 2),
            'total_processing_fees': round(total_fees, 2),
            'total_shipping': round(total_shipping, 2),
            'total_tax': round(total_tax, 2),
            'net_profit': round(total_net_profit, 2),
            'profit_margin': round(overall_profit_margin, 2),
            'total_orders': len(orders)
        },
        'profit_breakdown': profit_breakdown,
        'last_updated': datetime.now().isoformat()
    })


@app.route('/api/daily-digest')
def get_daily_digest():
    """Generate daily digest report"""
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    access_token = store_tokens.get(shop)
    if not access_token:
        return jsonify({"error": "Shop not authenticated. Please complete OAuth first."}), 401
    
    # Get today's orders
    today = datetime.now().strftime('%Y-%m-%d')
    orders_data = make_shopify_request(shop, access_token, f'orders.json?created_at_min={today}&status=any')
    
    if not orders_data:
        return jsonify({"error": "Failed to fetch daily data"}), 500
    
    orders = orders_data.get('orders', [])
    
    # Calculate daily metrics
    daily_revenue = sum(float(order['total_price']) for order in orders)
    daily_orders = len(orders)
    daily_aov = daily_revenue / daily_orders if daily_orders > 0 else 0
    
    # Calculate profit metrics
    daily_cogs = sum(float(order['subtotal_price']) * 0.4 for order in orders)
    daily_fees = sum((float(order['total_price']) * 0.029) + 0.30 for order in orders)
    daily_profit = daily_revenue - daily_cogs - daily_fees
    daily_margin = (daily_profit / daily_revenue * 100) if daily_revenue > 0 else 0
    
    # Get top products
    product_sales = {}
    for order in orders:
        for item in order.get('line_items', []):
            product_title = item['title']
            quantity = item['quantity']
            if product_title in product_sales:
                product_sales[product_title] += quantity
            else:
                product_sales[product_title] = quantity
    
    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Generate digest
    digest = {
        'date': today,
        'shop': shop,
        'metrics': {
            'revenue': round(daily_revenue, 2),
            'orders': daily_orders,
            'average_order_value': round(daily_aov, 2),
            'profit': round(daily_profit, 2),
            'profit_margin': round(daily_margin, 2)
        },
        'top_products': [{'product': product, 'quantity_sold': qty} for product, qty in top_products],
        'orders': [{
            'id': order['id'],
            'name': order['name'],
            'total': float(order['total_price']),
            'status': order['financial_status'],
            'created_at': order['created_at']
        } for order in orders[:10]],  # Last 10 orders
        'generated_at': datetime.now().isoformat()
    }
    
    return jsonify(digest)

@app.route('/api/send-daily-digest', methods=['POST'])
def send_daily_digest():
    """Send daily digest via email (placeholder for email service integration)"""
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    # Get daily digest data
    digest_response = get_daily_digest()
    if digest_response[1] != 200:  # Check status code
        return digest_response
    
    digest_data = digest_response[0].get_json()
    
    # In production, you would integrate with:
    # - SendGrid, Mailgun, or AWS SES for email
    # - Slack API for Slack notifications
    # - Twilio for SMS notifications
    
    # For now, just return the digest data
    return jsonify({
        "message": "Daily digest generated successfully",
        "digest": digest_data,
        "note": "Email/Slack integration needed for actual sending"
    })

