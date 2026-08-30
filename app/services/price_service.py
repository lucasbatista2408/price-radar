from app.scraper.amazon import amazon_scraper

from app.database import (
    get_products,
    save_price_history,
    get_price_history
)


def check_product_price(product):
    updated_product = amazon_scraper(product)

    if updated_product is None:
        return None

    save_price_history(updated_product)

    target_reached = (
        updated_product.price <= updated_product.target_price
    )

    return updated_product, target_reached


def check_all_products():
    products = get_products()

    results = []

    for product in products:
        result = check_product_price(product)

        if result is None:
            results.append({
                "product": product,
                "price": None,
                "target_reached": False,
                "error": True
            })
            continue

        updated_product, target_reached = result

        results.append({
            "product": updated_product,
            "price": updated_product.price,
            "target_reached": target_reached,
            "error": False
        })

    return results


def get_product_price_history(product_id):
    return get_price_history(product_id)