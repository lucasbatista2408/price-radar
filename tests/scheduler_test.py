import time

from app.services.price_service import check_live_price
from app.integrations.telegram import send_offer


PRODUCT_ID = 28


while True:
    product = check_live_price(PRODUCT_ID)
    
    if product is not None:
        send_offer(
            f"🧪 TESTE\n"
            f"{product.name}\n"
            f"R$ {product.price:.2f}\n"
            f"{product.url}"
        )

    time.sleep(60)