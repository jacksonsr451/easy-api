from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        
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


setup(
    name="easy-api",
    version="0.2.0",
    description="A FastAPI project generator",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Jackson Severino da Rocha",
    author_email="jacksonsr451@gmail.com",
    url="https://github.com/jacksonsr451/easy-api",
    packages=find_packages(where=".", exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "alembic",
        "python-decouple",
        "pytest",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': CustomInstallCommand,
    },
)
