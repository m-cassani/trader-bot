# 📊 Robô de Trading Pessoal para Ações Brasileiras

Este projeto é um robô de trading **automatizado e modular**, focado no mercado de **ações brasileiras (B3)**.
Atualmente, o sistema está preparado para:

- ✅ Realizar backtests históricos de estratégias simples, como **médias móveis.**
- ✅ Gerar sinais de compra e venda com visualização gráfica.
- ✅ Simular operações em tempo real (**paper trading**).
- 🚧 Integração futura com Telegram para envio de alertas.
- 🚧 Evolução para execução automatizada com gerenciamento completo de portfólio.

---

## 🚀 Objetivos do Projeto

- Criar um robô de trading **para uso pessoal.**
- Automatizar e validar estratégias simples de trading.
- Simular operações tanto com dados históricos quanto em tempo real.
- Futuramente integrar com APIs de execução e envio de alertas.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- pandas
- numpy
- yfinance
- matplotlib

---

## 📂 Estrutura do Projeto

```text
trader-bot/
├── README.md
├── requirements.txt
├── .gitignore
└── src/
    ├── bot.py                 # Script principal com controle de execução via argumentos
    ├── strategies/            # Estratégias de trading (ex: cruzamento de médias móveis)
    │     └── moving_average_crossover.py
    ├── backtest/              # Módulos de backtest (histórico e tempo real)
    │     ├── historical_backtest.py
    │     └── realtime_backtest.py
    └── utils/                 # Funções auxiliares
          ├── data_collector.py   # Coleta e armazenamento de dados
          ├── file_manager.py     # Gerenciamento de arquivos (logs e relatórios)
          └── plot_signals.py     # Geração de gráficos de sinais
data/
├── input/
│    └── tickers.txt            # Lista de tickers a serem monitorados
└── output/                     # Resultados, gráficos, logs e relatórios
```

---

## ⚙️ Execução Local

### Exemplo 1: Backtest histórico (últimos 365 dias)

```bash
python src/bot.py --mode test-historical --strategy moving_average_crossover --initial_cash 5000
```

### Exemplo 2: Backtest em tempo real (paper trading)

```bash
python src/bot.py --mode test-realtime --strategy moving_average_crossover --initial_cash 5000 --duration 7 --window_size 365
```

### Parâmetros Disponíveis

| Parâmetro        | Descrição                             | Default     |
| ---------------- | ------------------------------------- | ----------- |
| `--mode`         | `test-historical` ou `test-realtime`  | Obrigatório |
| `--strategy`     | Estratégia a ser utilizada            | Obrigatório |
| `--initial_cash` | Valor inicial da carteira             | 5000        |
| `--duration`     | Tempo de execução (real time) em dias | 7           |
| `--window_size`  | Tamanho da janela para médias móveis  | 365         |

---

## 📦 Como funciona cada módulo

| Módulo                        | Responsabilidade                              |
| ----------------------------- | --------------------------------------------- |
| `bot.py`                      | Gerencia a execução via argumentos            |
| `data_collector.py`           | Baixa e organiza os dados financeiros         |
| `plot_signals.py`             | Gera gráficos com sinais de compra e venda    |
| `file_manager.py`             | Salva logs de trades e resumos de performance |
| `historical_backtest.py`      | Executa backtests históricos                  |
| `realtime_backtest.py`        | Simula operações em tempo real                |
| `moving_average_crossover.py` | Calcula as médias móveis e gera sinais        |

---

## 🔭 Melhorias Futuras

- 📬 Integração com Telegram para envio de alertas.
- 🚀 Execução contínua via Docker.
- 📈 Suporte a múltiplas estratégias simultâneas.
- ⚙️ Conexão com corretora para envio de ordens reais.
- 📊 Implementação de logging estruturado.
- 🔍 Testes automatizados para validação das estratégias.
