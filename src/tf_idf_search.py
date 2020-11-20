import numpy as np
import pickle
from scipy.sparse import csc_matrix
from scipy import spatial
from src.preprocessing import tokenize
from src.build_tf_idf import store_path

def tf_idf_search(quest: str, query_n: int = 10):
    with open(store_path+'selected_term_list.pkl', 'rb') as f:
        selected_term_list = pickle.load(f)

    term2num_dict = {selected_term_list[n]: n for n in range(len(selected_term_list))}

    with open(store_path+'tf_idf_sparse_matrix.pkl', 'rb') as fm:
        tf_idf_csc_matrix = pickle.load(fm)

    tokens = tokenize(quest)
    sqrt_n = np.sqrt(len(tokens))
    quest_vec = np.zeros(dtype=np.float, shape=(1000, 1))
    for t in tokens:
        quest_vec[term2num_dict[t]] = 1.0 / sqrt_n

    score_array = tf_idf_csc_matrix.multiply(quest_vec)
    score_array = score_array.sum(axis = 0)
    print(score_array)
    result_list = list(np.array(score_array.argsort())[0])[::-1][0:10]
    return result_list








