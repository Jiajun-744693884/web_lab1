import unittest
import time
import os
from src.preprocessing import *

class MyTestCase(unittest.TestCase):
    def test_preprocessing(self):
        root_path = '../../data/maildir/allen-p/_sent_mail/'
        filename = '2.'
        filepath = os.path.join(root_path, filename)
        start = time.time()
        msg = preprocess_email(filepath)
        end = time.time()
        print(end - start)
        print(msg)
        # self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
