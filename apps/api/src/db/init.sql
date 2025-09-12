-- Initialize ProfitPeek database
-- This file is used by Docker Compose to set up the initial database

-- Create database if it doesn't exist (handled by POSTGRES_DB env var)
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for better performance
-- These will be created after tables are created by SQLAlchemy

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE profitpeek TO profitpeek;
