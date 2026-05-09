"""
Módulo: bfs.py
Algoritmo: Busca em Largura (BFS)
Responsabilidade: calcular o cone de impacto de um módulo — todos os módulos
que precisam ser revalidados após uma mudança no módulo de entrada.

Complexidade de tempo:  O(V + E)
Complexidade de espaço: O(V) — fila + conjunto de visitados
"""

from collections import deque


def calcular_cone_impacto(grafo, vertice_inicial: str) -> dict:
    """
    Executa BFS a partir de vertice_inicial no grafo.
    Retorna:
        {
            "inicio": str,
            "impactados": [v1, v2, ...],   # módulos alcançáveis, por camadas
            "camadas": [[camada1], [camada2], ...]  # ordenados por distância
        }
    Complexidade: O(V + E)
    """
    if vertice_inicial not in grafo.obter_vertices():
        return {"inicio": vertice_inicial, "impactados": [], "camadas": []}

    visitados = {vertice_inicial}      # O(V) no pior caso
    fila = deque([(vertice_inicial, 0)])
    impactados = []
    camadas = []

    while fila:                   # cada vértice entra na fila uma vez — O(V)
        vertice, profundidade = fila.popleft()

        if vertice != vertice_inicial:
            # Garantir que a camada existe
            while len(camadas) <= profundidade - 1:
                camadas.append([])
            camadas[profundidade - 1].append(vertice)
            impactados.append(vertice)

        for vizinhos in grafo.obter_vizinhos(vertice):   # O(E) no total
            if vizinhos not in visitados:
                visitados.add(vizinhos)
                fila.append((vizinhos, profundidade + 1))

    return {
        "inicio": vertice_inicial,
        "impactados": impactados,
        "camadas": camadas
    }