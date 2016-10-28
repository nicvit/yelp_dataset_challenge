#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pymongo import MongoClient




client = MongoClient('localhost', 27017)
if client is None:
    print "Couldn't connect!"
else:
    print ("Connected.")



# change dbc values to the ones appropriate for your setup.

dbc = client.mongo2.review_2  # ...


# Query database - get data in ascendiong date.
# print results with limit on to see them
cursor = dbc.find({"review_id": u'u-Gbz-uGIIKC0SN2MwXtLw'})

for i in cursor:
	print i
	
	