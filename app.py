from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

inventory = {}
low_stock = []
transactions = []

@app.route('/')
def index():
    return render_template('index.html', items=inventory, low_stock=low_stock)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            name = request.form['name']
            quantity = float(request.form['quantity'])
            price = float(request.form['price'])

            inventory[name] = {'quantity': quantity, 'price': price}
            if quantity < 5:
                if name not in low_stock:
                    low_stock.append(name)
        except KeyError as e:
            return f"Missing form field: {e}", 400

        return redirect(url_for('index'))

    return render_template('add_items.html')

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        item = request.form['item']
        qty = float(request.form['quantity'])

        if item in inventory and inventory[item]['quantity'] >= qty:
            inventory[item]['quantity'] -= qty
            cost = qty * inventory[item]['price']
            transactions.append({'item': item, 'quantity': qty, 'cost': cost})

            if inventory[item]['quantity'] < 5 and item not in low_stock:
                low_stock.append(item)

        return redirect(url_for('index'))

    return render_template('purchase.html', items=inventory)

@app.route('/transactions')
def transaction_history():
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
