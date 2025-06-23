from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            name TEXT PRIMARY KEY,
            quantity REAL,
            price REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            name TEXT,
            quantity REAL,
            price REAL,
            total REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add')
def add_item_page():
    return render_template('add_item.html')

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = float(request.form['quantity'])
    price = float(request.form['price'])

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO inventory (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory_page'))

@app.route('/purchase')
def purchase_item_page():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()
    conn.close()
    return render_template('purchase_item.html', items=items)

@app.route('/purchase_item', methods=['POST'])
def purchase_item():
    name = request.form['name']
    quantity = float(request.form['quantity'])

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT quantity, price FROM inventory WHERE name = ?', (name,))
    item = c.fetchone()

    if item and item[0] >= quantity:
        new_quantity = item[0] - quantity
        total = quantity * item[1]
        c.execute('UPDATE inventory SET quantity = ? WHERE name = ?', (new_quantity, name))
        c.execute('INSERT INTO transactions (name, quantity, price, total) VALUES (?, ?, ?, ?)', (name, quantity, item[1], total))
        conn.commit()
    conn.close()
    return redirect(url_for('inventory_page'))

@app.route('/alerts')
def low_stock_alerts():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT name, quantity FROM inventory WHERE quantity < 5')
    alerts = c.fetchall()
    conn.close()
    return render_template('alerts.html', alerts=alerts)

@app.route('/inventory')
def inventory_page():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()
    conn.close()
    return render_template('inventory.html', items=items)

@app.route('/edit/<name>')
def edit_item(name):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory WHERE name = ?', (name,))
    item = c.fetchone()
    conn.close()
    return render_template('edit_item.html', item=item)

@app.route('/update_item/<name>', methods=['POST'])
def update_item(name):
    quantity = float(request.form['quantity'])
    price = float(request.form['price'])

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('UPDATE inventory SET quantity = ?, price = ? WHERE name = ?', (quantity, price, name))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory_page'))

@app.route('/transactions')
def show_transactions():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row  # ✅ allow dict-like access
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return render_template('recent_transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
