from typing import List, Optional, Type, IO
from lark import Lark, Transformer
from .type_processors import JunkpyTypeProcessor, JunkpyBaseTypeProcessorMeta
import threading
from pathlib import Path



class JunkpyTransformer(Transformer):
	def __init__(self, parser_instance, type_processors: list = None):
		super().__init__()
		
		self._parser_instance = parser_instance
		self._type_processors_keyword_dict = {}
		init_type_processors = JunkpyBaseTypeProcessorMeta.BASE_TYPE_PROCESSOR_CLASSES
		if(type_processors is not None):
			init_type_processors += type_processors if(isinstance(type_processors, list)) else [type_processors]
	
		for type_processor in init_type_processors:
			if(issubclass(type_processor, JunkpyTypeProcessor)):
				self._type_processors_keyword_dict[type_processor.KEYWORD] = type_processor()
				
			else:
				raise TypeError(f"Unsupported class type <{type_processor}>'")
				
				
	def typed_value(self, value):
		return self.typed_value_parser(value[0], {} if(len(value) == 2) else value[1], value[-1])
		
		
	def typed_null_value(self, value):
		return self.typed_value_parser(value[0], {} if(len(value) == 1) else value[1], None)
		
		
	def typed_value_parser(self, type_cls, type_kwargs, value):
		file_path = self._parser_instance._parsing_files.get(threading.current_thread().native_id, None)

		type_processor = self._type_processors_keyword_dict.get(type_cls, None)
		if(type_processor is None):
			raise ValueError(f"Unsupported type <{type_cls}>")
		
		loaded_value = type_processor.load(value, file_path, **type_kwargs)
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



class Junkpy:
	__JUNKPY_GRAMMAR = r"""
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
	

	def __init__(self, type_processors: Optional[List[Type[JunkpyTypeProcessor]]] = None):
		"""
		Initializes the Junkpy parser.

		Args:
			data_classes (Optional[List[JunkpyTypeProcessor]]): List of type processors to be used for typed value conversion.
		"""
		self._parsing_files = {}
		self.__parser = Lark(self.__JUNKPY_GRAMMAR, start='value', parser='lalr', transformer=JunkpyTransformer(self, type_processors))

	
	def loads(self, string: str) -> object:
		"""
		Parses a Junkpy string and returns the corresponding Python object.

		Args:
			string (str): The Junkpy string to parse.

		Returns:
			object: The parsed Python object.
		"""
		return self.__parser.parse(string)
		
	
	def load(self, fp: IO) -> object:
		"""
		Parses a Junkpy file-like object and returns the corresponding Python object.

		Args:
			fp (file-like): The file-like object containing the Junkpy data.

		Returns:
			object: The parsed Python object.
		"""
		
		with fp as opened_fp:
			return self.loads(opened_fp.read())
		
		
	def load_file(self, file_path: str) -> object:
		"""
		Parses a Junkpy file and returns the corresponding Python object.

		Args:
			file_path (str): The path to the Junkpy file.

		Returns:
			object: The parsed Python object.
		"""

		thread_id = threading.current_thread().native_id
		try:
			self._parsing_files[thread_id] = Path(file_path)
			return_data = self.load(open(file_path, "rt"))
		
		finally:
			del self._parsing_files[thread_id]

		return return_data

