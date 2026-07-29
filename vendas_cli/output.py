"""Formatação do relatório em texto (tabela) ou JSON."""

from __future__ import annotations

import json


def formatar_texto(relatorio: dict) -> str:
    """Tabela legível no terminal."""
    linhas: list[str] = []

    periodo = relatorio.get("periodo")
    if periodo:
        inicio = periodo.get("inicio") or "..."
        fim = periodo.get("fim") or "..."
        linhas.append(f"Período: {inicio} a {fim}")
        linhas.append("")

    linhas.append(f"{'Produto':<20} {'Quantidade':>10} {'Valor Total':>14}")
    linhas.append("-" * 46)

    for item in relatorio["vendas_por_produto"]:
        linhas.append(
            f"{item['produto']:<20} {item['quantidade']:>10} "
            f"{item['valor_total']:>14.2f}"
        )

    if not relatorio["vendas_por_produto"]:
        linhas.append("(nenhuma venda no período)")

    linhas.append("-" * 46)
    linhas.append(f"{'TOTAL':<20} {'':>10} {relatorio['valor_total']:>14.2f}")

    mais = relatorio.get("produto_mais_vendido")
    if mais:
        linhas.append("")
        linhas.append(
            f"Produto mais vendido: {mais['produto']} "
            f"({mais['quantidade']} un., R$ {mais['valor_total']:.2f})"
        )
    else:
        linhas.append("")
        linhas.append("Produto mais vendido: (nenhum)")

    return "\n".join(linhas)


def formatar_json(relatorio: dict) -> str:
    """JSON indentado, com acentos preservados."""
    return json.dumps(relatorio, ensure_ascii=False, indent=2)


def formatar(relatorio: dict, formato: str) -> str:
    """Escolhe entre texto e JSON."""
    if formato == "json":
        return formatar_json(relatorio)
    if formato == "text":
        return formatar_texto(relatorio)
    raise ValueError(f"Formato inválido: {formato!r}. Use 'text' ou 'json'.")
