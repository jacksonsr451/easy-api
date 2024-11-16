from setuptools import setup
import os
import subprocess

def post_install():
    subprocess.call([os.path.join(os.path.dirname(__file__), 'post_install.py')])

setup(
    name="easy-api",
    version="0.1.3",
    description="A FastAPI project generator",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Jackson Severino da Rocha",
    author_email="jacksonsr451@gmail.com",
    url="https://github.com/jacksonsr451/easy-api",
    packages=['jackson_easy_api'],
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
    data_files=[('', ['jackson_easy_api/manage.py'])],
    entry_points={
        'console_scripts': [
            'post-install = post_install:move_manage_py',
        ],
    },
)

post_install()
