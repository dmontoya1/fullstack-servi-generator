import os
import pytest
import shutil
from fullstack_generator.core.backend_generator import BackendGenerator

@pytest.fixture
def config():
    return {}  # Configuración de prueba

@pytest.fixture
def temp_output_dir(tmpdir):
    return str(tmpdir)

def test_backend_generator_django(config, temp_output_dir):
    generator = BackendGenerator(config)
    project_name = "test_django_project"
    
    backend_path = generator.generate(project_name, 'django', temp_output_dir)
    
    # Verificar que se crearon directorios
    assert os.path.exists(backend_path)
    assert os.path.exists(os.path.join(backend_path, 'manage.py'))
    assert os.path.exists(os.path.join(backend_path, 'apps'))
    assert os.path.exists(os.path.join(backend_path, 'tests'))
    assert os.path.exists(os.path.join(backend_path, 'requirements.txt'))

def test_backend_generator_flask(config, temp_output_dir):
    generator = BackendGenerator(config)
    project_name = "test_flask_project"
    
    backend_path = generator.generate(project_name, 'flask', temp_output_dir)
    
    # Verificar que se crearon directorios
    assert os.path.exists(backend_path)
    assert os.path.exists(os.path.join(backend_path, 'app', '__init__.py'))
    assert os.path.exists(os.path.join(backend_path, 'tests'))
    assert os.path.exists(os.path.join(backend_path, 'requirements.txt'))

def test_backend_generator_fastapi(config, temp_output_dir):
    generator = BackendGenerator(config)
    project_name = "test_fastapi_project"
    
    backend_path = generator.generate(project_name, 'fastapi', temp_output_dir)
    
    # Verificar que se crearon directorios
    assert os.path.exists(backend_path)
    assert os.path.exists(os.path.join(backend_path, 'app', 'main.py'))
    assert os.path.exists(os.path.join(backend_path, 'tests'))
    assert os.path.exists(os.path.join(backend_path, 'requirements.txt'))

def test_backend_generator_invalid_framework(config, temp_output_dir):
    generator = BackendGenerator(config)
    project_name = "test_invalid_project"
    
    with pytest.raises(ValueError):
        generator.generate(project_name, 'invalid_framework', temp_output_dir)