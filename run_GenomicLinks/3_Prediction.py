#!/usr/bin/env python

# validating interacts in memory based on CPU/GPU
import os
import time
import pandas as pd
import traceback
import numpy as np
import sys
from keras.models import load_model
from itertools import chain
import re


np.set_printoptions(suppress=True)


def matrix_fasta_regions(chrm, tmp_one, tmp_two, reference_version='v4'):
    # Adjust file_path construction based on reference version
    if reference_version == 'v5':
        chrm_str = 'chr' + str(chrm)
    else:
        chrm_str = str(chrm)   
    file_path = chr_dir + chrm_str + "/" + str(tmp_one) + "_" + str(tmp_two) + ".txt"
    fp = open(file_path)
    arr_matrix = np.zeros((4, 2500))  # ACGT
    for i, line in enumerate(fp):
        if i == 1:  # Assuming the sequence starts at the second line of the file
            for line_character_count, c in enumerate(line.strip()):
                if c in "ACGT":
                    arr_matrix["ACGT".index(c)][line_character_count] = 1
                elif c == "N":  # Unknown
                    arr_matrix[:, line_character_count] = 0.25
                elif c == "D":  # Deletion
                    arr_matrix[:, line_character_count] = 0  # or however you want to handle deletions
    fp.close()
    return arr_matrix.astype('int')


def prediction(test1, test2):
    pred_result = []
    pred_labels = model.predict([test1, test2])
    for item in zip(pred_labels):
        if np.round(item) == 1:
            result = 1
        else:
            result = 0
        pred_result.append([result, "%.8f" % item[0][0]])
    return pred_result


def ext_first(lst):
    return [item[1] for item in lst]


def ext_second(lst):
    return [item[0] for item in lst]


def run_prediction(csvfile):
    num_lines = sum(1 for line in open(csvfile))
    chunk_size = 20000
    first_record = True
    tmp_s1 = []
    tmp_e1 = []
    count = 0
    file_number = 0
    try:
        for chunk in pd.read_csv(csvfile, sep="\t", header=None, skiprows=1,
                                 chunksize=chunk_size):
            start_time = time.time()
            test1 = []
            test2 = []
            A = []
            B = []
            main_predict=[]
            tmp_records = []
            regions = np.array(chunk)
            for item in regions:

                if first_record:
                    chrm1 = item[0]
                    tmp_s1 = item[1]
                    tmp_e1 = item[2]
                    test1 = matrix_fasta_regions(chrm1, tmp_s1, tmp_e1)
                    first_record = False

                if  tmp_s1 != item[1] and tmp_e1 != item[2]:
                    test1 = matrix_fasta_regions(item[0], item[1], item[2])
                    chrm1 = item[0]
                    tmp_s1 = item[1]
                    tmp_e1 = item[2]
                print(chrm1,tmp_s1,tmp_e1,"\t",item[3], item[4], item[5])
                test2 = matrix_fasta_regions(item[3], item[4], item[5])
                A.append(test1)
                B.append(test2)
                count += 1
                tmp_records.append([chrm1, tmp_s1, tmp_e1,item[3], item[4], item[5]])

            A = np.array(A).transpose(0, 2, 1)
            B = np.array(B).transpose(0, 2, 1)
            print("\n--- Computing predictions ... ---")
            result = prediction(A, B)
            main_predict.append(result)
            first_record = True
            print("--- Processed: ", count, "out of: ", num_lines)
            main_predict = list(chain.from_iterable(main_predict))
            dataframe = pd.DataFrame(tmp_records, columns=['chr', 's1', 'e1', 'chr', 's2', 'e2'])
            dataframe['prob'] = ext_first(main_predict)
            dataframe['interacted'] = ext_second(main_predict)
            dataframe = dataframe.reset_index(drop=True)
            print("--- Writing into file ... ---- ")
            file_number += 1
            dataframe.to_csv(output + "/pred-" + str(file_number) + "-" + str(count) +
                             ".csv", sep='\t', index=False, encoding='utf-8')
            print("--- %s seconds ---" % (time.time() - start_time))
            print(15*"-")

    except Exception as e:
        print("type error: " + str(e))
        print(traceback.format_exc())





FOLDER = sys.argv[1]
chr_dir = FOLDER+"chr/"
output = FOLDER

model = load_model('/var/www/html/Gp/program/data/weights-improvement-dp2500-58.hdf5')


run_prediction(FOLDER+"/out.csv")

