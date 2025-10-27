#!/usr/bin/env python3
"""
Apache Log Producer
Membaca Apache access log secara real-time dan mengirim ke Kafka
"""

import os
import time
import json
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ApacheLogProducer:
    def __init__(self, bootstrap_servers, topic, log_file_path):
        """
        Initialize Apache Log Producer
        
        Args:
            bootstrap_servers: Kafka bootstrap servers
            topic: Kafka topic name
            log_file_path: Path to Apache access log file
        """
        self.topic = topic
        self.log_file_path = log_file_path
        self.running = False
        
        logger.info(f"Initializing Kafka Producer...")
        logger.info(f"Bootstrap Servers: {bootstrap_servers}")
        logger.info(f"Topic: {topic}")
        logger.info(f"Log File: {log_file_path}")
        
        # Initialize Kafka Producer
        max_retries = 10
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: k.encode('utf-8') if k else None,
                    acks='all',
                    retries=3,
                    max_in_flight_requests_per_connection=1
                )
                logger.info("✅ Kafka Producer initialized successfully!")
                break
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("Failed to initialize Kafka Producer after all retries")
                    raise
    
    def parse_apache_log(self, log_line):
        """
        Parse Apache log line and extract information
        
        Args:
            log_line: Raw log line from Apache
            
        Returns:
            dict: Parsed log data
        """
        try:
            # Basic parsing - dapat disesuaikan dengan format log Apache Anda
            # Format: IP - - [timestamp] "method path protocol" status size
            
            parts = log_line.split()
            if len(parts) < 10:
                return None
            
            log_data = {
                'raw_log': log_line.strip(),
                'ip_address': parts[0],
                'timestamp': datetime.now().isoformat(),
                'log_timestamp': ' '.join(parts[3:5]).strip('[]'),
                'method': parts[5].strip('"'),
                'path': parts[6],
                'protocol': parts[7].strip('"'),
                'status_code': parts[8],
                'response_size': parts[9],
                'user_agent': ' '.join(parts[11:]).strip('"') if len(parts) > 11 else 'Unknown'
            }
            
            return log_data
            
        except Exception as e:
            logger.warning(f"Error parsing log line: {e}")
            # Return raw log if parsing fails
            return {
                'raw_log': log_line.strip(),
                'timestamp': datetime.now().isoformat(),
                'parse_error': str(e)
            }
    
    def wait_for_log_file(self):
        """Wait for log file to exist"""
        logger.info(f"Waiting for log file: {self.log_file_path}")
        
        while not os.path.exists(self.log_file_path):
            logger.info(f"Log file not found, waiting...")
            time.sleep(5)
        
        logger.info(f"✅ Log file found: {self.log_file_path}")
    
    def tail_log_file(self):
        """
        Tail Apache log file and send new lines to Kafka (like tail -f)
        """
        self.running = True
        messages_sent = 0
        
        logger.info(f"🚀 Starting to tail Apache log file...")
        logger.info(f"📂 Monitoring: {self.log_file_path}")
        logger.info(f"📤 Sending to topic: {self.topic}")
        logger.info("=" * 70)
        
        try:
            # Wait for log file to exist
            self.wait_for_log_file()
            
            # Open file and seek to end
            with open(self.log_file_path, 'r') as file:
                # Go to end of file
                file.seek(0, 2)
                
                logger.info("👀 Watching for new log entries...")
                
                while self.running:
                    line = file.readline()
                    
                    if line:
                        # Parse log line
                        log_data = self.parse_apache_log(line)
                        
                        if log_data:
                            try:
                                # Send to Kafka
                                future = self.producer.send(
                                    self.topic,
                                    key=log_data.get('ip_address', 'unknown'),
                                    value=log_data
                                )
                                
                                # Wait for send to complete
                                record_metadata = future.get(timeout=10)
                                
                                messages_sent += 1
                                
                                logger.info(
                                    f"✅ [{messages_sent}] Sent to Kafka: "
                                    f"{log_data.get('ip_address', 'N/A')} - "
                                    f"{log_data.get('method', 'N/A')} "
                                    f"{log_data.get('path', 'N/A')} - "
                                    f"Status: {log_data.get('status_code', 'N/A')}"
                                )
                                
                            except KafkaError as e:
                                logger.error(f"❌ Error sending to Kafka: {e}")
                    else:
                        # No new line, sleep briefly
                        time.sleep(0.1)
                        
        except KeyboardInterrupt:
            logger.info("⚠️ Producer interrupted by user")
        except Exception as e:
            logger.error(f"❌ Error in producer: {e}", exc_info=True)
        finally:
            self.stop()
            logger.info(f"📊 Total messages sent: {messages_sent}")
    
    def stop(self):
        """Stop the producer"""
        self.running = False
        if hasattr(self, 'producer'):
            logger.info("Flushing and closing producer...")
            self.producer.flush()
            self.producer.close()
            logger.info("✅ Producer closed")


def main():
    """Main function"""
    # Get configuration from environment variables
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    topic = os.getenv('KAFKA_TOPIC', 'apache-logs')
    log_file_path = os.getenv('LOG_FILE_PATH', '/logs/access_log')
    
    logger.info("=" * 70)
    logger.info("🚀 APACHE LOG PRODUCER STARTING")
    logger.info("=" * 70)
    logger.info(f"Kafka Bootstrap Servers: {bootstrap_servers}")
    logger.info(f"Kafka Topic: {topic}")
    logger.info(f"Log File Path: {log_file_path}")
    logger.info("=" * 70)
    
    # Create and start producer
    producer = ApacheLogProducer(bootstrap_servers, topic, log_file_path)
    producer.tail_log_file()


if __name__ == '__main__':
    main()
