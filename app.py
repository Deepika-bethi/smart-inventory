from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

inventory = []
transactions = []

@app.route('/')
def index():
    low_stock = [item for item in inventory if item['quantity'] < 5]
    return render_template('index.html', items=inventory, low_stock=low_stock)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])

        for item in inventory:
            if item['name'] == name:
                item['quantity'] += quantity
                item['price'] = price
                break
        else:
            inventory.append({'name': name, 'quantity': quantity, 'price': price})

        return redirect('/')
    return render_template('add_items.html')

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])

        for item in inventory:
            if item['name'] == name and item['quantity'] >= quantity:
                item['quantity'] -= quantity
                transactions.append({'name': name, 'quantity': quantity, 'total': quantity * item['price']})
                break

        return redirect('/')
    return render_template('purchase.html', items=inventory)

@app.route('/transactions')
def transaction_history():
    return render_template('transactions.html', transactions=transactions)

# ✅ Updated code for Render deployment below:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
