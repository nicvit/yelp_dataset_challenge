__author__ = 'Adisorn'

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'FoDS')))

from yelp.data.collection import *

DATABASE_NAME = 'yelp'
BUS_ID = 'KjymOs12Mpy0Kd54b7T9MA'

class AchelmyStore:

    def __init__(self):
        self.__dbConnector = DBConnector(os.path.join(CONFIG_PATH, 'config.json'), )
        self.__dbConnector.connect()
        self.__db = self.__dbConnector.get_database_name(DATABASE_NAME, 'achelmy_calls')
        self.__client = self.__dbConnector.get_client()

    def get_uncalled_ids(self, business_id='', n=200, mode=0):# mode 0 = sentiment, 1 = combined
        db = self.__client[DATABASE_NAME]
        collection = db['review_category']

        achelmy_collection_name = 'achelmy_combined_calls' if mode == 0 else 'achelmy_calls'
        achelmy_collection = db[achelmy_collection_name]
        called_review_result = achelmy_collection.find_one({'business_id': business_id})

        review_ids = []
        if called_review_result is not None:
            review_ids.extend(called_review_result['reviews'])

        print("called ids: {} objects".format(len(review_ids)))

        #list(db.users.find({"document_up.tags":{"$nin":["solide"]}}))
        query = dict()
        query['business_id'] = business_id
        query['review_id'] = {'$nin': review_ids}

        projection = dict()
        projection['review_id'] = 1

        uncalled_result = collection.find(query, projection)
        i = 0
        res = []
        for review in uncalled_result:
            #print(review['review_id'])
            res.append(review['review_id'])
            i += 1
            if i == n:
                break

        print("get: {} unique objects".format(len(res)))
        return res

    def get_uncalled_sentiment_review_ids(self, business_id='', n=200):
        return self.get_uncalled_ids(business_id, n, 0)

    def get_uncalled_combined_review_ids(self, business_id='', n=200):
        return self.get_uncalled_ids(business_id, n, 1)

    def add_called_review_ids(self, business_id='', called_ids=[]):
        db = self.__client[DATABASE_NAME]
        collection = db['achelmy_calls']

        query = dict()
        query['business_id'] = business_id
        doc = collection.find_one(query)

        if doc is None:
            dct = dict()
            dct['business_id'] = business_id
            dct['reviews'] = called_ids

            collection.insert(dct)
        else:
            called_reviews = doc['reviews']
            ids_set = set()
            all_reviews = []
            all_reviews.extend(called_reviews)
            all_reviews.extend(called_ids)
            for review_id in all_reviews:
                ids_set.add(review_id)

            update_dict = dict()
            update_dict['reviews'] = list(ids_set)
            collection.find_one_and_update(
                filter={'business_id': business_id},
                update={'$set': update_dict},
                return_document=ReturnDocument.AFTER)

            #print("set: {} objects".format(len(ids_set)))

if __name__ == '__main__':
    acm = AchelmyStore()
    res = acm.get_uncalled_review_ids(BUS_ID, 200)
    acm.add_called_review_ids(BUS_ID, res)
