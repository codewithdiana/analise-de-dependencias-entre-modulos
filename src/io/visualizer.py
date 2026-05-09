"""
Módulo: visualizer.py
Responsabilidade: gerar visualização gráfica do grafo de dependências,
com destaque visual para ciclos (vermelho) e cone de impacto (laranja).
"""

import networkx as nx
import matplotlib.pyplot as plt


def desenhar_grafo(
    graph,
    ciclos: list = None,
    impacto: list = None,
    title: str = "Grafo de Dependências"
):
    ciclos = ciclos or []
    impacto = impacto or []

    # ── Construção do grafo ───────────────────────────────
    G = nx.DiGraph()
    G.add_nodes_from(graph.obter_vertices())
    G.add_edges_from(graph.obter_arestas())

    pos = nx.spring_layout(
        G,
        seed=42,
        k=1.2,
        iterations=100
)

    # ── Classificação de arestas ──────────────────────────
    arestas_do_ciclo = set()
    for ciclo in ciclos:
        for i in range(len(ciclo) - 1):
            arestas_do_ciclo.add((ciclo[i], ciclo[i + 1]))

    conjunto_de_impacto = set(impacto)

    arestas_impactadas = set()
    for origem, destino in graph.obter_arestas():
        if destino in conjunto_de_impacto:
            arestas_impactadas.add((origem, destino))

    arestas_normais = [
        e for e in G.edges()
        if e not in arestas_do_ciclo and e not in arestas_impactadas
    ]

    # ── Classificação de nós ──────────────────────────────
    vertices_do_ciclo = set()
    for ciclo in ciclos:
        vertices_do_ciclo.update(ciclo)

    nos_normais = [
        v for v in G.nodes()
        if v not in vertices_do_ciclo and v not in conjunto_de_impacto
    ]

    # ── Desenho ──────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 6))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)

    # Nós normais
    nx.draw_networkx_nodes(
        G, pos, nodelist=nos_normais,
        node_color="#AED6F1", node_size=1800, ax=ax
    )

    # Nós em ciclo
    if vertices_do_ciclo:
        nx.draw_networkx_labels(
            G,
            pos,
            font_size=8,
            font_weight="bold",
            font_color="white",
            ax=ax
)

    # Nós impactados
    if conjunto_de_impacto:
        nx.draw_networkx_nodes(
            G, pos, nodelist=list(conjunto_de_impacto),
            node_color="#F39C12", node_size=1800, ax=ax
        )

    # Arestas normais
    nx.draw_networkx_edges(
        G, pos, edgelist=arestas_normais,
        edge_color="#888888", arrows=True,
        arrowsize=20, width=1.5,
        connectionstyle="arc3,rad=0.1", ax=ax
    )

    # Arestas de ciclo
    if arestas_do_ciclo:
        nx.draw_networkx_edges(
            G, pos, edgelist=list(arestas_do_ciclo),
            edge_color="#E74C3C", arrows=True,
            arrowsize=25, width=2.5,
            connectionstyle="arc3,rad=0.1", ax=ax
        )

    # Arestas de impacto
    if arestas_impactadas:
        nx.draw_networkx_edges(
            G, pos, edgelist=list(arestas_impactadas),
            edge_color="#F39C12", arrows=True,
            arrowsize=25, width=2.5,
            connectionstyle="arc3,rad=0.1", ax=ax
        )

    # Labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold", ax=ax)

    # ── Legenda ──────────────────────────────────────────
    legend_elements = [
        plt.Line2D([0], [0], marker="o", color="w",
                   markerfacecolor="#AED6F1", markersize=12, label="Módulo normal"),
    ]

    if vertices_do_ciclo:
        legend_elements.append(
            plt.Line2D([0], [0], marker="o", color="w",
                       markerfacecolor="#E74C3C", markersize=12, label="Ciclo")
        )

    if conjunto_de_impacto:
        legend_elements.append(
            plt.Line2D([0], [0], marker="o", color="w",
                       markerfacecolor="#F39C12", markersize=12, label="Impacto")
        )

    ax.legend(handles=legend_elements, loc="upper left", fontsize=9)
    ax.axis("off")

    plt.tight_layout()

    return fig