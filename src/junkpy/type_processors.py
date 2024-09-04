from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional, Type
if TYPE_CHECKING:
	from .base import JunkMetadata, JunkParser

from decimal import Decimal
from datetime import datetime, timedelta, date, time
from pathlib import Path
from re import Pattern
import os
import re



class JunkTypeProcessor:
	"""
	Represents a type processor used in Junkpy for parsing and loading data of a Junk file.

	Attributes:
		CLASS (type): The Python object type to be returned by the type processor.
		KEYWORD (str): The keyword used to identify this type processor in Junk syntax.

	Methods:
		load(self, value, file_path, **kwargs): A method that processes the parsed value and returns a python object of the type defined by CLASS attribute.

	"""
	CLASS: type = None
	KEYWORD: str = None 
	

	def __init__(self, parser):
		self.__parser = parser


	def load(self, value: Any, **kwargs) -> Any:
		"""
		Loads the given value and returns an instance of a python object.

		Args:
			value: The parsed value to be modified or loaded.
			**kwargs: Modifiers included when forcing the type in a Junk file.

		Returns:
			object: An instance of the modified or loaded value.

		"""
		return self.CLASS(value)


	@property
	def metadata(self) -> JunkMetadata:
		return self.__parser._local_storage.get()
	

	@property
	def parser(self) -> JunkParser:
		return self.__parser



class JunkBaseTypeProcessorMeta(type):
	BASE_TYPE_PROCESSOR_CLASSES = []
	
	@classmethod
	def __new__(metacls, cls, name, bases, dct):
		type_processor = super().__new__(cls, name, bases, dct)
		metacls.BASE_TYPE_PROCESSOR_CLASSES.append(type_processor)
		return type_processor



class JunkBaseTypeProcessor(JunkTypeProcessor, metaclass=JunkBaseTypeProcessorMeta):
	pass
	


# Numeric
class JunkBoolTypeProcessor(JunkBaseTypeProcessor):
	CLASS = bool
	KEYWORD = "bool"
		
		
	
class JunkIntegerTypeProcessor(JunkBaseTypeProcessor):
	CLASS = int
	KEYWORD = "int"
	
	
	
class JunkHexTypeProcessor(JunkBaseTypeProcessor):
	CLASS = int
	KEYWORD = "hex"
	
	
	def load(self, value, **kwargs):
		return self.CLASS(value, 16)
		
		
		
class JunkOctalTypeProcessor(JunkBaseTypeProcessor):
	CLASS = int
	KEYWORD = "octal"
	
	
	def load(self, value, **kwargs):
		return self.CLASS(value, 8)
		
		
		
class JunkBinaryTypeProcessor(JunkBaseTypeProcessor):
	CLASS = int
	KEYWORD = "bin"
	
	
	def load(self, value, **kwargs):
		return self.CLASS(value, 2)
	
	
	
class JunkComplexTypeProcessor(JunkBaseTypeProcessor):
	CLASS = complex
	KEYWORD = "complex"
	
	
	
class JunkFloatTypeProcessor(JunkBaseTypeProcessor):
	CLASS = float
	KEYWORD = "float"
	


class JunkDecimalTypeProcessor(JunkBaseTypeProcessor):
	CLASS = Decimal
	KEYWORD = "decimal"
	
	

# List
class JunkSetTypeProcessor(JunkBaseTypeProcessor):
	CLASS = set
	KEYWORD = "set"
	


# String
class JunkStringTypeProcessor(JunkBaseTypeProcessor):
	CLASS = str
	KEYWORD = "string"
	
	
	
class JunkRegexTypeProcessor(JunkBaseTypeProcessor):
	CLASS = Pattern
	KEYWORD = "regex"
	
	
	def load(self, value, **kwargs):
		return re.compile(str(value))

	

# Date/Time
class JunkTimeDeltaTypeProcessor(JunkBaseTypeProcessor):
	CLASS = timedelta
	KEYWORD = "timedelta"
	
	
	def load(self, value, **kwargs):
		if(isinstance(value, list)):
			return self.CLASS(*value)
			
		elif(isinstance(value, dict)):
			return self.CLASS(**value)
			
		else:
			return self.CLASS(seconds=float(value))
		
		
		
class JunkTimestampTypeProcessor(JunkBaseTypeProcessor):
	CLASS = datetime
	KEYWORD = "timestamp"
	
	
	def load(self, value, **kwargs):
		return self.CLASS.fromtimestamp(float(value))
		
		

class JunkDatetimeTypeProcessorParent(JunkBaseTypeProcessor):
	
	def load(self, value, **kwargs):
		if(isinstance(value, list)):
			return self.CLASS(*value)
			
		elif(isinstance(value, dict)):
			return self.CLASS(**value)
			
		elif(isinstance(value, str)):
			return self.CLASS.fromisoformat(value)
			
		else:
			raise ValueError(f"Unsupported value for type <{self.KEYWORD}>: {value}")
			
			
			
class JunkTimeTypeProcessor(JunkDatetimeTypeProcessorParent):
	CLASS = time
	KEYWORD = "time"
	
	
	
class JunkDateTypeProcessor(JunkDatetimeTypeProcessorParent):
	CLASS = date
	KEYWORD = "date"
	
	
	
class JunkDateTimeTypeProcessor(JunkDatetimeTypeProcessorParent):
	CLASS = datetime
	KEYWORD = "datetime"



# System
class JunkEnvVarTypeProcessor(JunkBaseTypeProcessor):
	CLASS = str
	KEYWORD = "env"
	
	
	def load(self, value, **kwargs):
		return os.path.expandvars(self.CLASS(value))		
		
		
		
class JunkPathTypeProcessor(JunkBaseTypeProcessor):
	CLASS = Path
	KEYWORD = "path"
	
	
	def load(self, value, **kwargs):
		return self.CLASS(os.path.expandvars(str(value)))


