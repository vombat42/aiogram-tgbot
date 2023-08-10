from aiogram.filters.callback_data import CallbackData
# from typing import Optional

class ExInfo(CallbackData, prefix='ex'):
	action: str 
	ex_id: int
	name: str
	unit: str
	# ex_id: Optional[int]
	# name: Optional[str]
	# unit: Optional[str]
