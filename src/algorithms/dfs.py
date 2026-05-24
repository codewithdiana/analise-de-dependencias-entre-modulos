"""
Módulo: dfs.py
Algoritmo: DFS com coloração de vértices (branco/cinza/preto)
Responsabilidade: detectar ciclos em grafos dirigidos e reportar o caminho completo.

Complexidade de tempo:  O(V + E)
Complexidade de espaço: O(V) — array de cores + pilha de recursão
"""

BRANCO = "branco"   # não visitado
CINZA  = "cinza"    # em processamento (na pilha de recursão)
PRETO = "preto"   # processamento concluído

def detectar_ciclos(grafo) -> dict:
    """
    Executa DFS com coloração em todos os vértices do grafo.
    Retorna:
        {
            "tem_ciclos": bool,
            "ciclos": [ [v1, v2, ..., v1], ... ]  # cada ciclo como caminho
        }
    Complexidade: O(V + E)
    """
    cores = {v: BRANCO for v in grafo.obter_vertices()}   # O(V)
    ciclos = []

    def visitar_dfs(vertice, caminho):
        cores[vertice] = CINZA          # marca como em processamento
        caminho.append(vertice)

        for vizinho in grafo.obter_vizinhos(vertice):   # O(grau(vertex))
            if cores[vizinho] == CINZA:
                # Aresta de retorno encontrada → ciclo detectado
                # Reconstruir o caminho do ciclo a partir de 'path'
                ciclo_inicial = caminho.index(vizinho)
                ciclo = caminho[ciclo_inicial:] + [vizinho]
                ciclos.append(ciclo)

            elif cores[vizinho] == BRANCO:
                visitar_dfs(vizinho, caminho)

        caminho.pop()
        cores[vertice] = PRETO         # processamento concluído

    for vertice in grafo.obter_vertices():   # O(V)
        if cores[vertice] == BRANCO:
            visitar_dfs(vertice, [])

    return {
        "tem_ciclos": len(ciclos) > 0,
        "ciclos": ciclos
    }
