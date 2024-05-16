from abc import ABC, abstractmethod

import base64







class IFormatter(ABC):



	def __init__(self):
		super().__init__()



	# NOTE: The point of having postfixes is so the final formatter can know the different pieces.
	def _get_unique_postfix(self) -> str:
		name = self.__class__.__name__
		b64_name = base64.b64encode(name.encode("utf-8")).decode("utf-8")
		return f"|`FORMATTER_POSTFIX`{b64_name}|"



	@staticmethod
	def _strip_postfixes(string:str) -> str:
		# example string: `abc - foo|def - bar|ghi - hi|`

		if not string.endswith("|"):
			raise Exception("This should never happen.")

		ret_str = ""
		_splitted = string.split("|`FORMATTER_POSTFIX`")[:-1]  # last is always fluff.
		ret_str += _splitted[0]  # first is always juicy.
		_splitted = _splitted[1:]

		for splitted in _splitted:
			end = None
			# look for the closing pipe...
			for i, char in enumerate(splitted):
				if char == "|":
					end = i
			assert end is not None
			ret_str += splitted[end:]
		
		return ret_str
				


	@staticmethod
	def handle(inst, string:str, is_first: bool) -> str:
		if not is_first:
			string = IFormatter._strip_postfixes(string)
		addition = inst._handle(string)
		if addition is None:
			raise Exception("The formatter did not return a string.")
		return f"{addition}{inst._get_unique_postfix()}"



	@abstractmethod
	def _handle(self, string:str) -> str:
		pass