#!/bin/sh
set -e
# apk add git
pip install -r requirements.txt
python3 -m unittest discover tests
