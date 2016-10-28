#!/usr/bin/env python
from __future__ import division
import numpy as np
import scipy.stats as stats
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from pymongo import MongoClient



data = [[1, 2, 15, 1, u'2009-12'], [2, 5, 18, 2, u'2010-01'], [3, 2, 10, 2, u'2010-02'], [4, 2, 8, 6, u'2010-03'], [5, 3, 10, 3, u'2010-04'], [6, 3, 8, 12, u'2010-05'], [7, 5, 7, 5, u'2010-06'], [8, 2, 12, 6, u'2010-07'], [9, 5, 15, 3, u'2010-08'], [10, 3, 7, 4, u'2010-09'], [11, 3, 9, 2, u'2010-10'], [12, 5, 6, 5, u'2010-11'], [13, 3, 8, 5, u'2010-12'], [14, 5, 7, 2, u'2011-01'], [15, 1, 5, 7, u'2011-02'], [16, 3, 11, 9, u'2011-03'], [17, 1, 7, 3, u'2011-04'], [18, 1, 4, 6, u'2011-05'], [19, 4, 7, 7, u'2011-06'], [20, 4, 8, 6, u'2011-07'], [21, 0, 6, 5, u'2011-08'], [22, 2, 5, 4, u'2011-09'], [23, 1, 3, 2, u'2011-10'], [24, 1, 4, 5, u'2011-11'], [25, 2, 6, 2, u'2011-12'], [26, 4, 9, 8, u'2012-01'], [27, 1, 7, 3, u'2012-02'], [28, 3, 4, 7, u'2012-03'], [29, 4, 4, 3, u'2012-04'], [30, 1, 8, 5, u'2012-05'], [31, 3, 8, 2, u'2012-06'], [32, 8, 10, 4, u'2012-07'], [33, 3, 7, 5, u'2012-08'], [34, 1, 2, 7, u'2012-09'], [35, 3, 3, 6, u'2012-10'], [36, 1, 0, 3, u'2012-11'], [37, 0, 4, 5, u'2012-12'], [38, 4, 6, 8, u'2013-01'], [39, 1, 8, 9, u'2013-02'], [40, 2, 6, 3, u'2013-03'], [41, 4, 9, 3, u'2013-04'], [42, 4, 8, 3, u'2013-05'], [43, 1, 12, 8, u'2013-06'], [44, 4, 12, 2, u'2013-07'], [45, 6, 14, 5, u'2013-08'], [46, 5, 5, 3, u'2013-09'], [47, 4, 13, 7, u'2013-10'], [48, 1, 4, 10, u'2013-11'], [49, 0, 7, 10, u'2013-12'], [50, 1, 6, 4, u'2014-01'], [51, 1, 11, 10, u'2014-02'], [52, 4, 10, 6, u'2014-03'], [53, 5, 7, 5, u'2014-04'], [54, 3, 5, 4, u'2014-05'], [55, 2, 4, 10, u'2014-06'], [56, 4, 13, 11, u'2014-07'], [57, 1, 13, 14, u'2014-08'], [58, 4, 6, 6, u'2014-09'], [59, 6, 9, 6, u'2014-10'], [60, 5, 9, 8, u'2014-11'], [61, 2, 7, 2, u'2014-12'], [62, 3, 3, 0, u'2015-01']]
data=data[0:len(data)-1]
months = []
negratio = []


for i in data:
	months.append(i[0])
	negratio.append(i[1]/(i[1]+i[2]+i[3]))
	
testnormal = stats.normaltest(negratio)
print testnormal
	
negMean = np.mean(negratio)
negStd = np.std(negratio)


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

print data[28] # [46, 5, 5, 3, u'2013-09']
print data[31] # [29, 4, 4, 3, u'2012-04']
print data[45] # [32, 8, 10, 4, u'2012-07']

plt.plot(months, negratio, 'g')
plt.axhline(y = (negMean + 2 * negStd), linewidth=1, color = 'r')
plt.axhline(y = (negMean), linewidth=1, color = 'm') # , xmin=0.25, xmax=0.402

plt.show()







