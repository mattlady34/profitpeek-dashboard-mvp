from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Environment variables
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')
SHOPIFY_WEBHOOK_SECRET = os.getenv('SHOPIFY_WEBHOOK_SECRET')

@app.route('/')
def home():
    return jsonify({
        "message": "ProfitPeek API - Simple Version",
        "status": "healthy",
        "version": "5.0.0",
        "api_key_loaded": bool(SHOPIFY_API_KEY),
        "webhook_secret_loaded": bool(SHOPIFY_WEBHOOK_SECRET),
        "endpoints": {
            "auth": "/auth/start?shop=your-shop.myshopify.com",
            "test": "/test",
            "dashboard": "/api/dashboard?shop=your-shop.myshopify.com"
        }
    })

@app.route('/test')
def test():
    return jsonify({"message": "Test endpoint working!", "status": "success"})

@app.route('/auth/start')
def auth_start():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    # Generate OAuth URL
    oauth_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope=read_orders,read_products,read_customers&redirect_uri=https://profitpeek-dashboard.onrender.com/auth/callback"
    
    return jsonify({
        "message": "OAuth URL generated",
        "shop": shop,
        "oauth_url": oauth_url
    })

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    shop = request.args.get('shop')
    
    return jsonify({
        "message": "OAuth callback received",
        "shop": shop,
        "code": code,
        "note": "In production, exchange code for access token"
    })

@app.route('/api/dashboard')
def dashboard():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    return jsonify({
        "message": "Dashboard working!",
        "shop": shop,
        "test_data": {
            "total_revenue": 1000,
            "total_orders": 10,
            "average_order_value": 100
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
