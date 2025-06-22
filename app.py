from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

inventory = []
transactions = []

@app.route('/')
def index():
    low_stock = [item for item in inventory if item['quantity'] < 3]
    return render_template('index.html', items=inventory, low_stock=low_stock)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])

        for item in inventory:
            if item['name'].lower() == name.lower():
                item['quantity'] += quantity
                item['price'] = price
                break
        else:
            inventory.append({'name': name, 'quantity': quantity, 'price': price})
        return redirect(url_for('index'))

    return render_template('add_items.html')

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    message = ""
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])

        for item in inventory:
            if item['name'].lower() == name.lower():
                if item['quantity'] >= quantity:
                    item['quantity'] -= quantity
                    transactions.append({
                        'name': name,
                        'quantity': quantity,
                        'total': round(quantity * item['price'], 2)
                    })
                    message = f"Purchased {quantity} kg of {name}"
                else:
                    message = f"Not enough {name} in stock!"
                break
        else:
            message = f"{name} not found in inventory."

    return render_template('purchase.html', items=inventory, message=message)

@app.route('/transactions')
def view_transactions():
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
