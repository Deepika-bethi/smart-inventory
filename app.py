from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_NAME = 'inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- HOME ----------
@app.route('/')
def home():
    return render_template('index.html')

# ---------- ADD ITEM ----------
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])

        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)',
                     (name, quantity, price))
        conn.commit()
        conn.close()
        return redirect(url_for('inventory_page'))

    return render_template('add_items.html')

# ---------- INVENTORY PAGE ----------
@app.route('/inventory')
def inventory_page():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('inventory.html', items=items)

# ---------- EDIT ITEM ----------
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])

        conn.execute('UPDATE items SET name = ?, quantity = ?, price = ? WHERE id = ?',
                     (name, quantity, price, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('inventory_page'))

    conn.close()
    return render_template('edit_item.html', item=item)

# ---------- CUSTOMER MODE (PURCHASE) ----------
@app.route('/customer')
def customer_mode():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('purchase.html', items=items)

# ---------- PURCHASE HANDLER ----------
@app.route('/purchase/<int:item_id>', methods=['POST'])
def purchase_item(item_id):
    quantity = float(request.form['quantity'])

    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()

    if item and item['quantity'] >= quantity:
        new_quantity = item['quantity'] - quantity
        conn.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item_id))
        conn.execute('INSERT INTO transactions (item_name, quantity, price) VALUES (?, ?, ?)',
                     (item['name'], quantity, item['price']))
        conn.commit()

    conn.close()
    return redirect(url_for('customer_mode'))

# ---------- ALERTS PAGE ----------
@app.route('/alerts')
def alerts():
    conn = get_db_connection()
    alerts = conn.execute('SELECT * FROM items WHERE quantity <= 3').fetchall()
    conn.close()
    return render_template('alerts.html', alerts=alerts)

# ---------- TRANSACTIONS PAGE ----------
@app.route('/transactions')
def show_transactions():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions').fetchall()
    conn.close()
    return render_template('recent_transactions.html', transactions=transactions)

# ---------- INIT DATABASE ----------
def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# ---------- RUN APP ----------
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
