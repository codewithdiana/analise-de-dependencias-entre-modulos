# E2 — Design Técnico, Arquitetura e Backlog

> **Disciplina:** Teoria dos Grafos
> **Prazo:** 20 de abril de 2026
> **Peso:** 20% da nota final

---

# Identificação do Grupo

| Campo              | Preenchimento                                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Nome do projeto    | Análise de Dependências em Sistemas de Software                                                                                                  |
| Repositório GitHub | [https://github.com/codewithdiana/analise-de-dependencias-entre-modulos](https://github.com/codewithdiana/analise-de-dependencias-entre-modulos) |
| Integrante 1       | Diana Kellen de Almeida Malaquias — 39161960                                                                                                     |
| Integrante 2       | Gabriela Yuri Kobayashi — 38408406                                                                                                               |
| Integrante 3       | Julia Aparecida Venâncio dos Santos — 38226189                                                                                                   |

---

# 1. Algoritmos Escolhidos

## 1.1 Algoritmo Principal

| Campo                  | Resposta                                                         |
| ---------------------- | ---------------------------------------------------------------- |
| Nome do algoritmo      | Busca em Profundidade (DFS) com coloração de vértices            |
| Categoria              | Busca em grafos / detecção de ciclos                             |
| Complexidade de tempo  | O(V + E)                                                         |
| Complexidade de espaço | O(V) — pilha de recursão + array de cores                        |
| Problema que resolve   | Detecção de ciclos no grafo de dependências entre módulos Python |

## Por que este algoritmo foi escolhido?

A DFS com coloração de vértices (branco/cinza/preto) é a abordagem clássica para detecção de ciclos em grafos dirigidos. Um ciclo existe quando a DFS encontra uma aresta de retorno para um vértice ainda cinza (em processamento). Além de detectar a existência do ciclo, essa abordagem permite reconstruir o caminho completo do ciclo utilizando a pilha de recursão, permitindo identificar exatamente quais módulos estão em dependência circular.

## Alternativa descartada e motivo

| Algoritmo alternativo        | Motivo da exclusão                                                                        |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| Algoritmo de Kosaraju (SCCs) | Identifica componentes fortemente conexos, mas não reporta diretamente o caminho do ciclo |
| Floyd-Warshall               | Complexidade O(V³), inviável para projetos maiores                                        |

## Limitações no contexto do problema

* Projetos com muitos módulos podem causar estouro de pilha devido à profundidade recursiva da DFS.
* Mitigação possível: implementação iterativa usando pilha explícita.

## Referência bibliográfica

> CORMEN, T. H. et al. *Introduction to Algorithms*. 3. ed. Cambridge: MIT Press, 2009.

---

## 1.2 Algoritmo Adicional — Kahn

| Campo                  | Resposta                     |
| ---------------------- | ---------------------------- |
| Nome do algoritmo      | Algoritmo de Kahn            |
| Categoria              | Ordenação topológica em DAGs |
| Complexidade de tempo  | O(V + E)                     |
| Complexidade de espaço | O(V + E)                     |

## Justificativa

Após a verificação de ausência de ciclos pela DFS, o algoritmo de Kahn é utilizado para determinar uma sequência válida de compilação ou execução dos módulos. O algoritmo processa iterativamente os vértices com grau de entrada zero, evitando recursão e funcionando corretamente mesmo em grafos desconexos.

## Referência bibliográfica

> KAHN, A. B. Topological sorting of large networks. *Communications of the ACM*, v. 5, n. 11, p. 558–562, 1962.

---

## 1.3 Algoritmo Adicional — BFS

| Campo                  | Resposta                          |
| ---------------------- | --------------------------------- |
| Nome do algoritmo      | Busca em Largura (BFS)            |
| Categoria              | Busca em grafos / alcançabilidade |
| Complexidade de tempo  | O(V + E)                          |
| Complexidade de espaço | O(V)                              |

## Justificativa

A BFS é utilizada para cálculo do cone de impacto. A partir de um módulo alterado, o algoritmo percorre todos os módulos alcançáveis, representando os arquivos potencialmente afetados pela mudança. Os resultados são retornados em camadas de distância, permitindo priorização de testes e análise de dependências transitivas.

## Referência bibliográfica

> CORMEN, T. H. et al. *Introduction to Algorithms*. 3. ed. Cambridge: MIT Press, 2009.

---

# 2. Arquitetura em Camadas

![Diagrama de arquitetura](https://github.com/codewithdiana/analise-de-dependencias-entre-modulos/blob/main/img/arquitetura_e2.png)

> O sistema foi organizado em quatro camadas principais para separar responsabilidades, facilitar manutenção e permitir evolução independente dos componentes.

## Descrição das camadas

| Camada                | Responsabilidade                                                                                                               | Artefatos principais                              |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| Apresentação (UI/CLI) | Receber comandos do usuário via terminal/interface, exibir resultados textuais e acionar a visualização do grafo               | `main.py`, `app.py`                               |
| Aplicação (Service)   | Orquestrar o fluxo: carregar arquivos → construir grafo → executar algoritmos → retornar resultados                            | `dependency_service.py`                           |
| Domínio (Core)        | Representar o grafo dirigido utilizando lista de adjacência e implementar DFS, Kahn e BFS                                      | `grafo.py`, `dfs.py`, `kahn.py`, `bfs.py`         |
| Infraestrutura (I/O)  | Leitura de arquivos `.py`, JSON, CSV e projetos `.zip`, parsing automático de imports e visualização com NetworkX + Matplotlib | `file_reader.py`, `py_parser.py`, `visualizer.py` |

## Fluxo arquitetural

```text
Entrada de arquivos (.py/.json/.csv/.zip)
        ↓
Parsing de imports e leitura de dependências
        ↓
Construção do grafo dirigido (lista de adjacência)
        ↓
Execução dos algoritmos:
    • DFS → detecção de ciclos
    • Kahn → ordenação topológica
    • BFS → cone de impacto
        ↓
Geração dos resultados
        ↓
Visualização do grafo e exibição na UI/CLI
```

---

# 3. Estrutura de Diretórios

```textanalise-de-dependencias-entre-modulos/
├── docs/
│   ├── README.md
│   ├── E1_Grupos1_Grafos.md
│   └── E2_Grupo1_Grafos.md
├── img/
│   ├── arquitetura_e2.png
│   └── diagrama_conceitual.png
├── src/
│   ├── algorithms/
│   │   ├── dfs.py                # DFS com coloração — detecção de ciclos
│   │   ├── kahn.py               # Algoritmo de Kahn — ordenação topológica
│   │   └── bfs.py                # BFS — cone de impacto
│   ├── core/
│   │   └── grafo.py              # Estrutura do grafo (lista de adjacência)
│   ├── io/
│   │   ├── file_reader.py        # Leitura de .py, JSON, CSV e ZIP
│   │   ├── py_parser.py          # Parsing automático de imports Python
│   │   └── visualizer.py         # Visualização com NetworkX + Matplotlib
│   ├── service/
│   │   └── dependency_service.py # Orquestração dos fluxos
│   ├── ui/
│   │   └── app.py                # Interface/UI
│   └── main.py                   # Ponto de entrada principal
├── tests/
│   ├── test_grafo.py
│   ├── test_dfs.py
│   ├── test_kahn.py
│   └── test_bfs.py
├── data/
│   ├── exemplo_projeto.json
│   └── exemplo_com_ciclo.json
└── requirements.txt
```

## Justificativa da organização

A camada `service/` foi adicionada para separar a orquestração da aplicação da implementação dos algoritmos. O arquivo `py_parser.py` foi agrupado em `io/` por lidar diretamente com leitura e interpretação de arquivos Python. As imagens dos diagramas foram organizadas em `img/` para separar artefatos visuais da documentação textual.

---

# 4. Definição do Dataset

## Formatos de entrada aceitos

O sistema aceita:

* Arquivos JSON
* Arquivos CSV
* Arquivos Python (`.py`)
* Projetos compactados (`.zip`)

Os arquivos descrevem módulos e relações de importação, modelados como um grafo dirigido em que:

* cada módulo representa um vértice;
* cada importação representa uma aresta dirigida.

## Exemplo de entrada JSON

```json
{
  "modulos": [
    "database/connection.py",
    "database/query.py",
    "auth/login.py",
    "auth/token.py",
    "main.py"
  ],
  "dependencias": [
    { "origem": "main.py", "destino": "auth/login.py" },
    { "origem": "main.py", "destino": "database/connection.py" },
    { "origem": "auth/login.py", "destino": "auth/token.py" },
    { "origem": "auth/login.py", "destino": "database/connection.py" },
    { "origem": "database/query.py", "destino": "database/connection.py" }
  ]
}
```

## Estratégia de geração aleatória

| Parâmetro             | Descrição                |
| --------------------- | ------------------------ |
| Número de vértices    | configurável             |
| Densidade             | configurável             |
| Quantidade de arestas | proporcional à densidade |

---

# 5. Backlog do Projeto

## 5.1 In-Scope

| # | Funcionalidade                         | Prioridade | Critério de aceite                                                |
| - | -------------------------------------- | ---------- | ----------------------------------------------------------------- |
| 1 | Leitura de JSON e CSV                  | Alta       | O sistema deve carregar corretamente vértices e arestas           |
| 2 | Parsing automático de imports Python   | Média      | O sistema deve identificar imports internos e gerar o grafo       |
| 3 | Importação de projetos `.zip`          | Média      | O sistema deve extrair o projeto e analisar dependências internas |
| 4 | DFS com detecção de ciclos             | Alta       | O sistema deve identificar e reportar ciclos completos            |
| 5 | Ordenação topológica com Kahn          | Alta       | O sistema deve retornar sequência válida de execução              |
| 6 | BFS para cone de impacto               | Alta       | O sistema deve retornar módulos impactados sem repetição          |
| 7 | Visualização com NetworkX + Matplotlib | Média      | O sistema deve gerar visualização do grafo                        |
| 8 | Interface CLI/UI                       | Média      | O usuário deve acessar funcionalidades via interface              |

---

## 5.2 Out-of-Scope

| Funcionalidade excluída     | Motivo                                      |
| --------------------------- | ------------------------------------------- |
| Suporte a outras linguagens | Manter foco em Python                       |
| Integração com PyPI         | Fora do escopo algorítmico                  |
| Interface gráfica web       | Complexidade elevada para a disciplina      |
| Integração com CI/CD        | Não agrega ao objetivo de teoria dos grafos |

---

# Checklist de Entrega

* [x] Complexidades declaradas
* [x] Alternativas descartadas justificadas
* [x] Arquitetura em camadas definida
* [x] Referências bibliográficas presentes
* [x] Backlog definido
* [x] Critérios de aceite presentes
* [x] Estrutura de entrada documentada

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
