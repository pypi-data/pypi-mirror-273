from .general import *

class Str ():

	def __init__ (self, entry : str = "") -> None:

		self._value : str = entry
		self._default_value : str = self._value

	def set_to (self, entry : Union[str, None] = None) -> None:

		self._value = entry if (entry != None) else self._default_value

	def value (self) -> str:

		return (self._value)

	def concatenate (self, entry : str = "", separator : str = "") -> str:

		return (f"{self._value}{separator}{entry}")

	def length (self) -> int:

		return (len (self._value))

	def set_concatenate (self, entry : str = "", separator : str = "") -> None:

		self._value = f"{self._value}{separator}{entry}"

	def has (self, entry : str) -> bool:

		return (entry in self._value)
	
	def is_equal_to (self, entry : Union[str, None] = None) -> bool:

		return (self._value == entry) if (entry != None) else (self._value == self._default_value)

	def is_not_equal_to (self, entry : Union[str, None] = None) -> bool:

		return (self._value != entry)if (entry != None) else (self._value != self._default_value)

class Ext_Str (Str):

	def __repr__ (self) -> str:

		return (f"Str : {self._value}")
	
	def __setitem__ (self, entry : str, index : Union[int, None] = None) -> None:

		if (index == None):

			self._value = f"{self._value}{entry}"

		else:

			self._value[index] = entry

	def __getitem__ (self, index : int = 0) -> str:

		return (self._value[index])