from shared.utils.counters import AutoCounter
from shared.utils.data import *
from shared.errors import *


CANCEL = "c"
ITEM_NONE = -1
NUMBER_SEPARATER = ") "


class ListPicker:
    ''' Display a list of items to a user and get them to pick one.
    '''

    def __init__(self, console, number_separater = NUMBER_SEPARATER):

        self._console = console
        self._number_separater = number_separater

    def __repr__(self):

        return "ListPicker [" + \
            "]"

    def pick_item (self, string_list, default=ITEM_NONE, indent=2):
        ''' Displays the list of items. Asks the user to select one
            and returns the index of the selected item.
            
            It will return -1 if no item selected.
        '''
        
        # Print:
        
        indent_text = " " * indent
        counter = AutoCounter (start_value = 1)
        
        for item in string_list:
            self._console.print_line (indent_text + str (counter.next) + self._number_separater + item)
        self._console.print_line()

        # Select:

        index = ITEM_NONE
        
        while index == ITEM_NONE:
            
            self._console.print_line ("Please select one (c for cancel)")
            pick_text = self._console.read_line()
            
            if pick_text == "":
                
                if default != ITEM_NONE:
                    index = default
                    
            elif pick_text == CANCEL:
                
                raise UserRequestExit()
            
            elif datautils.is_int (pick_text):
                
                pick_value = int (pick_text)
                
                if pick_value < 1 or pick_value > len (string_list):
                    self._console.print_line ("Invalid value. Must be between 1 and " + str (len (string_list)) + ".")
                else:
                    index = pick_value - 1
                     
            else:
                self._console.print_line ("Invalid value.")
        
        return index

