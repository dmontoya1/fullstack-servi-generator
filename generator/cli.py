# generator/cli.py

import os
import re
import subprocess
import typer
import logging
import questionary  # Para selección interactiva con flechas
from generator.templates_manager import render_template
from generator.hooks import install_git_hooks, initialize_git_repo
from generator.logger import get_logger

app = typer.Typer(invoke_without_command=True, help="Generador de proyectos FullStack con backend y frontend.")
logger = get_logger(__name__)


def valid_slug(slug: str) -> bool:
    pattern = r"^[a-z0-9_]+$"
    return re.match(pattern, slug) is not None


@app.callback()
def main(ctx: typer.Context):
    # Si no se invoca ningún subcomando, entra en modo interactivo
    if ctx.invoked_subcommand is None:
        banner = r"""
  /$$$$$$  /$$$$$$$$ /$$$$$$$  /$$    /$$ /$$$$$$       /$$$$$$$$ /$$$$$$ 
 /$$__  $$| $$_____/| $$__  $$| $$   | $$|_  $$_/      | $$_____//$$__  $$
| $$  \__/| $$      | $$  \ $$| $$   | $$  | $$        | $$     | $$  \__/
|  $$$$$$ | $$$$$   | $$$$$$$/|  $$ / $$/  | $$        | $$$$$  |  $$$$$$ 
 \____  $$| $$__/   | $$__  $$ \  $$ $$/   | $$        | $$__/   \____  $$
 /$$  \ $$| $$      | $$  \ $$  \  $$$/    | $$        | $$      /$$  \ $$
|  $$$$$$/| $$$$$$$$| $$  | $$   \  $/    /$$$$$$      | $$     |  $$$$$$/
 \______/ |________/|__/  |__/    \_/    |______/      |__/      \______/ 
"""
        typer.echo(banner)
        typer.echo("Bienvenido a Full Stack Servi interactivo, te ayudaremos a crear tu proyecto.")

        project_scope = questionary.select(
            "¿Qué tipo de proyecto deseas crear?",
            choices=["back", "front", "fullstack"]
        ).ask()

        if project_scope == "back":
            backend_framework = questionary.select(
                "¿Qué framework de backend?",
                choices=["django", "flask", "fastapi"]
            ).ask()

            if backend_framework == "django":
                slug = questionary.text("Ingresa el slug del proyecto (ej: mi_proyecto)").ask()
                if not valid_slug(slug):
                    typer.echo("Error: El slug debe contener solo letras minúsculas, números y guiones bajos.")
                    raise typer.Exit(code=1)
                author = questionary.text("Ingresa el autor del proyecto", default="Autor Desconocido").ask()
                docker = questionary.confirm("¿Incluir configuración Docker?", default=False).ask()
                drf = questionary.confirm("¿Incluir Django REST Framework?", default=False).ask()
                db_type = questionary.select(
                    "Selecciona la base de datos para Django",
                    choices=["sqlite", "postgres", "mysql"]
                ).ask()
                from generator.cli import create_django
                create_django(project_slug=slug, author=author, docker=docker, drf=drf, db_type=db_type)
            elif backend_framework in ["flask", "fastapi"]:
                slug = questionary.text("Ingresa el slug del proyecto (ej: mi_proyecto)").ask()
                if not valid_slug(slug):
                    typer.echo("Error: El slug debe contener solo letras minúsculas, números y guiones bajos.")
                    raise typer.Exit(code=1)
                author = questionary.text("Ingresa el autor del proyecto", default="Autor Desconocido").ask()
                docker = questionary.confirm("¿Incluir configuración Docker?", default=False).ask()
                if backend_framework == "flask":
                    from generator.cli import create_flask
                    create_flask(project_slug=slug, author=author, docker=docker)
                else:
                    typer.echo("FastAPI aún no está implementado. Prueba con Django o Flask.")
            else:
                typer.echo("Framework de backend no reconocido.")

        elif project_scope == "front":
            frontend_framework = questionary.select(
                "¿Qué framework de frontend?",
                choices=["react", "vue", "angular"]
            ).ask()
            project_name = questionary.text("Ingresa el nombre del proyecto").ask()
            author = questionary.text("Ingresa el autor del proyecto", default="Autor Desconocido").ask()
            from generator.cli import create
            create(project_type="frontend", framework=frontend_framework, project_name=project_name, author=author)

        elif project_scope == "fullstack":
            # Para fullstack se pide backend y frontend
            backend_framework = questionary.select(
                "¿Qué framework de backend?",
                choices=["django", "flask", "fastapi"]
            ).ask()
            frontend_framework = questionary.select(
                "¿Qué framework de frontend?",
                choices=["react", "vue", "angular"]
            ).ask()
            backend_slug = questionary.text("Ingresa el slug del proyecto de backend").ask()
            if not valid_slug(backend_slug):
                typer.echo("Error: El slug debe contener solo letras minúsculas, números y guiones bajos.")
                raise typer.Exit(code=1)
            frontend_name = questionary.text("Ingresa el nombre del proyecto de frontend").ask()
            author = questionary.text("Ingresa el autor del proyecto", default="Autor Desconocido").ask()
            # Crear backend
            if backend_framework == "django":
                docker_back = questionary.confirm("¿Incluir configuración Docker en backend?", default=False).ask()
                drf = questionary.confirm("¿Incluir Django REST Framework en backend?", default=False).ask()
                db_type = questionary.select(
                    "Selecciona la base de datos para Django",
                    choices=["sqlite", "postgres", "mysql"]
                ).ask()
                from generator.cli import create_django
                create_django(project_slug=backend_slug, author=author, docker=docker_back, drf=drf, db_type=db_type)
            elif backend_framework in ["flask", "fastapi"]:
                docker_back = questionary.confirm("¿Incluir configuración Docker en backend?", default=False).ask()
                if backend_framework == "flask":
                    from generator.cli import create_flask
                    create_flask(project_slug=backend_slug, author=author, docker=docker_back)
                else:
                    typer.echo("FastAPI aún no está implementado para backend.")
            else:
                typer.echo("Framework de backend no reconocido.")
            # Crear frontend
            from generator.cli import create
            create(project_type="frontend", framework=frontend_framework, project_name=frontend_name, author=author)
        else:
            typer.echo("Opción no reconocida. Elige: back, front o fullstack.")


@app.command("create-django")
def create_django(
    project_slug: str = typer.Option(..., "--slug", "-s", help="Nombre del proyecto (slug: minúsculas, sin espacios, usa guiones bajos)"),
    author: str = typer.Option("Autor Desconocido", "--author", "-a", help="Nombre del autor del proyecto"),
    docker: bool = typer.Option(False, "--docker", help="Incluir configuración Docker en el proyecto"),
    drf: bool = typer.Option(False, "--drf", help="Incluir Django REST Framework en el proyecto"),
    db_type: str = typer.Option("sqlite", "--db", "-d", help="Tipo de base de datos (sqlite, postgres, mysql)")
):
    """
    Genera un proyecto Django completo.
    """
    logger.info("Iniciando generación del proyecto Django.")
    if not valid_slug(project_slug):
        typer.echo("Error: El slug del proyecto debe contener solo letras minúsculas, números y guiones bajos, sin espacios.")
        logger.error("Slug inválido: %s", project_slug)
        raise typer.Exit(code=1)

    context = {
        "project_slug": project_slug,
        "author": author,
        "docker": docker,
        "drf": drf,
        "db_type": db_type
    }
    template_path = os.path.join("templates", "backend", "django", "project_template")
    destination_path = os.path.join(os.getcwd(), project_slug)

    if not os.path.exists(template_path):
        typer.echo(f"Error: No se encontró la plantilla en: {template_path}")
        logger.error("Plantilla no encontrada: %s", template_path)
        raise typer.Exit(code=1)
    if os.path.exists(destination_path):
        typer.echo(f"Error: La carpeta {destination_path} ya existe.")
        logger.error("Carpeta destino ya existe: %s", destination_path)
        raise typer.Exit(code=1)

    try:
        render_template(template_path, destination_path, context)
        typer.echo(f"Proyecto Django '{project_slug}' generado exitosamente en {destination_path}.")
        logger.info("Proyecto generado exitosamente en %s", destination_path)
    except Exception as e:
        typer.echo("Error al renderizar la plantilla: " + str(e))
        logger.exception("Error al renderizar la plantilla")
        raise typer.Exit(code=1)

    if docker:
        docker_template_path = os.path.join(template_path, "docker")
        if os.path.exists(docker_template_path):
            try:
                render_template(docker_template_path, os.path.join(destination_path, "docker"), context)
                typer.echo("Configuración Docker incluida.")
                logger.info("Docker configurado correctamente.")
            except Exception as e:
                typer.echo("Error al incluir Docker: " + str(e))
                logger.exception("Error al incluir configuración Docker")
        else:
            typer.echo("Advertencia: No se encontró la plantilla de Docker.")
            logger.warning("Plantilla de Docker no encontrada en %s", docker_template_path)

    try:
        initialize_git_repo(destination_path)
        typer.echo("Repositorio Git inicializado.")
        logger.info("Repositorio Git inicializado en %s", destination_path)
    except Exception as e:
        typer.echo("Error al inicializar el repositorio Git: " + str(e))
        logger.exception("Error al inicializar Git repo")

    try:
        install_git_hooks(destination_path)
        typer.echo("Git hooks instalados (si se configuraron).")
        logger.info("Git hooks instalados en %s", destination_path)
    except Exception as e:
        typer.echo("Error al instalar git hooks: " + str(e))
        logger.exception("Error al instalar git hooks")
        raise typer.Exit(code=1)


@app.command("create-flask")
def create_flask(
    project_slug: str = typer.Option(..., "--slug", "-s", help="Nombre del proyecto (slug: minúsculas, sin espacios, usa guiones bajos)"),
    author: str = typer.Option("Autor Desconocido", "--author", "-a", help="Nombre del autor del proyecto"),
    docker: bool = typer.Option(False, "--docker", help="Incluir configuración Docker en el proyecto")
):
    """
    Genera un proyecto Flask completo.
    """
    logger.info("Iniciando generación del proyecto Flask.")
    if not valid_slug(project_slug):
        typer.echo("Error: El slug del proyecto debe contener solo letras minúsculas, números y guiones bajos, sin espacios.")
        logger.error("Slug inválido: %s", project_slug)
        raise typer.Exit(code=1)

    context = {"project_slug": project_slug, "author": author, "docker": docker}
    template_path = os.path.join("templates", "backend", "flask", "project_template")
    destination_path = os.path.join(os.getcwd(), project_slug)

    if not os.path.exists(template_path):
        typer.echo(f"Error: No se encontró la plantilla en: {template_path}")
        logger.error("Plantilla no encontrada: %s", template_path)
        raise typer.Exit(code=1)
    if os.path.exists(destination_path):
        typer.echo(f"Error: La carpeta {destination_path} ya existe.")
        logger.error("Carpeta destino ya existe: %s", destination_path)
        raise typer.Exit(code=1)

    try:
        render_template(template_path, destination_path, context)
        typer.echo(f"Proyecto Flask '{project_slug}' generado exitosamente en {destination_path}.")
        logger.info("Proyecto generado exitosamente en %s", destination_path)
    except Exception as e:
        typer.echo("Error al renderizar la plantilla: " + str(e))
        logger.exception("Error al renderizar la plantilla")
        raise typer.Exit(code=1)

    if docker:
        docker_template_path = os.path.join(template_path, "docker")
        if os.path.exists(docker_template_path):
            try:
                render_template(docker_template_path, os.path.join(destination_path, "docker"), context)
                typer.echo("Configuración Docker incluida.")
                logger.info("Docker configurado correctamente.")
            except Exception as e:
                typer.echo("Error al incluir Docker: " + str(e))
                logger.exception("Error al incluir configuración Docker")
        else:
            typer.echo("Advertencia: No se encontró la plantilla de Docker.")
            logger.warning("Plantilla de Docker no encontrada en %s", docker_template_path)

    try:
        initialize_git_repo(destination_path)
        typer.echo("Repositorio Git inicializado.")
        logger.info("Repositorio Git inicializado en %s", destination_path)
    except Exception as e:
        typer.echo("Error al inicializar el repositorio Git: " + str(e))
        logger.exception("Error al inicializar Git repo")

    try:
        install_git_hooks(destination_path)
        typer.echo("Git hooks instalados (si se configuraron).")
        logger.info("Git hooks instalados en %s", destination_path)
    except Exception as e:
        typer.echo("Error al instalar git hooks: " + str(e))
        logger.exception("Error al instalar git hooks")
        raise typer.Exit(code=1)


@app.command("create")
def create(
    project_type: str = typer.Option(..., "--type", "-t", help="Tipo de proyecto: 'backend' o 'frontend'"),
    framework: str = typer.Option(..., "--framework", "-f", help="Framework (ej. django, flask, react, vue, angular)"),
    project_name: str = typer.Option(..., "--name", "-n", help="Nombre del proyecto a generar"),
    author: str = typer.Option("Autor Desconocido", "--author", "-a", help="Nombre del autor del proyecto")
):
    """
    Genera un proyecto basado en las plantillas predefinidas para backend o frontend.
    """
    logger.info("Generando proyecto genérico: %s (%s - %s)", project_name, project_type, framework)
    template_path = os.path.join("templates", project_type, framework, "project_template")
    destination_path = os.path.join(os.getcwd(), project_name)

    if not os.path.exists(template_path):
        typer.echo(f"Error: No se encontró la plantilla en: {template_path}")
        logger.error("Plantilla no encontrada: %s", template_path)
        raise typer.Exit(code=1)

    if os.path.exists(destination_path):
        typer.echo(f"Error: La carpeta {destination_path} ya existe.")
        logger.error("Carpeta destino ya existe: %s", destination_path)
        raise typer.Exit(code=1)

    context = {"project_name": project_name, "author": author}

    try:
        render_template(template_path, destination_path, context)
        typer.echo(f"Proyecto '{project_name}' generado exitosamente en {destination_path}.")
        logger.info("Proyecto generado exitosamente en %s", destination_path)
    except Exception as e:
        typer.echo("Error al renderizar la plantilla: " + str(e))
        logger.exception("Error al renderizar la plantilla")
        raise typer.Exit(code=1)

    try:
        install_git_hooks(destination_path)
        typer.echo("Git hooks instalados (si se configuraron).")
        logger.info("Git hooks instalados en %s", destination_path)
    except Exception as e:
        typer.echo("Error al instalar git hooks: " + str(e))
        logger.exception("Error al instalar git hooks")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
