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

dbc = client.mongo2.review_2  # ...


# Query database - get data in ascendiong date.
# print results with limit on to see them
cursor = dbc.find({"business_id": "zTCCbg7mGslxACL5KlAPIQ"}).sort("date", 1)#.limit(20)

# print cursor.count()
# 987 reviews.



"""

Data Schema:

[[Month #, #negatives, #neutrals, #positives],
...]

"""


# Pre initialize data


month = 0
positives = 0
negatives = 0
neutrals = 0
mnstr = "0123456"
		
revStatsData = []

neednlp = []


for i in cursor:
	# print str([i["date"][0:7], i["sentiment"]["score"]])
	if i["date"][0:7] == mnstr:
		try:
			if float(i["sentiment"]["score"]) >= 0.3:
					positives = positives + 1
			elif float(i["sentiment"]["score"]) <= -0.3:
				negatives = negatives + 1
			else:
				neutrals = neutrals + 1
		except KeyError:
			neednlp.append(i["review_id"])
		
		
			
	else:
		# Debugging: 
		# print "New Month!"
		# print i["date"][0:7]
		# print mnstr
		
		if month != 0:
			revStatsData.append([month, negatives, neutrals, positives, mnstr])
		
		mnstr = i["date"][0:7]
		month += 1
		positives = 0
		negatives = 0
		neutrals = 0
		try:
			if float(i["sentiment"]["score"]) >= 0.3:
					positives = positives + 1
			elif float(i["sentiment"]["score"]) <= -0.3:
				negatives = negatives + 1
			else:
				neutrals = neutrals + 1
		except KeyError:
			neednlp.append(i["review_id"])
revStatsData.append([month, negatives, neutrals, positives, mnstr])
			
print revStatsData

"""
results:

[[1, 2, 15, 1], [2, 5, 18, 2], [3, 2, 10, 2], [4, 2, 8, 6], [5, 3, 10, 3], [6, 3, 8, 12], [7, 5, 7, 5], [8, 2, 12, 6], [9, 5, 15, 3], [10, 3, 7, 4], [11, 3, 9, 2], [12, 5, 6, 5], [13, 3, 8, 5], [14, 5, 7, 2], [15, 1, 5, 7], [16, 3, 11, 9], [17, 1, 7, 3], [18, 1, 4, 6], [19, 4, 7, 7], [20, 4, 8, 6], [21, 0, 6, 5], [22, 2, 5, 4], [23, 1, 3, 2], [24, 1, 4, 5], [25, 2, 6, 2], [26, 4, 9, 8], [27, 1, 7, 3], [28, 3, 4, 7], [29, 4, 4, 3], [30, 1, 8, 5], [31, 3, 8, 2], [32, 8, 10, 4], [33, 3, 7, 5], [34, 1, 2, 7], [35, 3, 3, 6], [36, 1, 0, 3], [37, 0, 4, 5], [38, 4, 6, 8], [39, 1, 8, 9], [40, 2, 6, 3], [41, 4, 9, 3], [42, 4, 8, 3], [43, 1, 12, 8], [44, 4, 12, 2], [45, 6, 14, 5], [46, 5, 5, 3], [47, 4, 13, 7], [48, 1, 4, 10], [49, 0, 7, 10], [50, 1, 6, 4], [51, 1, 11, 10], [52, 4, 10, 6], [53, 5, 7, 5], [54, 3, 5, 4], [55, 2, 4, 10], [56, 4, 13, 11], [57, 1, 13, 14], [58, 4, 6, 6], [59, 6, 9, 6], [60, 5, 9, 8], [61, 2, 7, 2], [62, 3, 3, 0]]

"""


print len(neednlp)
print neednlp

# neednlp:
# [u'u-Gbz-uGIIKC0SN2MwXtLw', u'FyCc8g7LCVpU4BGCz-WUog']
		


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
