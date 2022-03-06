from os import environ
from datetime import date
from datetime import datetime
from datetime import timedelta


SOURCE = 'source'
SOURCE_DIRECTORY = 'source_directory'
SOURCE_NAME = 'source_name'
TARGET = 'target'
TARGET_DIRECTORY = 'target_directory'
TARGET_NAME = 'target_name'

PARAMETERS = 'parameters'

DATE = 'date'
DATE_TIME_1 = 'date_time'
DATE_TIME_2 = 'dateTime'
TIME = 'time'

NOW = 'now'
TODAY = 'today'
YESTERDAY = 'yesterday'

YEAR = 'year'
MONTH = 'month'
DAY = 'day'
HOUR = 'hour'
MINUTE = 'minute'
SECOND = 'second'

FIRST_DATE_1 = 'first_date'
FIRST_DATE_2 = 'firstDate'

BIWEEK_NUMBER_1 = 'biweek_number'
BIWEEK_NUMBER_PADDED_1 = 'padded_biweek_number'
BIWEEK_NEXT_NUMBER_1 = 'biweek_next_number'
BIWEEK_NEXT_NUMBER_PADDED_1 = 'padded_biweek_next_number'
BIWEEK_START_DATE_1 = 'biweek_start_date'
BIWEEK_END_DATE_1 = 'biweek_end_date'
BIWEEK_NEXT_START_DATE_1 = 'biweek_next_start_date'
BIWEEK_NEXT_END_DATE_1 = 'biweek_next_end_date'

BIWEEK_NUMBER_2 = 'biweekNumber'
BIWEEK_NUMBER_PADDED_2 = 'paddedBiweekNumber'
BIWEEK_NEXT_NUMBER_2 = 'biweekNextNumber'
BIWEEK_NEXT_NUMBER_PADDED_2 = 'paddedBiweekNextNumber'
BIWEEK_START_DATE_2 = 'biweekStartDate'
BIWEEK_END_DATE_2 = 'biweekEndDate'
BIWEEK_NEXT_START_DATE_2 = 'biweekNextStartDate'
BIWEEK_NEXT_END_DATE_2 = 'biweekNextEndDate'

WEEK_NUMBER_1 = 'week_number'
WEEK_NUMBER_PADDED_1 = 'padded_week_number'
WEEK_NEXT_NUMBER_1 = 'week_next_number'
WEEK_NEXT_NUMBER_PADDED_1 = 'padded_week_next_number'
WEEK_START_DATE_1 = 'week_start_date'
WEEK_END_DATE_1 = 'week_end_date'
WEEK_NEXT_START_DATE_1 = 'week_next_start_date'
WEEK_NEXT_END_DATE_1 = 'week_next_end_date'

WEEK_NUMBER_2 = 'weekNumber'
WEEK_NUMBER_PADDED_2 = 'paddedWeekNumber'
WEEK_NEXT_NUMBER_2 = 'weekNextNumber'
WEEK_NEXT_NUMBER_PADDED_2 = 'paddedWeekNextNumber'
WEEK_START_DATE_2 = 'weekStartDate'
WEEK_END_DATE_2 = 'weekEndDate'
WEEK_NEXT_START_DATE_2 = 'weekNextStartDate'
WEEK_NEXT_END_DATE_2 = 'weekNextEndDate'

LOWER_CASE_1 = '_lower_case'
UPPER_CASE_1 = '_upper_case'
NO_SPACES_1 = '_no_spaces'

LOWER_CASE_2 = 'LowerCase'
UPPER_CASE_2 = 'UpperCase'
NO_SPACES_2 = 'NoSpaces'


def default_variables():

	variables = {}

	set_environment_variables(variables)
	set_datetime_today(variables)
	set_datetime_yesterday(variables)

	return variables


def add_variable(variables, name, value):

	no_spaces = value.replace(' ', '')

	variables[name] = value

	variables[name + LOWER_CASE_1] = value.lower()
	variables[name + LOWER_CASE_2] = value.lower()
	variables[name + UPPER_CASE_1] = value.upper()
	variables[name + UPPER_CASE_2] = value.upper()

	variables[name + NO_SPACES_1] = no_spaces
	variables[name + NO_SPACES_2] = no_spaces

	variables[name + LOWER_CASE_1 + NO_SPACES_1] = no_spaces.lower()
	variables[name + LOWER_CASE_2 + NO_SPACES_2] = no_spaces.lower()
	variables[name + UPPER_CASE_1 + NO_SPACES_1] = no_spaces.upper()
	variables[name + UPPER_CASE_2 + NO_SPACES_2] = no_spaces.upper()


def set_datetime_today(variables):

	now = datetime.today()

	variables[DATE] = f'{now:%Y-%m-%d}'
	variables[TODAY] = f'{now:%Y-%m-%d}'

	variables[DATE_TIME_1] = f'{now:%Y-%m-%d}'
	variables[DATE_TIME_2] = f'{now:%Y-%m-%d}'
	variables[NOW] = f'{now:%Y-%m-%d %H:%M:%S}'

	variables[YEAR] = f'{now:%Y}'
	variables[MONTH] = f'{now:%m}'
	variables[DAY] = f'{now:%d}'
	variables[HOUR] = f'{now:%H}'
	variables[MINUTE] = f'{now:%M}'
	variables[SECOND] = f'{now:%S}'

	return variables


def set_datetime_yesterday(variables):

	yesterday = date.today() - timedelta(days = 1)

	variables[YESTERDAY] = f'{yesterday:%Y-%m-%d}'

	variables[YESTERDAY + '_' + YEAR] = f'{yesterday:%Y}'
	variables[YESTERDAY + '_' + MONTH] = f'{yesterday:%m}'
	variables[YESTERDAY + '_' + DAY] = f'{yesterday:%d}'

	return variables


def set_environment_variables(variables):

	for key in environ.keys():
		variables[key] = environ[key]

	return variables
