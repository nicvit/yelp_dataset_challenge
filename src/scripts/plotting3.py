import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from pymongo import MongoClient

###############################################################################################
# Function that queries mongo

def get_results():
	client = MongoClient('localhost', 27017)
	if client is None:
		print "Couldn't connect!"
	else:
		print ("Connected.")

	# change dbc values to the ones appropriate for your setup.
	dbc = client.yelp.review_category  # ...
	
	# Query database - get data in ascending date.
	client.close()
	print "Disconnected."

	return list(dbc.find({"business_id": "zTCCbg7mGslxACL5KlAPIQ"}).sort("date", 1))


###############################################################################################
###############################################################################################
# Function that group reviews by month

def group_by_month(results):  # results must be a list of reviews
	months = {'01': [], '02': [], '03': [], '04': [], '05': [], '06': [],
						 '07': [], '08': [], '09': [], '10': [], '11': [], '12': []
						 } 
	
	for review in results:
		date_splitted = review['date'].split('-')
		months[date_splitted[1].encode('ascii','ignore')].append(review)

	return dict(months)

###############################################################################################


###############################################################################################
###############################################################################################
# Function to count review sentiment.score


def count_month_subtotals(grouped_by_month_dict):    # month_key EX.: '01' '03' '10' ...
		for month_reviews in grouped_by_month_dict
			print month_reviews
			exit()
			for review in month_reviews:
				print review
				exit()
				total = len(month_reviews)
				positives = 0
				negatives = 0
				neutrals = 0
	 
				if review['sentiment']['score'] >= 0.3:
					positives = positives + 1
				elif review['sentiment']['score'] <= -0.3:
					negatives = negatives + 1
				else:
					neutrals = neutrals + 1
				print total, positives, negatives, neutrals
		




if __name__ == '__main__':
	
	query_results = get_results()

	grouped_by_month = group_by_month(query_results)
	#print grouped_by_month['03']

	
	#month_03_list = grouped_by_month['03']
	#print month_03_list[0]['sentiment']['score']
	#print '----------------------------------------------- \n -----------------------------------'
	#print month_03_list[2]['sentiment']['score']
	
	count_month_subtotals(grouped_by_month)












	


	