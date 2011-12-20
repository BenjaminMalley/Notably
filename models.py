from database import Model
import datetime
from app import conn, db
from mongokit import Connection

class Entry(Model):
	collection_name = 'entries'	
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

conn.register([Entry])
