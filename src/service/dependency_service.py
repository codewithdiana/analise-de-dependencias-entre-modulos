"""
Módulo: dependency_service.py
Responsabilidade: orquestrar os fluxos do sistema (Padrão Facade).
"""

from src.core.grafo import Grafo
from src.algorithms.dfs import detectar_ciclos
from src.algorithms.kahn import ordenacao_topologica
from src.algorithms.bfs import calcular_cone_impacto

class DependencyService:

    def __init__(self, graph: Grafo):
        self.graph = graph

    def detectar_ciclos(self) -> dict:
        return detectar_ciclos(self.graph)

    def ordenacao_topologica(self) -> dict:
        return ordenacao_topologica(self.graph)

    def calcular_cone_impacto(self, module: str) -> dict:
        return calcular_cone_impacto(self.graph, module)

    def obter_resumo(self) -> dict:
        return {
            "total_vertices": len(self.graph.obter_vertices()),
            "total_arestas": len(self.graph.obter_arestas()),
            "lista_modulos": self.graph.obter_vertices()
        }
