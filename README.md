# ProfitPeek - Real-time Profit Dashboard

A comprehensive real-time profit dashboard for Shopify merchants that provides trustworthy profit insights within 60 seconds of order payment.

## Features

- **Real-time Profit Tracking**: Get instant profit insights as orders come in with sub-60 second latency
- **Accurate Profit Calculation**: Track true profit with COGS, fees, shipping costs, and ad spend included
- **Order Drill-down**: Dive deep into individual orders to understand profit drivers and margins
- **Daily Digest**: Automated daily summaries comparing yesterday vs. 7/30-day averages
- **Data Health Monitoring**: Transparent data quality metrics and recommendations for improvement
- **90-day Backfill**: Automatically import and process your last 90 days of order data

## Tech Stack

### Backend (FastAPI)
- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Primary database for storing orders, profit data, and settings
- **Redis** - Caching and job queue for webhook processing
- **SQLAlchemy** - ORM for database operations
- **Celery** - Background task processing
- **Shopify Python API** - Integration with Shopify's GraphQL API

### Frontend (Next.js)
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **SWR** - Data fetching and caching
- **Recharts** - Data visualization
- **React Hook Form** - Form handling

### Infrastructure
- **Docker Compose** - Local development environment
- **MinIO** - S3-compatible object storage for bulk data
- **Postmark/SES** - Email delivery for daily digests

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose
- Shopify Partner account

### 1. Clone and Install

```bash
git clone <repository-url>
cd profitpeek-dashboard
npm install
```

### 2. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
# Required: Shopify API credentials, database URLs, etc.
```

### 3. Start Infrastructure

```bash
# Start PostgreSQL, Redis, and MinIO
docker-compose up -d

# Wait for services to be ready (about 30 seconds)
```

### 4. Setup Backend

```bash
cd apps/api

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the API server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Setup Frontend

```bash
cd apps/web

# Install dependencies
npm install

# Start the development server
npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Shopify App Setup

### 1. Create Shopify App

1. Go to your Shopify Partner Dashboard
2. Create a new app
3. Set the app URL to `https://your-domain.com`
4. Set the redirect URI to `https://your-domain.com/auth/callback`

### 2. Configure Webhooks

The app will automatically register these webhooks:
- `orders/create`
- `orders/updated`
- `orders/paid`
- `orders/cancelled`
- `orders/fulfilled`
- `orders/partially_fulfilled`
- `refunds/create`
- `transactions/create`

### 3. Required Scopes

- `read_orders`
- `read_products`
- `read_inventory`
- `read_customers`
- `read_analytics`

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://profitpeek:profitpeek_dev@localhost:5432/profitpeek
REDIS_URL=redis://localhost:6379

# Shopify App
SHOPIFY_API_KEY=your_shopify_api_key
SHOPIFY_API_SECRET=your_shopify_api_secret
SHOPIFY_WEBHOOK_SECRET=your_webhook_secret
SHOPIFY_APP_URL=https://your-app-domain.com
SHOPIFY_REDIRECT_URI=https://your-app-domain.com/auth/callback

# Email
SMTP_HOST=smtp.postmarkapp.com
SMTP_PORT=587
SMTP_USER=your_smtp_user
SMTP_PASSWORD=your_smtp_password
FROM_EMAIL=noreply@profitpeek.com

# Security
JWT_SECRET=your_jwt_secret_key_here
ENCRYPTION_KEY=your_32_byte_encryption_key
```

## Development

### Project Structure

```
profitpeek-dashboard/
├── apps/
│   ├── api/                 # FastAPI backend
│   │   ├── src/
│   │   │   ├── auth/        # Authentication
│   │   │   ├── webhooks/    # Webhook handlers
│   │   │   ├── services/    # Business logic
│   │   │   ├── routes/      # API endpoints
│   │   │   └── db/          # Database models
│   │   └── requirements.txt
│   └── web/                 # Next.js frontend
│       ├── src/
│       │   ├── app/         # App Router pages
│       │   ├── components/  # React components
│       │   ├── hooks/       # Custom hooks
│       │   └── lib/         # Utilities
│       └── package.json
├── packages/
│   └── shared/              # Shared types and utilities
└── docker-compose.yml
```

### Running Tests

```bash
# Backend tests
cd apps/api
pytest

# Frontend tests
cd apps/web
npm test
```

### Code Quality

```bash
# Lint and format
npm run lint
npm run format

# Type checking
npm run type-check
```

## Deployment

### Production Checklist

- [ ] Set up production database (PostgreSQL)
- [ ] Configure Redis for production
- [ ] Set up S3-compatible storage
- [ ] Configure email service (Postmark/SES)
- [ ] Set up monitoring and logging
- [ ] Configure SSL certificates
- [ ] Set up CI/CD pipeline
- [ ] Configure backup strategy

### Docker Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## API Documentation

### Authentication

All API endpoints require authentication via JWT token in the Authorization header:

```bash
Authorization: Bearer <your-jwt-token>
```

### Key Endpoints

- `GET /dashboard/summary?period=today` - Get dashboard summary
- `GET /orders/{order_id}` - Get order details with profit breakdown
- `GET /dashboard/health` - Get data health metrics
- `POST /webhooks/*` - Shopify webhook endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@profitpeek.com or join our Discord community.

## Roadmap

- [ ] Advanced analytics and reporting
- [ ] Multi-currency support
- [ ] Slack integration
- [ ] Mobile app
- [ ] API rate limiting
- [ ] Advanced cost tracking
- [ ] Profit forecasting
- [ ] Custom dashboards
