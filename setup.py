from setuptools import setup, find_packages

setup(
    name="easy-api",
    version="0.2.0",
    description="A FastAPI project generator",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Jackson Severino da Rocha",
    author_email="jacksonsr451@gmail.com",
    url="https://github.com/jacksonsr451/jackson_easy_api",
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
    entry_points={
        'console_scripts': [
            'start=jackson_easy_api.cli:start_project',
        ],
    },
)
