from decimal import Decimal
from datetime import datetime, timedelta, date, time
from path import Path
from re import Pattern
import os
import re



class JunkpyDataClass:
	CLASS = None
	KEYWORD = None
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value)



class JunkpyBaseDataClassMeta(type):
	BASE_DATA_CLASSES = []
	
	@classmethod
	def __new__(metacls, cls, name, bases, dct):
		data_class = super().__new__(cls, name, bases, dct)
		metacls.BASE_DATA_CLASSES.append(data_class)
		return data_class



class JunkpyBaseDataClass(JunkpyDataClass, metaclass=JunkpyBaseDataClassMeta):
	pass
	


# Numeric
class JunkpyBoolDataClass(JunkpyBaseDataClass):
	CLASS = bool
	KEYWORD = "bool"
		
		
	
class JunkpyIntegerDataClass(JunkpyBaseDataClass):
	CLASS = int
	KEYWORD = "int"
	
	
	
class JunkpyHexDataClass(JunkpyBaseDataClass):
	CLASS = int
	KEYWORD = "hex"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 16)
		
		
		
class JunkpyOctalDataClass(JunkpyBaseDataClass):
	CLASS = int
	KEYWORD = "octal"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 8)
		
		
		
class JunkpyBinaryDataClass(JunkpyBaseDataClass):
	CLASS = int
	KEYWORD = "bin"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 2)
	
	
	
class JunkpyComplexDataClass(JunkpyBaseDataClass):
	CLASS = complex
	KEYWORD = "complex"
	
	
	
class JunkpyFloatDataClass(JunkpyBaseDataClass):
	CLASS = float
	KEYWORD = "float"
	


class JunkpyDecimalDataClass(JunkpyBaseDataClass):
	CLASS = Decimal
	KEYWORD = "decimal"
	
	

# List
class JunkpySetDataClass(JunkpyBaseDataClass):
	CLASS = set
	KEYWORD = "set"
	


# String
class JunkpyStringDataClass(JunkpyBaseDataClass):
	CLASS = str
	KEYWORD = "string"
	
	
	
class JunkpyRegexDataClass(JunkpyBaseDataClass):
	CLASS = Pattern
	KEYWORD = "regex"
	
	@classmethod
	def load(cls, value, **kwargs):
		return re.compile(str(value))

	

# Date/Time
class JunkpyTimeDeltaDataClass(JunkpyBaseDataClass):
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
		
		
		
class JunkpyTimestampDataClass(JunkpyBaseDataClass):
	CLASS = datetime
	KEYWORD = "timestamp"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS.fromtimestamp(float(value))
		
		

class JunkpyDatetimeDataClassParent(JunkpyBaseDataClass):
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
			
			
			
class JunkpyTimeDataClass(JunkpyDatetimeDataClassParent):
	CLASS = time
	KEYWORD = "time"
	
	
	
class JunkpyDateDataClass(JunkpyDatetimeDataClassParent):
	CLASS = date
	KEYWORD = "date"
	
	
	
class JunkpyDateTimeDataClass(JunkpyDatetimeDataClassParent):
	CLASS = datetime
	KEYWORD = "datetime"



# System
class JunkpyEnvVarDataClass(JunkpyBaseDataClass):
	CLASS = str
	KEYWORD = "env"
	
	@classmethod
	def load(cls, value, **kwargs):
		return os.path.expandvars(cls.CLASS(value))		
		
		
		
class JunkpyPathDataClass(JunkpyBaseDataClass):
	CLASS = Path
	KEYWORD = "path"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(os.path.expandvars(str(value)))


