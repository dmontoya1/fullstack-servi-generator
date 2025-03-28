from flask import Flask
from .extensions import db
from .blueprints import main_bp


def create_app():
    app = Flask(__name__)

    # Configuración básica (puedes mejorarla, por ejemplo, cargando variables de entorno)
    app.config.from_pyfile('config.py', silent=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(main_bp)

    return app