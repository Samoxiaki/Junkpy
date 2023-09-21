#!/usr/bin/env python3
from junkpy import Junkpy, JunkpyTypeProcessor
from pathlib import Path
import unittest
from concurrent.futures import ThreadPoolExecutor


class ThreadingTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		
		cls.FILE_PATH_1 = Path(__file__).parent / "test_files/test_file_threads1.junk"
		cls.FILE_PATH_2 = Path(__file__).parent / "test_files/test_file_threads2.junk"
		cls.NUM_THREADS = 4
		cls.ITERATIONS = 64

		class ThreadChecker1(JunkpyTypeProcessor):
			CLASS = int
			KEYWORD = "thread_checker1"
			
			def load(self, value, file_path, **kwargs):
				if(file_path != cls.FILE_PATH_1):
					raise Exception("Wrong file.")

				return self.CLASS(value)
			

		class ThreadChecker2(JunkpyTypeProcessor):
			CLASS = int
			KEYWORD = "thread_checker2"
			
			def load(self, value, file_path, **kwargs):
				if(file_path != cls.FILE_PATH_2):
					raise Exception("Wrong file.")

				return self.CLASS(value)	


		cls.PARSER = Junkpy([
			ThreadChecker1,
			ThreadChecker2
		])
	

	def test_load_threading(self):
		futures = []
		with ThreadPoolExecutor(self.NUM_THREADS) as executor:
			for _ in range(self.ITERATIONS):
				futures.append(executor.submit(self.PARSER.load_file, self.FILE_PATH_1))
				futures.append(executor.submit(self.PARSER.load_file, self.FILE_PATH_2))


		for future in futures:
			self.assertIsInstance(future.result(), list)



if __name__ == '__main__':
	unittest.main()

