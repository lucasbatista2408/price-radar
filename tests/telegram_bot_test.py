import time

from app.integrations.telegram import (
    clear_updates,
    get_updates,
    send_message,
)

offset = clear_updates()

# Estados do fluxo do Telegram
waiting_for_url = False
waiting_for_price = False

# Dados coletados do produto (mantidos até a persistência no banco/API)
product_url = None
target_price = None

# Controle de tempo limite
timeout_at = None

while True:
    response = get_updates(offset, timeout=1)

    for update in response.get("result", []):
        offset = update["update_id"] + 1

        message = update.get("message")
        if message is None:
            continue

        text = message.get("text", "").strip()

        # 1. Comando /add
        if text == "/add":
            if waiting_for_url or waiting_for_price:
                send_message("Já estamos realizando um cadastro. 🙂")
                continue

            waiting_for_url = True
            waiting_for_price = False
            timeout_at = time.time() + 30
            send_message("Me envie a URL do produto.")
            continue

        # 2. Comando /cancel
        if text == "/cancel":
            if waiting_for_url or waiting_for_price:
                waiting_for_url = False
                waiting_for_price = False
                timeout_at = None
                product_url = None
                target_price = None
                send_message("Operação cancelada. 👍")
            continue

        # 3. Etapa 1: Captura a URL
        if waiting_for_url:
            if text.startswith("http://") or text.startswith("https://"):
                product_url = text  # Salva a URL na variável
                print(f"URL salva temporariamente: {product_url}")

                waiting_for_url = False
                waiting_for_price = True
                timeout_at = time.time() + 30  # Renova timeout para o preço

                send_message(
                    "URL recebida! 👍\n"
                    "Agora me diga o preço que você quer pagar."
                )
            else:
                send_message(
                    "Isso não parece uma URL válida. "
                    "Envie um link começando com http:// ou https://"
                )
                timeout_at = time.time() + 30
            continue

        # 4. Etapa 2: Captura o Preço e Dispara para a API
        if waiting_for_price:
            cleaned_text = text.upper().replace("R$", "").replace("REAIS", "").replace(",", ".").strip()
            
            try:
                target_price = float(cleaned_text)  # Salva o preço na variável
                print(f"Preço salvo temporariamente: R$ {target_price:.2f}")

                # -------------------------------------------------------------
                # AQUI ENTRA A CHAMADA DA SUA API DO PRICERADAR
                # Exemplo:
                # response = api.create_product(url=product_url, target_price=target_price)
                # -------------------------------------------------------------

                # Notifica o usuário que os dados foram coletados/salvos
                send_message(
                    f"Produto cadastrado com sucesso! 🎉\n"
                    f"URL: {product_url}\n"
                    f"Preço-alvo: R$ {target_price:.2f}"
                )

                # SÓ AGORA resetamos as variáveis e o estado do fluxo
                waiting_for_price = False
                timeout_at = None
                product_url = None
                target_price = None

            except ValueError:
                send_message(
                    "Não consegui entender esse preço. "
                    "Envie apenas o valor, por exemplo: 100.00 ou R$ 100,00"
                )
            continue

    # 5. Checagem de Timeout (se expirar, aí sim limpamos tudo)
    if (waiting_for_url or waiting_for_price) and time.time() >= timeout_at:
        send_message(
            "Acho que o cadastro ficou pelo caminho 😅. "
            "Quando quiser tentar de novo, é só mandar /add."
        )

        waiting_for_url = False
        waiting_for_price = False
        timeout_at = None
        product_url = None
        target_price = None