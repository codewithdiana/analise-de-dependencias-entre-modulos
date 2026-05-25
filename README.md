# Analisador de Dependências

Uma ferramenta interativa desenvolvida em Python e Streamlit para mapear, visualizar e analisar dependências entre módulos de projetos Python.

Utilizando Teoria dos Grafos e Análise Estática de Código utilizando AST (Abstract Syntax Tree), o sistema processa projetos compactados em `.zip`, identificando relações de importação, ciclos de dependência, ordem topológica de execução e impacto arquitetural de alterações no código-fonte.

## Principais Funcionalidades

* Geração de grafo interativo de dependências a partir de código-fonte em Python (via AST).
* Identificação de dependências circulares utilizando Busca em Profundidade (DFS).
* Geração de ordem segura de compilação, carregamento ou execução de testes baseada em Ordenação Topológica (Algoritmo de Kahn).
* Análise de impacto de modificações utilizando Busca em Largura (BFS) reversa para identificar módulos afetados.
* Geração automatizada de relatórios e explicações arquiteturais com apoio de Inteligência Artificial (Groq / LLaMA 3).

---

## Demonstração

Entenda como o projeto funciona na prática através de uma análise visual:

[Assista ao vídeo de demonstração no YouTube](https://youtu.be/E-1emplTEzY?si=rdykZwUP_EY4WikG)

---

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Frontend:** Streamlit
* **Visualização de Grafos:** PyVis / NetworkX
* **Inteligência Artificial:** Groq API (LLaMA 3.3 70B)
* **Algoritmos Core:** DFS (Depth-First Search), BFS (Breadth-First Search) e Algoritmo de Kahn.

---

## Como Executar o Projeto

### Pré-requisitos

* Python 3.8 ou superior instalado.
* Uma chave de API gratuita do :contentReference[oaicite:0]{index=0} (opcional, apenas para os recursos de IA).

---

### Passo a Passo

**1. Clone ou baixe o repositório**

Faça o download do repositório em `.zip` e extraia os arquivos, ou clone o projeto:

```bash
git clone <url-do-repositorio>
cd analise-de-dependencias-entre-modulos
```

---

**2. Crie e ative um ambiente virtual**

```bash
python -m venv .venv
```

**Windows**
```bash
.venv\Scripts\activate
```

**Linux/Mac**
```bash
source .venv/bin/activate
```

---

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

---

**4. Configure a chave da IA (Opcional)**

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_aqui
```

---

**5. Execute a aplicação**

```bash
streamlit run ui/app.py
```
