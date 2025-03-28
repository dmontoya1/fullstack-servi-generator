from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fullstack-project-generator",
    version="0.1.0",
    author="Tu Nombre",
    author_email="tu.email@example.com",
    description="Generador de proyectos FullStack con configuraciones predefinidas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.tu-usuario/fullstack-project-generator",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click>=8.1.3',
        'pyyaml>=6.0',
        'cookiecutter>=2.1.1',
    ],
    entry_points={
        'console_scripts': [
            'fullstack-gen=fullstack_generator.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.8',
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black',
            'mypy',
        ],
    },
)
