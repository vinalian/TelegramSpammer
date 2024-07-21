import os
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from django.core.asgi import get_asgi_application
from .settings import STATIC_ROOT, MEDIA_ROOT

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

application = get_asgi_application()

app = Starlette(debug=True, routes=[
    Mount('/static', StaticFiles(directory=STATIC_ROOT), name='/static/'),
    Mount('/media', StaticFiles(directory=MEDIA_ROOT), name='/media/'),
    Mount('/', application)
])
