#!/usr/bin/env python3
from junkpy import JunkParser
from re import Pattern
from pathlib import Path
from decimal import Decimal
from datetime import datetime, date, time, timedelta
import unittest



class BuiltinTypesTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.PARSER = JunkParser()
		cls.FILE_PATH = Path(__file__).parent / "test_files/test_file_builtin_forced_types.junk"
		cls.KEY_TYPE_PAIRS = {
			"string": str,
			"regex": Pattern,
			"env": str,
			"path": Path,
			"int": int,
			"bin": int,
			"octal": int,
			"hex": int,
			"complex": complex,
			"float": float,
			"decimal": Decimal,
			"bool": bool,
			"set": set,
			"timestamp": datetime,
			"timedelta": timedelta,
			"time": time,
			"date": date,
			"datetime": datetime,
			"chained": str
		}
		
		
	def test_builtin_forced_types(self):
		data = self.PARSER.load_file(self.FILE_PATH)
		
		for key, key_type in self.KEY_TYPE_PAIRS.items():
			with self.subTest():
				self.assertIsInstance(data[key], key_type, msg=f"{key}, {key_type}, {type(data[key])}")
				


if __name__ == '__main__':
	unittest.main()

