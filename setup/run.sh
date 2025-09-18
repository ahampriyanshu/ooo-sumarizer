#!/bin/bash

bash setup/install.sh
bash setup/cleanup.sh
bash setup/seed.sh
python3 run_agent.py
