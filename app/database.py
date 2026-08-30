import sqlite3
from app.models import Product
from datetime import datetime

DB_NAME = "price_radar.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            target_price REAL NOT NULL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        price REAL NOT NULL,
        checked_at TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    connection.commit()
    connection.close()



def save_product(product):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO products (name, url, target_price)
        VALUES (?, ?, ?)
    """, (
        product.name,
        product.url,
        product.target_price
    ))

    connection.commit()
    connection.close()



def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, url, target_price
        FROM products
    """)

    rows = cursor.fetchall()

    connection.close()

    products = []

    for row in rows:
        product = Product(
            id=row[0],
            name=row[1],
            url=row[2],
            target_price=row[3]
        )

        products.append(product)

    return products



def save_price_history(product):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO price_history (product_id, price, checked_at)
        VALUES (?, ?, ?)
    """, (
        product.id,
        product.price,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()



def get_price_history(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT price, checked_at
        FROM price_history
        WHERE product_id = ?
        ORDER BY checked_at DESC
    """, (product_id,))

    rows = cursor.fetchall()

    connection.close()

    return rows