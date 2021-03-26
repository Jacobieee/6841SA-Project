import os
import matplotlib.pyplot as plt
import numpy as np
import time as t
import nltk

import db_handle as dh

path = os.getcwd()
num_top_words = 10


def vis_timeslots():
    get_time = "SELECT log_time FROM Keylogger"
    res = dh.SQLquery(get_time, ())

    labels = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
              '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    time = {}
    for label in labels:
        time[label] = 0

    for r in res:
        time[r[0][:2]] += 1

    num_log = []
    for number in time.values():
        num_log.append(number)
    print(num_log)

    x = np.arange(len(labels))
    width = 0.8

    fig, ax = plt.subplots()
    f = ax.bar(x - width/2, num_log, width, label=labels, align='edge')

    plt.gcf().set_size_inches((12.8, 9.6))
    ax.set_xlabel('timeslot')
    ax.set_ylabel('num_info logged')
    ax.set_title('number of information logged in each timeslot')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    plt.savefig(path + "/imgs/timeslots.png")


def vis_top_words():
    get_content = "SELECT Log_info FROM Keylogger"
    res = dh.SQLquery(get_content, ())


start = t.time()
vis_timeslots()
end = t.time()
print(end-start)

