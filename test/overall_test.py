import unittest
import time
from src.preprocessing import *
from src.build_inverted_index import *
from src.build_tf_idf import *
from src.tf_idf_search import *
from src.bool_search import *

class MyTestCase(unittest.TestCase):
    def test_all(self):
        root_path = '../../data/maildir/'
        store_path = '../result/overall/'
        n_select_term = 1000
        start = time.time()
        print("[selecting term ...]")
        # selected_term_list = term_selection(root_path, n_select_term, store_path)

        print("[building inverted index dict ...]")
        # inv_index_list = build_inverted_index(root_path, store_path)

        print("[building tf-idf matrix ...]")
        # tf_idf_csc = build_tf_idf_matrix(root_path, store_path)

        # print(tf_idf_csc.toarray())
        with open(store_path + 'num2file.pkl', 'rb') as f:
            num2file_dict = pickle.load(f)
        bool_search_answer = bool_search(store_path + 'inverted_idx.pkl')
        for answer in bool_search_answer:
            print(num2file_dict[answer])
        # query = "color concret"
        # query = 'hcfr part tile'
        # query = 'enronxg'
        query = 'new market'
        score_array, query_result = tf_idf_search(query, query_top_n=10, n_select_term=n_select_term, store_path=store_path)
        # print(query_result)
        for t in query_result:
             print(num2file_dict[t])
             print(score_array[0, t])
             print()

        end = time.time()
        print(end - start)



if __name__ == '__main__':
    unittest.main()
