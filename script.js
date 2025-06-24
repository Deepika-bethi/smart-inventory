function getDeviceId() {
    if (!localStorage.getItem("deviceId")) {
        const id = 'device_' + Math.random().toString(36).substring(2, 15);
        localStorage.setItem("deviceId", id);
    }
    return localStorage.getItem("deviceId");
}

function getInventory() {
    const deviceId = getDeviceId();
    return JSON.parse(localStorage.getItem(deviceId + '_inventory') || '[]');
}

function setInventory(data) {
    const deviceId = getDeviceId();
    localStorage.setItem(deviceId + '_inventory', JSON.stringify(data));
}

function showSection(id) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById(id).style.display = 'block';
    if (id === 'inventory') renderInventory();
    if (id === 'alerts') renderAlerts();
}

function goHome() {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.getElementById('mainMenu').style.display = 'flex';
}

function addItem() {
    const name = document.getElementById('itemName').value;
    const qty = parseFloat(document.getElementById('itemQty').value);
    const price = parseFloat(document.getElementById('itemPrice').value);

    if (!name || qty <= 0 || price <= 0) {
        alert("Please enter valid data");
        return;
    }

    const inventory = getInventory();
    inventory.push({ name, quantity: qty, price });
    setInventory(inventory);

    alert("Item saved!");
    document.getElementById('itemName').value = '';
    document.getElementById('itemQty').value = '';
    document.getElementById('itemPrice').value = '';
}

function renderInventory() {
    const inventory = getInventory();
    const table = document.getElementById('inventoryTable');
    table.innerHTML = `<tr><th>Item</th><th>Qty</th><th>Price</th><th>Stock</th><th>Action</th></tr>`;
    inventory.forEach((item, index) => {
        const stockStatus = item.quantity < 5 ? `<span style="color:red;">Low Stock</span>` : 'In Stock';
        table.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>${item.price}</td>
                <td>${stockStatus}</td>
                <td><button onclick="editItem(${index})">Edit</button></td>
            </tr>
        `;
    });
}

function editItem(index) {
    const inventory = getInventory();
    const item = inventory[index];
    const newQty = prompt("New Quantity:", item.quantity);
    const newPrice = prompt("New Price:", item.price);
    if (newQty !== null && newPrice !== null) {
        inventory[index].quantity = parseFloat(newQty);
        inventory[index].price = parseFloat(newPrice);
        setInventory(inventory);
        renderInventory();
    }
}

function renderAlerts() {
    const inventory = getInventory();
    const list = document.getElementById('alertList');
    list.innerHTML = '';
    inventory.forEach(item => {
        if (item.quantity < 5) {
            const li = document.createElement('li');
            li.textContent = `${item.name} - only ${item.quantity} kg left`;
            list.appendChild(li);
        }
    });
}
