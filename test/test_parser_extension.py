#!/usr/bin/env python3
from junkpy import JunkMetadata, JunkParser, JunkTypeProcessor
from pathlib import Path
import unittest


class ParserExtensionTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.FILE_PATH = Path(__file__).parent / "test_files/test_file_parser_extensions.junk"
		cls.FILE_PATH_RECURSIVE = Path(__file__).parent / "test_files/test_file_parser_extensions_recursive.junk"
		cls.FILE_PATH_RECURSIVE_ALT = Path(__file__).parent / "test_files/test_file_autodetected_types.junk"
	

	def test_parser_extensions(self):
		class AcummulatedValue(JunkTypeProcessor):
			CLASS = int
			KEYWORD = "accumulated"
			
			def load(self, value, **kwargs):
				ret = self.CLASS(value)
				self.metadata.total += ret

				return ret	


		class ExtendedParser(JunkParser):
			def before_parsing(self, metadata: JunkMetadata):
				metadata.total = 0


			def after_parsing(self, metadata: JunkMetadata, parsed_data: object):
				new_data = {
					"data" : parsed_data,
					"total_accumulated" : metadata.total
				}
				return new_data
				
		junk_parser = ExtendedParser([AcummulatedValue])
		parsed_data = junk_parser.load_file(self.FILE_PATH)

		expected = sum(parsed_data["data"])
		self.assertEqual(expected, parsed_data["total_accumulated"])



	def test_parser_extensions_recursive_parsing(self):
		target_file = self.FILE_PATH_RECURSIVE
		target_file_2 = self.FILE_PATH_RECURSIVE_ALT

		class RecursiveParser(JunkParser):
			def before_parsing(self, metadata: JunkMetadata):
				if(metadata.file_path == target_file):
					metadata.parsed_file_before_data = self.load_file(target_file_2)


			def after_parsing(self, metadata: JunkMetadata, parsed_data: object):
				if(metadata.file_path == target_file):
					metadata.parsed_file_after_data = self.load_file(target_file_2)

					new_data = {
						"before": metadata.parsed_file_before_data,
						"after": metadata.parsed_file_after_data,
					}

					return new_data
				
				else: 
					return parsed_data

		junk_parser = RecursiveParser()
		parsed_data = junk_parser.load_file(target_file)

		self.assertEqual(parsed_data["before"], parsed_data["after"])



if __name__ == '__main__':
	unittest.main()

