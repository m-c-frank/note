#!/bin/bash

# Configuration
POST_URL="http://localhost:3010/api/note"

# Function to post diff to URL
post_diff() {
    # Get the current git repository path
    repo_path=$(git rev-parse --show-toplevel)

    # Get git diff
    diff=$(git diff --cached)

    # Prepare JSON data with repo path and diff
    json_data=$(jq -n --arg rp "$repo_path" --arg df "$diff" '{origin: $rp, content: $df}')

    # Use curl to post the data
    response=$(curl -w "%{http_code}" -o /dev/null -X POST -H "Content-Type: application/json" -d "$json_data" "$POST_URL")

    if [ "$response" -ne 200 ]; then
        echo "Failed to post diff. Server response: $response"
        exit 1
    fi
}

# Main execution
post_diff

