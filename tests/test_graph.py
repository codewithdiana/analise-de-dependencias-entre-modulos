"""
Testes unitários — Graph
Execute com: pytest tests/test_graph.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.grafo import Grafo


class TestGraph:

    def testar_adicionar_vertice(self):
        g = Grafo()
        g.adicionar_vertice("X")
        assert "X" in g.obter_vertices()

    def testar_adicionar_aresta_cria_vertices(self):
        g = Grafo()
        g.adicionar_aresta("A", "B")
        assert "A" in g.obter_vertices()
        assert "B" in g.obter_vertices()

    def testar_obter_vizinhos(self):
        g = Grafo()
        g.adicionar_aresta("A", "B")
        g.adicionar_aresta("A", "C")
        assert set(g.obter_vizinhos("A")) == {"B", "C"}

    def testar_grafo_vazio(self):
        g = Grafo()
        assert g.obter_vertices() == []
        assert g.obter_arestas() == []

    def testar_evitar_arestas_duplicadas(self):
        g = Grafo()
        g.adicionar_aresta("A", "B")
        g.adicionar_aresta("A", "B")
        assert g.obter_vizinhos("A").count("B") == 1

    def testar_grau_de_entrada(self):
        g = Grafo()
        g.adicionar_aresta("A", "B")
        g.adicionar_aresta("C", "B")
        assert g.grau_de_entrada("B") == 2
        assert g.grau_de_entrada("A") == 0