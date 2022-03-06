import os
from shared.os.base import BaseOS
from shared.os.const import *

class MacOS(BaseOS):
    
    FILE_SEPARATOR = FILE_SEPARATOR_LINUX
    NEWLINE = NEWLINE_LINUX
    OS_NAME = 'OS X'
    PATH_SEPARATOR = PATH_SEPARATOR_LINUX
    USER_HOME_DIRECTORY_VARIABLE = 'HOME'
    USER_APP_SUBDIRECTORY = 'Library/Application Support'

    def file_separator(self):
        return MacOS.FILE_SEPARATOR

    def is_linux(self):
        return False

    def is_osx(self):
        return True

    def is_windows(self):
        return False

    def newline(self):
        return MacOS.NEWLINE
    
    def open_document (self, file_name):
        os.system ('open "' + file_name + '"')

    def os_name(self):
        return MacOS.OS_NAME

    def normalize_path(self, path):
        
        if path:
            path = path \
                .replace (FILE_SEPARATOR_WINDOWS, MacOS.FILE_SEPARATOR) \
                .replace (PATH_SEPARATOR_WINDOWS, MacOS.PATH_SEPARATOR)
            
        return path
    
    def normalize_paths(self, paths):
        return [self.normalize_path(path) for path in paths]

    def path_separator(self):
        return MacOS.PATH_SEPARATOR

    def user_app_dir(self):
        return os.path.join(self.user_dir(), MacOS.USER_APP_SUBDIRECTORY)

    def user_dir(self):
        return os.getenv(MacOS.USER_HOME_DIRECTORY_VARIABLE)

