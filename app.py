from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# 🔧 Ensure DB exists on first run (for Render)
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

@app.route('/')
def index():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items)

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
    return redirect(url_for('index'))

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
    return redirect(url_for('index'))

@app.route('/transactions')
def show_transactions():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return render_template('recent_transactions.html', transactions=transactions)

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
        return redirect(url_for('index'))
    else:
        c.execute('SELECT * FROM items WHERE id=?', (item_id,))
        item = c.fetchone()
        conn.close()
        return render_template('edit_item.html', item=item)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
