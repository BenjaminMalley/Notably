import notably
import unittest

class NotablyTestCase(unittest.TestCase):

	def setUp(self):
		notably.app.config.update({
			'DATABASE': 'test',
			'MONGODB_HOST': 'localhost',
			'MONGODB_PORT': 27017,
			'TESTING': True,
			'SECRET_KEY': 'testing key',
			'USERNAME': 'test',
			'PASSWORD': 'default'
		})
		
		self.app = notably.app.test_client()
		self.conn = notably.Connection(notably.app.config['MONGODB_HOST'], notably.app.config['MONGODB_PORT'])
		self.conn.register([Entry, User])

		#reset the entries collection every time so we know there are no entries when we test
		conn[DATABASE].entries.drop() 
		entries = conn[DATABASE].entries
		
	def tearDown(self):
		pass

if __name__=='__main__':
	unittest.main()
