from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

inventory = {}
transactions = []

@app.route('/')
def index():
    return render_template('index.html', items=inventory)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])
        inventory[name] = {'quantity': quantity, 'price': price}
        return redirect(url_for('index'))
    return render_template('add_items.html')

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        item_name = request.form['item']
        quantity = float(request.form['quantity'])
        if item_name in inventory and inventory[item_name]['quantity'] >= quantity:
            inventory[item_name]['quantity'] -= quantity
            transactions.append({
                'item': item_name,
                'quantity': quantity,
                'price': inventory[item_name]['price']
            })
        return redirect(url_for('index'))
    return render_template('purchase.html', items=inventory)

@app.route('/alerts')
def alerts():
    low_stock_items = {name: data for name, data in inventory.items() if data['quantity'] < 5}
    return render_template('alerts.html', low_stock=low_stock_items)

@app.route('/recent_transactions')
def recent_transactions():
    return render_template('recent_transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
