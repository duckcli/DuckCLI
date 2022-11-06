
#!/bin/sh -e
set-x
autoflake --remove-all-unused-imports --recursive --in-place ./src/duckcli tests --exclude=__init__.py
black ./src/duckcli tests
isort ./src/duckcli tests