#!/usr/bin/env python3

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def create_directories():
    """Create necessary directory structure"""
    directories = [
        'agentic_os',
        'agentic_os/core',
        'agentic_os/agents',
        'agentic_os/business_modules',
        'agentic_os/monitoring',
        'agentic_os/api',
        'agentic_os/web',
        'agentic_os/database',
        'data',
        'logs',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_database():
    """Initialize SQLite database"""
    db_path = "data/agentic_os.db"
    conn = sqlite3.connect(db_path)
    
    # Create main tables
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            config TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            business_id INTEGER,
            status TEXT DEFAULT 'idle',
            config TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (business_id) REFERENCES businesses (id)
        );
        
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY,
            business_id INTEGER,
            metric_name TEXT NOT NULL,
            metric_value REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (business_id) REFERENCES businesses (id)
        );
        
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            component TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conn.commit()
    conn.close()
    print(f"✓ Database initialized: {db_path}")

def create_config():
    """Create default configuration"""
    config_content = '''
# Agentic OS Configuration

DATABASE_URL=sqlite:///data/agentic_os.db
REDIS_URL=redis://localhost:6379
API_HOST=0.0.0.0
API_PORT=8080

# AI Configuration
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Business Module Configuration
SHOPIFY_API_KEY=your_shopify_key_here
STRIPE_API_KEY=your_stripe_key_here
SENDGRID_API_KEY=your_sendgrid_key_here

# Monitoring Configuration
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Security
SECRET_KEY=your_secret_key_here
'''
    
    with open('config/.env', 'w') as f:
        f.write(config_content)
    print("✓ Configuration file created: config/.env")

def main():
    print("🚀 Setting up Agentic OS...")
    print("=" * 50)
    
    try:
        create_directories()
        create_database()
        create_config()
        
        print("\n" + "=" * 50)
        print("✅ Agentic OS setup completed successfully!")
        print("\nNext steps:")
        print("1. Update config/.env with your API keys")
        print("2. Run: python agentic_os/main.py")
        print("3. Open: http://localhost:8080")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()