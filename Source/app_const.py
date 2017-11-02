from ua.core.data.appinfo import AppInfo

APP_NAME = 'QDoc'

APP_VERSION      = '1.2.0'
APP_BUILD_DATE   = '2017-11-02'
APP_BUILD_NUMBER = '14'
APP_CREATED_DATE = '2017-02-03'

APP_INFO = AppInfo (APP_NAME, APP_VERSION, APP_BUILD_DATE, APP_BUILD_NUMBER, APP_CREATED_DATE)

HELP_USAGE = APP_INFO.name + ' [-l] [-n] [-h] [-p] [-v] target_qdoc [param1 [param2 ...]]'

DATE_FORMAT = '%Y.%m.%d'
DATE_SEPARATOR = '.'

SETTINGS_DIR = 'QDoc'
