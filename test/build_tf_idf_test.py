import unittest
import time
import os
from src.build_tf_idf import *

class MyTestCase(unittest.TestCase):
    def test_build_tf_idf(self):
        root_path = '../../data/maildir/'
        start = time.time()
        tf_idf_csc = build_tf_idf_matrix(root_path)
        end = time.time()
        print(end - start)
        print(tf_idf_csc.toarray()[:, 0])


if __name__ == '__main__':
    unittest.main()
