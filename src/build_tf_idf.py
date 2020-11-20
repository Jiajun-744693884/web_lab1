import os
import json
import progressbar
from src.preprocessing import preprocess_email
from collections import Counter
import pickle
from scipy.sparse import csc_matrix
from sklearn.preprocessing import normalize
import numpy as np
import math

store_path = '../result/'
N = 517401

def calculate_tf_idf(tf, df):
    return (1 + math.log(tf, 10)) * (math.log(N / df, 10))

def build_tf_idf_matrix(root_path):
    '''
    Build tf-idf matrix as a csc sparse matrix.
    :param root_path:
    :return:
    '''
    row = []
    col = []
    data = []
    with open(store_path+'selected_term_list.pkl', 'rb') as f:
        selected_term_list = pickle.load(f)
    with open(store_path + 'inverted_idx.pkl', 'rb') as fb:
        inverted_idx_dict = pickle.load(fb)

    term2num_dict = {selected_term_list[n] : n for n in range(len(selected_term_list))}

    p = progressbar.ProgressBar()
    file_total = 517408 + 1
    p.start(file_total)
    file_count = 0
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if '.json' in filename or '.DS_Store' in filename or '.txt' in filename:
                continue
            filepath = os.path.join(root, filename)

            # try:
            word_list = preprocess_email(filepath)
            word_count = Counter(word_list)
            # calculate tf-idf value
            for word, tf in word_count.items():
                if word in selected_term_list:
                    df = inverted_idx_dict[word][0]
                    col.append(file_count)
                    row.append(term2num_dict[word])
                    data.append(calculate_tf_idf(tf, df))
            file_count += 1
            p.update(file_count)
            # except Exception as e:
            #     print(f"[Exception] at {filepath}: {e}")

    tf_idf_matrix = csc_matrix((data, (row, col)), shape=(len(selected_term_list), file_count))
    tf_idf_matrix = normalize(tf_idf_matrix, norm='l2', axis=0)
    p.finish()

    with open(store_path+'tf_idf_sparse_matrix.pkl','wb') as m:
        pickle.dump(tf_idf_matrix, m)

    return tf_idf_matrix
