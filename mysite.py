import os, datetime
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import socket

app = Flask('__name__')

#########_CONFIG_################

app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path,'posts.db'),
    SECRET_KEY='devkey',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('MYSITE_SETTINGS', silent=True)


#######_DATABASE_STUFF_#############
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the DATABASE....ur good to go!')

#############_VIEWS_#######################3

@app.route('/', methods=['POST','GET'])
def show_posts():
    db = get_db()
    if request.method == 'POST':
        db.execute('insert into entries(title, text) values(?,?)',
                [request.form['title'], request.form['text']])
    db.commit()
    cur=db.execute('select title, text, date_created from entries order by id desc')
    entries = cur.fetchall()
    a = request.remote_addr
    return render_template('index.html', entries=entries, a=a)

if __name__ == ('__main__'):
    app.run(debug=True)
