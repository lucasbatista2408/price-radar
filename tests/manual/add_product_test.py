from app.services.product_service import add_product
from app.exceptions import ProductScrapingError, ProductAlreadyExistsError


def add_product_test():
    try:
        product = add_product(
            "https://www.amazon.com.br/Al%C3%A9m-Bem-Mal-Friedrich-Nietzsche/dp/6583970341/145-4701801-8206328?pd_rd_w=SWRGJ&content-id=amzn1.sym.ea5263f5-901f-4a74-9b73-3fc0e530788d&pf_rd_p=ea5263f5-901f-4a74-9b73-3fc0e530788d&pf_rd_r=Y2MJ0CG95E7CDH53XHTG&pd_rd_wg=juoWn&pd_rd_r=5884fe99-67e5-418c-9beb-cc9e05c3b8ba&pd_rd_i=6583970341&psc=1",
            60.00
        )

        print(f"Nome: {product.name}")
        print(f"Preço: R$ {product.price:.2f}")
        print(f"Target: R$ {product.target_price:.2f}")
        print(f"Imagem: {product.image_url}")

    except ProductScrapingError as error:
        print(f"Erro ao buscar produto: {error}")

    except ProductAlreadyExistsError as error:
        print(f"Erro: {error}")