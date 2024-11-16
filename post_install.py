# post_install.py
import os
import shutil
import sys

def move_manage_py():
    source = os.path.join(os.path.dirname(__file__), 'jackson_easy_api', 'manage.py')

    destination = os.path.join(os.getcwd(), 'manage.py')

    try:
        if os.path.exists(source):
            shutil.copy(source, destination)
            print("Arquivo 'manage.py' copiado para a raiz do projeto.")
        else:
            print("O arquivo 'manage.py' não foi encontrado no pacote.")
    except Exception as e:
        print(f"Erro ao mover 'manage.py': {e}")

if __name__ == '__main__':
    move_manage_py()
