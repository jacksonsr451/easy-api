# dentro de jackson_easy_api/cli.py

import os
import shutil
from pathlib import Path
import subprocess
import sys

def format_app(app_name: str):
    """
    Format the given app using isort and blue, using Poetry or pip as appropriate.
    """
    if not os.path.isdir(app_name):
        print(f"Error: The app directory '{app_name}' does not exist.")
        return

    try:
        print(f"Formatting the app: {app_name}")

        if os.path.exists("poetry.lock"):
            print("Poetry detected. Using Poetry to run formatters...")
            subprocess.check_call(["poetry", "run", "isort", app_name])
            subprocess.check_call(["poetry", "run", "blue", app_name])
        elif os.path.exists("requirements.txt"):
            print("Poetry not detected. Using pip to run formatters...")
            subprocess.check_call([sys.executable, "-m", "isort", app_name])
            subprocess.check_call([sys.executable, "-m", "blue", app_name])
        else:
            print("No dependency manager detected (poetry.lock or requirements.txt not found).")
            return

        print("Formatting completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during formatting: {e}")

def install_dependencies():
    try:
        packages = [
            "sqlalchemy",
            "alembic",
            "psycopg2-binary",
            "python-decouple",
            "pytest",
            "fastapi",
            "uvicorn",
        ]
        if os.path.exists('poetry.lock'):
            print("Poetry detected. Installing dependencies using Poetry...")
            
            for package in packages:
                subprocess.check_call(['poetry', 'add', package])
            print("Dependencies installed successfully using Poetry.")
        elif os.path.exists('requirements.txt'):
            print("Poetry not detected. Installing dependencies using pip...")
            for package in packages:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
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
