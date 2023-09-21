from decimal import Decimal
from datetime import datetime, timedelta, date, time
from pathlib import Path
from re import Pattern
import os
import re



class JunkpyTypeProcessor:
	"""
	Represents a type processor used in Junkpy for parsing and loading data.

	Attributes:
		CLASS (type): The Python object type to be returned by the type processor.
		KEYWORD (str): The keyword used to identify this type processor in Junkpy syntax.

	Methods:
		load(cls, value, **kwargs): A class method that loads the given value and returns a python object of the type defined by CLASS attribute.

	"""
	CLASS = None
	KEYWORD = None
	
	@classmethod
	def load(cls, value: object, **kwargs) -> object:
		"""
		Loads the given value and returns an instance of a python object.

		Args:
			value: The parsed value to be modified or loaded.
			**kwargs: Modifiers included when forcing the type in a Junkpy file.

		Returns:
			object: An instance of the modified or loaded value.

		"""
		return cls.CLASS(value)



class JunkpyBaseTypeProcessorMeta(type):
	BASE_TYPE_PROCESSOR_CLASSES = []
	
	@classmethod
	def __new__(metacls, cls, name, bases, dct):
		type_processor = super().__new__(cls, name, bases, dct)
		metacls.BASE_TYPE_PROCESSOR_CLASSES.append(type_processor)
		return type_processor



class JunkpyBaseTypeProcessor(JunkpyTypeProcessor, metaclass=JunkpyBaseTypeProcessorMeta):
	pass
	


# Numeric
class JunkpyBoolTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = bool
	KEYWORD = "bool"
		
		
	
class JunkpyIntegerTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = int
	KEYWORD = "int"
	
	
	
class JunkpyHexTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = int
	KEYWORD = "hex"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 16)
		
		
		
class JunkpyOctalTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = int
	KEYWORD = "octal"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 8)
		
		
		
class JunkpyBinaryTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = int
	KEYWORD = "bin"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 2)
	
	
	
class JunkpyComplexTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = complex
	KEYWORD = "complex"
	
	
	
class JunkpyFloatTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = float
	KEYWORD = "float"
	


class JunkpyDecimalTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = Decimal
	KEYWORD = "decimal"
	
	

# List
class JunkpySetTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = set
	KEYWORD = "set"
	


# String
class JunkpyStringTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = str
	KEYWORD = "string"
	
	
	
class JunkpyRegexTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = Pattern
	KEYWORD = "regex"
	
	@classmethod
	def load(cls, value, **kwargs):
		return re.compile(str(value))

	

# Date/Time
class JunkpyTimeDeltaTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = timedelta
	KEYWORD = "timedelta"
	
	@classmethod
	def load(cls, value, **kwargs):
		if(isinstance(value, list)):
			return cls.CLASS(*value)
			
		elif(isinstance(value, dict)):
			return cls.CLASS(**value)
			
		else:
			return cls.CLASS(seconds=float(value))
		
		
		
class JunkpyTimestampTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = datetime
	KEYWORD = "timestamp"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS.fromtimestamp(float(value))
		
		

class JunkpyDatetimeTypeProcessorParent(JunkpyBaseTypeProcessor):
	@classmethod
	def load(cls, value, **kwargs):
		if(isinstance(value, list)):
			return cls.CLASS(*value)
			
		elif(isinstance(value, dict)):
			return cls.CLASS(**value)
			
		elif(isinstance(value, str)):
			return cls.CLASS.fromisoformat(value)
			
		else:
			raise ValueError(f"Unsupported value for type <{cls.KEYWORD}>: {value}")
			
			
			
class JunkpyTimeTypeProcessor(JunkpyDatetimeTypeProcessorParent):
	CLASS = time
	KEYWORD = "time"
	
	
	
class JunkpyDateTypeProcessor(JunkpyDatetimeTypeProcessorParent):
	CLASS = date
	KEYWORD = "date"
	
	
	
class JunkpyDateTimeTypeProcessor(JunkpyDatetimeTypeProcessorParent):
	CLASS = datetime
	KEYWORD = "datetime"



# System
class JunkpyEnvVarTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = str
	KEYWORD = "env"
	
	@classmethod
	def load(cls, value, **kwargs):
		return os.path.expandvars(cls.CLASS(value))		
		
		
		
class JunkpyPathTypeProcessor(JunkpyBaseTypeProcessor):
	CLASS = Path
	KEYWORD = "path"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(os.path.expandvars(str(value)))


