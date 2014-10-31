# -*- coding: UTF-8 -*-

import os
from flask import Blueprint, current_app
from flask.ext.principal import identity_loaded

static_folder=os.path.join(os.pardir, 'static')
mod_auth= Blueprint('auth',__name__,static_folder=static_folder)

from . import views
