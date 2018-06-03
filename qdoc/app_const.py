from ua_app.app import AppInfo

APP_NAME = 'QDoc'

APP_VERSION      = '1.3.0'
APP_BUILD_DATE   = '2018-04-10'
APP_BUILD_NUMBER = '22'
APP_CREATED_DATE = '2017-02-03'

COMMIT_DATE      = '2017-12-14 13:54:03'
COMMIT_NAME      = '1da3d26'
BRANCH_NAME      = 'master'

APP_INFO = AppInfo (APP_NAME, APP_VERSION, APP_BUILD_DATE, APP_BUILD_NUMBER, APP_CREATED_DATE, COMMIT_DATE, COMMIT_NAME, BRANCH_NAME)

HELP_USAGE = APP_INFO.name + ' [-l] [-n] [-h] [-p] [-v] target_qdoc [param1 [param2 ...]]'

DATE_FORMAT = '%Y.%m.%d'
DATE_SEPARATOR = '.'

SETTINGS_DIR = 'QDoc'
