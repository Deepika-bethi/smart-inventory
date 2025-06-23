from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# ✅ Auto-create DB and tables if not found (for Render)
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            total REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ✅ Home with navigation buttons
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Add item page
@app.route('/add-item')
def add_item_page():
    return render_template('add_item.html')

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = float(request.form['quantity'])
    price = float(request.form['price'])

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory_page'))

# ✅ Purchase page
@app.route('/purchase-item')
def purchase_item_page():
    return render_template('purchase_item.html')

@app.route('/purchase', methods=['POST'])
def purchase():
    name = request.form['name']
    quantity = float(request.form['quantity'])

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT quantity, price FROM items WHERE name = ?', (name,))
    result = c.fetchone()

    if result:
        current_quantity, price = result
        if quantity <= current_quantity:
            new_quantity = current_quantity - quantity
            c.execute('UPDATE items SET quantity = ? WHERE name = ?', (new_quantity, name))
            total = quantity * price
            c.execute('INSERT INTO transactions (name, quantity, price, total) VALUES (?, ?, ?, ?)',
                      (name, quantity, price, total))
            conn.commit()

    conn.close()
    return redirect(url_for('inventory_page'))

# ✅ Alerts page
@app.route('/alerts')
def low_stock_alerts():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items WHERE quantity < 5')
    alerts = c.fetchall()
    conn.close()
    return render_template('alerts.html', alerts=alerts)

# ✅ Inventory page
@app.route('/inventory')
def inventory_page():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return render_template('inventory.html', items=items)

# ✅ Edit item page
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    if request.method == 'POST':
        new_name = request.form['name']
        new_quantity = float(request.form['quantity'])
        new_price = float(request.form['price'])
        c.execute('UPDATE items SET name=?, quantity=?, price=? WHERE id=?',
                  (new_name, new_quantity, new_price, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('inventory_page'))
    else:
        c.execute('SELECT * FROM items WHERE id=?', (item_id,))
        item = c.fetchone()
        conn.close()
        return render_template('edit_item.html', item=item)

# ✅ Transactions page
@app.route('/transactions')
def show_transactions():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return render_template('recent_transactions.html', transactions=transactions)

# ✅ Port setup for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
