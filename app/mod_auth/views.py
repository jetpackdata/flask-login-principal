from flask import g, Flask, flash, redirect, url_for, request, get_flashed_messages, current_app, session, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from . import mod_auth
from .. import login_manager
from flask.ext.principal import Principal, Identity, Permission, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed, UserNeed, ActionNeed

@login_manager.user_loader
def load_user(id):
    return User.get(id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Login first son')
    return redirect(url_for('.login'))

class UserNotFoundError(Exception):
    pass

# Needs
be_admin = RoleNeed('admin')
be_editor = RoleNeed('editor')
to_sign_in = ActionNeed('sign in')

# Permissions
user = Permission(to_sign_in)
user.description = "User's permissions"
editor = Permission(be_editor)
editor.description = "Editor's permissions"
admin = Permission(be_admin)
admin.description = "Admin's permissions"

apps_needs = [be_admin, be_editor, to_sign_in]
apps_permissions = [user, editor, admin]

def current_privileges():
    return (('{method} : {value}').format(method=n.method, value=n.value)
            for n in apps_needs if n in g.identity.provides)

# Simple user class base on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin
class User(UserMixin):
    '''Simple User class'''
    USERS = {
        # username: password
        'john': 'pass1',
        'mary': 'pass2',
        'peter': 'pass3'
    }

    ROLES = {
        # username: role
        'john': 'admin',
        'mary': 'user',
        'peter': 'editor'
    }



    def __init__(self, id):
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]
        self.roles=self.ROLES[id]


    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None


@mod_auth.route('/')
def index():
    return render_template('auth/index.html',priv=current_privileges())

@mod_auth.route('/login')
def login():
    if current_user.is_authenticated():
        return redirect(url_for('.index'))
    return render_template('auth/login.html')


@mod_auth.route('/login/check', methods=['post'])
def login_check():
    # validate username and password
    user = User.get(request.form['username'])
    if (user and user.password == request.form['password']):
        login_user(user)
        identity_changed.send(current_app._get_current_object(),identity=Identity(user.roles))
    else:
        flash('Username or password incorrect')

    return render_template('auth/index.html')


@mod_auth.route('/logout')
def logout():
    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('.index'))

@mod_auth.route('/admin')
@admin.require(http_exception=403)
def admin():
    return render_template('auth/admin.html')


@mod_auth.route('/edit')
@editor.require(http_exception=403)
def editor():
    return render_template('auth/editor.html')


@mod_auth.route('/about')
def about():
    return render_template('auth/about.html')



@mod_auth.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('login'))


@mod_auth.errorhandler(403)
def authorisation_failed(e):
    flash(('Your current identity is {id}. You need special privileges to'
           ' access this page').format(id=g.identity.id))

    return render_template('auth/privileges.html', priv=current_privileges())

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    needs = []

    if identity.id in ('user', 'editor', 'admin'):
        needs.append(to_sign_in)

    if identity.id in ('editor', 'admin'):
        needs.append(be_editor)

    if identity.id == 'admin':
        needs.append(be_admin)


    for n in needs:
        g.identity.provides.add(n)
