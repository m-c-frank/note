# README for Git Pre-commit Hook Script

## Overview
This script is designed to be used as a pre-commit hook in Git. It automatically posts the `git diff` of currently staged changes to a specified server endpoint before each commit.

## Prerequisites
- **Git**: Must be installed and configured on your machine.
- **JQ**: A command-line JSON processor.
- **cURL**: Command-line tool for transferring data with URLs.

## Installation
1. **Install Dependencies**:
   - Install **Git**, **JQ**, and **cURL** as mentioned in the previous section.

2. **Configure Git Hook**:
   - Place this script in the `.git/hooks` directory of your Git repository.
   - Rename the script to `pre-commit` (without any file extension).
   - Give it executable permissions using `chmod +x pre-commit`.

## Configuration
- Modify the `POST_URL` variable in the script to point to your desired server endpoint.

## How It Works
- When you commit changes, this pre-commit hook is triggered.
- It retrieves the path of the current Git repository and the diff of staged changes.
- The script formats this information into JSON using JQ.
- It then sends this JSON data to the specified server using cURL.
- If the POST request fails (response code is not 200), the commit is aborted with an error message.

## Usage
Simply stage your changes (`git add`) and commit (`git commit`). The pre-commit hook will automatically execute this script.

## Note
- This script should be placed in each repository where you want this functionality.
- Ensure that the server endpoint is correctly configured to handle incoming POST requests.

## Troubleshooting
- Confirm that Git, JQ, and cURL are properly installed and accessible in your PATH.
- Make sure the script has executable permissions.
- Check the `POST_URL` for correctness.

