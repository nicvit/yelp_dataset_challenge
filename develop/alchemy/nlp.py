import os
import sys
import logging
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'FoDS')))

from datetime import datetime
from api import AlchemyAPI
from yelp.data.collection import MongoQuery
from yelp.data.collection import DBConnector
from yelp.alchemy.nlp_exc.exception import NLPValueError
from yelp.alchemy.AchelmyDataStore import AchelmyStore

from pprint import pprint
# from Logger import LogBroadcaster

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))

BUS_ID = 'KjymOs12Mpy0Kd54b7T9MA'

class NLPHandler(object):
    def __init__(self):
        self.alchemy_api = AlchemyAPI()
        self.query = MongoQuery()
        self.collection_name = 'review_category'
        self.max_reviews_per_business = 1000
        self.top_businesses_limit = 10
        self.logger = logging.Logger('NLPLogger', level=logging.INFO)
        self.logger.addHandler(logging.FileHandler(filename=os.path.join(LOG_PATH, 'nlp.log'), mode='a+'))
        self.__broadcaster = None

    def set_broadcaster(self, b):
        self.__broadcaster = b
        #self.__broadcaster.broadcast_message("Test log...")

    def get_combined_result(self, review_text=''):
        opts = {
            'sentiment': 1
        }
        response = self.alchemy_api.combined('text', review_text, options=opts)

        if response['status'] == 'OK':
            return response
        else:
            raise NLPValueError('Error in combined call: ' + response['statusInfo'])

    def get_sentiment_result(self, review_text=''):
        response = self.alchemy_api.sentiment('text', review_text)
        if response['status'] == 'OK':
            return response
        else:
            raise NLPValueError('Error in sentiment analysis call: ' + response['statusInfo'])

    def create_mixed_collection(self):
        db_connector = DBConnector(os.path.join(CONFIG_PATH, 'config.json'))
        db_connector.connect()
        db_connector.reset_database_name('yelp', 'review_category')
        t_collection = db_connector.get_database_name('yelp', 'review_category')

        business_fields = ['business_id', 'categories']
        user_fields = ['user_id', 'elite', 'votes']
        review_fields = ['business_id', 'review_id', 'text', 'user_id', 'stars', 'date']

        col_name = 'review'
        documents = self.query.find_all(col_name, review_fields)

        index = 0
        batch_number = 5000

        batch_documents = [i for i in range(batch_number)]

        for review_doc in documents:
            try:
                business_id = review_doc['business_id']
                review_id = review_doc['review_id']
                text = review_doc['text']
                user_id = review_doc['user_id']
                stars = review_doc['stars']
                date = review_doc['date']

                business_doc = self.query.find_one('business', [('business_id', business_id)], business_fields)
                categories = business_doc['categories']

                user_doc = self.query.find_one('user', [('user_id', user_id)], user_fields)
                elite = len(user_doc['elite'])
                useful = user_doc['votes']['useful']

                new_doc = {
                    'review_id': review_id,
                    'business_id': business_id,
                    'user_id': user_id,
                    'elite': elite,
                    'useful': useful,
                    'categories': categories,
                    'text': text,
                    'stars': stars,
                    'date': date,
                }

                batch_documents[index % batch_number] = new_doc

                if (index + 1) % batch_number == 0:
                    t_collection.insert(batch_documents)
                    print("\n" + str(index + 1) + "\n")
                index += 1
            except:
                print 'Unexpected error:', sys.exc_info()[0], ', for index ', index
                raise
        db_connector.disconnect()

    def find_top_category(self):
        pipeline = [
            {"$unwind": "$categories"},
            {"$group": {"_id": "$categories", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        return self.query.aggregate(self.collection_name, pipeline, True)[0]['_id']

    def find_top_businesses_of_category(self, category, top_businesses=10):
        pipeline = [
            {"$unwind": "$categories"},
            {"$match": {"categories": category}},
            {"$group": {"_id": "$business_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$match": {"count": {"$lte": self.max_reviews_per_business}}},
            {"$limit": top_businesses}
        ]
        return self.query.aggregate(self.collection_name, pipeline, True)

    def update_mixed_collection_with_sentiment(self, business_doc):
        counter = 0

        query_list = [('business_id', business_doc['_id'])]
        field_list = ['review_id', 'text', 'sentiment']

        reviews = list(
                self.query.find_all_by(self.collection_name, query_list, field_list)
        )

        for review in reviews:
            if 'sentiment' not in review:
                review_id = review['review_id']
                sentiment = None
                try:
                    sentiment = self.get_sentiment_result(review['text'])['docSentiment']
                except NLPValueError as err:
                    print("{} is having problem with err: {}".format(review_id, err.message))

                if sentiment != None:
                    query_list = [('review_id', review_id)]
                    set_list = [('sentiment', sentiment)]

                    self.query.find_and_update(self.collection_name, query_list, set_list)

                    counter += 1
                    if counter % 50 == 0:
                        print(str(counter) + " reviews updated.")

    def print_uncalled_top_ten_business(self):
        top_category = self.find_top_category()
        top_ten_business_id_docs = self.find_top_businesses_of_category(top_category, self.top_businesses_limit)

        count = 0
        for business in top_ten_business_id_docs:
            query_list = [('business_id', business['_id'])]
            field_list = ['sentiment']

            reviews = list(
                    self.query.find_all_by(self.collection_name, query_list, field_list)
            )

            for review in reviews:
                if 'sentiment' not in review:
                    count += 1

            print(str(count) + " reviews not updated for business " + str(business['_id']))
            count = 0

    # CAREFUL WITH THIS ONE!!! IT HAS MEMORY ISSUES - RUN IT MANY TIMES AND CLEAR CACHE OF PC EVERYTIME
    # IF IT TAKES TOO MUCH TIME, IT NEEDS INDEX
    def update_mixed_collection_with_review_votes(self):
        counter = 0

        review_fields = ['votes']
        review_category_fields = ['review_id']
        review_category_query = [('review_useful', {"$exists": False})]

        review_categories = list(
                self.query.find_all_by(self.collection_name, review_category_query, review_category_fields)
        )

        for review_category in review_categories:
            review_id = review_category['review_id']

            query_list = [('review_id', review_id)]
            review = self.query.find_one('review', query_list, review_fields)

            set_list = [('review_useful', review['votes']['useful'])]
            self.query.find_and_update(self.collection_name, query_list, set_list)

            counter += 1
            if counter % 10000 == 0:
                print(str(counter) + " reviews finished.")

    def run_handler(self):
        top_category = self.find_top_category()
        top_ten_business_id_docs = self.find_top_businesses_of_category(top_category, self.top_businesses_limit)

        for business in top_ten_business_id_docs:
            run_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            self.logger.info(run_time + " - Business '" + str(business['_id']) + "' started.")

            print("Starting AlchemyAPI calls. Please check nlp.log inside 'logs' folder for business_id")

            try:
                self.update_mixed_collection_with_sentiment(business)
                self.logger.info("Business " + str(business['_id']) + " finished.")
            except NLPValueError as err:
                self.logger.exception(run_time + " - " + str(err.message))

    def run2_handler(self):
        business_id = BUS_ID
        limit = 200
        run_info = {}
        run_info['run_date'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        #dbc.find({"business_id": "zTCCbg7mGslxACL5KlAPIQ"}).sort("date", 1).limit(20)
        query_list = [('business_id', business_id)]
        projections = ['review_id', 'text', 'combined_result']
        documents = self.query.find_all_by('review_category', query_list, projections)

        total_reviews = documents.count()
        run_info['total_review'] = total_reviews
        success = 0
        failure_reviews = []

        print("get uncalled review: {}".format(documents.count()))
        i = 0
        for doc in documents:
            review_id = doc['review_id']

            if 'combined_result' in doc:
                continue

            result = self.get_combined_result(doc['text'])
            if type(result) == 'NLPValueError': # fail
                failure_reviews.append(review_id)
            else:
                data = dict()
                val = None
                if 'entities'in result:
                    val = result['entities']
                else:
                    val = []

                data['entities'] = val

                if 'concepts'in result:
                    val = result['concepts']
                else:
                    val = []

                data['concepts'] = val

                if 'keywords'in result:
                    val = result['keywords']
                else:
                    val = []

                data['keywords'] = val

                if 'taxonomy'in result:
                    val = result['taxonomy']
                else:
                    val = []

                data['taxonomy'] = val

                query_list = [('review_id', review_id)]
                set_list = [('combined_result', data)]

                self.query.find_and_update('review_category', query_list, set_list)

                if success % 50 == 0:
                    print(str(success) + " reviews updated.")

                success += 1
                #pprint(result)

            i += 1
            if i == limit:
                break

        run_info['success'] = success
        run_info['fail'] = total_reviews - success
        if success != total_reviews:
            run_info['failure_ids'] = failure_reviews

        pprint(run_info)

        with open('./run2_log.txt', 'w+') as outfile:
            json.dump(run_info, outfile, indent=4, ensure_ascii=False)


        """
        result = self.get_combined_result(doc['text'])
        print(result)

        """

    def tee_perform(self):
        #['u-Gbz-uGIIKC0SN2MwXtLw', 'FyCc8g7LCVpU4BGCz-WUog']
        review_id = 'FyCc8g7LCVpU4BGCz-WUog'
        query_list = [('review_id', review_id)]
        projections = ['review_id', 'text']
        review = self.query.find_one('review_category', query_list, projections)

        if review is not None:
            sentiment_res = self.get_sentiment_result(review['text'])
            pprint(sentiment_res)
            sentiment = self.get_sentiment_result(review['text'])['docSentiment']
            query_list = [('review_id', review_id)]
            set_list = [('sentiment', sentiment)]

            self.query.find_and_update(self.collection_name, query_list, set_list)


if __name__ == '__main__':
    nlp_handler = NLPHandler()
    # nlp_handler.create_mixed_collection()
    # nlp_handler.update_mixed_collection_with_review_votes()
    #nlp_handler.run_handler()
    #nlp_handler.print_uncalled_top_ten_business()
    #nlp_handler.tee_perform()
    nlp_handler.run2_handler()
