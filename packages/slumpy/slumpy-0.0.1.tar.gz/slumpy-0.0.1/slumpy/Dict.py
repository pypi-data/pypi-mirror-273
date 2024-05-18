from .general import *

class Dict ():

	def __init__ (self, entry : dict = {}) -> None:

		self._value : dict = entry
		self._default_value : dict = self._value

	def set_to (self, entry : Union[dict, None] = None) -> None:

		self._value = entry if (entry != None) else self._default_value

	def value (self) -> dict:

		return (self._value)

	def set_at (self, entry : Any, key : Any) -> None:

		self._value[key] = entry

	def value_at (self, key : Any) -> Any:

		return (self._value[key])
	
	def has (self, entry : Any) -> bool:

		return (entry in self._value)

	def is_equal_to (self, entry : Union[dict, None] = None) -> bool:

		return (self._value == entry) if (entry != None) else (self._value == self._default_value)

	def is_not_equal_to (self, entry : Union[dict, None] = None) -> bool:

		return (self._value != entry) if (entry != None) else (self._value != self._default_value)

class Ext_Dict (Dict):

	def __repr__ (self) -> str:

		return (f"Dict : {self._value}")

	def __setitem__ (self, entry : Any, key : Any) -> None:

		self._value[key] = entry

	def __getitem__ (self, key : Any) -> Any:

		return self._value[key]