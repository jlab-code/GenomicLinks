# GenomicLinks

GenomicLinks is a computational tool designed to predict chromatin interactions in Zea mays (corn). 
It utilizes genomic data to analyze and predict the interactions between different regions of chromatin, aiding researchers in understanding gene regulation and genome architecture in maize.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed the latest version of [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
* You have a Windows, Linux, or macOS machine.

## Installing GenomicLinks

To install GenomicLinks, follow these steps:

Linux and macOS:
conda env create -f jup.yml
conda activate jup


## Using GenomicLinks

1. Run the master script 0_runGenomicLinks.sh to process all steps automatically:
sh 0_runGenomicLinks.sh

Make sure all paths in the script are correctly set to match your directory structure and data files.

2. Individual Script Execution:
You can also run each script individually if you need more control over the execution or for debugging purposes:
    1_PreprocessBEDPE.R: Processes the BEDPE file and prepares data.
    2_ExtractRegion.py: Extracts regions from the genome.
    3_Prediction.py: Performs the prediction of chromatin interactions.
    4_MergePredictionResults.sh: Merges all individual prediction files into a final result.

Ensure you provide the necessary arguments and paths when running each script individually.


## Contact

If you want to contact me you can reach me at `<luca.schlegel@tum.de>`.


