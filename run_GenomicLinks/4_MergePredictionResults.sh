#!/bin/bash

# Check and set the folder containing the prediction CSV files
FOLDER=$1
if [ -z "$FOLDER" ]; then
    echo "Usage: $0 <folder_path>"
    exit 1
fi

# Construct the path to the subfolder where prediction files are stored
PREDICTIONS_DIR="${FOLDER}/predictions"

# Find the first CSV file to extract the header
first_file=$(find $PREDICTIONS_DIR -type f -name 'predictions-*.csv' | head -1)
if [ ! -f "$first_file" ]; then
    echo "No CSV files found to process in $PREDICTIONS_DIR."
    exit 1
fi

# Prepare the merged CSV file with the header
echo "Preparing merged CSV..."
head -1 "$first_file" > "${FOLDER}/final_loop_prediction.csv"

# Append all other CSV contents (excluding the headers) to the merged file
for file in $(find $PREDICTIONS_DIR -type f -name 'predictions-*.csv' | sort -V); do
    tail -n +2 "$file" >> "${FOLDER}/final_loop_prediction.csv"
done

echo "Merged CSV file created at: ${FOLDER}/final_loop_prediction.csv"
