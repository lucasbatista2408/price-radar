import time

from app.services.price_service import check_product_price
from app.integrations.telegram import notify, send_message
from app.services.product_service import get_product


PRODUCT_ID = 28
INTERVAL = 10


def run_scheduler():
    while True:
        product = get_product(PRODUCT_ID)

        if product is not None:
            updated_product, target_reached, should_notify = check_product_price(product)

            print(
                f"Produto: {updated_product.name}\n"
                f"Preço atual: R$ {updated_product.price:.2f}\n"
                f"Notificação: {'Sim' if should_notify else 'Não'}\n"
                )

            #if should_notify:
            notify()

        time.sleep(INTERVAL)   