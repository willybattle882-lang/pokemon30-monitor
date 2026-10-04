# Pokémon 30 Anos — Monitor Mercado Livre

Monitor Python para Mercado Livre Brasil.

Configuração:
- preço: até 110% do preço sugerido público
- frete: separado, não entra no limite
- alerta: Telegram
- compra/carrinho: não automatizados; somente link
- histórico: SQLite
- execução: local ou VPS barato

## Instalação

Python 3.11+:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e preencha TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID.

Teste:
```bash
python -m app.telegram_test
```

Uma varredura:
```bash
python -m app.main --once
```

Monitor contínuo:
```bash
python -m app.main
```

O catálogo local contém apenas preços confirmados. Produtos cujo preço sugerido ainda está como "a confirmar" são ignorados.
