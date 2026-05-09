"""
Testes unitários — DFS (detecção de ciclos)
Execute com: pytest tests/test_dfs.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.core.grafo import Grafo
from src.algorithms.dfs import detectar_ciclos


@pytest.fixture
def grafo_aciclico():
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("A", "C")
    g.adicionar_aresta("B", "D")
    g.adicionar_aresta("C", "D")
    return g

@pytest.fixture
def gafo_ciclico():
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("B", "C")
    g.adicionar_aresta("C", "A")
    return g


class TestarDFS:

    def testar_sucesso_sem_ciclo(self, grafo_aciclico):
        result = detectar_ciclos(grafo_aciclico)
        assert result["has_cycle"] is False
        assert result["cycles"] == []

    def testar_ciclo_detectado(self, gafo_ciclico):
        result = detectar_ciclos(gafo_ciclico)
        assert result["has_cycle"] is True
        assert len(result["cycles"]) >= 1

    def testar_grafo_vazio(self):
        g = Grafo()
        result = detectar_ciclos(g)
        assert result["has_cycle"] is False

    def testar_caminho_do_ciclo_completo(self, gafo_ciclico):
        result = detectar_ciclos(gafo_ciclico)
        cycle = result["cycles"][0]
        # O ciclo deve começar e terminar no mesmo vértice
        assert cycle[0] == cycle[-1]

    def testar_grafo_desconexo_sem_ciclo(self):
        g = Grafo()
        g.adicionar_aresta("A", "B")
        g.adicionar_aresta("C", "D")
        result = detectar_ciclos(g)
        assert result["has_cycle"] is False