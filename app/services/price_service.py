from app.repositories.product_repository import (
    get_product_by_id,
    get_all_products,
    save_price_history,
    get_price_history,
    get_latest_price,
)

from app.integrations.scraper.amazon import amazon_scraper


def check_product_price(product):

    previous_price = get_latest_price(product.id)

    updated_product = amazon_scraper(product)

    if updated_product is None:
        return None

    target_reached = (
        updated_product.price <= updated_product.target_price
    )

    price_dropped = (
        previous_price is not None
        and updated_product.price < previous_price
    )

    should_notify = (
        target_reached
        and price_dropped
    )

    save_price_history(updated_product)

    print(f"Previous price: {previous_price}")

    return updated_product, target_reached, should_notify

def check_all_products():
    products = get_all_products()

    results = []

    for product in products:
        result = check_product_price(product)

        if result is None:
            results.append({
                "product": product,
                "price": None,
                "target_reached": False,
                "should_notify": False,
                "error": True
            })
            continue

        updated_product, target_reached, should_notify = result

        results.append({
            "product": updated_product,
            "price": updated_product.price,
            "target_reached": target_reached,
            "should_notify": should_notify,
            "error": False
        })

    return results

def get_product_price_history(product_id):
    return get_price_history(product_id)

def check_live_price(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        return None

    product_live_price = amazon_scraper(product)

    if product_live_price is None:
        return None

    return product_live_price