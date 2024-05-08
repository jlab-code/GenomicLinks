# GenomicLinks

GenomicLinks is a computational tool designed to predict chromatin interactions in Zea mays (maize). 
It utilizes genomic data to analyze and predict the interactions between different regions of chromatin, aiding researchers in understanding gene regulation and genome architecture in maize.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed the latest version of [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
* You have a Windows, Linux, or macOS machine.


To install GenomicLinks, follow these steps:

1. **Clone the repository**:
   Clone the GenomicLinks repository to your local machine using git:
   ```bash
   git clone https://github.com/jlab-code/GenomicLinks.git
   cd GenomicLinks

1. **Setup Conda environmnet**:
    Create and activate conda env.
    ```bash
    conda env create -f jup.yml
    conda activate jup

3. **Download Reference Genome**:
   Download the Zea mays reference genome fasta file. 
   Ensure you place it in the appropriate directory or update the script paths to its location. 
   Reference genome files can typically be found at:
   - [NCBI Zea mays](https://www.ncbi.nlm.nih.gov/genome/?term=zea+mays)
   - [Ensembl Plants for Zea mays](http://plants.ensembl.org/Zea_mays/Info/Index)

## Using GenomicLinks

1. Run the master script 0_runGenomicLinks.sh to process all steps automatically:

    ```bash
    sh 0_runGenomicLinks.sh

Make sure all paths in the script are correctly set to match your directory structure and data files.

2. Individual Script Execution:
You can also run each script individually if you need more control over the execution or for debugging purposes:

    ```bash
    python3 1_PreprocessBEDPE.R "/path/to/your/bedpe/file" "/path/to/your/scripts_directory/prediction_output" #Processes the BEDPE file and prepares data.
    python3 2_ExtractRegion.py "/path/to/your/scripts_directory/prediction_output" "/path/to/fasta/file" #Extracts regions from the genome.
    python3 3_Prediction.py "/path/to/your/scripts_directory/prediction_output" "/path/to/your/scripts_directory/weights-improvement-dp2500-58.hdf5 "#Performs the prediction of chromatin interactions.
    python3 4_MergePredictionResults.sh "/path/to/your/scripts_directory/prediction_output" #Merges all individual prediction files into a final result.


Ensure you provide the necessary arguments and paths when running each script individually.


## Web Tool

For easier access and usage, visit [genomiclinks.com](http://genomiclinks.com) where you can use GenomicLinks through a user-friendly web interface.

## Contact

If you want to contact me you can reach me at `<luca.schlegel@tum.de>`.


