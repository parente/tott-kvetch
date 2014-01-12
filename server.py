import os
import json
import sqlite3
import datetime
from bottle import request, response, get, post, static_file, template, run

STATIC_PATH='/static'
conn = None

@get('/')
def index():
    '''
    Serve the index page.
    '''
    return template('index.tpl', static_path=STATIC_PATH)

@get('%s/<filename:path>' % STATIC_PATH)
def send_static(filename):
    '''
    Serve static files.
    '''
    return static_file(filename, root='public')

@get('/favorites')
def get_favorites():
    '''
    Select posts in the db from highest votes to lowest. Cap at 10.
    '''
    rows = conn.execute('''SELECT rowid, body, votes, timestamp FROM posts 
        ORDER BY votes desc LIMIT 10''')
    posts = [row for row in rows]
    response.content_type = 'application/json'
    return json.dumps(posts)

@get('/posts')
def get_posts():
    '''
    Select posts in the db from newest to oldest. Cap at 10.
    '''
    rows = conn.execute('''SELECT rowid, body, votes, timestamp FROM posts 
        ORDER BY timestamp desc LIMIT 10''')
    posts = [row for row in rows]
    response.content_type = 'application/json'
    return json.dumps(posts)

@post('/posts')
def add_post():
    '''
    Add a post. 140 chars or less Respond with the post ID and timestamp.
    '''
    post = request.json
    c = conn.cursor()
    post['timestamp'] = datetime.datetime.utcnow().isoformat()
    post['body'] = post['body'][:140]
    try:
        c.execute('INSERT INTO posts(body, votes, timestamp) VALUES (:body, 0, :timestamp)', post)
        conn.commit()
    finally:
        c.close()
    post['rowid'] = c.lastrowid
    response.content_type = 'application/json'
    return post

@post('/posts/<rowid:int>/upvote')
def upvote(rowid):
    '''
    Increments the vote count for a post. Returns the current vote total.
    '''
    c = conn.cursor()
    post = {}
    try:
        c.execute('UPDATE posts SET votes = votes + 1 WHERE rowid = ?', (rowid, ))
        conn.commit()
    finally:
        c.close()
    rows = conn.execute('SELECT votes FROM posts WHERE rowid = ?', (rowid, ))
    post['rowid'] = rowid
    post['votes'] = rows.fetchone()['votes']
    response.content_type = 'application/json'
    return post

def dict_factory(cursor, row):
    '''
    Make all rows dictionaries with column name keys.

    http://docs.python.org/2.6/library/sqlite3.html#sqlite3.Connection.row_factory
    '''
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d

def init_db(name='kvetch.db'):
    '''
    Connect to the db. Create the posts table if the db is new.
    '''
    global conn
    exists = os.path.isfile(name)
    conn = sqlite3.connect(name)
    conn.row_factory = dict_factory
    if not exists:
        with conn:
            conn.execute('''CREATE TABLE posts
            (body text, votes int, timestamp timestamp)''')

if __name__ == '__main__':
    init_db()

    if os.environ.get('BOTTLE_DEV'):
        run(host='0.0.0.0', port=8080, reloader=True, debug=True) 
    else:
        run(host='0.0.0.0', port=8080) 