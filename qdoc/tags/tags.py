'''
Created on Nov 14, 2017

@author: Tadhg
'''

from datetime import date
from ua_core.utils import dateutils


# Tags - Suffixes

TAG_SUFFIX_LOWER_CASE = 'LowerCase'
TAG_SUFFIX_NO_SPACES = 'NoSpaces'

# Tags - General

TAG_NAME = 'name'

# Tags - Dates:

TAG_BIWEEK_NUMBER = 'biweekNumber'
TAG_BIWEEK_NUMBER_PADDED = 'paddedBiweekNumber'
TAG_DATE = 'date'
TAG_FIRST_DATE = 'firstDate'
TAG_WEEK_NUMBER = 'weekNumber'
TAG_WEEK_NUMBER_PADDED = 'paddedWeekNumber'
TAG_WEEK_NEXT_NUMBER = 'weekNextNumber'
TAG_WEEK_NEXT_NUMBER_PADDED = 'paddedWeekNextNumber'

TAG_WEEK_START_DATE = 'weekStartDate'
TAG_WEEK_END_DATE = 'weekEndDate'
TAG_WEEK_NEXT_START_DATE = 'weekNextStartDate'
TAG_WEEK_NEXT_END_DATE = 'weekNextEndDate'


class tags:
    
    _tag_dict = {}
    
    def __init__(self, tag_dict = None):

        if tag_dict:
            self._tag_dict = tag_dict
        
        self._set_defaults()
        self._set_calculated_defaults()
        
        
    # Dict Like Functions:
    
    def clear(self):
        self._tag_dict.clear()
    
    def items(self):
        return self._tag_dict.items()

    def keys(self):
        return self._tag_dict.keys()

    def values(self):
        return self._tag_dict.values()

    def __cmp__(self, dict_):
        return self.__cmp__(self._tag_dict, dict_)

    def __contains__(self, item):
        return item in self._tag_dict

    def __iter__(self):
        return self._tag_dict.__iter__()
        
    def __getitem__(self, key):
        return self._tag_dict.__getitem__(key)
    
    def __setitem__(self, key, value):
        self._tag_dict.__setitem__(key, value)
    

    
    # Normal Functions:
    
    def copy(self):
        
        return self._tag_dict
    
    def _add_tag_lower_case_no_space (self, tag_dict, tag_name, tag_value):
        ''' Adds the tag to the dictionary in 4 forms:
                As is, lower case, no spaces, lower case + no spaces
        '''
        
        tag_dict[tag_name] = tag_value
        tag_dict[tag_name + TAG_SUFFIX_LOWER_CASE] = tag_value.lower()
        
        tag_value_no_spaces = tag_value.replace (' ', '')
        tag_dict[tag_name + TAG_SUFFIX_NO_SPACES] = tag_value_no_spaces
        tag_dict[tag_name + TAG_SUFFIX_LOWER_CASE + TAG_SUFFIX_NO_SPACES] = tag_value_no_spaces.lower()
        
    def _set_defaults(self, tag_dict):
        ''' Sets default tags:
                todays date.
        '''
        
        if not TAG_DATE in tag_dict:
            self.tag_dict[TAG_DATE] = self._to_date_string (date.today())
        
        
    def _set_calculated_defaults (self, tag_dict):
        ''' Sets calculated defaults base on existing values:
                from name, first date
        '''
        
        if TAG_NAME in tag_dict:
            
            self._add_tag_lower_case_no_space (tag_dict, TAG_NAME, tag_dict[TAG_NAME])
        
        if TAG_FIRST_DATE in tag_dict:
            
            now_date = dateutils.to_date_from_string (tag_dict[TAG_DATE])
            first_date = dateutils.to_date_from_string (tag_dict[TAG_FIRST_DATE])
        
            week_number = dateutils.week_number (first_date, now_date)
            week_number_string = str (week_number)
            week_start_date = dateutils.week_start_date (first_date, week_number)
            week_end_date = dateutils.week_end_date (week_start_date)
            
            tag_dict[TAG_WEEK_NUMBER] = week_number_string
            tag_dict[TAG_WEEK_NUMBER_PADDED] = week_number_string.rjust (3, '0')
            tag_dict[TAG_WEEK_START_DATE] = dateutils.to_date_string (week_start_date)
            tag_dict[TAG_WEEK_END_DATE] = dateutils.to_date_string (week_end_date)
            
            week_next_number_string = str (week_number + 1)
            week_next_start_date = dateutils.week_start_date (first_date, week_number + 1)
            week_next_end_date = dateutils.week_end_date (week_next_start_date)

            tag_dict[TAG_WEEK_NEXT_NUMBER] = week_next_number_string
            tag_dict[TAG_WEEK_NEXT_NUMBER_PADDED] = week_next_number_string.rjust (3, '0')
            tag_dict[TAG_WEEK_NEXT_START_DATE] = dateutils.to_date_string (week_next_start_date)
            tag_dict[TAG_WEEK_NEXT_END_DATE] = dateutils.to_date_string (week_next_end_date)

            biweek_number = int (week_number / 2)
            biweek_number_string = str (biweek_number)
            tag_dict[TAG_BIWEEK_NUMBER] = biweek_number_string
            tag_dict[TAG_BIWEEK_NUMBER_PADDED] = biweek_number_string.rjust (3, '0')
