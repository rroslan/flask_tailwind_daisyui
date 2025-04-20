from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Explicit development mode settings
    app.config['ENV'] = 'development' if app.debug else 'production'
    if app.debug:
        app.config.update(
            DEBUG=True,
            TESTING=True
        )
        print(f"\n=== Running in DEVELOPMENT mode (DEBUG={app.debug}) ===\n")

    # Configure session
    app.config.update(
        SESSION_COOKIE_SECURE=not app.debug,  # Secure only in production
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=timedelta(days=7)
    )

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.auth'
    login_manager.session_protection = "strong"
    
    # Import models after db initialization to avoid circular imports
    # Import models after db initialization to avoid circular imports
    from app import models
    
    # Set up user loader
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import bp as main_bp
    from app.auth.routes import bp as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': models.User}

    return app

