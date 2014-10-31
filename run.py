# -*- coding: utf-8 -*-
import os
from app import create_app
from flask.ext.script import Manager, Shell, Server
from app.mod_auth.views import User


app=create_app(os.environ.get('env_running_machine'))
manager = Manager(app)

def make_shell_context():
  return dict(app=app,user=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(host="0.0.0.0", port=8000))


if __name__ == '__main__':
    manager.run()
