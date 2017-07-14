from datetime import date
from datetime import datetime
from datetime import timedelta
import os

from ua.core.comp.duplicates import DuplicateTracker
from ua.core.comp.findfile import FindFile
from ua.core.errors.errors import InvalidConfig
from ua.core.errors.errors import ItemAlreadyExists
from ua.core.errors.errors import UserRequestExit
from ua.core.errors.errors import FailedValidations

from ua.core.utils import fileutils
from ua.core.utils import strutils

from parser import text_parser_perc
from parser.text_parser_perc import has_var

from qdoc.qdoc_helpers import *

QDOC_DEF_EXT = 'qdef'


SETTING_FILE_NAME = 'fileName'
SETTING_FILE_DIR = 'fileDir'
SETTING_FIRST_DATE = 'firstDate'

TAG_COMMAND_COPY_ONLY = "copyOnly"
TAG_DATE = 'date'
TAG_FILE_NAME = SETTING_FILE_NAME
TAG_PARAMS = 'params'
TAG_WEEK_NUMBER = 'weekNumber'
TAG_WEEK_NUMBER_PADDED = 'paddedWeekNumber'
TAG_WEEK_NEXT_NUMBER = 'weekNextNumber'
TAG_WEEK_NEXT_NUMBER_PADDED = 'paddedWeekNextNumber'

TAG_WEEK_START_DATE = 'weekStartDate'
TAG_WEEK_END_DATE = 'weekEndDate'
TAG_WEEK_NEXT_START_DATE = 'weekNextStartDate'
TAG_WEEK_NEXT_END_DATE = 'weekNextEndDate'

TAG_USER_NOTES = "userNotes"


class QDoc:
    ''' Responsible for reading the definition, locating and creating the target file.
    '''

    def __init__(self, date_format, date_separator, def_file, ua_os, load_data = True):

        self._date_format = date_format
        self._date_separator = date_separator
        self._def_file = def_file
        self._ua_os = ua_os
        
        self._target_file_path = None
        self._def_tag_dict_actual = None
        
        if load_data:
            # Not loaded for unit tests only:
            self._def_tag_dict = self._retrieve_def_tag_dict (self._def_file)
            self._param_tags = self._get_params_from_dict (self._def_tag_dict)
            self._template = self._retrieve_template (self._def_file)
    
    def create(self):
        '''
            Creates a document from the qdoc_def and parsed_params.
            Saves it in the target directory.
        '''
        
        # Get/Create Content:
        
        if TAG_COMMAND_COPY_ONLY not in self._def_tag_dict:
            file_content = text_parser_perc.replace_variables(self._def_tag_dict_actual, self._template)
            file_content = text_parser_perc.remove_escapes(file_content)
        else:
            file_content = self._template

        
        # Create new file:
        
        target_file_path = self.target_file_path()
        target_file_dir = fileutils.file_dir (target_file_path)
        
        if not os.path.exists(target_file_dir):
            os.makedirs(target_file_dir)

        if not fileutils.is_file_exists(target_file_path):
            file = open (self._target_file_path, 'wb')
            file.write (file_content.encode ('utf-8'))
        else:
            raise ItemAlreadyExists (target_file_path)

    def def_file_path (self):
        return self._def_file.path
    
    def target_file_dir(self):
        return self._def_tag_dict_actual[SETTING_FILE_DIR]
    
    def target_file_name(self):
        return self._def_tag_dict_actual[SETTING_FILE_NAME]
    
    def target_file_path(self):
        return self._target_file_path
    
    def set_params (self, params):
        
        def_tag_dict_actual = self._def_tag_dict.copy()
        
        # add param tag values:

        param_tags = self._param_tags
        
        for tag, value in zip (param_tags, params):
            def_tag_dict_actual[tag] = value
        
        # request missing data:
        
        if len (param_tags) > len (params):
            for tag in param_tags[len(params):]:
                if tag not in def_tag_dict_actual:
                    
                    print (tag + ": ", end='')
                    value = input()
                    
                    if strutils.is_blank(value):
                        raise UserRequestExit ('User exited entering parameter \'' + tag + '\'.')
                    
                    def_tag_dict_actual[tag] = value
        
        # Update variables:
        
        def_tag_dict_actual = text_parser_perc.update_variable_values (def_tag_dict_actual)
        
        # check for file name:
        
        target_file_path = self._get_target_file_path (def_tag_dict_actual)
        
        if has_var (target_file_path):

            self._target_file_path = None
            self._def_tag_dict_actual = None

            raise FailedValidations('File path couldn\'t be generated: \'' + self._file_path + '\'')

        else:
            
            self._def_tag_dict_actual = def_tag_dict_actual
            self._target_file_path = target_file_path
            
    def tag_dict(self):
        return self._def_tag_dict_actual.copy()
    
    def user_notes(self):
        
        if TAG_USER_NOTES in self._def_tag_dict:
            return self._def_tag_dict[TAG_USER_NOTES]
        else:
            return None

    def _calc_week_end_date (self, week_start_date):

        timediff = timedelta (days = 6)
        week_end_date = week_start_date + timediff
        
        return week_end_date
    
    def _calc_week_number (self, start_date_string, end_date_string):
        
        start_date = self._to_date (start_date_string)
        end_date = self._to_date (end_date_string)
        
        timediff = end_date - start_date
        week_number = 1 + (timediff.days // 7)
        
        return week_number
    
    def _calc_week_next_number (self, start_date_string, end_date_string):
        
        return 1 + self._calc_week_number (start_date_string, end_date_string)
    
    def _calc_week_start_date (self, start_date_string, week_number_string):
        
        start_date = self._to_date (start_date_string)
        timediff = timedelta (days = 7 * (int (week_number_string) - 1))
        week_start_date = (start_date + timediff).date()
        
        return week_start_date
    
    def _create_file (self, def_tag_dict, template_file_path, target_file_path):
        pass
    
    def _get_def_file_name(self):
        return self._def_file.name + "." + QDOC_DEF_EXT
    
    def _get_params_from_dict (self, def_tag_dict):
        
        if TAG_PARAMS in def_tag_dict:
            params_string = def_tag_dict[TAG_PARAMS]
            params = [ param.strip() for param in params_string.split(',')]
        else:
            params = []
        
        return params

    def _get_target_file_path (self, def_tag_dict):
        ''' Get the target file path by reading the tags from the tag dict.
        '''
        return self._ua_os.join_path (def_tag_dict[SETTING_FILE_DIR], def_tag_dict[SETTING_FILE_NAME])
    
    def _retrieve_def_tag_dict (self, def_file):
        ''' Read in the tags from the def file
            Then process as many of the tags as possible.
        '''
        
        # Read file
        tag_dict = read_file_to_dict (def_file.path);

        # Validate
        self._validate_def (tag_dict)

        # Parse

        self._set_tag_defaults (tag_dict)
        tag_dict = text_parser_perc.update_variable_values (tag_dict)
        
        return tag_dict

    def _retrieve_template (self, def_file):
        
        # Get file list.
        def_dir = fileutils.file_dir(def_file.path)
        name = def_file.name
        
        file_names = fileutils.read_dir_file_names (def_dir, name + ".*")
        
        # Pick non .def file:
        template_file_path = None
        for file_name in file_names:
            if file_name != self._get_def_file_name():
                template_file_path = self._ua_os.join_path(def_dir, file_name)
         
        if not template_file_path:
            raise InvalidConfig ('No template found for \'' + name + '\'')
        
        # Read contents
        template_file = open(template_file_path, 'r')
        template = template_file.read() 
        
        return template

    def _set_tag_defaults (self, tag_dict):
        
        if not TAG_DATE in tag_dict:
            tag_dict[TAG_DATE] = self._to_date_string (date.today())
        
        if SETTING_FIRST_DATE in tag_dict and not TAG_WEEK_NUMBER in tag_dict:
            week_number = self._calc_week_number (tag_dict[SETTING_FIRST_DATE], tag_dict[TAG_DATE])
            tag_dict[TAG_WEEK_NUMBER] = str (week_number)
            tag_dict[TAG_WEEK_NEXT_NUMBER] = str (week_number + 1)
        
        if TAG_WEEK_NUMBER in tag_dict:
            tag_dict[TAG_WEEK_NUMBER_PADDED] = tag_dict[TAG_WEEK_NUMBER].rjust (3, '0')
        
        if TAG_WEEK_NUMBER in tag_dict:
            week_start_date = self._calc_week_start_date (tag_dict[SETTING_FIRST_DATE], tag_dict[TAG_WEEK_NUMBER])
            week_end_date = self._calc_week_end_date (week_start_date)
            tag_dict[TAG_WEEK_START_DATE] = self._to_date_string (week_start_date)
            tag_dict[TAG_WEEK_END_DATE] = self._to_date_string (week_end_date)
        
        if TAG_WEEK_NEXT_NUMBER in tag_dict:
            tag_dict[TAG_WEEK_NEXT_NUMBER_PADDED] = tag_dict[TAG_WEEK_NEXT_NUMBER].rjust (3, '0')
        
        if TAG_WEEK_NEXT_NUMBER in tag_dict:
            week_next_start_date = self._calc_week_start_date (tag_dict[SETTING_FIRST_DATE], tag_dict[TAG_WEEK_NEXT_NUMBER])
            week_next_end_date = self._calc_week_end_date (week_next_start_date)
            tag_dict[TAG_WEEK_NEXT_START_DATE] = self._to_date_string (week_next_start_date)
            tag_dict[TAG_WEEK_NEXT_END_DATE] = self._to_date_string (week_next_end_date)
            
    def _to_date (self, date_string):
        
        date_string = date_string.replace ('/', self._date_separator)
        date_string = date_string.replace ('-', self._date_separator)
        date_string = date_string.replace ('.', self._date_separator)
        
        date_actual = datetime.strptime (date_string, self._date_format)
        
        return date_actual
    
    def _to_date_string (self, date):
        
        return date.strftime (self._date_format)

    def _validate_def (self, tag_dict):

        errors = []
        
        if not SETTING_FILE_DIR in tag_dict:
            errors.append('Missing setting \'' + SETTING_FILE_DIR +'\'.')

        if not SETTING_FILE_NAME in tag_dict:
            errors.append('Missing setting \'' + SETTING_FILE_NAME +'\'.')
            
        if errors:
            raise InvalidConfig (errors)


class QdocDefFile:
    """ 
        Created with CodeCrank.io
    """

    def __init__ (self, name = None, path = None):

        self.name = name
        self.path = path

    def __repr__ (self):

        return "QdocDefFile [" + \
            "name=" + (self.name if self.name is not None else "[None]") + \
            ", path=" + (self.path if self.path is not None else "[None]") + \
            "]"


class QDocs:
    ''' Container class and manager class for QDoc classes
    '''
    
    def __init__(self, date_format, date_separator, def_settings_subdir, ua_os):
        
        self._date_format = date_format
        self._date_separator = date_separator
        self._ua_os = ua_os

        self.def_dirs = self._find_def_dirs(def_settings_subdir, ua_os)
        self._def_file_dict, self._duplicates_dict = self._retrieve_def_file_dict_and_duplicate_dict(self.def_dirs)
    
    def def_names(self):
        
        def_names = [def_name for def_name in self._def_file_dict]
        def_names.sort()
        
        return def_names
    
    def duplicates_dict(self):
        return self._duplicates_dict
    
    def has_duplicates (self):
        return len (self._duplicates_dict) > 0
         
    def retrieve_qdoc (self, def_name):
        
        def_file_actual = None
        
        if def_name in self._def_file_dict:
            
            def_file_actual = self._def_file_dict[def_name]
        
        else:
            
            # Try to match subname:

            find_count = 0
            
            for def_file_key in self._def_file_dict:
                
                def_file = self._def_file_dict[def_file_key]
                
                if strutils.startswith_ignore_case(def_file.name, def_name):
                    def_file_actual = def_file
                    find_count += 1
            
            if find_count > 1:
                
                # print matching names:
                
                print ("Names (" + str (find_count) + "): ")
                for def_file_key in self._def_file_dict:
                
                    def_file = self._def_file_dict[def_file_key]
                    
                    if strutils.startswith_ignore_case(def_file.name, def_name):
                        print ("   " + def_file.name)

                print()
                
                raise FailedValidations('Ambiguous name \'' + def_name + '\'.')

            
            if find_count < 1:

                raise FailedValidations('Could not find \'' + def_name + '\'.')
        
        return QDoc(date_format = self._date_format, date_separator = self._date_separator, def_file = def_file_actual, ua_os = self._ua_os)

    def _find_def_dirs (self, settings_subdir, ua_os):
        '''
            Find the location of the definitions directory
            
            raises InvalidConfigurationException if not found.
        '''
    
        find_file = FindFile (ua_os)
        parent_dirs = find_file.findAll(settings_subdir)
        
        if parent_dirs is None:
            raise InvalidConfig ("Configuration Error: Could not locate " + settings_subdir + " settings directory.") 
        
        def_dirs = [ fileutils.join (parent_dir, settings_subdir) for parent_dir in parent_dirs ]
        
        return def_dirs

    def _retrieve_def_file_dict_and_duplicate_dict (self, def_dirs):
        '''
            Returns the names of all available qdoc definitions from the qdoc settings directory
        '''
        
        def_file_dict = {}
        duplicates_tracker = DuplicateTracker()
        
        for def_dir in def_dirs:
            
            file_paths = fileutils.read_dir_file_paths(def_dir, "*." + QDOC_DEF_EXT)
            
            for file_path in file_paths:
                def_name = fileutils.file_base_name(file_path)
                qdoc_def_file = QdocDefFile(def_name , file_path)
                
                def_file_dict[def_name] = qdoc_def_file
                duplicates_tracker.add(def_name, qdoc_def_file)
        
        return def_file_dict, duplicates_tracker.duplicates_dict()


