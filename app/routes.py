from flask import redirect, render_template, request
from app.utils import int_to_id
from app.db import get_db_connection
import re

from app.app import app

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form['url']

    if(url is None or url == ""):
        return redirect('/')
    
    # Check if the URL is valid
    regex = re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', url)
    
    if(regex is None):
        return redirect('/')
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Insert the URL into the database
    cursor.execute('INSERT INTO links (long_url) VALUES (?)', (url, ))
    
    shortened_url = int_to_id(cursor.lastrowid)

    # Update the shortened URL in the database
    cursor.execute('UPDATE links SET short_url = ? WHERE id = ?', (shortened_url, cursor.lastrowid))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect('/shortened?short=' + shortened_url)

@app.route('/shortened')
def shortened():
    shortened_url = request.args.get('short')
    return render_template('shortened.html', shortened_url=shortened_url)

@app.route('/track/<short_url>')
def track(short_url):
    connection = get_db_connection()

    result = connection.execute('SELECT * FROM links WHERE short_url = ?', (short_url,)).fetchone()
    
    connection.close()
    
    if(result is None):
        return render_template('track.html', short_url="000", long_url="Not found", clicks=0)

    return render_template('track.html', short_url=short_url, long_url=result['long_url'], clicks=result['clicks'])

@app.route('/<short_url>')
def redirect_to_url(short_url):
    # Get the long URL from the database
    connection = get_db_connection()
    result = connection.execute('SELECT * FROM links WHERE short_url = ?', (short_url,)).fetchone()

    if(result is None):
        connection.commit()
        connection.close()
        return redirect('/')
    
    # Update the number of clicks
    connection.execute('UPDATE links SET clicks = clicks + 1 WHERE short_url = ?', (short_url,))
    
    connection.commit()
    connection.close()

    return redirect(result['long_url'])

