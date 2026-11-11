from .auth_routes import auth_bp
from .discipline_routes import discipline_bp
from .task_routes import task_bp
from .api_routes import api_bp
from .main_routes import main_bp

__all__ = ['auth_bp', 'discipline_bp', 'task_bp', 'api_bp', 'main_bp']
