from app.services.product_service import add_product
from app.exceptions import ProductScrapingError, ProductAlreadyExistsError


def app():
    try:
        product = add_product(
            "https://www.amazon.com.br/gp/product/8569980612?smid=A1ZZFT5FULY4LN&psc=1",
            75.00
        )

        print(f"Produto cadastrado: {product.name}")
        print(f"Preço: R$ {product.price:.2f}")

    except ProductScrapingError as error:
        print(f"Erro ao buscar produto: {error}")

    except ProductAlreadyExistsError as error:
        print(f"Erro: {error}")