"""
Módulo: kahn.py
Algoritmo: Algoritmo de Kahn (ordenação topológica)
Responsabilidade: determinar a ordem segura de compilação/execução dos módulos.
Suporta grafos desconexos — processa todos os componentes.

Complexidade de tempo:  O(V + E)
Complexidade de espaço: O(V + E) — fila + array de graus de entrada
"""

from collections import deque


def ordenacao_topologica(grafo) -> dict:
    """
    Executa o algoritmo de Kahn sobre o grafo.
    Retorna:
        {
            "successo": bool,         # False se houver ciclo
            "ordem": [v1, v2, ...],  # sequência segura de build
            "nao_processados": [...]     # vértices não processados (apenas se houver ciclo)
        }
    Complexidade: O(V + E)
    """
    vertices = grafo.obter_vertices()   # O(V)

    # Calcular grau de entrada de cada vértice — O(V + E)
    grau_de_entrada = {v: 0 for v in vertices}
    for origem, destino in grafo.obter_arestas():
        grau_de_entrada[destino] += 1

    # Enfileirar vértices com grau de entrada zero — O(V)
    fila = deque([v for v in vertices if grau_de_entrada[v] == 0])
    ordem = []

    while fila:                          # cada vértice entra na fila uma vez — O(V)
        vertice = fila.popleft()
        ordem.append(vertice)

        for vizinhos in grafo.obter_vizinhos(vertice):   # O(E) no total
            grau_de_entrada[vizinhos] -= 1
            if grau_de_entrada[vizinhos] == 0:
                fila.append(vizinhos)

    # Se nem todos os vértices foram processados → há ciclo
    nao_processados = [v for v in vertices if v not in ordem]

    return {
        "successo": len(ordem) == len(vertices),
        "ordem": ordem,
        "nao_processados": nao_processados
    }