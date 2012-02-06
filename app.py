from flask import render_template, request, Flask
from flask.views import MethodView
from config import *
import datetime
from mongoengine import connect
from models import Revision, Entry

#configure the app
app = Flask(__name__)
app.config.from_object(__name__)

connect(DATABASE,
		host=MONGODB_HOST,
		port=MONGODB_PORT,
		username=USERNAME,
		password=PASSWORD)

class EntryAPI(MethodView):
	
	def post(self):
		revision = Revision(content=request.form['content'], rows=request.form['rows'])
		entry = Entry()
		entry.revisions.append(revision)
		entry.save()
		return entry.id
	
	def put(self, entry_id):
		entry = Entry.get(id=entry_id)


@app.route('/', methods=['GET'])
def show_entries():
	#return all entries by this user sorted by date
	print list(Entry.objects)
	return render_template('entry.html', entries=list(Entry.objects)) 

@app.route('/login/', methods=['GET', 'POST'])
def login():
	pass	

def update_entry(entry_id=None):
	'''Update an existing entry at /update/entry_id/ or make a new one at /update/.
	Returns the entry_id of the new or updated entry.'''
	entry = Entry()
	if entry_id != None:
		entry = Entry.objects(id=entry_id)[0]
	revision = Revision(content=request.form['content'], rows=request.form['rows'])
	entry.revisions.append(revision)
	entry.save()
	return str(entry.id)
	
app.add_url_rule('/entry/', defaults={'entry_id': None}, view_func=update_entry, methods=['POST'])
app.add_url_rule('/entry/<entry_id>/', view_func=update_entry, methods=['POST'])
	
@app.route('/remove/', methods=['POST'])
def remove_entry():
	entry = db.entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	entry.visible = False
	entry.save()
	return str(entry._id)

@app.route('/template/entry/', methods=['GET'])
def get_entry_template():
	tmp = Entry()
	tmp.revisions.append(Revision(content='', rows=0))
	return render_template('entry.html',
		#create a fake single entry so the template renders a single entry div
		entries=[tmp],
		standalone=True) #prevent jinja2 from rendering the parent template

@app.route('/revisions/', methods=['POST'])
def get_revisions():
	entry = db.entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	return render_template('revisions.html', entry=entry, num_entries=enumerate(entry.content))	

@app.route('/version/', methods=['POST'])
def change_current_revision():
	entry = db.entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	entry.content.append(entry.content.pop(int(request.form['version'])))
	entry.date.pop(int(request.form['version']))
	entry.date.append(datetime.datetime.now())
	entry.save()
	return str(entry._id)

@app.route('/post/<entry_id>/', methods=['GET'])
def get_public_entry(entry_id):
	entry = db.entries.Entry.one({'_id': pymongo.objectid.ObjectId(entry_id)})
	if entry.public:
		return entry.content[-1]
	else: return "yeah, right"

@app.route('/publicize/', methods=['POST'])
def publicize_entry():
	entry = db.entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	entry.public = True
	entry.save()
	#return the markup for a Public URL for JS to add to the page
	return "<li><a href='/post/{0}/'>Public URL</a></li>".format(str(entry._id))

@app.route('/signup/', methods=['POST'])
def add_user():
	name = request.form['name']
	#make sure the user name isn't taken
	if name in [user.name for user in list(users.User.fetch())]:
		return 'bad'
	else:
		user = users.User() #add a new user 
		user.name = name 
		import random  
		user.salt = unicode(''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(16)))
		import hashlib
		user.password = unicode(hashlib.md5(user.salt + request.form['pw']).hexdigest())
		user.save()
		print [user.name for user in list(users.User.fetch())]
		return str(user._id)
	

if __name__ == '__main__':
	app.run(debug=True)
