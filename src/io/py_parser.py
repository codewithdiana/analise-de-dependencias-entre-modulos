"""
Módulo: py_parser.py
Responsabilidade: Analisar arquivos .py e extrair dependências (imports).
"""

import ast
import os
from typing import List


def extrair_dependencias_de_arquivo(filepath: str) -> List[str]:
    """
    Lê um arquivo .py e retorna uma lista de módulos internos importados.
    """
    dependencias = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            # Caso 1: import modulo
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependencias.append(alias.name)

            # Caso 2: from modulo import algo
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    dependencias.append(node.module)

    except Exception as e:
        print(f"  [Aviso] Erro ao processar {filepath}: {e}")

    return dependencias


def analisar_projeto_python(root_path: str) -> dict:
    """
    Percorre um diretório, encontra arquivos .py e constrói o mapa de dependências.
    """
    projeto_info = {
        "modulos": [],
        "dependencias": []
    }
    
    # Otimização O(1) para checagem rápida
    deps_unicas = set() 

    # 1. Mapear todos os arquivos .py como módulos (vértices)
    arquivos_py = []
    for root, dirs, files in os.walk(root_path):
        
        # 🚀 A MÁGICA DA VELOCIDADE ESTÁ AQUI:
        # Força o Python a ignorar pastas inúteis e gigantescas!
        dirs[:] = [d for d in dirs if d not in ['.venv', 'venv', 'env', '__pycache__', '.git', 'node_modules', '.idea', '.vscode']]

        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), root_path)
                rel_path_norm = rel_path.replace(os.sep, "/")
                projeto_info["modulos"].append(rel_path_norm)
                arquivos_py.append((os.path.join(root, file), rel_path_norm))

    # 2. Extrair dependências de cada arquivo
    for full_path, rel_path_origem in arquivos_py:
        deps_encontradas = extrair_dependencias_de_arquivo(full_path)

        for dep in deps_encontradas:
            caminho_tentativa = dep.replace(".", "/") + ".py"

            possiveis_destinos = [
                caminho_tentativa,
                "src/" + caminho_tentativa,
                dep.replace(".", "/") + "/__init__.py"
            ]

            for destino in possiveis_destinos:
                destino_norm = destino.replace("//", "/")

                if destino_norm in projeto_info["modulos"]:
                    if rel_path_origem != destino_norm:
                        nova_dep = (rel_path_origem, destino_norm) 
                        
                        if nova_dep not in deps_unicas:
                            deps_unicas.add(nova_dep)
                            projeto_info["dependencias"].append({"origem": rel_path_origem, "destino": destino_norm})
                    break

    return projeto_info
