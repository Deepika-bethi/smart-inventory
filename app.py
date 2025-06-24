from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_FILE = 'inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create items table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL
        )
    ''')
    # Create transactions table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            total REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB once when the app starts
initialize_database()

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

# You can keep other routes here like /add, /purchase, etc.

if __name__ == '__main__':
    app.run(debug=True)
