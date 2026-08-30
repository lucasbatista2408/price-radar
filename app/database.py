import sqlite3
from datetime import datetime

from app.models import Product


DB_NAME = "price_radar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            asin TEXT,
            url TEXT NOT NULL UNIQUE,
            target_price REAL NOT NULL,
            image_url TEXT
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
        INSERT OR IGNORE INTO products
        (name, asin, url, target_price, image_url)
        VALUES (?, ?, ?, ?, ?)
    """, (
        product.name,
        product.asin,
        product.url,
        product.target_price,
        product.image_url
    ))

    if cursor.rowcount == 0:
        connection.commit()
        connection.close()
        return None

    product.id = cursor.lastrowid

    connection.commit()
    connection.close()

    return product


def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.name,
            p.asin,
            p.url,
            p.target_price,
            p.image_url,
            ph.price
        FROM products p
        LEFT JOIN price_history ph
            ON ph.id = (
                SELECT ph2.id
                FROM price_history ph2
                WHERE ph2.product_id = p.id
                ORDER BY ph2.checked_at DESC
                LIMIT 1
            )
    """)

    rows = cursor.fetchall()

    connection.close()

    products = []

    for row in rows:
        product = Product(
            id=row[0],
            name=row[1],
            asin=row[2],
            url=row[3],
            target_price=row[4],
            image_url=row[5],
            price=row[6]
        )

        products.append(product)

    return products

def get_product_by_asin(asin):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, asin, url, target_price, image_url
        FROM products
        WHERE asin = ?
    """, (asin,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return Product(
        id=row[0],
        name=row[1],
        asin=row[2],
        url=row[3],
        target_price=row[4],
        image_url=row[5]
    )


def save_price_history(product):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO price_history
        (product_id, price, checked_at)
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