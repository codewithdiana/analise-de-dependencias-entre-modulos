"""
Módulo: grafo.py
Responsabilidade: representar o grafo dirigido como lista de adjacência.
Complexidade de espaço: O(V + E)
"""


class Grafo:
    def __init__(self):
        # Dicionário: vértice -> lista de vizinhos  O(1) por inserção
        self.lista_adjacencia = {}

    def adicionar_vertice(self, vertice: str):
        """Adiciona um vértice se ainda não existir. O(1)"""
        if vertice not in self.lista_adjacencia:
            self.lista_adjacencia[vertice] = []

    def adicionar_aresta(self, origin: str, destination: str):
        """Adiciona aresta dirigida origin → destination. O(1)"""
        self.adicionar_vertice(origin)
        self.adicionar_vertice(destination)
        if destination not in self.lista_adjacencia[origin]:
            self.lista_adjacencia[origin].append(destination)

    def obter_vizinhos(self, vertice: str) -> list:
        """Retorna lista de vizinhos de um vértice. O(1)"""
        return self.lista_adjacencia.get(vertice, [])

    def obter_vertices(self) -> list:
        """Retorna todos os vértices do grafo. O(V)"""
        return list(self.lista_adjacencia.keys())

    def obter_arestas(self) -> list:
        """Retorna todas as arestas como tuplas (origem, destino). O(V + E)"""
        arestas = []
        for origem, vizinhos in self.lista_adjacencia.items():
            for destino in vizinhos:
                arestas.append((origem, destino))
        return arestas

    def grau_de_entrada(self, vertice: str) -> int:
        """Calcula o grau de entrada de um vértice. O(V + E)"""
        total = 0
        for vizinhos in self.lista_adjacencia.values():
            if vertice in vizinhos:
                total += 1
        return total

    def carregar_do_json(self, data: dict):
        """
        Carrega dados de um JSON no formato:
        {
            "A": ["B", "C"],
            "B": ["D"],
            "C": [],
            "D": []
        }
        """
        self.lista_adjacencia.clear()  # limpa grafo antes de carregar

        for origem, destinos in data.items():
            if not destinos:
                self.adicionar_vertice(origem)

            for destino in destinos:
                self.adicionar_aresta(origem, destino)

    def to_dict(self) -> dict:
        """Retorna o grafo como dicionário (útil para debug/UI)."""
        return self.lista_adjacencia

    def __repr__(self):
        linhas = ["Grafo dirigido:"]
        for vertice, vizinhos in self.lista_adjacencia.items():
            linhas.append(f"  {vertice} → {vizinhos}")
        return "\n".join(linhas)