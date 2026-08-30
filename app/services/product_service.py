from app.models import Product
from app.scraper.amazon import amazon_scraper
from app.database import save_product


def add_product(url, target_price):
    product = Product(
        name="",
        url=url,
        target_price=target_price
    )

    product = amazon_scraper(product)

    if product is None:
        return None

    save_product(product)

    return product