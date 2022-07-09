from flask import Flask
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from lchs.settings import getSetting

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "TestingSecretKey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://lchs_user:password@127.0.0.1/lchs"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.config["CONTENT_FOLDER"] = getSetting('contentFolder')

    app.view_functions["static"] = login_required(app.send_static_file)

    from .auth import routes as auth_routes

    app.register_blueprint(auth_routes.auth, url_prefix="/auth")

    from .main import routes as main_routes

    app.register_blueprint(main_routes.main, url_prefix="/")

    return app
