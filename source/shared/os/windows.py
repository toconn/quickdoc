import os
from shared.os.base import BaseOS
from shared.os.const import *

class Windows(BaseOS):
    
    FILE_SEPARATOR = FILE_SEPARATOR_WINDOWS
    NEWLINE = NEWLINE_WINDOWS
    OS_NAME = 'Windows'
    PATH_SEPARATOR = PATH_SEPARATOR_WINDOWS
    USER_HOME_DIRECTORY_VARIABLE = 'HOMEPATH'
    USER_APP_SUBDIRECTORY_VAR = 'APPDATA'

    def file_separator(self):
        return Windows.FILE_SEPARATOR

    def is_linux(self):
        return False

    def is_osx(self):
        return True

    def is_windows(self):
        return False

    def newline(self):
        return Windows.NEWLINE

    def open_document (self, file_name):
        os.system ('start "' + file_name + '"')

    def os_name(self):
        return Windows.OS_NAME

    def normalize_path(self, path):
        
        if path:
            path = path \
                .replace (FILE_SEPARATOR_LINUX, Windows.FILE_SEPARATOR) \
                .replace (PATH_SEPARATOR_LINUX, Windows.PATH_SEPARATOR)
            
        return path
    
    def normalize_paths(self, paths):
        return [self.normalize_path(path) for path in paths]

    def path_separator(self):
        return Windows.PATH_SEPARATOR

    def user_app_dir(self):
        return os.getenv(Windows.USER_APP_SUBDIRECTORY_VAR)

    def user_dir(self):
        return os.getenv(Windows.USER_HOME_DIRECTORY_VARIABLE)

