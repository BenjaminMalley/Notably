from flask_router import Flask
from flask import render_template, session, g, request
from mongokit import Connection
import datetime
from config import *

app = Flask(__name__)
app.config.from_object(__name__)
	
connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])

@app.get('/')
def show_entries():
	...db code...
	return render_template('index.html', entries=entries)	

@app.route('/login/')
def login():
	pass

@app.post('/add/')
def add_entry():
	g.db.execute("insert into entries (content, rows, created) values (?, ?, datetime('now'))", (request.form['content'], request.form['rows']))
	g.db.commit()
	return 'OK' #eventually, we want to send back the unique ID for the entry, but for now it's enough to know we submitted it

@app.put('/modify/')
def modify_entry():
	g.db.execute("update entries set content=? and rows=? and modified=datetime('now') where id=?",(request.form['content'],request.form['rows'],request.form['id']))
	g.db.commit()
	return 'OK'
	
if __name__ == '__main__':
	app.run(debug=True)
