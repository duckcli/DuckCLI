#!/usr/bin/env bash

set-e
set-x

mypy  ./src/duckcli
black ./src/duckcli tests --check
isort ./src/duckcli tests --check-only