from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Header, APIRouter
from fastapi.staticfiles import StaticFiles

from apis.base import api_router
from webapps.base import api_router as web_app_router

from db.session import engine
from db.base import Base

from core.config import settings

#from sqladmin import Admin, ModelView
#from admin.admin_auth import AdminAuthBackend
#from admin.admin_config import PojistenecAdmin, PojisteniAdmin, UdalostAdmin

#from static.script.vytvor_polozky_db import over_admina, zadej_admina
#from static.script.vytvor_polozky_db import vytvor_dummy_pojistence, vytvor_dummy_pojisteni


def include_router(app):

    """Include APIs and WebAps routers"""

    app.include_router(api_router)
    app.include_router(web_app_router)


def configure_static(app):

    """Configure static folder and docs folder"""

    app.mount(
        "/static",
        StaticFiles(directory="static"),
        name="static"
    )

    app.mount(
        "/documentation",
        StaticFiles(directory="documentation", html=True),
        name="documentation"
    )


def create_tables():

    """Create tables"""
    print("create_tables")
    Base.metadata.create_all(bind=engine)


def start_application():

    app = FastAPI(

        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION
    )

    #print("addding sqladmin to /admin")
    #authentication_backend = AdminAuthBackend(secret_key=settings.SECRET_KEY)

    #admin = Admin(app, engine, authentication_backend=authentication_backend)

    include_router(app)
    configure_static(app)
    create_tables()
    #admin.add_view(PojistenecAdmin)
    #admin.add_view(PojisteniAdmin)
    #admin.add_view(UdalostAdmin)
    #zadej_admina()
    #vytvor_dummy_pojistence()
    #over_admina()
    #vytvor_dummy_pojisteni()

    return app

app = start_application()
