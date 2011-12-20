from mongokit import Connection
from flask import render_template, request, Flask, session
from config import *
import datetime
import pymongo

#configure the database
conn = Connection(MONGODB_HOST, MONGODB_PORT)
db = conn[DATABASE]
from models import *

#configure the app
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def show_entries():
	#return all entries by this user sorted by date
	return render_template('entry.html', entries=sorted(
		list(db.entries.find()),
		key=lambda x: x['date'][-1],
		reverse=True)) 

@app.route('/login/', methods=['GET', 'POST'])
def login():
	pass	

@app.route('/update/', methods=['POST'])
def update_entry():
	try:
		entry = db.entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	except KeyError:
		entry = db.entries.Entry()
	entry.content.append(request.form['content'])
	entry.date.append(datetime.datetime.now())
	entry.rows.append(int(request.form['rows']))
	entry.visible = True
	entry.public = False
	entry.save()
	return str(entry._id)
	
@app.route('/remove/', methods=['POST'])
def remove_entry():
	entry = db.entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	entry.visible = False
	entry.save()
	return str(entry._id)

@app.route('/template/entry/', methods=['GET'])
def get_entry_template():
	return render_template('entry.html',
		#create a fake single entry so the template renders a single entry div
		entries=[{'rows': '', '_id': '', 'content': '', 'visible': 1}],
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
