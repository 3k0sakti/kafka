#!/usr/bin/env python3
"""
Kafka Consumer - Simple Version
Versi minimal untuk consume data dari Kafka

Install dependencies:
    pip install kafka-python

Usage:
    python simple_consumer.py
"""

from kafka import KafkaConsumer
import json

# Konfigurasi
KAFKA_SERVER = 'localhost:9092'
TOPIC = 'apache-logs'

def main():
    print("🚀 Connecting to Kafka...")
    print(f"   Server: {KAFKA_SERVER}")
    print(f"   Topic: {TOPIC}")
    print("-" * 60)
    
    # Create consumer
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("✅ Connected! Waiting for messages...")
    print("   (Generate traffic: curl http://localhost:8080/)")
    print("   (Press Ctrl+C to stop)\n")
    
    count = 0
    try:
        for message in consumer:
            count += 1
            data = message.value
            
            print(f"\n{'='*60}")
            print(f"Message #{count}")
            print(f"{'='*60}")
            print(f"Raw: {data.get('raw_log', 'N/A')}")
            print(f"IP: {data.get('ip_address', 'N/A')}")
            print(f"Method: {data.get('method', 'N/A')} {data.get('path', 'N/A')}")
            print(f"Status: {data.get('status_code', 'N/A')}")
            
    except KeyboardInterrupt:
        print("\n\n👋 Stopped by user")
    finally:
        consumer.close()
        print(f"\n📊 Total messages: {count}")

if __name__ == '__main__':
    main()
