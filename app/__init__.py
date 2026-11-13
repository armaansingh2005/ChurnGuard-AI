import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from config import BASE_DIR, get_config


app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    from app.models.database_models import User

    return db.session.get(User, int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    db.init_app(app)
    login_manager.init_app(app)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(BASE_DIR / "data" / "raw", exist_ok=True)
    os.makedirs(BASE_DIR / "data" / "processed", exist_ok=True)
    os.makedirs(BASE_DIR / "ml" / "model_artifacts", exist_ok=True)

    with app.app_context():
        from app.models.database_models import User, Customer, Prediction

        db.create_all()

        # Initialize a basic app state if no users exist.
        if not User.query.first():
            from werkzeug.security import generate_password_hash

            default_user = User(
                username="admin",
                email="admin@churnguard.ai",
                password_hash=generate_password_hash("admin123"),
            )
            db.session.add(default_user)
            db.session.commit()

        from app.routes.auth import auth_bp
        from app.routes.dashboard import dashboard_bp
        from app.routes.prediction import prediction_bp
        from app.routes.analytics import analytics_bp
        from app.routes.customers import customers_bp
        from app.routes.history import history_bp
        from app.routes.settings import settings_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(prediction_bp)
        app.register_blueprint(analytics_bp)
        app.register_blueprint(customers_bp)
        app.register_blueprint(history_bp)
        app.register_blueprint(settings_bp)

        model_path = BASE_DIR / "ml" / "model_artifacts" / "best_model.joblib"
        if not model_path.exists():
            from ml.train import train_and_save_models

            train_and_save_models()

    @app.route("/")
    def index():
        return render_template("login.html")

    return app
