import sys
import os
import subprocess
import argparse
from alembic import command
from alembic.config import Config

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def generate_migration(message: str):
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, message=message, autogenerate=True)


def find_package_name():
    base_path = os.getcwd()

    for root, dirs, files in os.walk(base_path):
        if 'main.py' in files:
            return os.path.basename(root)

    raise FileNotFoundError("main.py not found in the project directory.")

def create_alembic_ini(project_path: str):
    alembic_ini_content = """[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.
sqlalchemy.url =

[post_write_hooks]
# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
    with open(os.path.join(project_path, "alembic.ini"), "w") as file:
        file.write(alembic_ini_content)
    print("File 'alembic.ini' created.")


def create_alembic_env_file(project_path: str, app_name: str):
    alembic_env_content = """import sys
import importlib
from os.path import abspath, dirname
from sqlalchemy import engine_from_config, pool
from alembic import context
from decouple import config as env_config

from {app_name}.core.settings import settings

sys.path.append(dirname(dirname(abspath(__file__))))

from {app_name}.core.database import Base

DATABASE_URL = env_config("DATABASE_URL", default="sqlite:///./test.db")

config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)

for app_name in settings.apps:
    try:
        app_module = importlib.import_module(f"{app_name}.models")
        print(f"Models loaded from {app_name}")
    except ModuleNotFoundError:
        print(f"Could not load models from {app_name}")

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""".format(app_name=app_name)
    alembic_dir = os.path.join(project_path, "alembic")
    if not os.path.exists(alembic_dir):
        os.makedirs(alembic_dir)

    with open(os.path.join(alembic_dir, "env.py"), "w") as file:
        file.write(alembic_env_content)
    print("File 'env.py' created in alembic directory.")


def create_alembic_script_file(project_path: str):
    alembic_script_content = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
"""
    alembic_dir = os.path.join(project_path, "alembic")
    if not os.path.exists(alembic_dir):
        os.makedirs(alembic_dir)

    with open(os.path.join(alembic_dir, "script.py.mako"), "w") as file:
        file.write(alembic_script_content)
    print("File 'script.py.mako' created in alembic directory.")


def create_versions_folder(project_path: str):
    versions_dir = os.path.join(project_path, "alembic", "versions")
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
    print("Versions directory created.")

def create_gitignore(project_path: str):
    gitignore_content = """# .gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
*.manifest
*.spec
pip-log.txt
pip-delete-this-directory.txt
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/
*.mo
*.pot
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
instance/
.webassets-cache
.scrapy
docs/_build/
.pybuilder/
target/
.ipynb_checkpoints
profile_default/
ipython_config.py
.pdm.toml
__pypackages__/
celerybeat-schedule
celerybeat.pid
*.sage.py
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.spyderproject
.spyproject
.ropeproject
/site
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
cython_debug/
.idea/
.vscode/
poetry.toml
.ruff_cache/
pyrightconfig.json
test.db
"""

    with open(os.path.join(project_path, ".gitignore"), "w") as file:
        file.write(gitignore_content)
    print("File '.gitignore' created in {project_path}.".format(project_path=project_path))

def create_env(project_path: str):
    env_content = """# .env
DATABASE_URL=sqlite:///./test.db
"""

    with open(os.path.join(project_path, ".env"), "w") as file:
        file.write(env_content)
    print("File '.env' created in {project_path}.".format(project_path=project_path))

def create_project_structure(project_name: str):
    base_path = os.getcwd()

    project_path = os.path.join(base_path, project_name)

    if os.path.exists(project_path):
        print(f"Error: The project '{project_name}' already exists!")
        sys.exit(1)

    os.makedirs(project_path)
    os.makedirs(os.path.join(project_path, "core"))

    create_main_file(project_path)
    create_database_file(project_path)
    create_settings_file(project_path)
    create_alembic_ini(base_path)
    create_env(base_path)
    create_gitignore(base_path)

    create_alembic_env_file(base_path, project_name)
    create_alembic_script_file(base_path)
    create_versions_folder(base_path)

    print(f"Project '{project_name}' created successfully at {project_path}")

def create_main_file(project_path: str):
    main_content = """from {project_path}.core.settings import settings

app = settings.create_app()
""".format(project_path=project_path)
    with open(os.path.join(project_path, "__init__.py"), "w") as file:
        file.write("")

    with open(os.path.join(project_path, "main.py"), "w") as file:
        file.write(main_content)
    print("File 'main.py' created.")

def create_database_file(project_path: str):
    database_content = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_URL = config("DATABASE_URL", default="sqlite:///./test.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
    with open(os.path.join(project_path, "core", "database.py"), "w") as file:
        file.write(database_content)
    print("File 'database.py' created in 'core'.")

def create_settings_file(project_path: str):
    settings_content = """import importlib
from typing import List
from fastapi import FastAPI

class Settings:
    app_title: str = "API School"
    app_version: str = "1.0.0"
    apps: List[str] = []

    @staticmethod
    def create_app() -> FastAPI:
        application: FastAPI = FastAPI(
            title=settings.app_title,
            version=settings.app_version,
        )

        for app_name in settings.apps:
            app_module = importlib.import_module(f"{app_name}.routes")
            application.include_router(app_module.router, prefix=f"/{app_name}", tags=[app_name])

        return application

settings = Settings()
"""
    with open(os.path.join(project_path, "core", "__init__.py"), "w") as file:
        file.write("")

    with open(os.path.join(project_path, "core", "settings.py"), "w") as file:
        file.write(settings_content)
    print("File 'settings.py' created in 'core'.")

def create_app_structure(app_name: str):
    base_path = os.getcwd()

    app_path = os.path.join(base_path, app_name)

    if os.path.exists(app_path):
        print(f"Error: The app '{app_name}' already exists!")
        sys.exit(1)

    os.makedirs(app_path)

    package_name = find_package_name()

    files = {
        '__init__.py': """""",
        'tests.py': """# {app_name}.tests.py
import pytest
from fastapi.testclient import TestClient
from {package_name}.main import app

client = TestClient(app)

def test_example():
    response = client.get("/{app_name}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from {app_name}"}
""".format(app_name=app_name,package_name=package_name),
        'models.py': """# {app_name}.models.py
from sqlalchemy import Column, Integer, String
from {package_name}.core.database import Base

""".format(package_name=package_name, app_name=app_name),

        'routes.py': """# {app_name}.routes.py
from fastapi import APIRouter

router = APIRouter()

# Define your routes here
""".format(app_name=app_name),

        'schemas.py': """# {app_name}.schemas.py
from pydantic import BaseModel

""".format(app_name=app_name),

        'services.py': """# {app_name}.services.py
from .models import {app_name}
from sqlalchemy.orm import Session

""".format(app_name=app_name),
    }

    for filename, content in files.items():
        file_path = os.path.join(app_path, filename)
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created in '{app_path}'.")

    print(f"App '{app_name}' successfully created in {app_path}")

def run_tests(app_name=None):
    test_dir = os.getcwd()

    if app_name:
        test_dir = os.path.join(test_dir, app_name)

    print(f"Running tests in '{test_dir}'...")

    try:
        result = subprocess.run(['pytest', test_dir], check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed: {e.stderr}")
        sys.exit(1)

def main():
    # Set up argparse to handle the commands
    parser = argparse.ArgumentParser(description="Manage your FastAPI project")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Migrate command
    subparsers.add_parser("migrate", help="Run migrations")

    # Create project command
    create_project_parser = subparsers.add_parser("createproject", help="Create a new project")
    create_project_parser.add_argument("project_name", type=str, help="Name of the new project")

    # Make migrations command
    make_migrations_parser = subparsers.add_parser("makemigrations", help="Generate new migration with a message")
    make_migrations_parser.add_argument("message", type=str, help="The message for the new migration")

    # Create app command
    create_app_parser = subparsers.add_parser("createapp", help="Create a new app")
    create_app_parser.add_argument("app_name", type=str, help="Name of the new app")

    # Test command (new one)
    test_parser = subparsers.add_parser("test", help="Run tests for the specified app or all apps")
    test_parser.add_argument("app_name", nargs="?", type=str, help="Name of the app to run tests for (optional)")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "migrate":
        print("Running migrations...")
        run_migrations()
    elif args.command == "makemigrations":
        print(f"Generating migration: {args.message}")
        generate_migration(args.message)
    elif args.command == "createapp":
        print(f"Creating app: {args.app_name}")
        create_app_structure(args.app_name)
    elif args.command == "createproject":
        print(f"Creating project: {args.project_name}")
        create_project_structure(args.project_name)
    elif args.command == "test":
        print(f"Running tests for {args.app_name if args.app_name else 'all apps'}...")
        run_tests(args.app_name)
    elif args.command in ["--help", "-h"]:
        show_help()
    else:
        show_help()
        print(f"Unknown command: {args.command}")
        sys.exit(1)

def show_help():
    print("""
Usage: manage.py <command> [options]

Commands:
  createproject <name>  Create a new project with the given name
  createapp <name>  Create a new app with the given name
  makemigrations    Generate new migration with a message
  migrate           Run migrations
  test <app_name>   Run tests for the given app (or all apps if no app_name is provided)
  --help, -h        Show this help message
    """)

if __name__ == "__main__":
    main()

