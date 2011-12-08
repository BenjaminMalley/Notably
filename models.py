from mongokit import Document

class Entry(Document):
	structure = {
		'content': unicode,
		'creation_date': datetime.datetime,
		'rows': int,
	}
	required_fields = ['content', 'creation_date', 'rows']
	use_dot_notation = True
	
	def __repr__(self):
		return '<Entry {0}>'.format(self.content)
	
class User(Document):
	structure = {
		'user_name': unicode,
	}
	required_fields = ['user_name']
	use_dot_notation = True
	
	def __repr__(self):
		return '<User {0}>'.format(self.user_name)