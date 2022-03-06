import os
from shared.utils.files import *

class FindFile:

    ''' Search a list of config / user directories to find a file
    
        Priority:

            Current Dir
            App Environment Variable
            User_App_Data_Dir Environment Variable / Subdirectory
            Standard User Data Dir / Subdirectory
            Standard User App Data Dir / Subdirectory
            
        Uses builder pattern to set up.
    '''

    DIRECTORY_ENVIRONMENT_VARIABLE = 'User_App_Data_Dir'
    
    def __init__(self, os, debug = False, environment_variable = None):
        
        self._os = os
        
        self._debug = debug
        self._environment_variable = environment_variable
        self._search_current_dir = True
        self._search_user_app_dir = True
        self._search_user_app_dir_env_var = True
        self._search_user_dir = True
        self._subdirectory = None
   
    def find_all (self, file_name):
        ''' Return the directories containing the file.
            Returns an empty if not found.
        '''
        actual_dir_list = []
        
        for dir_name in self._get_search_directories():

            path = join(dir_name, file_name)
            self._print (path)
            
            if is_directory(path):
                
                self._print ('  Found')
                actual_dir_list.append (dir_name)
            
        return actual_dir_list
    
    def find_first (self, file_name):
        ''' Return the directory containing the file.
            Returns None if not found.
        '''
        actual_dir = None
        
        for dir_name in self._get_search_directories():

            path = join(dir_name, file_name)
            self._print (path)
            
            if is_directory(path):
                
                self._print ('Found')
                actual_dir = dir_name
                break
            
        return actual_dir
    
    def environment_variable (self, Variable):
        
        self._environment_variable = Variable
        return self
    
    def search_current_dir (self, search_current_dir):
        ''' Set whether to search the current directory (true | false).
        '''
        
        self._search_current_dir = search_current_dir
        return self

    def search_user_app_dir (self, search_user_app_dir):
        ''' Set whether to search the standard user app directory (true | false).
        '''
        
        self._search_user_app_dir = search_user_app_dir
        return self

    def search_user_app_dir_env_var (self, search_user_app_dir_env_var):
        ''' Set whether to search the directory set by the user app directory environment variable (true | false).
        '''
        
        self._search_user_app_dir_env_var = search_user_app_dir_env_var
        return self

    def search_user_dir (self, search_user_dir):
        ''' Set whether to search the user directory (true | false).
        '''
        
        self._search_user_dir = search_user_dir
        return self

    def subdir_name (self, subdir_name):
        ''' Set the subdirectory name.
        '''
        
        self._subdirectory = subdir_name
        return self

    def _get_dir_subdir (self, dir_name):
        ''' Correctly concatenates the pre-set subdirectory name to the directory.
        '''
        
        if self._subdirectory is not None:
            dir_name = os.path.join (dir, self._subdirectory)
        #else:
            # No subdirectory
            # Return the directory as is.
        
        return dir_name
    
    def _get_search_directories(self):
        
        directories = []
        
        # Current Directory:
        if self._search_current_dir:

            directories.append (os.getcwd())
            
        # App Environment Variable:
        if self._environment_variable is not None:

            path_value = os.getenv(self._environment_variable)
            if path_value is not None:
                directories.append(path_value)
        
        # User_App_Data_Dir:
        if self._search_user_app_dir_env_var:

            user_app_data_directories_value = os.getenv(self.DIRECTORY_ENVIRONMENT_VARIABLE)
            
            if user_app_data_directories_value is not None:
                
                user_app_data_directories_value = self._os.normalize_path (user_app_data_directories_value)
                user_app_data_directories = user_app_data_directories_value.split (self._os.PATH_SEPARATOR)
                
                for dir in user_app_data_directories:
                    if dir: # Check for empty strings caused by starting or ending path separator.
                        directories.append (self._get_dir_subdir(dir))
                    
        # Standard User Dir:
        if self._search_user_dir:
            
            dir = self._os.user_dir()
            if dir: 
                directories.append(self._get_dir_subdir(dir))
        
        # Standard User App Dir:
        if self._search_user_app_dir:
            
            dir = self._os.user_app_dir()
            if dir: 
                directories.append(self._get_dir_subdir(dir))
            
        return directories
         
    def _print (self, text):
        
        if self._debug:
            print (text)

