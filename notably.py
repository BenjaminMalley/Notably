from flask_router import Flask
from flask import render_template, session, request
from mongokit import Connection
from config import *
from models import *
import datetime

app = Flask(__name__)
app.config.from_object(__name__)
	
conn = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
conn.register([Entry, User])

@app.route('/', methods=['GET'])
def show_entries():
	collection = conn[DATABASE].entries
	entries = list(collection.find())
	return render_template('index.html', entries=entries)	

@app.route('/login/')
def login():
	pass

@app.route('/add/', methods=['POST'])
def add_entry():
	collection = conn[DATABASE].entries
	entry = collection.Entry()
	entry.content = request.form['content']
	entry.creation_date = datetime.datetime.now()
	entry.rows = int(request.form['rows'])
	entry.visible = True
	entry.save()
	return str(entry._id)

@app.route('/modify/', methods=['PUT'])
def modify_entry():
	pass

if __name__ == '__main__':
	app.run(debug=True)
