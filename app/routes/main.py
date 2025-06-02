from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from app.models import Game, Genre, User, Purchase, PurchaseDetail
from app.routes.auth import login 
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm


main = Blueprint('main', __name__)

@main.route('/')
@login_required
def games():
    all_games = Game.query.all()
    all_genre = Genre.query.all()
    
    cart_item_count = 0
    if current_user.is_authenticated:
        cart = Purchase.query.filter_by(user_id=current_user.id, is_active=True).first()
        if cart and cart.details:
            cart_item_count = sum(detail.quantity for detail in cart.details)
    return render_template('games.html', games=all_games, genre=all_genre, cart_item_count=cart_item_count)



@main.route('/library')
@login_required
def library():
    # Obtener compras finalizadas
    purchases = Purchase.query.filter_by(user_id=current_user.id, is_active=False).all()
    
    # Obtener todos los detalles de esas compras
    library_items = []
    for purchase in purchases:
        for detail in purchase.details:
            library_items.append({
                "title": detail.game.title,
                "purchased_at": purchase.purchased_at,
                "image_url": detail.game.image_game_url
            })

    return render_template('library.html', items=library_items)
