"""Leitura e validação do CSV de vendas."""

from __future__ import annotations

import csv
import logging
from datetime import date
from pathlib import Path

from vendas_cli.core import Sale

logger = logging.getLogger(__name__)

COLUNAS_OBRIGATORIAS = ("produto", "quantidade", "preco_unitario")


def ler_vendas(caminho: Path) -> list[Sale]:
    """Lê o CSV e devolve uma lista de Sale.

    Linhas com dados inválidos são ignoradas (com warning no log).
    Levanta ValueError se faltar coluna obrigatória ou se não houver
    nenhuma linha válida.
    """
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    vendas: list[Sale] = []
    texto = _ler_texto(caminho)

    reader = csv.DictReader(texto.splitlines())

    if reader.fieldnames is None:
        raise ValueError(f"CSV vazio ou sem cabeçalho: {caminho}")

    colunas = {c.strip() for c in reader.fieldnames}
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in colunas]
    if faltando:
        raise ValueError(
            f"CSV sem colunas obrigatórias: {', '.join(faltando)}. "
            f"Esperado: {', '.join(COLUNAS_OBRIGATORIAS)}"
        )

    tem_data = "data" in colunas

    for numero, linha in enumerate(reader, start=2):
        try:
            produto = (linha.get("produto") or "").strip()
            if not produto:
                raise ValueError("produto vazio")

            quantidade = int(linha["quantidade"])
            preco_unitario = float(linha["preco_unitario"])

            if quantidade < 0 or preco_unitario < 0:
                raise ValueError("quantidade e preco_unitario devem ser >= 0")

            data_venda: date | None = None
            if tem_data:
                raw = (linha.get("data") or "").strip()
                if raw:
                    data_venda = date.fromisoformat(raw)

            vendas.append(
                Sale(
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario,
                    data=data_venda,
                )
            )
        except (ValueError, TypeError, KeyError) as exc:
            logger.warning("Linha %s ignorada: %s", numero, exc)

    if not vendas:
        raise ValueError(f"Nenhuma venda válida encontrada em: {caminho}")

    logger.info("Lidas %s vendas de %s", len(vendas), caminho)
    return vendas


def _ler_texto(caminho: Path) -> str:
    """Lê o arquivo tentando UTF-8 e, se falhar, Latin-1."""
    bruto = caminho.read_bytes()
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            return bruto.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Não foi possível decodificar o arquivo: {caminho}")


def filtrar_por_periodo(
    vendas: list[Sale],
    inicio: date | None = None,
    fim: date | None = None,
) -> list[Sale]:
    """Filtra vendas pelo intervalo inclusivo [inicio, fim].

    Se algum filtro for pedido e nenhuma venda tiver data, levanta ValueError.
    """
    if inicio is None and fim is None:
        return vendas

    if inicio is not None and fim is not None and inicio > fim:
        raise ValueError(
            f"--start ({inicio.isoformat()}) não pode ser maior que "
            f"--end ({fim.isoformat()})"
        )

    if not any(v.data is not None for v in vendas):
        raise ValueError(
            "CSV não possui coluna 'data'; não é possível filtrar por período. "
            "Inclua uma coluna 'data' no formato YYYY-MM-DD ou remova --start/--end."
        )

    filtradas: list[Sale] = []
    for venda in vendas:
        if venda.data is None:
            continue
        if inicio is not None and venda.data < inicio:
            continue
        if fim is not None and venda.data > fim:
            continue
        filtradas.append(venda)

    logger.info(
        "Filtro de período: %s → %s venda(s)",
        f"{inicio or '...'} a {fim or '...'}",
        len(filtradas),
    )
    return filtradas
