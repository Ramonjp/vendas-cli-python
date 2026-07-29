"""Modelo de venda e cálculos do relatório."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Sale:
    """Uma linha de venda do CSV."""

    produto: str
    quantidade: int
    preco_unitario: float
    data: date | None = None

    @property
    def valor_total(self) -> float:
        return round(self.quantidade * self.preco_unitario, 2)


def agrupar_por_produto(vendas: list[Sale]) -> list[dict]:
    """Soma quantidade e valor por produto (ordenado por valor desc)."""
    agrupado: dict[str, dict] = {}

    for venda in vendas:
        item = agrupado.setdefault(
            venda.produto,
            {"produto": venda.produto, "quantidade": 0, "valor_total": 0.0},
        )
        item["quantidade"] += venda.quantidade
        item["valor_total"] = round(item["valor_total"] + venda.valor_total, 2)

    return sorted(agrupado.values(), key=lambda x: (-x["valor_total"], x["produto"]))


def produto_mais_vendido(resumo: list[dict]) -> dict | None:
    """Produto com maior quantidade.

    Empate: maior valor_total; empate final: ordem alfabética.
    """
    if not resumo:
        return None

    return min(
        resumo,
        key=lambda x: (-x["quantidade"], -x["valor_total"], x["produto"]),
    )


def gerar_relatorio(
    vendas: list[Sale],
    inicio: date | None = None,
    fim: date | None = None,
) -> dict:
    """Monta o dicionário final do relatório."""
    por_produto = agrupar_por_produto(vendas)
    valor_total = round(sum(v.valor_total for v in vendas), 2)
    mais_vendido = produto_mais_vendido(por_produto)

    periodo = None
    if inicio is not None or fim is not None:
        periodo = {
            "inicio": inicio.isoformat() if inicio else None,
            "fim": fim.isoformat() if fim else None,
        }

    return {
        "periodo": periodo,
        "valor_total": valor_total,
        "produto_mais_vendido": mais_vendido,
        "vendas_por_produto": por_produto,
    }
