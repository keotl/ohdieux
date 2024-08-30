#!/bin/sh
yapf --diff --recursive ohdieux/ main* tests/
ruff check ohdieux/ main*
