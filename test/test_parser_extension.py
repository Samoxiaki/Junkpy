#!/usr/bin/env python3
from junkpy import JunkMetadata, JunkParser, JunkTypeProcessor
from pathlib import Path
import unittest


class ParserExtensionTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.FILE_PATH = Path(__file__).parent / "test_files/test_file_parser_extensions.junk"
	

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



if __name__ == '__main__':
	unittest.main()

