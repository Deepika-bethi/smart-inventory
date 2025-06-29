from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB_FILE = 'inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL
        )
    ''')
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

initialize_database()

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])
        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
        conn.commit()
        conn.close()
        return render_template('add_items.html', message="Item added successfully.")
    return render_template('add_items.html')

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        quantity = float(request.form['quantity'])
        item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
        if item and item['quantity'] >= quantity:
            new_quantity = item['quantity'] - quantity
            total = quantity * item['price']
            conn.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item_id))
            conn.execute('INSERT INTO transactions (item_name, quantity, price, total) VALUES (?, ?, ?, ?)',
                         (item['name'], quantity, item['price'], total))
            conn.commit()
        conn.close()
        return render_template('purchase.html', items=items, message="Purchase successful.")
    conn.close()
    return render_template('purchase.html', items=items)

@app.route('/transactions')
def transactions():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions').fetchall()
    conn.close()
    return render_template('recent_transactions.html', transactions=transactions)

@app.route('/alerts')
def alerts():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items WHERE quantity < 5').fetchall()
    conn.close()
    return render_template('alerts.html', items=items)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if request.method == 'POST':
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])
        conn.execute('UPDATE items SET quantity = ?, price = ? WHERE id = ?', (quantity, price, item_id))
        conn.commit()
        conn.close()
        return render_template('edit_item.html', item=item, message="Item updated.")
    conn.close()
    return render_template('edit_item.html', item=item)
@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('current_inventory.html', items=items)

