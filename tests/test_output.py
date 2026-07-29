"""Testes de formatação (texto e JSON)."""

from __future__ import annotations

import json

import pytest

from vendas_cli.output import formatar, formatar_json, formatar_texto


def _relatorio() -> dict:
    return {
        "periodo": {"inicio": "2025-01-01", "fim": "2025-03-31"},
        "valor_total": 399.4,
        "produto_mais_vendido": {
            "produto": "Camiseta",
            "quantidade": 4,
            "valor_total": 199.6,
        },
        "vendas_por_produto": [
            {"produto": "Camiseta", "quantidade": 4, "valor_total": 199.6},
            {"produto": "Calça", "quantidade": 2, "valor_total": 199.8},
        ],
    }


def test_formatar_json_valido() -> None:
    texto = formatar_json(_relatorio())
    dados = json.loads(texto)
    assert dados["valor_total"] == 399.4
    assert dados["produto_mais_vendido"]["produto"] == "Camiseta"
    assert len(dados["vendas_por_produto"]) == 2
    assert dados["periodo"]["inicio"] == "2025-01-01"


def test_formatar_texto_contem_produtos_e_total() -> None:
    texto = formatar_texto(_relatorio())
    assert "Camiseta" in texto
    assert "Calça" in texto
    assert "399.40" in texto
    assert "Produto mais vendido: Camiseta" in texto
    assert "Período: 2025-01-01 a 2025-03-31" in texto


def test_formatar_texto_sem_vendas() -> None:
    relatorio = {
        "periodo": None,
        "valor_total": 0.0,
        "produto_mais_vendido": None,
        "vendas_por_produto": [],
    }
    texto = formatar_texto(relatorio)
    assert "nenhuma venda" in texto
    assert "Produto mais vendido: (nenhum)" in texto


def test_formatar_dispatcher() -> None:
    relatorio = _relatorio()
    assert formatar(relatorio, "json").startswith("{")
    assert "Produto" in formatar(relatorio, "text")


def test_formatar_invalido() -> None:
    with pytest.raises(ValueError, match="Formato inválido"):
        formatar(_relatorio(), "xml")
