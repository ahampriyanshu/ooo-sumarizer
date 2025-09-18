#!/bin/bash

# OOO Summariser Test Cleanup Script
# This script cleans up all files created during test runs

# Remove all generated reports
rm -f reports/*.json

# Remove all cached agent reports
rm -f tests/cached_agent_report*.json
rm -f tests/test_data/reports/agent_report_*.json
rm -f tests/test_data/reports/cached_agent_report*.json

# Remove all database files
rm -f data/databases/*.db

# Remove pytest cache
rm -rf .pytest_cache/
rm -rf tests/__pycache__/
rm -rf data/__pycache__/
rm -rf mcp_servers/__pycache__/
rm -rf __pycache__/

# Remove unit test results
rm -f unit.xml

# Remove any temporary files
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
