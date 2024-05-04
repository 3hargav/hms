import time

from flask import Flask
from sqlalchemy.exc import OperationalError

from .models import db
from .views.department import department_bp
from .views.doctor import doc_bp
from .views.patient import patient_bp


def create_app():
    app = Flask(__name__)

    mysql_conn_str = "mysql://root:root@mysql_db:3306/hms"
    app.config["SQLALCHEMY_DATABASE_URI"] = mysql_conn_str

    db.init_app(app)

    def connect_to_database(retries=5, delay=5):
        attempt = 0
        connected = False

        while attempt < retries and not connected:
            try:
                db.create_all()
                connected = True
            except OperationalError:
                print("MySQL connection failed. Retrying in {} seconds...".format(delay))
                attempt += 1
                time.sleep(delay)

        if not connected:
            print("Failed to connect to MySQL after {} retries.".format(retries))

    with app.app_context():
        connect_to_database()

    app.register_blueprint(doc_bp, url_prefix='/api')
    app.register_blueprint(patient_bp, url_prefix='/api')
    app.register_blueprint(department_bp, url_prefix='/api')

    return app
