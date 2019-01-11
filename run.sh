#!/bin/bash

cd $(dirname $0)

source venv/bin/activate
python3 src/check_rne.py
