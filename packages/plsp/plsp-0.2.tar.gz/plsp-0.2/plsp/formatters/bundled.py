from .Formatter import IFormatter

from typing import Callable
from datetime import datetime



class TimeFormatter (IFormatter):
	def __default_further_parse_data(self, string:str) -> str:
		rd_or_st_or_th = None
		day_part = string.split("/")[0]
		rest_part = "/".join(string.split("/")[1:])
		if day_part.endswith("1"):
			rd_or_st_or_th = "st"
		elif day_part.endswith("2"):
			rd_or_st_or_th = "nd"
		elif day_part.endswith("3"):
			rd_or_st_or_th = "rd"
		else:
			rd_or_st_or_th = "th"
		return f"{day_part}{rd_or_st_or_th}/{rest_part}"

	def __init__(self, format_string:"str|None"=None, further_parse_data:"Callable[[str],str]|None"=None):
		super().__init__()
		self.format_string = "%d/%m/%y@%H:%M:%S.%f" if not format_string else format_string
		if further_parse_data is None:
			self.format_string = self.__default_further_parse_data(self.format_string)
		else:
			self.format_string = further_parse_data(self.format_string)

	def _handle(self, string:str) -> str:
		formatted_time = datetime.now().strftime(self.format_string)
		ret_str = ""
		sep = "|||"
		for line in string.split("\n"):
			ret_str += f"[{formatted_time}] {sep} {line}"
			sep = "---"
		return ret_str
	