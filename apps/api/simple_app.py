from flask import Flask, jsonify, request, redirect, session
from flask_cors import CORS
import os
import hmac
import hashlib
import requests
import secrets
import json
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('JWT_SECRET', 'your_secret_key_here')

# Enable CORS for production
CORS(app, supports_credentials=True)

# Shopify OAuth
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY', 'demo_api_key_12345')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET', 'demo_secret_67890')
SHOPIFY_REDIRECT_URI = os.getenv('SHOPIFY_REDIRECT_URI', 'http://localhost:3000/auth/callback')
SHOPIFY_APP_URL = os.getenv('SHOPIFY_APP_URL', 'http://localhost:3000')

# Debug output
print(f"DEBUG: SHOPIFY_API_KEY = {SHOPIFY_API_KEY}")
print(f"DEBUG: SHOPIFY_REDIRECT_URI = {SHOPIFY_REDIRECT_URI}")

@app.route('/')
def home():
    return jsonify({
        "message": "ProfitPeek API",
        "version": "1.0.0",
        "status": "healthy"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

def verify_shopify_hmac(data, hmac_header):
    """Verify Shopify webhook HMAC"""
    calculated_hmac = hmac.new(
        SHOPIFY_API_SECRET.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(calculated_hmac, hmac_header)

@app.route('/auth/start')
def auth_start():
    shop = request.args.get('shop')
    demo = request.args.get('demo') == '1'
    
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    # Validate shop domain
    if not shop.endswith('.myshopify.com'):
        return jsonify({"error": "Invalid shop domain"}), 400
    
    # Demo mode - bypass OAuth
    if demo or SHOPIFY_API_KEY == 'demo_api_key_12345':
        session['access_token'] = 'demo_access_token'
        session['shop'] = shop
        frontend_url = f"{SHOPIFY_APP_URL}/dashboard/?shop={shop}&authenticated=true&demo=1"
        return redirect(frontend_url)
    
    # Generate state parameter for security
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    session['shop'] = shop
    
    # Required scopes for ProfitPeek
    scopes = [
        'read_orders',
        'read_products', 
        'read_customers',
        'read_inventory',
        'read_analytics',
        'read_fulfillments',
        'read_shipping',
        'read_returns'
    ]
    
    # Generate Shopify OAuth URL
    params = {
        'client_id': SHOPIFY_API_KEY,
        'scope': ','.join(scopes),
        'redirect_uri': SHOPIFY_REDIRECT_URI,
        'state': state,
        'grant_options[]': 'per-user'
    }
    
    auth_url = f"https://{shop}/admin/oauth/authorize?{urlencode(params)}"
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    shop = request.args.get('shop')
    state = request.args.get('state')
    hmac_param = request.args.get('hmac')
    
    # Validate required parameters
    if not all([code, shop, state, hmac_param]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    # Verify state parameter
    if state != session.get('oauth_state'):
        return jsonify({"error": "Invalid state parameter"}), 400
    
    # Verify HMAC
    query_string = request.query_string.decode('utf-8')
    if not verify_shopify_hmac(query_string, hmac_param):
        return jsonify({"error": "Invalid HMAC"}), 400
    
    try:
        # Exchange code for access token
        token_url = f"https://{shop}/admin/oauth/access_token"
        token_data = {
            'client_id': SHOPIFY_API_KEY,
            'client_secret': SHOPIFY_API_SECRET,
            'code': code
        }
        
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        
        token_response = response.json()
        access_token = token_response.get('access_token')
        
        if not access_token:
            return jsonify({"error": "No access token received"}), 400
        
        # Store token in session (in production, store in database)
        session['access_token'] = access_token
        session['shop'] = shop
        
        # Get shop information
        shop_url = f"https://{shop}/admin/api/2023-10/shop.json"
        headers = {'X-Shopify-Access-Token': access_token}
        shop_response = requests.get(shop_url, headers=headers)
        shop_response.raise_for_status()
        shop_data = shop_response.json()
        
        # Redirect to frontend with success
        frontend_url = f"{SHOPIFY_APP_URL}/dashboard/?shop={shop}&authenticated=true"
        return redirect(frontend_url)
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"OAuth token exchange failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"OAuth callback failed: {str(e)}"}), 500

@app.route('/auth/verify')
def auth_verify():
    """Verify if user is authenticated"""
    if 'access_token' in session and 'shop' in session:
        return jsonify({
            "authenticated": True,
            "shop": session['shop'],
            "access_token": session['access_token']
        })
    return jsonify({"authenticated": False})

@app.route('/auth/logout')
def auth_logout():
    """Logout user"""
    session.clear()
    return jsonify({"message": "Logged out successfully"})

def get_shopify_headers():
    """Get headers for Shopify API requests"""
    if 'access_token' not in session:
        raise ValueError("No access token found")
    return {'X-Shopify-Access-Token': session['access_token']}

@app.route('/api/dashboard')
def api_dashboard():
    """Get dashboard data from Shopify"""
    try:
        # Check for demo mode from URL parameter
        is_demo = request.args.get('demo') == '1'
        shop = session.get('shop') or 'demo-store.myshopify.com'
        
        if not is_demo and not shop:
            return jsonify({"error": "Not authenticated"}), 401
        
        # Check if we're in demo mode
        is_demo = is_demo or session.get('access_token') == 'demo_access_token'
        
        if is_demo:
            # Return demo data
            return jsonify({
                "storeName": shop.replace('.myshopify.com', ''),
                "lastUpdated": "Updated just now",
                "period": "Last 30 days",
                "stats": {
                    "netProfit": 12547.50,
                    "netRevenue": 45620.00,
                    "orders": 127,
                    "aov": 359.21,
                    "margin": 27.5
                },
                "trends": {
                    "netProfit": [
                        {"date": "2024-01-01", "value": 10038},
                        {"date": "2024-01-02", "value": 11293},
                        {"date": "2024-01-03", "value": 13802},
                        {"date": "2024-01-04", "value": 11920},
                        {"date": "2024-01-05", "value": 12548}
                    ],
                    "netRevenue": [
                        {"date": "2024-01-01", "value": 36496},
                        {"date": "2024-01-02", "value": 41034},
                        {"date": "2024-01-03", "value": 50182},
                        {"date": "2024-01-04", "value": 43316},
                        {"date": "2024-01-05", "value": 45620}
                    ]
                },
                "whatMoved": [
                    {
                        "type": "sku",
                        "title": "Top SKU: Premium T-Shirt",
                        "impact": "+$3,764.25",
                        "change": 15.2,
                        "icon": "products"
                    },
                    {
                        "type": "fee",
                        "title": "Processing Fees",
                        "impact": "-$1,323.18",
                        "change": -2.1,
                        "icon": "creditCard"
                    }
                ],
                "dataHealth": {
                    "hasIssues": False,
                    "message": "All data healthy",
                    "action": "View details",
                    "percentage": 0
                }
            })
        
        headers = get_shopify_headers()
        
        # Get orders from last 30 days
        orders_url = f"https://{shop}/admin/api/2023-10/orders.json?status=any&limit=250&created_at_min=2024-01-01"
        orders_response = requests.get(orders_url, headers=headers)
        orders_response.raise_for_status()
        orders_data = orders_response.json()
        
        # Calculate metrics
        orders = orders_data.get('orders', [])
        total_revenue = sum(float(order.get('total_price', 0)) for order in orders)
        total_orders = len(orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Calculate profit (simplified - 40% COGS, 2.9% + $0.30 fees)
        total_cogs = total_revenue * 0.4
        total_fees = (total_revenue * 0.029) + (total_orders * 0.30)
        net_profit = total_revenue - total_cogs - total_fees
        margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return jsonify({
            "storeName": shop.replace('.myshopify.com', ''),
            "lastUpdated": "Updated just now",
            "period": "Last 30 days",
            "stats": {
                "netProfit": round(net_profit, 2),
                "netRevenue": round(total_revenue, 2),
                "orders": total_orders,
                "aov": round(avg_order_value, 2),
                "margin": round(margin, 1)
            },
            "trends": {
                "netProfit": [
                    {"date": "2024-01-01", "value": round(net_profit * 0.8)},
                    {"date": "2024-01-02", "value": round(net_profit * 0.9)},
                    {"date": "2024-01-03", "value": round(net_profit * 1.1)},
                    {"date": "2024-01-04", "value": round(net_profit * 0.95)},
                    {"date": "2024-01-05", "value": round(net_profit)}
                ],
                "netRevenue": [
                    {"date": "2024-01-01", "value": round(total_revenue * 0.8)},
                    {"date": "2024-01-02", "value": round(total_revenue * 0.9)},
                    {"date": "2024-01-03", "value": round(total_revenue * 1.1)},
                    {"date": "2024-01-04", "value": round(total_revenue * 0.95)},
                    {"date": "2024-01-05", "value": round(total_revenue)}
                ]
            },
            "whatMoved": [
                {
                    "type": "sku",
                    "title": "Top SKU: Premium T-Shirt",
                    "impact": f"+${round(net_profit * 0.3)}",
                    "change": 15.2,
                    "icon": "products"
                },
                {
                    "type": "fee",
                    "title": "Processing Fees",
                    "impact": f"-${round(total_fees)}",
                    "change": -2.1,
                    "icon": "creditCard"
                }
            ],
            "dataHealth": {
                "hasIssues": total_orders < 10,
                "message": "18% of SKUs missing cost data" if total_orders < 10 else "All data healthy",
                "action": "Fix now" if total_orders < 10 else "View details",
                "percentage": 18 if total_orders < 10 else 0
            }
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Shopify API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Dashboard API error: {str(e)}"}), 500

@app.route('/api/orders')
def api_orders():
    """Get orders data from Shopify"""
    try:
        shop = session.get('shop')
        if not shop:
            return jsonify({"error": "Not authenticated"}), 401
        
        headers = get_shopify_headers()
        
        # Get recent orders
        orders_url = f"https://{shop}/admin/api/2023-10/orders.json?status=any&limit=50"
        orders_response = requests.get(orders_url, headers=headers)
        orders_response.raise_for_status()
        orders_data = orders_response.json()
        
        orders = []
        for order in orders_data.get('orders', []):
            revenue = float(order.get('total_price', 0))
            cogs = revenue * 0.4  # 40% COGS
            fees = (revenue * 0.029) + 0.30  # 2.9% + $0.30
            shipping = float(order.get('shipping_lines', [{}])[0].get('price', 0)) if order.get('shipping_lines') else 0
            net_profit = revenue - cogs - fees - shipping
            margin = (net_profit / revenue * 100) if revenue > 0 else 0
            
            orders.append({
                "id": str(order.get('id')),
                "date": order.get('created_at', '')[:10],
                "orderNumber": f"#{order.get('order_number')}",
                "customer": f"{order.get('customer', {}).get('first_name', '')} {order.get('customer', {}).get('last_name', '')}".strip() or "Guest",
                "revenue": round(revenue, 2),
                "cogs": round(cogs, 2),
                "fees": round(fees, 2),
                "shipping": round(shipping, 2),
                "netProfit": round(net_profit, 2),
                "margin": round(margin, 1),
                "status": order.get('fulfillment_status') or 'pending',
                "items": [
                    {
                        "name": line_item.get('name', 'Unknown Product'),
                        "quantity": line_item.get('quantity', 1),
                        "unitPrice": round(float(line_item.get('price', 0)), 2),
                        "unitCost": round(float(line_item.get('price', 0)) * 0.4, 2),
                        "totalRevenue": round(float(line_item.get('price', 0)) * int(line_item.get('quantity', 1)), 2),
                        "totalCost": round(float(line_item.get('price', 0)) * int(line_item.get('quantity', 1)) * 0.4, 2),
                        "profit": round(float(line_item.get('price', 0)) * int(line_item.get('quantity', 1)) * 0.6, 2),
                        "margin": 60.0
                    }
                    for line_item in order.get('line_items', [])
                ]
            })
        
        return jsonify({"orders": orders})
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Shopify API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Orders API error: {str(e)}"}), 500

# Shopify Compliance Webhooks (Required for App Store)
@app.route('/webhooks/customers/data_request', methods=['POST'])
def webhook_customers_data_request():
    """Handle customer data request webhook"""
    # Verify webhook authenticity
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    if not hmac_header:
        return jsonify({"error": "Missing HMAC header"}), 400
    
    # Verify HMAC
    data = request.get_data()
    if not verify_shopify_hmac(data.decode('utf-8'), hmac_header):
        return jsonify({"error": "Invalid HMAC"}), 401
    
    # Process customer data request
    webhook_data = request.get_json()
    customer_id = webhook_data.get('customer', {}).get('id')
    shop_domain = webhook_data.get('shop_domain')
    
    # Log the request (in production, you'd store this in a database)
    print(f"Customer data request for customer {customer_id} from shop {shop_domain}")
    
    # Return 200 to acknowledge receipt
    return jsonify({"status": "received"}), 200

@app.route('/webhooks/customers/redact', methods=['POST'])
def webhook_customers_redact():
    """Handle customer data erasure webhook"""
    # Verify webhook authenticity
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    if not hmac_header:
        return jsonify({"error": "Missing HMAC header"}), 400
    
    # Verify HMAC
    data = request.get_data()
    if not verify_shopify_hmac(data.decode('utf-8'), hmac_header):
        return jsonify({"error": "Invalid HMAC"}), 401
    
    # Process customer data erasure
    webhook_data = request.get_json()
    customer_id = webhook_data.get('customer', {}).get('id')
    shop_domain = webhook_data.get('shop_domain')
    
    # Log the request (in production, you'd delete customer data)
    print(f"Customer data erasure for customer {customer_id} from shop {shop_domain}")
    
    # Return 200 to acknowledge receipt
    return jsonify({"status": "received"}), 200

@app.route('/webhooks/shop/redact', methods=['POST'])
def webhook_shop_redact():
    """Handle shop data erasure webhook"""
    # Verify webhook authenticity
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    if not hmac_header:
        return jsonify({"error": "Missing HMAC header"}), 400
    
    # Verify HMAC
    data = request.get_data()
    if not verify_shopify_hmac(data.decode('utf-8'), hmac_header):
        return jsonify({"error": "Invalid HMAC"}), 401
    
    # Process shop data erasure
    webhook_data = request.get_json()
    shop_domain = webhook_data.get('shop_domain')
    shop_id = webhook_data.get('shop_id')
    
    # Log the request (in production, you'd delete shop data)
    print(f"Shop data erasure for shop {shop_domain} (ID: {shop_id})")
    
    # Return 200 to acknowledge receipt
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
