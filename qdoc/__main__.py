import sys
import traceback
import app_const
import app_factory
from ua_core.errors.errors import UaException
from ua_app import apputils

try:

    # Parse Parameters:
    
    argument_parser = app_factory.create_argument_parser()
    parsed_params = apputils.get_parsed_args (argument_parser, sys.argv)
    apputils.show_defaults (argument_parser, parsed_params, app_const.APP_INFO)
    
    
    # Run App:
    
    app = app_factory.create_app()
    app.main (parsed_params)

except UaException as e:
    
    print ('\n'.join(e.messages))

except Exception as e:
    
    print ('Exception: ' + str(e))
    print (traceback.format_exc())
