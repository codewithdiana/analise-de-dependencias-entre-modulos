# E1 — Proposta e Definição do Projeto

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 16 de março de 2026  
> **Peso:** 10% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | Análise de Dependências em Sistemas de Software |
| Integrante 1 | Diana Kellen de Almeida Malaquias — 39161960 |
| Integrante 2 | Gabriela Yuri Kobayashi — 38408406 |
| Integrante 3 | Julia Aparecida Venâncio dos Santos — 38226189 |
| Domínio de aplicação | Engenharia de Software — análise de dependências entre módulos Python|

---

## 1. Contexto e Motivação

> Descreva o problema do mundo real que será abordado. Por que ele é relevante?  
> *Orientação: 2 a 3 parágrafos. Seja específico — evite generalizações.*

Em projetos grandes de software, as importações entre módulos criam uma rede complexa de dependências. Alterar um módulo pode gerar efeitos em cascata difíceis de prever. O sistema proposto mapeia esse grafo de dependências, identifica ciclos (acoplamento circular), organiza os módulos em ordem segura de compilação por meio de ordenação topológica e mostra o cone de impacto de qualquer mudança, permitindo ao desenvolvedor saber exatamente quais partes precisam ser recompiladas ou testadas novamente, reduzindo riscos e tempo de debugging.

À medida que as equipes crescem e os projetos ganham escala, a ausência de visibilidade sobre essas dependências torna-se um risco operacional concreto: regressões inesperadas, builds quebrados e ciclos de debugging desnecessários. Ferramentas como `pydeps` existem no mercado, mas não combinam visualização de impacto, detecção de ciclos e ordenação topológica em um único sistema interativo. O diferencial deste projeto está em colocar o desenvolvedor no centro: antes de qualquer commit, ele sabe exatamente o que pode quebrar.

O escopo está deliberadamente delimitado a **módulos internos do projeto** (arquivos `.py` locais), excluindo dependências externas gerenciadas via `pip`. Essa delimitação torna o problema tratável e o grafo resultante interpretável — o objetivo é analisar a estrutura que a equipe controla, não o ecossistema externo.

---

## 2. Objetivo Geral

> O que o sistema deve ser capaz de fazer ao final?  
> *Orientação: 1 frase clara e objetiva. Ex.: "O sistema deve calcular a rota de menor custo entre dois pontos em um mapa urbano."*

Desenvolver um sistema em Python capaz de receber como entrada a estrutura de módulos de um projeto, construir o grafo de dependências, executar análises algorítmicas sobre ele e apresentar os resultados de forma visual e interpretável. 

---

## 3. Objetivos Específicos

> Desmembre o objetivo geral em metas mensuráveis.  
> *Orientação: liste entre 3 e 5 itens. Cada item deve ser verificável — use verbos como "implementar", "calcular", "exibir", "carregar".*

- [x] **Construir o grafo de dependências:** o sistema deve ler a estrutura de um projeto Python — via arquivo de entrada estruturado (JSON ou CSV) como simplificação declarada do escopo — e construir um grafo dirigido representado internamente como lista de adjacência.  (uma forma eficiente de guardar quais módulos importam quais outros). 
- [x] **Detectar ciclos de dependência** utilizando DFS com coloração de vértices (branco/cinza/preto), reportando cada ciclo encontrado com o caminho completo.
- [x] **Gerar a ordenação topológica** dos módulos (quando o grafo for acíclico) utilizando o algoritmo de Kahn, com tratamento explícito de grafos desconexos — cada componente será processado independentemente, garantindo cobertura completa.
- [x] **Calcular o cone de impacto** de um módulo: dado um vértice de entrada, retornar todos os módulos alcançáveis que precisariam ser revalidados após uma mudança.
- [x] **Exibir o grafo resultante** de forma visual (via `networkx` + `matplotlib` ou similar), com destaque para ciclos detectados e para o caminho de impacto selecionado.

---

## 4. Público-Alvo / Caso de Uso Principal

> Para quem ou em qual cenário o sistema seria utilizado?  
> *Orientação: descreva um cenário concreto de uso. Ex.: "Um entregador de aplicativo que precisa otimizar a sequência de entregas em um bairro."*

O sistema é voltado a desenvolvedores e equipes de engenharia de software que trabalham com projetos Python modulares. O caso de uso principal é o seguinte:

Um desenvolvedor precisa alterar o módulo `database/connection.py`. Antes de fazer o commit, ele executa o sistema, que exibe quais outros módulos dependem direta ou indiretamente de `connection.py`, detecta se há ciclos no grafo e sugere a ordem de execução dos testes de regressão.

O sistema pode ser utilizado tanto com entradas estruturadas (JSON/CSV) quanto — como extensão futura — lendo imports diretamente do código-fonte, o que o torna adequado para uso acadêmico e didático.

---

## 5. Justificativa Técnica — Por que Grafos?

> Por que a modelagem em grafo é a abordagem mais adequada para este problema?  
> *Orientação: explique quais elementos do problema mapeiam naturalmente para vértices e arestas. Mencione se há pesos, direção, ou restrições que reforçam a escolha.*

A modelagem em grafo é a abordagem natural para este problema porque as relações de dependência são inerentemente binárias e direcionadas: "módulo A importa módulo B" é uma aresta dirigida A → B.

A detecção de ciclos é um problema clássico de grafos, resolvido eficientemente por DFS em O(V + E). Não existe abordagem equivalente sem a estrutura de grafo. A ordenação topológica — que define a sequência correta de build — só é definida para grafos dirigidos acíclicos (DAGs), e o algoritmo de Kahn opera diretamente sobre a estrutura do dígrafo em O(V + E). O cone de impacto é equivalente ao conjunto de vértices alcançáveis a partir de um nó, resolvido por BFS/DFS em O(V + E).

Alternativas como análise textual de imports sem estrutura de grafo não capturam a transitividade das dependências (A → B → C implica que A impacta C) e não permitem detectar ciclos de forma sistemática. Por fim, projetos reais possuem módulos utilitários sem dependentes, formando **componentes desconexos** — o sistema tratará cada componente separadamente na ordenação topológica, garantindo cobertura completa independentemente da conectividade do grafo.


---

## 6. Tipo de Grafo

> Especifique as características do grafo que o problema requer.

| Característica | Escolha | Justificativa breve |
|----------------|---------|---------------------|
| Dirigido ou não-dirigido | Dirigido (dígrafo) | A relação de importação tem sentido único: A importa B não implica B importa A. |
| Ponderado ou não-ponderado | Não-ponderado | Todas as arestas têm o mesmo peso semântico (existe dependência ou não existe). Não há métrica de intensidade relevante neste domínio. |
| Conectado / bipartido / geral | Geral (possivelmente desconexo) | Projetos reais possuem módulos utilitários sem dependentes, formando componentes isolados. O sistema trata cada componente separadamente na ordenação topológica. |
| Representação interna pretendida | Lista de adjacência | Eficiente em espaço O(V + E) para grafos esparsos, típicos em projetos de software, e permite que DFS, BFS e Kahn operem em tempo O(V + E) sem overhead de percorrer posições vazias como ocorreria em matriz de adjacência. |

---

## 7. Diagrama Conceitual

> Insira aqui ao menos uma figura que ilustre o domínio do problema.  
> *Pode ser uma imagem exportada do Draw.io, Excalidraw, foto de esboço à mão etc.*  

![Diagrama de dependências entre módulos Python](https://github.com/codewithdiana/analise-de-dependencias-entre-modulos/blob/main/img/diagrama_conceitual.png)

**Legenda:** 
- **Nós (vértices):** cada nó representa um módulo Python do projeto (ex.: `database/connection.py`, `auth/login.py`).  
- **Arestas dirigidas (→):** uma aresta de A para B indica que o módulo A importa o módulo B, ou seja, A depende de B.  
- **Arestas destacadas em vermelho:** indicam a presença de um ciclo de dependência detectado pelo algoritmo DFS.  
- **Arestas destacadas em laranja:** indicam o cone de impacto a partir de um módulo selecionado — todos os módulos alcançáveis que precisariam ser revalidados após uma mudança.  
- **Nós isolados:** módulos sem dependentes diretos (componentes desconexos), processados separadamente na ordenação topológica.

---

## Checklist de Entrega

Antes de submeter, confirme:

- [x] Texto entre 300 e 600 palavras (seções 1 a 5)
- [x] Todos os campos da tabela de identificação preenchidos
- [x] Tipo de grafo especificado com justificativa
- [x] Diagrama presente e referenciado no texto
- [x] Arquivo nomeado como `E1_NomeGrupo_Grafos.docx` (versão Word) ou PR aberto (versão GitHub)

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
