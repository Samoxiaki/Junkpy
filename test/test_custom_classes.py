#!/usr/bin/env python3

from junkpy import JunkParser, JunkTypeProcessor
from pathlib import Path
import unittest



class CustomClassesTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		
		cls.FILE_PATH = Path(__file__).parent / "test_files/test_file_custom_classes.junk"
		
		class CustomTestClass1(JunkTypeProcessor):
			CLASS = int
			KEYWORD = "custom1"
			
			def load(self, value, **kwargs):
				return self.CLASS(value) * 3
		
		
		
		class CustomTestClass2(JunkTypeProcessor):
			CLASS = int
			KEYWORD = "custom2"
			
			def load(self, value, **kwargs):
				ret_v = self.CLASS(value) * 3
				
				min_value, max_value = kwargs.get("min"), kwargs.get("max")
				
				if(None not in [min_value, max_value]):
					min_value, max_value = (min_value, max_value) if(min_value <= max_value) else (max_value, min_value)
				
				if(min_value is not None):
					ret_v = max(ret_v, min_value)
					
				if(max_value is not None):
					ret_v = min(ret_v, max_value)
					
					
				return self.CLASS(ret_v)
		
		
		class CustomTestClass3(JunkTypeProcessor):
			CLASS = int
			KEYWORD = "custom3"
			
			def load(self, value, **kwargs):
				ret_v = 0 if(value is None) else self.CLASS(value)
				
				if("add" in kwargs):
					ret_v += kwargs["add"]
					
				if("sub" in kwargs):
					ret_v -= kwargs["sub"]
					
				if("mul" in kwargs):
					ret_v *= kwargs["mul"]
					
				if("div" in kwargs):
					ret_v /= kwargs["div"]
					
					
				return self.CLASS(ret_v)
		
		
		cls.PARSER = JunkParser([
			CustomTestClass1,
			CustomTestClass2,
			CustomTestClass3
		])
		
		cls.EXPECTED_VALUES = {
			"test1":  int(88)*3,
			"test2": 100,
			"test3": 120,
			"test4": 120,
			"test5": 150,
			"test6": 50,
			"test7": 120,
			"test8": 20,
			"test9": 5,
			"test10": 360,
			"test11": 200,
		}
		
		
	def test_custom_classes(self):
		data = self.PARSER.load_file(self.FILE_PATH)
		
		for key, expected_value in self.EXPECTED_VALUES.items():
			with self.subTest():
				self.assertEqual(data[key], expected_value, msg=f"{key}, {expected_value}, {data[key]}")


if __name__ == '__main__':
	unittest.main()

