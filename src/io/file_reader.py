"""
Módulo: file_reader.py
Responsabilidade: ler arquivos JSON ou CSV e construir o grafo de dependências.
"""

import json
import csv
import os
from src.core.grafo import Grafo


def carregar_grafo(filepath: str) -> Grafo:
    """
    Carrega um grafo a partir de arquivo JSON ou CSV.
    Detecta o formato pela extensão do arquivo.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado😢: {filepath}")

    extensao = os.path.splitext(filepath)[1].lower()

    if extensao == ".json":
        return _carregar_via_json(filepath)
    elif extensao == ".csv":
        return _carregar_via_csv(filepath)
    else:
        raise ValueError(f"Formato não invalido!: {extensao}. Use .json ou .csv")


def _carregar_via_json(filepath: str) -> Grafo:
    """
    Formato esperado:
    {
        "modulos": ["a.py", "b.py", ...],
        "dependencias": [
            {"origem": "a.py", "destino": "b.py"},
            ...
        ]
    }
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = Grafo()

    for module in data.get("modulos", []):
        graph.adicionar_vertice(module)

    for dep in data.get("dependencias", []):
        graph.adicionar_aresta(dep["origem"], dep["destino"])

    return graph


def _carregar_via_csv(filepath: str) -> Grafo:
    """
    Formato esperado:
    origem,destino
    a.py,b.py
    ...
    """
    graph = Grafo()

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            graph.adicionar_aresta(row["origem"], row["destino"])

    return graph
