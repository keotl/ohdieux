#!/bin/sh
# Assuming image python:3.10-alpine
apk add git
pip install -r requirements.txt
python3 -m unittest discover tests
