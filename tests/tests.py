import unittest
import pandas as pd
import numpy as np
from glob import glob
from ej1 import *
from ej2 import *
from ej3 import *
from ej4 import *
from ej5 import *
from main import *

class TestDataExpl(unittest.TestCase):

    @classmethod
    def setUpClass(test_sca):
        test_sca._df = main_build_main_data()
	
	def get_basic_data(self):
		self.assertEqual(len(self._df),3)
		self.assertTrue(len(self._df[0])>0)
		self.assertTrue(len(self._df[1])>0)
		self.assertTrue(len(self._df[2])>0)
		self.assertTrue(isinstance(get_clean_data_csv('../../data/covid_concern_polls.csv'),pd.DataFrame))
    
	def plots_existence(self):
		main_do_all_execise()
		self.assertTrue(glob('*.png')==6)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDataExpl))
unittest.TextTestRunner(verbosity=2).run(suite)