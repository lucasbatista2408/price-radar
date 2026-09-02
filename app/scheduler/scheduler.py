import time

from app.services.price_service import check_live_price
from app.integrations.telegram import send_message


PRODUCT_ID = 28
INTERVAL = 10


def run_scheduler():
    while True:
        product = check_live_price(PRODUCT_ID)

        if product is not None:

            message = (
                f"<b>{product.name}</b>\n"
                f"🔻 PREÇO BAIXO\n"
                f"R$ {product.price:.2f}\n"
                f"🛒 <a href=\"{product.url}\">Comprar</a>"
            )

            if product is not None:
                send_message(message)

        time.sleep(INTERVAL)