import logging
import sys
import time

from app.exceptions import (
    ProductAlreadyExistsError,
    ProductNotFoundError,
    ProductScrapingError,
)
from app.integrations.telegram import (
    clear_updates,
    get_updates,
    send_message,
)
from app.services.product_service import (
    add_product,
    check_product_exists,
)

# Configuração simples de logs
logging.basicConfig(level=logging.INFO)


def run_bot():
    offset = clear_updates()

    # Estados do fluxo (Single-User)
    waiting_for_url = False
    waiting_for_price = False

    # Dados temporários do produto
    product_url = None
    target_price = None

    # Controle de tempo limite do fluxo
    timeout_at = None

    print("🤖 Telegram Bot do PriceRadar iniciado e aguardando comandos...")

    try:
        while True:
            # 1. Tratamento contra oscilações e falhas de rede na API do Telegram
            try:
                response = get_updates(offset, timeout=1)
            except Exception as e:
                logging.error(f"Erro de conexão com o Telegram: {e}")
                time.sleep(3)
                continue

            for update in response.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")
                if message is None:
                    continue

                text = message.get("text", "").strip()

                # 2. Comando /add
                if text == "/add":
                    if waiting_for_url or waiting_for_price:
                        send_message("Já estamos realizando um cadastro. 🙂")
                        continue

                    waiting_for_url = True
                    waiting_for_price = False
                    timeout_at = time.time() + 30

                    send_message("Me envie a URL do produto.")
                    continue

                # 3. Comando /cancel
                if text == "/cancel":
                    if waiting_for_url or waiting_for_price:
                        waiting_for_url = False
                        waiting_for_price = False
                        timeout_at = None
                        product_url = None
                        target_price = None

                        send_message("Operação cancelada. 👍")

                    continue

                # 4. Comando /update (Em desenvolvimento)
                if text == "/update":
                    waiting_for_url = False
                    waiting_for_price = False
                    timeout_at = None
                    product_url = None
                    target_price = None

                    send_message(
                        "🚧 <b>Funcionalidade em desenvolvimento!</b>\n\n"
                        "Em breve você poderá atualizar o preço-alvo dos seus produtos cadastrados por aqui. 😉"
                    )
                    continue

                # 5. Comando /stop ou /quit (Encerra o processo do bot)
                if text in ["/stop", "/quit"]:
                    send_message("Desligando o PriceRadar Bot... 👋 Até mais!")
                    print("🛑 Recebido comando de parada pelo Telegram. Encerrando...")
                    sys.exit(0)

                # 6. Etapa 1: Captura e Validação Antecipada da URL
                if waiting_for_url:
                    if not (text.startswith("http://") or text.startswith("https://")):
                        timeout_at = time.time() + 30
                        send_message(
                            "Isso não parece uma URL válida. "
                            "Envie um link começando com http:// ou https://"
                        )
                        continue

                    try:
                        send_message("Verificando o produto... 🔎")

                        # Consulta se o ASIN já está no banco de dados
                        existing_product = check_product_exists(text)

                        if existing_product is not None:
                            send_message(
                                f"⚠️ Você já está monitorando este produto!\n\n"
                                f"<b>{existing_product.name}</b>\n"
                                f"Preço-alvo cadastrado: R$ {existing_product.target_price:.2f}\n\n"
                                f"💡 <i>Se quiser alterar o preço-alvo, envie /update.</i>"
                            )

                            # Reseta o fluxo imediatamente
                            waiting_for_url = False
                            timeout_at = None
                            product_url = None
                            continue

                        # Produto novo: Salva URL e avança para o preço
                        product_url = text
                        print(f"URL salva temporariamente: {product_url}")

                        waiting_for_url = False
                        waiting_for_price = True
                        timeout_at = time.time() + 30

                        send_message(
                            "URL recebida! 👍\n"
                            "Agora me diga o preço que você quer pagar."
                        )

                    except ProductScrapingError:
                        send_message(
                            "❌ Não consegui identificar o código do produto (ASIN) a partir desse link. "
                            "Certifique-se de enviar o link completo da Amazon."
                        )
                        waiting_for_url = False
                        timeout_at = None
                        product_url = None

                    except Exception as err:
                        logging.error(f"Erro ao verificar produto: {err}")
                        send_message(
                            "❌ Ocorreu um erro ao verificar o produto. "
                            "Tente novamente em alguns instantes."
                        )
                        waiting_for_url = False
                        timeout_at = None
                        product_url = None

                    continue

                # 7. Etapa 2: Captura do preço e cadastro
                if waiting_for_price:
                    cleaned_text = (
                        text.upper()
                        .replace("R$", "")
                        .replace("REAIS", "")
                        .replace(",", ".")
                        .strip()
                    )

                    try:
                        target_price = float(cleaned_text)
                        print(f"Preço salvo temporariamente: R$ {target_price:.2f}")

                        send_message("Buscando informações do produto... ⏳")

                        try:
                            product = add_product(product_url, target_price)

                            send_message(
                                f"Produto cadastrado com sucesso! 👍\n\n"
                                f"<b>{product.name}</b>\n"
                                f"Preço-alvo: R$ {product.target_price:.2f}"
                            )

                        except ProductAlreadyExistsError:
                            send_message("⚠️ Você já está monitorando este produto!")

                        except ProductScrapingError:
                            send_message(
                                "❌ Não consegui extrair as informações deste link. "
                                "Verifique se a URL da Amazon está correta e tente novamente."
                            )

                        except ProductNotFoundError:
                            send_message("🔍 Produto não encontrado no marketplace informado.")

                        except Exception as err:
                            logging.error(f"Erro inesperado ao cadastrar produto: {err}")
                            send_message(
                                "❌ Ocorreu um erro interno ao cadastrar o produto. "
                                "Tente novamente em alguns instantes."
                            )

                        # Reseta o estado após concluir a tentativa
                        waiting_for_price = False
                        timeout_at = None
                        product_url = None
                        target_price = None

                    except ValueError:
                        timeout_at = time.time() + 30
                        send_message(
                            "Não consegui entender esse preço. "
                            "Envie apenas o valor, por exemplo: 100.00 ou R$ 100,00"
                        )

                    continue

            # 8. Checagem centralizada de timeout
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

    except KeyboardInterrupt:
        print("\n🛑 Encerramento solicitado via Terminal (Ctrl+C). Fechando bot...")
        sys.exit(0)


if __name__ == "__main__":
    run_bot()