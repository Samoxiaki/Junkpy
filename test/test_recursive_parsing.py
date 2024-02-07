#!/usr/bin/env python3
from junkpy import JunkParser, JunkTypeProcessor
import unittest
from concurrent.futures import ThreadPoolExecutor


class RecursiveParsingTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.RECURSIVE_DATA_STRINGS = [
			"""
				[
					(recursive_parsed) \"0\",
					(recursive_parsed) \"0\",
					(recursive_parsed) \"0\",
				]
			""",
			"""
				[
					(recursive_parsed) \"1\",
					(recursive_parsed) \"1\",
					(recursive_parsed) \"1\",
				]
			""",
		]
		cls.NUM_THREADS = 4
		cls.ITERATIONS = 64

		class RecursiveParser(JunkTypeProcessor):
			CLASS = object
			KEYWORD = "recursive_parsed"
			
			def load(self, value, **kwargs):
				return self.parser.loads(str(value))
			

		cls.PARSER = JunkParser([
			RecursiveParser,
		])
	

	def parse_and_check(self, data, expected_result):
		result = self.PARSER.loads(data)
		self.assertListEqual(result, expected_result)


	def test_recursive_parsing(self):
		futures = []
		with ThreadPoolExecutor(self.NUM_THREADS) as executor:
			for _ in range(self.ITERATIONS):
				futures.append(executor.submit(self.parse_and_check, self.RECURSIVE_DATA_STRINGS[0], [0]*3))
				futures.append(executor.submit(self.parse_and_check, self.RECURSIVE_DATA_STRINGS[1], [1]*3))


		for future in futures:
			future.result()



if __name__ == '__main__':
	unittest.main()

