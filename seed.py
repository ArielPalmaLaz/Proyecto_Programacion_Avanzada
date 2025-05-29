from app import create_app, db
from app.models import User, Genre, Game, Purchase, PurchaseDetail
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Crear géneros
    action = Genre(name='Action')
    rpg = Genre(name='RPG')
    strategy = Genre(name='Strategy')
    db.session.add_all([action, rpg, strategy])

    # Crear videojuegos con imagen
    game1 = Game(
        title='Space Warriors',
        description='Futuristic space battle game.',
        price=29.99,
        release_date=date(2023, 5, 10),
        developer='NovaCorp',
        genre=action,
        stock=50,
        image_game_url='https://image.api.playstation.com/vulcan/ap/rnd/202209/0708/kpdkl075Ikcx8C9P5Y1pBbH2.jpg'  # Ruta relativa a /static/
    )
    game2 = Game(
        title='Dragon Legends',
        description='Epic dragon fantasy RPG.',
        price=49.99,
        release_date=date(2024, 2, 1),
        developer='MythosGames',
        genre=rpg,
        stock=30,
        image_game_url='https://image.api.playstation.com/vulcan/ap/rnd/202209/0708/kpdkl075Ikcx8C9P5Y1pBbH2.jpg'
    )
    db.session.add_all([game1, game2])

    # Crear usuario
    user1 = User(name='Alice Smith', email='alice@example.com', password='hashed_password')
    db.session.add(user1)

    # Crear compra
    purchase = Purchase(user=user1, total_amount=79.98)
    db.session.add(purchase)

    # Detalle de compra
    detail1 = PurchaseDetail(purchase=purchase, game=game1, unit_price=29.99, quantity=1)
    detail2 = PurchaseDetail(purchase=purchase, game=game2, unit_price=49.99, quantity=1)
    db.session.add_all([detail1, detail2])

    db.session.commit()
    print("✅ Datos de prueba con imágenes insertados con éxito.")
