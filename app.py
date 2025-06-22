from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data stores
inventory = []
transactions = []

@app.route('/')
def index():
    return render_template('index.html', items=inventory)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        if name and quantity and price:
            inventory.append({
                'name': name,
                'quantity': float(quantity),
                'price': float(price)
            })
            return redirect(url_for('index'))
    return render_template('add_items.html')

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        quantity = request.form.get('quantity')
        for item in inventory:
            if item['name'] == item_name:
                qty = float(quantity)
                if item['quantity'] >= qty:
                    item['quantity'] -= qty
                    transactions.append({'item': item_name, 'quantity': qty})
                    break
        return redirect(url_for('index'))
    return render_template('purchase.html', items=inventory)

@app.route('/alerts')
def alerts():
    low_stock = [item for item in inventory if item['quantity'] < 5]
    return render_template('alerts.html', low_stock=low_stock)

@app.route('/recent_transactions')
def recent_transactions():
    return render_template('recent_transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
