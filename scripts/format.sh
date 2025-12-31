# !/bin/bash

# Format all Python files using ruff
ruff format .

# Check for any remaining issues
ruff check . --fix
