import numpy as np
import pickle
from scipy.sparse import csc_matrix
from scipy import spatial
from sklearn.preprocessing import normalize
from src.preprocessing import tokenize

def tf_idf_search(quest: str, query_top_n: int = 10, n_select_term: int = 1000, store_path='../result/'):
    '''

    :param quest: a string of quest words seperated by space. like: "AAA BB"
    :param query_top_n:
    :param n_select_term:
    :return: a list of file index
    '''

    # Read necessary files
    with open(store_path+'selected_term_list.pkl', 'rb') as f:
        selected_term_list = pickle.load(f)

    term2num_dict = {selected_term_list[n]: n for n in range(len(selected_term_list))}

    # print(term2num_dict)

    with open(store_path+'tf_idf_sparse_matrix.pkl', 'rb') as fm:
        tf_idf_csc_matrix = pickle.load(fm)

    #
    with open(store_path + 'inverted_idx.pkl', 'rb') as fb:
        inverted_idx_dict = pickle.load(fb)

    tokens = tokenize(quest)
    sqrt_n = np.sqrt(len(tokens))
    quest_vec = np.zeros(dtype=np.float, shape=(n_select_term, 1))
    for t in tokens:
        quest_vec[term2num_dict[t]] = 1.0
        quest_vec[term2num_dict[t]] *= inverted_idx_dict[t][0]

    quest_vec = normalize(quest_vec, norm='l2', axis=1)

    score_array = tf_idf_csc_matrix.multiply(quest_vec)
    score_array = score_array.sum(axis = 0)

    result_list = list(np.array(score_array.argsort())[0])[::-1][0: query_top_n]

    return [score_array, result_list]








