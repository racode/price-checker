import os

import pymongo
__author__ = "esobolie"

class Database(object):
    #URL = os.environ.get('MONGOLAB_URI')
    URL = "mongodb://{dbuser}:{dbpassword}@ds039404.mlab.com:39404/heroku_7wfgj110".format(dbuser=os.environ.get('dbuser'), dbpassword=os.environ.get('dbpassword'))
    #URL = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URL)
        Database.DATABASE = client["heroku_7wfgj110"]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        return Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)
