# dentro de jackson_easy_api/cli.py

import os
import shutil
from pathlib import Path
import subprocess
import sys

def install_dependencies():
    try:
        if os.path.exists('poetry.lock'):
            print("Poetry detected. Installing dependencies using Poetry...")
            subprocess.check_call([sys.executable, '-m', 'poetry', 'install'])
            print("Dependencies installed successfully using Poetry.")
        elif os.path.exists('requirements.txt'):
            print("Poetry not detected. Installing dependencies using pip...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("Dependencies installed successfully using pip.")
        else:
            print("No poetry.lock or requirements.txt found. Please ensure you're using a dependency manager.")
    except subprocess.CalledProcessError as e:
        print(f"Error while installing dependencies: {e}")

def start_project():
    install_dependencies()
    
    source = os.path.join(os.path.dirname(__file__), 'manage.py')
    destination = os.path.join(Path.cwd(), 'manage.py')

    if not os.path.exists(destination):
        try:
            shutil.copy(source, destination)
            print(f"'manage.py' foi copiado para a raiz do projeto.")
        except Exception as e:
            print(f"Erro ao copiar 'manage.py': {e}")
    else:
        print(f"Arquivo 'manage.py' já existe na raiz do projeto.")
