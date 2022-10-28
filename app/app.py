from flask import Flask, redirect, render_template, request
import os
from app.init_db import init_db

app = Flask(__name__)

from app import routes

if not os.path.exists('database.db'):
    print('Database not found. Creating...')
    init_db()

app.run(host='0.0.0.0')

