import os
import re
import sys
import numpy as np
import math
# import pandas as pd
# import matplotlib.pyplot as plt
from collections import Counter
import random

# dim_list = [17, 80, 26, 88, 90, 96, 57, 76, 70, 55, 54, 57, 61, 11, 38, 53, 94, 94, 92, 21, 23, 3, 45, 73, 41]
dim_list = [0, 1, 4, 6, 7, 8, 11, 14, 16, 17, 18, 19, 21, 22, 26, 28, 31, 33, 34, 35, 36, 37, 40, 42, 45, 47, 50, 51, 52, 54, 55, 57, 59, 60, 63, 65, 69, 71, 75, 81, 82, 87, 89, 91, 92, 93, 94, 96, 98, 99]
skyline_folder = "/Users/sliu104/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test/"
query_folder = "./"
raw_data_folder = "./"
projected_dim = 2
data_type = "random"
cardinality = 100000
top_k = 25

def dot(K, L):
    if len(K) != len(L):
        return 0
    return float("{0:.5f}".format(sum(i[0] * i[1] for i in zip(K, L))))


def load_data(raw_data_file_, card_, projected_dim_):
    f = open(raw_data_file_, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    data_list = []
    for i in range(card_):
        current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
    f.close()
    return data_list


def load_query(query_file_, card_, projected_dim_):
    f = open(query_file_, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    query_list = []
    for i in range(card_):
        current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        query_list.append(current_data_record)
    f.close()
    return query_list


def load_skyline_data(skyline_file_):
    f = open(skyline_file_, 'r')
    lines = f.readlines()
    cur_dim = int(lines[0])
    cur_card = int(lines[1])
    data_list = []
    for i in range(cur_card):
        current_data_record = np.fromstring(lines[i + 2], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
    f.close()
    return data_list, cur_card


def compute_ground_truth(query_, data_list_, top_k_):
    grountTruth_ = []
    dot_val_list_ = []
    for jj in range(data_list_.__len__()):
        dot_val_list_.append(dot(query_, data_list_[jj]))  # dot product value, the larger the better
    temp_grountTruth_ = np.argsort(dot_val_list_)[::-1]
    temp_grountTruth_ = temp_grountTruth_[0:top_k_]
    grountTruth_.extend(temp_grountTruth_)
    return grountTruth_


def compute_recall(grountTruth_, ret_index_):
    intersection = len(list(set(grountTruth_).intersection(set(ret_index_))))
    return float(1.0 * intersection / len(grountTruth_))


def load_ground_truth(ground_truth_file_, card_):
    f = open(ground_truth_file_, 'r')
    lines = f.readlines()
    data_list = []
    for i in range(card_):
        current_data_record = np.fromstring(lines[i], dtype=float, sep=' ')
        current_data_record = np.asarray(current_data_record)
        data_list.append(current_data_record)
    f.close()
    return data_list


result = {}
query_size = 100
ground_truth_file = "./ground_truth_100k.txt"
ground_truth = load_ground_truth(ground_truth_file, query_size)
for ii in range(dim_list.__len__()):
    dim_interest = dim_list[ii]
    query_file = query_folder + str(projected_dim) + "D_" + str(dim_interest) + ".txt"
    raw_data_file = raw_data_folder + data_type + "_" + str(dim_interest) + "_" + str(cardinality) + ".txt"
    raw_data = load_data(raw_data_file, cardinality, projected_dim)
    query_data = load_query(query_file, query_size, projected_dim)

    temp_ground_truth = []
    for jj in range(query_size):  # for each query compute top-k, use map for cache
        # groud_truth = compute_ground_truth(query_data[jj], raw_data, top_k) # for each query a top-k result
        # temp_ground_truth = groud_truth

        temp_ground_truth = ground_truth[jj]
        temp_local_result = []

        for kk in range(top_k):
            temp_dot_val = []
            skyline_file = skyline_folder + data_type + "_" + str(dim_interest) + "_" + str(
                cardinality) + "_qhull_layer_" + str(kk)
            skyline_data, skyline_size = load_skyline_data(skyline_file)

            for tt in range(skyline_data.__len__()):
                temp_dot_val.append(dot(query_data[jj], skyline_data[tt]))

                # raw_data = np.asarray(raw_data)
            skyline_data = np.asarray(skyline_data)
            min_length = min(top_k - kk, skyline_size)
            temp_index = np.argsort(temp_dot_val)[::-1][0: min_length]
            local_result = skyline_data[temp_index, 2]
            temp_local_result.extend(local_result)
        # print(temp_ground_truth)
        # print(temp_local_result)
        temp_recall = compute_recall(temp_ground_truth, set(temp_local_result))
        print("current selected dimension: " + str(dim_interest) + ", query index: " + str(jj) + ", current recall: " + str(temp_recall))
        # print(temp_recall)

print('Done')

# for jj in range(query_size):  # for each query compute top-k, use map for cache
#     groud_truth = compute_ground_truth(query_data[jj], raw_data, top_k)
#     temp_ground_truth = groud_truth
#     temp_dot_val = []
#     for tt in range(raw_data.__len__()):
#         temp_dot_val.append(dot(query_data[jj], raw_data[tt]))
#
#         raw_data = np.asarray(raw_data)
#
#     min_length = min(top_k - kk, skyline_size)
#     temp_index = np.argsort(temp_dot_val)[::-1][0: min_length]
#     local_result = raw_data[temp_index, 2]
#     if jj in temp_result.keys():
#         temp_result[jj] = np.asarray(np.concatenate((temp_result[jj], local_result), axis=None))
#     else:
#         temp_result[jj] = local_result


