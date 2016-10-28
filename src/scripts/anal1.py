#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pymongo import MongoClient
import scipy.stats as stats
from pprint import pprint


# Query a given business_id and identify problematic review clusters!

client = MongoClient('localhost', 27017)
if client is None:
    print "Couldn't connect!"
else:
    print ("Connected.")

# change dbc values to the ones appropriate for your setup.

dbc = client.mongo2.reviews  # ...
dbc2 = client.mongo2.users  # ...



"""

{u'count': 987, u'_id': u'zTCCbg7mGslxACL5KlAPIQ'}
{u'count': 981, u'_id': u'KjymOs12Mpy0Kd54b7T9MA'}
{u'count': 980, u'_id': u'5GKbGn9-fAgQ0njSh3OJ8A'}
{u'count': 969, u'_id': u'RhbOa-Ft3sZB4B_1j5LfyA'}
{u'count': 967, u'_id': u'WNy1uzcmm_UHmTyR--o5IA'}
{u'count': 948, u'_id': u'HyfFenprdpIA4rmKu6DW3g'}
{u'count': 946, u'_id': u'eLPld7Q17XxlclFGzZQX5g'}
{u'count': 942, u'_id': u'YacTpiq0ZptFcXD7I-kdGA'}
{u'count': 934, u'_id': u'SDwYQ6eSu1htn8vHWv128g'}
{u'count': 931, u'_id': u'LLDGTT7FExklkQvHebEjRg'}
{u'count': 921, u'_id': u'AeKTQBtPRDHLAFL9bzbUnA'}
{u'count': 915, u'_id': u'1yx2zLskVTe5WQdYjL2Apw'}
{u'count': 881, u'_id': u'BqD7X5CHXnJ14YbBBlLx1w'}
{u'count': 865, u'_id': u'aRkYtXfmEKYG-eTDf_qUsw'}
{u'count': 865, u'_id': u'-sC66z4SO3tR7nFCjfQwuQ'}
{u'count': 851, u'_id': u'H_SuH7uLiYahDMbNBB9kog'}
{u'count': 845, u'_id': u'Pz7SWZQhxL6ZbhL9jE2NTA'}
{u'count': 841, u'_id': u'YKOvlBNkF4KpUP9q7x862w'}
{u'count': 836, u'_id': u'vSf0pqvaLp5sVSjJPeOqqQ'}
{u'count': 826, u'_id': u'QnAzW6KMSciUcuJ20oI3Bw'}

"""
# change business_id to the one you are working on.
business_id = "5GKbGn9-fAgQ0njSh3OJ8A"

# Query database - get data in ascendiong date.
# change business_id to the one you are working on.
cursor = dbc.find({"business_id": business_id}).sort("date", 1)# .limit(20)
revlist = list(cursor)

sentiment = []

for i in revlist:
	if "sentiment" in i:
		if i["sentiment"]["type"] == u'neutral':
			sentiment.append(0)
		else:
			ia = float(i["sentiment"]["score"])
			ia = round(ia, 2)
			sentiment.append(ia)

# print sentiment


senMean = np.mean(sentiment)
senStd = np.std(sentiment)

sentiment[:] = [round(x - senMean, 2) for x in sentiment]
sentiment[:] = [round(x / senStd, 2) for x in sentiment]

# print np.mean(sentiment)
# should be 0 but is ~0.01 because of numerical error !!


notNormal = []
iter = range(0, len(sentiment) - 21, 1)

for it in iter:
    a1 = stats.normaltest(sentiment[it:(it + 20)])
    if a1[1] < 0.05:
        itavg = round(np.mean(sentiment[it:(it + 20)]),2)
        itadd = [it, itavg]
        notNormal.append(itadd)

# print notNormal


# client.close()
# print "Disconnected."
# Doesn't work - you can query after this and get results !

	
for cluster in notNormal:
	review1 = cluster[0]
	review_range = range(review1, review1 + 20, 1)
	usfs = 0
	for it in review_range:
		review = revlist[it]
		userid = review["user_id"]
		
		user = dbc2.find_one({"user_id":userid}, {"average_usefulness":1})
		usfs += float(user["average_usefulness"])
		
	cluster.append(round(usfs, 2))
	
	
with open('./anal1_3.txt', 'w+') as outfile:
	pprint(notNormal, stream=outfile)
