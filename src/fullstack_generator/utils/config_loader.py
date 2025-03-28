import os
import yaml
from typing import Dict, Any

def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Cargar configuración desde un archivo YAML
    
    :param config_path: Ruta al archivo de configuración
    :return: Diccionario con configuraciones
    """
    # Ruta por defecto si no se proporciona
    if config_path is None:
        config_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'config.yaml'
        )
    
    # Configuración por defecto
    default_config = {
        'backend_frameworks': ['django', 'flask', 'fastapi'],
        'frontend_frameworks': ['vue', 'react', 'angular'],
        'default_python_version': '3.9',
        'default_node_version': '14'
    }
    
    # Si el archivo no existe, devolver configuración por defecto
    if not os.path.exists(config_path):
        return default_config
    
    # Cargar configuración desde YAML
    try:
        with open(config_path, 'r') as file:
            user_config = yaml.safe_load(file)
        
        # Combinar configuración por defecto con configuración de usuario
        return {**default_config, **user_config}
    
    except (IOError, yaml.YAMLError) as e:
        print(f"Error al cargar configuración: {e}")
        return default_config
