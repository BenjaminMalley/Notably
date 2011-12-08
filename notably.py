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
conn[DATABASE].entries.drop() #reset the entries collection every time; for debug
entries = conn[DATABASE].entries

@app.route('/', methods=['GET'])
def show_entries():
	return render_template('index.html', entries=list(entries.find()).sort(key=lambda x: x.creation_date))	

@app.route('/login/')
def login():
	pass

@app.route('/add/', methods=['POST'])
def add_entry():
	entry = entries.Entry()
	entry.content = request.form['content']
	entry.creation_date = datetime.datetime.now()
	entry.rows = int(request.form['rows'])
	entry.visible = True
	entry.save()
	return str(entry._id)
	
@app.route('/modify/', methods=['POST'])
def modify_entry():
	entry = entries.find_one({'_id': pymongo.objectid.ObjectId(request.form['id'])})
	print entry
	return request.form['id']

if __name__ == '__main__':
	app.run(debug=True)

