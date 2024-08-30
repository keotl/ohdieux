#!/bin/sh
ruff check ohdieux/ main* tests/ --fix
yapf --in-place --recursive ohdieux/ main* tests/
