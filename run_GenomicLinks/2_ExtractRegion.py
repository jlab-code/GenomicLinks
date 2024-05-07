import os
import time
import pandas as pd
import subprocess
import traceback
import sys
import numpy as np

np.set_printoptions(suppress=True)

def write_temp_region(chrm, s1, e1, fasta_file):
    formatted_chrm = get_formatted_chrm(chrm, fasta_file)
    
    # Define the region string for bedtools
    region_str = f"{formatted_chrm}\t{s1}\t{e1}\n"

    # Write the region to a temporary file
    with open('temp_region.txt', 'w') as tmp_file:
        tmp_file.write(region_str)

    # Ensure the directory exists for the chromosome using numeric-only identifiers for folders
    numeric_chrm_dir = os.path.join(FOLDER, "chr", str(chrm))  # Directory uses numeric-only name
    os.makedirs(numeric_chrm_dir, exist_ok=True)

    # Define the output file path using numeric-only identifiers for folders
    output_file = f"{numeric_chrm_dir}/{str(s1)}_{str(e1)}.txt"

    # Execute the bedtools command to get fasta sequences
    bedtools_command = f"bedtools getfasta -fi {fasta_file} -bed temp_region.txt -fo {output_file}"
    subprocess.run(bedtools_command, shell=True)

def get_formatted_chrm(chrm, fasta_file):
    # Adjust chromosome formatting based on fasta_file naming
    if 'v5' in fasta_file or 'NAM' in fasta_file:
        return f'chr{chrm}'
    elif 'v4' in fasta_file:
        return chrm
    else:
        raise ValueError("Unknown FASTA file version or chromosome naming convention.")

def run_prediction(region_file, fasta_file):
    num_lines = sum(1 for line in open(file))
    count = 0
    start_time = time.time()
    try:
        print("Extracting regions ... ")
        df = pd.read_csv(file, sep="\t", header=None, skiprows=1)
        regions = np.array(df)
        for item in regions:
            print(item)
            chrm, s1, e1 = item[0:3]
            write_temp_region(chrm, s1, e1, fasta_file)
            count += 1
        print("Regions extracted and saved. --- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        print("Error during region extraction: " + str(e))
        print(traceback.format_exc())
    finally:
        os.remove("temp_region.txt")  # Cleanup temporary file

if __name__ == '__main__':
    FOLDER = sys.argv[1]  # Output folder for predictions
    fasta_file = sys.argv[2]  # FASTA file path

    # Prepare the output directory structure
    current_dir = os.getcwd()
    chr_dir = os.path.join(FOLDER, "chr")
    if not os.path.exists(chr_dir):
        try:
            os.makedirs(chr_dir)
        except OSError as e:
            print(f"Creation of the directory {chr_dir} failed: {e}")

    # Process regions from files
    region_files = [os.path.join(FOLDER, "region_A.csv"), os.path.join(FOLDER, "region_B.csv")]
    for file in region_files:
        run_prediction(file, fasta_file)

    # Return to the original directory
    os.chdir(current_dir)
