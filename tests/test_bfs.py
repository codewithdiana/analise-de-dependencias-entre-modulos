"""
Testes unitários — BFS (cone de impacto)
Execute com: pytest tests/test_bfs.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.core.grafo import Grafo
from src.algorithms.bfs import calcular_cone_impacto


@pytest.fixture
def grafo_aciclico():
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("A", "C")
    g.adicionar_aresta("B", "D")
    g.adicionar_aresta("C", "D")
    return g


class TestarBFS:

    def testar_cenario_padrao(self, grafo_aciclico):
        resultado = calcular_cone_impacto(grafo_aciclico, "A")
        assert set(resultado["impactados"]) == {"B", "C", "D"}

    def testar_modulo_folha(self, grafo_aciclico):
        resultado = calcular_cone_impacto(grafo_aciclico, "D")
        assert resultado["impactados"] == []

    def testar_grafo_vazio(self):
        g = Grafo()
        resultado = calcular_cone_impacto(g, "X")
        assert resultado["impactados"] == []

    def testar_camadas_de_impacto(self, grafo_aciclico):
        resultado = calcular_cone_impacto(grafo_aciclico, "A")
        assert set(resultado["camadas"][0]) == {"B", "C"}
        assert set(resultado["camadas"][1]) == {"D"}

    def testar_modulo_inexistente(self, grafo_aciclico):
        resultado = calcular_cone_impacto(grafo_aciclico, "Z")
        assert resultado["impactados"] == []
