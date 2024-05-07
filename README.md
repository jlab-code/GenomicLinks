# GenomicLinks

GenomicLinks is a computational tool designed to predict chromatin interactions in Zea mays (corn). 
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
* 1_PreprocessBEDPE.R: Processes the BEDPE file and prepares data.
* 2_ExtractRegion.py: Extracts regions from the genome.
* 3_Prediction.py: Performs the prediction of chromatin interactions.
* 4_MergePredictionResults.sh: Merges all individual prediction files into a final result.

Ensure you provide the necessary arguments and paths when running each script individually.


## Web Tool

For easier access and usage, visit [genomiclinks.com](http://genomiclinks.com) where you can use GenomicLinks through a user-friendly web interface.

## Contact

If you want to contact me you can reach me at `<luca.schlegel@tum.de>`.


