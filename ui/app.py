import streamlit as st
import json

from src.core.grafo import Grafo
from src.service.dependency_service import DependencyService

st.set_page_config(
    page_title="Analisador de Dependências",
    layout="wide"
)

# =========================
# 🎨 Estilo da Interface
# =========================
st.markdown("""
<style>

/* Fundo principal */
.stApp {
    background-color: #0E1117;
}

/* Espaçamento geral */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #222;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #1E1E1E;
    border-radius: 10px;
    padding: 10px 18px;
    color: white;
}

/* Inputs */
.stTextInput > div > div > input {
    border-radius: 10px;
}

/* Botões */
.stButton button {
    border-radius: 10px;
    width: 100%;
    font-weight: bold;
}

/* Imagens */
img {
    border-radius: 12px;
}

/* Esconde menu do Streamlit */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🏷️ Sidebar
# =========================
st.sidebar.markdown("# 🔍 Analyzer")

st.sidebar.markdown("""
Sistema de análise de dependências entre módulos Python.

Detecta:
- ciclos
- impacto
- ordenação topológica
""")

# =========================
# 🏷️ Título
# =========================
st.title("Análise de Dependências entre Módulos")

# =========================
# 📂 Upload JSON
# =========================
uploaded_file = st.file_uploader(
    "Envie um arquivo JSON",
    type=["json"]
)

graph = None
service = None

# =========================
# 📂 Carregamento
# =========================
if uploaded_file:

    data = json.load(uploaded_file)

    graph = Grafo()

    for origem, destinos in data.items():

        for destino in destinos:

            graph.adicionar_aresta(origem, destino)

    service = DependencyService(graph)

    st.success("Projeto carregado!")

# =========================
# 🧩 Abas
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Grafo",
    "Ciclos",
    "Ordenação",
    "Impacto",
    "Sobre"
])

# =========================
# 📊 GRAFO
# =========================
with tab1:

    st.header("Visualização do Grafo")

    if graph:

        from src.io.visualizer import desenhar_grafo

        fig = desenhar_grafo(graph)

        st.pyplot(fig)

    else:
        st.warning("Carregue um projeto primeiro.")

# =========================
# 🔄 CICLOS
# =========================
with tab2:

    st.header("Detecção de Ciclos")

    if service:

        if st.button("Detectar ciclos"):

            resultado = service.detectar_ciclos()

            if resultado.get("tem_ciclos"):

                st.error("Ciclos encontrados:")

                for ciclo in resultado.get("ciclos", []):

                    st.write(" → ".join(ciclo))

            else:
                st.success("Nenhum ciclo encontrado!")

    else:
        st.warning("Carregue um projeto primeiro.")

# =========================
# 📈 ORDENAÇÃO
# =========================
with tab3:

    st.header("Ordenação Topológica")

    if service:

        if st.button("Gerar ordenação"):

            resultado = service.ordenacao_topologica()

            if resultado.get("successo"):

                st.success("Ordem válida:")

                st.write(" → ".join(resultado.get("ordem", [])))

            else:
                st.error("Não foi possível ordenar.")

    else:
        st.warning("Carregue um projeto primeiro.")

# =========================
# 🎯 IMPACTO
# =========================
with tab4:

    st.header("Análise de Impacto")

    if service:

        modulo = st.text_input("Digite o módulo:")

        if st.button("Calcular impacto"):

            if modulo:

                # Verifica se módulo existe
                if modulo not in graph.obter_vertices():

                    st.error("Módulo não existente.")

                else:

                    resultado = service.calcular_cone_impacto(modulo)

                    impactados = resultado.get("impactados", [])

                    if impactados:

                        st.warning("Módulos impactados:")

                        st.write(" → ".join(impactados))

                    else:
                        st.success("Nenhum impacto encontrado.")

            else:
                st.info("Digite um módulo.")

    else:
        st.warning("Carregue um projeto primeiro.")

# =========================
# ℹ️ SOBRE
# =========================
# =========================
# ℹ️ SOBRE
# =========================
with tab5:

    st.header("Sobre o Projeto")

    st.markdown("""
### Objetivo

Este sistema analisa dependências entre módulos Python.

Ele permite:
- detectar ciclos
- calcular impacto
- gerar ordenação topológica
- visualizar dependências

---

### Funcionamento

Os módulos são representados como um grafo dirigido.

- cada nó representa um módulo
- cada aresta representa uma dependência

Exemplo:
A → B

Significa que:
A depende de B.

---

### Algoritmos Utilizados

DFS  
Detecta ciclos de dependência.

Algoritmo de Kahn  
Gera ordenação topológica.

BFS  
Calcula cone de impacto.

---

### Tecnologias

- Python
- Streamlit
- NetworkX
- Matplotlib

---

### Aplicações

- análise arquitetural
- debugging
- prevenção de regressões
- análise de impacto
""")