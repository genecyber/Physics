#!/bin/bash

# Base URL of the Flask application
BASE_URL="http://localhost:5001"

# Function to list directory contents
list_dir() {
    local path="$1"
    echo -e "\nListing contents of directory: $path"
    curl -s "${BASE_URL}/list_dir?path=${path}"
}

# Function to read file contents
read_file() {
    local path="$1"
    echo -e "\nReading contents of file: $path"
    curl -s "${BASE_URL}/read_file?path=${path}"
}

# Directories to crawl
directories=(
    "/"
    "/app"
    "/app/static"
    "/app/templates"
    "/node_app"
)

# Files to read
files=(
    "/app/static/index.html"
    "/app/debug_app.txt"
    "/app/debug_node_app_after_npm_install.txt"
    "/app/debug_node_app_build.txt"
    "/app/debug_app_static.txt"
)

# Crawl directories
for dir in "${directories[@]}"; do
    list_dir "$dir"
done

# Read files
for file in "${files[@]}"; do
    read_file "$file"
done
