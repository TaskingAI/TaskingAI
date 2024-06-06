#!/bin/bash

# Set the base directory
base_dir="bundles"

# Check if the base directory exists
if [ ! -d "$base_dir" ]; then
    echo "The directory $base_dir does not exist."
    exit 1
fi

echo "Starting to traverse directories under $base_dir..."

# Traverse through all directories under /bundles
for directory in "$base_dir"/*; do
    if [ -d "$directory" ]; then
        # Extract the directory name
        dir_name=$(basename "$directory")
        echo "Processing $dir_name..."

        # Check if the source file exists
        src_file_1="$directory/resources/i18n/en.yml"
        if [ ! -f "$src_file_1" ]; then
            echo "Source file $src_file_1 does not exist, skipping..."
            continue
        fi

        #
        src_file_2="$directory/resources/i18n/zh-CN.yml"
        if [ ! -f "$src_file_2" ]; then
            echo "Source file $src_file_2 does not exist, skipping..."
            continue
        fi

        # Execute the translation command
        echo "Running translation command for $dir_name..."
        tk_translate --file-type yaml --model gpt-4o --exclude name -s "$src_file_1" "$src_file_2" -t fr de -o "$directory/resources/i18n"
    else
        echo "Skipping $directory as it is not a directory..."
    fi
done

echo "Finished processing all directories."
