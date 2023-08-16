from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
	MAIN_MENU = State()


class StatesExercises(StatesGroup):
	EX_SELECT = State()
	EX_COUNT= State()
	EX_CONFIRM= State()


class StatesReport(StatesGroup):
	REP_SELECT = State()
	REP_START_PERIOD= State()
	REP_END_PERIOD= State()
	REP_CONFIRM= State()