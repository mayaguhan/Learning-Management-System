from flask import Flask
from flasgger import Swagger
from api.route.home import home_api
from flask_sqlalchemy import SQLAlchemy
import os

def create_app():
    app = Flask(__name__)

    app.config['SPM Backend'] = {
        'title': 'SPM Backend',
    }


    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + os.getenv("username") + ":" + os.getenv("password") + "@" + os.getenv("hostname") + "/" + "lms"
    db = SQLAlchemy(app)

    swagger = Swagger(app)
     ## Initialize Config
    app.config.from_pyfile('config.py')
    app.register_blueprint(home_api, url_prefix='/api')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
