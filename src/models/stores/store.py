import uuid

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors

__author__ = "esobolie"


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": _id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        """
        http://www.amaz -> http://www.amazon.com. Whether the two strings begin the same way
        :param url_prefix: prefix of store link
        :return:
        """
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        """
        Return a store from a url like "https://rozetka.com.ua/msi_ge72mvr7rg_075xua/p31373959/"
        :param url: The item's URL
        :return: a Store, or raises StoreNotFound if no store matches URL
        """
        for i in range(0, len(url) + 1):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                raise StoreErrors.StoreNotFoundException("The URL Prefix give us none results")

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})

