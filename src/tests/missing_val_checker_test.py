import unittest
import pandas as pd
import numpy as np
from template_client import TemplateClient
from mock_template import MockTemplate
import sys
sys.path.append("../commands")
from missing_val_checker import MissingValChecker

class MissingValCheckerTest(unittest.TestCase):
    '''
    '''
    
    def setUp(self):
        self.template_client = TemplateClient()
        self.mock_template = MockTemplate("mock_template", "a")
        self.template_client.add_template("mock_template", self.mock_template)
        self.mv = MissingValChecker("mock_template")
        
    def test_initialization(self):
        result = isinstance(self.mv, MissingValChecker)
        self.assertTrue(result)
        
    def test_completely_empty_dataframe(self):
        df = pd.DataFrame(columns = [])
        expected_result = [("a", -1), ("e", -1), ("f", -1)]
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_only_headers_dataframe(self):
        df = pd.DataFrame(columns = ["a", "b", "c", "d", "e", "f"])
        expected_result = [("a", -1), ("e", -1), ("f", -1)]
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_only_rows_dataframe(self):
        df = pd.DataFrame(columns = [],
                          index = [1, 1])
        expected_result = [("a", -1), ("e", -1), ("f", -1)]
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_no_fields_dataframe(self):
        df = pd.DataFrame(columns = ["a", "b", "c", "d", "e", "f"],
                          index = [0, 1])
        expected_result = [("a", 0), ("e", 0), ("f", 0),
                           ("a", 1), ("e", 1), ("f", 1)]
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
    
    def test_compete_one_row_dataframe(self):
        df = pd.DataFrame(columns = ["a", "b", "c", "d", "e", "f"],
                          index = [0],
                          data = [[1,1,1,1,1,1]])
        expected_result = []
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_compete_two_rows_dataframe(self):
        df = pd.DataFrame(columns = ["a", "b", "c", "d", "e", "f"],
                          index = [0, 1],
                          data = [[1,1,1,1,1,1],
                                  [1,1,1,1,1,1]])
        expected_result = []
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_no_mandatory_headers(self):
        df = pd.DataFrame(columns = ["b", "c", "d"],
                          index = [0, 1],
                          data = [[1,1,1],
                                  [1,1,1]])
        expected_result = [("a", -1), ("e", -1), ("f", -1)]
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_only_mandatory_headers(self):
        df = pd.DataFrame(columns = ["a", "e", "f"],
                          index = [0, 1],
                          data = [[1,1,1],
                                  [1,1,1]])
        expected_result = []
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_mixed_headers(self):
        df = pd.DataFrame(columns = ["a", "c", "d"],
                          index = [0, 1],
                          data = [[1,1,1],
                                  [1,1,1]])
        expected_result = [("e", -1), ("f", -1)]
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_empty_string(self):
        df = pd.DataFrame(columns = ["a", "b", "c", "d", "e", "f"],
                          index = [0, 1],
                          data = [[1, 1, 1, 1, 1, ""],
                                  [1, 1, 1, 1, 1, ""]])
        expected_result = [("f", 0), ("f", 1)]
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_weird_indices_complete(self):
        df = pd.DataFrame(columns = ["a", "b", "c", "d", "e", "f"],
                          index = ["apple", "orange"],
                          data = [[1, 1, 1, 1, 1, 1],
                                  [1, 1, 1, 1, 1, 1]])
        expected_result = []
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)
        
    def test_weird_indices_incomplete(self):
        df = pd.DataFrame(columns = ["a", "b", "c", "d", "e"],
                          index = ["apple", "orange"],
                          data = [[np.nan, 1, 1, 1, 1],
                                  [1, 1, 1, 1, 1]])
        expected_result = [("a", 0), ("f", -1)]
        result = self.mv.execute(df, self.template_client)
        self.assertCountEqual(expected_result, result)    
    
if __name__ == '__main__':
    unittest.main(exit=False)