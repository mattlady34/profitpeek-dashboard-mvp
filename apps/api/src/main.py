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
        "message": "ProfitPeek API - Rebuilt Version",
        "status": "healthy",
        "version": "3.0.0",
        "api_key_loaded": bool(SHOPIFY_API_KEY),
        "webhook_secret_loaded": bool(SHOPIFY_WEBHOOK_SECRET),
        "endpoints": {
            "test": "/test",
            "api_test": "/api/test",
            "profit_analysis": "/api/profit-analysis?shop=your-shop.myshopify.com",
            "dashboard": "/api/dashboard?shop=your-shop.myshopify.com"
        }
    })

@app.route('/test')
def test():
    return jsonify({"message": "Test endpoint working!", "status": "success"})

@app.route('/api/test')
def api_test():
    return jsonify({"message": "API test endpoint working!", "status": "success"})

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

@app.route('/api/profit-analysis')
def profit_analysis():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    return jsonify({
        "message": "Profit analysis working!",
        "shop": shop,
        "test_data": {
            "revenue": 1000,
            "cogs": 400,
            "fees": 29.30,
            "net_profit": 570.70,
            "margin": 57.07
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
