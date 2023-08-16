from aiogram.filters.callback_data import CallbackData
from datetime import date
# from typing import Optional

class ExInfo(CallbackData, prefix='ex'):
	action: str 
	ex_id: int
	name: str
	unit: str



