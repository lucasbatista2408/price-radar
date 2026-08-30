from app.database import create_tables, get_products
from app.services.price_service import check_product_price


def app():
    create_tables()

    print("🚨 Price Radar iniciado!")

    products = get_products() #Get all products from the database

    for product in products: #Update the price of each product, gets the current price and checks if it is below the target price

        result = check_product_price(product) #update the product price and returns the updated product

        if result is None: #control flow if the product is not found or the price could not be obtained
            print("Não foi possível obter o preço.")
            continue

        updated_product, is_target_reached = result

        print(
            f"Produto: {updated_product.name}\n"
            f"Preço: R$ {updated_product.price:.2f}\n"
        )

        if is_target_reached:
            print("🚨 PREÇO BAIXO!")
        else:
            print("Preço acima da meta.")