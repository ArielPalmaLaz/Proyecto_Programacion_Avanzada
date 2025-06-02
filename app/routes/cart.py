from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app.models import db, Game, Purchase, PurchaseDetail
from decimal import Decimal
from sqlalchemy.orm import joinedload

cart = Blueprint('cart', __name__)

def get_or_create_cart(user_id):
    cart = Purchase.query.filter_by(user_id=user_id, is_active=True).first()
    if not cart:
        cart = Purchase(user_id=user_id, total_amount=0, is_active=True)
        db.session.add(cart)
        db.session.commit()
    return cart

@cart.route('/add_to_cart/<int:game_id>')
@login_required
def add_to_cart(game_id):
    game = Game.query.get_or_404(game_id)

    # Verifica si el juego ya está en alguna compra finalizada
    purchased = db.session.query(PurchaseDetail).join(Purchase).filter(
        Purchase.user_id == current_user.id,
        Purchase.is_active == False,
        PurchaseDetail.game_id == game.id
    ).first()

    if purchased:
        flash("❗ Ya has comprado este juego.", "warning")
        return redirect(url_for('main.games'))

    # Verifica si ya está en el carrito actual
    active_purchase = Purchase.query.filter_by(user_id=current_user.id, is_active=True).first()

    if active_purchase:
        detail = PurchaseDetail.query.filter_by(purchase_id=active_purchase.id, game_id=game.id).first()
        if detail:
            flash("❗ Este juego ya está en tu carrito.", "warning")
            return redirect(url_for('main.games'))
    else:
        # Crea carrito si no existe
        active_purchase = Purchase(user_id=current_user.id, total_amount=0)
        db.session.add(active_purchase)
        db.session.commit()

    # Agrega el juego al carrito
    new_detail = PurchaseDetail(
        purchase_id=active_purchase.id,
        game_id=game.id,
        unit_price=game.price,
        quantity=1
    )
    active_purchase.total_amount += game.price
    db.session.add(new_detail)
    db.session.commit()

    flash(f"{game.title} agregado al carrito.", "success")
    return redirect(url_for('main.games'))

@cart.route('/cart')
@login_required
def view_cart():
    cart = Purchase.query.options(
        joinedload(Purchase.details).joinedload(PurchaseDetail.game)
    ).filter_by(user_id=current_user.id, is_active=True).first()

    if not cart or not cart.details:
        return render_template('cart/view_cart.html', items=[], total=0)

    total = sum(detail.unit_price * detail.quantity for detail in cart.details)
    return render_template('cart/view_cart.html', items=cart.details, total=total)


@cart.route('/checkout')
@login_required
def checkout():
    active_purchase = Purchase.query.filter_by(user_id=current_user.id, is_active=True).first()
    
    if not active_purchase or not active_purchase.details:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart.view_cart'))

    # Calcular el total
    total = sum([detail.unit_price * detail.quantity for detail in active_purchase.details])

    # Marcar la compra como finalizada
    active_purchase.total_amount = total
    active_purchase.is_active = False
    db.session.commit()

    flash("Purchase completed successfully! 🎉", "success")
    return redirect(url_for('main.games'))  # o a una vista de historial de compras

@cart.route('/remove_from_cart/<int:detail_id>')
@login_required
def remove_from_cart(detail_id):
    detail = PurchaseDetail.query.options(joinedload(PurchaseDetail.game)).get(detail_id)

    # Verifica que el detalle pertenezca al usuario actual
    if detail.purchase.user_id != current_user.id or not detail.purchase.is_active:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('cart.view_cart'))

    db.session.delete(detail)
    db.session.commit()
    flash(f"Removed {detail.game.title} from cart.", "success") 
    return redirect(url_for('cart.view_cart'))
