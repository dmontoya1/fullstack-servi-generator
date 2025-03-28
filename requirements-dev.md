# Requisitos para Desarrollo

## Dependencias de Desarrollo
- pytest
- pytest-cov
- flake8
- black
- mypy
- coverage

## Comandos Útiles
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar pruebas
pytest tests/

# Verificar cobertura de código
pytest --cov=src tests/

# Formatear código
black .

# Verificar tipos
mypy src/
```
