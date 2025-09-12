from flask import Flask, jsonify, request, redirect
import os

app = Flask(__name__)

# Shopify OAuth
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY', 'your_api_key')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET', 'your_api_secret')
SHOPIFY_REDIRECT_URI = os.getenv('SHOPIFY_REDIRECT_URI', 'https://profitpeek-dashboard.onrender.com/auth/callback')

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

@app.route('/auth/start')
def auth_start():
    shop = request.args.get('shop')
    if not shop:
        return jsonify({"error": "Shop parameter required"}), 400
    
    # Generate Shopify OAuth URL
    auth_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope=read_orders,read_products&redirect_uri={SHOPIFY_REDIRECT_URI}"
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    shop = request.args.get('shop')
    
    if not code or not shop:
        return jsonify({"error": "Missing code or shop parameter"}), 400
    
    # For now, just return success
    return jsonify({
        "message": "OAuth successful",
        "shop": shop,
        "code": code
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
