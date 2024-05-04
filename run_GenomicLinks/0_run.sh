#!/bin/bash
# Initialize Conda and activate the environment
source /home/luca/miniconda3/etc/profile.d/conda.sh
conda activate jup

# Run the R script
Rscript /mnt/storage3/webserver/codes/1_a_Preprocess_bedpe.R "$1"  #<remote_file_path>  
file_path="$1"


# Extract unique ID
tmp_id=${file_path#/mnt/storage3/webserver/data/input_01_}  # Removes everything before and including 'input_01_'
unique_user_id=${tmp_id%_.txt}    # Removes everything after and including the last '_'

echo "Unique User ID: $unique_user_id"
folder_path_predictions="/mnt/storage3/webserver/codes/predictions_${unique_user_id}/"




# Run the Python scripts within the Conda environment
python3 /mnt/storage3/webserver/codes/2_ExtractRegion.py "$folder_path_predictions" "$2" #<folder_path> <fasta_file_path>
python3 /mnt/storage3/webserver/codes/3_Prediction.py "$folder_path_predictions"

# Execute the shell script
sh /mnt/storage3/webserver/codes/4_MergePredictionResults.sh "$folder_path_predictions" 

# Send back zip file to the Webserver command is on webserver already
#scp -i /home/luca/.ssh/id_rsa -P 6969 /mnt/storage3/webserver/predictions/prediction.csv webserver@10.162.143.54:/var/www/html/genomiclink/output





# Deactivate the Conda environment
conda deactivate

