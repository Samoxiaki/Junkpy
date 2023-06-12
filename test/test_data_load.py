#!/usr/bin/env python3
from junkpy import Junkpy
from pathlib import Path
import unittest



class DataLoadTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.PARSER = Junkpy()
		cls.FILE_PATH = Path(__file__).parent / "test_files/test_file_simple.junk"
		cls.DATA_AS_STRING = """
			{
				"key1": 1,
				"key2": "2"
			}
		"""

	
	def test_load_from_string(self):
		data = self.PARSER.loads(self.DATA_AS_STRING)
		self.assertIsInstance(data, dict)


	def test_load_from_file_object(self):
		data = self.PARSER.load(open(self.FILE_PATH, "rt"))
		self.assertIsInstance(data, dict)
		
		
	def test_load_from_file(self):
		data = self.PARSER.load_file(self.FILE_PATH)
		self.assertIsInstance(data, dict)


if __name__ == '__main__':
	unittest.main()

