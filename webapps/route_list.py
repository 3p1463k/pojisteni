from webapps.auth import route_login
from webapps.auth import route_logout
from webapps.routes import route_about
from webapps.routes import route_home
from webapps.routes import route_kontakt
from webapps.routes import route_registrace
from webapps.routes import route_ucet
from webapps.routes import route_zalozit_pojisteni
from webapps.routes import route_zalozit_udalost


routes_list = [
    route_login.router,
    route_logout.router,
    route_home.router,
    route_kontakt.router,
    route_about.router,
    route_registrace.router,
    route_ucet.router,
    route_zalozit_pojisteni.router,
    route_zalozit_udalost.router,
]
