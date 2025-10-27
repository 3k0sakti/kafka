#!/usr/bin/env python3
"""
Apache Log Consumer
Membaca data dari Kafka dan print line per line
"""

import os
import time
import json
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ApacheLogConsumer:
    def __init__(self, bootstrap_servers, topic, group_id):
        """
        Initialize Apache Log Consumer
        
        Args:
            bootstrap_servers: Kafka bootstrap servers
            topic: Kafka topic name
            group_id: Consumer group ID
        """
        self.topic = topic
        self.group_id = group_id
        self.running = False
        
        logger.info(f"Initializing Kafka Consumer...")
        logger.info(f"Bootstrap Servers: {bootstrap_servers}")
        logger.info(f"Topic: {topic}")
        logger.info(f"Group ID: {group_id}")
        
        # Initialize Kafka Consumer
        max_retries = 10
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                self.consumer = KafkaConsumer(
                    topic,
                    bootstrap_servers=bootstrap_servers,
                    group_id=group_id,
                    auto_offset_reset='earliest',  # Start from beginning if no offset
                    enable_auto_commit=True,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    key_deserializer=lambda k: k.decode('utf-8') if k else None
                    # No consumer_timeout_ms = consumer will wait indefinitely
                )
                logger.info("✅ Kafka Consumer initialized successfully!")
                break
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("Failed to initialize Kafka Consumer after all retries")
                    raise
    
    def print_log_line(self, message_data, message_number):
        """
        Print log line dengan format yang rapi
        
        Args:
            message_data: Data log dari Kafka
            message_number: Nomor urut message
        """
        # Print separator
        print("\n" + "=" * 100)
        print(f"📨 MESSAGE #{message_number}")
        print("=" * 100)
        
        # Print timestamp
        timestamp = message_data.get('timestamp', 'N/A')
        print(f"🕐 Received at: {timestamp}")
        
        # Print raw log line
        raw_log = message_data.get('raw_log', 'N/A')
        print(f"\n📄 RAW LOG:")
        print(f"   {raw_log}")
        
        # Print parsed data (jika ada)
        if 'parse_error' not in message_data:
            print(f"\n📊 PARSED DATA:")
            print(f"   • IP Address    : {message_data.get('ip_address', 'N/A')}")
            print(f"   • Method        : {message_data.get('method', 'N/A')}")
            print(f"   • Path          : {message_data.get('path', 'N/A')}")
            print(f"   • Protocol      : {message_data.get('protocol', 'N/A')}")
            print(f"   • Status Code   : {message_data.get('status_code', 'N/A')}")
            print(f"   • Response Size : {message_data.get('response_size', 'N/A')} bytes")
            print(f"   • Log Timestamp : {message_data.get('log_timestamp', 'N/A')}")
            
            # Highlight status code dengan emoji
            status = message_data.get('status_code', '000')
            if status.startswith('2'):
                status_emoji = "✅"
            elif status.startswith('3'):
                status_emoji = "↩️"
            elif status.startswith('4'):
                status_emoji = "⚠️"
            elif status.startswith('5'):
                status_emoji = "❌"
            else:
                status_emoji = "❓"
            
            print(f"\n   {status_emoji} HTTP Status: {status}")
        else:
            print(f"\n⚠️ Parse Error: {message_data.get('parse_error', 'Unknown error')}")
        
        print("=" * 100 + "\n")
    
    def consume_messages(self):
        """
        Consume messages dari Kafka dan print line per line
        """
        self.running = True
        messages_consumed = 0
        
        logger.info("🚀 Starting Apache Log Consumer...")
        logger.info(f"📥 Listening to topic: {self.topic}")
        logger.info(f"👥 Consumer Group: {self.group_id}")
        logger.info("=" * 100)
        logger.info("⏳ Waiting for messages...")
        logger.info("=" * 100 + "\n")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                messages_consumed += 1
                
                # Get message data
                log_data = message.value
                
                # Print line by line
                self.print_log_line(log_data, messages_consumed)
                
                # Log ke file juga (optional)
                logger.info(
                    f"Consumed message #{messages_consumed} - "
                    f"Partition: {message.partition}, "
                    f"Offset: {message.offset}, "
                    f"Key: {message.key}"
                )
                
        except KeyboardInterrupt:
            logger.info("\n⚠️ Consumer interrupted by user")
        except Exception as e:
            logger.error(f"❌ Error in consumer: {e}", exc_info=True)
        finally:
            self.stop()
            logger.info(f"\n📊 Total messages consumed: {messages_consumed}")
    
    def stop(self):
        """Stop the consumer"""
        self.running = False
        if hasattr(self, 'consumer'):
            logger.info("Closing consumer...")
            self.consumer.close()
            logger.info("✅ Consumer closed")


def main():
    """Main function"""
    # Get configuration from environment variables
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    topic = os.getenv('KAFKA_TOPIC', 'apache-logs')
    group_id = os.getenv('KAFKA_GROUP_ID', 'apache-log-consumer-group')
    
    logger.info("=" * 100)
    logger.info("🚀 APACHE LOG CONSUMER STARTING")
    logger.info("=" * 100)
    logger.info(f"Kafka Bootstrap Servers: {bootstrap_servers}")
    logger.info(f"Kafka Topic: {topic}")
    logger.info(f"Consumer Group ID: {group_id}")
    logger.info("=" * 100 + "\n")
    
    # Create and start consumer
    consumer = ApacheLogConsumer(bootstrap_servers, topic, group_id)
    consumer.consume_messages()


if __name__ == '__main__':
    main()
