from .general import *

class List ():

	def __init__ (self, entry : list = []) -> None:

		self._value : list = entry
		self._default_value : list = self._value

	def set_to (self, entry : Union[list, None] = None) -> None:

		self._value = entry if (entry != None) else self._default_value

	def value (self) -> list:

		return (self._value)

	def set_at (self, entry : Any, index : int = 0) -> None:

		self._value[index] = entry

	def value_at (self, index : int = 0) -> Any:

		return (self._value[index])

	def length (self) -> int:

		return (len (self._value))

	def has (self, entry : Any) -> bool:

		return (entry in self._value)

	def is_empty (self) -> bool:

		return (len (self._value) == 0)

	def is_not_empty (self) -> bool:

		return (len (self._value) > 0)

	def is_equal_to (self, entry : Union[list, None] = None) -> bool:

		return (self._value == entry) if (entry != None) else (self._value == self._default_value)

	def is_not_equal_to (self, entry : Union[list, None] = None) -> bool:

		return (self._value != entry) if (entry != None) else (self._value != self._default_value)

	def append (self, entry : Any) -> None:

		self._value.append (entry)

class Ext_List (List):

	def __repr__ (self) -> str:

		return (f"List : {self._value}")
	
	def __iadd__ (self, entry : Any) -> None:

		self._value.append (entry)

	def __setitem__ (self, entry : Any, index : int = 0) -> None:

		self._value[index] = entry

	def __getitem__ (self, index : int = 0) -> Any:

		return (self._value[index])