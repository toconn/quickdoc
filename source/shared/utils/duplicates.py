class Duplicates:
    
    def __init__(self):
        self._items_by_name = {}
        self._duplicates_by_name = {}

    def __iter__(self):
        return iter(self._duplicates_by_name.values())
    
    def add (self, name, item):

        if self.not_duplicate(name):  
            self._add_new(name, item)
        else:
            self._add_duplicate(name, item)
    
    def duplicates(self):
        return self._duplicates_by_name
                
    def is_duplicate (self, name):
        return name in self._items_by_name

    def has_duplicates(self):
        return len(self._duplicates_by_name) > 0

    def no_duplicates(self):
        return not self.has_duplicates()

    def not_duplicate (self, name):
        return not self.is_duplicate(name)

    def _add_duplicate(self, name, item):

        if name not in self._duplicates_by_name:
            self._duplicates_by_name[name] = [self._items_by_name[name]]

        duplicate_items = self._duplicates_by_name[name]
        duplicate_items.append(item)

    def _add_new(self, name, item):
        self._items_by_name[name] = item

