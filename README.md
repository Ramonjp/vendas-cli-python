# vendas-cli

CLI em Python que lê um CSV de vendas e gera relatório (texto ou JSON):
total por produto, valor total e produto mais vendido, com filtro opcional por período.


## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows

pip install --upgrade pip
pip install -e ".[dev]"
```

## Uso

```bash
vendas-cli examples/vendas_exemplo.csv --format text
vendas-cli examples/vendas_exemplo.csv --format json
vendas-cli examples/vendas_com_data.csv --format json --start 2025-01-01 --end 2025-03-31
```

Parâmetros:

| Argumento | Descrição |
|---|---|
| `csv_path` | Caminho do CSV (obrigatório) |
| `--format text\|json` | Formato de saída (default: `text`) |
| `--start YYYY-MM-DD` | Data inicial do filtro (inclusiva) |
| `--end YYYY-MM-DD` | Data final do filtro (inclusiva) |

## Formato do CSV

Colunas obrigatórias:

```
produto,quantidade,preco_unitario
Camiseta,3,49.9
Calça,2,99.9
```

Coluna opcional `data` (formato `YYYY-MM-DD`) — necessária para usar `--start`/`--end`:

```
produto,quantidade,preco_unitario,data
Camiseta,3,49.9,2025-01-15
```

- `examples/vendas_exemplo.csv` — CSV do avaliador (sem coluna `data`).
- `examples/vendas_com_data.csv` — mesmo cenário com `data`, para demonstrar o filtro por período.
- Separador decimal: ponto (`.`).
- Encoding: UTF-8 (também aceita Latin-1).
- Linhas com valores inválidos são ignoradas (com warning no log).

**Produto mais vendido:** maior quantidade total; empate por maior valor total;
empate final por ordem alfabética.

## Testes

```bash
source .venv/bin/activate
pytest
```

Cobertura mínima: 80% (`pytest.ini`).

## Estrutura

```
vendas_cli/
  cli.py       # argparse + orquestração
  parser.py    # leitura do CSV
  core.py      # cálculos do relatório
  output.py    # formatação text/json
examples/
  vendas_exemplo.csv
  vendas_com_data.csv
tests/
```
