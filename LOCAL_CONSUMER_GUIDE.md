# Local Consumer untuk Kafka

Program Python standalone untuk consume data dari Kafka di komputer lokal Anda (di luar Docker).

## 📋 Prerequisites

### 1. Install Dependencies

```bash
# Install kafka-python library
pip install kafka-python

# Atau jika menggunakan pip3
pip3 install kafka-python
```

### 2. Pastikan Kafka Running

```bash
# Check containers running
docker-compose ps

# Should show kafka running on port 9092
```

## 🚀 Available Consumers

### 1. **Local Consumer** - Full Featured (RECOMMENDED)

File: `local_consumer.py`

**Features:**
- ✅ Format output yang rapi dan lengkap
- ✅ Auto-reconnect handling
- ✅ Graceful shutdown (Ctrl+C)
- ✅ Message statistics
- ✅ Color-coded status

**Usage:**
```bash
python3 local_consumer.py
```

**Output:**
```
====================================================================================================
📨 MESSAGE #1
====================================================================================================
🕐 Received at: 2025-10-27T03:18:53.118981

📄 RAW LOG:
   192.168.97.1 - - [27/Oct/2025:03:18:53 +0000] "GET / HTTP/1.1" 200 45

📊 PARSED DATA:
   • IP Address    : 192.168.97.1
   • Method        : GET
   • Path          : /
   • Protocol      : HTTP/1.1
   • Status Code   : 200
   • Response Size : 45 bytes

   ✅ HTTP Status: 200 (Success)
====================================================================================================
```

### 2. **Simple Consumer** - Minimal Version

File: `simple_consumer.py`

**Features:**
- ✅ Simple dan mudah dipahami
- ✅ Minimal code
- ✅ Cocok untuk pemula

**Usage:**
```bash
python3 simple_consumer.py
```

**Output:**
```
============================================================
Message #1
============================================================
Raw: 192.168.97.1 - - [27/Oct/2025:03:18:53 +0000] "GET / HTTP/1.1" 200 45
IP: 192.168.97.1
Method: GET /
Status: 200
```

### 3. **Custom Consumer** - With Filtering & Statistics

File: `custom_consumer.py`

**Features:**
- ✅ Filter messages (hanya tampilkan errors)
- ✅ Collect statistics
- ✅ Top paths analysis
- ✅ Method distribution

**Usage:**
```bash
python3 custom_consumer.py
```

**Output:**
```
🚨 ERROR DETECTED!
   Time: 15:30:45
   IP: 192.168.97.1
   GET /notfound -> 404
   Log: 192.168.97.1 - - [27/Oct/2025:03:18:53 +0000] "GET /notfound HTTP/1.1" 404 196

======================================================================
📊 STATISTICS (Total: 10 messages)
======================================================================

🔢 Status Codes:
   ✅ 200: 8
   ⚠️ 404: 2

📍 Methods:
   • GET: 10

🗂️ Top Paths:
   • /: 5
   • /api/users: 3
   • /notfound: 2
======================================================================
```

## 🎯 Quick Start

### Step 1: Make sure Kafka is running
```bash
docker-compose ps
# kafka should be Up (healthy)
```

### Step 2: Install dependency
```bash
pip3 install kafka-python
```

### Step 3: Run consumer
```bash
# Choose one:
python3 local_consumer.py      # Full featured
python3 simple_consumer.py     # Simple version
python3 custom_consumer.py     # With filtering
```

### Step 4: Generate traffic (in another terminal)
```bash
curl http://localhost:8080/
curl http://localhost:8080/api/users
curl http://localhost:8080/notfound  # 404 error
```

### Step 5: Watch data appear in consumer! 🎉

## 🔧 Configuration

Edit nilai di dalam file Python:

```python
# Kafka server (default: localhost:9092)
KAFKA_SERVER = 'localhost:9092'

# Topic name (default: apache-logs)
TOPIC = 'apache-logs'

# Consumer group ID (default: local-consumer-group)
GROUP_ID = 'local-consumer-group'
```

## 🛠️ Troubleshooting

### Error: "No module named 'kafka'"

```bash
# Install kafka-python
pip3 install kafka-python
```

### Error: "NoBrokersAvailable"

```bash
# Check Kafka is running
docker-compose ps

# Check port 9092 is exposed
docker-compose ps kafka

# Test connection
telnet localhost 9092
```

### Error: "Connection refused"

```bash
# Restart Kafka
docker-compose restart kafka

# Wait for Kafka to be ready
sleep 10

# Try again
python3 local_consumer.py
```

### No messages appearing

```bash
# Check if topic exists
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Generate traffic
curl http://localhost:8080/

# Check Docker consumer is sending messages
docker logs kafka-producer --tail 10
```

## 💡 Tips & Tricks

### 1. Run in background
```bash
nohup python3 local_consumer.py > consumer.log 2>&1 &

# View logs
tail -f consumer.log
```

### 2. Multiple consumers
```bash
# Terminal 1
python3 local_consumer.py

# Terminal 2 (different group ID to get same messages)
# Edit custom_consumer.py, change GROUP_ID
python3 custom_consumer.py
```

### 3. Save to file
```bash
python3 local_consumer.py > logs_output.txt
```

### 4. Filter with grep
```bash
python3 local_consumer.py | grep "ERROR"
python3 local_consumer.py | grep "404"
```

### 5. JSON output only
```bash
# Modify consumer to print only JSON
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic apache-logs \
  --from-beginning
```

## 📊 Comparison

| Feature | local_consumer.py | simple_consumer.py | custom_consumer.py |
|---------|------------------|-------------------|-------------------|
| Format rapi | ✅ | ❌ | ⚠️ |
| Statistics | ✅ | ❌ | ✅ |
| Filtering | ❌ | ❌ | ✅ |
| Error handling | ✅ | ⚠️ | ✅ |
| Beginner friendly | ⚠️ | ✅ | ❌ |
| Production ready | ✅ | ❌ | ⚠️ |

## 🎓 Learning Path

1. **Start with:** `simple_consumer.py` - Understand basics
2. **Then try:** `local_consumer.py` - See full implementation
3. **Finally:** `custom_consumer.py` - Learn filtering & stats

## 📝 Example Use Cases

### Monitor errors only
Use `custom_consumer.py` - automatically filters 4xx and 5xx errors

### Log all traffic
Use `local_consumer.py` with output redirection:
```bash
python3 local_consumer.py > traffic_log.txt
```

### Real-time dashboard
Use `custom_consumer.py` to see statistics every 10 messages

### Integration with other systems
Modify consumer to:
- Send to database
- Trigger alerts (email, Slack)
- Forward to other services
- Generate reports

## 🚀 Next Steps

1. **Modify** consumer untuk save ke database
2. **Add** email alerts untuk errors
3. **Create** dashboard dengan statistics
4. **Implement** machine learning untuk anomaly detection
5. **Scale** dengan multiple consumer instances

## 📚 Additional Resources

- Kafka Python Docs: https://kafka-python.readthedocs.io/
- Kafka Consumer Guide: https://kafka.apache.org/documentation/#consumerapi
- Python Kafka Examples: https://github.com/dpkp/kafka-python

---

**Happy Consuming! 🎉**
