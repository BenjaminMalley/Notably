from mongokit import Document, Connection
from pymongo import objectid
from contextlib import contextmanager
from config import MONGODB_HOST, MONGODB_PORT, DATABASE

class Model(Document):

	@classmethod
	@contextmanager
	def get_or_create(cls, id):
		conn = Connection(MONGODB_HOST, MONGODB_PORT)
		db = conn[DATABASE]
		conn.register([cls])
		entry = db[cls.collection_name].cls.one({'_id': objectid.ObjectId(id)})
		if entry==None:
			entry = db[cls.collection_name][cls.__name__]()
		yield entry
		print 'hello'
		entry.save()




