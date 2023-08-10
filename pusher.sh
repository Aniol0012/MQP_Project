#!/bin/bash

# Check if there's at least one argument for the commit message
if [ "$#" -lt 1 ]; then
    echo "Usage: ./pusher.sh <commit_message>"
    exit 1
fi

# Modify the line in config.py
sed -i 's/SCREEN_TO_OPEN_ROOT = 1  # 1 Para la segunda pantalla y 0 para la primera/SCREEN_TO_OPEN_ROOT = 0  # 1 Para la segunda pantalla y 0 para la primera/g' config.py

# Git operations
git add .
git commit -m "v$1"
git push

# Switch to the EN branch or create it if it doesn't exist
git checkout -b EN || git checkout EN

# Copy all changes from main branch excluding what's in .gitignore
git checkout main -- .

# Commit and push changes to the EN branch
git commit -m "v$1 - Copied from main"
git push origin EN

# Switch back to the main branch
git checkout main

# Restore the line in config.py
sed -i 's/SCREEN_TO_OPEN_ROOT = 0  # 1 Para la segunda pantalla y 0 para la primera/SCREEN_TO_OPEN_ROOT = 1  # 1 Para la segunda pantalla y 0 para la primera/g' config.py

echo "Changes pushed successfully!"
