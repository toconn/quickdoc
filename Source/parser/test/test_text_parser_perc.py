import unittest

from parser import text_parser_perc
from parser.text_parser_perc import ParseItem
from parser.parser_const import TYPE_TEXT
from parser.parser_const import TYPE_VAR

class Test (unittest.TestCase):

    def setUp(self):
        
        self._test_tag_dict = {'tag1': 'tag 1 value', 'composite_tag_2': "%variable1%"}


    def test_calc_actual_value_text_only_1(self):

        self._call_and_test_calc_actual_value({}, 'text', 'text')


    def test_calc_actual_value_1_tag(self):

        self._call_and_test_calc_actual_value(self._test_tag_dict, '%tag1%', 'tag 1 value')


    def test_calc_actual_value_composite_tag(self):

        self._call_and_test_calc_actual_value(self._test_tag_dict, '%composite_tag_2%', '%composite_tag_2%')


    def test_calc_actual_value_tag_and_text(self):

        self._call_and_test_calc_actual_value(self._test_tag_dict, '%tag1% - text', 'tag 1 value - text')


    def test_calc_actual_value_text_and_tag(self):

        self._call_and_test_calc_actual_value(self._test_tag_dict, 'text - %tag1%', 'text - tag 1 value')


    def test_parse_percent_variables_simple_text(self):
        
        test_input = 'simple text'
        expected = [ParseItem (TYPE_TEXT, test_input)]

        self._call_and_test_parse_variables(test_input, expected)


    def test_parse_percent_variables_simple_variable(self):
        
        test_input = '%variable%'
        expected = [ParseItem (TYPE_VAR, 'variable')]

        self._call_and_test_parse_variables(test_input, expected)


    def test_parse_percent_variables_text_variable(self):
        
        test_input = 'text%variable%'
        expected = [ParseItem (TYPE_TEXT, 'text'), ParseItem (TYPE_VAR, 'variable')]

        self._call_and_test_parse_variables(test_input, expected)


    def test_parse_percent_variables_variable_text(self):
        
        test_input = '%variable%text'
        expected = [ParseItem (TYPE_VAR, 'variable'), ParseItem (TYPE_TEXT, 'text')]

        self._call_and_test_parse_variables(test_input, expected)


    def test_parse_percent_variables_2_variable(self):
        
        test_input = '%variable1%%variable2%'
        expected = [ParseItem (TYPE_VAR, 'variable1'), ParseItem (TYPE_VAR, 'variable2')]

        self._call_and_test_parse_variables(test_input, expected)


    def test_parse_percent_variables_mashup(self):
        
        test_input = 'text%variable1%%variable2%%variable3% text2 %variable4% text3'
        expected = [ParseItem (TYPE_TEXT, 'text'), ParseItem (TYPE_VAR, 'variable1'), ParseItem (TYPE_VAR, 'variable2'), ParseItem (TYPE_VAR, 'variable3'), ParseItem (TYPE_TEXT, ' text2 '), ParseItem (TYPE_VAR, 'variable4'), ParseItem (TYPE_TEXT, ' text3')]

        self._call_and_test_parse_variables(test_input, expected)


    def _call_and_test_calc_actual_value (self, tag_dict, value, expected):
        
        actual = text_parser_perc.calc_actual_value(tag_dict, value)
        self.assertEquals (expected, actual)


    def _call_and_test_parse_variables (self, test_input, expected):
        
        actual = text_parser_perc.parse_variables(test_input)
        self._compare_parse_lists (expected, actual)

        
    def _compare_parse_lists (self, expected, actual):
        
        self.assertEquals (len (expected), len (actual))
        
        for expected_item, actual_item in zip (expected, actual):
            self.assertEquals (expected_item, actual_item)