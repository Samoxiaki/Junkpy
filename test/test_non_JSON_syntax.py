#!/usr/bin/env python3
from junkpy import JunkParser
from re import Pattern
from pathlib import Path
from decimal import Decimal
from datetime import datetime, date, time, timedelta
import unittest



class NonJSONSyntaxTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.PARSER = JunkParser()
		cls.UNQUOTED_KEYS_DATA = """
			{
				"quoted_key": 123,
				unquoted_key: 123,
				-unquoted_key2: 123
			}
		"""
		cls.UNQUOTED_KEYS_LENGTH = 3
		cls.UNQUOTED_KEYS_TYPE = dict
		
		cls.DICT_TRAILING_COMMA_DATA = """
			{
				"key1": 123,
				"key2": 123,
			}
		"""
		cls.DICT_TRAILING_COMMA_LENGTH = 2
		cls.DICT_TRAILING_COMMA_TYPE = dict
		
		cls.LIST_TRAILING_COMMA_DATA = """
			[
				123,
				123,
			]
		"""
		cls.LIST_TRAILING_COMMA_LENGTH = 2
		cls.LIST_TRAILING_COMMA_TYPE = list
		
		cls.DICT_NULL_DATA = """
			{
				"key1": ,
				"key2": ,
				"key3": (string)
			}
		"""
		cls.DICT_NULL_LENGTH = 3
		cls.DICT_NULL_TYPE = dict
		
		cls.LIST_WITH_COMMENTS_DATA = """
			# Comment
			[ # Comment
				123,
				# Comment
				123 # Comment
			]
			
			# Comment
			# Comment
		"""
		cls.LIST_WITHOUT_COMMENTS_DATA = """
			[
				123,
				123
			]
		"""
		
		
	def test_unquoted_keys(self):
		data = self.PARSER.loads(self.UNQUOTED_KEYS_DATA)
		self.assertIsInstance(data, self.UNQUOTED_KEYS_TYPE, msg=f"{type(data)}, {self.UNQUOTED_KEYS_TYPE}")
		self.assertEqual(len(data), self.UNQUOTED_KEYS_LENGTH, msg=f"{len(data)}, {self.UNQUOTED_KEYS_LENGTH}")
		
		
	def test_dict_trailing_comma(self):
		data = self.PARSER.loads(self.DICT_TRAILING_COMMA_DATA)
		self.assertIsInstance(data, self.DICT_TRAILING_COMMA_TYPE, msg=f"{type(data)}, {self.DICT_TRAILING_COMMA_TYPE}")
		self.assertEqual(len(data), self.DICT_TRAILING_COMMA_LENGTH, msg=f"{len(data)}, {self.DICT_TRAILING_COMMA_LENGTH}")
		
		
	def test_list_trailing_comma(self):
		data = self.PARSER.loads(self.LIST_TRAILING_COMMA_DATA)
		self.assertIsInstance(data, self.LIST_TRAILING_COMMA_TYPE, msg=f"{type(data)}, {self.LIST_TRAILING_COMMA_TYPE}")
		self.assertEqual(len(data), self.LIST_TRAILING_COMMA_LENGTH, msg=f"{len(data)}, {self.LIST_TRAILING_COMMA_LENGTH}")
		
		
	def test_dict_null(self):
		data = self.PARSER.loads(self.DICT_NULL_DATA)
		self.assertIsInstance(data, self.DICT_NULL_TYPE, msg=f"{type(data)}, {self.DICT_NULL_TYPE}")
		self.assertEqual(len(data), self.DICT_NULL_LENGTH, msg=f"{len(data)}, {self.DICT_NULL_LENGTH}")
	
	
	def test_comments(self):
		with_comments = self.PARSER.loads(self.LIST_WITH_COMMENTS_DATA)
		without_comments = self.PARSER.loads(self.LIST_WITHOUT_COMMENTS_DATA)
		self.assertEqual(with_comments, without_comments, msg=f"{with_comments}, {without_comments}")



if __name__ == '__main__':
	unittest.main()

