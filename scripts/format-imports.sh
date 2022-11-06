#!/bin/sh -e
set-x

#Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --thirdparty ./src/duckcli --apply  ./src/duckcli tests
sh ./scripts/format.sh