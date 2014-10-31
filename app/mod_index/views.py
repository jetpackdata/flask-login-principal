from flask import g, Flask, flash, redirect, url_for, request, get_flashed_messages, current_app, session, render_template
from . import mod_index

@mod_index.route('/')
def index():
    return render_template('auth/index.html')
