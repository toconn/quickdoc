def is_comment (text):
    if not text:
        return False
    else:
        return text.startswith ("#") or text.startswith ("//")

def is_int (text):
    
    try:
        int(text)
        return True
    except ValueError:
        return False

def not_comment (text):
    return not is_comment (text)


