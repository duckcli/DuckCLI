

#!/usr/bin/env bash

set -e
set -x
pytest --cov=src/duckcli --cov=tests --cov-report=term-missing -o console_output_style=progress