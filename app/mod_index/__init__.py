# -*- coding: UTF-8 -*-

import os
from flask import Blueprint

static_folder=os.path.join(os.pardir, 'static')
mod_index= Blueprint('index',__name__,static_folder=static_folder)

from . import views
