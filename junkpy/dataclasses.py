from decimal import Decimal
from datetime import datetime, timedelta, date, time
from path import Path
from re import Pattern
import os
import re



class JunkDataClass:
	CLASS = None
	KEYWORD = None
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value)



class JunkBaseDataClassMeta(type):
	BASE_DATA_CLASSES = []
	
	@classmethod
	def __new__(metacls, cls, name, bases, dct):
		data_class = super().__new__(cls, name, bases, dct)
		metacls.BASE_DATA_CLASSES.append(data_class)
		return data_class



class JunkBaseDataClass(JunkDataClass, metaclass=JunkBaseDataClassMeta):
	pass
	


# Numeric
class JunkBoolDataClass(JunkBaseDataClass):
	CLASS = bool
	KEYWORD = "bool"
		
		
	
class JunkIntegerDataClass(JunkBaseDataClass):
	CLASS = int
	KEYWORD = "int"
	
	
	
class JunkHexDataClass(JunkBaseDataClass):
	CLASS = int
	KEYWORD = "hex"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 16)
		
		
		
class JunkOctalDataClass(JunkBaseDataClass):
	CLASS = int
	KEYWORD = "octal"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 8)
		
		
		
class JunkBinaryDataClass(JunkBaseDataClass):
	CLASS = int
	KEYWORD = "bin"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(value, 2)
	
	
	
class JunkComplexDataClass(JunkBaseDataClass):
	CLASS = complex
	KEYWORD = "complex"
	
	
	
class JunkFloatDataClass(JunkBaseDataClass):
	CLASS = float
	KEYWORD = "float"
	


class JunkDecimalDataClass(JunkBaseDataClass):
	CLASS = Decimal
	KEYWORD = "decimal"
	
	

# List
class JunkSetDataClass(JunkBaseDataClass):
	CLASS = set
	KEYWORD = "set"
	


# String
class JunkStringDataClass(JunkBaseDataClass):
	CLASS = str
	KEYWORD = "string"
	
	
	
class JunkRegexDataClass(JunkBaseDataClass):
	CLASS = Pattern
	KEYWORD = "regex"
	
	@classmethod
	def load(cls, value, **kwargs):
		return re.compile(str(value))

	

# Date/Time
class JunkTimeDeltaDataClass(JunkBaseDataClass):
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
		
		
		
class JunkTimestampDataClass(JunkBaseDataClass):
	CLASS = datetime
	KEYWORD = "timestamp"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS.fromtimestamp(float(value))
		
		

class JunkDatetimeDataClassParent(JunkBaseDataClass):
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
			
			
			
class JunkTimeDataClass(JunkDatetimeDataClassParent):
	CLASS = time
	KEYWORD = "time"
	
	
	
class JunkDateDataClass(JunkDatetimeDataClassParent):
	CLASS = date
	KEYWORD = "date"
	
	
	
class JunkDateTimeDataClass(JunkDatetimeDataClassParent):
	CLASS = datetime
	KEYWORD = "datetime"



# System
class JunkEnvVarDataClass(JunkBaseDataClass):
	CLASS = str
	KEYWORD = "env"
	
	@classmethod
	def load(cls, value, **kwargs):
		return os.path.expandvars(cls.CLASS(value))		
		
		
		
class JunkPathDataClass(JunkBaseDataClass):
	CLASS = Path
	KEYWORD = "path"
	
	@classmethod
	def load(cls, value, **kwargs):
		return cls.CLASS(os.path.expandvars(str(value)))


