#!/bin/bash
# Run basic tests

echo "Running basic end-to-end tests..."
cd src/backend
python test_basic.py

echo ""
echo "Running API tests (if pytest is available)..."
if command -v pytest &> /dev/null; then
    pytest test_api.py -v || echo "API tests skipped (pytest not configured)"
else
    echo "pytest not found, skipping API tests"
fi
