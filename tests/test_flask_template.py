# tests/test_flask_template.py

import os
import tempfile
from generator.templates_manager import render_template


def test_flask_template_structure():
    """
    Valida que, al renderizar la plantilla Flask, se cree la estructura de archivos y carpetas esperada.
    """
    # Crear un directorio temporal para la prueba
    with tempfile.TemporaryDirectory() as temp_dir:
        # Ruta de la plantilla para Flask
        template_dir = os.path.join("templates", "backend", "flask", "project_template")
        # Directorio destino (por ejemplo, "test_flask_project")
        dest_dir = os.path.join(temp_dir, "test_flask_project")
        # Contexto para renderizar (variables que se reemplazarán en los archivos y nombres de carpetas)
        context = {"project_slug": "test_flask_project", "author": "Tester", "docker": False}

        # Renderizar la plantilla en el directorio destino
        render_template(template_dir, dest_dir, context)

        # Imprimir la lista de archivos y carpetas creados (útil para debug)
        print("Archivos creados:", os.listdir(dest_dir))

        # Verificar que se hayan creado archivos esenciales
        assert os.path.exists(os.path.join(dest_dir, ".gitignore")), ".gitignore no fue creado"
        assert os.path.exists(os.path.join(dest_dir, "README.md")), "README.md no fue creado"
        assert os.path.exists(os.path.join(dest_dir, "requirements.txt")), "requirements.txt no fue creado"

        # Verificar que exista la carpeta 'app'
        app_dir = os.path.join(dest_dir, "app")
        assert os.path.exists(app_dir), "La carpeta 'app' no fue creada"

        # Dentro de 'app', se debe encontrar el archivo __init__.py (Application Factory)
        assert os.path.exists(os.path.join(app_dir, "__init__.py")), "app/__init__.py no fue creado"

        # Verificar la presencia de otros archivos en 'app'
        assert os.path.exists(os.path.join(app_dir, "models.py")), "app/models.py no fue creado"
        assert os.path.exists(os.path.join(app_dir, "extensions.py")), "app/extensions.py no fue creado"

        # Verificar la carpeta de blueprints y su __init__.py
        blueprints_dir = os.path.join(app_dir, "blueprints")
        assert os.path.exists(blueprints_dir), "app/blueprints no fue creada"
        assert os.path.exists(os.path.join(blueprints_dir, "__init__.py")), "app/blueprints/__init__.py no fue creado"

        # Verificar que exista la carpeta de templates en app
        assert os.path.exists(os.path.join(app_dir, "templates")), "app/templates no fue creada"