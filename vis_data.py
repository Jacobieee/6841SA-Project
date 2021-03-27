import os
import matplotlib.pyplot as plt
import numpy as np
import time as t
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

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
    # print(num_log)

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
    # print(res[0][0])
    # get all the stopwords.
    words = stopwords.words('english')
    for w in ['!', ',', '.', '?', '-s', '-ly', '</s>', 's',
              '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l',
              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
              's', 'w', 'x', 'y', 'z']:
        words.append(w)

    log_words = []
    # get all the log information.
    for info in res:
        word = info[0].split(" ")
        log_words.extend(word)

    # filter the stopwords.
    filtered_info = [word for word in log_words if word not in words]
    for i in range(len(filtered_info)):
        # convert all the verbs to present tense.
        filtered_info[i] = WordNetLemmatizer().lemmatize(filtered_info[i], 'v')
        # print(filtered_info[i])
    # filtered_info = sorted(filtered_info, reverse=True)
    info_count = {}
    for info in filtered_info:
        if info not in info_count:
            info_count[info] = 1
        else:
            info_count[info] += 1
    # we get the top 10 frequent words.
    info_count = sorted(info_count.items(), key=lambda item: item[1], reverse=True)[:num_top_words]
    # print(info_count)
    fig, ax = plt.subplots()

    labels = []
    vals = []
    for info in info_count:
        labels.append(info[0])
        vals.append(info[1])

    def revlst(lst):
        lst.reverse()
        return lst

    pos = np.arange(len(labels))

    rects = ax.barh(pos, revlst(vals), align='center', height=0.5, tick_label=revlst(labels))
    ax.set_title("Top Frequent Words")

    ax.set_ylabel("Top Words")
    ax.set_xlabel("Frequency")
    plt.gcf().set_size_inches((12.8, 9.6))

    plt.savefig(path + "/imgs/topWords.png")


# start = t.time()
# vis_timeslots()
# vis_top_words()
# end = t.time()
# print(end-start)

