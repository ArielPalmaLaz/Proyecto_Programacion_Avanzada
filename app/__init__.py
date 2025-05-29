from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  
login_manager.login_message_category = 'warning'

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/videogamesStorage'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'password123'  

    db.init_app(app)
    login_manager.init_app(app)
    
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Importar y registrar rutas
    from app import models  # Asegura que se carguen los modelos
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
