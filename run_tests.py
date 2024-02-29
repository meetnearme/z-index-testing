import sys 
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_src.tests.test_queries import TestSpatialQueries
import unittest

if __name__ == "__main__":
    unittest.main()
