"""
Módulo: bfs.py
Algoritmo: Busca em Largura (BFS) com Grafo Reverso
Responsabilidade: calcular o cone de impacto de um módulo — todos os módulos
que precisam ser revalidados após uma mudança no módulo de entrada.

Complexidade de tempo:  O(V + E)
Complexidade de espaço: O(V + E) — grafo reverso + fila + conjunto de visitados
"""

from collections import deque

def calcular_cone_impacto(grafo, vertice_inicial: str) -> dict:
    """
    Executa BFS REVERSA a partir de vertice_inicial no grafo.
    Retorna:
        {
            "inicio": str,
            "impactados": [v1, v2, ...],   # módulos que IMPORTAM o vértice inicial
            "camadas": [[camada1], [camada2], ...]  # ordenados por distância de impacto
        }
    """
    if vertice_inicial not in grafo.obter_vertices():
        return {"inicio": vertice_inicial, "impactados": [], "camadas": []}

    grafo_reverso = {v: [] for v in grafo.obter_vertices()}
    for origem, destino in grafo.obter_arestas():
        grafo_reverso[destino].append(origem)

    visitados = {vertice_inicial}     
    fila = deque([(vertice_inicial, 0)])
    impactados = []
    camadas = []

    while fila:
        vertice, profundidade = fila.popleft()

        if vertice != vertice_inicial:

            while len(camadas) <= profundidade - 1:
                camadas.append([])
            camadas[profundidade - 1].append(vertice)
            impactados.append(vertice)

        for dependente in grafo_reverso[vertice]:
            if dependente not in visitados:
                visitados.add(dependente)
                fila.append((dependente, profundidade + 1))

    return {
        "inicio": vertice_inicial,
        "impactados": impactados,
        "camadas": camadas
    }
