#!/bin/bash

pip install -r requirements.txt
bash setup/cleanup.sh
bash setup/seed.sh
