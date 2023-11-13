from flask import Blueprint, render_template, redirect,url_for ,request,flash
from . import db
from .models import  User, Category, Product, Cart,CartItem,Order,OrderItem
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .admin_views import admin_views
from .user_views import user_views,admin_username


authentication = Blueprint("authentication",__name__)

#login section
@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if request.form.get('register') == 'true':
            if User.query.filter_by(username=username).first():
                flash('Username already exists. Please choose a different username.', 'error')
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user) 
                db.session.commit()
                login_user(new_user)  # Auto-login the newly registered user
                return redirect(url_for('user_views.home'))
            
        elif user and user.password == password:
            if user.username == admin_username:
                login_user(user)
                return redirect(url_for('admin_views.admin_home'))
            else:
                login_user(user)
                return redirect(url_for('user_views.home'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

# Routes
@authentication.route('/')
def index():
    return redirect(url_for('authentication.login'))


# route for logout
@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))