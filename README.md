# Library Management System

Sistema web desarrollado con Django para la gestión de una biblioteca con venta y préstamo de libros.

## Tecnologías

- Python
- Django
- PostgreSQL
- HTML
- CSS
- Bootstrap

## Funcionalidades

- Catálogo público
- Registro e inicio de sesión
- Compra de libros
- Préstamo de libros
- Panel administrativo

## Login con Google

La autenticación social usa `django-allauth`. Crea credenciales OAuth 2.0 en Google Cloud con el callback:

`http://localhost:8000/accounts/google/login/callback/`

Configura `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` en el entorno. En producción, usa el dominio HTTPS correspondiente y no guardes credenciales en el repositorio.

En el panel de administración crea una **Social application** con proveedor `Google`, pega el Client ID y Client Secret, y asígnala al sitio `localhost:8000` (en producción, al dominio correspondiente). Las variables de entorno configuran el proveedor, pero allauth necesita también este registro en la base de datos.

El checkout actual registra y confirma la orden dentro de una transacción, pero no procesa un cobro real mediante una pasarela.

## Datos de demostración

Para cargar un catálogo realista de demostración ejecuta desde `library_management_system/`:

`python manage.py seed_catalog`

El comando es idempotente: crea o actualiza categorías, autores, editoriales y libros usando sus nombres e ISBN, sin duplicarlos al repetirlo.