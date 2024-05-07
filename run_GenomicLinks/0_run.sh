#!/bin/bash

# Set the base directory and define paths to data files and folders.
BASE_DIR="/path/to/your/scripts_directory"
BEDPE_FILE="/path/to/your/bedpe/file"
FASTA_FILE="/path/to/fasta/file"

PREDICTIONS_FOLDER="$BASE_DIR/predictions_output" # Generated automatically
MODEL_WEIGHTS="$BASE_DIR/weights-improvement-dp2500-58.hdf5"

# Run the R script,Python scripts and shell script.
Rscript "$BASE_DIR/1_PreprocessBEDPE.R" $BEDPE_FILE $PREDICTIONS_FOLDER
python3 "$BASE_DIR/2_ExtractRegion.py" $PREDICTIONS_FOLDER $FASTA_FILE
python3 "$BASE_DIR/3_Prediction.py" $PREDICTIONS_FOLDER $MODEL_WEIGHTS
sh "$BASE_DIR/4_MergePredictionResults.sh" $PREDICTIONS_FOLDER

echo "Processing complete. Check $PREDICTIONS_FOLDER for output."
