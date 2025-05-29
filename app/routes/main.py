from flask import Blueprint, render_template
from app.models import Game, Genre, User
from app.routes.auth import login 
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm


main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    user = User.query.all()
    return render_template('index.html', user=user)

@main.route('/base')
def base():
    user = User.query.all()
    return render_template('base.html', user=user)

@main.route('/games')
@login_required
def games():
    all_games = Game.query.all()
    all_genre = Genre.query.all()
    return render_template('games.html', games=all_games, genre=all_genre)