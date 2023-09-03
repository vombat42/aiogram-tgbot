from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
	MAIN_MENU = State()


class StatesExercises(StatesGroup):
	EX_SELECT = State()
	EX_COUNT = State()
	EX_CONFIRM = State()
	EX_MANAGE_SELECT = State()
	EX_NEW_NAME = State()
	EX_NEW_UNIT = State()
	EX_NEW_CONFIRM = State()
	EX_DEL = State()
	EX_EDIT = State()
	EX_EDIT_NAME = State()
	EX_EDIT_NAME_CONFIRM = State()


class StatesReport(StatesGroup):
	REP_SELECT = State()
	REP_PERIOD = State()
	REP_CONFIRM = State()