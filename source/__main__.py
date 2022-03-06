import sys
import traceback
from shared.errors import *
from settings import *
from app import main

try:

    from sys import argv
    print(argv)
    print()

    parser = argument_parser()
    parameters = parser.parse_args()
    main(APP_SETTINGS, parameters, os())

except KeyboardInterrupt:

    pass

except UserRequestExit:

    pass

except ApplicationError as e:
    
    print ('\n'.join(e.messages))
    print ('')

except Exception as e:
    
    print ('Exception: ' + str(e))
    print (traceback.format_exc())

