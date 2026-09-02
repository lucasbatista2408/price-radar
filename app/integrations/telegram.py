import os

import requests
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_offer(image_url, caption):
    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendPhoto"
    )

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    response = requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": caption,
            "parse_mode": "HTML"
        },
        files={
            "photo": image_response.content
        }
    )

    response.raise_for_status()

    return response.json()

def send_message(message):
    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    response = requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
    )

    response.raise_for_status()

    return response.json()

def notify(product):
    message = (
        f"<b>{product.name}</b>\n"
        f"🔻 PREÇO BAIXO\n"
        f"R$ {product.price:.2f}\n"
        f"🛒 <a href=\"{product.url}\">Comprar</a>"
    )

    send_offer(product.image_url, message)

def get_updates(offset=None):
    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/getUpdates"
    )

    params = {}

    if offset is not None:
        params["offset"] = offset

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()