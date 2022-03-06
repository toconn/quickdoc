def either(value_1, value_2):
    if not value_1:
        return value_2
    return value_1


def iif(condition, true_value, false_value=None):
    '''This is a more readable replacement for python's built in inline
       if statement.
    '''
    if condition:
        return true_value
    return false_value


def iif_not(condition, true_value, false_value=None):
    '''This is readable reverse of the python's built in inline
       if statement.
    '''
    if condition:
        return false_value
    return true_value
