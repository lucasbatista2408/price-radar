from app.models import Product
from app.services.price_service import check_product_price
from app.services.product_service import add_product
from app.database import get_connection

def update_values_db(sql_query, values):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(sql_query, values)

    connection.commit()
    connection.close()

def delete_values_db(sql_query_history, sql_query_product, id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(sql_query_history, (id,))
    cursor.execute(sql_query_product, (id,))

    connection.commit()
    connection.close()

def test_should_notify_when_price_drops():
    product = Product(
        url = "https://www.amazon.com.br/Divina-Com%C3%A9dia-Dante-Alighieri-Luxo/dp/6583970333/?_encoding=UTF8&pd_rd_w=JA6aw&content-id=amzn1.sym.ab89b960-8f04-4350-9ac3-8c2d05219993&pf_rd_p=ab89b960-8f04-4350-9ac3-8c2d05219993&pf_rd_r=A418NNQCAN4CQC3P2VC1&pd_rd_wg=AVoIA&pd_rd_r=c7840fde-690f-4319-b9d3-a83986e5ee9b",
        target_price = 200.0)

    added_product = add_product(product.url, product.target_price)


    sql_update_query = """
        UPDATE price_history
        SET price = ?
        WHERE product_id = ?
        """
    values = (250.00,added_product.id)

    update_values_db(sql_update_query, values)

    checked_product, target_reached, should_notify = check_product_price(added_product)

    print(f"Produto: {checked_product.name}\n"
          f"Preço atual: R$ {checked_product.price:.2f}\n"
          f"Notificação: {'Sim' if should_notify else 'Não'}\n"
          )

    checked_product, target_reached, should_notify = check_product_price(added_product)

    print(f"Produto: {checked_product.name}\n"
          f"Preço atual: R$ {checked_product.price:.2f}\n"
          f"Notificação: {'Sim' if should_notify else 'Não'}\n"
          )

    sql_delete_history_query = """
    DELETE FROM price_history
    WHERE product_id = ?
    """
    sql_delete_product_query = """
    DELETE FROM products
    WHERE id = ?
    """

    delete_values_db(sql_delete_history_query, sql_delete_product_query, added_product.id)
