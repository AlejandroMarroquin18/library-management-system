from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Autor, Categoria, Editorial, Libro


CATEGORIES = [
    ('Narrativa', 'Novelas y relatos de ficción para todos los lectores.'),
    ('Ciencia ficción', 'Historias sobre futuros posibles, tecnología y sociedad.'),
    ('Fantasía', 'Mundos imaginarios, aventuras y mitologías.'),
    ('Ensayo', 'Ideas, análisis y pensamiento crítico.'),
    ('Historia', 'Obras sobre acontecimientos y procesos históricos.'),
    ('Ciencias', 'Divulgación científica y conocimiento del mundo natural.'),
]

AUTHORS = [
    {
        'nombre': 'Gabriel', 'apellido': 'García Márquez',
        'pais': 'Colombia', 'fecha_nacimiento': date(1927, 3, 6),
        'biografia': 'Escritor y periodista colombiano, ganador del Premio Nobel de Literatura en 1982.',
    },
    {
        'nombre': 'Jane', 'apellido': 'Austen',
        'pais': 'Reino Unido', 'fecha_nacimiento': date(1775, 12, 16),
        'biografia': 'Novelista inglesa reconocida por sus observaciones sobre la sociedad y las relaciones humanas.',
    },
    {
        'nombre': 'Julio', 'apellido': 'Cortázar',
        'pais': 'Argentina', 'fecha_nacimiento': date(1914, 8, 26),
        'biografia': 'Escritor argentino, una de las figuras centrales del boom de la literatura latinoamericana.',
    },
    {
        'nombre': 'Ursula K.', 'apellido': 'Le Guin',
        'pais': 'Estados Unidos', 'fecha_nacimiento': date(1929, 10, 21),
        'biografia': 'Autora estadounidense de ciencia ficción y fantasía, destacada por su exploración de la cultura y el poder.',
    },
    {
        'nombre': 'Antoine de', 'apellido': 'Saint-Exupéry',
        'pais': 'Francia', 'fecha_nacimiento': date(1900, 6, 29),
        'biografia': 'Escritor y aviador francés, autor de una de las obras más queridas de la literatura universal.',
    },
    {
        'nombre': 'Yuval Noah', 'apellido': 'Harari',
        'pais': 'Israel', 'fecha_nacimiento': date(1976, 2, 24),
        'biografia': 'Historiador y escritor conocido por sus ensayos de divulgación sobre la historia de la humanidad.',
    },
    {
        'nombre': 'Isabel', 'apellido': 'Allende',
        'pais': 'Chile', 'fecha_nacimiento': date(1942, 8, 2),
        'biografia': 'Escritora chilena, autora de novelas que combinan memoria familiar, historia y realismo mágico.',
    },
    {
        'nombre': 'George', 'apellido': 'Orwell',
        'pais': 'Reino Unido', 'fecha_nacimiento': date(1903, 6, 25),
        'biografia': 'Escritor y ensayista británico, conocido por sus novelas de crítica política y social.',
    },
    {
        'nombre': 'Mary', 'apellido': 'Shelley',
        'pais': 'Reino Unido', 'fecha_nacimiento': date(1797, 8, 30),
        'biografia': 'Novelista inglesa cuya obra Frankenstein es considerada una pieza fundacional de la ciencia ficción.',
    },
    {
        'nombre': 'Jorge Luis', 'apellido': 'Borges',
        'pais': 'Argentina', 'fecha_nacimiento': date(1899, 8, 24),
        'biografia': 'Escritor argentino de cuentos, poemas y ensayos sobre laberintos, memoria e infinitos.',
    },
    {
        'nombre': 'Mary Oliver', 'apellido': 'Oliver',
        'pais': 'Estados Unidos', 'fecha_nacimiento': date(1935, 9, 10),
        'biografia': 'Poeta estadounidense reconocida por su mirada contemplativa sobre la naturaleza y la vida cotidiana.',
    },
    {
        'nombre': 'Carl', 'apellido': 'Sagan',
        'pais': 'Estados Unidos', 'fecha_nacimiento': date(1934, 11, 9),
        'biografia': 'Astrónomo y divulgador científico que acercó la exploración del cosmos a millones de lectores.',
    },
    {
        'nombre': 'Umberto', 'apellido': 'Eco',
        'pais': 'Italia', 'fecha_nacimiento': date(1932, 1, 5),
        'biografia': 'Escritor, filósofo y semiólogo italiano, autor de novelas históricas y ensayos sobre cultura.',
    },
    {
        'nombre': 'Harper', 'apellido': 'Lee',
        'pais': 'Estados Unidos', 'fecha_nacimiento': date(1926, 4, 28),
        'biografia': 'Escritora estadounidense cuya obra abordó la justicia racial y la pérdida de la inocencia.',
    },
    {
        'nombre': 'Margaret', 'apellido': 'Atwood',
        'pais': 'Canadá', 'fecha_nacimiento': date(1939, 11, 18),
        'biografia': 'Escritora canadiense de narrativa y poesía, reconocida por sus ficciones especulativas.',
    },
    {
        'nombre': 'Stephen', 'apellido': 'Hawking',
        'pais': 'Reino Unido', 'fecha_nacimiento': date(1942, 1, 8),
        'biografia': 'Físico teórico y divulgador británico especializado en cosmología y agujeros negros.',
    },
    {
        'nombre': 'Carlos Ruiz', 'apellido': 'Zafón',
        'pais': 'España', 'fecha_nacimiento': date(1964, 9, 25),
        'biografia': 'Escritor español conocido por sus novelas ambientadas en una Barcelona literaria y misteriosa.',
    },
]

PUBLISHERS = [
    ('Penguin Clásicos', 'Reino Unido', 'https://www.penguin.co.uk/'),
    ('Editorial Sudamericana', 'Argentina', 'https://www.penguinlibros.com/'),
    ('Minotauro', 'España', 'https://www.planetadelibros.com/'),
    ('Salamandra', 'España', 'https://www.penguinlibros.com/'),
    ('Debate', 'España', 'https://www.penguinlibros.com/'),
]

BOOKS = [
    {
        'titulo': 'Cien años de soledad', 'isbn': '9780307474728',
        'fecha_publicacion': date(1967, 5, 30), 'precio_compra': '22.90',
        'precio_alquiler': '5.90', 'stock': 12, 'autor': ('Gabriel', 'García Márquez'),
        'editorial': 'Editorial Sudamericana', 'categoria': 'Narrativa',
        'descripcion': 'La saga de la familia Buendía en el pueblo imaginario de Macondo, entre memoria, amor y realismo mágico.',
    },
    {
        'titulo': 'Orgullo y prejuicio', 'isbn': '9780141439518',
        'fecha_publicacion': date(1813, 1, 28), 'precio_compra': '16.50',
        'precio_alquiler': '4.50', 'stock': 8, 'autor': ('Jane', 'Austen'),
        'editorial': 'Penguin Clásicos', 'categoria': 'Narrativa',
        'descripcion': 'Elizabeth Bennet y Fitzwilliam Darcy deberán enfrentarse a sus prejuicios antes de reconocer sus sentimientos.',
    },
    {
        'titulo': 'Rayuela', 'isbn': '9788420437484',
        'fecha_publicacion': date(1963, 6, 28), 'precio_compra': '21.90',
        'precio_alquiler': '5.50', 'stock': 7, 'autor': ('Julio', 'Cortázar'),
        'editorial': 'Editorial Sudamericana', 'categoria': 'Narrativa',
        'descripcion': 'Una novela abierta y experimental que sigue a Horacio Oliveira entre París y Buenos Aires.',
    },
    {
        'titulo': 'La mano izquierda de la oscuridad', 'isbn': '9780441478125',
        'fecha_publicacion': date(1969, 3, 1), 'precio_compra': '19.90',
        'precio_alquiler': '5.00', 'stock': 6, 'autor': ('Ursula K.', 'Le Guin'),
        'editorial': 'Minotauro', 'categoria': 'Ciencia ficción',
        'descripcion': 'Un enviado interestelar llega a un planeta cuyos habitantes pueden cambiar de género.',
    },
    {
        'titulo': 'El principito', 'isbn': '9780156012195',
        'fecha_publicacion': date(1943, 4, 6), 'precio_compra': '14.90',
        'precio_alquiler': '3.90', 'stock': 15, 'autor': ('Antoine de', 'Saint-Exupéry'),
        'editorial': 'Salamandra', 'categoria': 'Fantasía',
        'descripcion': 'Un piloto conoce en el desierto a un pequeño viajero que le revela una forma distinta de mirar el mundo.',
    },
    {
        'titulo': 'Sapiens: De animales a dioses', 'isbn': '9780062316097',
        'fecha_publicacion': date(2011, 1, 1), 'precio_compra': '24.90',
        'precio_alquiler': '6.50', 'stock': 9, 'autor': ('Yuval Noah', 'Harari'),
        'editorial': 'Debate', 'categoria': 'Historia',
        'descripcion': 'Un recorrido por las revoluciones que transformaron a Homo sapiens en la especie dominante del planeta.',
    },
    {
        'titulo': 'La casa de los espíritus', 'isbn': '9781501117015',
        'fecha_publicacion': date(1982, 1, 1), 'precio_compra': '21.50',
        'precio_alquiler': '5.50', 'stock': 10, 'autor': ('Isabel', 'Allende'),
        'editorial': 'Salamandra', 'categoria': 'Narrativa',
        'descripcion': 'Una saga familiar atravesada por la historia política de un país latinoamericano y por fuerzas sobrenaturales.',
    },
    {
        'titulo': '1984', 'isbn': '9780451524935',
        'fecha_publicacion': date(1949, 6, 8), 'precio_compra': '15.90',
        'precio_alquiler': '4.20', 'stock': 11, 'autor': ('George', 'Orwell'),
        'editorial': 'Penguin Clásicos', 'categoria': 'Ensayo',
        'descripcion': 'Una sociedad vigilada por el Gran Hermano convierte la libertad, la memoria y el lenguaje en actos de resistencia.',
    },
    {
        'titulo': 'Rebelión en la granja', 'isbn': '9780451526342',
        'fecha_publicacion': date(1945, 8, 17), 'precio_compra': '13.90',
        'precio_alquiler': '3.90', 'stock': 9, 'autor': ('George', 'Orwell'),
        'editorial': 'Penguin Clásicos', 'categoria': 'Narrativa',
        'descripcion': 'Una fábula política sobre una revolución que transforma los ideales de igualdad en una nueva forma de poder.',
    },
    {
        'titulo': 'Frankenstein', 'isbn': '9780486282114',
        'fecha_publicacion': date(1818, 1, 1), 'precio_compra': '12.90',
        'precio_alquiler': '3.50', 'stock': 8, 'autor': ('Mary', 'Shelley'),
        'editorial': 'Penguin Clásicos', 'categoria': 'Ciencia ficción',
        'descripcion': 'Victor Frankenstein desafía los límites de la ciencia y debe afrontar las consecuencias de crear vida.',
    },
    {
        'titulo': 'Ficciones', 'isbn': '9780802130303',
        'fecha_publicacion': date(1944, 1, 1), 'precio_compra': '18.90',
        'precio_alquiler': '4.90', 'stock': 6, 'autor': ('Jorge Luis', 'Borges'),
        'editorial': 'Editorial Sudamericana', 'categoria': 'Narrativa',
        'descripcion': 'Cuentos fundamentales que exploran bibliotecas infinitas, mundos imaginarios y los límites de la realidad.',
    },
    {
        'titulo': 'El Aleph', 'isbn': '9788420633139',
        'fecha_publicacion': date(1949, 1, 1), 'precio_compra': '17.90',
        'precio_alquiler': '4.75', 'stock': 7, 'autor': ('Jorge Luis', 'Borges'),
        'editorial': 'Editorial Sudamericana', 'categoria': 'Narrativa',
        'descripcion': 'Relatos breves donde el tiempo, la identidad y el infinito aparecen bajo formas inesperadas.',
    },
    {
        'titulo': 'Cosmos', 'isbn': '9780345539434',
        'fecha_publicacion': date(1980, 1, 1), 'precio_compra': '25.90',
        'precio_alquiler': '6.90', 'stock': 5, 'autor': ('Carl', 'Sagan'),
        'editorial': 'Debate', 'categoria': 'Ciencias',
        'descripcion': 'Un viaje por la historia de la ciencia, la evolución y la inmensidad del universo.',
    },
    {
        'titulo': 'El nombre de la rosa', 'isbn': '9780156001311',
        'fecha_publicacion': date(1980, 1, 1), 'precio_compra': '20.90',
        'precio_alquiler': '5.25', 'stock': 8, 'autor': ('Umberto', 'Eco'),
        'editorial': 'Salamandra', 'categoria': 'Historia',
        'descripcion': 'Una investigación detectivesca en una abadía medieval entre manuscritos, secretos y disputas teológicas.',
    },
    {
        'titulo': 'Matar a un ruiseñor', 'isbn': '9780060935467',
        'fecha_publicacion': date(1960, 7, 11), 'precio_compra': '18.50',
        'precio_alquiler': '4.90', 'stock': 10, 'autor': ('Harper', 'Lee'),
        'editorial': 'Penguin Clásicos', 'categoria': 'Narrativa',
        'descripcion': 'Una niña observa cómo su comunidad afronta el racismo y la injusticia a través del juicio de un hombre inocente.',
    },
    {
        'titulo': 'El cuento de la criada', 'isbn': '9780385490818',
        'fecha_publicacion': date(1985, 1, 1), 'precio_compra': '19.50',
        'precio_alquiler': '5.10', 'stock': 7, 'autor': ('Margaret', 'Atwood'),
        'editorial': 'Salamandra', 'categoria': 'Ciencia ficción',
        'descripcion': 'En una teocracia autoritaria, una mujer lucha por conservar su identidad y recuperar su libertad.',
    },
    {
        'titulo': 'Breves respuestas a las grandes preguntas', 'isbn': '9788491990221',
        'fecha_publicacion': date(2018, 10, 16), 'precio_compra': '22.50',
        'precio_alquiler': '5.90', 'stock': 6, 'autor': ('Stephen', 'Hawking'),
        'editorial': 'Debate', 'categoria': 'Ciencias',
        'descripcion': 'Reflexiones accesibles sobre el universo, el futuro de la humanidad y los grandes misterios de la ciencia.',
    },
    {
        'titulo': 'La sombra del viento', 'isbn': '9788408172175',
        'fecha_publicacion': date(2001, 1, 1), 'precio_compra': '21.90',
        'precio_alquiler': '5.50', 'stock': 9, 'autor': ('Carlos Ruiz', 'Zafón'),
        'editorial': 'Salamandra', 'categoria': 'Narrativa',
        'descripcion': 'Un joven descubre un libro maldito en la Barcelona de la posguerra y emprende una búsqueda literaria.',
    },
]


class Command(BaseCommand):
    help = 'Crea o actualiza un catálogo de demostración realista e idempotente.'

    def handle(self, *args, **options):
        categories = {}
        for name, description in CATEGORIES:
            categories[name], _ = Categoria.objects.update_or_create(
                nombre=name,
                defaults={'descripcion': description},
            )

        authors = {}
        for data in AUTHORS:
            lookup = {'nombre': data['nombre'], 'apellido': data['apellido']}
            authors[data['nombre'], data['apellido']], _ = Autor.objects.update_or_create(
                **lookup,
                defaults=data,
            )

        publishers = {}
        for name, country, website in PUBLISHERS:
            publishers[name], _ = Editorial.objects.update_or_create(
                nombre=name,
                defaults={'pais': country, 'sitio_web': website},
            )

        created_books = 0
        updated_books = 0
        for data in BOOKS:
            data['precio_compra'] = Decimal(data['precio_compra']) * 1000
            data['precio_alquiler'] = Decimal(data['precio_alquiler']) * 1000
            book_data = {
                **data,
                'autor': authors[data.pop('autor')],
                'editorial': publishers[data.pop('editorial')],
                'categoria': categories[data.pop('categoria')],
                'disponible': True,
            }
            _, created = Libro.objects.update_or_create(
                isbn=data['isbn'],
                defaults=book_data,
            )
            if created:
                created_books += 1
            else:
                updated_books += 1

        self.stdout.write(self.style.SUCCESS(
            f'Catálogo listo: {len(categories)} categorías, {len(authors)} autores, '
            f'{len(publishers)} editoriales y {created_books + updated_books} libros '
            f'({created_books} nuevos, {updated_books} actualizados).'
        ))
