#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from pymongo import MongoClient

"""
Access data from database and make a basic histogram plot.

"""


def get_results():
    client = MongoClient('localhost', 27017)
    if client is None:
        print "Couldn't connect!"
    else:
        print ("Connected.")

    # change dbc values to the ones appropriate for your setup.
    dbc = client.yelp.review_category  # ...

    # Query database - get data in ascendiong date.
    client.close()
    print "Disconnected."

    return dbc.find({"business_id": "zTCCbg7mGslxACL5KlAPIQ"}).sort("date", 1).limit(20)


def simple_plot(cursor):
    # print cursor.count()
    # 987 reviews.

    # print results with limit on to see them

    # intended for analysis - needs a way to handle day
    data = []

    # variables used for demonstration purposes.
    data_sent = []
    data_revN = []
    revN = 1
    for i in cursor:
        data.append([i["date"], i["sentiment"]["score"]])
        data_sent.append(i["sentiment"]["score"])
        data_revN.append(revN)
        revN += 1

    # sample plot - needs improvement

    plt.plot(data_revN, data_sent, 'g')

    plt.show()


def plot_daily_results(results):
    grouped_by_date = {}
    for item in results:
        if item['date'] not in grouped_by_date:
            grouped_by_date['date'] = item
            print(item)
        print(grouped_by_date)

    # matrix_needed = HERE DO CALCULATIONS TO CREATE THE MATRIX

    # plt.plot(matrix_needed, 'g')
    # plt.show()


if __name__ == '__main__':
    basic_result = get_results()
    # simple_plot(basic_result)
    plot_daily_results(basic_result)
