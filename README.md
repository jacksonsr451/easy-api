# Jackson Easy API

Easy API is a simple library for building APIs using FastAPI and SQLAlchemy. It provides an easy-to-use framework to help you create and manage APIs with minimal effort.

## Installation

To install Easy API, run the following command:

```bash
pip install jackson_easy_api
```

After installation, run the \`start\` command to initialize your project and generate the \`manage.py\` file in the root of your project:

```bash
start
```

## Available Commands

```bash
Commands:
  createproject <name>   Create a new project with the given name
  createapp <name>       Create a new app within your project
  makemigrations         Generate a new migration with a message
  migrate                Apply migrations to the database
  test <app_name>        Run tests for the specified app (or all apps if no app_name is provided)
  --help, -h             Show this help message
```

## Example Usage

1. Create a new project:

```bash
python manage.py createproject my_project
```

2. Create a new app within the project:

```bash
python manage.py createapp my_app
```

> **Important**: After creating a new app, you must add the app name to the \`apps\` list in \`settings.py\`. This ensures the app's routes are included in the FastAPI application. 

Here's an example of how to modify \`settings.py\`:

```python
import importlib
from typing import List
from fastapi import FastAPI

class Settings:
    app_title: str = "API School"
    app_version: str = "1.0.0"
    apps: List[str] = ["my_app"]  # Add your app here

    @staticmethod
    def create_app() -> FastAPI:
        application: FastAPI = FastAPI(
            title=settings.app_title,
            version=settings.app_version,
        )

        # Loop through the apps and include their routes
        for app_name in settings.apps:
            app_module = importlib.import_module(f"{app_name}.routes")
            application.include_router(app_module.router, prefix=f"{app_name}", tags=[app_name])

        return application

settings = Settings()
```

This configuration will ensure that the routes for your app (\`my_app\` in this case) are included in the FastAPI application with a URL prefix of \`/my_app\`.

3. Make migrations for your app:

```bash
python manage.py makemigrations
```

4. Apply migrations to the database:

```bash
python manage.py migrate
```

5. Run tests for a specific app:

```bash
python manage.py test my_app
```

## Documentation

For detailed documentation and usage examples, please visit the [GitHub repository](https://github.com/jacksonsr451/jackson_easy_api).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.