#!/bin/bash

# Debug script untuk troubleshooting Kafka setup

echo "=========================================="
echo "🔍 Kafka Troubleshooting & Debugging"
echo "=========================================="
echo ""

# Check Docker is running
echo "1️⃣ Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi
echo "✅ Docker is running"
echo ""

# Check containers status
echo "2️⃣ Container Status:"
echo "=========================================="
docker-compose ps
echo ""

# Check Kafka broker health
echo "3️⃣ Checking Kafka broker health..."
echo "=========================================="
if docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1; then
    echo "✅ Kafka broker is healthy"
else
    echo "❌ Kafka broker is NOT healthy"
    echo ""
    echo "Try restarting Kafka:"
    echo "  docker-compose restart kafka"
    exit 1
fi
echo ""

# Check Kafka topics
echo "4️⃣ Kafka Topics:"
echo "=========================================="
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list 2>/dev/null || echo "❌ Cannot list topics"
echo ""

# Check consumer groups
echo "5️⃣ Consumer Groups:"
echo "=========================================="
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list 2>/dev/null || echo "❌ Cannot list consumer groups"
echo ""

# Check if apache-logs topic exists and has data
echo "6️⃣ Apache Logs Topic Details:"
echo "=========================================="
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic apache-logs 2>/dev/null || echo "⚠️ Topic 'apache-logs' does not exist yet"
echo ""

# Check Apache log file
echo "7️⃣ Apache Log File Status:"
echo "=========================================="
if docker exec apache-server test -f /usr/local/apache2/logs/access_log; then
    echo "✅ Apache log file exists"
    LOG_SIZE=$(docker exec apache-server wc -l /usr/local/apache2/logs/access_log 2>/dev/null | awk '{print $1}')
    echo "   Lines in log: $LOG_SIZE"
else
    echo "❌ Apache log file does not exist"
fi
echo ""

# Check producer logs (last 10 lines)
echo "8️⃣ Producer Last Logs:"
echo "=========================================="
docker logs kafka-producer --tail 10 2>&1
echo ""

# Check consumer logs (last 10 lines)
echo "9️⃣ Consumer Last Logs:"
echo "=========================================="
docker logs kafka-consumer --tail 10 2>&1
echo ""

# Network connectivity test
echo "🔟 Network Connectivity Test:"
echo "=========================================="
echo "Testing producer -> kafka connection:"
docker exec kafka-producer ping -c 2 kafka 2>&1 | grep -E "transmitted|received" || echo "❌ Cannot ping kafka from producer"
echo ""
echo "Testing consumer -> kafka connection:"
docker exec kafka-consumer ping -c 2 kafka 2>&1 | grep -E "transmitted|received" || echo "❌ Cannot ping kafka from consumer"
echo ""

# Summary
echo "=========================================="
echo "📋 Quick Commands"
echo "=========================================="
echo ""
echo "View consumer output in real-time:"
echo "  docker logs -f kafka-consumer"
echo ""
echo "Generate test traffic:"
echo "  curl http://localhost:8080/"
echo ""
echo "Restart all services:"
echo "  docker-compose restart"
echo ""
echo "Reset consumer offset to read from beginning:"
echo "  docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 \\"
echo "    --group apache-log-consumer-group --reset-offsets --to-earliest \\"
echo "    --execute --topic apache-logs"
echo ""
echo "View messages in Kafka directly:"
echo "  docker exec kafka kafka-console-consumer \\"
echo "    --bootstrap-server localhost:9092 --topic apache-logs --from-beginning"
echo ""
echo "=========================================="
