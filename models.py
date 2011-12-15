from mongokit import Document
import datetime

class Entry(Document):
	structure = {
		'content': [unicode],
		'date': [datetime.datetime],
		'rows': [int],
		'visible': bool,
		'public': bool,
	}
	required_fields = ['content', 'date', 'rows']
	use_dot_notation = True
	
	def __repr__(self):
		return '<Entry {0}>'.format(self.content)
	
class User(Document):
	structure = {
		'name': unicode,
		'password': unicode,
		'salt': unicode,
	}
	required_fields = ['name', 'password', 'salt']
	use_dot_notation = True
	
	def __repr__(self):
		return '<User {0}>'.format(self.name)
