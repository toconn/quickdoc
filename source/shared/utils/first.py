class IsFirst:

    def __init__(self):

        self._first = True

    def is_first(self):
        
        if not self._first:
            return False

        self._first = False
        return True

    def is_not_first(self):

        return not self.is_first()
