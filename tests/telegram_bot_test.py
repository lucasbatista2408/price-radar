from app.integrations.telegram import get_updates, send_message


offset = 132588215

while True:
    response = get_updates(offset)

    for update in response["result"]:
        print("UPDATE:", update["update_id"])
        offset = update["update_id"] + 1

        message = update.get("message")

        if message is None:
            continue

        text = message.get("text")

        if text == "/add":
            print("Comando /add recebido!")

            send_message(
                "Me envie a URL do produto que você quer adicionar."
            )