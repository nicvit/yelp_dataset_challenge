#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pymongo import MongoClient
import scipy.stats as stats



client = MongoClient('localhost', 27017)
if client is None:
    print "Couldn't connect!"
else:
    print ("Connected.")



# change dbc values to the ones appropriate for your setup.

dbc = client.mongo2.review_3  # ...


# Query database - get data in ascendiong date.
# print results with limit on to see them
cursor = dbc.find({"business_id": "zTCCbg7mGslxACL5KlAPIQ"}).sort("date", 1)#.limit(20)
# print cursor.count()
list1 = list(cursor)

keywordData = []
keywordList = set()

reviewCluster = range(312,332,1)

for iter in reviewCluster:
	crev = list1[iter]
	keywl = crev["combined_result"]["keywords"]
	for it1 in keywl:
		keywordList.add(it1["text"])
		
keywordList = list(keywordList)
print keywordList	
print len(keywordList)


"""
Strategy:

sample all keywords with less than -0.3 sentiment
[["keyword1", [sen#1, sen#2, ...]], ["keyword2", [sen#1, sen#2, ...]], ...]

{"keyword1": [sen#1, sen#2, ...]}

find average and standard deviation for those keywords
[["keyword1", avg, std], ["keyword2", avg, std], ...]

perform a normality test !?
[["keyword1", avg, std, [sen#1, sen#2, ...], pvalue]]


# 312 th review + 20

Implementation:

set([u'Mandalay Bay', u'bad place', u'Aria Buffet', u'selection', u'major property features', u'money', u'fond', u'Buffets', u'rest', u'better buffets', u'iced tea', u'manager', u'salad items', u'thanks', u'scale Cafe Lago', u'Circus Circus category', u'Bellagio', u'brunch', u'issues', u'Good thing', u'Tandoor Oven', u'Eggs Benedict', u'group', u'major disappointment', u'Times brakfast Lunch', u'4PM', u'Buffet', u'SHRIMP', u'resort credits', u'desert section', u'smile', u'BACON', u'plate', u'complaint', u'return', u'DESSERT BAR', u'food', u'stop', u'best rated buffets', u'little bit', u'chicken noodle soup', u'lunch', u'Dinner', u'vegas', u'dessert section', u'half', u'Gelato', u'OK', u'pies', u'creepy kind', u'crabs', u'Aria buffet', u'street vendor', u'course', u'brunch buffet', u'memorable item', u'Sunday', u'buffet quality', u'try', u'Desserts', u'split crab legs', u'night', u'sick right', u'lone exception', u'king crab legs', u'restaurants', u'cookies', u'eggs Benedict', u'crowd', u'Dinner price', u'sorbet', u'Lovely hotel', u'lobster', u'star', u'rocks', u'salads', u'BREAKFAST BURRITO', u'garlic naan bread', u'new hotel', u'hesitation', u'big draw', u'item', u'a-little dry.', u'cheaper buffets', u'gratuity', u'fresh clean', u'quality', u'best way', u'eating', u'bus boys', u'price', u'red', u'tandoori chicken', u'ginormous peeled shrimp', u'omg', u'sarcastic comment', u'Rio seafood buffet', u'Chinese red vinegar', u'Life venue', u'reason', u'las Vegas', u'itsy bitsy spiders', u'unlimited wine', u'Chinese accent', u'plates', u'Selection', u'CRAB LEGS', u'selections', u'row', u'lobster lol', u'chicken soup', u'giant crab lover', u'thing', u'dinner', u'Aria Aria', u'place', u'dessert counter', u'clothes', u'sweetness', u'weekends', u'waitress', u'1-3 stars', u'dessert macaroons', u'great hotel', u'desserts', u'heart', u'buffets', u'peanut butter blondies', u'soft cookies', u'lobster/unlimited wine night', u'Wynn', u'Las Vegas buffet', u'salmon was.. well..', u'motto', u'Wicked Spoon Buffet', u'brownies', u'service', u'sake', u'vegetables', u'high hopes', u'dud', u'horrible service', u'entire time', u'Good Price', u'Vegas', u'good biscuits', u'treat', u'stars', u'white', u'sushi', u'stomach', u'wine dinner', u'good sign', u'high chair', u'cocktail shrimp', u'carbs', u'hmm', u'Bellagio buffet', u'sweets', u'line', u'great ambiance', u'Waitress', u'holy crap', u'30- 7pm', u'crab legs', u'target', u'small selection', u'breakfast choices', u'extravagant buffet', u'complete stranger', u'Wonderful wait team', u'hummus', u'fruits', u'large group', u'open crab legs', u'girls trip', u'long break', u'palate', u'Good Food', u'entire property', u'oddball food options', u'Aria', u'tax', u'shame', u'beats', u'different dishes', u'lobster tail', u'cook', u'bucks', u'Family reunion', u'cream', u'best breakfast biscuits', u'wide selection', u'5-6 flavors', u'Cosmopolitan', u'variety', u'things', u'Price', u'Garlic nan', u'tip', u'repeat visit', u'carafes', u'setting', u'high end buffets', u'snow crabs', u'freakin macaroon cookie', u'crisp coleslaw', u'Saturday night', u'pretty strict diet', u'gravy', u'big Disappointment', u'kinds', u'bottle', u'Best Buffet', u'eggs', u'prime rib', u'spot', u'breakfast buffet', u'buffet', u'stay', u'chance', u'nights', u'mouth', u'quality food', u'plenty', u'friends', u'banana cream pie', u'lunch food', u'gourmet', u'Sunday Brunch', u'potato', u'average', u'Bad', u'deal', u'person', u'huge issue', u'normal dinner', u'time', u'Staff', u'amazing rooms', u'chocolate brownies', u'wine'])
__


{"keyword" : {	"overall_sentiment": []
				"avg": ,  
				"std": , 
				"cluster_sentiment":[],
				"pValue":			
			}
"""