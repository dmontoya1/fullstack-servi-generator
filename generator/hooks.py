# generator/hooks.py

import os
import shutil
import subprocess
import logging

logger = logging.getLogger(__name__)

def install_git_hooks(project_path: str):
    """
    Copia el archivo de configuración de pre-commit y ejecuta 'pre-commit install' si es posible.
    """
    hooks_config_source = os.path.join("templates", "git_hooks", "pre-commit-config.yaml")
    hooks_config_dest = os.path.join(project_path, ".pre-commit-config.yaml")
    
    if os.path.exists(hooks_config_source):
        shutil.copy2(hooks_config_source, hooks_config_dest)
        logger.debug("Archivo pre-commit-config.yaml copiado a %s", hooks_config_dest)
    else:
        logger.warning("No se encontró pre-commit-config.yaml en %s", hooks_config_source)
    
    # Ejecutar pre-commit install si pre-commit está instalado
    try:
        subprocess.run(["pre-commit", "install"], cwd=project_path, check=True)
        logger.debug("pre-commit instalado en %s", project_path)
    except Exception as e:
        logger.exception("No se pudo instalar pre-commit: %s", e)

def initialize_git_repo(project_path: str):
    """
    Inicializa un repositorio Git en 'project_path' si aún no existe.
    """
    if not os.path.exists(os.path.join(project_path, ".git")):
        try:
            subprocess.run(["git", "init"], cwd=project_path, check=True)
            logger.debug("Repositorio Git inicializado en %s", project_path)
        except Exception as e:
            logger.exception("Error al inicializar el repositorio Git: %s", e)
            raise e
