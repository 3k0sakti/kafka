.PHONY: help build up down logs restart clean test traffic

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d
	@echo "✅ All services started!"
	@echo "📊 View logs with: make logs"

up-build: ## Build and start all services
	docker-compose up -d --build
	@echo "✅ All services built and started!"

down: ## Stop all services
	docker-compose down
	@echo "✅ All services stopped"

down-clean: ## Stop all services and remove volumes
	docker-compose down -v
	@echo "✅ All services stopped and volumes removed"

logs: ## View logs from all services
	docker-compose logs -f

logs-producer: ## View producer logs
	docker-compose logs -f producer

logs-consumer: ## View consumer logs
	docker-compose logs -f consumer

logs-kafka: ## View Kafka logs
	docker-compose logs -f kafka

logs-apache: ## View Apache logs
	docker-compose logs -f apache

restart: ## Restart all services
	docker-compose restart
	@echo "✅ All services restarted"

restart-producer: ## Restart producer only
	docker-compose restart producer

restart-consumer: ## Restart consumer only
	docker-compose restart consumer

clean: ## Clean up everything (containers, volumes, images)
	docker-compose down -v --rmi all
	@echo "✅ Everything cleaned up"

ps: ## Show running containers
	docker-compose ps

traffic: ## Generate test traffic
	@echo "Generating traffic..."
	@for i in {1..10}; do \
		curl -s http://localhost:8080/ > /dev/null && echo "✅ Request $$i sent"; \
		sleep 1; \
	done
	@echo "✅ Traffic generation complete"

kafka-topics: ## List Kafka topics
	docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

kafka-consumer-groups: ## List consumer groups
	docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list

kafka-consume: ## Consume messages from Kafka topic
	docker exec kafka kafka-console-consumer \
		--bootstrap-server localhost:9092 \
		--topic apache-logs \
		--from-beginning

reset-consumer: ## Reset consumer offset to beginning
	docker exec kafka kafka-consumer-groups \
		--bootstrap-server localhost:9092 \
		--group apache-log-consumer-group \
		--reset-offsets --to-earliest --execute --topic apache-logs

shell-producer: ## Open shell in producer container
	docker exec -it kafka-producer /bin/bash

shell-consumer: ## Open shell in consumer container
	docker exec -it kafka-consumer /bin/bash

shell-kafka: ## Open shell in Kafka container
	docker exec -it kafka /bin/bash

health: ## Check health of all services
	@echo "Checking service health..."
	@docker-compose ps
	@echo ""
	@echo "Kafka health:"
	@docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1 && echo "✅ Kafka is healthy" || echo "❌ Kafka is not healthy"

install-tools: ## Install useful tools for debugging
	@echo "Installing kafkacat..."
	@which kafkacat > /dev/null || (echo "Please install kafkacat manually" && exit 1)
