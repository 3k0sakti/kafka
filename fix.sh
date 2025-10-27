#!/bin/bash

# Quick fix script untuk mengatasi error Kafka connection

echo "=========================================="
echo "🔧 Fixing Kafka Connection Issues"
echo "=========================================="
echo ""

echo "Step 1: Stopping all services..."
docker-compose down
echo "✅ Services stopped"
echo ""

echo "Step 2: Removing old volumes (optional)..."
read -p "Remove old volumes? This will clear all data (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose down -v
    echo "✅ Volumes removed"
fi
echo ""

echo "Step 3: Rebuilding and starting services..."
docker-compose up -d --build
echo "✅ Services started"
echo ""

echo "Step 4: Waiting for Kafka to be ready (40 seconds)..."
sleep 40
echo ""

echo "Step 5: Checking Kafka health..."
if docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1; then
    echo "✅ Kafka is healthy!"
else
    echo "⚠️ Kafka might not be ready yet. Wait a bit more and run:"
    echo "   docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092"
fi
echo ""

echo "Step 6: Creating topic (if not exists)..."
docker exec kafka kafka-topics --bootstrap-server localhost:9092 \
    --create --topic apache-logs --partitions 1 --replication-factor 1 \
    --if-not-exists 2>/dev/null
echo "✅ Topic checked/created"
echo ""

echo "=========================================="
echo "✅ Fix Complete!"
echo "=========================================="
echo ""
echo "Now you can:"
echo ""
echo "1. Watch consumer output:"
echo "   docker logs -f kafka-consumer"
echo ""
echo "2. Generate traffic:"
echo "   curl http://localhost:8080/"
echo ""
echo "3. Debug if needed:"
echo "   ./debug.sh"
echo ""
echo "4. Check container status:"
echo "   docker-compose ps"
echo ""
