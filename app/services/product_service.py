from app.models import Product
from app.scraper.amazon import amazon_scraper
from app.database import save_product, save_price_history


def add_product(url, target_price):
    product = Product(
        url=url,
        target_price=target_price
    )

    new_product = amazon_scraper(product)

    if new_product is None:
        return None

    saved_product = save_product(new_product)

    if saved_product is None:
        return None

    save_price_history(saved_product)

    return saved_product