# Easy API

Easy API is a simple library for building APIs using FastAPI and SQLAlchemy. It provides an easy-to-use framework to help you create and manage APIs with minimal effort.

## Installation

To install Easy API, run the following command:

```bash
pip install jackson_easy_api
```

After installation, run the `start` command to initialize your project and generate the `manage.py` file in the root of your project:

```bash
start
```

## Available Commands

```
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
start createproject my_project
```

2. Create a new app within the project:

```bash
start createapp my_app
```

3. Make migrations for your app:

```bash
start makemigrations
```

4. Apply migrations to the database:

```bash
start migrate
```

5. Run tests for a specific app:

```bash
start test my_app
```

## Documentation

For detailed documentation and usage examples, please visit the [GitHub repository](https://github.com/jacksonsr451/jackson_easy_api).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


