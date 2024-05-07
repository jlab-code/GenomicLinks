#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import numpy as np
from keras.models import load_model
from tensorflow.keras import backend as K
import time
import traceback
import sys

np.set_printoptions(suppress=True)

def matrix_fasta_regions(chrm, tmp_one, tmp_two, chr_dir):
    arr_matrix = np.zeros((4, 2500))  # ACGT
    with open(os.path.join(chr_dir, f"{chrm}/{tmp_one}_{tmp_two}.txt")) as fp:
        for i, line in enumerate(fp):
            if i == 1:  # Assuming the sequence starts at the second line of the file
                for j, c in enumerate(line.strip()):
                    if c in "ACGT":
                        arr_matrix["ACGT".index(c), j] = 1
                    elif c == "N":  # Equal distribution for 'N'
                        arr_matrix[:, j] = 0.25
                    elif c == "D":  # Zero for deletions 'D'
                        arr_matrix[:, j] = 0
    arr_matrix = arr_matrix.astype(int)
    return arr_matrix

def prediction(test1, test2, model):
    pred_labels = model.predict([test1, test2])
    return np.round(pred_labels[:, 0]), pred_labels[:, 0]

def run_prediction(csvfile, chr_dir, output, model):
    num_lines = sum(1 for line in open(csvfile))
    chunk_size = 50000  # Adjust chunk size in case of memory allocation errors.
    file_number = 0
    try:
        for chunk in pd.read_csv(csvfile, sep="\t", header=None, skiprows=1, chunksize=chunk_size):
            start_time = time.time()
            A, B, records = [], [], []
            for item in np.array(chunk):
                chrm1, s1, e1, chrm2, s2, e2 = item
                test1 = matrix_fasta_regions(chrm1, s1, e1, chr_dir)
                test2 = matrix_fasta_regions(chrm2, s2, e2, chr_dir)
                A.append(test1)
                B.append(test2)
                records.append([chrm1, s1, e1, chrm2, s2, e2])

            A = np.array(A).transpose(0, 2, 1)
            B = np.array(B).transpose(0, 2, 1)
            interacted, probs = prediction(A, B, model)

            dataframe = pd.DataFrame(records, columns=['chr1', 's1', 'e1', 'chr2', 's2', 'e2'])
            dataframe['interacted'] = interacted
            dataframe['prob'] = probs

            output_filename = os.path.join(output, f"predictions-{file_number}.csv")
            # Ensure the directory exists
            os.makedirs(output, exist_ok=True)
            dataframe.to_csv(output_filename, sep='\t', index=False, encoding='utf-8')
            file_number += 1
            print(f"Processed chunk: {file_number}, Time taken: {time.time() - start_time}s")
            # Clear session to avoid memory leak
            if 'K' in globals():
                K.clear_session()

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    predictions_dir = sys.argv[1]  # Directory for input and output
    model_path = sys.argv[2]  # Model file path
    model = load_model(model_path)

    output = os.path.join(predictions_dir, "predictions")
    csvfile = os.path.join(predictions_dir, "out.csv")
    chr_dir = os.path.join(predictions_dir, "chr")

    run_prediction(csvfile, chr_dir, output, model)
    print(f"Completed predictions for directory: {predictions_dir}")

