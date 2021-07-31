from ua_core.utils.os import ua_os_factory
from ua_console.console import Console
from ua_console.listpicker import ListPicker
from ua_core.utils.uaargparse import UaArgumentParser
from qdoc.qdoc import QDocs

from app import App
import app_const


def create_app():
    return App(create_qdocs(), create_ua_os(), create_list_picker())
    
def create_argument_parser():
    
    parser = UaArgumentParser(
        prog = app_const.APP_INFO.name,
        description = 'Creates a document from a template and fills in all the defaults.',
        usage = app_const.HELP_USAGE,
        add_help=False
    )
           
    parser.add_argument('qdoc_name', nargs='?', help='The qdoc to create') # 1st standard argument. Not optional.
    parser.add_argument('parameters', nargs='*', help='qdoc parameter values (if any)')

    # parsers.add_argument('\.', help='save in current directory', action='store_true', dest='to_current_dir')
    parser.add_argument('-l', '--list', help='list available qdocs', action='store_true', dest='list_docs_flag')        
    parser.add_argument('-n', '--new', help='create a new qdoc (will open latest if missing)', action='store_true', dest='new_doc_flag')        
    parser.add_argument('-h', '--help', help='show this help message', action='store_true', dest='show_help_flag')        
    parser.add_argument('-p', '--parameters', help='show parameters', action='store_true', dest='show_params_flag')
    parser.add_argument('-t', '--tags', help='show tags', action='store_true', dest='show_tags_flag')
    parser.add_argument('-v', '--version', help='show app version', action='store_true', dest='show_version_flag')
    
    return parser

def create_qdocs():
    return QDocs (date_format = app_const.DATE_FORMAT, date_separator = app_const.DATE_SEPARATOR, def_settings_subdir = app_const.SETTINGS_DIR, ua_os = create_ua_os())

def create_ua_os():
    return ua_os_factory.create_ua_os()

def create_console():
    return Console()

def create_list_picker():
    return ListPicker (create_console())
