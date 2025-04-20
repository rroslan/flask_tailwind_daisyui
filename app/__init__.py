from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models after db initialization to avoid circular imports
    from app import models
    
    # Register blueprints
    from app.routes import bp as main_bp
    from app.auth.routes import bp as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': models.User}

    return app

