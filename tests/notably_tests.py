import sys
from mongokit import Connection
import os
import unittest
import datetime
#import notably and models from one level up
sys.path.append(os.path.abspath('..'))
from app import app
from models import Entry

class NotablyTestCase(unittest.TestCase):
	'''Test case for notably--MONGO DB MUST BE RUNNING ON localhost:27107'''
	def setUp(self):
		app.config.update({
			'DATABASE': 'test',
			'MONGODB_HOST': 'localhost',
			'MONGODB_PORT': 27017,
			'TESTING': True,
			'SECRET_KEY': 'testing key',
		})
		
		self.generic_entry = {'content': 'test', 'rows': '1', 'date': datetime.datetime.now()}
		self.generic_user = {'name': 'test_user', 'pw': 'default'}	
	
		self.app = app.test_client()
		self.conn = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
		#self.conn.register([Entry, User])
		self.conn.register([Entry])
		#reset the collections
		self.conn[app.config['DATABASE']].entries.drop()
		self.conn[app.config['DATABASE']].users.drop()
	
	#we don't actually need to tear anything down--but we'll leave this in case that changes
	def tearDown(self):
		pass

	def test_entries_view(self):
		'''tests that the database is queried, index.html is rendered and returned.
		there are no entries in the test db so the index page will have nothing but and empty textarea'''
		rv = self.app.get('/')
		assert '<!DOCTYPE html>' in rv.data
		
	def test_add_entry(self):
		'''tests adding a new entry'''
		rv = self.app.post('/update/', data=self.generic_entry, follow_redirects=True)
		assert 'Bad Request' not in rv.data
		
	def test_update_entry(self):
		'''test modifying an existing entry'''
		#generate a new entry
		entries = self.conn[app.config['DATABASE']].entries
		entry = entries.Entry()
		entry.content.append(u'test')
		entry.rows.append(1)
		entry.date.append(datetime.datetime.now())	
		entry.save()
		new_entry = self.generic_entry
		new_entry.update({'id': entry._id})
		#post an entry update using the id of the entry we just created
		rv = self.app.post('/update/', data=new_entry, follow_redirects=True)
		import pymongo
		entry = entries.Entry.one({'_id': pymongo.objectid.ObjectId(entry._id)})
		assert len(entry.content) == 2
		assert 'Bad Request' not in rv.data

	#def test_add_user(self):
	#	rv = self.app.post('/signup/', data=self.generic_user, follow_redirects=True)
	#	assert 'Bad Request' not in rv.data
	#	rv = self.app.post('/signup/', data=self.generic_user, follow_redirects=True)
	#	assert 'bad' in rv.data
		
				
if __name__=='__main__':
	unittest.main()
