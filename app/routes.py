from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required 
from . import db, bcrypt
from .models import Usuario
from functools import wraps
from flask_login import current_user
from flask import abort

def rol_requerido(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('main.login'))
            if current_user.rol not in roles:
                abort(403)
                return f(*args, **kwargs)
            return decorated_function
        return decorator

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and bcrypt.check_password_hash(usuario.password, password):
            login_user(usuario)
            return redirect(url_for('main.dashboard'))
        else:
            flash('email o contraseña incorrectos', 'error')
            
    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return f'Bienvenido {current_user.nombre} - Rol: {current_user.rol}'

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))






