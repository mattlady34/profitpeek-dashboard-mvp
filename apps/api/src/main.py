from flask import Flask, jsonify, request, redirect
import os

app = Flask(__name__)

# Shopify OAuth - Read from environment variables
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')
SHOPIFY_REDIRECT_URI = os.getenv('SHOPIFY_REDIRECT_URI')

@app.route('/')
def home():
    return jsonify({
        "message": "ProfitPeek API",
        "version": "1.0.0",
        "status": "healthy",
        "api_key_loaded": bool(SHOPIFY_API_KEY)
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
    
    return jsonify({
        "message": "OAuth successful",
        "shop": shop,
        "code": code
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
