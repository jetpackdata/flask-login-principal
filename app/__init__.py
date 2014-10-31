# -*- coding: UTF-8 -*-

import os
from flask import Flask
from config import config
from flask.ext.login import LoginManager
from flask.ext.principal import Principal


login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
login_manager.login_message = u"You need to login to see this page"

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  login_manager.init_app(app)

  Principal(app)

  from .mod_auth import mod_auth as auth_blueprint
  app.register_blueprint(auth_blueprint,url_prefix='/auth')

  from .mod_index import mod_index as index_blueprint
  app.register_blueprint(index_blueprint)

  return app
