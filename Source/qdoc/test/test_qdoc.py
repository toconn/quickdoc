import unittest

from ua.core.errors.errors import InvalidConfigError
from ua.core.utils.os.ua_os_factory import create_ua_os

from app_const import DATE_FORMAT
from app_const import DATE_SEPARATOR
from qdoc.qdoc import QDoc
from qdoc.qdoc import SETTING_FILE_DIR
from qdoc.qdoc import SETTING_FILE_NAME
from qdoc.qdoc import TAG_PARAMS

class Test (unittest.TestCase):

    def setUp(self):
        
        self._qdoc = QDoc(DATE_FORMAT, DATE_SEPARATOR, None, create_ua_os(), False)
        self._test_tag_dict = {'tag1': 'tag 1 value', 'composite_tag_2': "%variable1%"}

    def test_calc_week_number_same_date(self):

        self._call_and_test_calc_week_number('2001-01-01', '2001-01-01', 1)

    def test_calc_week_number_next_week(self):

        self._call_and_test_calc_week_number('2001-01-01', '2001-01-08', 2)

    def test_calc_week_number_next_week_2(self):

        self._call_and_test_calc_week_number('2001-01-01', '2001-01-14', 2)

    def test_calc_week_next_number_next_week(self):

        self._call_and_test_calc_week_next_number('2001-01-01', '2001-01-08', 3)

    def test_get_params_from_dict_empty(self):

        self._call_and_test_get_params_from_dict ({}, [])

    def test_get_params_from_dict_2_items(self):

        self._call_and_test_get_params_from_dict ({TAG_PARAMS: 'Param1, Param2'}, ['Param1', 'Param2'])

    def test_validate_fail_all(self):

        self._call_and_test_validate ({}, True, [SETTING_FILE_DIR, SETTING_FILE_NAME])

    def test_validate_pass_all(self):

        self._call_and_test_validate ({SETTING_FILE_DIR: 'file dir', SETTING_FILE_NAME: 'file name'}, False, [])

    def _call_and_test_calc_week_number (self, start_date_string, end_date_string, expected):
        
        actual = self._qdoc._calc_week_number(start_date_string, end_date_string)
        self.assertEquals (expected, actual)

    def _call_and_test_calc_week_next_number (self, start_date_string, end_date_string, expected):
        
        actual = self._qdoc._calc_week_next_number(start_date_string, end_date_string)
        self.assertEquals (expected, actual)

    def _call_and_test_get_params_from_dict (self, def_tag_dict, expected):
        
        actual = self._qdoc._get_params_from_dict(def_tag_dict)
        self._test_string_list(actual, expected)

    def _call_and_test_validate (self, tag_dict, expected_exception, expected_error_sub_items):
        
        # Call:
        
        try:
            self._qdoc._validate_def(tag_dict)
            actual = None
            
        except InvalidConfigError as e:
            actual = e


        # Test results
            
        if expected_exception:
            
            if not actual:

                self.fail('Expected Invalid Config Error but none thrown!')
            
            else:
                
                self.assertEqual(len (expected_error_sub_items), len (actual.messages), 'Unexpected number of error messages returned.')
                
                for sub_item in expected_error_sub_items:
                    
                    item_found = False;
                    
                    for item in actual.messages:
                        if sub_item in item:
                            item_found = True
                            break
                        
                    if not item_found:
                        self.fail ('Missing error message. ' + sub_item + ' not found.')
        
        else:
            
            if actual:
                self.fail('Unexpected Invalid Config Error thrown: ' + actual.messages_as_string())

    
    def _test_string_list (self, actual, expected):
        
        self.assertEqual(len (expected), len (actual), 'List sizes are different.')
        
        for expected_item, actual_item in zip (expected, actual):
            self.assertEqual(expected_item, actual_item, 'List items don\'t match.')