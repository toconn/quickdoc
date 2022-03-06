import os
from shared.os.base import BaseOS
from shared.os.const import *

class Linux(BaseOS):
    
    FILE_SEPARATOR = FILE_SEPARATOR_LINUX
    NEWLINE = NEWLINE_LINUX
    OS_NAME = 'Linux'
    PATH_SEPARATOR = PATH_SEPARATOR_LINUX
    USER_HOME_DIRECTORY_VARIABLE = 'HOME'
    USER_APP_SUBDIRECTORY = '.config'

    def file_separator(self):
        return Linux.FILE_SEPARATOR

    def is_linux(self):
        return False

    def is_osx(self):
        return True

    def is_windows(self):
        return False

    def newline(self):
        return Linux.NEWLINE

    def open_document (self, file_name):
        raise NotImplementedError

    def os_name(self):
        return Linux.OS_NAME

    def normalize_path(self, path):
        
        if path:
            path = path \
                .replace (FILE_SEPARATOR_WINDOWS, Linux.FILE_SEPARATOR) \
                .replace (PATH_SEPARATOR_WINDOWS, Linux.PATH_SEPARATOR)
            
        return path
    
    def normalize_paths(self, paths):
        return [self.normalize_path(path) for path in paths]

    def path_separator(self):
        return Linux.PATH_SEPARATOR

    def user_app_dir(self):
        return os.path.join(self.user_dir(), Linux.USER_APP_SUBDIRECTORY)

    def user_dir(self):
        return os.getenv(Linux.USER_HOME_DIRECTORY_VARIABLE)
