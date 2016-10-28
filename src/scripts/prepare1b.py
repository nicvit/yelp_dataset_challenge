#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from pymongo import MongoClient


"""
Access data from database and make a basic histogram plot.

"""




client = MongoClient('localhost', 27017)
if client is None:
    print "Couldn't connect!"
else:
    print ("Connected.")



# change dbc values to the ones appropriate for your setup.

dbc = client.mongo2.review_1  # ...


# Query database - get data in ascendiong date.
cursor = dbc.find({"business_id": "zTCCbg7mGslxACL5KlAPIQ"}).sort("date", -1).limit(20)

# print cursor.count()
# 987 reviews.



# print results with limit on to see them

for i in cursor:
	print str([i["date"], i["sentiment"]["score"]])


# variables to used to plot/analyse data

# # intended for analysis - needs a way to handle day
# data = []

# # variables used for demonstration purposes.
# data_sent = []
# data_revN = []
# revN = 1

# for i in cursor:
	# data.append([i["date"], i["sentiment"]["score"]])
	# data_sent.append(i["sentiment"]["score"])
	# data_revN.append(revN)
	# revN +=1


	
	
# sample plot - needs improvement

# plt.plot(data_revN, data_sent, 'g')

# plt.show()


client.close()
print "Disconnected."
