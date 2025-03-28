import os
import json

class DockerConfigGenerator:
    def __init__(self):
        pass
    
    def generate(self, project_name: str, backend_framework: str, 
                 frontend_framework: str, output_dir: str):
        """
        Generar configuraciones de Docker para el proyecto
        
        :param project_name: Nombre del proyecto
        :param backend_framework: Framework de backend
        :param frontend_framework: Framework de frontend
        :param output_dir: Directorio de salida
        """
        project_path = os.path.join(output_dir, project_name)
        
        # Dockerfile para Backend
        backend_dockerfile = self._get_backend_dockerfile(backend_framework)
        with open(os.path.join(project_path, 'backend', 'Dockerfile'), 'w') as f:
            f.write(backend_dockerfile)
        
        # Dockerfile para Frontend
        frontend_dockerfile = self._get_frontend_dockerfile(frontend_framework)
        with open(os.path.join(project_path, 'frontend', 'Dockerfile'), 'w') as f:
            f.write(frontend_dockerfile)
        
        # Docker Compose
        docker_compose = self._get_docker_compose(project_name)
        with open(os.path.join(project_path, 'docker-compose.yml'), 'w') as f:
            f.write(docker_compose)
    
    def _get_backend_dockerfile(self, backend_framework: str) -> str:
        """Generar Dockerfile para backend según el framework"""
        dockerfiles = {
            'django': '''
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
''',
            'flask': '''
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
''',
            'fastapi': '''
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        }
        return dockerfiles.get(backend_framework, dockerfiles['django'])
    
    def _get_frontend_dockerfile(self, frontend_framework: str) -> str:
        """Generar Dockerfile para frontend según el framework"""
        dockerfiles = {
            'vue': '''
FROM node:14

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8080
CMD ["npm", "run", "serve"]
''',
            'react': '''
FROM node:14

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "start"]
''',
            'angular': '''
FROM node:14

WORKDIR /app

COPY package*.json ./
RUN npm install @angular/cli
RUN npm install

COPY . .

EXPOSE 4200
CMD ["ng", "serve", "--host", "0.0.0.0"]
'''
        }
        return dockerfiles.get(frontend_framework, dockerfiles['react'])
    
    def _get_docker_compose(self, project_name: str) -> str:
        """Generar Docker Compose básico"""
        return f'''
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
'''