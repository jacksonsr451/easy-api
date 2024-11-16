# dentro de jackson_easy_api/cli.py

import os
import shutil
from pathlib import Path

def start_project():
    # Caminho do arquivo manage.py dentro do pacote
    source = os.path.join(os.path.dirname(__file__), 'manage.py')

    # Caminho de destino onde o manage.py será copiado para a raiz do projeto
    destination = os.path.join(Path.cwd(), 'manage.py')

    # Verificar se o manage.py já existe na raiz do projeto
    if not os.path.exists(destination):
        try:
            shutil.copy(source, destination)
            print(f"'manage.py' foi copiado para a raiz do projeto.")
        except Exception as e:
            print(f"Erro ao copiar 'manage.py': {e}")
    else:
        print(f"Arquivo 'manage.py' já existe na raiz do projeto.")
