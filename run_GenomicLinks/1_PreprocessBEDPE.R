#!/usr/bin/env Rscript

# Clear the environment and load necessary libraries
rm(list = ls())
library(dplyr)
library(data.table)

# Command line arguments for file paths
args <- commandArgs(trailingOnly = TRUE)
bedpe_file_path <- args[1]
output_folder <- args[2] 

# Check if the output folder exists, and create it if it doesn't
if (!dir.exists(output_folder)) {
  dir.create(output_folder, recursive = TRUE)
  message("Output folder created at: ", output_folder)
}

# Read the BEDPE file
raw.bedpe <- fread(bedpe_file_path)
raw.bedpe <- data.frame(raw.bedpe)

# Check data and adjust columns if necessary
if (ncol(raw.bedpe) > 6) {
  raw.bedpe <- select(raw.bedpe, 1:6)
  message("Extra columns removed. Data has correct format now.")
} else {
  message("Data has correct format.")
}

# Adjust the difference between s1 and e1 to 2500
midpoint <- round((raw.bedpe[,2] + raw.bedpe[,3]) / 2)
raw.bedpe[,2] <- midpoint - 1250
raw.bedpe[,3] <- midpoint + 1250

# Adjust the difference between s2 and e2 to 2500
midpoint2 <- round((raw.bedpe[,5] + raw.bedpe[,6]) / 2)
raw.bedpe[,5] <- midpoint2 - 1250
raw.bedpe[,6] <- midpoint2 + 1250

# Name the columns appropriately
colnames(raw.bedpe) <- c("chr1", "s1", "e1", "chr2", "s2", "e2")

# Save the adjusted bedpe file
fwrite(raw.bedpe, file.path(output_folder, "out.csv"), sep = "\t", scipen = 50)

# Create and write distinct regions A and B
tmpA <- distinct(raw.bedpe, chr1, s1, e1)
fwrite(tmpA, file.path(output_folder, "region_A.csv"), sep = "\t", scipen = 50)

tmpB <- distinct(raw.bedpe, chr2, s2, e2)
fwrite(tmpB, file.path(output_folder, "region_B.csv"), sep = "\t", scipen = 50)

# Create unique folders
uniqFolder<-unique(raw.bedpe$chr1)

# Create main chr and sun chr
dir.create(file.path(output_folder,"/chr"), showWarnings = FALSE)
mainDir= paste0(output_folder,"/chr")
for (subDir in uniqFolder){
  dir.create(file.path(mainDir,subDir), showWarnings = FALSE)
}

message("Pairs created and files saved to ", output_folder)
