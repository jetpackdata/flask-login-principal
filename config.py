# -*- coding: UTF-8 -*-

import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY='\xc4\x92n\x15g\xb0\xa7\x00\x00\xa1\xe1\x91C0\xbe\xf4\xfe\xb8\xaf\x81\x10b\xe3\xcf'
  DEBUG = True

  @staticmethod
  def init_app(app):
    pass

class TestingConfig(Config):
  TESTING = False

class ProductionConfig(Config):
  pass

config = {
  'testing' : TestingConfig,
  'production': ProductionConfig
}
