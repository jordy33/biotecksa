from flask import Flask,url_for
from flask_restx import Api
from flask_mail import Mail
import os
mail = Mail()

def create_app():
    from bio_backend.users_namespace import users_namespace
    from bio_backend.cultivos_namespace import cultivos_namespace
    app = Flask(__name__)

    #Add this code to work behing haproxy
    # @property
    # def specs_url(self):
    #     return url_for(self.endpoint('specs'), _external=True, _scheme='https')
    #
    # Api.specs_url = specs_url

    ### End

    api = Api(app, version='0.1', title='Bioteksa Backend API',
              description='CRUD API')


    @app.route('/check')
    def check():
        return "UP"

    from bio_backend.db import db, db_config
    app.config['RESTX_MASK_SWAGGER'] = False
    app.config.update(db_config)
    mail.init_app(app)
    db.init_app(app)
    app.db = db

    api.add_namespace(users_namespace)
    api.add_namespace(cultivos_namespace)
    return app
