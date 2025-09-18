#!/bin/bash

bash setup/install.sh
bash setup/cleanup.sh
bash setup/seed.sh
python3 setup/pregenerate_reports.py
python3 -m pytest tests/ -v --junit-xml=unit.xml -n auto
