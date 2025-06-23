from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Data storage
items = []
transactions = []

# Home - User Mode
@app.route('/')
def index():
    return render_template('index.html', items=items)

# Add Item Page
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])

        for item in items:
            if item['name'] == name:
                item['quantity'] += quantity
                item['price'] = price  # update price if needed
                flash(f"Updated {name}: quantity and price.", "info")
                break
        else:
            items.append({'name': name, 'quantity': quantity, 'price': price})
            flash(f"Added {name} to inventory.", "success")

        return redirect(url_for('index'))

    return render_template('add_items.html')

# Purchase Page
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        name = request.form['name']
        purchase_quantity = float(request.form['quantity'])

        for item in items:
            if item['name'] == name:
                if item['quantity'] >= purchase_quantity:
                    item['quantity'] -= purchase_quantity
                    total = purchase_quantity * item['price']
                    
                    transactions.append({
                        'name': name,
                        'quantity': purchase_quantity,
                        'price': item['price'],
                        'total': total
                    })
                    flash(f"Purchased {purchase_quantity} kg of {name} for ₹{total}.", "success")
                else:
                    flash(f"Not enough {name} in stock!", "danger")
                break
        else:
            flash(f"Item {name} not found!", "danger")

        return redirect(url_for('index'))

    return render_template('purchase.html', items=items)

# Recent Transactions Page
@app.route('/transactions')
def recent_transactions():
    return render_template('recent_transactions.html', transactions=transactions)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
