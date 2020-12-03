import time
from src.preprocessing import *
from src.build_inverted_index import *
from src.build_tf_idf import *
from src.tf_idf_search import *
from src.bool_search import *

if __name__ == '__main__':
    root_path = '../dataset/maildir/'
    store_path = '../result/'
    n_select_term = 1000

    # do preprocessing to all files and save pkl
    preprocess_all_files(root_path)

    Ndoc = get_file_num(root_path)
    print("[selecting term ...]")
    selected_term_list = term_selection(root_path, n_select_term, store_path)

    print("[building inverted index dict ...]")
    inv_index_list = build_inverted_index(root_path, store_path)

    print("[building tf-idf matrix ...]")
    tf_idf_csc = build_tf_idf_matrix(root_path, store_path)

    with open(store_path + 'num2file.pkl', 'rb') as f:
        num2file_dict = pickle.load(f)

    print("======= bool search ========")
    bool_search_answer = bool_search(store_path + 'inverted_idx.pkl', Ndoc=Ndoc)
    print("search result: ")
    for answer in bool_search_answer:
        print(f"file: {num2file_dict[answer]}")

    print()
    print("======= semantic search ========")
    query = input("[Input your query: (words to be searched, separated by space)] ")
    start = time.time()
    score_array, query_result = tf_idf_search(query, Ndoc=Ndoc, query_top_n=10, n_select_term=n_select_term, store_path=store_path)

    print("search result: ")
    for i, t in enumerate(query_result):
         print(f"======= No.{i+1} =======")
         print(f"file: {num2file_dict[t]}")
         print(f"score: {score_array[0, t]}")

    end = time.time()
    print(f"semantic search time: {end - start}")
