from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('inventory.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    try:
        items = conn.execute('SELECT * FROM items').fetchall()
    except sqlite3.OperationalError:
        items = []
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
        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    conn = get_db_connection()
    try:
        items = conn.execute('SELECT * FROM items').fetchall()
    except sqlite3.OperationalError:
        items = []
        conn.close()
        return render_template('purchase.html', items=items)

    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        purchase_qty = float(request.form['quantity'])

        item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()

        if item and item['quantity'] >= purchase_qty:
            new_qty = item['quantity'] - purchase_qty
            conn.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_qty, item_id))

            total_price = purchase_qty * item['price']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            conn.execute('INSERT INTO transactions (item_name, quantity, price, total_price, timestamp) VALUES (?, ?, ?, ?, ?)',
                         (item['name'], purchase_qty, item['price'], total_price, timestamp))
            conn.commit()

            conn.close()
            return redirect(url_for('index'))

    conn.close()
    return render_template('purchase.html', items=items)

@app.route('/alerts')
def alerts():
    conn = get_db_connection()
    try:
        alerts = conn.execute('SELECT * FROM items WHERE quantity <= 3').fetchall()
    except sqlite3.OperationalError:
        alerts = []
    conn.close()
    return render_template('alerts.html', alerts=alerts)

@app.route('/transactions')
def transactions():
    conn = get_db_connection()
    try:
        transactions = conn.execute('SELECT * FROM transactions ORDER BY timestamp DESC').fetchall()
    except sqlite3.OperationalError:
        transactions = []
    conn.close()
    return render_template('recent_transactions.html', transactions=transactions)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()

    if request.method == 'POST':
        new_name = request.form['name']
        new_quantity = float(request.form['quantity'])
        new_price = float(request.form['price'])

        conn.execute('UPDATE items SET name = ?, quantity = ?, price = ? WHERE id = ?',
                     (new_name, new_quantity, new_price, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_item.html', item=item)

# ✅ FINAL SAFE /create-db route
@app.route('/create-db')
def create_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            quantity REAL,
            price REAL,
            total_price REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()
    return 'Tables created successfully.'

if __name__ == '__main__':
    app.run(debug=True)
