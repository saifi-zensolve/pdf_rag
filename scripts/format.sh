# !/bin/bash

# Format all Python files using ruff
echo "\n\033[36m[FORMAT] Starting formatting...\033[0m"
ruff format .

# Check for any remaining issues
echo "\n\033[36m[FORMAT] Checking for remaining issues...\033[0m"
ruff check . --fix

echo "\n\033[36m[FORMAT] Formatting complete!\033[0m"
