# 📡 PriceRadar

O **PriceRadar** é uma aplicação pessoal e modular para monitoramento contínuo de preços de produtos em diferentes marketplaces. 

O objetivo do projeto é permitir o cadastro de produtos através de links e preços-alvo. O sistema executa rotinas periódicas em lote para verificar a variação de preços e notifica o usuário via Telegram assim que um produto atinge ou fica abaixo do valor desejado.

---

## 🎯 Principais Recursos

- **Monitoramento por Preço-Alvo**: Alertas automáticos disparados apenas quando o valor atinge a meta.
- **Integração Interativa via Telegram**:
  - Cadastro interativo de produtos via conversa com bot (`/add`, `/cancel`).
  - Notificações visuais de ofertas com foto do produto, valor atualizado e link direto de compra.
- **Processamento em Lote (Batch/Offset)**: Rotina otimizada para verificação de preços sem sobrecarregar a fila de produtos.
- **Arquitetura Desacoplada e Modular**: Camadas bem definidas (*Services*, *Repositories*, *Integrations*, *Workers*) facilitando a adição de novos marketplaces sem impactar o núcleo do sistema.

---

## 🏛️ Arquitetura e Tecnologia

O projeto foi construído em **Python** focando em previsibilidade, estabilidade e facilidade de manutenção.
