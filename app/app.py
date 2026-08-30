from app.database import get_products
from app.services.price_service import check_product_price


def app():
    products = get_products()

    for product in products:
        result = check_product_price(product)

        if result is None:
            print(f"Não foi possível verificar: {product.name}")
            continue

        updated_product, is_target_reached = result

        print(f"Nome: {updated_product.name}")
        print(f"Preço: R$ {updated_product.price:.2f}")
        print(f"Target: R$ {updated_product.target_price:.2f}")

        if is_target_reached:
            print("🎯 Target atingido!")
        else:
            print("Target ainda não atingido.")

        print()