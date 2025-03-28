import click
from .core.backend_generator import BackendGenerator
from .core.frontend_generator import FrontendGenerator
from .core.git_hooks import GitHooksManager
from .core.docker_config import DockerConfigGenerator
from .utils.config_loader import load_config
from .utils.validators import validate_project_name, validate_framework

@click.command()
@click.option('--project-name', 
              prompt='Nombre del proyecto', 
              callback=validate_project_name,
              help='Nombre para el nuevo proyecto')
@click.option('--backend-framework', 
              type=click.Choice(['django', 'flask', 'fastapi']), 
              prompt='Framework de backend',
              callback=validate_framework,
              help='Framework para el backend')
@click.option('--frontend-framework', 
              type=click.Choice(['vue', 'react', 'angular']), 
              prompt='Framework de frontend',
              callback=validate_framework,
              help='Framework para el frontend')
@click.option('--output-dir', 
              default='.', 
              help='Directorio de salida para el proyecto')
def main(project_name, backend_framework, frontend_framework, output_dir):
    """
    Genera un proyecto FullStack con la estructura y configuraciones predefinidas
    """
    # Cargar configuración
    config = load_config()
    
    # Generar proyecto
    try:
        # Backend
        backend_gen = BackendGenerator(config)
        backend_path = backend_gen.generate(
            project_name, 
            backend_framework, 
            output_dir
        )
        
        # Frontend
        frontend_gen = FrontendGenerator(config)
        frontend_path = frontend_gen.generate(
            project_name, 
            frontend_framework, 
            output_dir
        )
        
        # Git Hooks
        git_hooks_manager = GitHooksManager()
        git_hooks_manager.setup_hooks(output_dir)
        
        # Docker Configuration
        docker_config_gen = DockerConfigGenerator()
        docker_config_gen.generate(
            project_name, 
            backend_framework, 
            frontend_framework, 
            output_dir
        )
        
        click.echo(click.style(
            f"✅ Proyecto {project_name} generado exitosamente!", 
            fg='green'
        ))
        click.echo(f"Backend: {backend_path}")
        click.echo(f"Frontend: {frontend_path}")
    
    except Exception as e:
        click.echo(click.style(
            f"❌ Error al generar el proyecto: {str(e)}", 
            fg='red'
        ))

if __name__ == '__main__':
    main()