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
        title='Persona 5',
        description='Estilazo.',
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
    game3 = Game(
        title='Persona 3',
        description='Simplemente persona 3',
        price=59.99,
        release_date=date(2024, 2, 1),
        developer='MythosGames',
        genre=rpg,
        stock=30,
        image_game_url='https://image.api.playstation.com/vulcan/ap/rnd/202307/2605/7b70e463bf05b20fbf99f8bf81956aa805969da98d9dcde8.jpg'
    )
    game4 = Game(
        title='Persona4',
        description="The best person's game",
        price=29.99,
        release_date=date(2024, 2, 1),
        developer='MythosGames',
        genre=rpg,
        stock=30,
        image_game_url='https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1113000/capsule_616x353.jpg?t=1704380046'
    )
    game5 = Game(
        title='Naruto Ultima Ninja Stomr',
        description='Naruto game',
        price=35.99,
        release_date=date(2024, 2, 1),
        developer='MythosGames',
        genre=rpg,
        stock=30,
        image_game_url='https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/349040/capsule_616x353.jpg?t=1703080866'
    )
    db.session.add_all([game1, game2, game3, game4, game5])

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
