import unittest
import time
import os
from src.build_inverted_index import *

class MyTestCase(unittest.TestCase):

    # def test_build_inverted_index(self):
    #     root_path = '../../data/maildir/allen-p/_sent_mail/'
    #     # filename = '6.'
    #     filename = ''
    #     filepath = os.path.join(root_path, filename)
    #
    #     start = time.time()
    #     inv_index_list = training(filepath)
    #     end = time.time()
    #     print(end - start)
    #     print(inv_index_list)
    #     # self.assertEqual(True, False)

    def test_term_selection(self):
        root_path = '../../data/maildir/'
        start = time.time()
        selected_term_list = term_selection(root_path)
        end = time.time()
        print(selected_term_list)
        print(len(selected_term_list))

if __name__ == '__main__':
    unittest.main()
