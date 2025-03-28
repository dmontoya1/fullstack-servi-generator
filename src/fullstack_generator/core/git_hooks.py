import os
import stat

class GitHooksManager:
    def __init__(self):
        pass
    
    def setup_hooks(self, project_path: str):
        """
        Configurar hooks de Git básicos
        
        :param project_path: Ruta al directorio raíz del proyecto
        """
        # Crear directorio de hooks si no existe
        git_hooks_dir = os.path.join(project_path, '.git', 'hooks')
        os.makedirs(git_hooks_dir, exist_ok=True)
        
        # Pre-commit hook
        pre_commit_path = os.path.join(git_hooks_dir, 'pre-commit')
        with open(pre_commit_path, 'w') as f:
            f.write('''#!/bin/sh
# Ejecutar linters y verificaciones básicas antes de commit

# Verificar formato con black
black --check .

# Verificar importaciones con isort
isort --check-only .

# Ejecutar tests
pytest tests/

# Si cualquier comando falla, rechazar el commit
exit $?
''')
        
        # Hacer el hook ejecutable
        st = os.stat(pre_commit_path)
        os.chmod(pre_commit_path, st.st_mode | stat.S_IEXEC)
