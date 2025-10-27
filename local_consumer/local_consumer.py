#!/usr/bin/env python3
"""
Kafka Consumer - Standalone Version
Untuk dijalankan di komputer lokal (di luar Docker)

Install dependencies terlebih dahulu:
    pip install kafka-python

Usage:
    python local_consumer.py
"""

import json
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import sys
import signal

# Configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']  # Kafka server di localhost
KAFKA_TOPIC = 'apache-logs'
KAFKA_GROUP_ID = 'local-consumer-group'

class LocalApacheLogConsumer:
    def __init__(self):
        self.consumer = None
        self.running = False
        self.message_count = 0
        
    def initialize(self):
        """Initialize Kafka Consumer"""
        print("=" * 80)
        print("🚀 KAFKA CONSUMER - LOCAL VERSION")
        print("=" * 80)
        print(f"📡 Connecting to Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
        print(f"📋 Topic: {KAFKA_TOPIC}")
        print(f"👥 Consumer Group: {KAFKA_GROUP_ID}")
        print("=" * 80)
        
        try:
            self.consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                group_id=KAFKA_GROUP_ID,
                auto_offset_reset='latest',  # Hanya baca message baru
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None
                # No timeout - will wait indefinitely for messages
            )
            print("✅ Connected to Kafka successfully!")
            print("\n⏳ Waiting for messages...")
            print("💡 Tip: Generate traffic with: curl http://localhost:8080/")
            print("🛑 Press Ctrl+C to stop\n")
            print("=" * 80 + "\n")
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to Kafka: {e}")
            print("\n💡 Troubleshooting:")
            print("   1. Make sure Docker containers are running: docker-compose ps")
            print("   2. Check Kafka is accessible: docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list")
            print("   3. Check port 9092 is exposed: docker-compose ps kafka")
            return False
    
    def format_log_message(self, data, message_number):
        """Format and print log message"""
        # Print separator
        print("\n" + "=" * 80)
        print(f"📨 MESSAGE #{message_number}")
        print("=" * 80)
        
        # Timestamp
        timestamp = data.get('timestamp', 'N/A')
        print(f"🕐 Received at: {timestamp}")
        
        # Raw log
        raw_log = data.get('raw_log', 'N/A')
        print(f"\n📄 RAW LOG:")
        print(f"   {raw_log}")
        
        # Parsed data
        if 'parse_error' not in data:
            print(f"\n📊 PARSED DATA:")
            print(f"   • IP Address    : {data.get('ip_address', 'N/A')}")
            print(f"   • Method        : {data.get('method', 'N/A')}")
            print(f"   • Path          : {data.get('path', 'N/A')}")
            print(f"   • Protocol      : {data.get('protocol', 'N/A')}")
            print(f"   • Status Code   : {data.get('status_code', 'N/A')}")
            print(f"   • Response Size : {data.get('response_size', 'N/A')} bytes")
            print(f"   • Log Timestamp : {data.get('log_timestamp', 'N/A')}")
            
            # Status emoji
            status = data.get('status_code', '000')
            if status.startswith('2'):
                status_emoji = "✅"
                status_text = "Success"
            elif status.startswith('3'):
                status_emoji = "↩️"
                status_text = "Redirect"
            elif status.startswith('4'):
                status_emoji = "⚠️"
                status_text = "Client Error"
            elif status.startswith('5'):
                status_emoji = "❌"
                status_text = "Server Error"
            else:
                status_emoji = "❓"
                status_text = "Unknown"
            
            print(f"\n   {status_emoji} HTTP Status: {status} ({status_text})")
        else:
            print(f"\n⚠️ Parse Error: {data.get('parse_error', 'Unknown error')}")
        
        print("=" * 80 + "\n")
    
    def consume_messages(self):
        """Consume messages from Kafka"""
        self.running = True
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                self.message_count += 1
                
                # Get message data
                log_data = message.value
                
                # Print formatted message
                self.format_log_message(log_data, self.message_count)
                
                # Print metadata
                print(f"ℹ️  Metadata: Partition={message.partition}, Offset={message.offset}, Key={message.key}")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Stopping consumer...")
        except Exception as e:
            print(f"\n❌ Error consuming messages: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop consumer gracefully"""
        self.running = False
        if self.consumer:
            print("\n🔄 Closing consumer connection...")
            self.consumer.close()
            print("✅ Consumer closed")
        
        print("\n" + "=" * 80)
        print("📊 SUMMARY")
        print("=" * 80)
        print(f"Total messages consumed: {self.message_count}")
        print("=" * 80)
        print("\n👋 Thank you for using Kafka Consumer!")


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n⚠️ Received interrupt signal...")
    sys.exit(0)


def main():
    """Main function"""
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create consumer
    consumer = LocalApacheLogConsumer()
    
    # Initialize connection
    if not consumer.initialize():
        sys.exit(1)
    
    # Start consuming messages
    consumer.consume_messages()


if __name__ == '__main__':
    main()
