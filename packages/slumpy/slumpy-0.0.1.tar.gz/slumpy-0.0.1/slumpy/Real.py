from .general import *

class Real ():
	
	def __init__ (self, entry : float = 0.0) -> None:

		self._value : float = entry
		self._default_value : float = self._value

	def set_to (self, entry : float = None) -> None:

		self._value = entry if (entry != None) else self._default_value

	def value (self) -> float:

		return (self._value)

	def plus (self, entry : float = 0.0) -> float:

		return (self._value + entry)

	def minus (self, entry : float = 0.0) -> float:

		return (self._value - entry)

	def multiplied_by (self, entry : float = 1.0) -> float:

		return (self._value * entry)

	def divided_by (self, entry : float = 1.0) -> float:

		return (self._value / entry)
	
	def module_of (self, entry : float = 1.0) -> float:

		return (self._value % entry)

	def power_of (self, entry : float = 1.0) -> float:

		return (self._value ** entry)

	def set_plus (self, entry : float = 0.0) -> None:

		self._value += entry

	def set_minus (self, entry : float = 0.0) -> None:

		self._value -= entry

	def set_multiplied_by (self, entry : float = 1.0) -> None:

		self._value *= entry

	def set_divided_by (self, entry : float = 1.0) -> None:

		self._value /= entry
	
	def set_module_of (self, entry : float = 1.0) -> None:

		self._value %= entry
	
	def set_power_of (self, entry : float = 1.0) -> None:

		self._value **= entry

	def is_equal_to (self, entry : Union [float, None] = None) -> bool:

		return (self._value == entry) if (entry != None) else (self._value == self._default_value)

	def is_not_equal_to (self, entry : Union [float, None] = None) -> bool:

		return (self._value != entry) if (entry != None) else (self._value != self._default_value)

	def is_more_than (self, entry : Union [float, None] = None) -> bool:

		return (self._value > entry) if (entry != None) else (self._value > self._default_value)

	def is_less_than (self, entry : Union [float, None] = None) -> bool:

		return (self._value < entry) if (entry != None) else (self._value < self._default_value)

	def is_more_or_equal_than (self, entry : Union [float, None] = None) -> bool:

		return (self._value >= entry) if (entry != None) else (self._value >= self._default_value)

	def is_less_or_equal_than (self, entry : float = None) -> bool:

		return (self._value <= entry) if (entry != None) else (self._value <= self._default_value)

class Ext_Real (Real):

	def __repr__ (self) -> str:

		return (f"Real : {self._value}")

	def __add__ (self, entry : float = 0.0) -> float:

		return (self._value + entry) if (type (entry) == float) else (self._value + entry._value)
	
	def __sub__ (self, entry : float = 0.0) -> float:

		return (self._value - entry) if (type (entry) == float) else (self._value - entry._value)

	def __mul__ (self, entry : float = 1.0) -> float:

		return (self._value * entry) if (type (entry) == float) else (self._value * entry._value)

	def __div__ (self, entry : float = 1.0) -> float:

		return (self._value / entry) if (type (entry) == float) else (self._value / entry._value)

	def __mod__ (self, entry : float = 1.0) -> float:

		return (self._value % entry) if (type (entry) == float) else (self._value % entry._value)

	def __pow__ (self, entry : float = 1.0) -> float:

		return (self._value ** entry) if (type (entry) == float) else (self._value ** entry._value)
	
	def __iadd__ (self, entry : float = 0.0) -> float:

		self._value += entry

	def __isub__ (self, entry : float = 0.0) -> float:

		self._value -= entry

	def __imul__ (self, entry : float = 1.0) -> float:

		self._value *= entry

	def __idiv__ (self, entry : float = 1.0) -> float:

		self._value /= entry

	def __imod__ (self, entry : float = 1.0) -> float:

		self._value %= entry

	def __ipow__ (self, entry : float = 1.0) -> float:

		self._value **= entry