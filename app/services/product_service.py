from app.exceptions import (
    ProductAlreadyExistsError,
    ProductNotFoundError,
    ProductScrapingError,
)
from app.integrations.scraper.amazon import amazon_scraper
from app.models import Product
from app.repositories.product_repository import (
    get_product_by_asin,
    get_product_by_id,
    save_price_history,
    save_product,
)
from app.utils import extract_asin


def check_product_exists(url: str) -> Product | None:
    """Extrai o ASIN da URL e verifica se o produto já está cadastrado no banco."""
    asin = extract_asin(url)

    if not asin:
        raise ProductScrapingError(
            "Não foi possível identificar o código ASIN na URL fornecida."
        )

    return get_product_by_asin(asin)


def add_product(url: str, target_price: float) -> Product:
    """Valida, executa o scraping e cadastra o novo produto no banco."""
    
    # 1. Extrai o ASIN uma única vez
    asin = extract_asin(url)

    if not asin:
        raise ProductScrapingError(
            "Não foi possível identificar o código ASIN na URL fornecida."
        )

    # 2. Valida duplicidade usando o ASIN já extraído
    existing_product = get_product_by_asin(asin)
    if existing_product:
        raise ProductAlreadyExistsError("O produto já existe na base de dados.")

    # 3. Cria o objeto base com o ASIN já em mãos
    product = Product(url=url, target_price=target_price, asin=asin)

    # 4. Executa o Scraping
    new_product = amazon_scraper(product)

    if new_product is None:
        raise ProductScrapingError(
            "Não foi possível obter o título ou preço a partir do link fornecido."
        )

    # 5. Salva no banco com a proteção caso retorne None
    saved_product = save_product(new_product)

    if saved_product is None:
        raise ProductAlreadyExistsError(
            "Não foi possível salvar o produto no banco de dados."
        )

    save_price_history(saved_product)

    return saved_product


def get_product(product_id: int) -> Product:
    """Busca um produto pelo ID interno."""
    product = get_product_by_id(product_id)

    if product is None:
        raise ProductNotFoundError("O produto não foi encontrado.")

    return product