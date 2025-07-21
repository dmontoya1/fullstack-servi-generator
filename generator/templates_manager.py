# generator/templates_manager.py

import os
import shutil
import logging
import re

logger = logging.getLogger(__name__)


_VAR_PATTERN = re.compile(r"{{\s*(\w+)(?:\|(\w+))?\s*}}")


def _render_string(value: str, context: dict) -> str:
    """Reemplaza expresiones simples de Jinja como ``{{ variable }}``."""

    def replacer(match: re.Match) -> str:
        key = match.group(1)
        flt = match.group(2)
        result = str(context.get(key, ""))
        if flt == "title":
            result = result.title()
        return result

    return _VAR_PATTERN.sub(replacer, value)


def render_template(template_dir: str, destination_dir: str, context: dict):
    """Copia ``template_dir`` a ``destination_dir`` aplicando reemplazos simples."""

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)
        logger.debug("Carpeta creada: %s", destination_dir)

    for item in os.listdir(template_dir):
        src_item = os.path.join(template_dir, item)
        rendered_name = _render_string(item, context)
        dest_item = os.path.join(destination_dir, rendered_name)

        if os.path.isdir(src_item):
            render_template(src_item, dest_item, context)
        else:
            try:
                with open(src_item, "r", encoding="utf-8") as f:
                    content = f.read()
                rendered_content = _render_string(content, context)
                os.makedirs(os.path.dirname(dest_item), exist_ok=True)
                with open(dest_item, "w", encoding="utf-8") as f:
                    f.write(rendered_content)
                logger.debug("Archivo renderizado: %s", dest_item)
            except UnicodeDecodeError:
                shutil.copy2(src_item, dest_item)
                logger.debug("Archivo copiado: %s", dest_item)
