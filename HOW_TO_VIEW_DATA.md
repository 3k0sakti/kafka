# 📊 Cara Melihat Data dari Producer ke Consumer

## 🎯 Quick Guide

### 1️⃣ **Cara Paling Mudah - Lihat Consumer Logs** ⭐

```bash
docker logs -f kafka-consumer
```

**Output yang akan muncul:**
```
====================================================================================================
📨 MESSAGE #1
====================================================================================================
🕐 Received at: 2025-10-27T10:30:45.123456

📄 RAW LOG:
   172.18.0.7 - - [27/Oct/2025:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234

📊 PARSED DATA:
   • IP Address    : 172.18.0.7
   • Method        : GET
   • Path          : /api/users
   • Protocol      : HTTP/1.1
   • Status Code   : 200
   • Response Size : 1234 bytes
   • Log Timestamp : 27/Oct/2025:10:30:45 +0000

   ✅ HTTP Status: 200
====================================================================================================
```

### 2️⃣ **Generate Traffic untuk Testing**

Buka terminal baru dan jalankan:

```bash
# Single request
curl http://localhost:8080/

# Multiple requests
curl http://localhost:8080/api/users
curl http://localhost:8080/products
curl http://localhost:8080/about

# Loop untuk generate banyak traffic
for i in {1..10}; do 
    curl http://localhost:8080/
    sleep 1
done
```

Setiap request akan muncul di consumer logs!

### 3️⃣ **Lihat Data Langsung dari Kafka**

Jika consumer bermasalah, Anda bisa baca langsung dari Kafka:

```bash
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic apache-logs \
  --from-beginning
```

**Output format JSON:**
```json
{
  "raw_log": "172.18.0.7 - - [27/Oct/2025:10:30:45 +0000] \"GET / HTTP/1.1\" 200 45",
  "ip_address": "172.18.0.7",
  "timestamp": "2025-10-27T10:30:45.123456",
  "method": "GET",
  "path": "/",
  "status_code": "200"
}
```

### 4️⃣ **Monitoring Real-time**

Buka **3 terminal** sekaligus:

**Terminal 1 - Consumer Output:**
```bash
docker logs -f kafka-consumer
```

**Terminal 2 - Producer Output:**
```bash
docker logs -f kafka-producer
```

**Terminal 3 - Generate Traffic:**
```bash
watch -n 2 curl -s http://localhost:8080/
```

## 🔍 Verification Steps

### Cek Status Semua Container
```bash
docker-compose ps
```

Expected output:
```
NAME              STATUS           PORTS
apache-server     Up              0.0.0.0:8080->80/tcp
kafka             Up (healthy)    0.0.0.0:9092->9092/tcp
kafka-consumer    Up
kafka-producer    Up
log-generator     Up
zookeeper         Up              0.0.0.0:2181->2181/tcp
```

### Debug Script (All-in-One Check)
```bash
./debug.sh
```

### Manual Debug Steps

**1. Check Kafka is healthy:**
```bash
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
```

**2. Check topic exists:**
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list
```
Should show: `apache-logs`

**3. Check consumer group:**
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group apache-log-consumer-group
```

**4. Check Apache log file:**
```bash
docker exec apache-server tail -f /usr/local/apache2/logs/access_log
```

## 🚨 Troubleshooting

### ❌ Error: "Fetch to node 1 failed"

**Quick Fix:**
```bash
./fix.sh
```

**Manual Fix:**
```bash
# Stop everything
docker-compose down

# Start fresh
docker-compose up -d --build

# Wait 40 seconds
sleep 40

# Check status
docker-compose ps
```

### ❌ Consumer tidak menerima data

**Reset consumer offset:**
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group apache-log-consumer-group \
  --reset-offsets --to-earliest \
  --execute --topic apache-logs

# Restart consumer
docker-compose restart consumer
```

### ❌ Tidak ada traffic

**Check traffic generator:**
```bash
docker logs log-generator
```

**Generate manual:**
```bash
curl http://localhost:8080/
```

## 📈 Advanced Monitoring

### View Producer Stats
```bash
# Last 20 lines
docker logs kafka-producer --tail 20

# Follow in real-time
docker logs -f kafka-producer
```

### View Consumer Stats
```bash
# See message count
docker logs kafka-consumer | grep "MESSAGE #" | tail -5

# See only errors
docker logs kafka-consumer | grep ERROR

# See only successful messages
docker logs kafka-consumer | grep "✅"
```

### Kafka Topic Info
```bash
# Topic details
docker exec kafka kafka-topics --bootstrap-server localhost:9092 \
  --describe --topic apache-logs

# Consumer lag (berapa message belum diproses)
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group apache-log-consumer-group
```

## 🎬 Complete Flow Example

### Step by Step:

1. **Start all services:**
   ```bash
   docker-compose up -d --build
   ```

2. **Wait for Kafka to be ready:**
   ```bash
   sleep 40
   ```

3. **Open consumer logs:**
   ```bash
   docker logs -f kafka-consumer
   ```

4. **Generate traffic (new terminal):**
   ```bash
   curl http://localhost:8080/
   curl http://localhost:8080/api/users
   curl http://localhost:8080/products
   ```

5. **Watch data flow in consumer terminal!** 🎉

### Expected Flow:

```
Apache Server → access_log file → Producer reads → Kafka topic → Consumer reads → Print line by line
```

## 💡 Tips & Tricks

### 1. Filter Consumer Output
```bash
# Only show successful (200) requests
docker logs kafka-consumer | grep "Status: 200"

# Only show errors (4xx, 5xx)
docker logs kafka-consumer | grep -E "Status: [45]"

# Count messages
docker logs kafka-consumer | grep "MESSAGE #" | wc -l
```

### 2. Real-time Traffic Monitoring
```bash
# Watch consumer in real-time with color
docker logs -f kafka-consumer | grep --color=always -E "MESSAGE|Status|Method"
```

### 3. Performance Testing
```bash
# Generate 100 requests quickly
for i in {1..100}; do curl -s http://localhost:8080/ > /dev/null & done

# Check how many messages consumer processed
docker logs kafka-consumer | grep "MESSAGE #" | tail -1
```

### 4. JSON Output Only (if you prefer)
```bash
# View raw Kafka messages (JSON format)
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic apache-logs \
  --from-beginning \
  | jq .
```

## 🎯 Summary

**Untuk melihat data yang dikirim producer di consumer:**

1. ✅ **Paling Mudah**: `docker logs -f kafka-consumer`
2. ✅ **Generate Traffic**: `curl http://localhost:8080/`
3. ✅ **Debug**: `./debug.sh`
4. ✅ **Fix Issues**: `./fix.sh`

**That's it! Happy Streaming! 🚀**
