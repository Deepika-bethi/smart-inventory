from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample in-memory inventory and transaction log
inventory = []
transactions = []

@app.route('/')
def index():
    return render_template('index.html', items=inventory)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])

        for item in inventory:
            if item['name'] == name:
                item['quantity'] += quantity
                flash(f"{name} updated successfully!", "success")
                break
        else:
            inventory.append({'name': name, 'quantity': quantity, 'price': price})
            flash(f"{name} added successfully!", "success")

        return redirect(url_for('index'))
    return render_template('add_items.html')

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        name = request.form['name']
        qty = float(request.form['quantity'])

        for item in inventory:
            if item['name'] == name:
                if item['quantity'] >= qty:
                    item['quantity'] -= qty
                    transactions.append({'name': name, 'quantity': qty, 'price': item['price']})
                    flash(f"{qty} kg of {name} purchased!", "success")
                else:
                    flash(f"Not enough stock for {name}", "danger")
                break
        else:
            flash(f"{name} not found in inventory", "danger")

        return redirect(url_for('index'))
    return render_template('purchase.html', items=inventory)

@app.route('/transactions')
def recent_transactions():
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
