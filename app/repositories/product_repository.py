from datetime import datetime

from app.database import get_connection
from app.models import Product


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


def get_product_by_id(product_id):
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
        WHERE p.id = ?
    """, (product_id,))

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
        image_url=row[5],
        price=row[6]
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
        SELECT
            p.id,
            p.name,
            p.image_url,
            ph.price,
            ph.checked_at
        FROM products p
        LEFT JOIN price_history ph
            ON p.id = ph.product_id
        WHERE p.id = ?
        ORDER BY ph.checked_at DESC
    """, (product_id,))

    rows = cursor.fetchall()

    connection.close()

    return rows

def get_latest_price(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT price
        FROM price_history
        WHERE product_id = ?
        ORDER BY checked_at DESC
        LIMIT 1
    """, (product_id,))

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return row[0]