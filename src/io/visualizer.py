"""
Módulo: visualizer.py

Responsabilidade:
Gerar visualização INTERATIVA do grafo de dependências,
com suporte a:
- zoom
- hover
- drag
- responsividade
- dark mode
- destaque para ciclos (vermelho)
- destaque para cone de impacto (laranja)
- destaque para módulo em foco (azul claro maior)
"""

import os
import tempfile
from pyvis.network import Network

def desenhar_grafo_interativo(
    graph,
    ciclos: list = None,
    impacto: list = None,
    modulo_foco: str = None
) -> str:
    """
    Gera o código HTML de um grafo interativo usando pyvis.
    Retorna a string HTML para ser injetada no Streamlit.
    """
    ciclos = ciclos or []
    impacto_set = set(impacto or [])

    # Mapeia vértices e arestas que fazem parte de um ciclo
    vertices_ciclo = set()
    arestas_ciclo = set()
    for ciclo in ciclos:
        vertices_ciclo.update(ciclo)
        for i in range(len(ciclo) - 1):
            arestas_ciclo.add((ciclo[i], ciclo[i+1]))

    # Configuração base da rede
    net = Network(
        height="600px", 
        width="100%", 
        bgcolor="#0E1117", 
        font_color="white", 
        directed=True
    )

    # ──────────────────────────────────────────
    # NÓS (VÉRTICES)
    # ──────────────────────────────────────────
    todas_arestas = graph.obter_arestas()

    for v in graph.obter_vertices():
        # Lógica de cores e tamanhos (igual estava no app.py)
        if v in vertices_ciclo:
            color = "#E74C3C"  # Vermelho para ciclos
            size = 18
        elif v in impacto_set:
            color = "#F39C12"  # Laranja para impacto
            size = 18
        elif v == modulo_foco:
            color = "#58A6FF"  # Azul forte/maior para o módulo selecionado
            size = 25
        else:
            color = "#AED6F1"  # Azul claro padrão
            size = 18

        # Monta o Tooltip (Hover)
        vizinhos_saida = graph.obter_vizinhos(v)
        vizinhos_entrada = [o for o, d in todas_arestas if d == v]
        tooltip = (
            f"📦 {v}\n"
            f"→ Importa: {', '.join(vizinhos_saida) if vizinhos_saida else 'nenhum'}\n"
            f"← Importado por: {', '.join(vizinhos_entrada) if vizinhos_entrada else 'nenhum'}"
        )
        
        # O nome curto no nó visual (para não poluir a tela)
        label_curto = v.split("/")[-1]

        net.add_node(
            v, 
            label=label_curto, 
            title=tooltip, 
            color=color, 
            size=size
        )

    # ──────────────────────────────────────────
    # ARESTAS (DEPENDÊNCIAS)
    # ──────────────────────────────────────────
    for origem, destino in todas_arestas:
        if (origem, destino) in arestas_ciclo:
            cor_aresta = "#E74C3C"
            largura = 3
        elif destino in impacto_set:
            cor_aresta = "#F39C12"
            largura = 2
        else:
            cor_aresta = "#555555"
            largura = 1.5

        net.add_edge(
            origem, 
            destino, 
            color=cor_aresta, 
            width=largura
        )

    net.set_options("""
    {
      "nodes": { 
          "font": { "size": 13, "color": "white" }, 
          "borderWidth": 2 
      },
      "edges": { 
          "arrows": { "to": { "enabled": true, "scaleFactor": 0.8 } }, 
          "smooth": { "type": "curvedCW", "roundness": 0.1 } 
      },
      "physics": { 
          "enabled": true, 
          "solver": "forceAtlas2Based", 
          "stabilization": { "iterations": 150 } 
      },
      "interaction": { 
          "hover": true, 
          "tooltipDelay": 100 
      }
    }
    """)

    # ── GERA HTML E LIMPA MEMÓRIA/DISCO ────────────────────────────────────────────
    arquivo_temporario = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(arquivo_temporario.name)

    with open(arquivo_temporario.name, "r", encoding="utf-8") as f:
        html_content = f.read()

    # ── Apaga o arquivo físico para não estourar o disco ────────────────────────────────────────────
    try:
        os.unlink(arquivo_temporario.name)
    except Exception:
        pass

    return html_content
