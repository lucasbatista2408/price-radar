from app.exceptions import (
    ProductAlreadyExistsError,
    ProductScrapingError,
    ProductNotFoundError
)

from app.models import Product

from app.scraper.amazon import amazon_scraper

from app.database import (save_product, save_price_history, get_product_by_asin, get_product_by_id)

from app.utils import extract_asin


def add_product(url, target_price):
    asin = extract_asin(url)

    if asin is None:
        raise ProductScrapingError(
            "Não foi possível identificar o ASIN na URL fornecida."
        )

    existing_product = get_product_by_asin(asin)

    if existing_product is not None:
        raise ProductAlreadyExistsError(
            "O produto já existe na base de dados."
        )

    product = Product(
        url=url,
        target_price=target_price,
        asin=asin
    )

    new_product = amazon_scraper(product)

    if new_product is None:
        raise ProductScrapingError(
            "Não foi possível obter o produto a partir da URL fornecida."
        )

    saved_product = save_product(new_product)

    if saved_product is None:
        raise ProductAlreadyExistsError(
            "O produto já existe na base de dados."
        )

    save_price_history(saved_product)

    return saved_product


def get_product(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        raise ProductNotFoundError(
            "O produto não foi encontrado."
        )

    return product