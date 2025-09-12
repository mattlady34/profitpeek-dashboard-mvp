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
