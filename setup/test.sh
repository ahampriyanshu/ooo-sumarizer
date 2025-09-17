#!/bin/bash

python3 data/seed_data_test1.py
python3 -m pytest tests/ -v --junit-xml=unit.xml
