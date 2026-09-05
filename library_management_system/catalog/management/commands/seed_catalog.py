from datetime import date

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
