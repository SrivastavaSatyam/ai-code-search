#!/bin/bash

API_URL="http://localhost:8000"

echo "Testing API root endpoint..."
curl -X GET $API_URL/

echo -e "\n\nAdding code snippets..."
curl -v -X POST $API_URL/add-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
  }'

echo -e "\n\nTrying with additional parameters..."
curl -X POST $API_URL/add-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
    "language": "python"
  }'

echo -e "\n\nSearching for code..."
curl -X POST $API_URL/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "fibonacci sequence",
    "limit": 2
  }'

echo -e "\n\nSaving index..."
curl -X POST $API_URL/save-index 