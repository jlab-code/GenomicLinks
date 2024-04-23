import os
import time
import pandas as pd
import subprocess
import traceback
import sys
import numpy as np

np.set_printoptions(suppress=True)

def write_temp_region_old(chrm, s1, e1, fasta_file):
    with open('temp_region.txt', 'w') as tmp_file:
        tmp_file.write(str(chrm) + "\t" + str(s1) + "\t" + str(e1))
        tmp_file.close()
    with open('temp_bash.sh', 'w') as the_file:
        the_file.write(
            f"bedtools getfasta -fi {fasta_file} -bed temp_region.txt > {str(chrm)}/{str(s1)}_{str(e1)}.txt")
    subprocess.call(["sh", "./temp_bash.sh"])


def index_fasta_file(fasta_file):
    # Index the fasta file using samtools faidx
    subprocess.run(f"samtools faidx {fasta_file}", shell=True, check=True)

def get_formatted_chrm(chrm, fasta_file):
    # Determine whether the reference is v4 or v5 based on the fasta_file name or another indicator
    if 'v5' in fasta_file or 'NAM' in fasta_file:
        # v5 references use 'chr' + number
        return f'chr{chrm}'
    elif 'v4' in fasta_file:
        # v4 references use just the number, no 'chr' prefix
        return chrm
    else:
        raise ValueError("Unknown FASTA file version or chromosome naming convention.")

def write_temp_region(chrm, s1, e1, fasta_file):
    formatted_chrm = get_formatted_chrm(chrm, fasta_file)
    
    # Define the region string using the appropriate chromosome format for bedtools
    region_str = f"{formatted_chrm}\t{s1}\t{e1}\n"

    # Write the region to a temporary file
    with open('temp_region.txt', 'w') as tmp_file:
        tmp_file.write(region_str)

    # Ensure the directory exists for the chromosome using numeric-only identifiers for folders
    numeric_chrm_dir = os.path.join(FOLDER, "chr", str(chrm))  # Directory uses numeric-only name
    os.makedirs(numeric_chrm_dir, exist_ok=True)

    # Define the output file path using numeric-only identifiers for folders
    output_file = f"{numeric_chrm_dir}/{str(s1)}_{str(e1)}.txt"

    # Prepare the bedtools command using the appropriate chromosome format for bedtools
    bedtools_command = f"bedtools getfasta -fi {fasta_file} -bed temp_region.txt -fo {output_file}"

    # Execute the bedtools command
    subprocess.run(bedtools_command, shell=True)


    
def run_prediction(file, fasta_file):
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
        print("Writing into file ... ")
        print("--- %s seconds ---" % (time.time() - start_time))
        os.remove("temp_region.txt")  # Remove only the temp_region.txt file
    except Exception as e:
        print("type error: " + str(e))
        print(traceback.format_exc())


if __name__ == '__main__':
    # CHANGES HERE
    FOLDER= sys.argv[1]
    fasta_file = sys.argv[2] #'/mnt/storage3/webserver/fasta/Zm-B73-REFERENCE-NAM-5.0.fa' #sys.argv[2]
    #index_fasta_file(fasta_file) # only run this for creatin of fasta/move/modification etc. 
    current_dir=os.getcwd()
    dir = os.path.join(FOLDER, "chr")
    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except OSError:
            print("Creation of the directory failed")
    os.chdir(dir)
    regionFile=["../region_A.csv","../region_B.csv"]
    for i in range(len(regionFile)):
        run_prediction(regionFile[i], fasta_file)
    os.chdir(current_dir)

