"""
Módulo: main.py
Responsabilidade: ponto de entrada do sistema — CLI com menu interativo.

Uso:
    python src/main.py --input data/exemplo_projeto.json
    python src/main.py --input data/exemplo_projeto.json --module database/connection.py
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.io.file_reader import carregar_grafo
from src.service.dependency_service import DependencyService


SEPARATOR = "─" * 60


def exibir_cabecalho():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Análise de Dependências em Sistemas de Software        ║")
    print("║   Teoria dos Grafos — DGJ                                ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()


def exibir_resumo(service):
    info = service.obter_resumo()
    print(f"  Grafo carregado com sucesso!")
    print(f"  Módulos (vértices): {info['vertices']}")
    print(f"  Dependências (arestas): {info['edges']}")
    print()


def executar_deteccao_ciclos(service):
    print(SEPARATOR)
    print("  [1] DETECÇÃO DE CICLOS — DFS com coloração de vértices")
    print(SEPARATOR)
    result = service.detectar_ciclos()

    if result["has_cycle"]:
        print(f"  ⚠  {len(result['cycles'])} ciclo(s) encontrado(s):\n")
        for i, cycle in enumerate(result["cycles"], 1):
            path = " → ".join(cycle)
            print(f"  Ciclo {i}: {path}")
    else:
        print("  ✓  Nenhum ciclo detectado! O grafo é acíclico (DAG).")
    print()


def executar_ordenacao_topologica(service):
    print(SEPARATOR)
    print("  [2] ORDENAÇÃO TOPOLÓGICA — Algoritmo de Kahn")
    print(SEPARATOR)
    result = service.ordenacao_topologica()

    if result["success"]:
        print("  ✓  Ordem segura de compilação:\n")
        for i, module in enumerate(result["order"], 1):
            print(f"  {i:2}. {module}")
    else:
        print("  ✗  Não foi possível gerar a ordenação — ciclo detectado!")
        print(f"  Módulos não processados: {result['unprocessed']}")
    print()


def run_impact_cone(service, module):
    print(SEPARATOR)
    print(f"  [3] CONE DE IMPACTO — BFS a partir de: {module}")
    print(SEPARATOR)
    result = service.calcular_cone_impacto(module)

    if not result["impacted"]:
        print("  Nenhum módulo impactado (módulo folha ou não encontrado).")
    else:
        print(f"  {len(result['impacted'])} módulo(s) precisam ser revalidados:\n")
        for i, layer in enumerate(result["layers"], 1):
            label = "direto" if i == 1 else f"transitivo (distância {i})"
            for mod in layer:
                print(f"  [{label}] {mod}")
    print()


def menu(service):
    while True:
        print(SEPARATOR)
        print("  Menu principal")
        print(SEPARATOR)
        print("  1. Detectar ciclos de dependência")
        print("  2. Ordenação topológica (ordem de build)")
        print("  3. Calcular cone de impacto de um módulo")
        print("  4. Listar todos os módulos")
        print("  0. Sair")
        print()

        choice = input("  Escolha uma opção: ").strip()

        if choice == "1":
            executar_deteccao_ciclos(service)

        elif choice == "2":
            executar_ordenacao_topologica(service)

        elif choice == "3":
            print("\n  Módulos disponíveis:")
            for mod in service.obter_resumo()["modules"]:
                print(f"    - {mod}")
            module = input("\n  Digite o nome do módulo: ").strip()
            run_impact_cone(service, module)

        elif choice == "4":
            print()
            for mod in service.obter_resumo()["modules"]:
                print(f"  • {mod}")
            print()

        elif choice == "0":
            print("\n  Encerrando. Até mais!\n")
            break

        else:
            print("\n  Opção inválida. Tente novamente.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Análise de Dependências em Sistemas de Software"
    )
    parser.add_argument(
        "--input", required=True,
        help="Caminho para o arquivo de entrada (.json ou .csv)"
    )
    parser.add_argument(
        "--module", default=None,
        help="Módulo para calcular cone de impacto (opcional)"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Executa todas as análises automaticamente e sai"
    )
    args = parser.parse_args()

    exibir_cabecalho()

    # Tela de entrada
    print(f"  Carregando grafo de: {args.input}")
    try:
        Grafo = carregar_grafo(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n  ERRO: {e}\n")
        sys.exit(1)

    service = DependencyService(Grafo)
    exibir_resumo(service)

    # Tela de resultado — modo automático
    if args.all:
        executar_deteccao_ciclos(service)
        executar_ordenacao_topologica(service)
        if args.module:
            run_impact_cone(service, args.module)
    elif args.module:
        run_impact_cone(service, args.module)
    else:
        # Modo interativo
        menu(service)


if __name__ == "__main__":
    main()
