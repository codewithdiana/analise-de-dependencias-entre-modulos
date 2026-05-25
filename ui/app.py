import streamlit as st
import json
import os
import sys
import zipfile
import tempfile

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from src.core.grafo import Grafo
from src.service.dependency_service import DependencyService
from src.io.visualizer import desenhar_grafo_interativo
from dotenv import load_dotenv
from pathlib import Path
import streamlit.components.v1 as components

GRAPH_ICON = "https://img.icons8.com/fluency-systems-filled/24/58A6FF/combo-chart.png"
CYCLE_ICON = "https://img.icons8.com/fluency-systems-filled/24/58A6FF/refresh.png"
ORDER_ICON = "https://img.icons8.com/fluency-systems-filled/24/58A6FF/sorting-arrows-horizontal.png"
IMPACT_ICON = "https://img.icons8.com/fluency-systems-filled/24/58A6FF/high-importance.png"

def section_title(icon_url, title):
    return (
        '<div style="display:flex; align-items:center; gap:10px; margin-bottom:1rem;">'
        f'<img src="{icon_url}" width="22">'
        f'<h3 style="margin:0; color:white;">{title}</h3>'
        '</div>'
    )

load_dotenv()
# Puxa a chave do groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("API Key do Groq não configurada no arquivo .env!")

def carregar_css():
    diretorio_atual = os.path.dirname(__file__)

    caminho_css = os.path.join(diretorio_atual, "assets", "estilo.css")
    
    try:
        with open(caminho_css, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo CSS não encontrado no caminho: {caminho_css}")

carregar_css()

# ── Estado ────────────────────────────────────────────────
if 'graph'              not in st.session_state: st.session_state.graph              = None
if 'service'            not in st.session_state: st.session_state.service            = None
if 'chat_history'       not in st.session_state: st.session_state.chat_history       = []
if 'modulo_selecionado' not in st.session_state: st.session_state.modulo_selecionado = None
if 'chat_open'          not in st.session_state: st.session_state.chat_open          = False
if 'chat_input_val'     not in st.session_state: st.session_state.chat_input_val     = ""


# ── Groq ──────────────────────────────────────────────────
def chamar_groq(messages: list, max_tokens: int = 3000) -> str:
    api_key = GROQ_API_KEY or os.environ.get("GROQ_API_KEY", "")
    if not api_key or api_key == "sua_chave_aqui":
        return "⚠️ API Key do Groq não configurada. Edite a variável GROQ_API_KEY no início de app.py."
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao chamar Groq: {e}"


def explicar_com_ia(prompt: str) -> str:
    return chamar_groq([{"role": "user", "content": prompt}])


def montar_contexto_grafo() -> str:
    if not st.session_state.graph:
        return ""
    vertices = st.session_state.graph.obter_vertices()
    arestas  = st.session_state.graph.obter_arestas()
    linhas = ["Módulos (vértices):"] + [f"  - {v}" for v in vertices]
    linhas += ["\nDependências (origem importa destino):"]
    linhas += [f"  - {o} → {d}" for o, d in arestas]
    return "\n".join(linhas)


def gerar_nomes_exibicao(vertices: list) -> dict:
    """
    Gera nomes curtos para exibição, com desambiguação quando há duplicatas.
    Ex: "sistema-main/src/main.py" → "main.py"
    Se dois arquivos têm o mesmo nome: "src/main.py" e "tests/main.py"
    """
    # Conta quantos vértices têm o mesmo nome de arquivo
    from collections import Counter
    nomes_base = [v.replace("\\", "/").split("/")[-1] for v in vertices]
    contagem = Counter(nomes_base)

    resultado = {}
    for v in vertices:
        partes = v.replace("\\", "/").split("/")
        nome_base = partes[-1]
        if contagem[nome_base] == 1:
            # Único — mostra só o nome do arquivo
            resultado[v] = nome_base
        else:
            # Duplicado — mostra pasta/arquivo para diferenciar
            if len(partes) >= 2:
                resultado[v] = partes[-2] + "/" + nome_base
            else:
                resultado[v] = v
    return resultado


def renderizar_resposta_ia(resposta: str):
    st.markdown(
        f'<div class="ia-box"><div class="ia-box-title">🤖 AGENTE IA</div>'
        f'{resposta.replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True
    )


def processar_zip_com_py(uploaded_file):
    """
    Extrai o ZIP e lista os arquivos .py encontrados.
    Retorna (temp_dir, arquivos_py, todos_modulos) ou (None, None, None).
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip:
            tmp_zip.write(uploaded_file.getvalue())
            tmp_zip_path = tmp_zip.name

        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(tmp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        os.unlink(tmp_zip_path)

        arquivos_py = []
        for root, dirs, files in os.walk(temp_dir):
            dirs[:] = [d for d in dirs if d not in ['.venv', 'venv', '__pycache__', '.git', 'node_modules']]
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    rel_path  = os.path.relpath(full_path, temp_dir).replace(os.sep, "/")
                    arquivos_py.append((full_path, rel_path))

        if not arquivos_py:
            return (None, None, None)

        todos_modulos = [rel for _, rel in arquivos_py]
        return (temp_dir, arquivos_py, todos_modulos)
    except Exception as e:
        st.error(f"Erro ao processar ZIP: {e}")
        return (None, None, None)


def detectar_raiz_projeto(temp_dir: str, arquivos_py: list) -> str:
    """
    Detecta a pasta raiz real do projeto dentro do ZIP.
    ZIPs do GitHub costumam ter uma pasta raiz (ex: projeto-main/)
    e dentro dela outra pasta src/ onde os módulos realmente vivem.
    Retorna o caminho absoluto da pasta que contém os módulos.
    """
    if not arquivos_py:
        return temp_dir

    # Pega o prefixo comum de todos os arquivos .py
    caminhos = [rel for _, rel in arquivos_py]
    partes_comuns = caminhos[0].split("/")

    for caminho in caminhos[1:]:
        partes = caminho.split("/")
        partes_comuns = [p for i, p in enumerate(partes_comuns) if i < len(partes) and p == partes[i]]
        if not partes_comuns:
            break

    # Remove a parte do nome do arquivo (último elemento)
    # e usa o prefixo de pastas comuns como raiz
    prefixo = "/".join(partes_comuns)
    raiz = os.path.join(temp_dir, prefixo) if prefixo else temp_dir

    # Se a raiz resultante não existir como dir, sobe um nível
    if not os.path.isdir(raiz):
        raiz = os.path.dirname(raiz)

    return raiz if os.path.isdir(raiz) else temp_dir

def analisar_zip_com_ast(temp_dir: str, arquivos_py: list, todos_modulos: list) -> "Grafo":
    """
    Analisa dependências usando AST local (rápido, sem API).
    Detecta automaticamente a pasta raiz do projeto dentro do ZIP
    para resolver corretamente os caminhos de import.
    """
    from src.io.py_parser import analisar_projeto_python

    mapa = construir_mapa_modulos(arquivos_py)

    graph = Grafo()
    for mod_grafo in todos_modulos:
        graph.adicionar_vertice(mod_grafo)

    # Tenta múltiplas raízes: a raiz detectada + subpastas comuns
    raiz_principal = detectar_raiz_projeto(temp_dir, arquivos_py)
    raizes_para_tentar = [raiz_principal]

    # Adiciona subpastas candidatas (ex: src/, app/, lib/)
    for subpasta in ["src", "app", "lib", "source"]:
        candidata = os.path.join(raiz_principal, subpasta)
        if os.path.isdir(candidata):
            raizes_para_tentar.append(candidata)

    # Também tenta a pasta pai da raiz (caso o ZIP tenha projeto-main/src/arquivos)
    pai = os.path.dirname(raiz_principal)
    if pai != raiz_principal and os.path.isdir(pai):
        raizes_para_tentar.insert(0, pai)

    deps_encontradas = set()
    for raiz in raizes_para_tentar:
        projeto_info = analisar_projeto_python(raiz)
        for dep in projeto_info.get("dependencias", []):
            origem_parser  = dep.get("origem", "")
            destino_parser = dep.get("destino", "")
            origem_grafo   = mapa.get(origem_parser)
            destino_grafo  = mapa.get(destino_parser)
            if origem_grafo and destino_grafo and origem_grafo != destino_grafo:
                par = (origem_grafo, destino_grafo)
                if par not in deps_encontradas:
                    deps_encontradas.add(par)
                    graph.adicionar_aresta(origem_grafo, destino_grafo)

    return graph


def construir_mapa_modulos(arquivos_py: list) -> dict:
    """
    Constrói um mapa flexível: várias formas de referenciar um módulo -> caminho canônico.
    Isso resolve o problema de o Groq retornar "chatbot/mensagens.py" enquanto
    o módulo está indexado como "sistema-main/src/chatbot/mensagens.py".
    """
    mapa = {}
    for full_path, rel_path in arquivos_py:
        # Chave 1: caminho completo (ex: "sistema-main/src/chatbot/mensagens.py")
        mapa[rel_path] = rel_path

        partes = rel_path.split("/")
        # Chave 2: só o nome do arquivo (ex: "mensagens.py")
        mapa[partes[-1]] = rel_path

        # Chaves 3..N: todos os sufixos possíveis
        # ex: "chatbot/mensagens.py", "src/chatbot/mensagens.py", etc.
        for i in range(1, len(partes)):
            sufixo = "/".join(partes[i:])
            if sufixo not in mapa:
                mapa[sufixo] = rel_path

            # Também com prefixo "src/" caso o import use "from src.X import Y"
            com_src = "src/" + sufixo
            if com_src not in mapa:
                mapa[com_src] = rel_path

    return mapa


def extrair_imports_ast(filepath: str) -> list:
    """
    Extrai todos os nomes de módulos importados de um arquivo .py via AST.
    Retorna lista de strings como ["src.banco_dados.conexao", "entidades.paciente"].
    """
    import ast as _ast
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            tree = _ast.parse(f.read())
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, _ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except Exception:
        pass
    return imports

# ── Carregar arquivo ──────────────────────────────────────
def normalizar_string(valor) -> str:
    if valor is None: return ""
    return str(valor).strip()

def carregar_grafo_de_arquivo(file_path):
    graph  = Grafo()
    avisos = []
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict):
                modulos = data.get("modulos") or []
                if not isinstance(modulos, list): modulos = []
                for m in modulos:
                    nome = normalizar_string(m)
                    if nome: graph.adicionar_vertice(nome)
                deps = data.get("dependencias") or []
                if not isinstance(deps, list): deps = []
                for dep in deps:
                    if not isinstance(dep, dict): avisos.append(f"Ignorado: {dep}"); continue
                    o = normalizar_string(dep.get("origem") or dep.get("source") or dep.get("from") or "")
                    d = normalizar_string(dep.get("destino") or dep.get("target") or dep.get("to") or "")
                    if o and d: graph.adicionar_aresta(o, d)
            else:
                st.error("Formato JSON não reconhecido."); return None
        elif file_path.endswith('.csv'):
            import csv
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    o = normalizar_string(row.get("origem") or row.get("source") or "")
                    d = normalizar_string(row.get("destino") or row.get("target") or "")
                    if o and d: graph.adicionar_aresta(o, d)
        if avisos:
            st.warning(f"{len(avisos)} item(ns) ignorado(s).")
        return graph
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}"); return None

# ── Detalhes do módulo ────────────────────────────────────
def exibir_detalhes_modulo(modulo: str):
    graph = st.session_state.graph
    importa       = graph.obter_vizinhos(modulo)
    importado_por = [o for o, d in graph.obter_arestas() if d == modulo]
    
    st.markdown(f"""
    <div class="dep-card">
        <div class="dep-title">📦 {modulo}</div>
        
        <div class="dep-import-box">
            <b class="text-import">→ Importa ({len(importa)}):</b><br>
            {'<br>'.join([f'&nbsp;&nbsp;• {v}' for v in importa]) if importa else '&nbsp;&nbsp;(nenhum)'}
        </div>
        
        <div class="dep-imported-box">
            <b class="text-imported">← Importado por ({len(importado_por)}):</b><br>
            {'<br>'.join([f'&nbsp;&nbsp;• {v}' for v in importado_por]) if importado_por else '&nbsp;&nbsp;(nenhum — módulo folha)'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-header">ENTRADA DE DADOS</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Arraste um arquivo", type=["json", "csv", "zip"], label_visibility="collapsed")

    if uploaded_file:
        try:
            extensao = uploaded_file.name.split('.')[-1].lower()
            graph = None

            if extensao == 'zip':
                temp_dir, arquivos_py, todos_modulos = processar_zip_com_py(uploaded_file)
                if arquivos_py is None:
                    st.error("Nenhum arquivo .py encontrado no ZIP.")
                else:
                    total = len(arquivos_py)

                    st.info(f"{total} arquivo(s)")
                    with st.spinner(f"Analisando {total} arquivo(s) via AST..."):
                            graph = analisar_zip_com_ast(temp_dir, arquivos_py, todos_modulos)
                    st.success(f"{total} arquivo(s) analisados via AST")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extensao}") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                graph = carregar_grafo_de_arquivo(tmp_path)
                os.unlink(tmp_path)

            if graph:
                st.session_state.graph              = graph
                st.session_state.service            = DependencyService(graph)
                st.session_state.chat_history       = []
                st.session_state.modulo_selecionado = None
                st.success("Arquivo carregado!")
        except Exception as e:
            st.error(f"Erro: {e}")

    if st.session_state.graph:
        st.markdown("---")
        st.info(
            f"**{len(st.session_state.graph.obter_vertices())}** módulos\n"
            f"**{len(st.session_state.graph.obter_arestas())}** dependências"
        )
    else:
        st.markdown('<div style="color:#8B949E;font-size:0.8rem;margin-top:10px;">Carregue um arquivo para começar</div>', unsafe_allow_html=True)

# ── CABEÇALHO ─────────────────────────────────────────────
st.markdown("""
    <div class="header-card">
        <div class="header-title">
            <img src="https://img.icons8.com/ios-filled/50/58A6FF/hexagon.png" width="30"/>
            DepGraph <span class="header-description">Análise de Dependências Python</span>
        </div>
        <div class="header-subtitle">Teoria dos Grafos — <b>Grupo 1</b></div>
    </div>
    """, unsafe_allow_html=True)

# ── CONFIGURAÇÃO DAS ABAS ──────────────────────────────────
tabs = st.tabs([
    "Grafo",
    "Ciclos",
    "Ordenação",
    "Impacto"
])

# ── ABA 0: GRAFO ────────────────────────────────────────────
with tabs[0]:
    st.markdown(
        section_title(GRAPH_ICON, "Visualização do Grafo"),
        unsafe_allow_html=True
    )    
    if st.session_state.graph:
        col1, col2 = st.columns([4, 1])

        with col2:
            st.markdown("### Filtros")
            show_cycles = st.checkbox("Destacar Ciclos", value=True)
            show_impact = st.checkbox("Destacar Impacto", value=False)
            selected_impact = None
            if show_impact:
                _verts = st.session_state.graph.obter_vertices()
                _nomes = gerar_nomes_exibicao(_verts)
                _sel_impact = st.selectbox("Módulo Alvo:", options=_verts, format_func=lambda v: _nomes.get(v, v))
                selected_impact = _sel_impact

            st.markdown("---")
            st.markdown("### Detalhes")
            _todos_vertices = st.session_state.graph.obter_vertices()
            _mapa_nomes = gerar_nomes_exibicao(_todos_vertices)

            modulo_sel = st.selectbox(
                "Clique num módulo:",
                options=["(nenhum)"] + _todos_vertices,
                format_func=lambda v: _mapa_nomes.get(v, v) if v != "(nenhum)" else "(nenhum)",
                key="mod_sel"
            )
            if modulo_sel != "(nenhum)":
                st.session_state.modulo_selecionado = modulo_sel
            else:
                st.session_state.modulo_selecionado = None

        with col1:
            ciclos_para_desenho  = st.session_state.service.detectar_ciclos().get("ciclos", []) if show_cycles else []
            impacto_para_desenho = st.session_state.service.calcular_cone_impacto(selected_impact).get("impactados", []) if show_impact and selected_impact else []

            # Utiliza a função corrigida do seu visualizer.py
            html_grafo = desenhar_grafo_interativo(
                st.session_state.graph,
                ciclos=ciclos_para_desenho,
                impacto=impacto_para_desenho,
                modulo_foco=st.session_state.modulo_selecionado
            )
            if html_grafo:
                components.html(html_grafo, height=615, scrolling=False)
                st.caption("Passe o mouse sobre um nó para ver suas dependências.")

        if st.session_state.modulo_selecionado:
            st.markdown("---")
            exibir_detalhes_modulo(st.session_state.modulo_selecionado)
            if st.button("Analisar este módulo com IA", key="ia_modulo"):
                with st.spinner("Analisando..."):
                    mod = st.session_state.modulo_selecionado
                    importa       = st.session_state.graph.obter_vizinhos(mod)
                    importado_por = [o for o, d in st.session_state.graph.obter_arestas() if d == mod]
prompt = (
                        f'Você é um especialista em engenharia de software.\n'
                        f'Analise o módulo "{mod}" e explique em português:\n'
                        f'1. O papel deste módulo no sistema.\n'
                        f'2. Por que ele importa: {importa if importa else "nenhum módulo interno"}.\n'
                        f'3. Quem depende dele ({importado_por if importado_por else "ninguém"}) e o impacto disso.\n'
                        f'4. Risco se for modificado ou removido.\n'
                        f'Contexto: {montar_contexto_grafo()}'
                    )
                    renderizar_resposta_ia(explicar_com_ia(prompt))

        st.markdown("---")
        if st.button("Explicar grafo completo com IA", key="ia_grafo"):
            with st.spinner("Analisando o grafo..."):
                prompt = (
                    'Analise o grafo de dependências e explique em português:\n'
                    '1. Quais módulos dependem de quais.\n'
                    '2. Quais são os mais críticos (mais importados).\n'
                    '3. Quais são módulos folha.\n'
                    '4. Exemplo real do que acontece se um módulo central for modificado.\n'
                    f'{montar_contexto_grafo()}'
                )
                renderizar_resposta_ia(explicar_com_ia(prompt))
    else:
        st.markdown(
            '<div class="upload-prompt">'
            '<img src="https://img.icons8.com/ios/100/30363D/hexagon.png"/>'
            '<p class="upload-prompt-text">Carregue um arquivo para visualizar o grafo</p>'
            '</div>', 
            unsafe_allow_html=True
        )


# ── ABA 1: CICLOS ───────────────────────────────────────────
with tabs[1]:
    st.markdown(
        section_title(CYCLE_ICON, "Detecção de Ciclos"),
        unsafe_allow_html=True
    )

    if st.session_state.service:
        resultado = st.session_state.service.detectar_ciclos()
        if resultado.get("tem_ciclos"):
            st.error(f"{len(resultado.get('ciclos', []))} ciclo(s) encontrado(s)!")
            for i, ciclo in enumerate(resultado.get("ciclos", []), 1):
                st.code(f"Ciclo {i}: " + " → ".join(ciclo))
        else:
            st.success("Nenhum ciclo detectado! O grafo é acíclico (DAG).")

        st.markdown("---")
        if st.button("Explicar ciclos com IA", key="ia_ciclos"):
            with st.spinner("Analisando..."):
                ciclos     = resultado.get("ciclos", [])
                ciclos_str = "\n".join([f"Ciclo {i+1}: " + " → ".join(c) for i, c in enumerate(ciclos)]) if ciclos else "Nenhum."
                prompt = (
                    'Analise os ciclos de dependência e explique em português:\n'
                    '1. O que cada ciclo significa na prática.\n'
                    '2. Exemplo real do problema causado (ex: ImportError circular).\n'
                    '3. Como resolver cada ciclo (refatoração concreta).\n'
                    f'{montar_contexto_grafo()}\n'
                    f'Ciclos: {ciclos_str}'
                )
                renderizar_resposta_ia(explicar_com_ia(prompt))
    else:
        st.info("Aguardando carregamento do projeto...")


# ── ABA 2: ORDENAÇÃO ────────────────────────────────────────
with tabs[2]:
    st.markdown(
        section_title(ORDER_ICON, "Ordenação Topológica"),
        unsafe_allow_html=True
    )
    if st.session_state.service:
        resultado       = st.session_state.service.ordenacao_topologica()
        ordem           = resultado.get("ordem", [])
        nao_processados = resultado.get("nao_processados", [])
        sucesso         = resultado.get("sucesso", False)

        def formatar_item(i, caminho, status="ok"):
            partes = caminho.split("/")
            arquivo = partes[-1]
            pasta = "/".join(partes[:-1]) + "/" if len(partes) > 1 else ""

            return (
                f'<div class="ordem-card {status}">'
                f'<span class="ordem-idx">{i}</span>'
                f'<span><span class="ordem-pasta">{pasta}</span><span class="ordem-arquivo">{arquivo}</span></span>'
                '</div>'
            )

        if sucesso:
            st.success("Ordem completa de compilação:")
            itens = "".join([formatar_item(i+1, m) for i, m in enumerate(ordem)])
            st.markdown(f'<div style="margin-top:1rem;">{itens}</div>', unsafe_allow_html=True)
        else:
            st.warning("Ciclos detectados — ordenação parcial disponível.")
            if ordem:
                st.markdown("**Módulos ordenados:**")
                itens = "".join([formatar_item(i+1, m) for i, m in enumerate(ordem)])
                st.markdown(f'<div style="margin-top:1rem; margin-bottom:1.5rem;">{itens}</div>', unsafe_allow_html=True)
            if nao_processados:
                st.markdown("**Bloqueados por ciclos:**")
                itens = "".join([formatar_item("⛔", m, "erro") for m in nao_processados])
                st.markdown(f'<div style="margin-top:1rem;">{itens}</div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Explicar com IA", key="ia_ordem"):
            with st.spinner("Analisando..."):
                prompt = (
                    'Explique a ordenação topológica em português:\n'
                    '1. O que significa a ordem gerada.\n'
                    '2. Exemplo real do que acontece na ordem errada.\n'
                    '3. Se houver bloqueados, como resolver.\n'
                    f'{montar_contexto_grafo()}\n'
                    f'Ordem: {" → ".join(ordem) if ordem else "Nenhuma."}\n'
                    f'Bloqueados: {", ".join(nao_processados) if nao_processados else "Nenhum."}'
                )
                renderizar_resposta_ia(explicar_com_ia(prompt))
    else:
        st.info("Aguardando carregamento do projeto...")


# ── ABA 3: IMPACTO ──────────────────────────────────────────
with tabs[3]:
    st.markdown(
        section_title(IMPACT_ICON, "Análise de Impacto"),
        unsafe_allow_html=True
    )
    
    if st.session_state.service:
        mod = st.selectbox("Escolha o módulo:", options=st.session_state.graph.obter_vertices(), key="impact_sel")
        col1, col2 = st.columns(2)
        with col1: analisar    = st.button("Analisar impacto", key="btn_impact")
        with col2: analisar_ia = st.button("Analisar com IA",  key="btn_ia_impact")

        if analisar or analisar_ia:
            res        = st.session_state.service.calcular_cone_impacto(mod)
            impactados = res.get("impactados", [])
            camadas    = res.get("camadas", [])

            if impactados:
                st.warning(f"{len(impactados)} módulo(s) para revalidar:")
                for i, camada in enumerate(camadas, 1):
                    label = "Direto" if i == 1 else f"Transitivo (distância {i})"
                    st.markdown(f"**{label}:** {' · '.join([f'`{m}`' for m in camada])}")
            else:
                st.success("Nenhum módulo impactado.")

            if analisar_ia:
                with st.spinner("Analisando..."):
                    camadas_str = "\n".join([f"  Distância {i+1}: {', '.join(c)}" for i, c in enumerate(camadas)]) if camadas else "  Nenhum."
                    prompt = (
                        f'O desenvolvedor vai modificar "{mod}". Explique em português:\n'
                        '1. Quais módulos serão afetados diretamente e por que.\n'
                        '2. Quais serão afetados indiretamente.\n'
                        '3. Exemplo real do que pode quebrar.\n'
                        '4. Ordem recomendada para re-testar.\n'
                        f'{montar_contexto_grafo()}\n'
                        f'Módulo: {mod}\n'
                        f'Impacto:\n{camadas_str}'
                    )
                    renderizar_resposta_ia(explicar_com_ia(prompt))
    else:
        st.info("Aguardando carregamento do projeto...")

# ── CHAT DRAWER ──────────────────────────────────────────
# Estratégia: st.text_input invisível como ponte JS → Python.
# O JS escreve no input via execCommand/nativeInputValueSetter,
# dispara um evento 'input', e o Streamlit faz rerun automaticamente.

# Input invisível que recebe a mensagem do JS
# Esconde o input ponte via CSS — label_visibility não esconde o campo visual
st.markdown('<style>[data-testid="stTextInput"]:last-of-type { position: absolute !important; opacity: 0 !important; height: 0 !important; pointer-events: none !important; }</style>', unsafe_allow_html=True)
chat_input_ponte = st.text_input(
    "chat_ponte",
    key="chat_ponte",
    label_visibility="collapsed"
)

#  ── Processa mensagem se chegou algo no input ponte ──────────────────────────────────────────
if chat_input_ponte and chat_input_ponte != st.session_state.get("last_chat_msg", ""):
    st.session_state["last_chat_msg"] = chat_input_ponte
    st.session_state.chat_open = True

    if not st.session_state.chat_history or st.session_state.chat_history[-1].get("content") != chat_input_ponte:
        st.session_state.chat_history.append({"role": "user", "content": chat_input_ponte})

    contexto = montar_contexto_grafo()
    system_msg = f"""Você é um agente especialista em análise de dependências de software Python.
Responda em português, de forma clara e direta, usando os nomes reais dos módulos do projeto.
Seja conciso mas informativo.

Contexto do projeto:
{contexto if contexto else 'Nenhum projeto carregado ainda.'}"""

    messages = [{"role": "system", "content": system_msg}]
    for msg in st.session_state.chat_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    with st.spinner("🤖 Agente IA pensando..."):
        resposta = chamar_groq(messages, max_tokens=800)

    st.session_state.chat_history.append({"role": "assistant", "content": resposta})
    st.rerun()

#  ── Monta histórico para o JS ──────────────────────────────────────────
chat_msgs_js = ""
for msg in st.session_state.chat_history:
    safe = (msg["content"]
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br>"))
    role = "user" if msg["role"] == "user" else "ia"
    chat_msgs_js += f'addMsg("{role}", `{safe}`);\n'

drawer_open_js = "true" if st.session_state.chat_open else "false"
