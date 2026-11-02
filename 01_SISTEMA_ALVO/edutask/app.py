import os
from flask import Flask
from .models import init_db, seed_initial_data
from .routes import auth_bp, discipline_bp, task_bp, api_bp, main_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'unisagrado-tqs-p2-secret-2026'),
        DATABASE=os.path.join(app.instance_path, 'edutask.db')
    )

    if test_config is not None:
        app.config.update(test_config)

    # Inicializa banco de dados e dados padrão
    init_db()
    seed_initial_data()

    # Registra Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(discipline_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
