#!/usr/bin/env python3
"""
Traffic Generator for Apache Server
Generates HTTP requests to create log entries
"""

import time
import random
import requests
from datetime import datetime

# Apache server URL
APACHE_URL = "http://apache:80"

# Sample paths to request
PATHS = [
    "/",
    "/index.html",
    "/about.html",
    "/contact.html",
    "/products.html",
    "/services.html",
    "/api/users",
    "/api/products",
    "/api/orders",
    "/images/logo.png",
    "/css/style.css",
    "/js/app.js",
    "/admin",
    "/login",
    "/logout",
    "/search?q=test",
    "/404-not-found",  # Will generate 404
]

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15",
]

def generate_request():
    """Generate a random HTTP request to Apache"""
    path = random.choice(PATHS)
    user_agent = random.choice(USER_AGENTS)
    
    headers = {
        'User-Agent': user_agent
    }
    
    try:
        url = f"{APACHE_URL}{path}"
        response = requests.get(url, headers=headers, timeout=5)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✅ GET {path} - Status: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ❌ Error requesting {path}: {e}")

def main():
    """Main function"""
    print("🚀 Starting Traffic Generator...")
    print(f"Target: {APACHE_URL}")
    print("=" * 70)
    
    # Wait for Apache to be ready
    print("⏳ Waiting for Apache server to be ready...")
    time.sleep(10)
    
    request_count = 0
    
    try:
        while True:
            generate_request()
            request_count += 1
            
            # Random delay between 1-5 seconds
            delay = random.uniform(1, 5)
            time.sleep(delay)
            
            # Print summary every 10 requests
            if request_count % 10 == 0:
                print(f"\n📊 Total requests generated: {request_count}\n")
                
    except KeyboardInterrupt:
        print(f"\n⚠️ Traffic generator stopped")
        print(f"📊 Total requests generated: {request_count}")

if __name__ == '__main__':
    main()
