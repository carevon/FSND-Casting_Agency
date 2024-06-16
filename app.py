from flask import Flask
from config import Config
from models import db
from auth import setup_auth
from flask_migrate import Migrate
from routes import routes
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)  # Initialize JWTManager
    setup_auth(app)
    app.register_blueprint(routes)

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
