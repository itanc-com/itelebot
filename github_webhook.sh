#!/bin/bash

# Read the GitHub webhook payload from stdin
payload=$(cat)

# Check if the payload contains the ref for the main branch
if [[ "$payload" == *'"ref": "refs/heads/main"'* ]]; then
    echo "Push detected to main branch. Running deployment script."
    # Run the deploy script
    /path/to/your/repo/deploy.sh
else
    echo "Push detected, but not on main branch. No action taken."
fi

