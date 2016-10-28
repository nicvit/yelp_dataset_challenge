#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pymongo import MongoClient
import scipy.stats as stats
from pprint import pprint


# Identify keywords(themes) in the reviews that are statistically significant negative

client = MongoClient('localhost', 27017)
if client is None:
    print "Couldn't connect!"
else:
    print ("Connected.")



# change dbc values to the ones appropriate for your setup.
dbc = client.mongo2.reviews  # ...

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
business_id = "zTCCbg7mGslxACL5KlAPIQ"

# Query database - get data in ascendiong date.
cursor = list(dbc.find({"business_id": business_id}).sort("date", 1))#.limit(20)

iter = range(0,len(cursor)-1)
keywordData = {}

# hardcode reviewCluster from results of anal1 + user feedback
reviewIdent = [309, 753]
file_counter = range(0,len(reviewIdent))



# create document of keywords and relevant statistics
"""
data schema:
{"keyword" : {	"overall_sentiment": []
				"avg": ,  
				"std": , 
				"cluster_sentiment":[],
				"pValue":			
			}
"""

for counter in file_counter:
	
	reviewCluster = range(reviewIdent[counter],reviewIdent[counter] + 20)
	for it in iter:
		if "combined_result" in cursor[it]:
			keywl = cursor[it]["combined_result"]["keywords"]
			for it1 in keywl:
				if it1["text"] not in keywordData:
					keywordData[it1["text"]] = {}
					keywordData[it1["text"]]["overall_sentiment"] = []
				
				if "sentiment" in it1:
					if it1["sentiment"]["type"] == u'neutral':
							keywordData[it1["text"]]["overall_sentiment"].append(0)
					else:
						ia = float(it1["sentiment"]["score"])
						ia = round(ia, 2)
						keywordData[it1["text"]]["overall_sentiment"].append(ia)
					
				if it in reviewCluster:
					if "cluster_sentiment" not in keywordData[it1["text"]]:
						keywordData[it1["text"]]["cluster_sentiment"] = []
					
					if "sentiment" in it1:
						if it1["sentiment"]["type"] == u'neutral':
								keywordData[it1["text"]]["cluster_sentiment"].append(0)
						else:
							ia = float(it1["sentiment"]["score"])
							ia = round(ia, 2)
							keywordData[it1["text"]]["cluster_sentiment"].append(ia)
				
			
	# print(keywordData)


	# keep only negative stastistically significant keywords
	unwanted_keys = set()
	for keyword, value in keywordData.items():
		if "cluster_sentiment" in value:
			avg = round(np.mean(value["overall_sentiment"]), 2)
			std = round(np.std(value["overall_sentiment"]), 2)
			value["avg"] = avg
			value["std"] = std
			if std == 0.0:
				unwanted_keys.add(keyword)
				continue
			
			savg = round(np.mean(value["cluster_sentiment"]), 2)
			value["savg"] = savg
			
			minVal = avg - (2*std)
			maxVal = avg + (2*std)
			if (savg > minVal and savg < maxVal) or savg > 0:
				unwanted_keys.add(keyword)
				
		else:
			unwanted_keys.add(keyword)
			
	for key in unwanted_keys:
		del keywordData[key]
	
	filename = "./anal2_1_" + str(counter+1) + ".txt"
	with open(filename, 'w+') as outfile:
		pprint(business_id, stream=outfile)
		pprint(str(reviewCluster), stream=outfile)
		pprint(keywordData, stream=outfile)

client.close()
print "Disconnected."