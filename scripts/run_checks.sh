#!/bin/sh
yapf --diff --recursive ohdieux/ main* tests/
if [ $? -ne "0" ]; then
    echo "There were formatting errors."
    exit 1
fi
ruff check ohdieux/ main*
if [ $? -ne "0" ]; then
    echo "There were lint errors."
    exit 1
fi
mypy ohdieux/ main*
if [ $? -ne "0" ]; then
    echo "There were type errors."
    exit 1
fi

# Add missing __init__.py files in test dir.
find tests -type d -not -name "__pycache__" -exec touch "{}/__init__.py" \;

python -m unittest discover
if [ $? -ne "0" ]; then
    echo "There were test failures."
    exit 1
fi

echo "All checks passed successfully."
