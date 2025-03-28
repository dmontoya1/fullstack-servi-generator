import re
import click

def validate_project_name(ctx, param, value):
    """
    Validar que el nombre del proyecto sea válido
    
    :param ctx: Contexto de click
    :param param: Parámetro
    :param value: Valor a validar
    :return: Nombre del proyecto validado
    """
    if not value:
        raise click.BadParameter("El nombre del proyecto no puede estar vacío")
    
    # Debe comenzar con letra, solo contener letras, números o guiones bajos
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', value):
        raise click.BadParameter(
            "El nombre del proyecto debe comenzar con una letra y "
            "contener solo letras, números, guiones o guiones bajos"
        )
    
    return value

def validate_framework(ctx, param, value):
    """
    Validar que el framework sea válido
    
    :param ctx: Contexto de click
    :param param: Parámetro
    :param value: Framework a validar
    :return: Framework validado
    """
    if not value:
        raise click.BadParameter("Debe seleccionar un framework")
    
    # Puedes agregar más validaciones específicas si lo deseas
    return value
