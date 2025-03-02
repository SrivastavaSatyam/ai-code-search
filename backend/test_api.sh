#!/bin/bash

API_URL="http://localhost:8000"

echo "Testing API root endpoint..."
curl -X GET $API_URL/

echo -e "\n\nAdding code snippets..."
curl -X POST $API_URL/add-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
  }'

curl -X POST $API_URL/add-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function quickSort(arr) {\n  if (arr.length <= 1) return arr;\n  const pivot = arr[0];\n  const left = arr.slice(1).filter(x => x < pivot);\n  const right = arr.slice(1).filter(x => x >= pivot);\n  return [...quickSort(left), pivot, ...quickSort(right)];\n}"
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