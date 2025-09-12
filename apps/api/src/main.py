from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

load_dotenv()

app = Flask(__name__)

# Environment variables
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')
SHOPIFY_WEBHOOK_SECRET = os.getenv('SHOPIFY_WEBHOOK_SECRET')

def generate_mock_orders():
    """Generate mock order data for testing"""
    orders = []
    for i in range(20):
        subtotal = round(random.uniform(50, 500), 2)
        orders.append({
            'id': 1000 + i,
            'name': f'#{1000 + i}',
            'subtotal_price': str(subtotal),
            'total_price': str(subtotal + 10),  # Add shipping
            'financial_status': random.choice(['paid', 'pending', 'partially_paid']),
            'created_at': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            'customer': {
                'first_name': f'Customer{i}',
                'last_name': 'Test'
            }
        })
    return orders

def calculate_profit(order):
    """Calculate profit for a single order"""
    subtotal = float(order.get('subtotal_price', 0))
    
    # COGS estimation (40% of subtotal)
    cogs = subtotal * 0.40
    
    # Processing fees (2.9% + $0.30)
    processing_fee = (subtotal * 0.029) + 0.30
    
    # Shipping cost
    shipping_cost = 10.0
    
    # Ad spend (placeholder)
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
        "message": "ProfitPeek API - Working Version",
        "status": "healthy",
        "version": "6.0.0",
        "api_key_loaded": bool(SHOPIFY_API_KEY),
        "webhook_secret_loaded": bool(SHOPIFY_WEBHOOK_SECRET),
        "endpoints": {
            "dashboard": "/api/dashboard?shop=your-shop.myshopify.com",
            "profit_analysis": "/api/profit-analysis?shop=your-shop.myshopify.com",
            "daily_digest": "/api/daily-digest?shop=your-shop.myshopify.com",
            "test": "/test"
        }
    })

@app.route('/test')
def test():
    return jsonify({"message": "Test endpoint working!", "status": "success"})

@app.route('/api/dashboard')
def get_dashboard():
    shop = request.args.get('shop', 'demo-shop.myshopify.com')
    
    # Generate mock data
    orders = generate_mock_orders()
    
    # Calculate metrics
    total_revenue = sum(float(order.get('subtotal_price', 0)) for order in orders)
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
    shop = request.args.get('shop', 'demo-shop.myshopify.com')
    
    # Generate mock data
    orders = generate_mock_orders()
    
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
    shop = request.args.get('shop', 'demo-shop.myshopify.com')
    
    # Generate yesterday's mock data
    yesterday_orders = generate_mock_orders()[:5]  # Simulate fewer orders yesterday
    
    # Calculate daily metrics
    daily_revenue = sum(float(order.get('subtotal_price', 0)) for order in yesterday_orders)
    daily_orders = len(yesterday_orders)
    daily_profit = sum(calculate_profit(order)['net_profit'] for order in yesterday_orders)
    
    digest_data = {
        "date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
        "revenue": round(daily_revenue, 2),
        "orders": daily_orders,
        "profit": round(daily_profit, 2),
        "margin": round((daily_profit / daily_revenue * 100) if daily_revenue > 0 else 0, 2)
    }
    
    return jsonify({
        "message": "Daily digest generated successfully",
        "shop": shop,
        "digest": digest_data,
        "note": "Mock data - OAuth integration needed for real data"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
