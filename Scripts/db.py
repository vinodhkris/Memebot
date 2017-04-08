import pymongo
from pymongo import MongoClient
import datetime
from bson.json_util import dumps

class MongoObj:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test_database
        self.collection = self.db.test_collection
        self.collection.drop_index("text")
        self.collection.create_index([("description",pymongo.TEXT),("actor",pymongo.TEXT)], name="text", default_language="english")

    def number_of_docs(self):
        return dumps(self.collection.count())

    def insert_doc(self,text,actor,image_name):
        self.collection.insert({"description":text, "actor":actor, "image_name":image_name})
        return 1

    def insert_bulk(self,descriptions,actors,image_names):
        records = []
        for i in xrange(len(image_names)):
            records.append({"description":descriptions[i], "actor":actors[i], "image_name":image_names[i]})
        result = self.collection.insert_many(records)
        return len(result.inserted_ids)

    def find_doc(self,description,actor):
        results = self.collection.find({'$text': {'$search': description+" "+actor}}, {'score': {'$meta': 'textScore'}})
        results = results.sort([( 'score', { '$meta': "textScore" } )])
        return dumps(results)

    def clear_db(self):
        self.collection.remove({})