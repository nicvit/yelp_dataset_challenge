#!/usr/bin/env python
from __future__ import division
import sys
import os
import logging
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from yelp.data.collection import MongoQuery

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))


class UserUpdater:
    def __init__(self):
        self.query = MongoQuery()
        self.users = None
        self.logger = logging.Logger('UserUpdateLogger', level=logging.INFO)
        self.logger.addHandler(logging.FileHandler(filename=os.path.join(LOG_PATH, 'user_update.log'), mode='a+'))

    def get_all_users(self):
        if not self.users:
            where = [
                ('review_count', {"$ne": 0}),
                ('average_usefulness', {"$exists": False})
            ]
            projection = ['user_id', 'votes', 'review_count']
            collection = 'user'
            self.users = list(self.query.find_all_by(collection_name=collection, query_list=where, fields=projection))

        return self.users

    def update_user(self, user, avg_usr_usefulness):
        runtime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        user_id = user['user_id']
        query_list = [('user_id', user_id)]
        set_list = [('average_usefulness', avg_usr_usefulness)]
        col = 'user'

        self.logger.info(runtime + " - Set average_usefulness = " + avg_usr_usefulness + " to user with ID: " + user_id)
        self.query.find_and_update(col, query_list, set_list)

    def update_all_users_with_user_usefulness(self):
        users = self.get_all_users()
        print(len(users))

        counter = 1
        for user in users:
            counter += 1

            avg_usr_usefulness = self.calculate_average_usefulness(user)
            self.update_user(user, avg_usr_usefulness)

            if counter % 1000 == 0:
                print(str(counter) + " users updated.")

        self.logger.info("Execution finished. " + str(counter) + " users updated.")
        return users

    @staticmethod
    def calculate_average_usefulness(user):
        return "%.2f" % (user['votes']['useful'] / user['review_count'])


if __name__ == '__main__':
    run_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    user_updater = UserUpdater()

    user_updater.logger.info(run_time + ' - Starting to update users with average_usefulness')
    user_updater.update_all_users_with_user_usefulness()
