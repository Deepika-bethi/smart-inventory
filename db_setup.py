import sqlite3

def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Items table
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL
        )
    ''')

    # Transactions table
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
    print("✅ Database setup complete.")

if __name__ == "__main__":
    init_db()
