from flask import render_template, request, Flask, session
from mongokit import Connection
from config import *
from models import *
import datetime
import pymongo

app = Flask(__name__)
app.config.from_object(__name__)

#configure database and prepare collections
conn = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
conn.register([Entry, User])
#conn[DATABASE].entries.drop() #reset the entries collection every time; for debug
entries = conn[DATABASE].entries
users = conn[DATABASE].users

@app.route('/', methods=['GET'])
def show_entries():
	#return all entries by this user sorted by date
	return render_template('entry.html', entries=sorted(
		list(entries.find()),
		key=lambda x: x['date'][-1],
		reverse=True)) 

@app.route('/login/', methods=['GET', 'POST'])
def login():
	pass	

@app.route('/update/', methods=['POST'])
def update_entry():
	try:
		entry = entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	except KeyError:
		entry = entries.Entry()
	entry.content.append(request.form['content'])
	entry.date.append(datetime.datetime.now())
	entry.rows.append(int(request.form['rows']))
	entry.visible = True
	entry.public = False
	entry.save()
	return str(entry._id)
	
@app.route('/remove/', methods=['POST'])
def remove_entry():
	entry = entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
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
	entry = entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	return render_template('revisions.html', entry=entry, num_entries=enumerate(entry.content))	

@app.route('/version/', methods=['POST'])
def change_current_revision():
	entry = entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	entry.content.append(entry.content.pop(int(request.form['version'])))
	entry.date.pop(int(request.form['version']))
	entry.date.append(datetime.datetime.now())
	entry.save()
	return str(entry._id)

@app.route('/post/<entry_id>/', methods=['GET'])
def get_public_entry(entry_id):
	entry = entries.Entry.one({'_id': pymongo.objectid.ObjectId(entry_id)})
	if entry.public:
		return entry.content[-1]
	else: return "yeah, right"

@app.route('/publicize/', methods=['POST'])
def publicize_entry():
	entry = entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	entry.public = True
	entry.save()
	#return the markup for a Public URL for JS to add to the page
	return "<li><a href='/post/{0}/'>Public URL</a></li>".format(str(entry._id))

@app.route('/signup/', methods=['POST'])
def add_user():
	user = users.User() #add a new 
	user.name = request.form['name']
	import random  
	user.salt = ''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(16))
	import hashlib
	user.pw = hashlib.md5(user.salt + request.form['pw']).hexdigest
	user.save()
	return 'ok'
	

if __name__ == '__main__':
	app.run(debug=True)
