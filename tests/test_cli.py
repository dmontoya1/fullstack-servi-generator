# tests/test_cli.py

import os
import tempfile
import pytest
from generator.templates_manager import render_template

def test_render_template_crea_estructura():
    # Crear un directorio temporal para la prueba
    with tempfile.TemporaryDirectory() as temp_dir:
        template_dir = os.path.join("templates", "backend", "django", "project_template")
        dest_dir = os.path.join(temp_dir, "test_project")
        context = {"project_slug": "test_project", "author": "Tester", "docker": False, "drf": False}
        
        render_template(template_dir, dest_dir, context)

        print("Archivos creados:", )
        print(os.listdir(dest_dir))
        
        # Verificar que se haya creado el directorio principal
        assert os.path.exists(os.path.join(dest_dir, "test_project"))
        # Verificar que se haya creado el archivo urls.py
        assert os.path.exists(os.path.join(dest_dir, "test_project", "urls.py"))
        # Verificar que se haya creado el archivo wsgi.py
        assert os.path.exists(os.path.join(dest_dir, "test_project", "wsgi.py"))
