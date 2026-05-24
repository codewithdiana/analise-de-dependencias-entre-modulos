"""
Módulo: file_reader.py
Responsabilidade: ler arquivos JSON, CSV ou ZIP e construir o grafo de dependências.
"""

import json
import csv
import os
import zipfile
import tempfile
import shutil
from src.core.grafo import Grafo
from src.io.py_parser import analisar_projeto_python


def carregar_grafo(filepath: str) -> Grafo:
    """
    Carrega um grafo a partir de arquivo JSON, CSV ou ZIP.
    Detecta o formato pela extensão do arquivo.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado😢: {filepath}")

    extensao = os.path.splitext(filepath)[1].lower()

    if extensao == ".json":
        return _carregar_via_json(filepath)
    elif extensao == ".csv":
        return _carregar_via_csv(filepath)
    elif extensao == ".zip":
        return _carregar_via_zip(filepath)
    else:
        raise ValueError(f"Formato inválido!: {extensao}. Use .json, .csv ou .zip")


def _carregar_via_json(filepath: str) -> Grafo:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return _construir_grafo_de_dict(data)


def _carregar_via_csv(filepath: str) -> Grafo:
    graph = Grafo()
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            o = row.get("origem") or row.get("source") or row.get("from")
            d = row.get("destino") or row.get("target") or row.get("to")
            if o and d:
                graph.adicionar_aresta(o, d)
    return graph


def _carregar_via_zip(filepath: str) -> Grafo:
    """
    Descompacta um ZIP e analisa os arquivos .py para gerar o grafo.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Analisa o projeto descompactado
        projeto_info = analisar_projeto_python(temp_dir)
        return _construir_grafo_de_dict(projeto_info)
    finally:
        shutil.rmtree(temp_dir)


def _construir_grafo_de_dict(data: dict) -> Grafo:
    """
    Auxiliar para criar o objeto Grafo a partir de um dicionário de dados.
    """
    graph = Grafo()
    for module in data.get("modulos", []):
        graph.adicionar_vertice(module)
    for dep in data.get("dependencias", []):
        graph.adicionar_aresta(dep["origem"], dep["destino"])
    return graph
