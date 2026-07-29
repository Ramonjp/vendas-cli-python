"""Testes end-to-end da CLI."""

from __future__ import annotations

import json
from pathlib import Path

from vendas_cli.cli import main

FIXTURES = Path(__file__).parent / "fixtures"

CSV_COM_DATA = """\
produto,quantidade,preco_unitario,data
Camiseta,3,49.9,2025-01-15
Calça,2,99.9,2025-02-10
Camiseta,1,49.9,2025-03-05
Tênis,1,199.9,2025-04-20
"""


def test_cli_text_ok(capsys) -> None:
    code = main([str(FIXTURES / "vendas_ok.csv"), "--format", "text"])
    assert code == 0
    out = capsys.readouterr().out
    assert "Camiseta" in out
    assert "TOTAL" in out


def test_cli_json_ok(capsys) -> None:
    code = main([str(FIXTURES / "vendas_ok.csv"), "--format", "json"])
    assert code == 0
    dados = json.loads(capsys.readouterr().out)
    assert dados["valor_total"] == 599.3
    assert dados["produto_mais_vendido"]["produto"] == "Camiseta"


def test_cli_com_filtro_data(tmp_path: Path, capsys) -> None:
    caminho = tmp_path / "vendas.csv"
    caminho.write_text(CSV_COM_DATA, encoding="utf-8")
    code = main(
        [
            str(caminho),
            "--format",
            "json",
            "--start",
            "2025-01-01",
            "--end",
            "2025-03-31",
        ]
    )
    assert code == 0
    dados = json.loads(capsys.readouterr().out)
    assert dados["periodo"]["inicio"] == "2025-01-01"
    assert dados["periodo"]["fim"] == "2025-03-31"
    assert len(dados["vendas_por_produto"]) == 2


def test_cli_arquivo_inexistente() -> None:
    code = main(["/tmp/nao_existe_xyz.csv"])
    assert code == 1


def test_cli_filtro_sem_coluna_data() -> None:
    code = main(
        [
            str(FIXTURES / "vendas_ok.csv"),
            "--start",
            "2025-01-01",
        ]
    )
    assert code == 1


def test_cli_start_maior_que_end(tmp_path: Path) -> None:
    caminho = tmp_path / "vendas.csv"
    caminho.write_text(CSV_COM_DATA, encoding="utf-8")
    code = main(
        [
            str(caminho),
            "--start",
            "2025-06-01",
            "--end",
            "2025-01-01",
        ]
    )
    assert code == 1
