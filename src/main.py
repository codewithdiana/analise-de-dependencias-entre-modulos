"""
Módulo: main.py
Responsabilidade: ponto de entrada do sistema.
"""

from src.core.grafo import Grafo
from src.service.dependency_service import DependencyService


def main():
    print("Projeto executado pela interface Streamlit.")
    print("Use o comando:")
    print("python -m streamlit run ui/app.py")


if __name__ == "__main__":
    main()
