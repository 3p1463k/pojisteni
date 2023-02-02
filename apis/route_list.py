from apis.version1.routes import route_druh_pojisteni
from apis.version1.routes import route_login
from apis.version1.routes import route_pojistence
from apis.version1.routes import route_pojisteni
from apis.version1.routes import route_udalosti


routes_list = [
    route_login.login_router,
    route_pojisteni.router,
    route_pojistence.router,
    route_udalosti.router,
    route_druh_pojisteni.router,
]
