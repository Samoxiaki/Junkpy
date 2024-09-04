#!/usr/bin/env python3
import os
from junkpy import JunkParser
from pathlib import Path
from pydantic import BaseModel
import unittest



class DataLoadTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.PARSER = JunkParser()
		cls.FILE_PATH = Path(__file__).parent / "test_files/test_file_simple.junk"
		cls.DATA_AS_STRING = """
			{
				"key1": 1,
				"key2": "2"
			}
		"""

		class TestModel(BaseModel):
			key1: int
			key2: str
		
		cls.TEST_MODEL = TestModel

	
	def test_load_from_string(self):
		data = self.PARSER.loads(self.DATA_AS_STRING)
		self.assertIsInstance(data, dict)


	def test_load_from_string_validated(self):
		data = self.PARSER.loads(self.DATA_AS_STRING, validate_to=self.TEST_MODEL)
		self.assertIsInstance(data, self.TEST_MODEL)


	def test_load_from_file_object(self):
		data = self.PARSER.load(open(self.FILE_PATH, "rt"))
		self.assertIsInstance(data, dict)
		
	def test_load_from_file_object_validated(self):
		data = self.PARSER.load(open(self.FILE_PATH, "rt"), validate_to=self.TEST_MODEL)
		self.assertIsInstance(data, self.TEST_MODEL)
		
		
	def test_load_from_file(self):
		data = self.PARSER.load_file(self.FILE_PATH)
		self.assertIsInstance(data, dict)


	def test_load_from_file_validated(self):
		data = self.PARSER.load_file(self.FILE_PATH, validate_to=self.TEST_MODEL)
		self.assertIsInstance(data, self.TEST_MODEL)


	def test_load_from_env(self):
		os.environ["JUNK_TEST_FILE"] = str(self.FILE_PATH)
		data = self.PARSER.load_file_from_env("JUNK_TEST_FILE")	
		self.assertIsInstance(data, dict)

	
	def test_load_from_env_validated(self):
		os.environ["JUNK_TEST_FILE"] = str(self.FILE_PATH)
		data = self.PARSER.load_file_from_env("JUNK_TEST_FILE", validate_to=self.TEST_MODEL)
		self.assertIsInstance(data, self.TEST_MODEL)


if __name__ == '__main__':
	unittest.main()

