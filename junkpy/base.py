from lark import Lark, Transformer
from .dataclasses import JunkpyDataClass, JunkpyBaseDataClassMeta



class JunkpyTransformer(Transformer):
	def __init__(self, data_classes:list=None):
		super().__init__()
		
		self._data_class_keyword_dict = {}
		init_data_classes = JunkpyBaseDataClassMeta.BASE_DATA_CLASSES
		if(data_classes is not None):
			init_data_classes += data_classes if(isinstance(data_classes, list)) else [data_classes]
	
		for data_class in init_data_classes:
			if(issubclass(data_class, JunkpyDataClass)):
				self._data_class_keyword_dict[data_class.KEYWORD] = data_class
				
			else:
				raise TypeError(f"Unsupported class type <{data_class}>'")
				
				
	def typed_value(self, value):
		return self.typed_value_parser(value[0], {} if(len(value) == 2) else value[1], value[-1])
		
		
	def typed_null_value(self, value):
		return self.typed_value_parser(value[0], {} if(len(value) == 1) else value[1], None)
		
		
	def typed_value_parser(self, type_cls, type_kwargs, value):
		data_class = self._data_class_keyword_dict.get(type_cls, None)
		if(data_class is None):
			raise ValueError(f"Unsupported type <{type_cls}>")
		
		return data_class.load(value, **type_kwargs)
	

	list = list
	dict = dict
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
			  | list
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
		
		dict : "{" [(pair|null_pair) ("," (pair|null_pair))*] ("}" | "," "}")
		list : "[" [(value | typed_value | typed_null_value) ("," (value | typed_value | typed_null_value))*] ("]" | "," "]")
		
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
	

	def __init__(self, data_classes:list=None):
		self.__parser = Lark(self.__JUNKPY_GRAMMAR, start='value', parser='lalr', transformer=JunkpyTransformer(data_classes))

	
	def loads(self, string):
		return self.__parser.parse(string)
		
	
	def load(self, fp):
		with fp as opened_fp:
			return self.loads(opened_fp.read())	
		
		
	def load_file(self, file_path):
		return self.load(open(file_path, "rt"))


