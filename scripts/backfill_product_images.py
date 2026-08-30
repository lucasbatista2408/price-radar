import sqlite3

from app.database import get_products
from app.scraper.amazon import amazon_scraper


DB_NAME = "price_radar.db"


def update_product_image(product_id, image_url):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE products
        SET image_url = ?
        WHERE id = ?
    """, (
        image_url,
        product_id
    ))

    connection.commit()
    connection.close()


def backfill_product_images():
    products = get_products()

    for product in products:
        if product.image_url is not None:
            continue

        print(f"Buscando imagem: {product.name}")

        updated_product = amazon_scraper(product)

        if updated_product is None:
            print(f"Não foi possível buscar: {product.name}")
            continue

        if updated_product.image_url is None:
            print(f"Imagem não encontrada: {product.name}")
            continue

        update_product_image(
            updated_product.id,
            updated_product.image_url
        )

        print(f"Imagem salva: {updated_product.image_url}")
        print()


if __name__ == "__main__":
    backfill_product_images()