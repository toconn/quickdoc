import os

from ua.core.utils import strutils

from parser.parser_const import TYPE_TEXT
from parser.parser_const import TYPE_VAR
from parser.parser_const import VAR_TAG_PERCENT

class ParseItem:
    """ 
        Created with CodeCrank.io
    """

    def __init__ (self, type, value):

        self.type = type
        self.value = value
        
    def __eq__ (self, other):

        if isinstance(other, self.__class__):
            return self.type == other.type and self.value == other.value
        
        return NotImplemented

    def __repr__ (self):

        return "ParseItem [" + \
            "type=" + (self.type if self.type is not None else "[None]") + \
            ", value=" + (self.value if self.value is not None else "[None]") + \
            "]"


def as_var (value):
    ''' Return the value in %variable% form
    '''
    return VAR_TAG_PERCENT + value + VAR_TAG_PERCENT


def calc_actual_value (var_dict, value):
    ''' Calculate the actual value for the value passed in
        processing all internal variables.
        
        If not possible, the variable will be passed back as it was found.
    '''
    
    if has_var (value):
        
        # Decompose value:
        value_items = parse_variables (value)
        new_values = []
        
        # Calculate any variables:
        
        for item in value_items:
        
            if item.type == TYPE_VAR:
                
                if item.value in var_dict:
                    
                    item_value = var_dict[item.value]

                    if not has_var (item_value):
                        new_values.append (item_value)
                    else:
                        # The requested item contains a variable of it's own
                        # so add it back in as a variable
                        new_values.append (as_var (item.value))
                
                else:
                    
                    # Check the environment for a match:
                    
                    item_value = os.environ.get(item.value)
                    
                    if item_value:
                        # match found
                        new_values.append (item_value)
                    else:
                        # no match. Put back as it was.
                        new_values.append (as_var (item.value))
                
            else:
                
                new_values.append (item.value)

        if len (new_values) > 0:
            new_value = "".join (new_values)
        else:
            # no items found (some dependent variables are still undefined).
            # return original item
            new_value = value

    else:

        # This is straight text. Return as is.
        new_value = value
    
    return new_value


def has_var (value):
    ''' Returns True if this value contain a variable?
    '''
    if value:
        return VAR_TAG_PERCENT in value
    else:
        return False


def parse_variables (text):
    
    parse_items = []
    
    if VAR_TAG_PERCENT in text:
        
        item_start = 0              # Set to first character.
        item_next_type = TYPE_TEXT  # Will alternate between var and text.
        percent_indexes = strutils.find_match_indexes (text, VAR_TAG_PERCENT)
        
        # Loop through % items:
        
        for index in percent_indexes:
            
            if not _is_escaped_percent(text, index):
            
                if index != item_start:
                    
                    # print ("Item (" + str (item_start) + " - " + str (index - 1) + ")")
                    
                    value = text[item_start : index]
                    parse_items.append (ParseItem (item_next_type, value))
                    
                if item_next_type == TYPE_TEXT:
                    item_next_type = TYPE_VAR
                else:
                    item_next_type = TYPE_TEXT
                    
                item_start = index + 1
            
            # else:
                
                # An escaped %. Ignore.
            
        if item_start < len (text):

            value = text[item_start:]
            parse_items.append (ParseItem (TYPE_TEXT, value))

    else:

        parse_items.append (ParseItem (TYPE_TEXT, text))
     
    return parse_items


def remove_escapes (text):
    
    # return strutils.replace (text, '\\\\', '\\')
    return strutils.replace (text, '\\%', '%')


def replace_variables (variable_dict, text):

    for var, value in variable_dict.items():
        text = strutils.replace (text, as_var (var), value)
        
    return text


def update_variable_values (var_dict):
    ''' Loop through all tags in the dictionary
        and calculate values for any that are composite (have embedded variables/tags).
    '''

    for tag, value in var_dict.items():
        if has_var (value):
            new_value = calc_actual_value (var_dict, value)
            var_dict[tag] = new_value
    
    return var_dict    
    

def _is_escaped_percent (text, index):
    return not (index == 0 or (index > 0 and text[index -1 : index + 1] != '\\%'))
