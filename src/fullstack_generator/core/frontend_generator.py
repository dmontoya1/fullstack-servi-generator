import os
import subprocess
from typing import Dict, Any

class FrontendGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.templates_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'templates', 
            'frontend'
        )
    
    def generate(self, project_name: str, framework: str, output_dir: str) -> str:
        """
        Genera la estructura de frontend para un framework específico
        
        :param project_name: Nombre del proyecto
        :param framework: Framework de frontend a utilizar
        :param output_dir: Directorio de salida
        :return: Ruta al directorio de frontend generado
        """
        # Validar framework
        supported_frameworks = ['vue', 'react', 'angular']
        if framework not in supported_frameworks:
            raise ValueError(f"Framework {framework} no soportado")
        
        # Crear directorios
        frontend_path = os.path.join(output_dir, project_name, 'frontend')
        os.makedirs(frontend_path, exist_ok=True)
        
        # Generar estructura según framework
        generator_method = getattr(self, f'_generate_{framework}')
        generator_method(project_name, frontend_path)
        
        return frontend_path
    
    def _generate_vue(self, project_name: str, frontend_path: str):
        """Generar estructura para proyecto Vue"""
        # Crear directorios base
        os.makedirs(os.path.join(frontend_path, 'src', 'components'), exist_ok=True)
        os.makedirs(os.path.join(frontend_path, 'src', 'views'), exist_ok=True)
        os.makedirs(os.path.join(frontend_path, 'src', 'services'), exist_ok=True)
        os.makedirs(os.path.join(frontend_path, 'src', 'store'), exist_ok=True)
        
        # Crear package.json básico
        package_json = {
            "name": project_name,
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "serve": "vue-cli-service serve",
                "build": "vue-cli-service build",
                "lint": "vue-cli-service lint"
            },
            "dependencies": {
                "vue": "^3.2.13",
                "vue-router": "^4.0.12",
                "vuex": "^4.0.2"
            },
            "devDependencies": {
                "@vue/cli-plugin-babel": "~4.5.0",
                "@vue/cli-plugin-eslint": "~4.5.0",
                "@vue/cli-service": "~4.5.0"
            }
        }
        
        import json
        with open(os.path.join(frontend_path, 'package.json'), 'w') as f:
            json.dump(package_json, f, indent=2)
    
    def _generate_react(self, project_name: str, frontend_path: str):
        """Generar estructura para proyecto React"""
        # Crear directorios base
        os.makedirs(os.path.join(frontend_path, 'src', 'components'), exist_ok=True)
        os.makedirs(os.path.join(frontend_path, 'src', 'pages'), exist_ok=True)
        os.makedirs(os.path.join(frontend_path, 'src', 'services'), exist_ok=True)
        os.makedirs(os.path.join(frontend_path, 'src', 'context'), exist_ok=True)
        
        # Crear package.json básico
        package_json = {
            "name": project_name,
            "version": "0.1.0",
            "private": True,
            "dependencies": {
                "react": "^17.0.2",
                "react-dom": "^17.0.2",
                "react-router-dom": "^6.2.1",
                "axios": "^0.24.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            }
        }
        
        import json
        with open(os.path.join(frontend_path, 'package.json'), 'w') as f:
            json.dump(package_json, f, indent=2)
    
    def _generate_angular(self, project_name: str, frontend_path: str):
        """Generar estructura para proyecto Angular"""
        # Crear directorios base
        os.makedirs(os.path.join(frontend_path, 'src', 'app', 'components'), exist_ok=True)
        os.makedirs(os.path.join(frontend_path, 'src', 'app', 'services'), exist_ok=True)
        os.makedirs(os.path.join(frontend_path, 'src', 'app', 'models'), exist_ok=True)
        
        # Crear package.json básico
        package_json = {
            "name": project_name,
            "version": "0.1.0",
            "scripts": {
                "ng": "ng",
                "start": "ng serve",
                "build": "ng build",
                "test": "ng test"
            },
            "dependencies": {
                "@angular/core": "^13.1.0",
                "@angular/forms": "^13.1.0",
                "@angular/router": "^13.1.0",
                "rxjs": "~7.4.0"
            },
            "devDependencies": {
                "@angular/cli": "^13.1.0",
                "@angular/compiler": "^13.1.0"
            }
        }
        
        import json
        with open(os.path.join(frontend_path, 'package.json'), 'w') as f:
            json.dump(package_json, f, indent=2)
