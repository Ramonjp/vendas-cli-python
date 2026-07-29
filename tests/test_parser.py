"""Testes do parser (leitura e filtro de CSV)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from vendas_cli.parser import filtrar_por_periodo, ler_vendas

FIXTURES = Path(__file__).parent / "fixtures"

CSV_COM_DATA = """\
produto,quantidade,preco_unitario,data
Camiseta,3,49.9,2025-01-15
Calça,2,99.9,2025-02-10
Camiseta,1,49.9,2025-03-05
Tênis,1,199.9,2025-04-20
"""


def test_ler_vendas_ok() -> None:
    vendas = ler_vendas(FIXTURES / "vendas_ok.csv")
    assert len(vendas) == 4
    assert vendas[0].produto == "Camiseta"
    assert vendas[0].quantidade == 3
    assert vendas[0].preco_unitario == 49.9
    assert vendas[0].data is None


def test_ler_vendas_com_data(tmp_path: Path) -> None:
    caminho = tmp_path / "vendas.csv"
    caminho.write_text(CSV_COM_DATA, encoding="utf-8")
    vendas = ler_vendas(caminho)
    assert len(vendas) == 4
    assert vendas[0].data == date(2025, 1, 15)


def test_ler_vendas_arquivo_inexistente() -> None:
    with pytest.raises(FileNotFoundError):
        ler_vendas(FIXTURES / "nao_existe.csv")


def test_ler_vendas_coluna_faltando(tmp_path: Path) -> None:
    caminho = tmp_path / "ruim.csv"
    caminho.write_text("produto,quantidade\nCamiseta,1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="colunas obrigatórias"):
        ler_vendas(caminho)


def test_ler_vendas_linha_invalida_ignorada(caplog: pytest.LogCaptureFixture) -> None:
    import logging

    with caplog.at_level(logging.WARNING):
        vendas = ler_vendas(FIXTURES / "vendas_invalida.csv")

    assert len(vendas) == 1
    assert vendas[0].produto == "Camiseta"
    assert any("ignorada" in r.message for r in caplog.records)


def test_ler_vendas_vazia() -> None:
    with pytest.raises(ValueError, match="Nenhuma venda válida"):
        ler_vendas(FIXTURES / "vendas_vazia.csv")


def test_filtrar_por_periodo(tmp_path: Path) -> None:
    caminho = tmp_path / "vendas.csv"
    caminho.write_text(CSV_COM_DATA, encoding="utf-8")
    vendas = ler_vendas(caminho)
    filtradas = filtrar_por_periodo(
        vendas, date(2025, 1, 1), date(2025, 3, 31)
    )
    assert len(filtradas) == 3
    assert all(v.produto in {"Camiseta", "Calça"} for v in filtradas)


def test_filtrar_sem_coluna_data() -> None:
    vendas = ler_vendas(FIXTURES / "vendas_ok.csv")
    with pytest.raises(ValueError, match="não possui coluna 'data'"):
        filtrar_por_periodo(vendas, date(2025, 1, 1), None)


def test_filtrar_start_maior_que_end(tmp_path: Path) -> None:
    caminho = tmp_path / "vendas.csv"
    caminho.write_text(CSV_COM_DATA, encoding="utf-8")
    vendas = ler_vendas(caminho)
    with pytest.raises(ValueError, match="não pode ser maior"):
        filtrar_por_periodo(vendas, date(2025, 6, 1), date(2025, 1, 1))


def test_filtrar_sem_filtro_retorna_tudo() -> None:
    vendas = ler_vendas(FIXTURES / "vendas_ok.csv")
    assert filtrar_por_periodo(vendas, None, None) == vendas
