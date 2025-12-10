#!/bin/bash

echo "Running tests..."

# Activate virtual environment
source venv/bin/activate

# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=html --cov-report=term

echo ""
echo "✓ Tests complete!"
echo "Coverage report: htmlcov/index.html