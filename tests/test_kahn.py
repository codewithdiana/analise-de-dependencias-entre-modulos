"""
Testes unitários — Algoritmo de Kahn (ordenação topológica)
Execute com: pytest tests/test_kahn.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.core.grafo import Grafo
from src.algorithms.kahn import ordenacao_topologica


@pytest.fixture
def grafo_aciclico():
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("A", "C")
    g.adicionar_aresta("B", "D")
    g.adicionar_aresta("C", "D")
    return g

@pytest.fixture
def grafo_ciclico():
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("B", "C")
    g.adicionar_aresta("C", "A")
    return g


class TestKahn:

    def testar_ordem_DAG_valida(self, grafo_aciclico):
        result = ordenacao_topologica(grafo_aciclico)
        assert result["successo"] is True
        ordem = result["ordem"]
        assert ordem.index("A") < ordem.index("B")
        assert ordem.index("A") < ordem.index("C")
        assert ordem.index("B") < ordem.index("D")
        assert ordem.index("C") < ordem.index("D")

    def testar_falha_por_ciclo(self, grafo_ciclico):
        result = ordenacao_topologica(grafo_ciclico)
        assert result["successo"] is False
        assert len(result["nao_processados"]) > 0

    def testar_grafo_vazio(self):
        g = Grafo()
        result = ordenacao_topologica(g)
        assert result["successo"] is True
        assert result["ordem"] == []

    def testar_grafo_desconexo(self):
        g = Grafo()
        g.adicionar_aresta("A", "B")
        g.adicionar_aresta("C", "D")
        result = ordenacao_topologica(g)
        assert result["successo"] is True
        assert len(result["ordem"]) == 4

    def testar_todos_vertices_na_ordem(self, grafo_aciclico):
        result = ordenacao_topologica(grafo_aciclico)
        assert set(result["ordem"]) == set(grafo_aciclico.obter_vertices())
