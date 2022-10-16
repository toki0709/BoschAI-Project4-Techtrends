import logging
import sqlite3
from urllib import response

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Capture any logs at the DEBUG level
logging.basicConfig(level=logging.DEBUG)

num_connections = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`


def get_db_connection():
    global num_connections

    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    num_connections = num_connections + 1
    return connection

# Function to get a post using its ID


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()

    if post is not None:
        logging.info("Article '%s' retrieved!" % post['title'])
    else:
        logging.info("Article %d was not found!", post_id)

    return post


def _get_count():
    connection = get_db_connection()
    count = connection.execute('SELECT count(*) as cnt FROM posts').fetchone()
    connection.close()
    return count['cnt']

# Define the main route of the web application


@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      return render_template('post.html', post=post)

# Define the About Us page


@app.route('/about')
def about():
    logging.info("The 'About Us' page was retrieved!")
    return render_template('about.html')

# Define the post creation functionality


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            logging.info(f" New article created with title {title}")
            return redirect(url_for('index'))
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def status():
    """
    return app status.
    """
    conn = get_db_connection()
    
    try:
        conn.execute("SELECT * FROM posts")
        response = app.response_class(response=json.dumps({"result": "OK - Healthy"}), status=500,
                                      mimetype='application/json')
        logging.info("OK - Healthy")

    except sqlite3.OperationalError:
        response = app.response_class(response=json.dumps({"result": "ERROR - unhealthy"}), status=500,
                                      mimetype='application/json')
        logging.info("ERROR - Unhealthy")
    
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts').fetchall()
    n_post = str(len(post))
    connection.commit()
    connection.close()
    return app.response_class(
        response=json.dumps({"status": "success", "code": 200, "data": {
                            "post": n_post}, "db_connection_count": db_connection_count}),
        status=200, mimetype='application/json')

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
