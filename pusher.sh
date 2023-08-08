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
git commit -m "$1"
git push

echo "Changes pushed successfully!"
