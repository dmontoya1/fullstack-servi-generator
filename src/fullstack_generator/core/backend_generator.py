import os
import subprocess
from typing import Dict, Any

class BackendGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.templates_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'templates', 
            'backend'
        )
    
    def generate(self, project_name: str, framework: str, output_dir: str) -> str:
        """
        Genera la estructura de backend para un framework específico
        
        :param project_name: Nombre del proyecto
        :param framework: Framework de backend a utilizar
        :param output_dir: Directorio de salida
        :return: Ruta al directorio de backend generado
        """
        # Validar framework
        supported_frameworks = ['django', 'flask', 'fastapi']
        if framework not in supported_frameworks:
            raise ValueError(f"Framework {framework} no soportado")
        
        # Crear directorios
        backend_path = os.path.join(output_dir, project_name, 'backend')
        os.makedirs(backend_path, exist_ok=True)
        
        # Generar estructura según framework
        generator_method = getattr(self, f'_generate_{framework}')
        generator_method(project_name, backend_path)
        
        return backend_path
    
    def _generate_django(self, project_name: str, backend_path: str):
        """Generar estructura para proyecto Django"""
        # Inicializar proyecto Django
        subprocess.run([
            'django-admin', 
            'startproject', 
            f'{project_name}_backend', 
            backend_path
        ], check=True)
        
        # Crear directorios adicionales
        os.makedirs(os.path.join(backend_path, 'apps'), exist_ok=True)
        os.makedirs(os.path.join(backend_path, 'tests'), exist_ok=True)
        
        # Crear requirements.txt
        requirements = [
            'django',
            'djangorestframework',
            'django-cors-headers',
            'python-dotenv',
            'psycopg2-binary',
        ]
        with open(os.path.join(backend_path, 'requirements.txt'), 'w') as f:
            f.write('\n'.join(requirements))
    
    def _generate_flask(self, project_name: str, backend_path: str):
        """Generar estructura para proyecto Flask"""
        # Crear estructura base
        os.makedirs(os.path.join(backend_path, 'app'), exist_ok=True)
        os.makedirs(os.path.join(backend_path, 'tests'), exist_ok=True)
        
        # Archivo principal de la aplicación
        with open(os.path.join(backend_path, 'app', '__init__.py'), 'w') as f:
            f.write('''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
''')
        
        # Crear requirements.txt
        requirements = [
            'flask',
            'flask-sqlalchemy',
            'flask-marshmallow',
            'python-dotenv',
        ]
        with open(os.path.join(backend_path, 'requirements.txt'), 'w') as f:
            f.write('\n'.join(requirements))
    
    def _generate_fastapi(self, project_name: str, backend_path: str):
        """Generar estructura para proyecto FastAPI"""
        # Crear estructura base
        os.makedirs(os.path.join(backend_path, 'app'), exist_ok=True)
        os.makedirs(os.path.join(backend_path, 'tests'), exist_ok=True)
        
        # Archivo principal
        with open(os.path.join(backend_path, 'app', 'main.py'), 'w') as f:
            f.write('''
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}
''')
        
        # Crear requirements.txt
        requirements = [
            'fastapi',
            'uvicorn',
            'sqlalchemy',
            'pydantic',
            'python-dotenv',
        ]
        with open(os.path.join(backend_path, 'requirements.txt'), 'w') as f:
            f.write('\n'.join(requirements))