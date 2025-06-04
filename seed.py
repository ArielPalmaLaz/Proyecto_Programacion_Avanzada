from app import create_app, db
from app.models import User, Genre, Game, Purchase, PurchaseDetail
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Crear géneros
    action = Genre(name='Accion')
    rpg = Genre(name='RPG')
    strategy = Genre(name='Estrategia')
    history = Genre(name='Historia')
    
    db.session.add_all([action, rpg, strategy])

    # Crear videojuegos con imagen
    game1 = Game(
        title='Persona 5 Royal',
        description='Ponte la máscara, acompaña a los Ladrones Fantasma de Corazones en sus asaltos ¡e infíltrate en la mente de los corruptos para hacerles cambiar de opinión!',
        price=29.99,
        release_date=date(2022, 5, 10),
        developer='ATLUS',
        genre=rpg,
        stock=50,
        image_game_url='https://image.api.playstation.com/vulcan/ap/rnd/202209/0708/kpdkl075Ikcx8C9P5Y1pBbH2.jpg'  # Ruta relativa a /static/
    )
    game2 = Game(
        title='Red Dead Redemtion 2',
        description='Con más de 175 premios al Juego del año y más de 250 valoraciones perfectas, Red Dead Redemption 2 es la épica historia de Arthur Morgan y la banda de Van der Linde, que huyen por Estados Unidos en los albores del siglo XX. También incluye acceso al mundo multijugador compartido de Red Dead Online.',
        price=49.99,
        release_date=date(2024, 2, 1),
        developer='RockStar',
        genre=history,
        stock=30,
        image_game_url='https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/1174180/header.jpg?t=1720558643'
    )
    game3 = Game(
        title='Persona 3 Reload',
        description='Sumérgete en la Hora Oscura y despierta lo más profundo de tu corazón. Persona 3 Reload es la fascinante nueva versión del RPG que definió el género y que ahora renace para la era moderna con gráficos y una jugabilidad de última generación',
        price=59.99,
        release_date=date(2024, 2, 1),
        developer='ATLUS',
        genre=rpg,
        stock=30,
        image_game_url='https://image.api.playstation.com/vulcan/ap/rnd/202307/2605/7b70e463bf05b20fbf99f8bf81956aa805969da98d9dcde8.jpg'
    )
    game4 = Game(
        title='Persona 4 Golden',
        description="Una historia de juventud en la que el protagonista y sus amigos se embarcan en una aventura a raíz de una serie de asesinatos",
        price=29.99,
        release_date=date(2020, 6, 7),
        developer='ATLUS',
        genre=rpg,
        stock=30,
        image_game_url='https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1113000/capsule_616x353.jpg?t=1704380046'
    )
    game5 = Game(
        title='NARUTO SHIPPUDEN: Ultimate Ninja STORM 4',
        description='¡Con el nuevo título de la aclamada saga STORM emprenderás un viaje impresionante y lleno de color! ¡Benefíciate de un sistema de combate totalmente renovado y prepárate para sumergirte en los combates más épicos que hayas visto nunca!',
        price=35.99,
        release_date=date(2024, 2, 1),
        developer='CyberConnect2',
        genre=action,
        stock=30,
        image_game_url='https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/349040/capsule_616x353.jpg?t=1703080866'
    )
    game6 = Game(
        title='Elden Ring',
        description='EL NUEVO RPG DE ACCIÓN DE FANTASÍA. Levántate, tiznado, y déjate guiar por la gracia para esgrimir el poder del Anillo de Elden y convertirte en un Señor de Elden en las Tierras Intermedias.',
        price=35.99,
        release_date=date(2024, 2, 1),
        developer='FROMSOFWARE',
        genre=rpg,
        stock=30,
        image_game_url='https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/1245620/header.jpg?t=1748630546'
    )
    db.session.add_all([game1, game2, game3, game4, game5, game6])

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
    print("Datos de prueba con imágenes insertados con éxito.")
