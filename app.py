from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock data to simulate database (replace with real DB in your app)
inventory = []
transactions = []
alerts_list = []

@app.route('/')
def index():
    # Show main dashboard with inventory and alerts summary
    return render_template('index.html', items=inventory, alerts=alerts_list)

@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        # Add item to inventory
        if name and quantity and price:
            inventory.append({
                'name': name,
                'quantity': float(quantity),
                'price': float(price)
            })
        return redirect(url_for('index'))
    return render_template('add_items.html')

@app.route('/alerts')
def alerts():
    # Simple alert: low stock items (e.g., quantity < 5)
    alerts_list.clear()
    for item in inventory:
        if item['quantity'] < 5:
            alerts_list.append(f"{item['name']} is low on stock: {item['quantity']} left")
    return render_template('alerts.html', alerts=alerts_list)

@app.route('/recent-transactions')
def recent_transactions():
    # Show recent transactions
    return render_template('recent_transactions.html', transactions=transactions)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        purchase_qty = request.form.get('quantity')

        # Process purchase and update inventory
        if item_name and purchase_qty:
            qty = float(purchase_qty)
            for item in inventory:
                if item['name'] == item_name:
                    if item['quantity'] >= qty:
                        item['quantity'] -= qty
                        transactions.append({
                            'item_name': item_name,
                            'quantity': qty,
                        })
                    break
        return redirect(url_for('index'))
    return render_template('purchase.html', items=inventory)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
