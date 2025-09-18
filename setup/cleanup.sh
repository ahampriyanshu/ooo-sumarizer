#!/bin/bash

# OOO Summariser Test Cleanup Script
# This script cleans up all files created during test runs

echo "🧹 Starting cleanup of test-generated files..."

# Remove all generated reports
echo "📄 Removing generated reports..."
rm -f reports/*.json
echo "   ✅ Removed all OOO reports"

# Remove all cached agent reports
echo "💾 Removing cached agent reports..."
rm -f tests/cached_agent_report*.json
rm -f tests/test_data/reports/agent_report_*.json
rm -f tests/test_data/reports/cached_agent_report*.json
echo "   ✅ Removed all cached agent reports"

# Remove all database files
echo "🗄️  Removing database files..."
rm -f data/databases/*.db
echo "   ✅ Removed all database files"

# Remove pytest cache
echo "🧪 Removing pytest cache..."
rm -rf .pytest_cache/
rm -rf tests/__pycache__/
rm -rf data/__pycache__/
rm -rf mcp_servers/__pycache__/
rm -rf __pycache__/
echo "   ✅ Removed all Python cache files"

# Remove unit test results
echo "📊 Removing test result files..."
rm -f unit.xml
echo "   ✅ Removed unit test results"

# Remove any temporary files
echo "🗑️  Removing temporary files..."
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ Removed temporary Python files"

echo ""
echo "🎉 Cleanup completed successfully!"
echo "📁 Cleaned directories:"
echo "   - reports/ (all JSON files)"
echo "   - tests/ (cached reports and cache)"
echo "   - tests/test_data/reports/ (agent reports with fixed constant ID)"
echo "   - data/databases/ (all database files)"
echo "   - All __pycache__ directories"
echo "   - Test result files"
echo ""
echo "✨ Project is now clean and ready for the next test run!"
