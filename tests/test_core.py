"""Testes dos cálculos do relatório."""

from __future__ import annotations

from datetime import date

from vendas_cli.core import (
    Sale,
    agrupar_por_produto,
    gerar_relatorio,
    produto_mais_vendido,
)


def _vendas_exemplo() -> list[Sale]:
    return [
        Sale("Camiseta", 3, 49.9),
        Sale("Calça", 2, 99.9),
        Sale("Camiseta", 1, 49.9),
        Sale("Tênis", 1, 199.9),
    ]


def test_agrupar_por_produto() -> None:
    resumo = agrupar_por_produto(_vendas_exemplo())
    por_nome = {item["produto"]: item for item in resumo}

    assert por_nome["Camiseta"]["quantidade"] == 4
    assert por_nome["Camiseta"]["valor_total"] == 199.6
    assert por_nome["Calça"]["quantidade"] == 2
    assert por_nome["Calça"]["valor_total"] == 199.8
    assert por_nome["Tênis"]["quantidade"] == 1
    assert por_nome["Tênis"]["valor_total"] == 199.9


def test_produto_mais_vendido_por_quantidade() -> None:
    resumo = agrupar_por_produto(_vendas_exemplo())
    mais = produto_mais_vendido(resumo)
    assert mais is not None
    assert mais["produto"] == "Camiseta"
    assert mais["quantidade"] == 4


def test_produto_mais_vendido_empate_por_valor() -> None:
    resumo = [
        {"produto": "A", "quantidade": 2, "valor_total": 50.0},
        {"produto": "B", "quantidade": 2, "valor_total": 80.0},
    ]
    mais = produto_mais_vendido(resumo)
    assert mais is not None
    assert mais["produto"] == "B"


def test_produto_mais_vendido_empate_alfabetico() -> None:
    resumo = [
        {"produto": "Zebra", "quantidade": 2, "valor_total": 50.0},
        {"produto": "Abacate", "quantidade": 2, "valor_total": 50.0},
    ]
    mais = produto_mais_vendido(resumo)
    assert mais is not None
    assert mais["produto"] == "Abacate"


def test_produto_mais_vendido_lista_vazia() -> None:
    assert produto_mais_vendido([]) is None


def test_gerar_relatorio() -> None:
    relatorio = gerar_relatorio(_vendas_exemplo())
    assert relatorio["valor_total"] == 599.3
    assert relatorio["periodo"] is None
    assert relatorio["produto_mais_vendido"]["produto"] == "Camiseta"
    assert len(relatorio["vendas_por_produto"]) == 3


def test_gerar_relatorio_com_periodo() -> None:
    vendas = [
        Sale("Camiseta", 1, 49.9, date(2025, 1, 10)),
        Sale("Calça", 1, 99.9, date(2025, 2, 10)),
    ]
    relatorio = gerar_relatorio(vendas, date(2025, 1, 1), date(2025, 3, 31))
    assert relatorio["periodo"] == {
        "inicio": "2025-01-01",
        "fim": "2025-03-31",
    }


def test_gerar_relatorio_vazio() -> None:
    relatorio = gerar_relatorio([])
    assert relatorio["valor_total"] == 0.0
    assert relatorio["produto_mais_vendido"] is None
    assert relatorio["vendas_por_produto"] == []
