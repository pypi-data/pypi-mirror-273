from .general import *

class Bool ():
	
	def __init__ (self, entry : bool = False) -> None:

		self._value : bool = entry
		self._default_value : bool = self._value

	def set_to (self, entry : Union[bool, None] = None) -> None:

		self._value = entry if (entry != None) else self._default_value

	def value (self) -> bool:

		return (self._value)

	def opposite (self) -> bool:

		return (not self._value)
	
	def is_true (self, entry : Union[bool, None] = None) -> bool:

		return (self._value == entry) if (entry != None) else (self._value == self._default_value)

	def is_not_true (self, entry : Union[bool, None] = None) -> bool:

		return (self._value != entry) if (entry != None) else (self._value != self._default_value)

class Ext_Bool (Bool):

	def __repr__ (self) -> str:

		return (f"Bool : {self._value}")