import os

class Console:
    """ A full featured implementation of console functions using
        termios (POSIX based).
    """
    
    def __init__(self):
        
        self._last_line_len = 0     # The length of the last print to the current line.
        
    def clear_line(self):
        ''' Clear the current line. Works only when using 'print' and not with 'print_line'.
        '''

        if self._last_line_len > 0:
            print(" " * self._last_line_len, end='\r')
            self._reset_line_len()
            
    def clear_screen(self):
        
        os.system('cls' if os.name=='nt' else 'clear')
    
    def newline(self):
        
        print ('')
    
    def print(self, text):
        ''' Print on the current line. Do not move to next line.
        '''

        print (text, end='\r')
        self._last_line_len = len(text)
        
    def print_line(self, text = ""):
        ''' Print and move to new line.
        '''

        print (text)
        self._reset_line_len()
        
    def read_line(self):
        
        text = input()
        # self._reset_line_len()
        
        return text
    
    def read_key(self):

        import termios
        import sys, tty
        def _getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        return _getch()
    
    def read_key_value(self):
        
        return ord(self.read_key())
    
    def _reset_line_len(self):
        
        self._last_line_len = 0

