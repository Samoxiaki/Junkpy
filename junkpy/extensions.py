from .type_processors import JunkTypeProcessor
from decimal import Decimal



class JunkBaseMagnitudeTypeProcessor(JunkTypeProcessor):
	CLASS = Decimal
	KEYWORD = None
	DEFAULT_UNIT = None
	UNITS = {}
	

	def load(self, value, **kwargs):
		input = kwargs.get("input")
		output = kwargs.get("output")
		input_ratio = self.UNITS.get((input if(input is not None) else self.DEFAULT_UNIT).lower(), self.UNITS[self.DEFAULT_UNIT])
		output_ratio = self.UNITS.get((output if(output is not None) else self.DEFAULT_UNIT).lower(), self.UNITS[self.DEFAULT_UNIT])
		
		return self.CLASS(value) * input_ratio / output_ratio
		
	
	
class JunkMassTypeProcessor(JunkBaseMagnitudeTypeProcessor):
	KEYWORD = "mass"
	DEFAULT_UNIT = "g"
	UNITS = {
		# Metric
		"ug": Decimal("0.000001"), # Microgram
		"µg": Decimal("0.000001"), # Microgram
		"mg": Decimal("0.001"), # Miligram
		"g": Decimal(1), # Gram
		"kg": Decimal(1000), # Kilogram
		"t": Decimal(1000000), # Ton
		
		# Imperial
		"oz": Decimal("28.349523125"), # Ounce
		"lb": Decimal("453.59237"), # Pound
		"st": Decimal("6350.29318"), # Stone
		"qr": Decimal("11339.80925"), # Quarter
	}
	
	
	
class JunkDistanceTypeProcessor(JunkBaseMagnitudeTypeProcessor):
	KEYWORD = "distance"
	DEFAULT_UNIT = "m"
	UNITS = {
		# Metric
		"pm": Decimal("0.000000000001"), # Picometer
		"nm": Decimal("0.000000001"), # Nanometer
		"um": Decimal("0.000001"), # Micrometer
		"µm": Decimal("0.000001"), # Micremeter
		"mm": Decimal("0.001"), # Millimeter
		"cm": Decimal("0.01"), # Centimeter
		"m": Decimal(1), # Meter
		"dam": Decimal(10), # Decameter
		"hm": Decimal(100), # Hectometer
		"km": Decimal(1000), # Kilometer
		
		# Imperial
		"mil": Decimal("0.0000254"), # Mil
		"in": Decimal("0.0254"), # Inch
		"ft": Decimal("0.3048"), # Foot
		"yd": Decimal("0.9144"), # Yard
		"mi": Decimal("1609.344"), # Mile
	}
	
	
	
class JunkVolumeTypeProcessor(JunkBaseMagnitudeTypeProcessor):
	KEYWORD = "volume"
	DEFAULT_UNIT = "l"
	UNITS = {
		# Metric
		"ml": Decimal("0.001"), # Milliliter
		"cl": Decimal("0.01"), # Centiliter
		"dl": Decimal("0.1"), # Deciliter
		"l": Decimal(1), # Liter
		"kl": Decimal(1000), # Kiloliter
		
		# Imperial
		"floz": Decimal("0.0295735296875"), # Fluid Ounce
		"pt": Decimal("0.473176473"), # Pint
		"qt": Decimal("0.946352946"), # Quart
		"gal": Decimal("3.785411784"), # Gallon
	}
	
	
	
class JunkSpeedTypeProcessor(JunkBaseMagnitudeTypeProcessor):
	KEYWORD = "speed"
	DEFAULT_UNIT = "m/s"
	UNITS = {
		# Metric
		"m/s": Decimal(1), # Meters per second
		"km/h": Decimal("0.2777777777777777777777777778"), # Kilometers per hour
		
		# Imperial
		"ft/s": Decimal("0.3048"), # Feet per second
		"mph": Decimal("0.447040972"), # Miles per hour
	}
	
	





