#!/bin/sh
# Add missing __init__.py files in test dir.
find tests -type d -not -name "__pycache__" -exec touch "{}/__init__.py" \;

python -m unittest discover
