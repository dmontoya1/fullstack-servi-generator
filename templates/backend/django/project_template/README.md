# {{ project_slug|title }}

Proyecto Django generado con fullstack-servi-generator.

## Autor
{{ author }}

## Configuración Inicial

1. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
    ```

2.	Configura las variables de entorno copiando config/.env.template a .env y ajusta los valores.

3.	Aplica las migraciones:
    ```bash
    python manage.py migrate
    ```

4.	Ejecuta el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```

{% if drf %}

## Django REST Framework

Este proyecto incluye DRF configurado. Puedes crear endpoints de API en tus apps.
{% endif %}

{% if docker %}

## Uso con Docker

El proyecto incluye configuraciones Docker. Para construir y correr el contenedor:

```bash
docker-compose up --build
```

{% endif %}
