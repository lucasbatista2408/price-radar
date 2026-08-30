from playwright.sync_api import sync_playwright
from app.utils import get_price

url = "https://www.amazon.com.br/gp/product/8568224067?smid=A1ZZFT5FULY4LN&psc=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)

    price = page.locator(".priceToPay")

  
    if price.count() > 0:
        price_value = get_price(price)
        print(f"Preço encontrado: R$ {price_value:.2f}")

        if price_value < 35.00:
            print("🚨 Preço abaixo de R$ 35,00! Compre agora!")
        else:
            print("Preço acima de R$ 35,00. Aguarde uma promoção.")

    else:
        print("Preço não encontrado")

    input("Pressione ENTER para fechar...")

    browser.close()

