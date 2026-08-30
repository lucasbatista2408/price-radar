from app.scraper.amazon import amazon_scraper
from app.database import save_price_history


def check_product_price(product):
    updated_product = amazon_scraper(product)

    if updated_product is None:
        return None

    save_price_history(updated_product)

    if updated_product.price <= updated_product.target_price:
        return updated_product, True

    return updated_product, False