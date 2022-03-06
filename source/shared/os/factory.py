from platform import system
from shared.os.const import *
from . import Linux
from . import MacOS
# from . import WindowsOS


def new_os (name = None):

    if not name:
        name = system()
    
    match name:
        case 'Linux':
            return Linux()
        case 'Darwin':
            return MacOS()
        case 'Windows':
            return Windows()
        case _:
            return None

