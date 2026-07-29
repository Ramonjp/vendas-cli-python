.PHONY: venv install test run run-filtro clean

venv:
	python3 -m venv .venv

install: venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"

test:
	.venv/bin/pytest

run:
	.venv/bin/vendas-cli examples/vendas_exemplo.csv --format text

run-filtro:
	.venv/bin/vendas-cli examples/vendas_com_data.csv --format json --start 2025-01-01 --end 2025-03-31

clean:
	rm -rf .venv .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
