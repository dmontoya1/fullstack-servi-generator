# generator/templates_manager.py

import os
import shutil
import logging
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


def render_template(template_dir: str, destination_dir: str, context: dict):
    """
    Copia y renderiza recursivamente la plantilla de 'template_dir' a 'destination_dir'
    usando el contexto. Renderiza tanto el contenido de los archivos como los nombres de
    directorios y archivos utilizando Jinja2.
    """
    # Crear una instancia de Jinja2 para renderizar nombres (usaremos un loader de string)
    env = Environment(loader=FileSystemLoader(template_dir), keep_trailing_newline=True)

    # Asegurarse de que exista el directorio destino
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        logger.debug("Carpeta creada: %s", destination_dir)

    # Listar todos los elementos en el directorio de la plantilla
    for item in os.listdir(template_dir):
        src_item = os.path.join(template_dir, item)
        # Renderizar el nombre del elemento (archivo o carpeta)
        rendered_item = env.from_string(item).render(**context)
        dest_item = os.path.join(destination_dir, rendered_item)

        if os.path.isdir(src_item):
            # Si es un directorio, crearlo en el destino y procesar recursivamente
            if not os.path.exists(dest_item):
                os.makedirs(dest_item)
                logger.debug("Carpeta creada: %s", dest_item)
            # Llamada recursiva: usar el mismo contexto
            render_template(src_item, dest_item, context)
        else:
            # Si es un archivo, determinar si se debe renderizar (archivo de texto) o copiar directamente
            if item.endswith(('.py', '.md', '.txt', '.json', '.yml', '.yaml', '.js', '.html', '.css')):
                # Leer el contenido original
                with open(src_item, "r", encoding="utf-8") as f:
                    content = f.read()
                # Renderizar el contenido usando Jinja2
                template_content = env.from_string(content)
                rendered_content = template_content.render(**context)
                with open(dest_item, "w", encoding="utf-8") as f:
                    f.write(rendered_content)
                logger.debug("Archivo renderizado: %s", dest_item)
            else:
                # Si es binario o no se desea renderizar, se copia tal cual
                shutil.copy2(src_item, dest_item)
                logger.debug("Archivo copiado: %s", dest_item)
