import logging
import sys
import time

from app.integrations.telegram import notify
from app.services.price_service import check_all_products

INTERVAL = 15 * 60  # 15 minutos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def run_scheduler():
    logging.info(
        "⏰ Scheduler do PriceRadar iniciado! "
        "Monitorando todos os produtos..."
    )

    try:
        while True:
            try:
                results = check_all_products()

                if not results:
                    logging.info(
                        "Nenhum produto cadastrado para monitorar no momento."
                    )

                for item in results:
                    product = item["product"]

                    if item["error"]:
                        logging.error(
                            f"Erro ao verificar o produto "
                            f"ID {product.id} ({product.name}): "
                            f"{item['error']}"
                        )
                        continue

                    logging.info(
                        f"Produto ID {product.id} ({product.name}) | "
                        f"Preço atual: R$ {item['price']:.2f} | "
                        f"Notificar: "
                        f"{'Sim' if item['should_notify'] else 'Não'}"
                    )

                    if item["should_notify"]:
                        notify(product)

            except Exception as e:
                logging.error(
                    f"Erro inesperado no ciclo do scheduler: {e}"
                )

            logging.info(
                f"Aguardando {INTERVAL // 60} minutos "
                "para o próximo ciclo...\n"
            )

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print(
            "\n🛑 Encerramento solicitado via Terminal "
            "(Ctrl+C). Fechando scheduler..."
        )
        sys.exit(0)


if __name__ == "__main__":
    run_scheduler()

