from sona.settings import settings

from .base import MiddlewareBase


middlewares = [
    MiddlewareBase.load_class(kls)() for kls in settings.SONA_MIDDLEWARE_CLASSES
]
