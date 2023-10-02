from typing import List, Optional, Type, IO
from lark import Lark, Transformer
from .type_processors import JunkTypeProcessor, JunkBaseTypeProcessorMeta
import threading
from pathlib import Path
from dataclasses import dataclass


@dataclass
class JunkMetadata:
	file_path : Path


class JunkParserThreadingLocalStorage(threading.local):
	def __init__(self):
		self.storage = []

	def push(self, data):
		self.storage.append(data)

	def get(self):
		return self.storage[-1]
	
	def pop(self):
		return self.storage.pop()
	


class JunkParser:
	__JUNK_GRAMMAR = r"""
		?value: dict
			| empty_dict
			| list
			| empty_list
			| string
			| integer_n
			| float_n
			| true
			| false
			| null
		
		typed_value: "(" ((string | var_name) | (string | var_name) type_kwargs) ")" (value | typed_value | typed_null_value)
		typed_null_value: "(" ((string | var_name) | (string | var_name) type_kwargs) ")" 
		pair : (string | var_name) ":" (value | typed_value | typed_null_value)
		null_pair : (string | var_name) ":" 
		
		dict : "{" (pair|null_pair) ("," (pair|null_pair))* ("}" | "," "}")
		empty_dict : "{" "}"
		
		list : "[" (value | typed_value | typed_null_value) ("," (value | typed_value | typed_null_value))* ("]" | "," "]")
		empty_list : "[" "]"
		
		integer_n: SIGNED_INT
		float_n: SIGNED_FLOAT
		true: "true"
		false: "false"
		null: "null"
		string : ESCAPED_STRING
		var_name : EXTENDED_CNAME
		type_option : (string | var_name) "=" (value | typed_value | typed_null_value)
		type_kwargs : ("," type_option)* 
		
		EXTENDED_CNAME : ("_"|"-"|LETTER) ("_"|"-"|LETTER|DIGIT)*
		SH_COMMENT: /#[^\n]*/
		
		%import common.ESCAPED_STRING
		%import common.LETTER
		%import common.DIGIT
		%import common.SIGNED_INT
		%import common.SIGNED_FLOAT
		%import common.WS
		%ignore WS
		%ignore SH_COMMENT
	"""
	

	def __init__(self, type_processors: Optional[List[Type[JunkTypeProcessor]]] = None):
		"""
		Initializes the Junk parser.

		Args:
			type_processors (Optional[List[JunkTypeProcessor]]): List of type processors to be used for typed value conversion.
		"""

		self._local_storage = JunkParserThreadingLocalStorage()

		self._type_processors_keyword_dict = {}
		init_type_processors = JunkBaseTypeProcessorMeta.BASE_TYPE_PROCESSOR_CLASSES

		if(type_processors is not None):
			init_type_processors += type_processors if(isinstance(type_processors, list)) else [type_processors]
	
		for type_processor in init_type_processors:
			if(issubclass(type_processor, JunkTypeProcessor)):
				self._type_processors_keyword_dict[type_processor.KEYWORD] = type_processor(self)
				
			else:
				raise TypeError(f"Unsupported class type <{type_processor}>'")
			

		self.__parser = Lark(self.__JUNK_GRAMMAR, start='value', parser='lalr', transformer=JunkTransformer(self))


	def loads(self, string: str) -> object:
		"""
		Parses a Junk string and returns the corresponding Python object.

		Args:
			string (str): The Junk string to parse.

		Returns:
			object: The parsed Python object.
		"""
		try:
			self._local_storage.push(
				JunkMetadata(
					file_path = None
				)
			)
			
			self.before_parsing(self._local_storage.get())

			return_data = self.__parser.parse(string)
			
			return_data =self.after_parsing(self._local_storage.get(), return_data)
		
		finally:
			self._local_storage.pop()

		return return_data 
		
	
	def load(self, fp: IO) -> object:
		"""
		Parses a Junk file-like object and returns the corresponding Python object.

		Args:
			fp (file-like): The file-like object containing the Junk data.

		Returns:
			object: The parsed Python object.
		"""
		try:
			self._local_storage.push(
				JunkMetadata(
					file_path = Path(fp.name)
				)
			)
			
			self.before_parsing(self._local_storage.get())

			with fp as opened_fp:
				return_data = self.__parser.parse(opened_fp.read())

			return_data = self.after_parsing(self._local_storage.get(), return_data)
		
		finally:
			self._local_storage.pop()

		return return_data
		
		
	def load_file(self, file_path: str) -> object:
		"""
		Parses a Junk file and returns the corresponding Python object.

		Args:
			file_path (str): The path to the Junk file.

		Returns:
			object: The parsed Python object.
		"""
		try:
			self._local_storage.push(
				JunkMetadata(
					file_path = Path(file_path)
				)
			)
			
			self.before_parsing(self._local_storage.get())

			with open(file_path, "rt") as opened_fp:
				return_data = self.__parser.parse(opened_fp.read())
		
			return_data = self.after_parsing(self._local_storage.get(), return_data)

		finally:
			self._local_storage.pop()

		return return_data


	def before_parsing(self, metadata: JunkMetadata):
		pass


	def after_parsing(self, metadata: JunkMetadata, parsed_data: object) -> object:
		return parsed_data



class JunkTransformer(Transformer):
	def __init__(self, parser_instance):
		super().__init__()
		self._parser_instance = parser_instance
	

	def typed_value(self, value):
		return self.typed_value_parser(value[0], {} if(len(value) == 2) else value[1], value[-1])
		
		
	def typed_null_value(self, value):
		return self.typed_value_parser(value[0], {} if(len(value) == 1) else value[1], None)
		
		
	def typed_value_parser(self, type_cls, type_kwargs, value):
		type_processor = self._parser_instance._type_processors_keyword_dict.get(type_cls, None)
		if(type_processor is None):
			raise ValueError(f"Unsupported type <{type_cls}>")
		
		loaded_value = type_processor.load(value, **type_kwargs)
		if(not isinstance(loaded_value, type_processor.CLASS)):
			raise TypeError(f"Unexpected output type for type processor ({type_cls}). Expected {type_processor.CLASS}, got {type(loaded_value)}")
			
		return loaded_value
	
	
	list = list
	empty_list = lambda self, value: list()
	dict = dict
	empty_dict = lambda self, value: dict()
	pair = tuple
	type_option = tuple
	type_kwargs = dict
	null_pair = lambda self, value: (value[0], None)		
	var_name = lambda self, value: str(value[0])
	string = lambda self, value: value[0][1:-1]
	float_n = lambda self, value: float(value[0])
	integer_n = lambda self, value: int(value[0])
	null = lambda self, _: None
	true = lambda self, _: True
	false = lambda self, _: False
