from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Header
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from sqladmin import ModelView
from sqlmodel import Session

from admin.admin_auth import AdminAuthBackend
from admin.admin_config import DruhPojisteniAdmin
from admin.admin_config import PojistenecAdmin
from admin.admin_config import PojisteniAdmin
from admin.admin_config import UdalostAdmin
from apis.base import api_router
from core.config import settings
from db.session import create_db_and_tables
from db.session import engine
from static.script.exceptions import exception_handlers
from static.script.vytvor_polozky_db import vytvor_dummy_pojistence
from static.script.vytvor_polozky_db import vytvor_dummy_pojisteni
from static.script.vytvor_polozky_db import zadej_admina
from webapps.base import api_router as web_app_router


def include_router(app):

    """Include APIs and WebAps routers"""

    app.include_router(api_router)
    app.include_router(web_app_router)


def configure_static(app):

    """Configure static folder and docs folder"""

    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        exception_handlers=exception_handlers,
    )

    authentication_backend = AdminAuthBackend(secret_key=settings.SECRET_KEY)
    admin = Admin(app, engine, authentication_backend=authentication_backend)

    include_router(app)
    configure_static(app)
    create_db_and_tables()

    admin.add_view(PojistenecAdmin)
    admin.add_view(PojisteniAdmin)
    admin.add_view(UdalostAdmin)
    admin.add_view(DruhPojisteniAdmin)

    # zadej_admina()
    vytvor_dummy_pojistence()
    vytvor_dummy_pojisteni()

    return app


app = start_application()
