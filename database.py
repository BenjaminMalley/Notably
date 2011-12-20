from pymongo import objectid
from contextlib import contextmanager
from config import MONGODB_HOST, MONGODB_PORT, DATABASE
from mongokit import Connection

@contextmanager
def get_or_create(cls, id):
	conn = Connection(MONGODB_HOST, MONGODB_PORT)
	db = conn[DATABASE]
	conn.register([cls])
	entry = db.entries.cls.one({'_id': objectid.ObjectId(id)})
	if entry==None:
		print cls 
		entry = db['entries'].cls()
	yield entry
	entry.save()

