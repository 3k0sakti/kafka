#!/bin/bash

# Quick Start Script for Apache Kafka Log Streaming
# This script will start all services and show the consumer output

echo "=========================================="
echo "🚀 Apache Kafka Log Streaming"
echo "=========================================="
echo ""

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Build and start all services
echo "📦 Building and starting all services..."
docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to be ready (30 seconds)..."
sleep 30

echo ""
echo "=========================================="
echo "📊 Service Status"
echo "=========================================="
docker-compose ps

echo ""
echo "=========================================="
echo "📋 Available Commands"
echo "=========================================="
echo ""
echo "View consumer output (line by line):"
echo "  docker logs -f kafka-consumer"
echo ""
echo "View producer output:"
echo "  docker logs -f kafka-producer"
echo ""
echo "Generate manual traffic:"
echo "  curl http://localhost:8080/"
echo ""
echo "Stop all services:"
echo "  docker-compose down"
echo ""
echo "Or use Makefile:"
echo "  make logs-consumer    # View consumer logs"
echo "  make logs-producer    # View producer logs"
echo "  make traffic          # Generate test traffic"
echo "  make down             # Stop all services"
echo ""
echo "=========================================="
echo ""
echo "🎉 All services are starting up!"
echo "Watch the consumer output with:"
echo ""
echo "  docker logs -f kafka-consumer"
echo ""
echo "=========================================="
