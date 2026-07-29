"""Entrypoint da CLI vendas-cli."""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

from vendas_cli.core import gerar_relatorio
from vendas_cli.output import formatar
from vendas_cli.parser import filtrar_por_periodo, ler_vendas

logger = logging.getLogger(__name__)


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vendas-cli",
        description="Gera relatório de vendas a partir de um arquivo CSV.",
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        help="Caminho do arquivo CSV de vendas",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        dest="formato",
        help="Formato de saída (default: text)",
    )
    parser.add_argument(
        "--start",
        type=date.fromisoformat,
        default=None,
        metavar="YYYY-MM-DD",
        help="Data inicial do filtro (inclusiva)",
    )
    parser.add_argument(
        "--end",
        type=date.fromisoformat,
        default=None,
        metavar="YYYY-MM-DD",
        help="Data final do filtro (inclusiva)",
    )
    return parser


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )


def main(argv: list[str] | None = None) -> int:
    """Orquestra a CLI. Retorna o exit code (0 = sucesso)."""
    parser = criar_parser()
    args = parser.parse_args(argv)
    configurar_logging()

    try:
        vendas = ler_vendas(args.csv_path)
        vendas = filtrar_por_periodo(vendas, args.start, args.end)
        relatorio = gerar_relatorio(vendas, args.start, args.end)
        print(formatar(relatorio, args.formato))
        return 0
    except (FileNotFoundError, ValueError) as exc:
        logger.error("%s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
