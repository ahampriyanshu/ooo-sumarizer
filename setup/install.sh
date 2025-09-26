#!/bin/bash

echo "Installing dependencies..."
pip install -q -r requirements.txt
bash setup/cleanup.sh
bash setup/seed.sh
