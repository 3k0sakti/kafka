# 🚀 Kafka Stream - Apache Log Real-time Monitoring

[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Kafka](https://img.shields.io/badge/Apache-Kafka-red.svg)](https://kafka.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-3k0sakti%2Fkafka-black.svg)](https://github.com/3k0sakti/kafka)

Implementasi lengkap **real-time streaming Apache access logs** menggunakan Apache Kafka dengan Docker.

## 📋 Overview

Project ini mengimplementasikan real-time streaming Apache access logs menggunakan Apache Kafka. System terdiri dari:

1. **Apache Web Server** - Generate access logs
2. **Kafka Producer** (Docker 1) - Membaca Apache logs secara real-time dan mengirim ke Kafka
3. **Kafka Consumer** (Docker 2) - Membaca dari Kafka dan print line per line
4. **Local Python Consumers** - 3 versi consumer untuk komputer lokal (simple/full/custom)
5. **Traffic Generator** - Generate HTTP traffic untuk testing

## 🎯 Key Features

✅ Real-time log streaming dengan Kafka
✅ Separate Docker containers (Producer & Consumer)
✅ Line-by-line data processing
✅ Multiple consumer options (Docker + Local Python)
✅ Auto traffic generation
✅ Complete troubleshooting tools
✅ Production-ready with health checks

## 🏗️ Architecture

```
┌─────────────────┐
│  Apache Server  │
│   (Port 8080)   │
└────────┬────────┘
         │ generates
         ▼
    access_log
         │
         │ tails
         ▼
┌─────────────────┐      ┌─────────────┐      ┌─────────────────┐
│    Producer     │─────▶│    Kafka    │─────▶│    Consumer     │
│   (Docker 1)    │ send │   Broker    │ read │   (Docker 2)    │
└─────────────────┘      └─────────────┘      └─────────────────┘
                                                       │
                                                       ▼
                                               Print line by line
```

## 📦 Components

### 1. Docker Compose Services
- **zookeeper**: Koordinator untuk Kafka
- **kafka**: Message broker
- **apache**: Web server yang generate logs
- **producer**: Membaca Apache logs dan kirim ke Kafka
- **consumer**: Membaca dari Kafka dan print output
- **log-generator**: Generate traffic ke Apache

### 2. Files
- `docker-compose.yml`: Orchestration semua services
- `producer.py`: Kafka producer script
- `consumer.py`: Kafka consumer script
- `Dockerfile.producer`: Docker image untuk producer
- `Dockerfile.consumer`: Docker image untuk consumer
- `requirements.txt`: Python dependencies
- `scripts/generate_traffic.py`: Traffic generator

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Minimal 4GB RAM available

### 1. Start All Services

```bash
# Build dan start semua containers
docker-compose up --build

# Atau run di background
docker-compose up -d --build
```

### 2. View Logs

```bash
# View producer logs (membaca Apache logs)
docker logs -f kafka-producer

# View consumer logs (print line by line)
docker logs -f kafka-consumer

# View Apache logs
docker logs -f apache-server

# View traffic generator
docker logs -f log-generator
```

### 3. Test Manual

Generate traffic secara manual:

```bash
# Generate beberapa requests
curl http://localhost:8080/
curl http://localhost:8080/index.html
curl http://localhost:8080/api/users
curl http://localhost:8080/notfound  # Generate 404
```

### 4. Stop Services

```bash
# Stop semua services
docker-compose down

# Stop dan hapus volumes
docker-compose down -v
```

## 📊 Output Format

### Producer Output
```
✅ [1] Sent to Kafka: 172.18.0.7 - GET / - Status: 200
✅ [2] Sent to Kafka: 172.18.0.7 - GET /index.html - Status: 200
```

### Consumer Output (Line by Line)
```
====================================================================================================
📨 MESSAGE #1
====================================================================================================
🕐 Received at: 2025-10-27T10:30:45.123456

📄 RAW LOG:
   172.18.0.7 - - [27/Oct/2025:10:30:45 +0000] "GET / HTTP/1.1" 200 45

📊 PARSED DATA:
   • IP Address    : 172.18.0.7
   • Method        : GET
   • Path          : /
   • Protocol      : HTTP/1.1
   • Status Code   : 200
   • Response Size : 45 bytes
   • Log Timestamp : 27/Oct/2025:10:30:45 +0000

   ✅ HTTP Status: 200
====================================================================================================
```

## 🔧 Configuration

### Environment Variables

#### Producer (producer.py)
```bash
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
KAFKA_TOPIC=apache-logs
LOG_FILE_PATH=/logs/access_log
```

#### Consumer (consumer.py)
```bash
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
KAFKA_TOPIC=apache-logs
KAFKA_GROUP_ID=apache-log-consumer-group
```

### Customize Configuration

Edit `docker-compose.yml` untuk mengubah:
- Kafka ports
- Apache ports (default: 8080)
- Volume paths
- Environment variables

## 📝 Log Format

Apache menggunakan "common" log format:
```
%h %l %u %t \"%r\" %>s %b
```

Dimana:
- `%h`: IP address client
- `%l`: Identity (biasanya -)
- `%u`: User ID (biasanya -)
- `%t`: Timestamp
- `%r`: Request line (method, path, protocol)
- `%s`: Status code
- `%b`: Response size

## 🛠️ Troubleshooting

### 🚨 Error: "Fetch to node 1 failed: Cancelled"

Ini adalah error koneksi Kafka yang umum. **Solusi Cepat:**

```bash
# Quick fix - restart semua dengan konfigurasi yang benar
./fix.sh

# Atau manual:
docker-compose down
docker-compose up -d --build
```

Tunggu ~40 detik untuk Kafka siap, lalu cek:
```bash
docker logs -f kafka-consumer
```

### 🔍 Debug Script

Gunakan debug script untuk cek semua status:
```bash
./debug.sh
```

Script ini akan check:
- ✅ Docker status
- ✅ Container status
- ✅ Kafka broker health
- ✅ Topics dan consumer groups
- ✅ Apache log file
- ✅ Network connectivity

### 💡 Cara Melihat Data di Consumer

**1. Real-time Consumer Output (RECOMMENDED):**
```bash
docker logs -f kafka-consumer
```
Ini akan menampilkan setiap log line yang diterima consumer dengan format:
```
====================================================================================================
📨 MESSAGE #1
====================================================================================================
🕐 Received at: 2025-10-27T10:30:45.123456

📄 RAW LOG:
   172.18.0.7 - - [27/Oct/2025:10:30:45 +0000] "GET / HTTP/1.1" 200 45

📊 PARSED DATA:
   • IP Address    : 172.18.0.7
   • Method        : GET
   • Path          : /
   • Status Code   : 200
====================================================================================================
```

**2. View Historical Consumer Logs:**
```bash
# Last 50 lines
docker logs kafka-consumer --tail 50

# All logs
docker logs kafka-consumer
```

**3. View Data Directly dari Kafka:**
```bash
# Consume dari Kafka topic langsung
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic apache-logs \
  --from-beginning
```

**4. Generate Traffic untuk Testing:**
```bash
# Single request
curl http://localhost:8080/

# Multiple requests
for i in {1..5}; do curl http://localhost:8080/api/users; sleep 1; done
```

### Producer tidak bisa connect ke Kafka
```bash
# Check Kafka health
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092

# Restart producer
docker-compose restart producer

# View producer logs
docker logs -f kafka-producer
```

### Consumer tidak menerima messages
```bash
# Check topic exists
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Check consumer group
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list

# Describe consumer group (show lag)
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group apache-log-consumer-group

# Reset consumer offset (start from beginning)
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group apache-log-consumer-group --reset-offsets --to-earliest --execute --topic apache-logs
```

### Apache logs tidak ter-generate
```bash
# Check Apache is running
docker ps | grep apache

# Generate manual traffic
curl http://localhost:8080/

# Check log file exists
docker exec apache-server ls -la /usr/local/apache2/logs/

# View Apache log directly
docker exec apache-server tail -f /usr/local/apache2/logs/access_log
```

### Containers keep restarting
```bash
# Check container logs
docker-compose logs kafka
docker-compose logs producer
docker-compose logs consumer

# Increase wait time in producer/consumer scripts
# Edit docker-compose.yml and add:
#   restart: on-failure
#   restart_policy:
#     delay: 10s
```

## 📈 Scaling

### Multiple Consumers
Untuk parallel processing, jalankan multiple consumer instances:

```bash
# Scale consumer service
docker-compose up -d --scale consumer=3
```

Setiap consumer akan mendapat partition berbeda (jika ada multiple partitions).

### Multiple Kafka Brokers
Edit `docker-compose.yml` untuk add more Kafka brokers untuk high availability.

## 🔍 Monitoring

### Kafka Topics
```bash
# List topics
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Describe topic
docker exec kafka kafka-topics --bootstrap-server localhost:9092 \
  --describe --topic apache-logs
```

### Consumer Groups
```bash
# List consumer groups
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list

# Describe consumer group
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group apache-log-consumer-group
```

## 🎯 Use Cases

1. **Real-time Log Monitoring**: Monitor Apache access logs in real-time
2. **Log Analytics**: Analyze traffic patterns, error rates
3. **Security Monitoring**: Detect suspicious activities
4. **Performance Monitoring**: Track response times and status codes
5. **Alerting**: Trigger alerts based on log patterns



## 🧪 Testing


### Load Testing
```bash
# Generate high traffic
for i in {1..1000}; do curl http://localhost:8080/ & done
```

## 📄 License

This project is for educational purposes.



---

**Happy Streaming! 🚀**
