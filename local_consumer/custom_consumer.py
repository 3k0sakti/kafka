#!/usr/bin/env python3
"""
Kafka Consumer - Custom Filter Version
Consumer dengan filtering dan custom processing

Install dependencies:
    pip install kafka-python

Usage:
    python custom_consumer.py
"""

from kafka import KafkaConsumer
import json
from datetime import datetime
from collections import defaultdict

# Konfigurasi
KAFKA_SERVER = 'localhost:9092'
TOPIC = 'apache-logs'
GROUP_ID = 'custom-consumer-group'

class CustomConsumer:
    def __init__(self):
        self.stats = {
            'total': 0,
            'status_codes': defaultdict(int),
            'methods': defaultdict(int),
            'paths': defaultdict(int)
        }
        
    def process_message(self, data):
        """Process dan filter message"""
        self.stats['total'] += 1
        
        # Collect statistics
        status = data.get('status_code', 'unknown')
        method = data.get('method', 'unknown')
        path = data.get('path', 'unknown')
        
        self.stats['status_codes'][status] += 1
        self.stats['methods'][method] += 1
        self.stats['paths'][path] += 1
        
        # Filter: hanya tampilkan error (4xx, 5xx)
        if status.startswith('4') or status.startswith('5'):
            print(f"\n🚨 ERROR DETECTED!")
            print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
            print(f"   IP: {data.get('ip_address', 'N/A')}")
            print(f"   {method} {path} -> {status}")
            print(f"   Log: {data.get('raw_log', 'N/A')}")
        
        # Tampilkan setiap 10 message
        if self.stats['total'] % 10 == 0:
            self.print_stats()
    
    def print_stats(self):
        """Print statistics"""
        print(f"\n{'='*70}")
        print(f"📊 STATISTICS (Total: {self.stats['total']} messages)")
        print(f"{'='*70}")
        
        print("\n🔢 Status Codes:")
        for status, count in sorted(self.stats['status_codes'].items()):
            emoji = "✅" if status.startswith('2') else "⚠️" if status.startswith('4') else "❌"
            print(f"   {emoji} {status}: {count}")
        
        print("\n📍 Methods:")
        for method, count in self.stats['methods'].items():
            print(f"   • {method}: {count}")
        
        print("\n🗂️ Top Paths:")
        top_paths = sorted(self.stats['paths'].items(), key=lambda x: x[1], reverse=True)[:5]
        for path, count in top_paths:
            print(f"   • {path}: {count}")
        
        print(f"{'='*70}\n")
    
    def run(self):
        """Run consumer"""
        print("🚀 Custom Consumer Starting...")
        print(f"   Server: {KAFKA_SERVER}")
        print(f"   Topic: {TOPIC}")
        print(f"   Filter: Showing only errors (4xx, 5xx)")
        print(f"   Stats: Every 10 messages")
        print("-" * 70)
        
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=[KAFKA_SERVER],
            group_id=GROUP_ID,
            auto_offset_reset='latest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        print("✅ Connected! Listening for messages...")
        print("   (Press Ctrl+C to stop and see final stats)\n")
        
        try:
            for message in consumer:
                data = message.value
                self.process_message(data)
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Stopping...")
        finally:
            consumer.close()
            self.print_stats()
            print("\n👋 Consumer stopped")

def main():
    consumer = CustomConsumer()
    consumer.run()

if __name__ == '__main__':
    main()
