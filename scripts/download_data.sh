#!/bin/bash
set -e

# Define the directory and file paths
DATA_DIR="data"
FILE_URL="https://huggingface.co/datasets/adesouza1/soap_notes/resolve/main/my_dataset/test.json"
OUTPUT_FILE="$DATA_DIR/test.json"

# Create the data directory if it doesn't exist
mkdir -p "$DATA_DIR"

# Download the file
echo "Downloading dataset to $OUTPUT_FILE..."
curl -L -o "$OUTPUT_FILE" "$FILE_URL"

echo "Dataset downloaded successfully."
