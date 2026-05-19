# E2 — Design Técnico, Arquitetura e Backlog

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 20 de abril de 2026  
> **Peso:** 20% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | Análise de Dependências em Sistemas de Software |
| Repositório GitHub | https://github.com/codewithdiana/analise-de-dependencias-entre-modulos |
| Integrante 1 | Diana Kellen de Almeida Malaquias — 39161960 |
| Integrante 2 | Gabriela Yuri Kobayashi — 38408406 |
| Integrante 3 | Julia Aparecida Venâncio dos Santos — 38226189 |

---

## 1. Algoritmos Escolhidos

### 1.1 Algoritmo Principal

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Busca em Profundidade (DFS) com coloração de vértices |
| Categoria | Busca em grafos / detecção de ciclos |
| Complexidade de tempo | O(V + E) |
| Complexidade de espaço | O(V) — pilha de recursão + array de cores |
| Problema que resolve | Detecção de ciclos no grafo de dependências entre módulos Python |

**Por que este algoritmo foi escolhido?**

<!-- Justifique a escolha para o seu domínio específico --> A DFS com coloração de vértices (branco/cinza/preto) é a abordagem canônica para detecção de ciclos em grafos dirigidos. Um ciclo existe se e somente se a DFS encontra uma aresta de retorno — ou seja, uma aresta que aponta para um vértice ainda cinza (em processamento). Além de detectar a existência do ciclo, essa abordagem permite reconstruir o caminho completo do ciclo por meio da pilha de recursão, o que é essencial para que o desenvolvedor identifique exatamente quais módulos estão em acoplamento circular.

**Alternativa descartada e motivo:**

| Algoritmo alternativo | Motivo da exclusão |
|----------------------|-------------------|
| Algoritmo de Kosaraju (SCCs) | Identifica componentes fortemente conexos, mas não reporta o caminho do ciclo diretamente — menos informativo para o caso de uso de debugging |
| Detecção por matriz de alcançabilidade (Floyd-Warshall) | Complexidade O(V³), inviável para projetos com centenas de módulos |

**Limitações no contexto do problema:**

- Em projetos com muitos módulos, a recursão profunda pode causar estouro de pilha (*stack overflow*) em Python. Mitigação: implementação iterativa com pilha explícita ou ajuste via `sys.setrecursionlimit`.

---

**Referência bibliográfica:**

> CORMEN, T. H. et al. *Introduction to Algorithms*. 3. ed. Cambridge: MIT Press, 2009. Cap. 22 — Busca em profundidade e detecção de ciclos.

---

### 1.2 Algoritmo Adicional *(se houver)*

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Algoritmo de Kahn (Ordenação Topológica) |
| Categoria | Ordenação em grafos dirigidos acíclicos (DAGs) |
| Complexidade de tempo | O(V + E) |
| Complexidade de espaço | O(V + E) |

**Justificativa:**

<!-- Por que este segundo algoritmo complementa o projeto? -->  Após a DFS confirmar que o grafo é acíclico, o Kahn determina a sequência segura de compilação/execução dos módulos. Ele processa iterativamente os vértices com grau de entrada zero, sem recursão, eliminando o risco de *stack overflow*. Para grafos desconexos — cenário comum em projetos reais — o algoritmo é executado por componente, garantindo cobertura completa: se ao final restar algum vértice não processado, isso confirma a presença de um ciclo, servindo como verificação secundária.


**Referência bibliográfica:**

> KAHN, A. B. Topological sorting of large networks. *Communications of the ACM*, v. 5, n. 11, p. 558–562, nov. 1962.

---

### 1.3 Algoritmo Adicional — BFS (Cone de Impacto)

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Busca em Largura (BFS) |
| Categoria | Busca em grafos / alcançabilidade |
| Complexidade de tempo | O(V + E) |
| Complexidade de espaço | O(V) |


**Justificativa:**

Dado um módulo modificado, a BFS visita todos os vértices alcançáveis a partir dele — que correspondem exatamente aos módulos impactados pela mudança. Os resultados são produzidos em ordem de distância (camadas de impacto), permitindo priorizar os testes de regressão: módulos na primeira camada têm dependência direta e são testados primeiro; módulos em camadas mais distantes têm dependência transitiva.


**Referência bibliográfica:**

> CORMEN, T. H. et al. *Introduction to Algorithms*. 3. ed. Cambridge: MIT Press, 2009. Cap. 22 — Busca em largura.

---

## 2. Arquitetura em Camadas

![Diagrama de arquitetura](https://github.com/codewithdiana/analise-de-dependencias-entre-modulos/blob/main/img/arquitetura_e2.png)

> *Diagrama a ser inserido em `docs/arquitetura_e2.png` — deve ilustrar as quatro camadas abaixo e o fluxo de dados entre elas.*

### Descrição das camadas

| Camada | Responsabilidade | Artefatos principais |
|--------|-----------------|----------------------|
| Apresentação (UI/CLI) | Receber comandos do usuário via terminal, exibir resultados textuais (ciclos, ordenação, cone de impacto) e acionar a visualização gráfica | `main.py`, `cli.py` |
| Aplicação (Service) | Orquestrar o fluxo: carregar dados → construir grafo → executar algoritmo selecionado → retornar resultado formatado | `dependency_service.py` |
| Domínio (Core) | Representar o grafo como lista de adjacência e implementar os três algoritmos (DFS, Kahn, BFS) | `graph.py`, `dfs.py`, `kahn.py`, `bfs.py` |
| Infraestrutura (I/O) | Ler arquivos JSON/CSV de entrada, fazer parsing opcional de arquivos `.py`, e acionar NetworkX + Matplotlib para visualização | `file_reader.py`, `py_parser.py`, `visualizer.py` |

---

## 3. Estrutura de Diretórios

```
analise-de-dependencias-entre-modulos/
├── docs/
│   ├── README.md
│   ├── E1_Grupos1_Grafos.md
│   └── E2_Grupo1_Grafos.md
├── img/
│   ├── arquitetura_e2.png
│   └── diagrama_conceitual.png
├── src/
│   ├── core/
│   │   └── graph.py              # Estrutura do grafo (lista de adjacência)
│   ├── algorithms/
│   │   ├── dfs.py                # DFS com coloração — detecção de ciclos
│   │   ├── kahn.py               # Algoritmo de Kahn — ordenação topológica
│   │   └── bfs.py                # BFS — cone de impacto
│   ├── io/
│   │   ├── file_reader.py        # Leitura de JSON/CSV
│   │   └── visualizer.py         # Geração do grafo visual (NetworkX + Matplotlib)
│   ├── service/
│   │   └── dependency_service.py # Orquestração dos fluxos
│   └── main.py                   # Ponto de entrada / CLI
├── tests/
│   ├── test_graph.py
│   ├── test_dfs.py
│   ├── test_kahn.py
│   └── test_bfs.py
├── data/
│   └── exemplo_projeto.json
└── requirements.txt
```

> **Justificativa de desvios:** foi adicionada uma pasta service/ que não existe no template original — ela separa "quem decide o que fazer" (o serviço) de "quem executa" (os algoritmos). O arquivo py_parser.py foi colocado dentro de io/ junto com o file_reader.py, pois os dois lidam com leitura de dados e faz sentido ficarem juntos. Por fim, as imagens dos diagramas foram organizadas em uma pasta img/ separada, em vez de dentro de docs/, para distinguir arquivos visuais de documentos de texto.

---

## 4. Definição do Dataset

**Formato de entrada aceito:**

<!-- JSON / CSV / GraphML / lista de adjacência — descreva a estrutura -->
JSON (padrão) ou CSV (alternativo). O arquivo descreve os módulos do projeto e suas relações de importação — cada módulo é um vértice e cada importação é uma aresta dirigida.


**Exemplo de estrutura do arquivo de entrada:**

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
    { "origem": "main.py",           "destino": "auth/login.py" },
    { "origem": "main.py",           "destino": "database/connection.py" },
    { "origem": "auth/login.py",     "destino": "auth/token.py" },
    { "origem": "auth/login.py",     "destino": "database/connection.py" },
    { "origem": "database/query.py", "destino": "database/connection.py" }
  ]
}
```


**Estratégia de geração aleatória:**

| Parâmetro | Descrição |
|-----------|-----------|
| Número de vértices | configurável via argumento |
| Densidade | configurável (0.0 a 1.0) |
| Faixa de pesos | mín/máx configuráveis |

---

## 5. Backlog do Projeto

### 5.1 In-Scope — O que será implementado

| # | Funcionalidade | Prioridade | Critério de aceite |
|---|---------------|------------|-------------------|
| 1 | Leitura do grafo a partir de arquivo JSON ou CSV com lista de dependências | Alta | Dado um arquivo JSON ou CSV válido contendo uma lista de dependências, quando o sistema realizar a leitura, então o grafo deve ser carregado com todos os vértices e arestas corretamente representados em lista de adjacência |
| 2 |Parsing automático de imports de arquivos `.py` reais (modo opcional) | Baixa | Dado um diretório com arquivos `.py`, quando o modo de parsing for ativado, então o sistema deve identificar os imports e gerar o grafo de dependências entre os módulos internos do projeto |
| 3 |Geração de grafos aleatórios parametrizáveis para testes (número de vértices, densidade)| Baixa | Dado um número de vértices e uma densidade informados pelo usuário, quando o sistema gerar o grafo, então deve ser criado um grafo aleatório que respeite os parâmetros definidos |
| 4 |Detecção de ciclos com reporte do caminho completo (DFS com coloração) | Alta | Dado um grafo com ciclo conhecido (ex.: A→B→C→A), quando o algoritmo for executado, então o sistema deve reportar a existência do ciclo e apresentar o caminho completo (ex.: `A → B → C → A`) |
| 5 | Ordenação topológica com saída em lista ordenada (Kahn) | Alta | Dado um DAG com dois componentes desconexos, quando a ordenação topológica for executada, então todos os vértices de ambos os componentes devem aparecer na lista de saída respeitando as dependências de cada componente |
| 6 | Cálculo do cone de impacto dado um módulo de entrada (BFS) | Alta | Dado o módulo `database/connection.py` como entrada, quando a BFS for executada, então o sistema deve retornar todos os módulos que dependem direta ou indiretamente dele, sem repetições, ordenados por distância |
| 7 |Visualização do grafo com NetworkX + Matplotlib (destaque para ciclos e cone de impacto) | Média | Dado um grafo com ciclo e um módulo de impacto selecionado, quando a visualização for gerada, então arestas de ciclo devem aparecer em vermelho e arestas do cone de impacto em laranja, com legenda identificando cada destaque |
| 8 |Interface de linha de comando (CLI) com menu interativo | Média / Baixa | Dado que o sistema foi iniciado via terminal, quando o usuário interagir com o menu, então ele deve conseguir acessar todas as funcionalidades disponíveis de forma clara e funcional.

### 5.2 Out-of-Scope — O que NÃO será feito

| Funcionalidade excluída | Motivo |
|------------------------|--------|
| Suporte a linguagens além de Python | Reduziria o foco do projeto sem ganho algorítmico relevante para a disciplina |
| Análise de dependências de pacotes externos (pip/PyPI) | Fora do escopo declarado no E1 — o foco é a estrutura interna que a equipe controla |
| Interface gráfica web ou desktop (GUI) | Matplotlib estático cobre os objetivos de visualização; uma GUI adicionaria complexidade sem ganho algorítmico |
| Integração com sistemas de CI/CD | Extensão de engenharia de software além do escopo de uma disciplina de teoria dos grafos |


---

## Checklist de Entrega

- [x] Big-O de tempo e espaço declarados para cada algoritmo
- [x] Ao menos 1 alternativa descartada com justificativa
- [x] Diagrama de arquitetura com 4 camadas identificadas
- [x] Referência bibliográfica para cada algoritmo (ABNT ou IEEE)
- [x] Backlog com ≥ 5 itens In-Scope e ≥ 3 Out-of-Scope
- [x] Ao menos 3 critérios de aceite no formato "dado / quando / então"
- [x] Exemplo de estrutura de arquivo de entrada presente

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
