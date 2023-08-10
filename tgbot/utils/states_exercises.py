from aiogram.fsm.state import StatesGroup, State


class StatesExercises(StatesGroup):
	EX_SELECT = State()
	EX_COUNT= State()
	EX_CONFIRM= State()