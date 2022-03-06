from argparse import ArgumentParser
from dataclasses import dataclass
from shared.data import AppInfo
from shared.os import *
from shared.ui.console import Console
from shared.ui.listpicker import ListPicker


@dataclass
class AppSettings:
	base_directory: str
	os: BaseOS
	ui: Console


APP_NAME = 'quickdoc'

APP_VERSION      = '2.0.1'
APP_BUILD_DATE   = '2022-03-03'
APP_BUILD_NUMBER = '24'
APP_CREATED_DATE = '2017-02-03'

DATE_FORMAT = '%Y.%m.%d'
DATE_SEPARATOR = '.'

BASE_DIRECTORY = 'QuickDoc'
QUICKDOC_EXTENSION = 'qdef'

HELP_USAGE = APP_NAME + ' [-l] [-n] [-h] [-p] [-v] name [param1 [param2 ...]]'

APP_INFO = AppInfo (APP_NAME, APP_VERSION, APP_BUILD_DATE, APP_BUILD_NUMBER, APP_CREATED_DATE)

APP_SETTINGS = AppSettings(
		BASE_DIRECTORY,
		new_os(),
		Console())


def argument_parser():
    
    parser = ArgumentParser(
        prog = APP_INFO.name,
        description = 'Creates a document from a template and fills in all the defaults.',
        usage = HELP_USAGE,
        add_help=False
    )
           
    parser.add_argument('name', nargs='?', help='The qdoc to create') # 1st standard argument. Not optional.
    parser.add_argument('parameters', nargs='*', help='qdoc parameter values (if any)')

    # parsers.add_argument('\.', help='save in current directory', action='store_true', dest='to_current_dir')
    parser.add_argument('-l', '--list', help='list available qdocs', action='store_true', dest='list_docs')        
    parser.add_argument('-n', '--new', help='create a new qdoc (will open latest if missing)', action='store_true', dest='new_doc')        
    parser.add_argument('-h', '--help', help='show this help message', action='store_true', dest='show_help')        
    parser.add_argument('-p', '--parameters', help='show parameters', action='store_true', dest='show_params')
    parser.add_argument('-t', '--tags', help='show tags', action='store_true', dest='show_tags_flag')
    parser.add_argument('-V', '--verbose', help='verbose', action='store_true', dest='verbose')
    parser.add_argument('-v', '--version', help='show app version', action='store_true', dest='show_version')
    
    return parser

def os():
    return new_os()

def list_picker():
    return ListPicker (Console())

