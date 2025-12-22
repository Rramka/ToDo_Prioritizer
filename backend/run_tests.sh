#!/bin/bash

# Test runner script for ToDo Prioritizer backend

echo "=========================================="
echo "  Running Backend Tests"
echo "=========================================="
echo ""

# Activate virtual environment if it exists
if [ -d "../venv" ]; then
    echo "Activating virtual environment..."
    source ../venv/bin/activate
fi

# Install test dependencies if needed
echo "Installing test dependencies..."
pip install -q -r requirements.txt

# Run tests
echo ""
echo "Running pytest..."
echo ""

pytest tests/ -v --tb=short

echo ""
echo "=========================================="
echo "  Test Summary"
echo "=========================================="

