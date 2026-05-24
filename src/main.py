"""
Módulo: main.py
Responsabilidade: Lançador do servidor Streamlit.
"""
import subprocess
import sys

def main():
    print("🚀 Iniciando a interface web do DepGraph...")
    # Executa o comando do Streamlit automaticamente
    subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/app.py"])

if __name__ == "__main__":
    main()
