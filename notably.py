from flask import render_template, request, Flask, url_for
from mongokit import Connection
from config import *
from models import *
import datetime
import pymongo

app = Flask(__name__)
app.config.from_object(__name__)
	
conn = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
conn.register([Entry, User])
#conn[DATABASE].entries.drop() #reset the entries collection every time; for debug
entries = conn[DATABASE].entries

@app.route('/', methods=['GET'])
def show_entries():
	#return all entries by this user sorted by date
	return render_template('index.html', entries=sorted(
		list(entries.find()),
		key=lambda x: x['date'][-1],
		reverse=True)) 


@app.route('/login/')
def login():
	pass

@app.route('/entry/', methods=['POST'])
def add_entry():
	entry = entries.Entry.one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	if entry==None:
		entry = entries.Entry()
	entry.content.append(request.form['content'])
	entry.date.append(datetime.datetime.now())
	entry.rows.append(int(request.form['rows']))
	entry.visible = True
	entry.save()
	return str(entry._id)
	
if __name__ == '__main__':
	app.run(debug=True)

