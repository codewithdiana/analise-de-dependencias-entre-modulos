# Analisador de Dependências

Uma ferramenta interativa construída em Python e Streamlit para mapear, visualizar e analisar as dependências internas de projetos. 

Utilizando Teoria dos Grafos e Análise Estática de Código (AST), o sistema processa arquivos `.zip` de projetos Python, gerando insights matemáticos e visuais sobre a sua arquitetura.

## Principais Funcionalidades

* Geração de grafo interativo de dependências a partir de código-fonte em Python (via AST).
* Identificação de dependências circulares utilizando Busca em Profundidade (DFS).
* Cálculo de ordem de compilação/teste segura baseada em Ordenação Topológica (Algoritmo de Kahn).
* Avaliação de raio de impacto de modificações através de Busca em Largura (BFS) reversa.
* Geração automatizada de relatórios e explicações de arquitetura via LLM (Integração Groq/LLaMA 3).


## Demonstração

Entenda como o projeto funciona na prática através de uma análise visual:
[🎥 Assista ao vídeo de demonstração no YouTube]([https://www.youtube.com/watch?v=ID_DO_SEU_VIDEO](https://youtu.be/E-1emplTEzY?si=rdykZwUP_EY4WikG))

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Frontend:** Streamlit
* **Visualização de Grafos:** PyVis / NetworkX
* **Inteligência Artificial:** Groq API (LLaMA-3.3-70b)
* **Algoritmos Core:** DFS (Depth-First Search), BFS (Breadth-First Search) e Algoritmo de Kahn.

## Como Executar o Projeto

### Pré-requisitos

* Python 3.8 ou superior instalado.
* Uma chave de API gratuita do [Groq](https://console.groq.com/) (opcional, apenas para os recursos de IA).

### Passo a Passo

**1. Clone ou baixe o repositório:**
Faça o download do repositório em `.zip` e extraia, ou navegue até a pasta pelo terminal:
```bash
cd local/analise-de-dependencias-entre-modulos
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv .venv

Windows
.venv\Scripts\activate

Linux/Mac
source .venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

Configure a chave da IA (Opcional): Em um arquivo .env, insira sua chave da API do Groq na variável GROQ_API_KEY.

**5. Execute a aplicação:**
```bash
streamlit run ui/app.py 
```
