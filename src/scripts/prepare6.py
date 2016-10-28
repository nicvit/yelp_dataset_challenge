#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pymongo import MongoClient
import scipy.stats as stats


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

[[Month #, "month_string", sent1,sent2, ...], 
... ]

"""


# Pre initialize data


month = 0
mnstr = "0123456"
		
revStatsData = []
sentiment = []

for i in cursor:
	# print str([i["date"][0:7], i["sentiment"]["score"]])
	if i["date"][0:7] == mnstr:
		if i["sentiment"]["type"] == u'neutral':
			sentiment.append(0)
		else:
			ia = float(i["sentiment"]["score"])
			ia = round(ia, 2)
			sentiment.append(ia)		
			
	else:
		# Debugging: 
		# print "New Month!"
		# print i["date"][0:7]
		# print mnstr
		
		if month != 0:
			revStatsData.append([month, mnstr, sentiment])
		
		mnstr = i["date"][0:7]
		month += 1
		sentiment =[]
		
		if i["sentiment"]["type"] == u'neutral':
			sentiment.append(0)
		else:
			ia = float(i["sentiment"]["score"])
			ia = round(ia, 2)
			sentiment.append(ia)
revStatsData.append([month, mnstr, sentiment])
			
print revStatsData

monthAvg = []

for it in revStatsData:
	monthAvg.append(round(np.mean(it[2]),2))


# sample plot - needs improvement

plt.plot(monthAvg, 'g')

plt.show()


client.close()
print "Disconnected."
