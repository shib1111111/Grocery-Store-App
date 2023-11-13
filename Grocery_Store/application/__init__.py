from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cf559170bf7a85a6f3f7e4dcfdb5bc11'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

    db.init_app(app)
    # Push the app context
    app.app_context().push()
  

    # Import and register the views blueprint
    from .user_views import user_views
    app.register_blueprint(user_views,url_prefix="/")

    from .admin_views import admin_views
    app.register_blueprint(admin_views,url_prefix="/")

    # Import and register the authentication blueprint
    from .authentication import authentication
    app.register_blueprint(authentication,url_prefix="/")

    from .models import  User, Category, Product, Cart,CartItem,Order,OrderItem
    create_database()
    
    login_manager = LoginManager(app)

  

    # Initialize the LoginManager
    login_manager = LoginManager()
    login_manager.login_view = "authentication.login"
    login_manager.init_app(app)
    
  # Login Manager Configuration
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    return app

def create_database():
    if not path.exists("applicaton/"+"todos.db"):
        db.create_all()
        print("Created database!")