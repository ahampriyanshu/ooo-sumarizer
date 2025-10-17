#!/bin/bash

bash scripts/install.sh
echo "🧪 Running tests..."
python3 -m pytest tests/ -v --junit-xml=unit.xml -n 5
