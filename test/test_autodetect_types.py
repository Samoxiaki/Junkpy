#!/usr/bin/env python3
from junkpy import JunkParser
from pathlib import Path
import unittest




class AutodetectTypesTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.PARSER = JunkParser()
		cls.FILE_PATH = Path(__file__).parent / "test_files/test_file_autodetected_types.junk"
		cls.KEY_TYPE_PAIRS = {
			"string": str,
			"int": int,
			"float": float,
			"bool": bool,
			"list": list,
			"empty_list": list,
			"dict": dict,
			"empty_dict": dict,
			"null": type(None)
		}
		cls.KEY_TO_BOOL = {
			"empty_list":  False,
			"empty_dict": False, 
			"list": True,
			"dict": True
		}
		
		
	def test_autodetection(self):
		data = self.PARSER.load_file(self.FILE_PATH)
		
		for key, key_type in self.KEY_TYPE_PAIRS.items():
			with self.subTest():
				self.assertIsInstance(data[key], key_type, msg=f"{key}, {key_type}, {type(data[key])}")
				
				
		for key, expected_bool_value in self.KEY_TO_BOOL.items():
			with self.subTest():
				self.assertTrue(bool(len(data[key])) == expected_bool_value, msg=f"{key}, {len(data[key])}, {expected_bool_value}")
				


if __name__ == '__main__':
	unittest.main()

